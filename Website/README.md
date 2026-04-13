# Website Temp Workspace

This folder is the temporary staging location for web deliverables.

Repo-wide launch and smoke instructions live in `docs/LAUNCH_READINESS.md`.

## Launch Website in Docker

Run from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/launch-website-docker.ps1
```

The launcher:

- starts `frontend`, `backend`, `worker`, `redis`, `mongo`, and `mailpit`
- detects the current LAN URL for other devices on the same private network
- publishes the frontend over self-signed HTTPS on port `8080`
- creates or refreshes the Windows firewall rule for port `8080`
- generates QR assets and a launch manifest under `%TEMP%\printnet_website_launch_<timestamp>\`
- prints the effective email mode (`real_smtp` or `mail_capture`)

Stop services:

```powershell
docker compose down
```

If you still want to launch the stack directly without the helper:

```powershell
docker compose up --build -d frontend backend worker redis mongo mailpit
```

Local URLs:

- Frontend: `https://localhost:8080`
- Backend health: `http://localhost:8000/api/v1/health/live`
- Mail capture UI when using the default local email sink: `http://localhost:8025`

The supported LAN-sharing path is the Docker frontend on port `8080` over HTTPS. The launcher QR points at the HTTPS `/signin` entry URL. Direct backend startup stays local-only and is not the QR target.

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
