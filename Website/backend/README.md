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

## Run Local

```powershell
cd Website/backend
python -m pip install -r requirements.txt
python main.py
```

If `fastapi` and `uvicorn` are installed, this starts the HTTP server on `127.0.0.1:8000`.
If not installed, the compatibility layer still allows test automation to run.
