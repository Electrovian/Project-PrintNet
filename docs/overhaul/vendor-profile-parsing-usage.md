# Vendor Profile Parsing Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T068`

## Run Parser

```powershell
powershell -ExecutionPolicy Bypass -File scripts/parse-vendor-profiles.ps1
```

## Run Parser With Vendor Limit (fast validation)

```powershell
powershell -ExecutionPolicy Bypass -File scripts/parse-vendor-profiles.ps1 -VendorLimit 5
```

## Strict Parsing Run

```powershell
powershell -ExecutionPolicy Bypass -File scripts/parse-vendor-profiles.ps1 -StrictDiscovery -StrictParsing
```

## Defaults

- Source path: `overhaul/eon_engine_mirror/resources/profiles`
- Report path: `docs/_vendor_profile_parsing_report.json`
- Summary path: `docs/_vendor_profile_parsing_summary.txt`
- Vendor limit: `0` (full parse)

## Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-vendor-profile-parsing-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-vendor-profile-parsing-integration.ps1
```
