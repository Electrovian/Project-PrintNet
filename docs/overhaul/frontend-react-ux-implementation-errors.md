# Frontend React UX Implementation Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T354`

## Frontend Contract Errors

- `CONTACT_NAME_REQUIRED`
- `CONTACT_EMAIL_REQUIRED`
- `CONTACT_EMAIL_INVALID`
- `CONTACT_PHONE_REQUIRED`
- `MODEL_NAME_REQUIRED`
- `PROFILE_ID_REQUIRED`
- `REQUESTED_BY_REQUIRED`
- `SESSION_USER_ID_REQUIRED`
- `PRINTER_ID_REQUIRED`
- `PRINTER_NAME_REQUIRED`
- `PRINTER_CONNECTOR_REQUIRED`
- `PRINTER_ENDPOINT_REQUIRED`

Handling:
- Raised as `FrontendContractError` during frontend payload normalization.
- Call sites should surface the error message to users and block invalid requests.

## Backend API Errors

- `FETCH_UNAVAILABLE`
  - Trigger: fetch function is unavailable.
- `BACKEND_API_ERROR` and backend-sourced codes
  - Trigger: non-2xx API response.

Handling:
- Raised as `BackendApiError` with `code`, `detail`, and `status`.
- UI state layer writes failure text into status line and preserves form input.
