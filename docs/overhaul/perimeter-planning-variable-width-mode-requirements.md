# Perimeter Planning Variable-Width Mode Requirements

Date: 2026-02-13  
Checklist ID: `T181`

## Objective

Implement deterministic variable-width perimeter planning in `slicer_v2` that adapts line widths per shell while preserving wall sequencing and layer/island ordering contracts.

## Required Outcomes

- A dedicated variable-width perimeter planning module.
- Width-aware shell planning over island outer loops and hole loops.
- Configurable width bounds (`min`/`max`) with base line-width anchoring.
- Support for wall sequence ordering and first-layer single-wall override.
- Stage artifact reporting for width usage, path counts, and warnings.

## Acceptance Criteria

- Produced widths remain inside configured bounds.
- Variable-width mode executes through the perimeter stage with deterministic outputs.
- Unit/integration/performance checks pass within runtime budget.
- Usage/defaults, migration notes, and completion gate docs are published.

