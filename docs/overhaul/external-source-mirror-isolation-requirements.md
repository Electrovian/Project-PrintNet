# External Source Mirror Isolation Requirements

Date: 2026-02-13  
Checklist ID: `T041`

## Objective

Keep upstream mirror sources available for migration work while guaranteeing they are isolated from tracked first-party source.

## Required Outcomes

- Mirror sync must target the ignored `overhaul/` tree.
- Verification must detect tracked files under `overhaul/`.
- Verification must confirm required ignore rules are present.
- Sync must emit a manifest for traceability.

## Acceptance Criteria

- Mirror verification exits non-zero on any policy violation.
- Verification writes a JSON report.
- Unit and integration tests cover success and failure cases.
- End-to-end verification runtime remains under 20 seconds.
