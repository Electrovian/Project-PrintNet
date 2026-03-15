# Vendor Profile Parsing Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T064`

## Error Classes

- `SOURCE_PATH_MISSING`
  - Trigger: source path does not exist.
  - Behavior: immediate failure.

- `SOURCE_PATH_NOT_DIRECTORY`
  - Trigger: source path exists but is not a directory.
  - Behavior: immediate failure.

- `PROFILE_FILE_MISSING`
  - Trigger: expected profile file is missing.
  - Behavior: immediate failure.

- `PROFILE_JSON_PARSE_ERROR`
  - Trigger: malformed JSON profile content.
  - Behavior: immediate failure.

- `PROFILE_JSON_NOT_OBJECT`
  - Trigger: JSON root is not an object.
  - Behavior: immediate failure.

- `STRICT_PARSING_WARNING_FAILURE`
  - Trigger: strict parsing mode enabled and warnings exist.
  - Behavior: parsing fails with warning count.

- `PARSING_COMMAND_FAILED`
  - Trigger: wrapper script process exits non-zero.
  - Behavior: PowerShell wrapper fails with exit code.
