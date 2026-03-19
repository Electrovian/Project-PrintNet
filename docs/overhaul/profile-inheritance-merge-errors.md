# Profile Inheritance and Merge Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T074`

## Error Classes

- `SOURCE_PATH_MISSING`
  - Trigger: source path does not exist.
  - Behavior: immediate failure.

- `SOURCE_PATH_NOT_DIRECTORY`
  - Trigger: source path exists but is not a directory.
  - Behavior: immediate failure.

- `PROFILE_FILE_MISSING`
  - Trigger: profile file listed by discovery is absent.
  - Behavior: immediate failure.

- `PROFILE_JSON_PARSE_ERROR`
  - Trigger: malformed profile JSON.
  - Behavior: immediate failure.

- `INVALID_MAX_CHAIN_DEPTH`
  - Trigger: non-positive max chain depth.
  - Behavior: immediate failure.

- `STRICT_INHERITANCE_WARNING_FAILURE`
  - Trigger: strict mode and warning count > 0.
  - Behavior: failure with warning count.

- `INHERITANCE_COMMAND_FAILED`
  - Trigger: wrapper script returns non-zero.
  - Behavior: PowerShell wrapper failure with exit code.
