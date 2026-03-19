# Dependency/Import Graph Migration Notes

Date: 2026-02-13
Checklist ID: `T029`

## Legacy Baseline

- Import dependency understanding was implicit and spread across ad-hoc inspections.

## Current Baseline

- `scripts/generate-dependency-graph.ps1` creates deterministic module and edge outputs.
- `scripts/test-dependency-graph.ps1` validates graph completeness and runtime budget.

## Migration Impact

- Refactor sequencing must use `_app_dependency_graph.txt` as coupling evidence.
- High-fan-in modules should be stabilized before deep slicer/connector rewrites.
