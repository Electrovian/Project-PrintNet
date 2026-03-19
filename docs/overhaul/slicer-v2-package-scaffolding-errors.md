# slicer_v2 Package Scaffolding Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T104`

## Error Classes

- `PRE_PIPELINE_VALIDATION_FAILED`
  - Trigger: pre-run context validation contains errors.
  - Behavior: raises `SlicerV2ValidationError`.

- `MESH_PATH_EMPTY`
  - Trigger: mesh path missing/blank in `SlicerContext`.
  - Behavior: validation failure.

- `MESH_PATH_MISSING`
  - Trigger: mesh file path does not exist.
  - Behavior: validation failure.

- `MESH_PATH_NOT_FILE`
  - Trigger: mesh path is not a file.
  - Behavior: validation failure.

- `SETTINGS_NOT_DICT`
  - Trigger: resolved settings payload is not a dict.
  - Behavior: validation failure.

- `SLICER_V2_CANCELLED_BEFORE_STAGE`
  - Trigger: cancellation flag set before a stage executes.
  - Behavior: raises `SlicerV2CancelledError`.

- `STAGE_FAILED`
  - Trigger: stage runner raises exception.
  - Behavior: raises `SlicerV2StageError`.

- `STAGE_ARTIFACT_MISSING`
  - Trigger: stage completed without registering artifact.
  - Behavior: post-validation failure.

- `STAGE_SEQUENCE_MISMATCH`
  - Trigger: executed stage order differs from `STAGE_SEQUENCE`.
  - Behavior: post-validation failure.

- `POST_PIPELINE_VALIDATION_FAILED`
  - Trigger: post-run validations contain errors.
  - Behavior: raises `SlicerV2ValidationError`.

- `SLICER_V2_SCAFFOLD_SMOKE_COMMAND_FAILED`
  - Trigger: smoke script process exits non-zero.
  - Behavior: wrapper failure with exit code.
