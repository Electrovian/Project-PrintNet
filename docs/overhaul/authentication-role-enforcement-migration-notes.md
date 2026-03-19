# Authentication and Role Enforcement Migration Notes

Date: 2026-02-13  
Checklist ID: `T369`

## Legacy Baseline

- Session creation existed but protected routes did not enforce auth context.
- Printer and job operations were callable without role checks.
- Frontend route availability did not account for role capabilities.

## Current Baseline

- Session token is now required for protected API calls.
- Role enforcement is applied to printer and job route domains.
- Student ownership restrictions are enforced for job submit/status/events.
- Frontend includes explicit role policy contracts and protected client-call token requirements.

## Migration Impact

- Existing callers must pass `auth_token` to protected backend endpoints.
- Client code must ensure session acquisition before protected operations.
- Role-based UX can now hide/disable privileged routes predictably.
