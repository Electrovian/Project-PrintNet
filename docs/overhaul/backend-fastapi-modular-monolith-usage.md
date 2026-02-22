# Backend FastAPI Modular Monolith Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T348`

## Run Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-backend-fastapi-monolith-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-backend-fastapi-monolith-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-backend-fastapi-monolith-integration.ps1
```

## Run Backend Entry Point

```powershell
cd Website/backend
python main.py
```

## Defaults

- App name: `EON-OpenSlicer Backend`
- API prefix: `/api/v1`
- Default role: `student`
- Queue name: `default`
- Unit budget: `25s`
- Integration budget: `25s`
- Smoke report paths:
  - `docs/_backend_fastapi_monolith_report.json`
  - `docs/_backend_fastapi_monolith_summary.txt`

## Notes

- If `fastapi` and `uvicorn` are installed, the app runs as a real HTTP server.
- If not installed, compatibility mode still allows automation and regression checks.
