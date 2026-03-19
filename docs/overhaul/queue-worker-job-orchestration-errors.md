# Queue Worker and Job Orchestration Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T374`

## Backend Errors

- `BACKEND_VALIDATION_ERROR` -> HTTP `400`
  - Trigger: invalid `max_jobs`, missing `worker_id`, invalid queue settings.

- `BACKEND_AUTHENTICATION_ERROR` -> HTTP `401`
  - Trigger: missing/invalid `auth_token` on queue endpoints.

- `BACKEND_AUTHORIZATION_ERROR` -> HTTP `403`
  - Trigger: student attempts worker heartbeat/tick.

- `BACKEND_ORCHESTRATION_ERROR` -> HTTP `503`
  - Trigger: queue worker processing failure or invalid job state transitions during tick.

- `BACKEND_NOT_FOUND` -> HTTP `404`
  - Trigger: missing job/printer references during lifecycle operations.

## Frontend Errors

- `BackendApiError("AUTH_TOKEN_REQUIRED")`
  - Trigger: queue client methods invoked without session token.
