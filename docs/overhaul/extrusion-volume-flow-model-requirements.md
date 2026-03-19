# Extrusion Volume and Flow Model Requirements

Date: 2026-02-13  
Checklist ID: `T231`

## Objective

Implement deterministic extrusion volume and flow modeling in `slicer_v2` to estimate filament length, material mass, and material cost from planned path lengths.

## Required Outcomes

- Dedicated extrusion-flow model module with typed outputs.
- Per-layer feature accounting for:
  - perimeter
  - infill
  - support
  - solid
  - bridge
- Global and feature-specific flow ratios.
- Filament conversion from volume (`mm3`) to filament length (`mm`), mass (`g`), and cost (`USD`).
- Backward-compatible G-code stage fields with additive extrusion-flow metadata.

## Acceptance Criteria

- Identical inputs produce deterministic extrusion-flow totals.
- Flow ratios and filament metadata affect output estimates as expected.
- Unit/integration/performance checks pass within runtime budget.
- Usage/defaults, migration notes, and completion gate docs are published.
