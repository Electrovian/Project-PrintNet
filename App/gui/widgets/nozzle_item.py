from __future__ import annotations

import math
from typing import Tuple

import numpy as np
import pyqtgraph.opengl as gl


def make_cone_mesh(height: float, radius: float, segments: int) -> Tuple[np.ndarray, np.ndarray]:
    verts = []
    faces = []
    height_val = float(height)
    radius_val = float(radius)
    segs = max(3, int(segments))
    verts.append([0.0, 0.0, height_val])
    for i in range(segs):
        ang = (2.0 * math.pi * i) / segs
        verts.append([radius_val * math.cos(ang), radius_val * math.sin(ang), 0.0])
    tip_index = 0
    for i in range(segs):
        i0 = 1 + i
        i1 = 1 + ((i + 1) % segs)
        faces.append([tip_index, i0, i1])
    return np.array(verts, dtype=float), np.array(faces, dtype=int)


def flip_mesh_z(verts: np.ndarray, faces: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    flipped = np.array(verts, dtype=float, copy=True)
    if flipped.size:
        flipped[:, 2] *= -1.0
    new_faces = np.array(faces, dtype=int, copy=True)
    if new_faces.ndim == 2 and new_faces.shape[1] >= 3:
        new_faces[:, [1, 2]] = new_faces[:, [2, 1]]
    return flipped, new_faces


def nozzle_z_offset(height: float, tip_offset: float, z: float, flipped: bool) -> float:
    height_val = float(height)
    tip_val = float(tip_offset)
    z_val = float(z)
    if flipped:
        return z_val + tip_val + height_val
    return z_val + tip_val - height_val


class NozzleItem:
    def __init__(
        self,
        *,
        height: float = 18.0,
        radius: float = 4.0,
        segments: int = 20,
        color: Tuple[float, float, float, float] = (0.8, 0.8, 0.8, 0.7),
        flipped: bool = True,
    ):
        self.height = float(height)
        self._flipped = bool(flipped)
        verts, faces = make_cone_mesh(self.height, float(radius), int(segments))
        if self._flipped:
            verts, faces = flip_mesh_z(verts, faces)
        self._base_verts = verts
        self._faces = faces
        md = gl.MeshData(vertexes=verts, faces=faces)
        item = gl.GLMeshItem(meshdata=md, smooth=True, color=color, shader="shaded")
        item.setGLOptions("translucent")
        self.item = item

    def set_visible(self, visible: bool):
        self.item.setVisible(bool(visible))

    def update_position(self, x: float, y: float, z: float, tip_offset: float = 2.0):
        offset_z = nozzle_z_offset(self.height, tip_offset, z, self._flipped)
        offset = np.array([float(x), float(y), offset_z], dtype=float)
        new_verts = self._base_verts + offset
        self.item.setMeshData(meshdata=gl.MeshData(vertexes=new_verts, faces=self._faces))
