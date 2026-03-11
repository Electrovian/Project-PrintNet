param(
    [switch]$Foreground
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Push-Location $repoRoot
try {
    $composeArgs = @("compose", "up", "--build")
    if (-not $Foreground) {
        $composeArgs += "-d"
    }
    $composeArgs += @("frontend", "backend", "worker", "redis", "mongo")

    Write-Host ("Running: docker " + ($composeArgs -join " "))
    docker @composeArgs
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }

    Write-Host "Frontend: http://localhost:8080"
    Write-Host "Backend health: http://localhost:8000/api/v1/health/live"
}
finally {
    Pop-Location
}
