# OctoPrint Connector Operations Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T298`

## Run Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-octoprint-connector-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-octoprint-connector-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-octoprint-connector-integration.ps1
```

## Defaults

- Connector type: `octoprint`
- Request timeout: `20s`
- Auth header: `X-Api-Key`
- Print dispatch sequence:
  1. `connect`
  2. `upload`
  3. `start_print`
  4. optional control/status operations (`pause`, `resume`, `cancel`, `status`)
