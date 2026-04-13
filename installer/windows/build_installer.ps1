param(
  [string]$AppExePath = "dist/EON-OpenSlicer.exe",
  [string]$AppVersion = "1.0.0"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$issPath = Join-Path $PSScriptRoot "EON-OpenSlicer.iss"
$exePath = Join-Path $root $AppExePath

if (-not (Test-Path $issPath)) {
  throw "Inno Setup script missing: $issPath"
}
if (-not (Test-Path $exePath)) {
  throw "Built app executable missing: $exePath"
}

$iscc = Get-Command "iscc" -ErrorAction SilentlyContinue
if (-not $iscc) {
  throw "ISCC executable not found. Install Inno Setup and ensure iscc is in PATH."
}

Write-Host "Building installer..."
& $iscc.Source "/DAppExe=$exePath" "/DAppVersion=$AppVersion" $issPath
Write-Host "Installer build complete."
