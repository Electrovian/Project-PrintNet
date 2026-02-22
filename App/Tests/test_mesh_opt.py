import os
import sys
import unittest

import trimesh

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.legacy_mesh_opt import simplify_mesh, wireframe_target_faces


class MeshOptTests(unittest.TestCase):
    def test_simplify_mesh_reduces_faces(self):
        mesh = trimesh.creation.icosphere(subdivisions=2, radius=10.0)
        target = wireframe_target_faces(mesh.faces.shape[0])
        result = simplify_mesh(mesh.vertices, mesh.faces, target)
        if result is None:
            self.skipTest("Mesh simplification not available")
        vertices, faces = result
        self.assertLessEqual(faces.shape[0], target)
        self.assertGreater(vertices.shape[0], 0)


if __name__ == "__main__":
    unittest.main()

