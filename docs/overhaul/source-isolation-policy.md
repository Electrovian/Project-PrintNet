# External Source Isolation Policy

## Goal
Allow local reference access to upstream code/processes while preventing accidental inclusion in this repository.

## Local Mirror Path
- Local-only mirror root: `overhaul/eon_engine_mirror`
- Git ignore rule: `overhaul/`

## Mandatory Rules
- Do not commit raw mirrored upstream files.
- Do not import upstream logos or brand assets into shipped UI.
- Re-implement runtime logic in first-party modules under `App/` and `platform/`.
- Treat mirrored source as read-only reference material.

## Allowed Imports
- Printer profile/preconfiguration data needed for runtime compatibility.
- Parser fixtures used in tests.
- Non-branded technical references for behavior parity.

## Disallowed Imports
- Upstream logos, names, splash screens, and theme assets.
- Upstream release packaging metadata and legal docs copied as if first-party docs.

## Verification
- `git status --short` must not include files from `overhaul/`.
- CI scan should fail if packaged artifacts contain banned upstream names/logos.
