# Slicer Settings Normalization Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T114`

## Error Classes

- `SETTINGS_PAYLOAD_NOT_DICT`
  - Trigger: non-dict payload passed to normalization.
  - Behavior: raises `SlicerV2SettingsNormalizationError`.

- `STRICT_SETTINGS_NORMALIZATION_WARNING_FAILURE`
  - Trigger: strict mode enabled and warnings are present.
  - Behavior: raises `SlicerV2SettingsNormalizationError`.

- `SLICER_V2_SETTINGS_NORMALIZATION_COMMAND_FAILED`
  - Trigger: normalization wrapper script exits non-zero.
  - Behavior: PowerShell wrapper failure with exit code.

## Warning Classes (Non-strict mode)

- `invalid_float`
- `invalid_int`
- `invalid_bool`
- `empty_choice`
- `invalid_choice`
