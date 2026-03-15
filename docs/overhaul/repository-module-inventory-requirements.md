# Repository Module Inventory Requirements

Date: 2026-02-13
Checklist IDs: `T011`

## Objective

Create a deterministic baseline inventory of the Python desktop codebase so migration tasks can be scoped and sequenced without relying on ad-hoc file discovery.

## Required Outputs

- `docs/_app_file_inventory.txt`: sorted list of files under `App/`.
- `docs/_app_import_inventory.txt`: Python import statements with file/line references.
- `docs/_app_slicer_connect_inventory.txt`: targeted references to slicer and printer-connect execution paths.

## Acceptance Criteria

- Running the inventory generator twice on an unchanged tree produces the same output ordering.
- Generated files include an ISO timestamp and source root header.
- The command exits non-zero when required paths are missing.
- The command can run from repository root without manual path edits.
