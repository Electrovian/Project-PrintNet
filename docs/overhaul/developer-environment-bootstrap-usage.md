# Developer Environment Bootstrap Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T038`

## Bootstrap

```powershell
powershell -ExecutionPolicy Bypass -File scripts/bootstrap-dev-environment.ps1
```

## Offline Bootstrap

```powershell
powershell -ExecutionPolicy Bypass -File scripts/bootstrap-dev-environment.ps1 -Offline -WheelCacheDir App/wheels
```

## Dry Run

```powershell
powershell -ExecutionPolicy Bypass -File scripts/bootstrap-dev-environment.ps1 -DryRun
```

## Launch App (Venv)

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-app-dev.ps1
```

## Defaults

- Python: `python`
- App dir: `App`
- Venv: `App/.venv`
- Requirements: `App/requirements.txt`
- Report output: `docs/_dev_bootstrap_report.json`
