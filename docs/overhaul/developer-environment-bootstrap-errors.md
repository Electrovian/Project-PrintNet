# Developer Environment Bootstrap Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T034`

## Error Classes

- `APP_DIR_MISSING`
  - Trigger: `AppDir` path does not exist.
  - Behavior: hard fail before executing steps.

- `REQUIREMENTS_MISSING`
  - Trigger: install requested and requirements file missing.
  - Behavior: hard fail before executing steps.

- `PYTHON_NOT_FOUND`
  - Trigger: configured python executable not found in PATH.
  - Behavior: hard fail before executing steps.

- `OFFLINE_CACHE_MISSING`
  - Trigger: `-Offline` with dependency install enabled and missing wheel cache dir.
  - Behavior: hard fail before executing steps.

- `STEP_FAILURE`
  - Trigger: any command step exits non-zero.
  - Behavior: step marked `failed`, report written, non-zero exit.
