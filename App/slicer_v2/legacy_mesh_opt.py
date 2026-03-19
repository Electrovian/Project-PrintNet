from __future__ import annotations

from typing import Optional, Tuple

import numpy as np
import trimesh


def wireframe_target_faces(face_count: int) -> int:
    if face_count <= 0:
        return 0
    if face_count < 50000:
        return face_count
    return max(20000, int(face_count * 0.1))


def simplify_mesh(vertices: np.ndarray,
                  faces: np.ndarray,
                  target_faces: int) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    if target_faces <= 0:
        return None
    if faces.shape[0] <= target_faces:
        return None
    try:
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    except Exception:
        return None
    simplify_attr = None
    if hasattr(mesh, "simplify_quadric_decimation"):
        simplify_attr = "simplify_quadric_decimation"
    elif hasattr(mesh, "simplify_quadratic_decimation"):
        simplify_attr = "simplify_quadratic_decimation"
    if simplify_attr is None:
        return None
    try:
        simplified = getattr(mesh, simplify_attr)(target_faces)
    except Exception:
        return None
    if simplified is None or simplified.faces.shape[0] == 0:
        return None
    return simplified.vertices, simplified.faces
