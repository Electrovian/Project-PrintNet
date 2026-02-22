# Profile Inheritance and Merge Migration Notes

Date: 2026-02-13  
Checklist ID: `T079`

## Legacy Baseline

- Parent/child profile relationships were handled ad hoc.
- Missing-parent and cycle issues were discovered late during runtime.
- Merge precedence was not documented as a strict contract.

## Current Baseline

- Inheritance resolution is centralized in `App/profiles_import/inheritance.py`.
- Parent-chain resolution is deterministic and warning-driven.
- Child-over-parent precedence is explicit and reproducible.
- Strict mode can fail on inheritance warnings for gated workflows.

## Migration Impact

- Import flows should call `discover_and_resolve_profile_inheritance(...)` rather than bespoke merge paths.
- Downstream mapping should consume `resolved_data` and `inherits_chain` metadata.
- Existing manual merge utilities should be deprecated after parity checks pass.
