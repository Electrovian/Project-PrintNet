# Build Instructions

## Desktop (Windows/Linux)

```bash
python -m pip install -r App/requirements.txt
python -m pip install pyinstaller
pyinstaller --onefile --windowed App/main.py
```

## Mobile (Android)

```bash
python -m pip install -r Mobile/requirements-mobile.txt
python -m Mobile.preflight
briefcase create android
briefcase build android
briefcase package android --adhoc-sign
```

## Mobile (iOS, macOS only)

```bash
python -m pip install -r Mobile/requirements-mobile.txt
python -m Mobile.preflight
briefcase create iOS
briefcase build iOS
briefcase package iOS --adhoc-sign
```

## Notes

- Desktop builds remain unchanged and use the PyQt5 UI.
- Mobile builds use the Toga UI for monitoring and job control only.
- Mobile apps require a backend server connection for slicing and job data.
- Run `python -m Mobile.preflight` before packaging to catch missing Python dependencies early.
