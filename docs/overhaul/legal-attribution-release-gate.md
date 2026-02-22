# Release Gate: Legal and Attribution Checklist

## Purpose
Define engineering checks required before any public release artifact is published.

## Inputs
- Internal approval record for use of upstream logic/process patterns.
- Current branding policy (`docs/overhaul/naming-policy.md`).
- Source isolation policy (`docs/overhaul/source-isolation-policy.md`).

## Release-Blocking Checks
- Confirm no upstream project names/logos in shipped UI assets.
- Confirm no files from `overhaul/` are tracked or packaged.
- Confirm profile data imports use first-party schema and runtime mapping.
- Confirm attribution and legal text in product docs matches approved guidance.

## Artifact Verification
- Scan built bundles for banned upstream brand strings.
- Scan icon/splash assets for non-EON branding.
- Archive scan results with release notes.

## Ownership
- Engineering owner signs technical checks.
- Product owner signs branding checks.
- Final release is blocked until all items are checked complete.
