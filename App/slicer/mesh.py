from dataclasses import dataclass, field
import math
from typing import Dict, Iterable, List, Tuple

import trimesh

from .geometry import Island2D, slice_mesh, polygons_with_holes

@dataclass
class MeshModel:
    """Simple wrapper around a trimesh mesh."""
    path: str
    mesh: trimesh.Trimesh
    _slice_cache: Dict[float, List[Island2D]] = field(default_factory=dict,
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
        return cls(path=path, mesh=m)

    @classmethod
    def from_trimesh(cls, mesh: trimesh.Trimesh, path: str = "<memory>") -> "MeshModel":
        return cls(path=path, mesh=mesh)

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
            triangles.append((tuple(v0.tolist()),
                              tuple(v1.tolist()),
                              tuple(v2.tolist())))
        return triangles

    def slice_layer(self, z_height: float) -> List[Island2D]:
        """Return islands + holes for a single Z plane, cached by Z."""
        key = round(float(z_height), 6)
        cached = self._slice_cache.get(key)
        if cached is not None:
            return cached

        loops = slice_mesh(self.mesh, z_height)
        islands = polygons_with_holes(loops)
        self._slice_cache[key] = islands
        return islands

    def slice_layers(self, z_heights: Iterable[float]) -> Dict[float, List[Island2D]]:
        """Slice multiple Z planes and return a dict of cached results."""
        return {float(z): self.slice_layer(float(z)) for z in z_heights}
