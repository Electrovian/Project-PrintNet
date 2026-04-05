# Mobile Setup

This folder contains the mobile-specific setup and documentation.

Repo-wide launch and smoke instructions live in `docs/LAUNCH_READINESS.md`.

Contents:
- `requirements-mobile.txt` (Toga/Briefcase dependencies)
- `MOBILE_DEPLOYMENT.md` (full guide)
- `MOBILE_QUICKSTART.md` (short guide)
- `PLATFORM_COMPARISON.md` (feature matrix)
- `VERSION.txt` (mobile app version marker)

The authoritative launch path for the demo is the Toga/Briefcase app in `Mobile/app_mobile.py`.
The Flutter runner under `Mobile/flutter_runner/` is experimental/future work and is not the launch target for this demo window.

Quick start from the repo root:
```bash
python -m pip install -r Mobile/requirements-mobile.txt
python -m Mobile.preflight
briefcase create android
briefcase build android
briefcase package android --adhoc-sign
```

The preflight command checks that `toga` and `requests` are available, and reports whether `briefcase` is installed.
Build outputs are created by Briefcase under `android/` and `iOS/`.
