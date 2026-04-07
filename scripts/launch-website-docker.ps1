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

function Ensure-PrivateFirewallRule {
    param(
        [string]$RuleName,
        [int]$Port
    )

    if ($env:OS -ne "Windows_NT") {
        return [pscustomobject]@{
            configured = $false
            rule_name = $RuleName
            detail = "Firewall automation skipped: non-Windows host."
        }
    }

    $rule = Get-NetFirewallRule -DisplayName $RuleName -ErrorAction SilentlyContinue
    if ($null -ne $rule) {
        $portFilter = Get-NetFirewallPortFilter -AssociatedNetFirewallRule $rule -ErrorAction SilentlyContinue
        $hasMatchingPort = $false
        foreach ($filter in @($portFilter)) {
            if ([string]$filter.Protocol -eq "TCP" -and [string]$filter.LocalPort -eq [string]$Port) {
                $hasMatchingPort = $true
                break
            }
        }
        if ($hasMatchingPort -and [string]$rule.Enabled -eq "True" -and [string]$rule.Profile -match "Private") {
            return [pscustomobject]@{
                configured = $true
                rule_name = $RuleName
                detail = "Existing private firewall rule is already configured."
            }
        }
    }

    if (-not (Test-IsAdministrator)) {
        throw "Administrator privileges are required to create the private-network firewall rule for port $Port."
    }

    if ($null -ne $rule) {
        Remove-NetFirewallRule -DisplayName $RuleName -ErrorAction Stop | Out-Null
    }

    New-NetFirewallRule `
        -DisplayName $RuleName `
        -Direction Inbound `
        -Action Allow `
        -Profile Private `
        -Protocol TCP `
        -LocalPort $Port `
        -EdgeTraversalPolicy Block | Out-Null

    return [pscustomobject]@{
        configured = $true
        rule_name = $RuleName
        detail = "Created private-network firewall rule."
    }
}

function Wait-HttpOk {
    param(
        [string]$Url,
        [int]$TimeoutSeconds = 90
    )

    $deadline = (Get-Date).AddSeconds([math]::Max(1, $TimeoutSeconds))
    while ((Get-Date) -lt $deadline) {
        try {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 300) {
                return
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

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$timestamp = Get-Date -Format "yyyyMMddTHHmmss"
$outputDir = Join-Path $env:TEMP "printnet_website_launch_$timestamp"
$firewallRuleName = "PrintNet Website Frontend 8080 (Private LAN)"
$previousEnv = @{}

foreach ($key in @(
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
    "BACKEND_SMTP_USE_SSL"
)) {
    $previousEnv[$key] = [Environment]::GetEnvironmentVariable($key, "Process")
}

Push-Location $repoRoot
try {
    $lanInfo = Get-PrimaryLanIPv4
    $firewallInfo = Ensure-PrivateFirewallRule -RuleName $firewallRuleName -Port 8080

    $demoAdminEmail = Set-DefaultEnvValue -Name "BACKEND_SUPER_ADMIN_EMAIL" -Value "demo.admin@printnet.local"
    $demoAdminPassword = Set-DefaultEnvValue -Name "BACKEND_SUPER_ADMIN_PASSWORD" -Value "PrintNetDemo123!"
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

    $frontendLocalUrl = "http://localhost:8080"
    $frontendLanUrl = "http://$($lanInfo.IPAddress):8080"
    $backendHealthUrl = "http://$($lanInfo.IPAddress):8000/api/v1/health/live"
    $mailpitUiUrl = "http://localhost:8025"

    Wait-HttpOk -Url $backendHealthUrl -TimeoutSeconds 90
    Wait-HttpOk -Url $frontendLocalUrl -TimeoutSeconds 90
    Wait-HttpOk -Url $frontendLanUrl -TimeoutSeconds 90
    if ($emailMode -eq "mail_capture") {
        Wait-HttpOk -Url $mailpitUiUrl -TimeoutSeconds 90
    }

    New-Item -ItemType Directory -Force -Path $outputDir | Out-Null
    $qrJson = & python "Website/backend/scripts/generate_qr_assets.py" --url $frontendLanUrl --output-dir $outputDir --stem "printnet_frontend_lan"
    if ($LASTEXITCODE -ne 0) {
        throw "QR asset generation failed."
    }
    $qrManifest = $qrJson | ConvertFrom-Json
    $manifest = [ordered]@{
        generated_at_utc = (Get-Date).ToUniversalTime().ToString("o")
        frontend_local_url = $frontendLocalUrl
        frontend_lan_url = $frontendLanUrl
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
    Write-Host "Backend health:   $backendHealthUrl"
    Write-Host "Firewall rule:    $($firewallInfo.rule_name)"
    Write-Host "Email mode:       $emailMode"
    if ($emailMode -eq "mail_capture") {
        Write-Host "Mail capture UI:  $mailpitUiUrl"
    }
    Write-Host "QR PNG:           $($qrManifest.png_path)"
    Write-Host "QR SVG:           $($qrManifest.svg_path)"
    Write-Host "Manifest:         $manifestPath"
    Write-Host "Demo admin user:  $demoAdminEmail"

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
