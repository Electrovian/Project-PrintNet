from dataclasses import dataclass
from typing import Tuple

import trimesh

@dataclass
class MeshModel:
    """Simple wrapper around a trimesh mesh."""
    path: str
    mesh: trimesh.Trimesh

    @classmethod
    def from_file(cls, path: str) -> "MeshModel":
        m = trimesh.load(path, force="mesh")
        if not isinstance(m, trimesh.Trimesh):
            # If it's a Scene, merge into one mesh
            m = trimesh.util.concatenate(m.dump())
        return cls(path=path, mesh=m)

    @property
    def bounds(self) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        mn, mx = self.mesh.bounds
        return tuple(mn.tolist()), tuple(mx.tolist())
