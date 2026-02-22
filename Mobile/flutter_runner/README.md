# Flutter Runner (Shared Mobile + Web)

This workspace is a temporary Flutter runner layout that shares logic across:

- Android
- iOS
- Web

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
