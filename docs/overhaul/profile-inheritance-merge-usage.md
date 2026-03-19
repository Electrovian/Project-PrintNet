# Profile Inheritance and Merge Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T078`

## Run Inheritance Resolution

```powershell
powershell -ExecutionPolicy Bypass -File scripts/resolve-profile-inheritance.ps1
```

## Bounded Integration Run

```powershell
powershell -ExecutionPolicy Bypass -File scripts/resolve-profile-inheritance.ps1 -VendorLimit 5
```

## Strict Run

```powershell
powershell -ExecutionPolicy Bypass -File scripts/resolve-profile-inheritance.ps1 -StrictDiscovery -StrictInheritance
```

## Defaults

- Source path: `overhaul/eon_engine_mirror/resources/profiles`
- Report path: `docs/_profile_inheritance_report.json`
- Summary path: `docs/_profile_inheritance_summary.txt`
- Vendor limit: `0` (full set)
- Max chain depth: `64`

## Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-profile-inheritance-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-profile-inheritance-integration.ps1
```
