# Technical Debt Register: Slicer and Connect Flows

Task reference: `9`
Last updated: `2026-02-09`

## Scope

This register records current known technical debt in:

- Desktop slicing flow (`App/gui/Windows/controller/print.py`, `App/gui/Windows/controller/ui.py`)
- Slicer runtime and orchestration (`App/slicer_v2`)
- Printer connectivity path (`App/integrations/printer_manager.py`, `App/connectors`)

## Debt Items

| ID | Area | Description | Impact | Evidence | Linked Plan Tasks |
|---|---|---|---|---|---|
| TD-SC-001 | Desktop print cache | `_last_gcode_path` invalidation is still partial and relies on selected reset paths. | Can send stale G-code after transform/settings changes. | `App/gui/Windows/controller/print.py`, `App/gui/Windows/controller/ui.py` | `28`, `29`, `42` |
| TD-SC-002 | Printer state sync | Printer selection propagation is not fully consistent across all views. | Wrong target device risk and UX drift. | `App/gui/Windows/controller/ui.py`, `App/gui/Windows/device.py`, `App/gui/Windows/control.py` | `30`, `32`, `43` |
| TD-SC-003 | Slice cancellation lifecycle | Long-running slice workers need stronger cancellation-safe wrapping and state transitions. | UI lockups, ghost jobs, user confusion. | `App/gui/Windows/controller/print.py` | `39`, `40` |
| TD-SC-004 | Slicer v2 geometry depth | Core stage logic exists, but advanced geometry robustness and deterministic edge handling remain incomplete. | Incorrect paths on thin/complex geometry; parity risk. | `App/slicer_v2/geometry.py`, `App/slicer_v2/perimeters.py`, `App/slicer_v2/infill.py` | `82-111`, `115-120` |
| TD-SC-005 | Motion/extrusion semantics | Travel/retraction/flow policies are still MVP-level and need fuller policy coverage. | Print quality regressions and firmware-specific mismatches. | `App/slicer_v2/travel.py`, `App/slicer_v2/gcode.py` | `121-137`, `145-147` |
| TD-SC-006 | Output validation depth | Validation exists but not yet complete for bounds, supportability, and deterministic ordering gates. | Late print failures and reduced safety checks. | `App/slicer_v2/validators.py` | `140-144` |
| TD-SC-007 | Connector telemetry | Connector commands/errors are not fully mapped into standardized telemetry events. | Limited observability and slower incident triage. | `App/integrations/printer_manager.py`, `App/connectors/*.py` | `192`, `205` |
| TD-SC-008 | Connector test matrix | Protocol smoke/contract/failure-mode tests are incomplete. | Runtime regressions may escape before deployment. | `App/Tests/test_connectors_*.py` | `197-203` |
| TD-SC-009 | Credential handling | Secure credential storage abstraction is not complete across desktop/backend boundary. | Security and operability risk. | `App/connectors`, `platform/backend` | `193` |
| TD-SC-010 | Backend persistence path | Backend still uses in-memory state for critical entities. | Non-durable jobs/imports; restart loss. | `platform/backend/app/db/state.py` | `211`, `173-175` |

## Fine-Grained Remediation Queue

### High Priority (Blockers for stable print workflows)

- [ ] Enforce deterministic `_last_gcode_path` invalidation on any mesh transform and slicing setting mutation.
- [ ] Add multi-view printer-selection synchronization tests and fix inconsistent propagation paths.
- [ ] Add cancellation-safe worker wrapper and explicit state transitions for slice/upload/print lifecycle.

### Medium Priority (Correctness and quality)

- [ ] Complete geometry robustness items (winding, hole containment, offsets, topology cleanup).
- [ ] Complete motion and extrusion policy depth (retraction strategy, seam/wipe behavior, flow overrides).
- [ ] Finish output validation gates (bounds, support span sanity, deterministic feature ordering checks).

### Medium Priority (Connect reliability and observability)

- [ ] Standardize connector telemetry events and error codes.
- [ ] Complete connector contract tests, network-drop tests, and duplicate-start idempotency checks.

### Security and platform durability

- [ ] Implement secure credential storage abstraction (desktop encrypted + backend secret refs).
- [ ] Replace in-memory backend store with Mongo persistence and Redis-backed worker coordination.

