import os
import sys
import unittest
import trimesh

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
TESTS = os.path.abspath(os.path.dirname(__file__))
if TESTS not in sys.path:
    sys.path.insert(0, TESTS)

from slicer.mesh import MeshModel
from harness import BaseTestCase


class MeshModelTests(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls._box_mesh_template = trimesh.creation.box(extents=(2.0, 4.0, 6.0))

    def _box_mesh(self):
        return self._box_mesh_template.copy()

    def test_bounds(self):
        mesh = self._box_mesh()
        model = MeshModel.from_trimesh(mesh, path="box")
        bounds = model.bounds
        self.assertPointsAlmostEqual(bounds[0], (-1.0, -2.0, -3.0))
        self.assertPointsAlmostEqual(bounds[1], (1.0, 2.0, 3.0))

    def test_overhang_face_indices(self):
        mesh = self._box_mesh()
        model = MeshModel.from_trimesh(mesh, path="box")
        indices = model.overhang_face_indices(45.0)
        self.assertGreater(len(indices), 0)
        none_indices = model.overhang_face_indices(180.0)
        self.assertEqual(len(none_indices), 0)

    def test_overhang_triangles_count(self):
        mesh = self._box_mesh()
        model = MeshModel.from_trimesh(mesh, path="box")
        tris = model.overhang_triangles(45.0)
        indices = model.overhang_face_indices(45.0)
        self.assertEqual(len(tris), len(indices))
        self.assertTrue(all(len(tri) == 3 for tri in tris))

    def test_slice_layer_cache(self):
        mesh = self._box_mesh()
        model = MeshModel.from_trimesh(mesh, path="box")
        first = model.slice_layer(0.0)
        second = model.slice_layer(0.0)
        self.assertIs(first, second)
        self.assertIsInstance(first, list)

    def test_slice_layers_dict(self):
        mesh = self._box_mesh()
        model = MeshModel.from_trimesh(mesh, path="box")
        layers = model.slice_layers([0.0, 1.0])
        self.assertIn(0.0, layers)
        self.assertIn(1.0, layers)
        self.assertIsInstance(layers[0.0], list)


if __name__ == "__main__":
    unittest.main()
