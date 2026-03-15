# EON-OpenSlicer Overhaul Migration Workflow

Date: 2026-02-13

## Branch and Commit Conventions (T010)

- Primary overhaul branch family: `overhaul/<stream>-<short-topic>`.
- High-risk migration work must be isolated per stream:
  - `overhaul/slicer-core-*`
  - `overhaul/profiles-*`
  - `overhaul/connectors-*`
  - `overhaul/platform-*`
- Keep commits atomic and scoped to one checklist task or one tightly coupled task pair.

## Pull Request Expectations

- Every PR must link checklist IDs (for example: `T124`, `T125`).
- Every PR must include:
  - changed modules list
  - test evidence
  - rollback note
  - migration impact note

## Protection Rules

- No direct pushes to protected integration branches.
- Require passing test and lint checks before merge.
- Require at least one technical review for connector, slicer, or auth/security changes.

## Task Tracking Rules

- `docs/overhaul/task-checklist.md` is the source of truth for progress.
- Use `scripts/update-task-checklist.ps1` to mark task state.
- Long-form notes and tradeoffs go to `docs/overhaul/general-thoughts.txt`.
