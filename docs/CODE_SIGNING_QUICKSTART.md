# Code Signing Quick Start Guide

This guide provides a quick overview of the code signing implementation for EON-OpenSlicer.

## What Problem Does This Solve?

When users download and run `EON-OpenSlicer.exe` on Windows, they see warnings like:
- "Windows protected your PC"
- "Unknown publisher"
- "This app might harm your device"

**Code signing eliminates these warnings** by digitally signing the executable with a trusted certificate, verifying the publisher's identity.

## Quick Overview

### For Users
- Signed releases will not trigger Windows SmartScreen warnings
- You can verify the publisher's identity in the executable's properties
- The signature ensures the file hasn't been tampered with

### For Developers

The repository now includes:
1. **Automated signing in GitHub Actions** - Signs executables automatically when building releases
2. **Local signing scripts** - For developers to sign executables on their machines
3. **Comprehensive documentation** - Step-by-step guides for setup and troubleshooting

## Setup Steps (For Repository Maintainers)

### 1. Obtain a Code Signing Certificate

**Recommended providers:**
- Sectigo: ~$200-400/year
- DigiCert: ~$400-500/year
- GlobalSign: ~$250-400/year

**What you need:**
- Business verification (for OV certificates)
- Certificate in .pfx format
- Certificate password

See [CODE_SIGNING.md](./CODE_SIGNING.md#getting-a-code-signing-certificate) for detailed instructions.

### 2. Configure GitHub Secrets

Convert your certificate to Base64 and add to GitHub repository secrets:

**Windows PowerShell:**
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("cert.pfx")) | Out-File cert-base64.txt
```

**Add to GitHub:**
1. Go to repository Settings → Secrets and variables → Actions
2. Add secret `WINDOWS_CERTIFICATE` with the Base64 string
3. Add secret `CERTIFICATE_PASSWORD` with the password

See [GITHUB_SECRETS_SETUP.md](./GITHUB_SECRETS_SETUP.md) for detailed instructions.

### 3. Automatic Signing

Once secrets are configured, the GitHub Actions workflow will automatically:
- ✅ Build the Windows executable with version information
- ✅ Sign the executable using your certificate
- ✅ Verify the signature
- ✅ Package and upload the signed executable

## Local Development

### Sign an Executable Locally

```powershell
.\scripts\sign-executable.ps1 -ExecutablePath "dist\EON-OpenSlicer.exe" -CertificatePath "cert.pfx" -CertificatePassword "password"
```

### Build and Sign

```powershell
# 1. Build with PyInstaller
pyinstaller --noconfirm --clean --onefile --windowed --name EON-OpenSlicer --paths App --add-data "App/assets;assets" App/main.py

# 2. Sign the executable
.\scripts\sign-executable.ps1 -ExecutablePath "dist\EON-OpenSlicer.exe" -CertificatePath "your-cert.pfx"
```

## Verifying a Signed Executable

### Method 1: Windows Properties
1. Right-click `EON-OpenSlicer.exe`
2. Select **Properties**
3. Go to **Digital Signatures** tab
4. You should see the signature listed with the publisher name

### Method 2: Using signtool
```powershell
signtool verify /pa /v EON-OpenSlicer.exe
```

## Important Security Notes

⚠️ **Never commit certificate files to Git**
⚠️ **Never share certificate passwords publicly**
⚠️ **Store certificates securely**
⚠️ **Use GitHub Secrets for CI/CD**

The `.gitignore` file is already configured to exclude certificate files:
- `*.pfx`
- `*.p12`
- `*.cer`
- `certificate-base64.txt`

## What's Included

### Documentation
- [`CODE_SIGNING.md`](./CODE_SIGNING.md) - Comprehensive guide
- [`GITHUB_SECRETS_SETUP.md`](./GITHUB_SECRETS_SETUP.md) - GitHub setup instructions
- [`scripts/README.md`](../scripts/README.md) - Scripts documentation

### Scripts
- [`scripts/sign-executable.ps1`](../scripts/sign-executable.ps1) - PowerShell signing script

### Configuration
- `.github/workflows/build.yml` - Updated with signing steps
- `.gitignore` - Excludes certificate files

## Testing Without a Real Certificate

For testing the signing process without purchasing a certificate:

```powershell
# Generate self-signed test certificate
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=EON-OpenSlicer Test" -CertStoreLocation Cert:\CurrentUser\My
$pwd = ConvertTo-SecureString -String "TestPassword123" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "test-cert.pfx" -Password $pwd

# Sign with test certificate
.\scripts\sign-executable.ps1 -ExecutablePath "dist\EON-OpenSlicer.exe" -CertificatePath "test-cert.pfx" -CertificatePassword "TestPassword123"
```

**Note:** Self-signed certificates do NOT remove Windows warnings, but they're useful for testing the signing process.

## Building Trust with Windows SmartScreen

Even with a valid certificate:
- New certificates may show warnings initially
- Windows SmartScreen builds reputation over time
- More unique downloads = better reputation
- Full trust can take weeks to months

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "No certificates were found" | Check certificate password and file format |
| "signtool.exe not found" | Install Windows SDK |
| Workflow skips signing | Verify GitHub secrets are set correctly |
| Signature verification fails | Check timestamp server availability |

See [CODE_SIGNING.md](./CODE_SIGNING.md#troubleshooting) for detailed troubleshooting.

## Cost Analysis

### One-Time Setup
- Certificate purchase: $200-500/year
- Setup time: 2-4 hours

### Ongoing Maintenance
- Certificate renewal: Annually
- Update GitHub secrets: When certificate renewed
- Zero additional build time (signing is fast)

### Benefits
- Professional appearance
- User trust and confidence
- No Windows warnings
- Tamper detection

## Next Steps

1. **Immediate**: Review this documentation
2. **Week 1**: Obtain code signing certificate
3. **Week 1**: Configure GitHub secrets
4. **Week 2**: Test signing with next release
5. **Ongoing**: Monitor certificate expiration

## Support and Resources

- [Microsoft Authenticode Documentation](https://docs.microsoft.com/en-us/windows-hardware/drivers/install/authenticode)
- [SignTool Documentation](https://docs.microsoft.com/en-us/windows/win32/seccrypto/signtool)
- [GitHub Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

## Questions?

For detailed information, see:
- **Certificate acquisition**: [CODE_SIGNING.md](./CODE_SIGNING.md)
- **GitHub setup**: [GITHUB_SECRETS_SETUP.md](./GITHUB_SECRETS_SETUP.md)
- **Local signing**: [scripts/README.md](../scripts/README.md)
