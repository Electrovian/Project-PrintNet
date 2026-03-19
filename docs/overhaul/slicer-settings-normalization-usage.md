# Slicer Settings Normalization Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T118`

## Normalize Default Sample Payload

```powershell
powershell -ExecutionPolicy Bypass -File scripts/normalize-slicer-v2-settings.ps1
```

## Normalize From JSON Settings File

```powershell
powershell -ExecutionPolicy Bypass -File scripts/normalize-slicer-v2-settings.ps1 -SettingsPath path/to/settings.json
```

## Strict Run

```powershell
powershell -ExecutionPolicy Bypass -File scripts/normalize-slicer-v2-settings.ps1 -Strict
```

## Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-settings-normalization-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-slicer-v2-settings-normalization-integration.ps1
```

## Defaults

- Keep unknown keys: `true`
- Report path: `docs/_slicer_v2_settings_normalization_report.json`
- Summary path: `docs/_slicer_v2_settings_normalization_summary.txt`
