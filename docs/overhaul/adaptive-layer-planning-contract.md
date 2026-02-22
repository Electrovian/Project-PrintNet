# Adaptive Layer Planning Contract

Date: 2026-02-13  
Checklist ID: `T152`

## Core Module

- `App/slicer_v2/adaptive_layers.py`

Primary types:

- `AdaptiveLayerRange`
- `AdaptiveLayerPlanReport`
- `AdaptiveLayerPlan`

Primary API:

- `build_layer_plan(resolved_settings, z_min_mm, z_max_mm, model_height_mm, max_layer_count=2000) -> AdaptiveLayerPlan`

## Stage Integration Contract

- `App/slicer_v2/slice_grid.py`
  - delegates layer scheduling to `build_layer_plan`.
  - emits `adaptive_layering_enabled`, `adaptive_layering_strategy`, and `adaptive_layer_report`.

- `App/slicer_v2/settings.py`
  - normalizes adaptive keys:
    - `adaptive_layering_enabled`
    - `adaptive_layer_min`
    - `adaptive_layer_max`
    - `adaptive_top_bottom_refine_mm`
    - `adaptive_layer_ranges`

## Script Contract

- `scripts/run-slicer-v2-adaptive-layer-smoke.ps1`
- `scripts/test-slicer-v2-adaptive-layer-unit.ps1`
- `scripts/test-slicer-v2-adaptive-layer-integration.ps1`

Outputs:

- `docs/_slicer_v2_adaptive_layer_report*.json`
- `docs/_slicer_v2_adaptive_layer_summary*.txt`

