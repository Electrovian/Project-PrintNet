# Profile-to-Internal Settings Mapping Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T088`

## Run Mapping

```powershell
powershell -ExecutionPolicy Bypass -File scripts/map-profile-settings.ps1
```

## Bounded Integration Run

```powershell
powershell -ExecutionPolicy Bypass -File scripts/map-profile-settings.ps1 -VendorLimit 5
```

## Strict Run

```powershell
powershell -ExecutionPolicy Bypass -File scripts/map-profile-settings.ps1 -StrictDiscovery -StrictInheritance -StrictMapping
```

## Defaults

- Source path: `overhaul/eon_engine_mirror/resources/profiles`
- Report path: `docs/_profile_settings_mapping_report.json`
- Summary path: `docs/_profile_settings_mapping_summary.txt`
- Vendor limit: `0` (full set)
- Max chain depth: `64`

## Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-profile-settings-mapping-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-profile-settings-mapping-integration.ps1
```
