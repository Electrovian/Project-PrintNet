param(
    [switch]$WithComposeSmoke
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$PythonExe = "python"
$NodeExe = "node"
$NpmExe = "npm"
$DockerExe = "docker"
$Timestamp = Get-Date -Format "yyyyMMddTHHmmss"
$ScratchRoot = Join-Path $env:TEMP "printnet_launch_readiness_$Timestamp"
$AuditDir = Join-Path $ScratchRoot "visual_audit"
New-Item -ItemType Directory -Force -Path $ScratchRoot | Out-Null

function Write-Step {
    param([string]$Label)
    Write-Host ""
    Write-Host "== $Label =="
}

function Get-GitStatusSnapshot {
    Push-Location $RepoRoot
    try {
        return @(& git status --porcelain=v1 | Sort-Object)
    }
    finally {
        Pop-Location
    }
}

function Assert-GitBaseline {
    param(
        [string[]]$Baseline,
        [string]$Label
    )

    $Current = Get-GitStatusSnapshot
    $Delta = Compare-Object -ReferenceObject $Baseline -DifferenceObject $Current -SyncWindow 0
    if ($null -ne $Delta) {
        $Lines = $Delta | ForEach-Object { "$($_.SideIndicator) $($_.InputObject)" }
        $Message = ($Lines -join [Environment]::NewLine)
        throw "Tracked worktree drift detected after '$Label'.`n$Message"
    }
}

function Invoke-StepCommand {
    param(
        [string]$Label,
        [string]$WorkingDirectory,
        [string]$Executable,
        [string[]]$Arguments,
        [string[]]$Baseline,
        [hashtable]$EnvironmentOverrides = @{}
    )

    Write-Step $Label
    Push-Location $WorkingDirectory
    $Previous = @{}
    try {
        foreach ($Key in $EnvironmentOverrides.Keys) {
            $Previous[$Key] = [Environment]::GetEnvironmentVariable($Key, "Process")
            [Environment]::SetEnvironmentVariable($Key, [string]$EnvironmentOverrides[$Key], "Process")
        }
        & $Executable @Arguments
        if ($LASTEXITCODE -ne 0) {
            throw "Command failed with exit code ${LASTEXITCODE}: $Executable $($Arguments -join ' ')"
        }
    }
    finally {
        foreach ($Key in $EnvironmentOverrides.Keys) {
            [Environment]::SetEnvironmentVariable($Key, $Previous[$Key], "Process")
        }
        Pop-Location
    }
    Assert-GitBaseline -Baseline $Baseline -Label $Label
}

function Get-FreeTcpPort {
    $Listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, 0)
    try {
        $Listener.Start()
        return ([System.Net.IPEndPoint]$Listener.LocalEndpoint).Port
    }
    finally {
        $Listener.Stop()
    }
}

function Start-LoggedProcess {
    param(
        [string]$FilePath,
        [string[]]$ArgumentList,
        [string]$WorkingDirectory,
        [string]$LogStem,
        [hashtable]$EnvironmentOverrides = @{}
    )

    $StdOutPath = Join-Path $ScratchRoot "$LogStem.out.log"
    $StdErrPath = Join-Path $ScratchRoot "$LogStem.err.log"
    $Previous = @{}
    try {
        foreach ($Key in $EnvironmentOverrides.Keys) {
            $Previous[$Key] = [Environment]::GetEnvironmentVariable($Key, "Process")
            [Environment]::SetEnvironmentVariable($Key, [string]$EnvironmentOverrides[$Key], "Process")
        }
        $Process = Start-Process `
            -FilePath $FilePath `
            -ArgumentList $ArgumentList `
            -WorkingDirectory $WorkingDirectory `
            -RedirectStandardOutput $StdOutPath `
            -RedirectStandardError $StdErrPath `
            -PassThru `
            -WindowStyle Hidden
    }
    finally {
        foreach ($Key in $EnvironmentOverrides.Keys) {
            [Environment]::SetEnvironmentVariable($Key, $Previous[$Key], "Process")
        }
    }

    return [pscustomobject]@{
        Process = $Process
        StdOutPath = $StdOutPath
        StdErrPath = $StdErrPath
    }
}

function Stop-LoggedProcess {
    param($ProcessInfo)

    if ($null -eq $ProcessInfo) {
        return
    }
    $Process = $ProcessInfo.Process
    if ($null -eq $Process) {
        return
    }
    if (-not $Process.HasExited) {
        Stop-Process -Id $Process.Id -Force
        $Process.WaitForExit()
    }
}

function Read-ProcessLogs {
    param($ProcessInfo)

    $Out = ""
    $Err = ""
    if ($null -ne $ProcessInfo) {
        if (Test-Path $ProcessInfo.StdOutPath) {
            $Out = Get-Content -Path $ProcessInfo.StdOutPath -Raw
        }
        if (Test-Path $ProcessInfo.StdErrPath) {
            $Err = Get-Content -Path $ProcessInfo.StdErrPath -Raw
        }
    }
    return [pscustomobject]@{
        StdOut = $Out
        StdErr = $Err
    }
}

function Wait-HttpOk {
    param(
        [string]$Url,
        [int]$TimeoutSeconds = 60
    )

    $CurlExe = $null
    if ($env:OS -eq "Windows_NT") {
        $CurlCmd = Get-Command "curl.exe" -ErrorAction SilentlyContinue
        if ($null -ne $CurlCmd) {
            $CurlExe = [string]$CurlCmd.Source
        }
    }

    $Deadline = (Get-Date).AddSeconds([math]::Max(1, $TimeoutSeconds))
    while ((Get-Date) -lt $Deadline) {
        try {
            if ($Url -like "https://*" -and $CurlExe) {
                $StatusText = & $CurlExe -k -L -s -o NUL -w "%{http_code}" $Url
                $StatusCode = 0
                if ([int]::TryParse([string]$StatusText, [ref]$StatusCode) -and $StatusCode -ge 200 -and $StatusCode -lt 300) {
                    return
                }
            }
            else {
                $Response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5
                if ($Response.StatusCode -ge 200 -and $Response.StatusCode -lt 300) {
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

function Invoke-ComposeSmoke {
    param(
        [string[]]$Baseline
    )

    Write-Step "Docker compose smoke"
    Push-Location $RepoRoot
    try {
        & $DockerExe compose up --build -d frontend backend worker redis mongo mailpit
        if ($LASTEXITCODE -ne 0) {
            throw "docker compose up failed"
        }
        Wait-HttpOk -Url "http://127.0.0.1:8000/api/v1/health/live" -TimeoutSeconds 90
        Wait-HttpOk -Url "https://127.0.0.1:8080" -TimeoutSeconds 90
    }
    finally {
        & $DockerExe compose down | Out-Null
        Pop-Location
    }
    Assert-GitBaseline -Baseline $Baseline -Label "Docker compose smoke"
}

$Baseline = Get-GitStatusSnapshot
$BackendInfo = $null

try {
    Invoke-StepCommand -Label "Desktop startup smoke" `
        -WorkingDirectory $RepoRoot `
        -Executable $PythonExe `
        -Arguments @("-m", "App.testing.desktop_startup_smoke") `
        -Baseline $Baseline

    Invoke-StepCommand -Label "Desktop smoke suite" `
        -WorkingDirectory $RepoRoot `
        -Executable $PythonExe `
        -Arguments @("App\Tests\run_tests.py", "--scope", "smoke") `
        -Baseline $Baseline

    Invoke-StepCommand -Label "Desktop visual audit" `
        -WorkingDirectory $RepoRoot `
        -Executable $PythonExe `
        -Arguments @("-m", "App.testing.visual_audit", "--scenario", "demo", "--output-dir", $AuditDir) `
        -Baseline $Baseline

    Invoke-StepCommand -Label "Backend test suite" `
        -WorkingDirectory (Join-Path $RepoRoot "Website\backend") `
        -Executable $PythonExe `
        -Arguments @("-m", "pytest", "tests", "-q") `
        -Baseline $Baseline

    $BackendPort = Get-FreeTcpPort
    $BackendBaseUrl = "http://127.0.0.1:$BackendPort/api/v1"
    Write-Step "Backend live health probe"
    $BackendInfo = Start-LoggedProcess `
        -FilePath $PythonExe `
        -ArgumentList @("-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "$BackendPort") `
        -WorkingDirectory (Join-Path $RepoRoot "Website\backend") `
        -LogStem "backend-live"
    try {
        Wait-HttpOk -Url "$BackendBaseUrl/health/live" -TimeoutSeconds 60
    }
    catch {
        $Logs = Read-ProcessLogs -ProcessInfo $BackendInfo
        throw "Backend live health probe failed.`nSTDOUT:`n$($Logs.StdOut)`nSTDERR:`n$($Logs.StdErr)"
    }
    Assert-GitBaseline -Baseline $Baseline -Label "Backend live health probe"

    Invoke-StepCommand -Label "Backend worker smoke" `
        -WorkingDirectory (Join-Path $RepoRoot "Website\backend") `
        -Executable $PythonExe `
        -Arguments @("scripts\worker_smoke.py", "--backend-timeout", "45", "--worker-timeout", "30", "--worker-cycles", "1") `
        -Baseline $Baseline

    Invoke-StepCommand -Label "Frontend node tests" `
        -WorkingDirectory (Join-Path $RepoRoot "Website\frontend") `
        -Executable $NodeExe `
        -Arguments @(
            "--test",
            "tests/frontend_contracts.test.mjs",
            "tests/frontend_auth_role.test.mjs",
            "tests/frontend_observability_release_readiness.test.mjs",
            "tests/frontend_queue_worker_orchestration.test.mjs"
        ) `
        -Baseline $Baseline

    Invoke-StepCommand -Label "Frontend production build" `
        -WorkingDirectory (Join-Path $RepoRoot "Website\frontend") `
        -Executable $NpmExe `
        -Arguments @("run", "build") `
        -Baseline $Baseline

    Invoke-StepCommand -Label "Frontend browser smoke" `
        -WorkingDirectory (Join-Path $RepoRoot "Website\frontend") `
        -Executable $NpmExe `
        -Arguments @("run", "test:browser") `
        -Baseline $Baseline `
        -EnvironmentOverrides @{ "PRINTNET_API_BASE_URL" = $BackendBaseUrl }

    Invoke-StepCommand -Label "Mobile unit tests" `
        -WorkingDirectory $RepoRoot `
        -Executable $PythonExe `
        -Arguments @("-m", "unittest", "discover", "-s", "Mobile/tests", "-q") `
        -Baseline $Baseline

    Invoke-StepCommand -Label "Mobile preflight" `
        -WorkingDirectory $RepoRoot `
        -Executable $PythonExe `
        -Arguments @("-m", "Mobile.preflight") `
        -Baseline $Baseline

    Invoke-StepCommand -Label "Docker compose config" `
        -WorkingDirectory $RepoRoot `
        -Executable $DockerExe `
        -Arguments @("compose", "config", "-q") `
        -Baseline $Baseline

    if ($WithComposeSmoke) {
        Invoke-ComposeSmoke -Baseline $Baseline
    }
}
finally {
    Stop-LoggedProcess -ProcessInfo $BackendInfo
}

Write-Host ""
Write-Host "Launch readiness checks completed."
Write-Host "Visual audit output: $AuditDir"
