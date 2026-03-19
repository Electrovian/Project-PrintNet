# Geometry Primitives and Utilities Requirements

Date: 2026-02-13  
Checklist ID: `T121`

## Objective

Introduce canonical geometry primitives for `slicer_v2` with deterministic utility behavior for bounds, area, containment, winding, and island semantics.

## Required Outcomes

- Typed geometry primitives: `Point2`, `AABB`, `Polygon`, `Island`.
- Robust validation for finite coordinates and non-degenerate polygons.
- Utility helpers for polygon/island construction and basic geometric metrics.
- Deterministic winding normalization for island outer/holes.
- Scriptable smoke output to verify behavior and numerical sanity.

## Acceptance Criteria

- Invalid geometry inputs fail with explicit geometry error codes.
- Unit and integration checks cover containment, bounds, area, and winding behavior.
- Performance checks complete under documented budget.
- Public exports in `slicer_v2` package include geometry primitives/utilities.
