# Mobile Setup

This folder contains the mobile-specific setup and documentation.

Contents:
- `requirements-mobile.txt` (mobile dependencies)
- `MOBILE_DEPLOYMENT.md` (full guide)
- `MOBILE_QUICKSTART.md` (short guide)
- `PLATFORM_COMPARISON.md` (feature matrix)
- `VERSION.txt` (mobile app version marker)

Quick start (from repo root):
```bash
python -m pip install -r Mobile/requirements-mobile.txt
briefcase create android
briefcase build android
briefcase package android --adhoc-sign
```

Build outputs are created by Briefcase under `android/` and `iOS/`.
