# Vendor/Machine/Process/Filament Parsing Requirements

Date: 2026-02-13  
Checklist ID: `T061`

## Objective

Parse vendor index + machine/process/filament profile JSON files into deterministic typed summaries for downstream inheritance/merge stages.

## Required Outcomes

- Vendor index parser (`machine_model_list`, `process_list`, `filament_list`).
- Category profile parser with expected type checks.
- Warning model for mismatches/missing keys.
- Machine-readable report and human-readable summary outputs.

## Acceptance Criteria

- Invalid source path fails fast.
- Invalid JSON fails with explicit parse errors.
- Type mismatches are counted and surfaced in warnings.
- Unit/integration/performance checks pass.
