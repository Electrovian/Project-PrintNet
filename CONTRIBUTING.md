# Contributing to Mobile Development

Thank you for your interest in contributing to EON-OpenSlicer's mobile platform support!

## Development Setup

### For Desktop Development
```bash
git clone https://github.com/Electrovian/Project-EON-OpenSlicer.git
cd Project-EON-OpenSlicer
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r App/requirements.txt
```

### For Mobile Development
```bash
pip install -r requirements-mobile.txt
```

## Architecture Overview

The project uses a unified codebase with platform-specific entry points:

```
App/
├── __main__.py          # Unified entry point (platform detection)
├── main.py              # Desktop entry point (PyQt5)
├── app_mobile.py        # Mobile entry point (Toga)
├── gui/                 # Desktop GUI components (PyQt5)
├── slicer/              # Core slicing engine (platform-agnostic)
├── config/              # Configuration (platform-agnostic)
└── integrations/        # External integrations (platform-agnostic)
```

### Platform Detection

`App/__main__.py` automatically detects the platform and loads:
- **Desktop (Windows, Linux, macOS)**: Loads `main.py` with PyQt5
- **Mobile (iOS, Android)**: Loads `app_mobile.py` with Toga

## Code Structure

### Shared Code (Platform-Agnostic)
The following modules work across all platforms:
- `slicer/` - Core 3D slicing algorithms
- `config/` - Configuration management
- `integrations/` - API and printer integrations

### Desktop-Only Code
- `gui/` - PyQt5-based UI components
- `main.py` - Desktop application entry point

### Mobile-Only Code
- `app_mobile.py` - Toga-based mobile UI
- Limited to monitoring and basic controls

## Making Changes

### For Desktop Features
1. Make changes in `App/gui/` or `App/main.py`
2. Test with: `cd App && python main.py`
3. Ensure changes don't break core algorithms in `slicer/`

### For Mobile Features
1. Make changes in `App/app_mobile.py`
2. Test with: `briefcase dev` or `python app_mobile.py`
3. Test on actual devices when possible

### For Shared Features
1. Make changes in `slicer/`, `config/`, or `integrations/`
2. Test on both desktop and mobile platforms
3. Ensure no platform-specific dependencies are introduced

## Testing

### Desktop Testing
```bash
cd App
python -m pytest Tests/
```

### Mobile Testing
```bash
# Run in development mode
briefcase dev

# Build and test Android
briefcase run android

# Build and test iOS (macOS only)
briefcase run iOS
```

## Building for Distribution

### Desktop Builds
See `.github/workflows/build.yml` for automated builds, or:

**Windows:**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name EON-OpenSlicer App/main.py
```

**Linux:**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name EON-OpenSlicer App/main.py
```

### Mobile Builds
See `.github/workflows/build-mobile.yml` for automated builds, or:

**Android:**
```bash
briefcase create android
briefcase build android
briefcase package android --adhoc-sign
```

**iOS:**
```bash
briefcase create iOS
briefcase build iOS
briefcase package iOS --adhoc-sign
```

## Pull Request Guidelines

### Before Submitting
1. Test your changes on the target platform(s)
2. Run existing tests: `python -m pytest App/Tests/`
3. Update documentation if adding features
4. Follow existing code style

### PR Description Should Include
- What platform(s) are affected
- What was changed and why
- Testing performed
- Screenshots for UI changes

### Review Process
- Desktop changes: Test on Windows and Linux
- Mobile changes: Test on iOS and Android if possible
- Shared code: Test on all platforms

## Common Scenarios

### Adding a New UI Feature (Desktop)
1. Add UI components in `App/gui/`
2. Update `App/gui/main_window.py` to integrate
3. Test with: `python App/main.py`
4. Add tests in `App/Tests/`

### Adding a New UI Feature (Mobile)
1. Add UI components in `App/app_mobile.py`
2. Use Toga widgets (Button, Label, Box, etc.)
3. Test with: `briefcase dev`
4. Test on device: `briefcase run android` or `briefcase run iOS`

### Adding a New Slicer Algorithm
1. Add implementation in `App/slicer/`
2. Ensure no platform-specific dependencies
3. Add tests in `App/Tests/`
4. Test on both desktop and mobile

### Updating Dependencies

**Desktop dependencies:** Update `App/requirements.txt`
```bash
pip freeze > App/requirements.txt  # After adding new packages
```

**Mobile dependencies:** Update `requirements-mobile.txt` AND `pyproject.toml`
```toml
[tool.briefcase.app.eon_openslicer.android]
requires = [
    "toga>=0.4.0",
    "your-new-package>=1.0.0",
]
```

## Platform-Specific Considerations

### Android
- Minimum API Level 21 (Android 5.0)
- Test on both phone and tablet form factors
- Consider touch-based interactions
- File access requires permissions

### iOS
- Minimum iOS 13.0
- Test on both iPhone and iPad
- App Store guidelines apply
- Code signing required for device testing

### Windows
- Test on Windows 10 and 11
- Ensure PyQt5 dependencies are met
- Antivirus may flag built executables (false positive)

### Linux
- Test on Ubuntu/Debian-based distros
- Qt system dependencies may be required
- Provide `.desktop` files for integration

## Resources

- [BeeWare Documentation](https://docs.beeware.org/)
- [Toga Widget Reference](https://toga.readthedocs.io/)
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Build Instructions](BUILD_INSTRUCTIONS.md)
- [Mobile Deployment Guide](docs/MOBILE_DEPLOYMENT.md)

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Open a GitHub Issue with:
  - Platform and OS version
  - Python version
  - Steps to reproduce
  - Expected vs actual behavior
- **Features**: Open a GitHub Issue describing the use case

## Code of Conduct

Please be respectful and constructive in all interactions. We're all here to make EON-OpenSlicer better for everyone.

Thank you for contributing! 🎉
