# Perimeter Planning Classic Mode Requirements

Date: 2026-02-13  
Checklist ID: `T171`

## Objective

Implement deterministic classic perimeter planning in `slicer_v2` using island graphs as input and producing ordered shell loops for each printable layer.

## Required Outcomes

- A dedicated classic perimeter planner module decoupled from stage orchestration.
- Per-layer loop planning across island outer boundaries and hole boundaries.
- Wall-order sequencing support (`outer_to_inner`, `inner_to_outer`).
- First-layer single-wall override support.
- Stable summary/report metadata for downstream travel/G-code stages.

## Acceptance Criteria

- Layer/island shell planning is deterministic for identical input.
- Perimeter stage switches to classic planner whenever island graph data is present.
- Unit/integration/performance checks pass inside the runtime budget.
- Usage/defaults, migration notes, and completion gate docs are published.

