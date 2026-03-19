# Website Temp Workspace

This folder is the temporary staging location for web deliverables.

To avoid copy-paste drift, the Flutter runner and shared logic live in:

- `Mobile/flutter_runner/`
- Shared package: `Mobile/flutter_runner/packages/eon_shared`
- App entrypoint: `Mobile/flutter_runner/apps/eon_mobile`

Use the same app target for both mobile and web:

```powershell
cd Mobile/flutter_runner/apps/eon_mobile
flutter pub get
flutter run -d chrome
```

For Android/iOS:

```powershell
flutter run -d android
flutter run -d ios
```
