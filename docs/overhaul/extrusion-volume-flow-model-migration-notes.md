# Extrusion Volume and Flow Model Migration Notes

Date: 2026-02-13  
Checklist ID: `T239`

## Legacy Baseline

- `slicer_v2` G-code stage previously did not model extrusion volume/filament flow.
- Filament length, mass, and cost were not computed from layer feature paths.

## Current Baseline

- `App/slicer_v2/extrusion_flow.py` introduces deterministic per-layer extrusion-flow modeling.
- `App/slicer_v2/gcode.py` now aggregates planned feature lengths and emits extrusion volume, filament, mass, and cost estimates.
- `App/slicer_v2/settings.py` now normalizes global/feature flow controls and filament material metadata.

## Migration Impact

- Existing G-code artifact fields remain available for compatibility.
- New fields are additive (`extrusion_path_length_mm_total`, `extrusion_volume_mm3_total`, `estimated_filament_mm`, `estimated_mass_g`, `estimated_cost_usd`, `extrusion_flow` payload).
