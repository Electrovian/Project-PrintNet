# EON-OpenSlicer Branding and Compliance Baseline

Date: 2026-02-13

## Naming Policy (T005)

- All new user-facing naming must use `EON-OpenSlicer`.
- Do not present upstream product names in UI titles, splash text, onboarding copy, or release notes.
- Any upstream references that are required for engineering context must stay in internal docs only.

## User-Facing Brand String Audit (T006)

Scope scanned on 2026-02-13:
- `App/`
- `docs/`
- `README.md`

Findings:
- `App/README.md` previously contained `Bambu style` wording and was updated.
- `App/gui/viewer/core.py` contained a non-user-facing comment with `Bambu-like` wording and was updated.
- No remaining direct Orca/Bambu strings were found in scanned user-facing copy after this patch set.

## Asset Name Audit (T007)

Scope scanned on 2026-02-13:
- `App/assets/`

Findings:
- Current icon filenames (`app_icon.png`, `open.png`, `print.png`, `slice.png`) are neutral.
- No upstream-brand identifiers were found in asset filenames.

## Legal Attribution Strategy (T008)

- Runtime code will remain EON-OpenSlicer authored code and naming.
- Upstream-inspired implementation details are treated as reference input, not copied branding.
- If direct upstream files are mirrored locally for migration analysis, they remain outside version control in ignored local folders.
- Attribution notes, when needed, will be maintained in internal engineering documentation and not embedded as end-user branding.

## External Source Isolation Policy (T009)

- External upstream mirrors must reside under `overhaul/`.
- `overhaul/` is git-ignored to prevent accidental commits.
- Sync operations must use explicit scripts, source paths, and target paths for traceability.
- Production/runtime imports from local mirrors are not allowed without explicit review and dedicated import pipelines.
