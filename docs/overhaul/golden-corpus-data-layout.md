# Deterministic Test-Data Layout for Golden Corpus

Task reference: `16`
Last updated: `2026-02-09`

## Goal

Define a deterministic, scalable storage layout for slicer golden fixtures and outputs so regression checks are reproducible across machines and runs.

## Root Layout

```text
tests/
  golden/
    slicer_v2/
      README.md
      fixtures/
        models/
        settings/
        profiles/
      expected/
        gcode/
        traces/
        metrics/
      manifests/
      reports/
```

## Directory Semantics

- `fixtures/models/`: source STL/3MF test geometry inputs.
- `fixtures/settings/`: normalized slicer settings JSON per case.
- `fixtures/profiles/`: resolved profile snapshots used by case.
- `expected/gcode/`: canonical expected G-code outputs.
- `expected/traces/`: pipeline trace JSON outputs.
- `expected/metrics/`: expected summary metrics (time, length, mass).
- `manifests/`: immutable corpus index and checksum files.
- `reports/`: generated comparison reports (not committed by default unless approved).

## Naming Convention

Case id pattern:

`<class>__<model>__<profile>__<variant>`

Example:

- `bridge__cantilever_block__mk4_0p4__baseline`
- `thinwall__tube_0p45__x1c_0p4__low_flow`

File naming:

- `<case_id>.stl` in `fixtures/models/`
- `<case_id>.settings.json` in `fixtures/settings/`
- `<case_id>.profile.json` in `fixtures/profiles/`
- `<case_id>.gcode` in `expected/gcode/`
- `<case_id>.trace.json` in `expected/traces/`
- `<case_id>.metrics.json` in `expected/metrics/`

## Determinism Rules

- Fixture settings must include explicit random seed for any randomized behavior.
- Golden comparisons:
  - Primary: semantic token comparison for G-code (not raw whitespace sensitive).
  - Secondary: normalized line comparison for deterministic sections.
- Numeric tolerances:
  - geometry/traces: `1e-6` where feasible
  - metrics: explicit per-metric tolerance documented in case manifest

## Manifest Format

`tests/golden/slicer_v2/manifests/corpus.v1.json`

Required fields per case:

- `case_id`
- `model_file`
- `settings_file`
- `profile_file`
- `expected_gcode_file`
- `expected_trace_file`
- `expected_metrics_file`
- `checksums` (sha256 per artifact)
- `tags` (e.g. `bridge`, `thinwall`, `support`)

## Mutation Policy

- Golden files can only change with explicit rationale in PR notes.
- Any golden update must include:
  - reason for change
  - impacted case ids
  - summary of semantic deltas
- New cases require manifest entry and checksums in same change.

## Fine-Grained Implementation Checklist

- [x] Define corpus directory tree and naming conventions.
- [x] Define determinism and comparison rules.
- [x] Define manifest schema and mutation policy.
- [ ] Add initial `tests/golden/slicer_v2/` directory scaffold.
- [ ] Add first corpus manifest with baseline case set.
- [ ] Add harness wiring for automated golden validation (task `227`).

