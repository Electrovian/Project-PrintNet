# External Source Mirror Isolation Error Taxonomy

Date: 2026-02-13  
Checklist ID: `T044`

## Error Classes

- `SOURCE_PATH_MISSING`
  - Trigger: sync source path does not exist.
  - Behavior: immediate failure.

- `TARGET_POLICY_VIOLATION`
  - Trigger: sync target path is outside `overhaul/`.
  - Behavior: immediate failure.

- `PROFILES_SOURCE_MISSING`
  - Trigger: `-ProfilesOnly` set and source `resources/profiles` missing.
  - Behavior: immediate failure.

- `ROBOCOPY_FAILURE`
  - Trigger: `robocopy` exit code >= 8.
  - Behavior: sync failure with exit details.

- `GITIGNORE_RULE_MISSING`
  - Trigger: required ignore rule not found in `.gitignore`.
  - Behavior: verification failure.

- `TRACKED_MIRROR_FILES_FOUND`
  - Trigger: any tracked file detected under mirror root.
  - Behavior: verification failure.
