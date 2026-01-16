import unittest

import numpy as np

from gui.auto_orient import (
    face_normals_and_areas,
    orientation_metrics,
    pick_best_orientation,
    rotation_from_to,
    select_candidate_normals,
)


class TestAutoOrient(unittest.TestCase):
    def _box_mesh(self, size_x: float, size_y: float, size_z: float):
        hx, hy, hz = size_x / 2.0, size_y / 2.0, size_z / 2.0
        verts = np.array(
            [
                [-hx, -hy, -hz],
                [hx, -hy, -hz],
                [hx, hy, -hz],
                [-hx, hy, -hz],
                [-hx, -hy, hz],
                [hx, -hy, hz],
                [hx, hy, hz],
                [-hx, hy, hz],
            ],
            dtype=float,
        )
        faces = np.array(
            [
                [0, 1, 2],
                [0, 2, 3],
                [4, 6, 5],
                [4, 7, 6],
                [0, 4, 5],
                [0, 5, 1],
                [1, 5, 6],
                [1, 6, 2],
                [2, 6, 7],
                [2, 7, 3],
                [3, 7, 4],
                [3, 4, 0],
            ],
            dtype=int,
        )
        return verts, faces

    def test_orientation_metrics_bed_face(self):
        verts = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], dtype=float)
        faces = np.array([[0, 2, 1]], dtype=int)
        normals, areas = face_normals_and_areas(verts, faces)
        support, height = orientation_metrics(
            verts,
            faces,
            normals,
            areas,
            np.eye(3, dtype=float),
            overhang_angle=45.0,
        )
        self.assertEqual(support, 0.0)
        self.assertEqual(height, 0.0)

    def test_pick_best_orientation_min_time(self):
        verts, faces = self._box_mesh(10.0, 20.0, 30.0)
        normals, areas = face_normals_and_areas(verts, faces)
        candidates = select_candidate_normals(normals, areas, max_candidates=6)
        self.assertGreater(len(candidates), 0)
        metrics = []
        for n in candidates:
            rot = rotation_from_to(n, np.array([0.0, 0.0, -1.0], dtype=float))
            support, height = orientation_metrics(
                verts,
                faces,
                normals,
                areas,
                rot,
                overhang_angle=45.0,
            )
            metrics.append({"support": support, "height": height})
        best_idx = pick_best_orientation(metrics, "min_time")
        self.assertIsNotNone(best_idx)
        assert best_idx is not None
        self.assertAlmostEqual(metrics[best_idx]["height"], 10.0, places=5)


if __name__ == "__main__":
    unittest.main()
