# G-code Emission Semantics Requirements

Date: 2026-02-13  
Checklist ID: `T241`

## Objective

Implement deterministic G-code semantic emission in `slicer_v2` using flow/travel planning artifacts and normalized firmware/macro settings.

## Required Outcomes

- Dedicated semantic emitter module with typed per-layer command metadata.
- Deterministic setup, layer, and teardown command generation.
- Support for absolute and relative extrusion modes.
- Startup and end macro injection with safe normalization.
- Firmware flavor validation for MVP flavors (`marlin`, `klipper`, `prusalink`, `generic`).
- Backward-compatible `gcode` stage artifact with additive semantic metadata.

## Acceptance Criteria

- Identical inputs produce deterministic command order and counts.
- Emission reflects configured extrusion mode and firmware flavor.
- Startup/end macros are injected when configured.
- Unit/integration/performance checks pass within runtime budget.
- Usage/defaults, migration notes, and completion gate docs are published.
