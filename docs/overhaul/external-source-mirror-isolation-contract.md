# External Source Mirror Isolation Contract

Date: 2026-02-13  
Checklist ID: `T042`

## Core Scripts

- `scripts/sync-overhaul-source.ps1`
- `scripts/verify-source-mirror-isolation.ps1`

## Sync Contract

`sync-overhaul-source.ps1` parameters:

- `-SourcePath`
- `-TargetPath` (must be under `overhaul/`)
- `-ProfilesOnly`
- `-DryRun`
- `-ManifestPath`

Manifest payload:

- `timestamp_utc`
- `source_path`
- `target_path`
- `profiles_only`
- `dry_run`
- `robocopy_exit_code`
- `file_count`

## Verification Contract

`verify-source-mirror-isolation.ps1` parameters:

- `-RepoRoot`
- `-MirrorRootRelative`
- `-GitIgnoreRelativePath`
- `-RequiredIgnoreRule`
- `-ReportPath`
- `-RequireMirrorDirectory`

Verification report payload:

- `timestamp_utc`
- `success`
- `repo_root`
- `mirror_root_relative`
- `checks[]` with `name`, `status`, `message`

## Failure Contract

- Any failing check writes report then exits non-zero.
- `TARGET_POLICY_VIOLATION` if sync target is outside `overhaul/`.
