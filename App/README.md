# App

This directory contains the current desktop slicer and print workflow used by the demo build.

## Quick Start

Run the app from this folder with:

```powershell
python main.py
```

Run the demo smoke suite with:

```powershell
python .\Tests\run_tests.py --scope smoke
```

Run the headless desktop startup smoke with:

```powershell
python -m App.testing.desktop_startup_smoke
```

Run the FFF parity corpus with a manifest that points at real mesh files:

```powershell
python -m App.testing.fff_parity --manifest <manifest.json> --profile <profile.json> --output <report.json>
```

The parity runner now fails fast if the manifest references missing meshes or if no comparable models are available.

## Notes

- `App/Tests/run_tests.py` is the entrypoint for the curated smoke suite.
- `App/testing/desktop_startup_smoke.py` verifies real offscreen startup without hanging in the full event loop.
- `App/testing/fff_parity.py` works both as a module and as a direct script.
- The desktop app now defaults to `desktop` OpenGL on interactive Windows sessions and `software` OpenGL for headless/offscreen test runs.
- You can still force a specific renderer with `EON_OPENGL_MODE=desktop` or `EON_OPENGL_MODE=software` before launching `python main.py`.
- `docs/LAUNCH_READINESS.md` is the authoritative repo-wide launch runbook.
- If you are looking for repo-wide task tracking, start with `docs/TASKS.md`.
