# G-code Emission Semantics Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T244`

## Error Classes

- `GCODE_EMISSION_SEQUENCE_NON_NUMERIC`
  - Trigger: sequence input contains non-numeric value.
  - Behavior: raises `SlicerV2GCodeEmissionError`.

- `GCODE_EMISSION_SEQUENCE_NEGATIVE`
  - Trigger: sequence input contains negative count/length.
  - Behavior: raises `SlicerV2GCodeEmissionError`.

- `GCODE_EMISSION_SEQUENCE_NON_POSITIVE`
  - Trigger: required positive sequence values are zero/non-positive.
  - Behavior: raises `SlicerV2GCodeEmissionError`.

- `GCODE_EMISSION_PRINT_SPEED_INVALID`
- `GCODE_EMISSION_TRAVEL_SPEED_INVALID`
  - Trigger: print/travel speed is out of allowed range.
  - Behavior: raises `SlicerV2GCodeEmissionError`.

- `GCODE_EMISSION_RETRACT_LENGTH_INVALID`
  - Trigger: retract length is outside `0..20`.
  - Behavior: raises `SlicerV2GCodeEmissionError`.

- `GCODE_EMISSION_FIRMWARE_UNSUPPORTED`
  - Trigger: firmware flavor not supported by semantic emitter.
  - Behavior: raises `SlicerV2GCodeEmissionError`.

- `GCODE_EMISSION_MACRO_INVALID_TYPE`
- `GCODE_EMISSION_MACRO_INVALID_NEWLINE`
- `GCODE_EMISSION_MACRO_TOO_LONG`
  - Trigger: startup/end macro payload is invalid.
  - Behavior: raises `SlicerV2GCodeEmissionError`.

- `GCODE_EMISSION_LAYER_COUNT_EXCESSIVE`
  - Trigger: computed layer count exceeds safety cap.
  - Behavior: raises `SlicerV2GCodeEmissionError`.

- `SLICER_V2_GCODE_EMISSION_SMOKE_COMMAND_FAILED`
  - Trigger: smoke command exits non-zero.
  - Behavior: PowerShell wrapper failure with exit code.

## Warning Classes (report-level)

- `gcode_emission:layer_heights_short`
- `gcode_emission:layer_z_values_short`
- `gcode_emission:layer_filament_lengths_short`
- `layer_<idx>:travel_moves_without_length`
- `layer_<idx>:filament_without_path_length`
