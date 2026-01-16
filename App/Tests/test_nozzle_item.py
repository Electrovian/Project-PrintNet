import unittest

import numpy as np

from gui.widgets.nozzle_item import flip_mesh_z, make_cone_mesh, nozzle_z_offset


class TestNozzleItem(unittest.TestCase):
    def test_make_cone_mesh_shapes(self):
        verts, faces = make_cone_mesh(10.0, 2.0, 8)
        self.assertEqual(verts.shape, (9, 3))
        self.assertEqual(faces.shape, (8, 3))
        np.testing.assert_allclose(verts[0], np.array([0.0, 0.0, 10.0]))
        self.assertTrue(np.allclose(verts[1:, 2], 0.0))

    def test_flip_mesh_z(self):
        verts = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 1.0]], dtype=float)
        faces = np.array([[0, 1, 2]], dtype=int)
        new_verts, new_faces = flip_mesh_z(verts, faces)
        np.testing.assert_allclose(
            new_verts,
            np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, -1.0]]),
        )
        self.assertTrue(np.array_equal(new_faces, np.array([[0, 2, 1]], dtype=int)))

    def test_nozzle_z_offset_flipped(self):
        self.assertAlmostEqual(nozzle_z_offset(18.0, 2.0, 0.0, False), -16.0)
        self.assertAlmostEqual(nozzle_z_offset(18.0, 2.0, 0.0, True), 20.0)


if __name__ == "__main__":
    unittest.main()
