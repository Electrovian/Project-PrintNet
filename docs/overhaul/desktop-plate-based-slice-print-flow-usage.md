# Desktop Plate-Based Slice/Print Flow Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T268`

## Run Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-desktop-plate-flow-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-desktop-plate-flow-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-desktop-plate-flow-integration.ps1
```

## Defaults

- Plate slicing entrypoint: `slice_current_plate()`
- Plate print entrypoint: `print_current_plate()`
- Compatibility aliases:
  - `slice_current_model()`
  - `print_current_model()`
- Multi-model export filename suffix: `_plate`
- Reusable cache requirement: existing file and exact plate/settings signature match.
