# Developer Environment Bootstrap Contract

Date: 2026-02-13  
Checklist ID: `T032`

## Core Scripts

- `scripts/bootstrap-dev-environment.ps1`
- `scripts/run-app-dev.ps1`

## Bootstrap Parameters

- `-PythonExe` default `python`
- `-AppDir` default `App`
- `-VenvDir` default `App/.venv`
- `-RequirementsPath` default `App/requirements.txt`
- `-WheelCacheDir` default `App/wheels`
- `-InstallDependencies` default `$true`
- `-Offline` switch
- `-DryRun` switch
- `-VerifyImports` switch
- `-ForceRecreate` switch
- `-ReportPath` default `docs/_dev_bootstrap_report.json`

## Report Contract

Report is JSON with:

- `timestamp_utc` (ISO 8601)
- `success` (bool)
- `dry_run` (bool)
- `offline` (bool)
- `fatal_error` (string or null)
- `config` (object)
- `steps` (array)

Step object fields:

- `name`
- `status` (`ok`, `simulated`, `failed`)
- `command`
- `duration_ms`
- `message`

## Failure Contract

- Missing app dir / requirements / python: hard failure.
- Offline mode without wheel cache: hard failure.
- Any command step failure: marks step `failed`, writes report, exits non-zero.
