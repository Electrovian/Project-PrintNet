# External Source Mirror Isolation Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T048`

## Sync Mirror (Profiles Only)

```powershell
powershell -ExecutionPolicy Bypass -File scripts/sync-overhaul-source.ps1 -SourcePath "C:\path\to\upstream\slicer" -ProfilesOnly
```

## Sync Mirror (Full)

```powershell
powershell -ExecutionPolicy Bypass -File scripts/sync-overhaul-source.ps1 -SourcePath "C:\path\to\upstream\slicer"
```

## Verify Isolation

```powershell
powershell -ExecutionPolicy Bypass -File scripts/verify-source-mirror-isolation.ps1
```

## Defaults

- Mirror root: `overhaul/`
- Verify report: `docs/_external_source_isolation_report.json`
- Required ignore rule: `/overhaul/`
