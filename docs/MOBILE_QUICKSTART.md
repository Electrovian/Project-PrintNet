# Quick Start: Building Mobile Apps

This is a quick reference for building EON-OpenSlicer for mobile devices.

## Prerequisites

Install Briefcase:
```bash
pip install briefcase
```

## Build Commands

### Android

```bash
# One-time setup
briefcase create android

# Build and run
briefcase build android
briefcase run android

# Create distributable APK
briefcase package android --adhoc-sign
```

Output: `android/gradle/EON-OpenSlicer/app/build/outputs/apk/debug/app-debug.apk`

### iOS (macOS only)

```bash
# One-time setup
briefcase create iOS

# Build and run in simulator
briefcase build iOS
briefcase run iOS

# Create distributable IPA
briefcase package iOS --adhoc-sign
```

Output: `iOS/EON-OpenSlicer/build/`

## Install on Device

### Android
```bash
adb install path/to/app-debug.apk
```

### iOS
Open in Xcode and deploy, or:
```bash
briefcase run iOS -d "Device Name"
```

## Update After Code Changes

```bash
briefcase update android
briefcase update iOS
```

## Common Issues

**Android SDK not found**: Briefcase will download it automatically on first build

**iOS signing errors**: Use `--adhoc-sign` for testing without certificates

See `docs/MOBILE_DEPLOYMENT.md` for detailed documentation.
