# Island Graph and Adjacency Modeling Requirements

Date: 2026-02-13  
Checklist ID: `T161`

## Objective

Implement deterministic per-layer island graph generation from region contours, including hole association and adjacency metadata for same-layer and vertical neighbor layers.

## Required Outcomes

- Convert contour sets into normalized islands (`outer + holes`).
- Compute per-layer adjacency edges for islands with intersecting spatial bounds.
- Compute vertical adjacency edges across neighboring layers.
- Expose stable island graph artifacts for downstream perimeter/travel workstreams.
- Keep failure behavior explicit with a dedicated island-graph error class.

## Acceptance Criteria

- A single contour produces one island with zero holes.
- Nested contour cases produce expected outer/hole/island relationships.
- Unit/integration/performance checks pass within the defined budget.
- Usage/defaults, migration notes, and completion gate docs are published.

