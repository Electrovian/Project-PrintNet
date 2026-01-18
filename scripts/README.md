# Build and Signing Scripts

This directory contains utility scripts for building and signing the EON-OpenSlicer application.

## Scripts

### sign-executable.ps1

PowerShell script for signing Windows executables with a code signing certificate.

**Usage:**
```powershell
.\scripts\sign-executable.ps1 -ExecutablePath "dist\EON-OpenSlicer.exe" -CertificatePath "path\to\cert.pfx" -CertificatePassword "your_password"
```

**Parameters:**
- `ExecutablePath` (required): Path to the .exe file to sign
- `CertificatePath` (optional): Path to the .pfx certificate file
- `CertificatePassword` (optional): Certificate password (will prompt if not provided)
- `TimestampServer` (optional): Timestamp server URL (default: DigiCert)

**Example:**
```powershell
# Sign with certificate
.\scripts\sign-executable.ps1 -ExecutablePath "dist\EON-OpenSlicer.exe" -CertificatePath "mycert.pfx" -CertificatePassword "mypassword"

# Generate and use a test certificate (for testing only)
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=EON-OpenSlicer Test" -CertStoreLocation Cert:\CurrentUser\My
$pwd = ConvertTo-SecureString -String "TestPassword123" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "test-cert.pfx" -Password $pwd
.\scripts\sign-executable.ps1 -ExecutablePath "dist\EON-OpenSlicer.exe" -CertificatePath "test-cert.pfx" -CertificatePassword "TestPassword123"
```

## Prerequisites

- Windows 10 or later
- Windows SDK (includes signtool.exe)
  - Download: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
- Code signing certificate (.pfx format)

## See Also

- [Code Signing Documentation](../docs/CODE_SIGNING.md) - Complete guide to code signing
- [Build Workflow](../.github/workflows/build.yml) - GitHub Actions build configuration
