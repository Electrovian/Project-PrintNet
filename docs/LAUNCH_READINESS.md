# Launch Readiness

This is the authoritative repo-wide launch and smoke runbook for the April 7, 2026 demo window.

## One Command

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\launch_readiness.ps1
```

Optional compose smoke:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\launch_readiness.ps1 -WithComposeSmoke
```

## What It Runs

- Desktop startup smoke: `python -m App.testing.desktop_startup_smoke`
- Desktop demo smoke suite: `python App\Tests\run_tests.py --scope smoke`
- Desktop visual audit pack to a temp folder: `python -m App.testing.visual_audit --scenario demo --output-dir <temp>`
- Backend unit/smoke coverage:
  - `python -m pytest tests -q`
  - live backend health probe
  - `python scripts/worker_smoke.py`
- Frontend checks:
  - `node --test tests/*.mjs`
  - `npm run build`
  - `npm run test:browser`
- Mobile checks:
  - `python -m unittest discover -s Mobile/tests -q`
  - `python -m Mobile.preflight`
- Deploy preflight:
  - `docker compose config -q`

The launch runner snapshots `git status --porcelain` before it starts and fails if any command introduces new tracked-file drift beyond the baseline dirty state already present in the worktree.

## Product Defaults

- Desktop `App/` is the primary demo surface.
- Mobile uses the Toga/Briefcase app in `Mobile/app_mobile.py`.
- `Mobile/flutter_runner/` is experimental and not the launch target for this demo.
- Backend runtime uploads belong under `Website/backend/runtime/uploads`.
- Frontend build output and browser smoke artifacts are runtime output, not source.

## Manual Final Gate

Run this after the scripted checks pass:

1. Launch the desktop app on the real demo machine.
2. Walk `Files`, `Activity`, `Prepare`, `Preview`, `Device`, and `Calibration/Control`.
3. Slice one tree-support model and one organic-support model.
4. Export G-code and run send/start against every live printer connector available that day.
5. Repeat at the actual display scaling, then verify 125% scaling if available.

## Known Failure Modes

- `python -m Mobile.preflight` fails when `toga` is not installed. That is expected until mobile dependencies are installed with `python -m pip install -r Mobile/requirements-mobile.txt`.
- `python -m App.testing.fff_parity` fails if the configured corpus manifest points at missing meshes. That is intentional false-green protection.
