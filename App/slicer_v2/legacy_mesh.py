from dataclasses import dataclass, field
from collections import OrderedDict
import math
from typing import Dict, Iterable, List, Tuple

import trimesh
import threading

from .legacy_geometry import Island2D, slice_mesh, polygons_with_holes

@dataclass
class MeshModel:
    """Simple wrapper around a trimesh mesh."""
    path: str
    mesh: trimesh.Trimesh
    _slice_cache: OrderedDict[Tuple[float, float], List[Island2D]] = field(default_factory=OrderedDict,
                                                            init=False,
                                                            repr=False)
    _slice_cache_bytes: Dict[Tuple[float, float], int] = field(default_factory=dict,
                                                               init=False,
                                                               repr=False)
    _slice_cache_total_bytes: int = field(default=0,
                                          init=False,
                                          repr=False)
    _slice_cache_limit_bytes: int | None = field(default=None,
                                                 init=False,
                                                 repr=False)
    _slice_cache_lock: threading.RLock = field(default_factory=threading.RLock,
                                               init=False,
                                               repr=False)

    @classmethod
    def from_file(cls, path: str) -> "MeshModel":
        m = trimesh.load(path, force="mesh")
        if not isinstance(m, trimesh.Trimesh):
            # If it's a Scene, merge into one mesh
            dump = getattr(m, "dump", None)
            if callable(dump):
                m = trimesh.util.concatenate(dump())
            else:
                m = trimesh.util.concatenate(m)
        model = cls(path=path, mesh=m)
        _apply_default_cache_limit(model)
        return model

    @classmethod
    def from_trimesh(cls, mesh: trimesh.Trimesh, path: str = "<memory>") -> "MeshModel":
        model = cls(path=path, mesh=mesh)
        _apply_default_cache_limit(model)
        return model

    @property
    def bounds(self) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        mn, mx = self.mesh.bounds
        return tuple(mn.tolist()), tuple(mx.tolist())

    def overhang_face_indices(self, overhang_angle: float) -> List[int]:
        """Return face indices considered overhangs by normal angle."""
        normals = self.mesh.face_normals
        cos_limit = math.cos(math.radians(float(overhang_angle)))
        mask = (normals[:, 2] < cos_limit) & (normals[:, 2] < 0.0)
        return [index for index, flag in enumerate(mask) if flag]

    def overhang_triangles(self, overhang_angle: float) -> List[Tuple[Tuple[float, float, float],
                                                                     Tuple[float, float, float],
                                                                     Tuple[float, float, float]]]:
        """Return triangles for faces exceeding the overhang angle."""
        normals = self.mesh.face_normals
        cos_limit = math.cos(math.radians(float(overhang_angle)))
        mask = (normals[:, 2] < cos_limit) & (normals[:, 2] < 0.0)
        faces = self.mesh.faces[mask]
        vertices = self.mesh.vertices
        triangles = []
        for face in faces:
            v0, v1, v2 = vertices[face]
            triangles.append((tuple(v0),
                              tuple(v1),
                              tuple(v2)))
        return triangles

    def slice_layer(self, z_height: float, tolerance: float = 0.0) -> List[Island2D]:
        """Return islands + holes for a single Z plane, cached by Z."""
        try:
            tol = float(tolerance)
        except (TypeError, ValueError):
            tol = 0.0
        key = (round(float(z_height), 6), round(tol, 6))
        with self._slice_cache_lock:
            cached = self._slice_cache.get(key)
            if cached is not None:
                self._slice_cache.move_to_end(key)
                return cached

        loops = slice_mesh(self.mesh, z_height, tolerance=tol)
        islands = polygons_with_holes(loops)
        with self._slice_cache_lock:
            self._slice_cache[key] = islands
            self._slice_cache.move_to_end(key)
            estimated = _estimate_islands_bytes(islands)
            prev = self._slice_cache_bytes.get(key, 0)
            self._slice_cache_bytes[key] = estimated
            self._slice_cache_total_bytes += max(0, estimated - prev)
            self._enforce_cache_limit()
        return islands

    def slice_layers(self,
                     z_heights: Iterable[float],
                     tolerance: float = 0.0) -> Dict[float, List[Island2D]]:
        """Slice multiple Z planes and return a dict of cached results."""
        return {float(z): self.slice_layer(float(z), tolerance=tolerance) for z in z_heights}

    def set_slice_cache_limit(self, max_mb: float | None):
        with self._slice_cache_lock:
            if max_mb is None:
                self._slice_cache_limit_bytes = None
            else:
                limit = max(1.0, float(max_mb))
                self._slice_cache_limit_bytes = int(limit * 1024 * 1024)
            self._enforce_cache_limit()

    def clear_slice_cache(self):
        with self._slice_cache_lock:
            self._slice_cache.clear()
            self._slice_cache_bytes.clear()
            self._slice_cache_total_bytes = 0

    def _enforce_cache_limit(self):
        if self._slice_cache_limit_bytes is None:
            return
        limit = self._slice_cache_limit_bytes
        while self._slice_cache_total_bytes > limit and self._slice_cache:
            key, _value = self._slice_cache.popitem(last=False)
            removed = self._slice_cache_bytes.pop(key, 0)
            self._slice_cache_total_bytes = max(0, self._slice_cache_total_bytes - removed)


def _estimate_islands_bytes(islands: List[Island2D]) -> int:
    point_count = 0
    for outer, holes in islands:
        point_count += len(outer)
        for hole in holes:
            point_count += len(hole)
    if point_count <= 0:
        return 0
    # Roughly 20-30% higher than the previous estimate to account for list/tuple overhead.
    bytes_per_point = 40
    return int(point_count * bytes_per_point)


def _apply_default_cache_limit(model: MeshModel):
    try:
        from config.performance import resolve_performance_limits
        from config.defaults import DEFAULTS
    except Exception:
        return
    limits = resolve_performance_limits(DEFAULTS.get("performance"))
    max_mb = limits.get("max_slice_cache_mb")
    if max_mb is None:
        return
    try:
        model.set_slice_cache_limit(float(max_mb))
    except Exception:
        return

