# Connector Abstraction and Registry Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T288`

## Run Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-connector-registry-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-connector-registry-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-connector-registry-integration.ps1
```

## Defaults

- Default registry factory: `build_default_connector_registry()`
- Built-in connector types:
  - `local_file`
  - `octoprint`
  - `octoprint_legacy`
- Connector resolution precedence:
  1. `connector_type` / `connector` / `protocol`
  2. inferred `octoprint` when OctoPrint fields are present
  3. fallback `local_file`
