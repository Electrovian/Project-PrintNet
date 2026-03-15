# PrusaLink Connector Operations Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T318`

## Run Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-prusalink-connector-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-prusalink-connector-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-prusalink-connector-integration.ps1
```

## Defaults

- Connector type: `prusalink`
- Request timeout: `20s`
- Auth header: `X-Api-Key`
- Print dispatch sequence:
  1. `connect`
  2. `upload`
  3. `start_print`
  4. optional control/status operations (`pause`, `resume`, `cancel`, `status`)
