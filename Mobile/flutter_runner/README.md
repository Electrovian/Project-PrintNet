# Flutter Runner (Experimental)

This workspace is an experimental Flutter runner layout that may be used for future shared mobile and web work.

It is not the authoritative launch path for the April 2026 demo.

Structure:

- `apps/eon_mobile`: app shell entrypoint
- `packages/eon_shared`: shared domain/process code

Quick start:

```powershell
cd Mobile/flutter_runner/apps/eon_mobile
flutter pub get
flutter run -d chrome
```

Mobile targets:

```powershell
flutter run -d android
flutter run -d ios
```

Use this runner only as future/experimental work. The current supported mobile launch path is the Toga/Briefcase app in `Mobile/app_mobile.py`.
