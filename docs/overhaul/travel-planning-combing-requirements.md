# Travel Planning and Combing Requirements

Date: 2026-02-13  
Checklist ID: `T221`

## Objective

Implement deterministic travel planning in `slicer_v2`, including combing behavior, retract decisions, and Z-hop handling across layer feature transitions.

## Required Outcomes

- Dedicated travel planner module with typed outputs.
- Feature-transition based travel move planning per layer.
- Combing-aware move routing with deterministic detour behavior.
- Retract and Z-hop decision flags per move.
- Aggregate travel metrics (move counts, lengths, combed/fallback splits, retract/z-hop totals).
- Backward-compatible travel-stage outputs with additive fields.

## Acceptance Criteria

- Identical inputs produce deterministic travel planning outputs.
- Combing-enabled runs produce combed moves when feasible.
- Unit/integration/performance checks pass within runtime budget.
- Usage/defaults, migration notes, and completion gate docs are published.
