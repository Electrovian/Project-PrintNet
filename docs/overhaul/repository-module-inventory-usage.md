# Repository Module Inventory Usage and Defaults

Date: 2026-02-13
Checklist ID: `T018`

## Generator Command

```powershell
powershell -ExecutionPolicy Bypass -File scripts/generate-module-inventory.ps1
```

## Parameters

- `-AppRoot` default: `App`
- `-OutputDir` default: `docs`

## Output Files

- `docs/_app_file_inventory.txt`
- `docs/_app_import_inventory.txt`
- `docs/_app_slicer_connect_inventory.txt`

## Validation Command

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-module-inventory.ps1
```

## Validation Defaults

- `-MaxSeconds` default runtime budget: `20`
- Fails if inventory files are missing headers or empty payloads.
