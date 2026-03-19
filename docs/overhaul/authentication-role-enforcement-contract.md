# Authentication and Role Enforcement Contract

Date: 2026-02-13  
Checklist ID: `T362`

## Backend Modules

- `Website/backend/printnet_backend/authz.py`
  - `AuthContext`
  - `VALID_ROLES`
  - `normalize_role(...)`
  - `resolve_auth_context(...)`
  - `require_roles(...)`
  - `require_any_role(...)`
  - `ensure_submitter_allowed(...)`
  - `ensure_job_visible(...)`
- `Website/backend/printnet_backend/errors.py`
  - authentication/authorization error classes and HTTP mappings.
- Protected route updates:
  - `routes/auth.py` (`/auth/whoami`)
  - `routes/profiles.py`
  - `routes/printers.py`
  - `routes/jobs.py`

## Frontend Modules

- `Website/frontend/src/auth/rolePolicy.js`
  - `normalizeRole(...)`
  - `hasRequiredRole(...)`
  - `canAccessRoute(...)`
  - `allowedRoutes(...)`
- `Website/frontend/src/api/backendClient.js`
  - protected endpoint calls require `authToken`.
- `Website/frontend/src/state/usePrintNetState.js`
  - session token capture and protected request usage.

## Protected Endpoint Contract

- `/profiles/catalog` requires query `auth_token`.
- `/printers/register` requires body `auth_token` and role in `operator/admin`.
- `/printers/list` requires query `auth_token` and role in `operator/admin`.
- `/jobs/submit` requires body `auth_token`; students can only submit for own `requested_by`.
- `/jobs/status` and `/jobs/events` require query `auth_token`; students can only access own jobs.
- `/auth/whoami` requires query `auth_token`.
