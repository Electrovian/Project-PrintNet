# Travel Planning and Combing Contract

Date: 2026-02-13  
Checklist ID: `T222`

## Core Module

- `App/slicer_v2/travel_planning.py`

Primary types:

- `TravelMovePlan`
- `LayerTravelPlan`
- `TravelPlanningReport`

Primary API:

- `build_travel_plan(layer_graphs, layer_perimeter_counts, layer_infill_counts, layer_support_counts, travel_speed_mm_s, combing_enabled, combing_max_detour_ratio, retract_enabled, retract_min_travel_mm, z_hop_enabled, z_hop_mm) -> (list[LayerTravelPlan], TravelPlanningReport)`

## Stage Integration Contract

- `App/slicer_v2/travel.py`
  - consumes:
    - `islands.layer_graphs`
    - `perimeters.layer_perimeter_counts`
    - `infill.layer_infill_counts`
    - `supports.layer_support_path_counts`
  - emits:
    - `travel_move_count`
    - `travel_length_mm_total`
    - `travel_combed_move_count`
    - `travel_fallback_move_count`
    - `travel_retract_count`
    - `travel_z_hop_count`
    - `layer_travel_move_counts`
    - `layer_travel_lengths_mm`
    - `layer_travel_combed_counts`
    - `layer_travel_fallback_counts`
    - `report`
  - retains fallback behavior when island graph data is unavailable.

## Settings Contract

- `App/slicer_v2/settings.py` normalizes:
  - `travel_speed`
  - `travel_combing_enabled`
  - `travel_combing_max_detour_ratio`
  - `travel_retract_enabled`
  - `travel_retract_min_travel_mm`
  - `travel_z_hop_enabled`
  - `travel_z_hop_mm`
  - common aliases (`avoid_crossing_walls`, `combing_max_detour_ratio`, `retraction_enable`, `retract_min_travel`, `z_hop_enable`, `z_hop_height`).

## Script Contract

- `scripts/run-slicer-v2-travel-planning-smoke.ps1`
- `scripts/test-slicer-v2-travel-planning-unit.ps1`
- `scripts/test-slicer-v2-travel-planning-integration.ps1`

Outputs:

- `docs/_slicer_v2_travel_planning_report*.json`
- `docs/_slicer_v2_travel_planning_summary*.txt`
