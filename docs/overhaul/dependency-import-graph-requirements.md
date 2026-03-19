# Dependency and Import Graph Requirements

Date: 2026-02-13
Checklist ID: `T021`

## Objective

Produce a deterministic dependency graph for `App/` Python modules so coupling, layering, and migration order are explicit.

## Required Outputs

- `docs/_app_dependency_graph.txt`: module-to-module dependency edges.
- `docs/_app_dependency_modules.txt`: normalized module index.

## Acceptance Criteria

- Graph generation is deterministic on unchanged source trees.
- Output includes generator metadata header.
- Output includes at least one module and one edge for non-empty repos.
- Missing `AppRoot` fails with non-zero status.
