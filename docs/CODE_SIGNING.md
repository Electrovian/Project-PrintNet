# Code Signing for Windows Executable

## Overview

This document explains how to set up code signing for the EON-OpenSlicer Windows executable to prevent Windows SmartScreen warnings about unverified publishers.

## Why Code Signing?

When users download and run the EON-OpenSlicer executable on Windows, they may see warnings like:
- "Windows protected your PC"
- "Unknown publisher"
- "This app might harm your device"

Code signing resolves these warnings by:
1. Verifying the publisher's identity
2. Ensuring the executable hasn't been tampered with
3. Building trust with Windows SmartScreen over time

## Getting a Code Signing Certificate

### Option 1: Commercial Certificate Authority (Recommended for Production)

Purchase a code signing certificate from a trusted CA:
- **Sectigo (formerly Comodo)** - ~$200-400/year
- **DigiCert** - ~$400-500/year
- **GlobalSign** - ~$250-400/year

**Requirements:**
- Business verification (for OV certificates)
- EV certificates require a hardware token (USB)
- Processing time: 1-7 business days

**Steps:**
1. Choose a CA and purchase a code signing certificate
2. Complete identity verification process
3. Download certificate (usually .pfx or .p12 format)
4. Store certificate password securely

### Option 2: Self-Signed Certificate (Testing Only)

For testing purposes only (will not remove Windows warnings):

```powershell
# Generate self-signed certificate
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=EON-OpenSlicer" -CertStoreLocation Cert:\CurrentUser\My

# Export to PFX
$pwd = ConvertTo-SecureString -String "YourPassword" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "EON-OpenSlicer-TestCert.pfx" -Password $pwd
```

**Note:** Self-signed certificates still trigger Windows warnings but can be used for testing the signing process.

## Setting Up GitHub Actions for Code Signing

### 1. Store Certificate in GitHub Secrets

1. Convert your certificate to Base64:
   ```bash
   # On Linux/Mac
   base64 -i certificate.pfx -o certificate.txt
   
   # On Windows (PowerShell)
   [Convert]::ToBase64String([IO.File]::ReadAllBytes("certificate.pfx")) | Out-File certificate.txt
   ```

2. In GitHub repository settings, add secrets:
   - `WINDOWS_CERTIFICATE`: The Base64-encoded certificate content
   - `CERTIFICATE_PASSWORD`: The certificate password

### 2. The Signing Process

The GitHub Actions workflow automatically:
1. Decodes the certificate from secrets
2. Builds the executable with PyInstaller
3. Signs the executable using signtool
4. Verifies the signature
5. Packages and uploads the signed executable

## Local Signing (For Developers)

### Prerequisites

Install Windows SDK (includes signtool.exe):
- Download from: https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/
- Or install via Visual Studio Installer

### Signing an Executable Locally

```powershell
# Locate signtool (usually in Windows SDK bin folder)
$signtool = "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe"

# Sign the executable
& $signtool sign /f "path\to\certificate.pfx" /p "certificate_password" /tr http://timestamp.digicert.com /td SHA256 /fd SHA256 "dist\EON-OpenSlicer.exe"

# Verify signature
& $signtool verify /pa "dist\EON-OpenSlicer.exe"
```

### Parameters Explained

- `/f` - Certificate file path
- `/p` - Certificate password
- `/tr` - Timestamp server URL (RFC 3161)
- `/td` - Timestamp digest algorithm
- `/fd` - File digest algorithm
- `/pa` - Verify using default authentication

## Timestamp Servers

Timestamping ensures your signature remains valid even after the certificate expires. Use one of these free timestamp servers:

- DigiCert: `http://timestamp.digicert.com`
- Sectigo: `http://timestamp.sectigo.com`
- GlobalSign: `http://timestamp.globalsign.com`

## Building Reputation with SmartScreen

Even with a valid code signature:
- New certificates may still show warnings initially
- Windows SmartScreen builds reputation over time
- More downloads from unique users = better reputation
- Can take weeks to months for full trust

## Troubleshooting

### "No certificates were found that met all the given criteria"
- Certificate is expired
- Certificate is not installed in the certificate store
- Wrong certificate format

### "SignTool Error: No certificates were found"
- Incorrect password
- Corrupted certificate file
- Certificate not suitable for code signing

### Signature verification fails
- Timestamp server is down (try a different one)
- Certificate has been revoked
- System time is incorrect

## Security Best Practices

1. **Never commit certificates to version control**
2. **Use strong passwords** for certificate files
3. **Restrict access** to certificates (use GitHub Secrets)
4. **Rotate certificates** before expiration
5. **Monitor certificate validity** periodically
6. **Use EV certificates** for highest trust (if budget allows)

## Resources

- [Microsoft Authenticode Documentation](https://docs.microsoft.com/en-us/windows-hardware/drivers/install/authenticode)
- [SignTool Documentation](https://docs.microsoft.com/en-us/windows/win32/seccrypto/signtool)
- [Windows SmartScreen FAQ](https://docs.microsoft.com/en-us/windows/security/threat-protection/microsoft-defender-smartscreen/microsoft-defender-smartscreen-overview)

## Support

For issues with code signing:
1. Check the GitHub Actions logs for error messages
2. Verify certificate validity and password
3. Test signing process locally before committing
4. Contact your Certificate Authority for certificate issues
