# Backend FastAPI Modular Monolith Contract

Date: 2026-02-13  
Checklist ID: `T342`

## Core Modules

- `Website/backend/printnet_backend/app.py`
  - `create_app(settings=None, state=None)`
- `Website/backend/printnet_backend/settings.py`
  - `BackendSettings`
- `Website/backend/printnet_backend/errors.py`
  - backend exception classes and HTTP mapping
- `Website/backend/printnet_backend/services.py`
  - `BackendState` in-memory domain service
- `Website/backend/printnet_backend/routes/`
  - `health.py`
  - `auth.py`
  - `profiles.py`
  - `printers.py`
  - `jobs.py`
- `Website/backend/printnet_backend/compat.py`
  - real FastAPI usage when available
  - compatibility fallback for environments without FastAPI

## Endpoint Contract (`/api/v1`)

- `GET /health/live`
- `GET /health/ready`
- `POST /auth/session`
- `GET /profiles/catalog`
- `POST /printers/register`
- `GET /printers/list`
- `POST /jobs/submit`
- `GET /jobs/status`
- `GET /jobs/events`

## Payload/Response Contract

- Session create request:
  - `user_id`
  - `role` (optional, default `student`)
- Printer register request:
  - `printer_id`
  - `name`
  - `connector_type`
  - `endpoint`
- Job submit request:
  - `model_name`
  - `profile_id`
  - `requested_by`
  - `printer_id` (optional)
- Error response:
  - `{ "ok": false, "error": { "code": "...", "detail": "..." } }`
