# Slicer v1 Compatibility Reference (Frozen)

Task reference: `49`  
Last updated: `2026-02-10`

## Purpose

Freeze current v1 slicer behavior as a stable compatibility baseline while `slicer_v2` work continues behind feature flag and fallback.

## Source of Truth

- Manifest: `tests/golden/slicer_v1/manifests/corpus.v1.json`
- Generator: `scripts/freeze-slicer-v1-baseline.py`

## Frozen Case Set

- `v1_box_default__mk4_0p4__baseline`
- `v1_dual_island_infill__mk4_0p4__baseline`
- `v1_cylinder_walls__mk4_0p4__baseline`

## Freeze Command

```powershell
python .\scripts\freeze-slicer-v1-baseline.py --mode freeze
```

## Verify Command

```powershell
python .\scripts\freeze-slicer-v1-baseline.py --mode verify
```

## Current Baseline Checksums (G-code)

- `v1_box_default__mk4_0p4__baseline`: `70af332896287e6e550534064a0885ea8656fb15f0f549ca5927fd54a0ebf5f6`
- `v1_dual_island_infill__mk4_0p4__baseline`: `98bbf1ef0372a794a56e62da93771a0bdc88b2a0f9dbd82601f5c2ae06cc9346`
- `v1_cylinder_walls__mk4_0p4__baseline`: `db4e067054931de8e63baf7a574ab1a8d3392000f106fda306bcbf14078c09e8`

## Compatibility Rule

Until task `150` declares v2 emitter stability, any intentional behavior change in v1 fallback comparisons must:

1. include rationale, impacted case IDs, and semantic delta summary;
2. refresh the frozen artifacts and manifest checksums in the same change;
3. preserve rollback ability to current v1 fallback path (`USE_SLICER_V2` disabled).
