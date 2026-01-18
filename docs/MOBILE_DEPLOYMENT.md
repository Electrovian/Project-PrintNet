# Mobile Deployment Guide

This guide explains how to build and deploy EON-OpenSlicer to iOS and Android mobile devices and tablets.

## Overview

EON-OpenSlicer now supports deployment to mobile platforms in addition to Windows desktop. The application uses:
- **Desktop (Windows, Linux, macOS)**: PyQt5 for full-featured desktop experience
- **Mobile (iOS, Android)**: Toga framework for native mobile interface

## Architecture

The project uses [BeeWare Briefcase](https://briefcase.readthedocs.io/) for cross-platform packaging. The codebase includes:

- `App/main.py` - Desktop entry point (PyQt5)
- `App/app_mobile.py` - Mobile entry point (Toga)
- `App/__main__.py` - Unified entry point that auto-detects platform
- `pyproject.toml` - Briefcase configuration for all platforms

## Prerequisites

### For Android Development

1. **Python 3.12+**
2. **Java JDK 17+**
   ```bash
   # Ubuntu/Debian
   sudo apt install openjdk-17-jdk
   
   # macOS
   brew install openjdk@17
   ```

3. **Android SDK**
   - Download from https://developer.android.com/studio
   - Or use Briefcase which will download it automatically

4. **Briefcase**
   ```bash
   pip install briefcase
   ```

### For iOS Development

1. **macOS** (iOS builds require macOS)
2. **Python 3.12+**
3. **Xcode 14+** (from Mac App Store)
4. **Xcode Command Line Tools**
   ```bash
   xcode-select --install
   ```
5. **Briefcase**
   ```bash
   pip install briefcase
   ```

## Building for Mobile

### Android

#### Create the project
```bash
cd /path/to/Project-PrintNet  # Repository directory
briefcase create android
```

This creates the Android project structure in the `android/` directory.

#### Build the APK
```bash
briefcase build android
```

#### Package for distribution
```bash
# Debug APK (for testing)
briefcase package android --adhoc-sign

# Release APK (for production - requires signing key)
briefcase package android
```

The APK will be created in `android/gradle/EON-OpenSlicer/app/build/outputs/apk/`.

#### Install on device
```bash
briefcase run android
```

Or manually install:
```bash
adb install android/gradle/EON-OpenSlicer/app/build/outputs/apk/debug/app-debug.apk
```

### iOS

#### Create the project
```bash
cd /path/to/Project-PrintNet  # Repository directory
briefcase create iOS
```

This creates the Xcode project in the `iOS/` directory.

#### Build the app
```bash
briefcase build iOS
```

#### Package for distribution
```bash
# Ad-hoc distribution (for testing)
briefcase package iOS --adhoc-sign

# App Store distribution (requires Apple Developer account and certificates)
briefcase package iOS
```

#### Run in simulator
```bash
briefcase run iOS
```

#### Deploy to device
1. Open `iOS/EON-OpenSlicer/EON-OpenSlicer.xcodeproj` in Xcode
2. Connect your iOS device
3. Select your device from the target dropdown
4. Click Run (⌘R)

## Mobile App Features

The mobile version provides a simplified interface focused on:

- **Print Job Monitoring**: View active and queued print jobs
- **Printer Status**: Check printer connectivity and status
- **Job Management**: Basic controls for managing print jobs
- **Server Connection**: Connect to the EON-OpenSlicer server

**Note**: The mobile app is designed for monitoring and light management. Full slicing and advanced features are available on the desktop version.

## Configuration

### Modifying App Metadata

Edit `pyproject.toml` to customize:
- App name and bundle identifier
- Version number
- Permissions (Android) / Info.plist entries (iOS)
- Dependencies

### Android Permissions

Current permissions (configured in `pyproject.toml`):
- `INTERNET` - For server communication
- `CAMERA` - For QR code scanning
- `READ_EXTERNAL_STORAGE` / `WRITE_EXTERNAL_STORAGE` - For file access

### iOS Permissions

Current Info.plist entries:
- `NSCameraUsageDescription` - Camera access for QR codes
- `NSPhotoLibraryUsageDescription` - Photo library for importing models

## Automated Builds (CI/CD)

The repository includes GitHub Actions workflows:

### Desktop Build
- Workflow: `.github/workflows/build.yml`
- Triggers: Push to tags matching `v*`
- Platforms: Windows, Linux

### Mobile Build
- Workflow: `.github/workflows/build-mobile.yml`
- Triggers: Push to tags matching `v*-mobile` or manual dispatch
- Platforms: Android, iOS

To trigger a mobile build:
```bash
git tag v1.0.0-mobile
git push origin v1.0.0-mobile
```

Or use the GitHub Actions UI to manually trigger the workflow.

## Distribution

### Android

1. **Google Play Store**
   - Requires a Google Play Developer account ($25 one-time fee)
   - Follow: https://play.google.com/console/about/guides/publish/
   
2. **Direct Distribution (APK)**
   - Users must enable "Install from Unknown Sources"
   - Distribute the APK file directly

3. **Enterprise Distribution**
   - Use Mobile Device Management (MDM) solutions

### iOS

1. **Apple App Store**
   - Requires Apple Developer account ($99/year)
   - Follow: https://developer.apple.com/app-store/submissions/

2. **TestFlight** (Beta Testing)
   - Free with Apple Developer account
   - Distribute to up to 10,000 testers

3. **Enterprise Distribution**
   - Requires Apple Developer Enterprise account ($299/year)
   - For internal organizational use only

## Troubleshooting

### Android Build Issues

**Problem**: `ANDROID_SDK_ROOT not set`
```bash
export ANDROID_SDK_ROOT=$HOME/Android/Sdk
```

**Problem**: Gradle build failures
```bash
# Clean and rebuild
briefcase build android --update
```

### iOS Build Issues

**Problem**: Code signing errors
- Ensure you have a valid Apple Developer account
- Use `--adhoc-sign` flag for testing

**Problem**: Python modules not found
```bash
# Update dependencies
briefcase update iOS
```

### General Issues

**Check Briefcase logs**:
```bash
briefcase build android -v  # Verbose output
briefcase build iOS --log    # Full logging
```

## Development Tips

1. **Test on actual devices** - Emulators/simulators don't always reflect real device behavior
2. **Start with debug builds** - Use `--adhoc-sign` before setting up production signing
3. **Incremental updates** - Use `briefcase update` after code changes
4. **Platform-specific code** - Use platform detection in `__main__.py` to handle platform differences

## Additional Resources

- [BeeWare Briefcase Documentation](https://briefcase.readthedocs.io/)
- [Toga Widget Toolkit](https://toga.readthedocs.io/)
- [Android Developer Guide](https://developer.android.com/guide)
- [iOS Developer Guide](https://developer.apple.com/documentation/)

## Support

For issues specific to mobile deployment, please open an issue on GitHub with:
- Platform (Android/iOS)
- Device model and OS version
- Build logs
- Steps to reproduce
