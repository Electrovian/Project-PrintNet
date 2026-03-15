# Profile Storage and Query Index Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T094`

## Error Classes

- `SOURCE_PATH_MISSING`
  - Trigger: source path does not exist.
  - Behavior: immediate failure.

- `SOURCE_PATH_NOT_DIRECTORY`
  - Trigger: source path exists but is not a directory.
  - Behavior: immediate failure.

- `OUTPUT_PATH_IS_DIRECTORY`
  - Trigger: output index path points to directory.
  - Behavior: immediate failure.

- `INDEX_PATH_MISSING`
  - Trigger: load path not found.
  - Behavior: immediate failure.

- `INDEX_PATH_NOT_FILE`
  - Trigger: load path is not file.
  - Behavior: immediate failure.

- `INDEX_JSON_PARSE_ERROR`
  - Trigger: persisted index JSON is malformed.
  - Behavior: immediate failure.

- `QUERY_LIMIT_INVALID`
  - Trigger: query limit <= 0.
  - Behavior: immediate failure.

- `STRICT_PROFILE_STORAGE_WARNING_FAILURE`
  - Trigger: strict storage mode enabled with warnings.
  - Behavior: fail storage stage with warning count.

- `PROFILE_STORAGE_INDEX_COMMAND_FAILED`
  - Trigger: wrapper command returns non-zero.
  - Behavior: PowerShell wrapper failure with exit code.
