# Dependency and Import Graph Contract

Date: 2026-02-13
Checklist ID: `T022`

## Script Interface

- Script path: `scripts/generate-dependency-graph.ps1`
- Parameters:
  - `-AppRoot <string>` default `App`
  - `-OutputDir <string>` default `docs`

## Graph Format

- Module list file (`_app_dependency_modules.txt`) uses one module per line.
- Edge file (`_app_dependency_graph.txt`) uses one edge per line:
  - `<source_module> -> <imported_module>`

## Header Contract

Each output starts with:
- `generated_at: <ISO 8601 UTC>`
- `app_root: <resolved path>`
- `generator: scripts/generate-dependency-graph.ps1`

## Failure Contract

- Missing app root: hard failure.
- Empty parse result on non-empty module set: warning plus non-zero failure.
- Runtime exceptions: hard failure with actionable message.
