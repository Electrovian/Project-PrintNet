# Rollback Strategy by Migration Phase

Task reference: `19`
Last updated: `2026-02-09`

## Objective

Define explicit rollback triggers and execution steps for each major migration phase so failures can be contained quickly without blocking core desktop print operations.

## Rollback Principles

- Prefer feature-flag rollback over code revert when possible.
- Preserve last-known-good desktop print path (`v1 slicer` + stable connector behavior).
- Rollbacks must be idempotent and executable by on-call operator without new code changes.
- Every rollback action should emit telemetry/audit events.

## Phase Rollback Matrix

| Phase | Scope | Trigger | Primary Rollback | Validation Gate |
|---|---|---|---|---|
| P1 | Desktop stability fixes | New crash/regression in print/send path | Revert to last stable release tag for desktop UI/controller package | Load model -> slice -> export/send smoke passes |
| P2 | `slicer_v2` integration | Incorrect slices, critical G-code invalidation, high fail rate | Disable `USE_SLICER_V2`, force v1 path | Golden baseline sample + one real-device smoke print |
| P3 | Profiles import runtime path | Import failures, bad mapping causing invalid settings | Disable one-time import path; use cached/stable profile snapshot | Profile selection + sample slice passes |
| P4 | Connector registry integration | Connector command failures or wrong protocol selection | Fallback to prior connector binding (OctoPrint-only fallback path where needed) | Health check + upload/start for active printer |
| P5 | Backend/worker queue path | Job loss, status drift, worker instability | Route desktop direct path only; disable backend job submit endpoints | Direct desktop flow stable; backend returns maintenance state |
| P6 | Mongo/Redis persistence | Data corruption or unavailable persistence | Switch to read-only maintenance mode; pause writes and jobs | No new writes; existing job/status reads stable |
| P7 | k3d/K8s deploy rollout | Failed rollout or bad release image | Roll back Helm release revision; pin previous image tags | Liveness/readiness/ingress checks green |

## Detailed Playbooks

### Playbook A: Slicer v2 rollback

1. Set `USE_SLICER_V2=false`.
2. Restart desktop app process.
3. Emit event `desktop.slice.rollback.activate`.
4. Run smoke: load STL, slice, preview, export, send.
5. Record incident with sample failing case IDs.

### Playbook B: Connector rollback

1. Freeze new printer registration edits.
2. Force connector type to last known good per affected printer.
3. Emit event `desktop.connector.rollback.activate`.
4. Run health/upload/status check against affected printer.
5. Re-enable updates only after passing checks.

### Playbook C: Platform deployment rollback

1. `helm history` identify previous stable revision.
2. `helm rollback` to stable revision.
3. Verify API health, worker heartbeat, frontend availability.
4. Emit event `backend.system.rollback.activate`.
5. Keep new writes paused until postmortem confirms root cause.

## Data Safety and Audit Requirements

- Keep immutable import manifests and job event logs even during rollback.
- Never delete queue/job records during rollback execution.
- Tag all rollback events with:
  - `rollback_phase`
  - `rollback_reason`
  - `operator_id`
  - `build_version_from`
  - `build_version_to`

## Fine-Grained Implementation Checklist

- [x] Define rollback matrix by migration phase with trigger/action/gate.
- [x] Define executable playbooks for slicer, connector, and deployment rollback.
- [x] Define data safety + audit requirements during rollback.
- [ ] Add scripted rollback helpers for platform Helm revisions.
- [ ] Add desktop runtime flag toggle helper and rollback status banner.
- [ ] Add rollback drills to release readiness review (`229`).

