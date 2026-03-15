# Repository Module Inventory Contract

Date: 2026-02-13
Checklist IDs: `T012`

## Script Interface

- Script path: `scripts/generate-module-inventory.ps1`
- Parameters:
  - `-AppRoot <string>` default `App`
  - `-OutputDir <string>` default `docs`

## Output Contract

Each output file starts with:
- `generated_at: <ISO 8601 UTC>`
- `app_root: <resolved path>`
- `generator: scripts/generate-module-inventory.ps1`

Then each file includes newline-delimited content:
- `docs/_app_file_inventory.txt`: relative file paths.
- `docs/_app_import_inventory.txt`: `path:line: import statement`.
- `docs/_app_slicer_connect_inventory.txt`: `path:line: matching line`.

## Failure Contract

- Missing `AppRoot` directory: hard failure.
- Missing `OutputDir` directory: auto-create.
- Missing `rg` binary: fallback to PowerShell native scan.
- Any unhandled exception: hard failure with error message and non-zero exit.
