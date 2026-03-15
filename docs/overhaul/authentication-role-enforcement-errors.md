# Authentication and Role Enforcement Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T364`

## Backend Auth Errors

- `BACKEND_AUTHENTICATION_ERROR` -> HTTP `401`
  - Trigger: missing token, invalid token, unresolved session.
  - Examples:
    - `AUTH_TOKEN_REQUIRED`
    - `AUTH_TOKEN_INVALID`

- `BACKEND_AUTHORIZATION_ERROR` -> HTTP `403`
  - Trigger: role lacks permission or ownership constraints fail.
  - Examples:
    - `AUTH_ROLE_DENIED`
    - `AUTH_SUBMITTER_MISMATCH`
    - `AUTH_JOB_ACCESS_DENIED`

- `BACKEND_VALIDATION_ERROR` -> HTTP `400`
  - Trigger: invalid role input or malformed request fields.
  - Example:
    - `AUTH_ROLE_INVALID`

## Frontend Auth Errors

- `FrontendAuthError`
  - Trigger: invalid role values in UI role policy helpers.

- `BackendApiError` with `AUTH_TOKEN_REQUIRED`
  - Trigger: protected frontend client methods called without `authToken`.
