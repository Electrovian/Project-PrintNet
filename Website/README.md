# Website Temp Workspace

This folder is the temporary staging location for web deliverables.

Repo-wide launch and smoke instructions live in `docs/LAUNCH_READINESS.md`.

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

The supported mobile launch path for this demo is the Toga/Briefcase app in `Mobile/app_mobile.py`.
The Flutter runner under `Mobile/flutter_runner/` is experimental/future work and should not be treated as the launch target.

If you are working on the experimental Flutter runner, the shared logic lives in:

- `Mobile/flutter_runner/`
- Shared package: `Mobile/flutter_runner/packages/eon_shared`
- App entrypoint: `Mobile/flutter_runner/apps/eon_mobile`

Experimental Flutter web/mobile targets:

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
