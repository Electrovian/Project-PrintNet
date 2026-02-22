# Mesh Slicing and Contour Assembly Requirements

Date: 2026-02-13  
Checklist ID: `T141`

## Objective

Implement mesh slicing and contour assembly in `slicer_v2` to generate deterministic per-layer 2D contours from STL mesh input.

## Required Outcomes

- STL mesh loading (ASCII + binary) into canonical mesh data.
- Triangle-plane slicing at specified Z heights.
- Segment deduplication and contour loop assembly.
- Per-layer contour output with warning/report metadata.
- Stage integration so `mesh` and `regions` reflect real slicing signals.

## Acceptance Criteria

- Missing/invalid mesh files fail with explicit mesh slicing errors.
- Slicing synthetic box mesh yields non-empty contours at mid-layers.
- Unit/integration/performance checks pass within budget.
- Reports are reproducible for identical input and layer schedule.
