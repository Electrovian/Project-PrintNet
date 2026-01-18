# Platform Comparison

This document compares EON-OpenSlicer features across different platforms.

## Feature Matrix

| Feature | Windows | Linux | macOS | iOS | Android |
|---------|---------|-------|-------|-----|---------|
| **Full 3D Slicing** | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| **STL/OBJ Import** | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| **G-Code Generation** | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| **3D Preview** | ✅ | ✅ | ⚠️ | ❌ | ❌ |
| **Print Job Monitoring** | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| **Printer Status** | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| **Job Queue Management** | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| **Server Connection** | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| **Settings Configuration** | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| **Multi-Printer Support** | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| **Crash Reporting** | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |
| **Activity Logging** | ✅ | ✅ | ⚠️ | ⚠️ | ⚠️ |

**Legend:**
- ✅ Full Support
- ⚠️ Planned/Partial Support
- ❌ Not Available

## Platform Details

### Windows Desktop ✅
**Status:** Fully Supported (Primary Platform)

**Capabilities:**
- Complete 3D slicing engine with all features
- Full PyQt5 GUI with all panels and controls
- Direct printer communication
- File system access for STL/OBJ files
- Advanced settings and configuration
- Performance optimized for desktop hardware

**Requirements:**
- Windows 10 or later
- Python 3.12+
- 4GB RAM minimum, 8GB recommended
- Graphics card with OpenGL support

**Distribution:**
- Standalone `.exe` via PyInstaller
- No Python installation required for end users
- Available in GitHub Releases

---

### Linux Desktop ✅
**Status:** Fully Supported

**Capabilities:**
- All Windows features
- Native Linux integration
- Terminal and GUI modes

**Requirements:**
- Ubuntu 20.04+, Debian 11+, or equivalent
- Python 3.12+
- X11 or Wayland
- Qt dependencies: `sudo apt-get install python3-pyqt5`

**Distribution:**
- Standalone binary via PyInstaller
- AppImage format (planned)
- Available in GitHub Releases

---

### macOS Desktop ⚠️
**Status:** Planned (Not Yet Implemented)

**Capabilities (When Implemented):**
- All desktop features
- Native macOS UI integration
- Apple Silicon (M1/M2) support

**Requirements:**
- macOS 11 (Big Sur) or later
- Python 3.12+

**Distribution (Planned):**
- `.dmg` installer via Briefcase
- App Store distribution (future consideration)

---

### iOS Mobile ✅
**Status:** Beta (Monitoring/Management Only)

**Capabilities:**
- View print job queue
- Monitor printer status
- Basic job management (pause/resume/cancel)
- Server connectivity
- Push notifications (planned)

**Limitations:**
- No 3D slicing (use desktop for slicing)
- No file import (server-based only)
- Limited settings configuration
- Requires server connection

**Requirements:**
- iOS 13.0 or later
- iPhone or iPad
- Network connection to EON-OpenSlicer server

**Distribution:**
- Ad-hoc IPA for testing
- TestFlight for beta testing
- App Store submission (planned)

---

### Android Mobile ✅
**Status:** Beta (Monitoring/Management Only)

**Capabilities:**
- View print job queue
- Monitor printer status
- Basic job management (pause/resume/cancel)
- Server connectivity
- Push notifications (planned)

**Limitations:**
- No 3D slicing (use desktop for slicing)
- No file import (server-based only)
- Limited settings configuration
- Requires server connection

**Requirements:**
- Android 5.0 (API 21) or later
- Phone or tablet
- Network connection to EON-OpenSlicer server

**Distribution:**
- APK for direct installation
- Google Play Store (planned)
- F-Droid (under consideration)

---

## UI Framework Differences

### Desktop (Windows, Linux, macOS)
**Framework:** PyQt5

**Advantages:**
- Rich widget library
- Native performance
- Advanced graphics (OpenGL)
- Complex layouts and interactions
- Mature and stable

**Use Case:** Full-featured application

---

### Mobile (iOS, Android)
**Framework:** Toga (BeeWare)

**Advantages:**
- Native mobile widgets
- Cross-platform consistency
- Touch-optimized
- Lightweight
- Modern Python-native API

**Use Case:** Monitoring and basic management

---

## Use Case Recommendations

### Desktop Application (Windows/Linux)
**Best For:**
- 3D model slicing and preparation
- Advanced configuration and settings
- Direct printer management
- Full-featured workflow
- Power users and lab operators

**Workflow:**
1. Import 3D models (STL/OBJ)
2. Configure print settings
3. Generate G-code
4. Send to printer or save
5. Monitor print progress

---

### Mobile Application (iOS/Android)
**Best For:**
- Monitoring prints on the go
- Quick status checks
- Basic job management
- Lab technicians and students
- Remote monitoring

**Workflow:**
1. Connect to server
2. View job queue
3. Check printer status
4. Pause/resume/cancel jobs
5. Receive notifications (planned)

---

## Deployment Scenarios

### Scenario 1: Personal Use
- **Setup:** Desktop app only
- **Use Case:** Individual user with local printer
- **Platforms:** Windows or Linux

### Scenario 2: Lab Environment
- **Setup:** Desktop apps + Server + Mobile apps
- **Use Case:** University 3D print lab
- **Platforms:** 
  - Lab stations: Windows/Linux desktop
  - Server: Linux
  - Staff/Students: iOS/Android mobile

### Scenario 3: Remote Monitoring
- **Setup:** Server + Mobile apps
- **Use Case:** Check print status remotely
- **Platforms:** iOS/Android mobile

---

## Roadmap

### Short Term (Current)
- [x] Windows desktop support
- [x] Linux desktop support
- [x] iOS mobile beta
- [x] Android mobile beta
- [x] Basic server integration

### Medium Term (Next 6 months)
- [ ] macOS desktop support
- [ ] Mobile push notifications
- [ ] Enhanced mobile UI
- [ ] Camera integration for monitoring
- [ ] QR code printer pairing

### Long Term (Future)
- [ ] Web interface
- [ ] Cloud slicing service
- [ ] App Store/Play Store distribution
- [ ] Collaborative features
- [ ] Advanced mobile features

---

## Migration Guide

### From Desktop to Mobile
Mobile apps complement desktop apps; they don't replace them. Use mobile for monitoring prints that were prepared on desktop.

**Desktop remains necessary for:**
- Model import and slicing
- Advanced configuration
- G-code generation

**Mobile is great for:**
- Checking print status
- Managing job queue
- Receiving alerts

### Setting Up Multi-Platform Environment

1. **Install desktop app** (Windows/Linux)
2. **Configure server** (if using networked setup)
3. **Install mobile app** (iOS/Android)
4. **Connect mobile to server**
5. **Sync printers and settings**

---

## Technical Architecture

### Desktop Architecture
```
┌─────────────────────────────────────┐
│         PyQt5 GUI Layer            │
├─────────────────────────────────────┤
│       Business Logic Layer         │
│  (Slicer, Config, Integrations)   │
├─────────────────────────────────────┤
│      Platform Services Layer       │
│   (File I/O, Printer Comm, etc.)  │
└─────────────────────────────────────┘
```

### Mobile Architecture
```
┌─────────────────────────────────────┐
│         Toga UI Layer              │
├─────────────────────────────────────┤
│    Simplified Business Logic       │
│  (Server Client, Job Management)   │
├─────────────────────────────────────┤
│      Mobile Platform Services      │
│   (Notifications, Camera, etc.)    │
└─────────────────────────────────────┘
```

### Unified Entry Point
```python
App/__main__.py
    ├── Detects platform
    ├── iOS/Android → app_mobile.py (Toga)
    └── Windows/Linux/macOS → main.py (PyQt5)
```

---

## Support and Feedback

We welcome feedback on platform-specific features and issues!

- **Desktop Issues:** [GitHub Issues](https://github.com/Electrovian/Project-EON-OpenSlicer/issues)
- **Mobile Issues:** [GitHub Issues](https://github.com/Electrovian/Project-EON-OpenSlicer/issues) (tag with "mobile")
- **Feature Requests:** [GitHub Discussions](https://github.com/Electrovian/Project-EON-OpenSlicer/discussions)

---

## Frequently Asked Questions

**Q: Can I slice 3D models on my phone?**
A: Not currently. Mobile apps are designed for monitoring and management. Use the desktop app for slicing.

**Q: Do I need a server for the mobile app?**
A: Yes, mobile apps connect to a server to access print job data and printer status.

**Q: Will macOS be supported?**
A: Yes, it's planned. The framework (PyQt5/Briefcase) supports macOS.

**Q: Can I use the mobile app offline?**
A: Not currently. Mobile apps require server connection. Offline mode is under consideration.

**Q: Why different UI frameworks (PyQt5 vs Toga)?**
A: PyQt5 doesn't have good mobile support. Toga is designed for mobile and provides native widgets on iOS/Android.

**Q: Will mobile apps support all desktop features eventually?**
A: No. Complex features like 3D slicing are better suited for desktop. Mobile focuses on monitoring and basic management.
