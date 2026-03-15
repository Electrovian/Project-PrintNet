# Polygon Offset and Cleanup Pipeline Requirements

Date: 2026-02-13  
Checklist ID: `T131`

## Objective

Provide deterministic polygon cleanup and signed offset capability for `slicer_v2` so later mesh/perimeter/infill stages can rely on stable 2D geometry preprocessing.

## Required Outcomes

- Polygon cleanup with collinear-point removal and minimum-area filtering.
- Signed polygon offset (positive = outward, negative = inward).
- Batch cleanup/offset orchestration with report metadata.
- Strict mode to fail on warning conditions.
- Scriptable smoke output for CI/debug visibility.

## Acceptance Criteria

- Tiny/degenerate polygons are dropped deterministically.
- Outward offset increases area for standard convex shapes.
- Inward offset reduces area and can drop invalid results safely.
- Unit/integration/performance checks pass within documented budgets.
