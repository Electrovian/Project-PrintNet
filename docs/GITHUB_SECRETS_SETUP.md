# Setting Up GitHub Secrets for Code Signing

This guide shows how to configure GitHub repository secrets for automatic code signing in GitHub Actions.

## Prerequisites

- A code signing certificate in .pfx format
- Admin access to the GitHub repository
- PowerShell (Windows) or Bash (Linux/Mac)

## Step 1: Convert Certificate to Base64

### On Windows (PowerShell)

```powershell
# Convert certificate to Base64
[Convert]::ToBase64String([IO.File]::ReadAllBytes("path\to\your-certificate.pfx")) | Out-File -FilePath certificate-base64.txt -NoNewline

# View the Base64 string
Get-Content certificate-base64.txt
```

### On Linux/Mac (Bash)

```bash
# Convert certificate to Base64
base64 -i your-certificate.pfx -o certificate-base64.txt

# View the Base64 string
cat certificate-base64.txt
```

## Step 2: Add Secrets to GitHub Repository

1. Go to your GitHub repository
2. Click on **Settings** (tab at the top)
3. In the left sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**

### Add WINDOWS_CERTIFICATE Secret

1. Name: `WINDOWS_CERTIFICATE`
2. Value: Paste the entire Base64 string from `certificate-base64.txt`
3. Click **Add secret**

### Add CERTIFICATE_PASSWORD Secret

1. Click **New repository secret** again
2. Name: `CERTIFICATE_PASSWORD`
3. Value: Enter your certificate password
4. Click **Add secret**

## Step 3: Verify Secrets

You should now see two secrets listed:
- `WINDOWS_CERTIFICATE`
- `CERTIFICATE_PASSWORD`

## Step 4: Test the Workflow

### Option 1: Create a Tag (Automatic Release)

```bash
git tag v1.0.0
git push origin v1.0.0
```

This will trigger the build workflow and create a signed release.

### Option 2: Manual Workflow Dispatch

1. Go to **Actions** tab in GitHub
2. Select **build-app** workflow
3. Click **Run workflow**
4. Select the branch and click **Run workflow**

## Verification

After the workflow completes:

1. Download the Windows artifact
2. Extract `EON-OpenSlicer.exe`
3. Right-click the .exe → **Properties**
4. Go to **Digital Signatures** tab
5. You should see your signature listed

## Security Notes

### Certificate Security

- **Never commit** certificate files to the repository
- **Never share** the Base64 certificate string publicly
- **Delete** the `certificate-base64.txt` file after adding it to GitHub secrets
- **Rotate** certificates before they expire

### GitHub Secrets Best Practices

1. **Limit access**: Only repository admins can view/edit secrets
2. **Audit access**: Review who has admin access regularly
3. **Use environment secrets** for production: Consider using environment-specific secrets
4. **Monitor usage**: Check Actions logs for unauthorized usage

## Troubleshooting

### "No certificates were found"

- Verify the Base64 string is complete (no line breaks or truncation)
- Check that the certificate password is correct
- Ensure the certificate hasn't expired

### Workflow shows "signtool.exe not found"

- This is expected on the GitHub runner environment
- The workflow handles this by searching for signtool in Windows SDK paths
- If persisting, the Windows SDK might not be fully installed on the runner

### Signature not applied

If `secrets.WINDOWS_CERTIFICATE` is empty, the signing step is skipped:
- Verify secrets are named exactly as shown above (case-sensitive)
- Check that secrets are in the repository, not your personal account
- Ensure you have permissions to access repository secrets

## Testing Locally

Before setting up GitHub secrets, test signing locally:

```powershell
.\scripts\sign-executable.ps1 -ExecutablePath "dist\EON-OpenSlicer.exe" -CertificatePath "your-cert.pfx" -CertificatePassword "your-password"
```

## Certificate Management

### Certificate Expiration

Code signing certificates typically last 1-3 years. Set a reminder to renew:

1. **3 months before expiration**: Start renewal process with CA
2. **1 month before expiration**: Test new certificate
3. **Update GitHub secrets** with new certificate

### Revoking a Certificate

If your certificate is compromised:

1. Contact your Certificate Authority immediately to revoke
2. Delete the compromised secrets from GitHub
3. Obtain a new certificate
4. Update GitHub secrets with the new certificate
5. Re-sign and re-release all executables

## Resources

- [GitHub Encrypted Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Code Signing Documentation](./CODE_SIGNING.md)
- [Microsoft Authenticode](https://docs.microsoft.com/en-us/windows-hardware/drivers/install/authenticode)

## Support

For issues:
1. Check the GitHub Actions workflow logs
2. Review this troubleshooting section
3. Consult the main [CODE_SIGNING.md](./CODE_SIGNING.md) documentation
4. Contact your Certificate Authority for certificate-specific issues
