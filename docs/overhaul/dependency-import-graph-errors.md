# Dependency/Import Graph Error Taxonomy

Date: 2026-02-13
Checklist ID: `T024`

## Error Classes

- `APP_ROOT_MISSING`
  - Trigger: `AppRoot` path does not exist.
  - Action: Fail fast with non-zero exit.

- `NO_PYTHON_FILES`
  - Trigger: `AppRoot` contains no `*.py` files.
  - Action: Fail fast with non-zero exit.

- `EMPTY_EDGE_SET`
  - Trigger: module set exists but zero dependency edges parsed.
  - Action: emit warning and fail with non-zero exit.

- `OUTPUT_WRITE_FAILURE`
  - Trigger: output files cannot be written.
  - Action: fail with non-zero exit and path details.
