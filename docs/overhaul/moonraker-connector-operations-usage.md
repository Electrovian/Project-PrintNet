# Moonraker Connector Operations Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T308`

## Run Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-moonraker-connector-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-moonraker-connector-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-moonraker-connector-integration.ps1
```

## Defaults

- Connector type: `moonraker`
- Request timeout: `20s`
- Optional auth header: `Authorization: Bearer <token>`
- Print dispatch sequence:
  1. `connect`
  2. `upload`
  3. `start_print`
  4. optional control/status operations (`pause`, `resume`, `cancel`, `status`)
