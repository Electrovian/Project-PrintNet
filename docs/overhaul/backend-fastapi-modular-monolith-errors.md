# Backend FastAPI Modular Monolith Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T344`

## Domain Errors

- `BACKEND_VALIDATION_ERROR` -> HTTP `400`
  - Trigger: malformed/invalid payloads or missing required fields.
  - Example: missing `user_id`, invalid `connector_type`, missing `profile_id`.

- `BACKEND_NOT_FOUND` -> HTTP `404`
  - Trigger: requested profile/printer/job does not exist.
  - Example: `JOB_NOT_FOUND`, `JOB_PROFILE_NOT_FOUND`, `JOB_PRINTER_NOT_FOUND`.

- `BACKEND_CONFLICT` -> HTTP `409`
  - Trigger: duplicate resource insertion.
  - Example: duplicate `printer_id` on register.

- `BACKEND_INTERNAL_ERROR` -> HTTP `500`
  - Trigger: unexpected unhandled backend exception.

## Guard/Error Cases

- `SESSION_USER_ID_REQUIRED`
- `PRINTER_ID_REQUIRED`
- `PRINTER_NAME_REQUIRED`
- `PRINTER_CONNECTOR_INVALID`
- `PRINTER_ENDPOINT_REQUIRED`
- `JOB_MODEL_NAME_REQUIRED`
- `JOB_PROFILE_ID_REQUIRED`
- `JOB_REQUESTED_BY_REQUIRED`
- `JOB_ID_REQUIRED`
