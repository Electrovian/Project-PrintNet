# Extrusion Volume and Flow Model Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T234`

## Error Classes

- `EXTRUSION_FLOW_LENGTH_NEGATIVE`
  - Trigger: any per-layer feature path length is negative.
  - Behavior: raises `SlicerV2ExtrusionFlowError`.

- `EXTRUSION_FLOW_LINE_WIDTH_INVALID`
  - Trigger: extrusion line width is non-positive.
  - Behavior: raises `SlicerV2ExtrusionFlowError`.

- `EXTRUSION_FLOW_NOZZLE_DIAMETER_INVALID`
  - Trigger: nozzle diameter is non-positive.
  - Behavior: raises `SlicerV2ExtrusionFlowError`.

- `EXTRUSION_FLOW_FILAMENT_DIAMETER_INVALID`
  - Trigger: filament diameter is non-positive.
  - Behavior: raises `SlicerV2ExtrusionFlowError`.

- `EXTRUSION_FLOW_MULTIPLIER_INVALID`
  - Trigger: global flow multiplier is outside `0.1..3.0`.
  - Behavior: raises `SlicerV2ExtrusionFlowError`.

- `EXTRUSION_FLOW_PERIMETER_RATIO_INVALID`
- `EXTRUSION_FLOW_INFILL_RATIO_INVALID`
- `EXTRUSION_FLOW_SUPPORT_RATIO_INVALID`
- `EXTRUSION_FLOW_SOLID_RATIO_INVALID`
- `EXTRUSION_FLOW_BRIDGE_RATIO_INVALID`
  - Trigger: feature flow ratio is outside `0.1..3.0`.
  - Behavior: raises `SlicerV2ExtrusionFlowError`.

- `EXTRUSION_FLOW_FILAMENT_DENSITY_INVALID`
  - Trigger: filament density is negative.
  - Behavior: raises `SlicerV2ExtrusionFlowError`.

- `EXTRUSION_FLOW_FILAMENT_COST_INVALID`
  - Trigger: filament cost is negative.
  - Behavior: raises `SlicerV2ExtrusionFlowError`.

- `EXTRUSION_FLOW_SMALL_FEATURE_THRESHOLD_INVALID`
  - Trigger: small-feature threshold is negative.
  - Behavior: raises `SlicerV2ExtrusionFlowError`.

- `EXTRUSION_FLOW_SMALL_FEATURE_BOOST_INVALID`
  - Trigger: small-feature flow boost ratio is outside `1.0..2.0`.
  - Behavior: raises `SlicerV2ExtrusionFlowError`.

- `SLICER_V2_EXTRUSION_FLOW_SMOKE_COMMAND_FAILED`
  - Trigger: smoke command exits non-zero.
  - Behavior: PowerShell wrapper failure with exit code.

## Warning Classes (report-level)

- `extrusion_flow:line_width_narrow_vs_nozzle`
- `extrusion_flow:line_width_wide_vs_nozzle`
- `extrusion_flow:no_layers`
- `extrusion_flow:default_layer_heights_applied`
- `extrusion_flow:no_path_length`
