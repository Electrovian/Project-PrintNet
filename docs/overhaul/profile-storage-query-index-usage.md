# Profile Storage and Query Index Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T098`

## Build and Persist Index

```powershell
powershell -ExecutionPolicy Bypass -File scripts/store-profile-index.ps1
```

## Bounded Integration Run

```powershell
powershell -ExecutionPolicy Bypass -File scripts/store-profile-index.ps1 -VendorLimit 5
```

## Strict Run

```powershell
powershell -ExecutionPolicy Bypass -File scripts/store-profile-index.ps1 -StrictDiscovery -StrictInheritance -StrictMapping -StrictStorage
```

## Defaults

- Source path: `overhaul/eon_engine_mirror/resources/profiles`
- Index path: `docs/_profile_storage_index.json`
- Report path: `docs/_profile_storage_index_report.json`
- Summary path: `docs/_profile_storage_index_summary.txt`
- Vendor limit: `0` (full set)
- Max chain depth: `64`

## Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-profile-storage-index-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-profile-storage-index-integration.ps1
```
