from __future__ import annotations

import math
from typing import Iterable, List, Tuple

import numpy as np


def face_normals_and_areas(vertices: np.ndarray, faces: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    if vertices.size == 0 or faces.size == 0:
        return np.zeros((0, 3), dtype=float), np.zeros((0,), dtype=float)
    tris = vertices[faces]
    v1 = tris[:, 1] - tris[:, 0]
    v2 = tris[:, 2] - tris[:, 0]
    normals = np.cross(v1, v2)
    lengths = np.linalg.norm(normals, axis=1)
    areas = lengths * 0.5
    normals_unit = np.zeros_like(normals)
    mask = lengths > 1e-9
    normals_unit[mask] = normals[mask] / lengths[mask][:, None]
    return normals_unit, areas


def select_candidate_normals(
    normals: np.ndarray,
    areas: np.ndarray,
    max_candidates: int = 24,
    dot_threshold: float = 0.995,
) -> List[np.ndarray]:
    if normals.size == 0 or areas.size == 0:
        return []
    order = np.argsort(-areas)
    candidates: List[np.ndarray] = []
    for idx in order:
        if len(candidates) >= max_candidates:
            break
        if not np.isfinite(areas[idx]) or areas[idx] <= 1e-9:
            continue
        n = normals[idx]
        if not np.all(np.isfinite(n)):
            continue
        if any(float(np.dot(n, c)) >= dot_threshold for c in candidates):
            continue
        candidates.append(n)
    return candidates


def rotation_from_to(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    a = np.array(source, dtype=float)
    b = np.array(target, dtype=float)
    a_norm = float(np.linalg.norm(a))
    b_norm = float(np.linalg.norm(b))
    if a_norm < 1e-9 or b_norm < 1e-9:
        return np.eye(3, dtype=float)
    a = a / a_norm
    b = b / b_norm
    c = float(np.dot(a, b))
    if c > 0.9999:
        return np.eye(3, dtype=float)
    if c < -0.9999:
        axis = np.array([1.0, 0.0, 0.0], dtype=float)
        if abs(a[0]) > 0.9:
            axis = np.array([0.0, 1.0, 0.0], dtype=float)
        axis = axis - a * float(np.dot(axis, a))
        axis_norm = float(np.linalg.norm(axis))
        if axis_norm < 1e-9:
            return np.eye(3, dtype=float)
        axis = axis / axis_norm
        return rotation_axis_angle(axis, math.pi)

    v = np.cross(a, b)
    s = float(np.linalg.norm(v))
    axis = v / max(1e-9, s)
    angle = math.atan2(s, c)
    return rotation_axis_angle(axis, angle)


def rotation_axis_angle(axis: np.ndarray, angle: float) -> np.ndarray:
    kx, ky, kz = axis
    c = float(math.cos(angle))
    s = float(math.sin(angle))
    v1 = 1.0 - c
    return np.array(
        [
            [kx * kx * v1 + c, kx * ky * v1 - kz * s, kx * kz * v1 + ky * s],
            [ky * kx * v1 + kz * s, ky * ky * v1 + c, ky * kz * v1 - kx * s],
            [kz * kx * v1 - ky * s, kz * ky * v1 + kx * s, kz * kz * v1 + c],
        ],
        dtype=float,
    )


def orientation_metrics(
    vertices: np.ndarray,
    faces: np.ndarray,
    normals: np.ndarray,
    areas: np.ndarray,
    rotation: np.ndarray,
    overhang_angle: float,
    bed_tol: float = 1e-4,
) -> Tuple[float, float]:
    if vertices.size == 0 or faces.size == 0:
        return 0.0, 0.0
    verts_rot = vertices @ rotation.T
    normals_rot = normals @ rotation.T
    z_vals = verts_rot[:, 2]
    min_z = float(np.min(z_vals))
    max_z = float(np.max(z_vals))
    height = max(0.0, max_z - min_z)

    tri_z = verts_rot[faces, 2]
    bed_mask = np.max(tri_z, axis=1) <= (min_z + float(bed_tol))

    cos_limit = math.cos(math.radians(float(overhang_angle)))
    overhang_mask = (normals_rot[:, 2] < cos_limit) & (normals_rot[:, 2] < 0.0) & (~bed_mask)
    support_area = float(np.sum(areas[overhang_mask]))
    return support_area, float(height)


def pick_best_orientation(metrics: Iterable[dict], mode: str) -> int | None:
    metrics_list = list(metrics)
    if not metrics_list:
        return None
    supports = np.array([m["support"] for m in metrics_list], dtype=float)
    heights = np.array([m["height"] for m in metrics_list], dtype=float)
    mode = (mode or "").strip().lower()
    if mode == "min_support":
        scores = supports + heights * 0.01
    elif mode == "min_time":
        scores = heights + supports * 0.01
    else:
        sup_range = float(np.ptp(supports))
        h_range = float(np.ptp(heights))
        sup_norm = (supports - float(np.min(supports))) / sup_range if sup_range > 1e-9 else 0.0
        h_norm = (heights - float(np.min(heights))) / h_range if h_range > 1e-9 else 0.0
        scores = 0.5 * sup_norm + 0.5 * h_norm
    return int(np.argmin(scores))
