# Build Instructions

Complete instructions for building EON-OpenSlicer for all supported platforms.

## Table of Contents
1. [Desktop Builds (Windows, Linux)](#desktop-builds)
2. [Mobile Builds (iOS, Android)](#mobile-builds)
3. [Development Setup](#development-setup)

---

## Desktop Builds

The desktop application uses PyQt5 for a full-featured 3D printing management experience.

### Windows

#### Using PyInstaller (Current Method)

1. **Install dependencies**:
   ```bash
   pip install -r App/requirements.txt
   pip install pyinstaller
   ```

2. **Build executable**:
   ```bash
   pyinstaller --noconfirm --clean --onefile --windowed ^
     --name EON-OpenSlicer ^
     --paths App ^
     --add-data "App/assets;assets" ^
     App/main.py
   ```

3. **Output**: `dist/EON-OpenSlicer.exe`

#### Using Briefcase (Alternative)

1. **Install Briefcase**:
   ```bash
   pip install briefcase
   ```

2. **Build**:
   ```bash
   briefcase create windows
   briefcase build windows
   briefcase package windows
   ```

### Linux

#### Using PyInstaller (Current Method)

1. **Install dependencies**:
   ```bash
   pip install -r App/requirements.txt
   pip install pyinstaller
   ```

2. **Build executable**:
   ```bash
   pyinstaller --noconfirm --clean --onefile --windowed \
     --name EON-OpenSlicer \
     --paths App \
     --add-data "App/assets:assets" \
     App/main.py
   ```

3. **Output**: `dist/EON-OpenSlicer`

#### Using Briefcase (Alternative)

1. **Install system dependencies**:
   ```bash
   sudo apt-get install python3-dev libgirepository1.0-dev
   ```

2. **Build**:
   ```bash
   pip install briefcase
   briefcase create linux
   briefcase build linux
   briefcase package linux
   ```

---

## Mobile Builds

The mobile application uses Toga for a lightweight, native mobile interface.

### Prerequisites

Both platforms:
```bash
pip install -r requirements-mobile.txt
```

### Android

#### Requirements
- Java JDK 17+
- Android SDK (automatically installed by Briefcase)

#### Build Steps

1. **Create Android project**:
   ```bash
   briefcase create android
   ```
   
   This will:
   - Download Android SDK if needed
   - Create the Gradle project structure
   - Set up Android app scaffolding

2. **Build the app**:
   ```bash
   briefcase build android
   ```

3. **Run in emulator** (for testing):
   ```bash
   briefcase run android
   ```

4. **Package for distribution**:
   ```bash
   # Debug build (for testing)
   briefcase package android --adhoc-sign
   
   # Release build (requires signing configuration)
   briefcase package android
   ```

5. **Output**: 
   - Debug APK: `android/gradle/EON-OpenSlicer/app/build/outputs/apk/debug/app-debug.apk`
   - Release APK: `android/gradle/EON-OpenSlicer/app/build/outputs/apk/release/app-release.apk`

#### Installing on Device

Via ADB:
```bash
adb devices  # Verify device is connected
adb install path/to/app-debug.apk
```

Or via Briefcase:
```bash
briefcase run android -d "Device Name"
```

### iOS

#### Requirements
- **macOS only**
- Xcode 14+ (from Mac App Store)
- Xcode Command Line Tools
- Apple Developer account (for device testing and distribution)

#### Build Steps

1. **Install Xcode Command Line Tools**:
   ```bash
   xcode-select --install
   ```

2. **Create iOS project**:
   ```bash
   briefcase create iOS
   ```
   
   This creates an Xcode project with proper iOS scaffolding.

3. **Build the app**:
   ```bash
   briefcase build iOS
   ```

4. **Run in simulator**:
   ```bash
   briefcase run iOS
   ```
   
   Or specify a simulator:
   ```bash
   briefcase run iOS -d "iPhone 15 Pro"
   ```

5. **Package for distribution**:
   ```bash
   # Ad-hoc build (for testing without App Store)
   briefcase package iOS --adhoc-sign
   
   # App Store build (requires certificates and provisioning profiles)
   briefcase package iOS
   ```

6. **Output**: 
   - `.app` file in `iOS/EON-OpenSlicer/build/`
   - `.ipa` file after packaging

#### Installing on Device

Via Xcode:
1. Open `iOS/EON-OpenSlicer/EON-OpenSlicer.xcodeproj`
2. Connect your iOS device
3. Select device from scheme menu
4. Click Run (⌘R)

Via Briefcase:
```bash
briefcase run iOS -d "Your Device Name"
```

---

## Development Setup

### Desktop Development

1. **Clone repository**:
   ```bash
   git clone https://github.com/Electrovian/Project-EON-OpenSlicer.git
   cd Project-EON-OpenSlicer
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/macOS
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r App/requirements.txt
   ```

4. **Run application**:
   ```bash
   cd App
   python main.py
   ```

### Mobile Development

1. **Install mobile requirements**:
   ```bash
   pip install -r requirements-mobile.txt
   ```

2. **Run in development mode**:
   ```bash
   briefcase dev
   ```
   
   This runs the app using Toga's development mode.

3. **Test mobile UI**:
   ```bash
   cd App
   python app_mobile.py
   ```

---

## Updating After Code Changes

### Desktop
Rebuild with PyInstaller:
```bash
pyinstaller EON-OpenSlicer.spec  # If spec file exists
```

### Mobile
Update and rebuild:
```bash
# Android
briefcase update android
briefcase build android

# iOS
briefcase update iOS
briefcase build iOS
```

---

## Automated Builds (GitHub Actions)

### Desktop CI/CD
- **Workflow**: `.github/workflows/build.yml`
- **Trigger**: Push tags matching `v*`
- **Platforms**: Windows, Linux
- **Output**: Zipped executables

### Mobile CI/CD
- **Workflow**: `.github/workflows/build-mobile.yml`
- **Trigger**: Push tags matching `v*-mobile` or manual dispatch
- **Platforms**: Android, iOS
- **Output**: APK, AAB (Android), IPA (iOS)

### Triggering Builds

Desktop release:
```bash
git tag v1.0.0
git push origin v1.0.0
```

Mobile release:
```bash
git tag v1.0.0-mobile
git push origin v1.0.0-mobile
```

---

## Troubleshooting

### Desktop Issues

**Missing PyQt5**:
```bash
pip install --force-reinstall PyQt5
```

**OpenGL errors on Linux**:
```bash
sudo apt-get install libgl1-mesa-glx
```

### Mobile Issues

**Android SDK not found**:
- Briefcase will download it automatically
- Or set `ANDROID_SDK_ROOT` environment variable

**iOS code signing**:
- Use `--adhoc-sign` for testing
- For App Store: Configure in Xcode

**Gradle build failures**:
```bash
briefcase build android --update --clean
```

**Module import errors**:
- Check `pyproject.toml` dependencies
- Run `briefcase update` to refresh

---

## Platform-Specific Notes

### Windows
- Requires Visual C++ Redistributable for end users
- Antivirus may flag the exe (false positive)

### Linux
- May need to install Qt dependencies system-wide
- `.desktop` files can be created for app launchers

### Android
- Minimum API level: 21 (Android 5.0)
- Target API level: 34 (Android 14)
- Requires ~500MB for Android SDK

### iOS
- Minimum iOS version: 13.0
- Requires macOS for building
- App Store requires annual $99 developer fee

---

## Additional Resources

- [PyInstaller Documentation](https://pyinstaller.org/)
- [Briefcase Documentation](https://briefcase.readthedocs.io/)
- [Toga Documentation](https://toga.readthedocs.io/)
- [Android Developer Guide](https://developer.android.com/)
- [iOS Developer Guide](https://developer.apple.com/)

## Getting Help

For build issues:
1. Check this document
2. Review `docs/MOBILE_DEPLOYMENT.md`
3. Open an issue on GitHub with:
   - Platform and OS version
   - Python version
   - Full build logs
   - Steps to reproduce
