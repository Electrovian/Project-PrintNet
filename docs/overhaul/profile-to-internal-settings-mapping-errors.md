# Profile-to-Internal Settings Mapping Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T084`

## Error Classes

- `SOURCE_PATH_MISSING`
  - Trigger: source path does not exist.
  - Behavior: immediate failure.

- `SOURCE_PATH_NOT_DIRECTORY`
  - Trigger: source path exists but is not a directory.
  - Behavior: immediate failure.

- `STRICT_MAPPING_WARNING_FAILURE`
  - Trigger: strict mapping mode enabled and mapping warnings exist.
  - Behavior: fail mapping stage with warning count.

- `PROFILE_SETTINGS_MAPPING_COMMAND_FAILED`
  - Trigger: PowerShell wrapper command returns non-zero.
  - Behavior: wrapper fails with exit code.

## Warning Classes (Non-fatal in Non-strict Mode)

- `invalid_float`
- `invalid_int`
- `invalid_bool`
- `invalid_percent`
- `invalid_ratio`
- `invalid_bed_shape`
- `insufficient_bed_shape_points`
- `unknown_category`
