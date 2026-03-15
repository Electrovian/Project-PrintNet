# Desktop Test Automation and Regression Usage and Defaults

Date: 2026-02-13  
Checklist ID: `T338`

## Run Smoke

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run-desktop-test-automation-smoke.ps1
```

## Run Unit and Integration Tests

```powershell
powershell -ExecutionPolicy Bypass -File scripts/test-desktop-test-automation-unit.ps1
powershell -ExecutionPolicy Bypass -File scripts/test-desktop-test-automation-integration.ps1
```

## Defaults

- Runner command: `python -m unittest`
- Default case timeout: `20s`
- Unit budget (`MaxSeconds`): `20s`
- Integration budget (`MaxSeconds`): `60s`
- Stop-on-failure default: `false`
- Default report path:
  - `docs/_desktop_test_automation_report.json`
- Default summary path:
  - `docs/_desktop_test_automation_summary.txt`
