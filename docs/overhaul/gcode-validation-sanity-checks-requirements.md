# G-code Validation and Sanity Checks Requirements

Date: 2026-02-13  
Checklist ID: `T251`

## Objective

Add deterministic post-emission G-code validation to `slicer_v2` to catch out-of-bounds moves, parse issues, and invalid sequencing before print handoff.

## Required Outcomes

- Dedicated validation module with typed report and issue records.
- Bed/build-volume bounds checks for emitted motion commands.
- Z monotonicity and extrusion monotonicity sanity checks with configurable strictness.
- Structured issue reporting in `gcode` stage artifacts.
- Configurable strict mode that can fail the stage on validation errors.

## Acceptance Criteria

- Validation executes on emitted G-code when enabled.
- Stage artifact exposes `gcode_validation_ok`, error/warning counts, and detailed report payload.
- Strict mode raises a stage error if validation detects errors.
- Unit/integration/performance checks pass within runtime budget.
- Usage/defaults, migration notes, and completion gate docs are published.
