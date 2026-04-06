# Backend FastAPI Modular Monolith

This folder contains the backend modular monolith skeleton for Project PrintNet.

## Layout

- `printnet_backend/app.py`: app factory and router registration.
- `printnet_backend/routes/`: modular API routers.
- `printnet_backend/services.py`: in-memory service layer for MVP scaffolding.
- `printnet_backend/orchestration.py`: queue/worker orchestration primitives.
- `printnet_backend/observability.py`: observability counters, audit redaction, release-readiness checks.
- `printnet_backend/settings.py`: env-backed settings contract.
- `printnet_backend/errors.py`: backend error taxonomy and HTTP mapping.
- `printnet_backend/compat.py`: FastAPI compatibility shim used when FastAPI is not installed.
- `scripts/worker_smoke.py`: short backend + worker launch smoke entrypoint.

## Run Local

```powershell
cd Website/backend
python -m pip install -r requirements.txt
python main.py
```

If `fastapi` and `uvicorn` are installed, this starts the HTTP server on `127.0.0.1:8000`.
If not installed, the compatibility layer still allows test automation to run.

This direct backend path is local-only. For LAN website sharing, QR generation, and email-capture defaults, use the repository-root Docker launcher in `scripts/launch-website-docker.ps1`.

## Runtime Data

Runtime uploads are written under `Website/backend/runtime/uploads` by default.
Legacy `Website/backend/uploads` paths are normalized to the runtime directory so new launch and smoke runs do not write into tracked source-tree locations.

## Worker Smoke

```powershell
cd Website/backend
python scripts/worker_smoke.py
```

This starts the backend, waits for the live health endpoint, runs the worker for one cycle, and asserts the expected startup and cycle output.
