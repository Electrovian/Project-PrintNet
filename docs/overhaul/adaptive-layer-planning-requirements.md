# Adaptive Layer Planning Requirements

Date: 2026-02-13  
Checklist ID: `T151`

## Objective

Implement deterministic adaptive layer planning in `slicer_v2` with fixed-height fallback, manual refinement ranges, top/bottom refinement controls, and exact Z-closure behavior.

## Required Outcomes

- A dedicated adaptive planning module decoupled from stage orchestration.
- Safe fallback to fixed scheduling when adaptive controls are disabled.
- Manual range-based layer refinement support.
- Exact closure to `z_max_mm` without trailing invalid micro-layers.
- Stage artifact output that downstream `regions/perimeters/infill` stages can consume without schema changes.

## Acceptance Criteria

- Fixed schedule and adaptive schedule produce deterministic layer heights and Z centers.
- Invalid adaptive settings fail with explicit adaptive-layer errors.
- Unit/integration/performance checks pass within budget.
- Usage/defaults, migration notes, and completion gate documents exist.

