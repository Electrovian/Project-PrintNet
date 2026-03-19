from __future__ import annotations

from .mesh_slicing import load_mesh_file
from .types import SlicerContext


STAGE_NAME = "mesh"


def run(context: SlicerContext) -> dict:
    mesh_data = load_mesh_file(context.mesh_path)
    artifact = {
        "mesh_path": mesh_data.mesh_path,
        "mesh_loaded": True,
        "mesh_source_format": mesh_data.source_format,
        "triangle_count": len(mesh_data.triangles),
        "x_min_mm": mesh_data.x_min_mm,
        "x_max_mm": mesh_data.x_max_mm,
        "y_min_mm": mesh_data.y_min_mm,
        "y_max_mm": mesh_data.y_max_mm,
        "z_min_mm": mesh_data.z_min_mm,
        "z_max_mm": mesh_data.z_max_mm,
        "mesh_data": mesh_data,
    }
    context.stage_artifacts[STAGE_NAME] = artifact
    return artifact
