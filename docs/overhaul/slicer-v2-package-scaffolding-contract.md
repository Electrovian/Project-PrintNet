# slicer_v2 Package Scaffolding Contract

Date: 2026-02-13  
Checklist ID: `T102`

## Core Modules

- `App/slicer_v2/types.py`
- `App/slicer_v2/errors.py`
- `App/slicer_v2/settings.py`
- `App/slicer_v2/context.py`
- `App/slicer_v2/pipeline.py`
- Stage modules:
  - `mesh.py`
  - `slice_grid.py`
  - `regions.py`
  - `perimeters.py`
  - `infill.py`
  - `supports.py`
  - `bridges.py`
  - `travel.py`
  - `gcode.py`
  - `validators.py`

Primary APIs:

- `create_context(...) -> SlicerContext`
- `normalize_settings(...) -> dict`
- `run_pipeline(context) -> PipelineResult`
- `STAGE_SEQUENCE` (ordered stage contract)

## Data Contract

- `SlicerContext` carries mesh path, resolved settings, runtime settings, stage artifacts, and execution order.
- `PipelineResult` returns context, validation report, and per-stage timing traces.
- Stage modules implement `run(context) -> dict` and register artifact by `STAGE_NAME`.

## Script Contract

- `scripts/run-slicer-v2-scaffold-smoke.ps1`
- `scripts/test-slicer-v2-scaffolding-unit.ps1`
- `scripts/test-slicer-v2-scaffolding-integration.ps1`

Outputs:

- `docs/_slicer_v2_scaffolding_report*.json`
- `docs/_slicer_v2_scaffolding_summary*.txt`
