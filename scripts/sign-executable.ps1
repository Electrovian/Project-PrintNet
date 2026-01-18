# Code Signing Script for EON-OpenSlicer
# This script signs the Windows executable with a code signing certificate

param(
    [Parameter(Mandatory=$true)]
    [string]$ExecutablePath,
    
    [Parameter(Mandatory=$false)]
    [string]$CertificatePath = "",
    
    [Parameter(Mandatory=$false)]
    [string]$CertificatePassword = "",
    
    [Parameter(Mandatory=$false)]
    [string]$TimestampServer = "http://timestamp.digicert.com"
)

function Find-SignTool {
    Write-Host "Searching for signtool.exe..."
    
    # Common paths for signtool.exe
    $possiblePaths = @(
        "C:\Program Files (x86)\Windows Kits\10\bin\*\x64\signtool.exe",
        "C:\Program Files\Microsoft SDKs\Windows\v7.1\Bin\signtool.exe",
        "C:\Program Files (x86)\Microsoft SDKs\Windows\v7.1A\Bin\signtool.exe"
    )
    
    foreach ($path in $possiblePaths) {
        $found = Get-ChildItem -Path $path -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) {
            return $found.FullName
        }
    }
    
    return $null
}

function Test-Executable {
    param([string]$Path)
    
    if (-not (Test-Path $Path)) {
        Write-Error "Executable not found: $Path"
        return $false
    }
    
    if ([System.IO.Path]::GetExtension($Path) -ne ".exe") {
        Write-Error "File is not an executable: $Path"
        return $false
    }
    
    return $true
}

# Main script
Write-Host "======================================"
Write-Host "EON-OpenSlicer Code Signing Script"
Write-Host "======================================"
Write-Host ""

# Validate executable
if (-not (Test-Executable -Path $ExecutablePath)) {
    exit 1
}

# Find signtool
$signtool = Find-SignTool
if (-not $signtool) {
    Write-Error "signtool.exe not found. Please install Windows SDK."
    Write-Host ""
    Write-Host "Download from: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/"
    exit 1
}

Write-Host "Found signtool: $signtool"
Write-Host ""

# Check for certificate
if ([string]::IsNullOrEmpty($CertificatePath)) {
    Write-Host "No certificate path provided."
    Write-Host "Usage: .\sign-executable.ps1 -ExecutablePath <path> -CertificatePath <cert.pfx> -CertificatePassword <password>"
    Write-Host ""
    Write-Host "To generate a test certificate (for testing only):"
    Write-Host '  $cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=EON-OpenSlicer Test" -CertStoreLocation Cert:\CurrentUser\My'
    Write-Host '  $pwd = ConvertTo-SecureString -String "TestPassword123" -Force -AsPlainText'
    Write-Host '  Export-PfxCertificate -Cert $cert -FilePath "test-cert.pfx" -Password $pwd'
    Write-Host ""
    exit 1
}

if (-not (Test-Path $CertificatePath)) {
    Write-Error "Certificate not found: $CertificatePath"
    exit 1
}

if ([string]::IsNullOrEmpty($CertificatePassword)) {
    $securePassword = Read-Host "Enter certificate password" -AsSecureString
    $CertificatePassword = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
        [Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePassword)
    )
}

# Sign the executable
Write-Host "Signing executable: $ExecutablePath"
Write-Host "Using certificate: $CertificatePath"
Write-Host "Timestamp server: $TimestampServer"
Write-Host ""

$signArgs = @(
    "sign",
    "/f", $CertificatePath,
    "/p", $CertificatePassword,
    "/tr", $TimestampServer,
    "/td", "SHA256",
    "/fd", "SHA256",
    "/v",
    $ExecutablePath
)

& $signtool $signArgs

if ($LASTEXITCODE -ne 0) {
    Write-Error "Signing failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Verifying signature..."
& $signtool verify /pa /v $ExecutablePath

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS: Executable signed and verified!" -ForegroundColor Green
} else {
    Write-Error "Signature verification failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}
