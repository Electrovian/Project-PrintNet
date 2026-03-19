# G-code Validation and Sanity Checks Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T254`

## Error Classes

- `GCODE_VALIDATION_LINES_NOT_SEQUENCE`
  - Trigger: `lines` input is not a sequence.
  - Behavior: raises `SlicerV2GCodeValidationError`.

- `GCODE_VALIDATION_INVALID_PARAMETER:<name>:<value>`
  - Trigger: invalid bounds, tolerance, or line limits.
  - Behavior: raises `SlicerV2GCodeValidationError`.

- `GCODE_VALIDATION_LINE_COUNT_EXCEEDED`
  - Trigger: line count exceeds configured maximum.
  - Behavior: raises `SlicerV2GCodeValidationError`.

- `GCODE_VALIDATION_NUMERIC_TOKEN_MISSING`
- `GCODE_VALIDATION_NUMERIC_TOKEN_INVALID`
  - Trigger: malformed motion token value (for `X/Y/Z/E/F/S` parsing).
  - Behavior: report error entry (and strict mode can fail stage).

- `GCODE_VALIDATION_X_NEGATIVE`
- `GCODE_VALIDATION_Y_NEGATIVE`
- `GCODE_VALIDATION_Z_NEGATIVE`
- `GCODE_VALIDATION_X_BOUNDS_EXCEEDED`
- `GCODE_VALIDATION_Y_BOUNDS_EXCEEDED`
- `GCODE_VALIDATION_Z_BOUNDS_EXCEEDED`
  - Trigger: commanded move exceeds configured machine bounds.
  - Behavior: report error entry.

- `GCODE_VALIDATION_Z_NON_MONOTONIC`
  - Trigger: commanded Z decreases while monotonic-Z check is enabled.
  - Behavior: report error entry.

- `GCODE_VALIDATION_E_NON_MONOTONIC`
  - Trigger: absolute extrusion decreases outside allowed retract context.
  - Behavior: report error entry.

- `GCODE_VALIDATION_UNKNOWN_COMMAND`
  - Trigger: non-`G/M/T` unknown command token.
  - Behavior: report error entry.

- `GCODE_VALIDATION_FAILED:<count>`
  - Trigger: strict mode enabled and validation produced errors.
  - Behavior: raises `SlicerV2GCodeValidationError`.

## Warning Classes

- `GCODE_VALIDATION_LINE_TOO_LONG`
- `GCODE_VALIDATION_ABSOLUTE_RETRACT_ALLOWED`
- `GCODE_VALIDATION_RELATIVE_NEGATIVE_E`
- `GCODE_VALIDATION_UNSUPPORTED_COMMAND`
