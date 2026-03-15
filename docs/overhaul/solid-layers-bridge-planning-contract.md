# Solid Layers and Bridge Planning Contract

Date: 2026-02-13  
Checklist ID: `T202`

## Core Module

- `App/slicer_v2/solid_bridges.py`

Primary types:

- `BridgeRegionPlan`
- `SolidLayerPlan`
- `SolidBridgeReport`

Primary API:

- `build_solid_layers_and_bridges(layer_graphs, vertical_edges=(), top_layers, bottom_layers, extrusion_width_mm, bridge_enabled, bridge_flow_ratio=1.0, bridge_speed_ratio=0.8) -> (list[SolidLayerPlan], SolidBridgeReport)`

## Stage Integration Contract

- `App/slicer_v2/bridges.py`
  - consumes:
    - `islands.layer_graphs`
    - `islands.vertical_edges`
  - emits:
    - `solid_layer_count`
    - `top_solid_layer_count`
    - `bottom_solid_layer_count`
    - `solid_path_count_total`
    - `solid_path_length_mm_total`
    - `bridge_region_count`
    - `bridge_path_count`
    - `bridge_path_length_mm_total`
    - `layer_classifications`
    - `report`
  - retains fallback behavior when island graph data is unavailable.

## Settings Contract

- `App/slicer_v2/settings.py` normalizes:
  - `top_layers`
  - `bottom_layers`
  - `bridge_enabled`
  - `bridge_flow_ratio`
  - `bridge_speed_ratio`
  - common aliases (`bridge_flow_multiplier`, `bridge_speed_multiplier`).

## Script Contract

- `scripts/run-slicer-v2-solid-bridges-smoke.ps1`
- `scripts/test-slicer-v2-solid-bridges-unit.ps1`
- `scripts/test-slicer-v2-solid-bridges-integration.ps1`

Outputs:

- `docs/_slicer_v2_solid_bridges_report*.json`
- `docs/_slicer_v2_solid_bridges_summary*.txt`
