# G-code Emission Semantics Migration Notes

Date: 2026-02-13  
Checklist ID: `T249`

## Legacy Baseline

- `slicer_v2` G-code output previously emitted a minimal scaffold header/body only.
- No semantic command modeling existed for per-layer travel/extrusion command intent.

## Current Baseline

- `App/slicer_v2/gcode_emission.py` introduces deterministic semantic command emission with typed layer/command metadata.
- `App/slicer_v2/gcode.py` now composes extrusion flow + travel planning outputs into semantic G-code lines.
- Startup/end macros, firmware flavor, and extrusion mode are now first-class normalized settings.

## Migration Impact

- Existing stage fields (`line_count`, `lines`, `estimated_time_seconds`) remain available.
- New fields are additive (`gcode_emission`, `layer_gcode_plans`, semantic command count metrics).
