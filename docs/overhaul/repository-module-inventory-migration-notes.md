# Repository Module Inventory Migration Notes

Date: 2026-02-13
Checklist ID: `T019`

## Legacy Baseline

- Module and import discovery was previously ad-hoc and manually maintained.
- Inventory artifacts were not guaranteed to be regenerated with deterministic ordering.

## Current Baseline

- `scripts/generate-module-inventory.ps1` is the single command for inventory generation.
- Output is deterministic and includes timestamp/source metadata headers.
- Generated inventory artifacts are:
  - `docs/_app_file_inventory.txt`
  - `docs/_app_import_inventory.txt`
  - `docs/_app_slicer_connect_inventory.txt`

## Migration Impact

- Future migration tasks should reference generated artifacts instead of manually curated lists.
- Any new top-level modules under `App/` must be captured by rerunning the generator.
