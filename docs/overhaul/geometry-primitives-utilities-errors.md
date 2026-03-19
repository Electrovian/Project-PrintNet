# Geometry Primitives and Utilities Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T124`

## Error Classes

- `NON_FINITE_VALUE`
  - Trigger: NaN/inf coordinate values.
  - Behavior: raises `SlicerV2GeometryError`.

- `POINT2_TUPLE_SIZE_INVALID`
  - Trigger: tuple passed to `Point2.from_tuple` not length 2.
  - Behavior: raises `SlicerV2GeometryError`.

- `AABB_BOUNDS_INVALID`
  - Trigger: `max < min` on any axis.
  - Behavior: raises `SlicerV2GeometryError`.

- `AABB_POINTS_EMPTY`
  - Trigger: empty point set passed to `AABB.from_points`.
  - Behavior: raises `SlicerV2GeometryError`.

- `POLYGON_POINT_COUNT_INVALID`
  - Trigger: fewer than 3 points before/after normalization.
  - Behavior: raises `SlicerV2GeometryError`.

- `POLYGON_DEGENERATE`
  - Trigger: polygon collapses during duplicate-point cleanup.
  - Behavior: raises `SlicerV2GeometryError`.

- `POLYGON_AREA_ZERO`
  - Trigger: signed area effectively zero.
  - Behavior: raises `SlicerV2GeometryError`.

- `BOUNDS_POLYGONS_EMPTY`
  - Trigger: empty polygon list passed to `bounds_for_polygons`.
  - Behavior: raises `SlicerV2GeometryError`.

- `SLICER_V2_GEOMETRY_SMOKE_COMMAND_FAILED`
  - Trigger: geometry smoke wrapper returns non-zero.
  - Behavior: wrapper failure with exit code.
