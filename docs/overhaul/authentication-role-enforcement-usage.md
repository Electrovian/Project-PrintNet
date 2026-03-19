# Authentication and Role Enforcement Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T368`

## Run Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-auth-role-enforcement-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-auth-role-enforcement-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-auth-role-enforcement-integration.ps1
```

## Defaults

- Valid roles:
  - `student`
  - `operator`
  - `admin`
- Protected endpoints require `auth_token`.
- Student restrictions:
  - cannot register/list printers
  - can submit jobs only for own identity
  - can view only own jobs/events
- Unit runtime budget: `30s`
- Integration runtime budget: `30s`
- Smoke report paths:
  - `docs/_auth_role_enforcement_report.json`
  - `docs/_auth_role_enforcement_summary.txt`
