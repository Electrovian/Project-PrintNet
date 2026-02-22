# Adaptive Layer Planning Migration Notes

Date: 2026-02-13  
Checklist ID: `T159`

## Legacy Baseline

- `slicer_v2` `slice_grid` stage previously produced only fixed-height schedules.
- Adaptive-layer controls were not represented in `slicer_v2` settings normalization.

## Current Baseline

- `App/slicer_v2/adaptive_layers.py` now owns deterministic layer schedule planning.
- `slice_grid` now delegates planning and emits adaptive strategy/report metadata.
- `settings.py` now normalizes adaptive scheduling keys and manual range payloads.

## Migration Impact

- Existing fixed-height behavior is preserved when adaptive settings remain disabled.
- Downstream stages continue consuming `layer_count`, `layer_heights_mm`, and `layer_z_values_mm` without schema break.
- Future overhang/island-driven adaptive logic can extend planner input without replacing the stage contract.

