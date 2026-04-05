# Project-PrintNet

Project-PrintNet is a slicer and print workflow codebase with the active application in `App/`.

## Start Here

- `docs/LAUNCH_READINESS.md` for the authoritative repo-wide launch and smoke runbook.
- `App/README.md` for the current app entrypoint, smoke suite, and parity runner.
- `docs/TASKS.md` for the live task tracker.
- `App/Tests/run_tests.py` for the curated smoke and full test entrypoints.

## Common Commands

```powershell
cd App
python main.py
python .\Tests\run_tests.py --scope smoke
python -m App.testing.fff_parity --manifest <manifest.json> --profile <profile.json> --output <report.json>
```

Repo-wide launch readiness:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\launch_readiness.ps1
```

The parity command now fails loudly when its corpus meshes are missing and does not return a false-green result when nothing can be compared.
