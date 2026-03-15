# Infill Planning Patterns Requirements

Date: 2026-02-13  
Checklist ID: `T191`

## Objective

Implement deterministic infill pattern planning in `slicer_v2` for sparse interior fill generation using island graph inputs.

## Required Outcomes

- Dedicated infill pattern planner module with typed outputs.
- Support for core sparse patterns:
  - `rectilinear`
  - `grid`
  - `gyroid`
  - `triangle` (mapped fallback behavior for MVP)
- Layer angle alternation controls (`start`, `step`).
- Stable path-count and path-length metadata for downstream travel/G-code stages.
- Backward-compatible stage artifact fields with additive infill metadata.

## Acceptance Criteria

- Infill planning is deterministic for identical inputs.
- Pattern mode and angle controls are reflected in stage artifacts.
- Unit/integration/performance checks pass within the runtime budget.
- Usage/defaults, migration notes, and completion gate docs are published.

