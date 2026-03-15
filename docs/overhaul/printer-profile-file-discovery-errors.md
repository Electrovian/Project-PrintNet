# Printer Profile File Discovery Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T054`

## Error Classes

- `SOURCE_PATH_EMPTY`
  - Trigger: source path input is empty.
  - Behavior: immediate failure.

- `SOURCE_PATH_MISSING`
  - Trigger: source path does not exist.
  - Behavior: immediate failure.

- `SOURCE_PATH_NOT_DIRECTORY`
  - Trigger: source path exists but is not a directory.
  - Behavior: immediate failure.

- `STRICT_DISCOVERY_WARNING_FAILURE`
  - Trigger: strict mode is enabled and warnings are produced.
  - Behavior: fail with warning count.

- `DISCOVERY_COMMAND_FAILED`
  - Trigger: discovery script process returns non-zero.
  - Behavior: script throws with exit code.
