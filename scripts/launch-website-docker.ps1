param(
    [switch]$Foreground
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

function Test-IsAdministrator {
    if ($env:OS -ne "Windows_NT") {
        return $false
    }
    try {
        $currentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent()
        $principal = [Security.Principal.WindowsPrincipal]::new($currentIdentity)
        return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    }
    catch {
        return $false
    }
}

function Get-PrimaryLanIPv4 {
    $virtualPattern = '^(Loopback|vEthernet|Hyper-V|WSL|Default Switch|Bluetooth|VirtualBox|VMware)'
    $routes = @(Get-NetRoute -DestinationPrefix "0.0.0.0/0" -AddressFamily IPv4 -ErrorAction SilentlyContinue |
        Sort-Object RouteMetric, InterfaceMetric)
    foreach ($route in $routes) {
        $addresses = @(Get-NetIPAddress -AddressFamily IPv4 -InterfaceIndex $route.InterfaceIndex -ErrorAction SilentlyContinue |
            Where-Object {
                $_.IPAddress -notlike "127.*" -and
                $_.IPAddress -notlike "169.254*" -and
                $_.ValidLifetime -ne ([TimeSpan]::Zero)
            } |
            Sort-Object SkipAsSource, PrefixLength -Descending)
        foreach ($address in $addresses) {
            $alias = [string]($address.InterfaceAlias)
            if ($alias -match $virtualPattern) {
                continue
            }
            return [pscustomobject]@{
                InterfaceAlias = $alias
                IPAddress = [string]$address.IPAddress
                PrefixLength = [int]$address.PrefixLength
            }
        }
    }

    $fallbacks = @(Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
        Where-Object {
            $_.IPAddress -notlike "127.*" -and
            $_.IPAddress -notlike "169.254*" -and
            $_.ValidLifetime -ne ([TimeSpan]::Zero) -and
            ([string]$_.InterfaceAlias) -notmatch $virtualPattern
        } |
        Sort-Object InterfaceMetric, SkipAsSource, PrefixLength)
    if ($fallbacks.Count -gt 0) {
        $selected = $fallbacks[0]
        return [pscustomobject]@{
            InterfaceAlias = [string]$selected.InterfaceAlias
            IPAddress = [string]$selected.IPAddress
            PrefixLength = [int]$selected.PrefixLength
        }
    }
    throw "Unable to determine a private LAN IPv4 address for website sharing."
}

function Ensure-LanFirewallRule {
    param(
        [string]$RuleName,
        [int]$Port,
        [string]$InterfaceAlias
    )

    if ($env:OS -ne "Windows_NT") {
        return [pscustomobject]@{
            configured = $false
            rule_name = $RuleName
            detail = "Firewall automation skipped: non-Windows host."
            requires_admin = $false
            lan_access_ready = $true
        }
    }

    $connectionProfiles = @()
    if (-not [string]::IsNullOrWhiteSpace($InterfaceAlias)) {
        $connectionProfiles = @(Get-NetConnectionProfile -InterfaceAlias $InterfaceAlias -ErrorAction SilentlyContinue)
    }
    $networkCategories = @($connectionProfiles | ForEach-Object { [string]$_.NetworkCategory } | Where-Object { $_ })
    $requiresPublicAccess = $networkCategories -contains "Public"

    $rule = Get-NetFirewallRule -DisplayName $RuleName -ErrorAction SilentlyContinue
    if ($null -ne $rule) {
        $portFilter = Get-NetFirewallPortFilter -AssociatedNetFirewallRule $rule -ErrorAction SilentlyContinue
        $addressFilter = Get-NetFirewallAddressFilter -AssociatedNetFirewallRule $rule -ErrorAction SilentlyContinue
        $hasMatchingPort = $false
        foreach ($filter in @($portFilter)) {
            if ([string]$filter.Protocol -eq "TCP" -and [string]$filter.LocalPort -eq [string]$Port) {
                $hasMatchingPort = $true
                break
            }
        }
        $remoteAddresses = @($addressFilter | ForEach-Object { [string]$_.RemoteAddress } | Where-Object { $_ })
        $hasLocalSubnetScope = $false
        foreach ($remoteAddress in $remoteAddresses) {
            if ($remoteAddress -match '(^|,)LocalSubnet($|,)') {
                $hasLocalSubnetScope = $true
                break
            }
        }
        $profileText = [string]$rule.Profile
        $profileSupportsCurrentNetwork = $profileText -match "Any"
        if (-not $profileSupportsCurrentNetwork -and $networkCategories.Count -gt 0) {
            foreach ($category in $networkCategories) {
                if ($profileText -match [regex]::Escape($category)) {
                    $profileSupportsCurrentNetwork = $true
                    break
                }
            }
        }
        if ($hasMatchingPort -and [string]$rule.Enabled -eq "True" -and $hasLocalSubnetScope -and $profileSupportsCurrentNetwork) {
            return [pscustomobject]@{
                configured = $true
                rule_name = $RuleName
                detail = "Existing LAN firewall rule is already configured."
                requires_admin = $false
                lan_access_ready = $true
            }
        }
    }

    if (-not (Test-IsAdministrator)) {
        $detail = "Firewall rule update skipped because this shell is not elevated. Local launch still works, but LAN access on port $Port may fail until an Administrator creates the LocalSubnet rule."
        if ($requiresPublicAccess) {
            $detail = "Firewall rule update skipped because this shell is not elevated and the active network is Public. Local launch still works, but same-network access on port $Port will usually fail until an Administrator creates the LocalSubnet rule."
        }
        return [pscustomobject]@{
            configured = $false
            rule_name = $RuleName
            detail = $detail
            requires_admin = $true
            lan_access_ready = $false
        }
    }

    if ($null -ne $rule) {
        Remove-NetFirewallRule -DisplayName $RuleName -ErrorAction Stop | Out-Null
    }

    New-NetFirewallRule `
        -DisplayName $RuleName `
        -Direction Inbound `
        -Action Allow `
        -Profile Any `
        -Protocol TCP `
        -LocalPort $Port `
        -RemoteAddress LocalSubnet `
        -EdgeTraversalPolicy Block | Out-Null

    return [pscustomobject]@{
        configured = $true
        rule_name = $RuleName
        detail = "Created LocalSubnet firewall rule for LAN access."
        requires_admin = $false
        lan_access_ready = $true
    }
}

function Wait-HttpOk {
    param(
        [string]$Url,
        [int]$TimeoutSeconds = 90
    )

    $curlExe = $null
    if ($env:OS -eq "Windows_NT") {
        $curlCmd = Get-Command "curl.exe" -ErrorAction SilentlyContinue
        if ($null -ne $curlCmd) {
            $curlExe = [string]$curlCmd.Source
        }
    }

    $deadline = (Get-Date).AddSeconds([math]::Max(1, $TimeoutSeconds))
    while ((Get-Date) -lt $deadline) {
        try {
            if ($Url -like "https://*" -and $curlExe) {
                $statusText = & $curlExe -k -L -s -o NUL -w "%{http_code}" $Url
                $statusCode = 0
                if ([int]::TryParse([string]$statusText, [ref]$statusCode) -and $statusCode -ge 200 -and $statusCode -lt 300) {
                    return
                }
            }
            else {
                $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5
                if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 300) {
                    return
                }
            }
        }
        catch {
            Start-Sleep -Milliseconds 500
            continue
        }
        Start-Sleep -Milliseconds 500
    }
    throw "Timed out waiting for $Url"
}

function Set-DefaultEnvValue {
    param(
        [string]$Name,
        [string]$Value
    )

    $existing = [Environment]::GetEnvironmentVariable($Name, "Process")
    if ([string]::IsNullOrWhiteSpace($existing)) {
        [Environment]::SetEnvironmentVariable($Name, $Value, "Process")
        return $Value
    }
    return $existing
}

function Get-DesktopActivityConfigPath {
    if ($env:OS -ne "Windows_NT") {
        return $null
    }
    $root = [string]$env:LOCALAPPDATA
    if ([string]::IsNullOrWhiteSpace($root)) {
        $root = [string]$env:TEMP
    }
    if ([string]::IsNullOrWhiteSpace($root)) {
        return $null
    }
    return Join-Path $root "EON-OpenSlicer\\cache\\activity_sync_config.json"
}

function Write-DesktopActivityConfig {
    param(
        [string]$BackendUrl,
        [string]$ServiceToken,
        [string]$MeUser = ""
    )

    $configPath = Get-DesktopActivityConfigPath
    if ([string]::IsNullOrWhiteSpace($configPath)) {
        return $null
    }

    $configDir = Split-Path -Parent $configPath
    if (-not [string]::IsNullOrWhiteSpace($configDir)) {
        New-Item -ItemType Directory -Force -Path $configDir | Out-Null
    }

    $payload = [ordered]@{
        version       = 1
        saved_at_utc  = (Get-Date).ToUniversalTime().ToString("o")
        base_url      = [string]($BackendUrl).TrimEnd("/")
        service_token = [string]$ServiceToken
        me_user       = [string]$MeUser
    }
    $payload | ConvertTo-Json -Depth 4 | Set-Content -Path $configPath -Encoding UTF8
    return $configPath
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$timestamp = Get-Date -Format "yyyyMMddTHHmmss"
$outputDir = Join-Path $env:TEMP "printnet_website_launch_$timestamp"
$firewallRuleName = "PrintNet Website Frontend 8080 (LAN Subnet)"
$previousEnv = @{}

foreach ($key in @(
    "BACKEND_OPERATOR_USER_IDS",
    "BACKEND_ACTIVITY_SERVICE_TOKEN",
    "BACKEND_SUPER_ADMIN_EMAIL",
    "BACKEND_SUPER_ADMIN_PASSWORD",
    "BACKEND_AUTH_EXPOSE_DEBUG_CODE",
    "BACKEND_AUTH_EMAIL_REQUIRE_SMTP",
    "BACKEND_AUTH_EMAIL_FROM",
    "BACKEND_SMTP_HOST",
    "BACKEND_SMTP_PORT",
    "BACKEND_SMTP_USERNAME",
    "BACKEND_SMTP_PASSWORD",
    "BACKEND_SMTP_STARTTLS",
    "BACKEND_SMTP_USE_SSL",
    "PRINTNET_API_BASE_URL",
    "PRINTNET_FRONTEND_SHARE_URL",
    "PRINTNET_TLS_COMMON_NAME",
    "PRINTNET_TLS_ALT_IP",
    "PRINTNET_TLS_ALT_DNS"
)) {
    $previousEnv[$key] = [Environment]::GetEnvironmentVariable($key, "Process")
}

Push-Location $repoRoot
try {
    $lanInfo = Get-PrimaryLanIPv4
    $firewallInfo = Ensure-LanFirewallRule -RuleName $firewallRuleName -Port 8080 -InterfaceAlias $lanInfo.InterfaceAlias

    $demoAdminEmail = Set-DefaultEnvValue -Name "BACKEND_SUPER_ADMIN_EMAIL" -Value "demo.admin@printnet.local"
    $demoAdminPassword = Set-DefaultEnvValue -Name "BACKEND_SUPER_ADMIN_PASSWORD" -Value "PrintNetDemo123!"
    $backendOperatorUsers = [string](Set-DefaultEnvValue -Name "BACKEND_OPERATOR_USER_IDS" -Value "queue-worker")
    $activityServiceToken = [string](Set-DefaultEnvValue -Name "BACKEND_ACTIVITY_SERVICE_TOKEN" -Value "printnet-local-activity")
    $null = Set-DefaultEnvValue -Name "BACKEND_AUTH_EXPOSE_DEBUG_CODE" -Value "0"
    $null = Set-DefaultEnvValue -Name "BACKEND_AUTH_EMAIL_REQUIRE_SMTP" -Value "1"
    $null = Set-DefaultEnvValue -Name "BACKEND_AUTH_EMAIL_FROM" -Value "no-reply@printnet.local"

    $smtpHost = [string](Set-DefaultEnvValue -Name "BACKEND_SMTP_HOST" -Value "mailpit")
    if ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable("BACKEND_SMTP_PORT", "Process"))) {
        if ($smtpHost.Trim().ToLowerInvariant() -eq "mailpit") {
            $null = Set-DefaultEnvValue -Name "BACKEND_SMTP_PORT" -Value "1025"
            $null = Set-DefaultEnvValue -Name "BACKEND_SMTP_STARTTLS" -Value "0"
            $null = Set-DefaultEnvValue -Name "BACKEND_SMTP_USE_SSL" -Value "0"
        } else {
            $null = Set-DefaultEnvValue -Name "BACKEND_SMTP_PORT" -Value "587"
        }
    }
    $null = Set-DefaultEnvValue -Name "BACKEND_SMTP_USERNAME" -Value ""
    $null = Set-DefaultEnvValue -Name "BACKEND_SMTP_PASSWORD" -Value ""
    if ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable("BACKEND_SMTP_STARTTLS", "Process"))) {
        $null = Set-DefaultEnvValue -Name "BACKEND_SMTP_STARTTLS" -Value "1"
    }
    if ([string]::IsNullOrWhiteSpace([Environment]::GetEnvironmentVariable("BACKEND_SMTP_USE_SSL", "Process"))) {
        $null = Set-DefaultEnvValue -Name "BACKEND_SMTP_USE_SSL" -Value "0"
    }
    [Environment]::SetEnvironmentVariable("PRINTNET_API_BASE_URL", "/api/v1", "Process")
    [Environment]::SetEnvironmentVariable(
        "PRINTNET_FRONTEND_SHARE_URL",
        "https://$($lanInfo.IPAddress):8080/signin",
        "Process"
    )
    [Environment]::SetEnvironmentVariable("PRINTNET_TLS_COMMON_NAME", $lanInfo.IPAddress, "Process")
    [Environment]::SetEnvironmentVariable("PRINTNET_TLS_ALT_IP", $lanInfo.IPAddress, "Process")
    [Environment]::SetEnvironmentVariable("PRINTNET_TLS_ALT_DNS", "localhost", "Process")

    $effectiveSmtpHost = [string][Environment]::GetEnvironmentVariable("BACKEND_SMTP_HOST", "Process")
    $emailMode = if ([string]::IsNullOrWhiteSpace($effectiveSmtpHost) -or $effectiveSmtpHost.Trim().ToLowerInvariant() -eq "mailpit") {
        "mail_capture"
    } else {
        "real_smtp"
    }

    $composeArgs = @("compose", "up", "--build", "-d", "frontend", "backend", "worker", "redis", "mongo", "mailpit")

    Write-Host ("Running: docker " + ($composeArgs -join " "))
    docker @composeArgs
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    $frontendLocalUrl = "https://localhost:8080"
    $frontendLanUrl = "https://$($lanInfo.IPAddress):8080"
    $frontendShareUrl = "$frontendLanUrl/signin"
    $backendHealthUrl = "http://localhost:8000/api/v1/health/live"
    $backendHealthProbeUrl = "http://127.0.0.1:8000/api/v1/health/live"
    $mailpitUiUrl = "http://localhost:8025"
    $desktopActivityBackendUrl = "http://127.0.0.1:8000/api/v1"

    Wait-HttpOk -Url $backendHealthProbeUrl -TimeoutSeconds 90
    Wait-HttpOk -Url $frontendLocalUrl -TimeoutSeconds 90
    Wait-HttpOk -Url $frontendLanUrl -TimeoutSeconds 90
    if ($emailMode -eq "mail_capture") {
        Wait-HttpOk -Url $mailpitUiUrl -TimeoutSeconds 90
    }

    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
    $qrJson = & python "Website/backend/scripts/generate_qr_assets.py" --url $frontendShareUrl --output-dir $outputDir --stem "printnet_frontend_lan"
    if ($LASTEXITCODE -ne 0) {
        throw "QR asset generation failed."
    }
    $desktopActivityConfigPath = Write-DesktopActivityConfig -BackendUrl $desktopActivityBackendUrl -ServiceToken $activityServiceToken
    $qrManifest = $qrJson | ConvertFrom-Json
    $manifest = [ordered]@{
        generated_at_utc = (Get-Date).ToUniversalTime().ToString("o")
        frontend_local_url = $frontendLocalUrl
        frontend_lan_url = $frontendLanUrl
        frontend_share_url = $frontendShareUrl
        backend_health_url = $backendHealthUrl
        qr_png_path = [string]$qrManifest.png_path
        qr_svg_path = [string]$qrManifest.svg_path
        firewall_rule_name = $firewallInfo.rule_name
        firewall_rule_configured = [bool]$firewallInfo.configured
        firewall_detail = [string]$firewallInfo.detail
        lan_interface = [string]$lanInfo.InterfaceAlias
        lan_ip = [string]$lanInfo.IPAddress
        email_mode = $emailMode
        mail_capture_ui_url = if ($emailMode -eq "mail_capture") { $mailpitUiUrl } else { "" }
        auth_admin_user_id = $demoAdminEmail
        launch_output_dir = $outputDir
    }
    $manifestPath = Join-Path $outputDir "website_launch_manifest.json"
    $manifest | ConvertTo-Json -Depth 5 | Set-Content -Path $manifestPath -Encoding UTF8

    Write-Host ""
    Write-Host "Frontend (local): $frontendLocalUrl"
    Write-Host "Frontend (LAN):   $frontendLanUrl"
    Write-Host "Share URL:        $frontendShareUrl"
    Write-Host "Backend health:   $backendHealthUrl"
    Write-Host "Firewall rule:    $($firewallInfo.rule_name)"
    Write-Host "Firewall detail:  $($firewallInfo.detail)"
    Write-Host "Email mode:       $emailMode"
    if ($emailMode -eq "mail_capture") {
        Write-Host "Mail capture UI:  $mailpitUiUrl"
    }
    Write-Host "QR PNG:           $($qrManifest.png_path)"
    Write-Host "QR SVG:           $($qrManifest.svg_path)"
    Write-Host "Manifest:         $manifestPath"
    Write-Host "Demo admin user:  $demoAdminEmail"
    if (-not [bool]$firewallInfo.lan_access_ready) {
        Write-Warning "LAN access is not ready yet. Re-run this launcher in an Administrator PowerShell window so it can create the LocalSubnet firewall rule."
    }

    if ($Foreground) {
        Write-Host ""
        Write-Host "Streaming compose logs. Press Ctrl+C to stop."
        docker compose logs -f frontend backend worker redis mongo mailpit
    }
}
finally {
    foreach ($key in $previousEnv.Keys) {
        [Environment]::SetEnvironmentVariable($key, $previousEnv[$key], "Process")
    }
    Pop-Location
}
