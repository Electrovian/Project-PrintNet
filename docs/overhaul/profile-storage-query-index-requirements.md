# Profile Storage and Query Index Requirements

Date: 2026-02-13  
Checklist ID: `T091`

## Objective

Persist mapped profile records into a deterministic local index and provide fast query paths for vendor/category/name/setting filters.

## Required Outcomes

- Deterministic profile record IDs and stable ordering.
- Local JSON index persistence and reload capability.
- Query API for vendor/category/name/mapped-key filters.
- Strict mode option for warning-gated workflows.
- Machine-readable report and summary outputs.

## Acceptance Criteria

- Invalid source/index paths fail fast with explicit errors.
- Stored index includes category and vendor aggregation counts.
- Unit/integration/performance checks pass.
- Index generated from same source is reproducible.
