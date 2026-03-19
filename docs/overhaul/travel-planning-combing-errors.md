# Travel Planning and Combing Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T224`

## Error Classes

- `TRAVEL_LAYER_GRAPH_INVALID`
  - Trigger: planner receives non-`LayerIslandGraph` input.
  - Behavior: raises `SlicerV2TravelPlanningError`.

- `TRAVEL_FEATURE_COUNT_NEGATIVE`
  - Trigger: perimeter/infill/support feature count is negative.
  - Behavior: raises `SlicerV2TravelPlanningError`.

- `TRAVEL_SPEED_INVALID`
  - Trigger: travel speed is outside `1..1000`.
  - Behavior: raises `SlicerV2TravelPlanningError`.

- `TRAVEL_COMBING_DETOUR_RATIO_INVALID`
  - Trigger: combing detour ratio is outside `1.0..5.0`.
  - Behavior: raises `SlicerV2TravelPlanningError`.

- `TRAVEL_RETRACT_MIN_INVALID`
  - Trigger: retract minimum travel distance is negative.
  - Behavior: raises `SlicerV2TravelPlanningError`.

- `TRAVEL_Z_HOP_HEIGHT_INVALID`
  - Trigger: Z-hop height is negative.
  - Behavior: raises `SlicerV2TravelPlanningError`.

- `SLICER_V2_TRAVEL_PLANNING_SMOKE_COMMAND_FAILED`
  - Trigger: smoke command exits non-zero.
  - Behavior: PowerShell wrapper failure with exit code.

## Warning Classes (report-level)

- `travel_planning:no_layer_graphs`
- `travel_planning:combing_requested_without_graphs`
- `travel_planning:z_hop_enabled_with_zero_height`
- `travel_planning:fallback_without_islands`
