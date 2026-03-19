# Printer Profile File Discovery Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T058`

## Run Discovery

```powershell
powershell -ExecutionPolicy Bypass -File scripts/discover-printer-profiles.ps1
```

## Run Discovery (Custom Source)

```powershell
powershell -ExecutionPolicy Bypass -File scripts/discover-printer-profiles.ps1 -SourcePath "C:\path\to\profiles"
```

## Run in Strict Mode

```powershell
powershell -ExecutionPolicy Bypass -File scripts/discover-printer-profiles.ps1 -Strict
```

## Defaults

- Source path: `overhaul/eon_engine_mirror/resources/profiles`
- Report path: `docs/_printer_profile_file_discovery_report.json`
- Summary path: `docs/_printer_profile_file_discovery_summary.txt`

## Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-printer-profile-discovery-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-printer-profile-discovery-integration.ps1
```
