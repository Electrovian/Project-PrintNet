from __future__ import annotations

from .mesh_slicing import MeshData, slice_mesh_to_contours
from .runtime import resolve_worker_count
from .types import SlicerContext


STAGE_NAME = "regions"


def run(context: SlicerContext) -> dict:
    mesh_artifact = context.stage_artifacts.get("mesh", {})
    grid = context.stage_artifacts.get("slice_grid", {})
    mesh_data = mesh_artifact.get("mesh_data")
    layer_z_values = grid.get("layer_z_values_mm", [])

    contour_sets = []
    segment_total = 0
    contour_total = 0
    contour_warning_count = 0
    if isinstance(mesh_data, MeshData) and isinstance(layer_z_values, list):
        worker_count = resolve_worker_count(context.runtime_settings, len(layer_z_values), default=1)
        contour_sets, contour_report = slice_mesh_to_contours(
            mesh_data,
            layer_z_values,
            max_workers=worker_count,
        )
        segment_total = contour_report.segment_count_total
        contour_total = contour_report.contour_count_total
        contour_warning_count = contour_report.warning_count

    layer_count = int(grid.get("layer_count", 0))
    region_count = max(1, contour_total if contour_total > 0 else layer_count)
    layer_contour_counts = [int(item.contour_count) for item in contour_sets]
    layer_segment_counts = [int(item.segment_count) for item in contour_sets]
    layer_contours = [list(item.contours) for item in contour_sets]

    artifact = {
        "region_count": region_count,
        "region_strategy": "mesh-slice-contours",
        "layer_count": len(contour_sets) if contour_sets else layer_count,
        "layer_contour_counts": layer_contour_counts,
        "layer_segment_counts": layer_segment_counts,
        "layer_contours": layer_contours,
        "segment_count_total": segment_total,
        "contour_count_total": contour_total,
        "contour_warning_count": contour_warning_count,
    }
    context.stage_artifacts[STAGE_NAME] = artifact
    return artifact
