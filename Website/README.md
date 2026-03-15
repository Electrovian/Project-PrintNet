# Website Temp Workspace

This folder is the temporary staging location for web deliverables.

## Launch Website in Docker

Run from the repository root:

```powershell
docker compose up --build -d frontend backend worker redis mongo
```

Open:

- Frontend: `http://localhost:8080`
- Backend health: `http://localhost:8000/api/v1/health/live`

Stop services:

```powershell
docker compose down
```

Optional helper script:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/launch-website-docker.ps1
```

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
