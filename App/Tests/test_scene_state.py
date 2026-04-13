from __future__ import annotations

import unittest

import numpy as np

from gui.scene_state import SceneState


def _box_part(name: str, size: float = 10.0):
    half = float(size) * 0.5
    vertices = np.array(
        [
            [-half, -half, -half],
            [half, -half, -half],
            [half, half, -half],
            [-half, half, -half],
            [-half, -half, half],
            [half, -half, half],
            [half, half, half],
            [-half, half, half],
        ],
        dtype=float,
    )
    faces = np.array(
        [
            [0, 1, 2],
            [0, 2, 3],
            [4, 5, 6],
            [4, 6, 7],
            [0, 1, 5],
            [0, 5, 4],
            [1, 2, 6],
            [1, 6, 5],
            [2, 3, 7],
            [2, 7, 6],
            [3, 0, 4],
            [3, 4, 7],
        ],
        dtype=int,
    )
    return {"name": name, "vertices": vertices, "faces": faces, "source_path": ""}


class SceneStateTests(unittest.TestCase):
    def test_default_plate_and_round_trip(self):
        scene = SceneState()
        self.assertEqual(scene.get_plate_ids(), [1])
        first = scene.add_imported_object("Sample", "sample.stl", [_box_part("Part 1"), _box_part("Part 2", 6.0)])
        second_plate = scene.create_plate("02")
        clone = scene.create_instance(first.object_id, plate_id=second_plate.id, offset=(20.0, 0.0, 0.0))

        payload = scene.to_dict()
        restored = SceneState.from_dict(payload)

        self.assertEqual(restored.get_plate_ids(), [1, 2])
        self.assertEqual(len(restored.objects), 1)
        self.assertEqual(len(restored.parts), 2)
        self.assertEqual(len(restored.instances), 2)
        self.assertEqual(restored.instances[int(clone.id)].plate_id, 2)

    def test_delete_plate_prunes_instances_and_orphans(self):
        scene = SceneState()
        first = scene.add_imported_object("Sample", "sample.stl", [_box_part("Part 1")])
        second_plate = scene.create_plate("02")
        second = scene.create_instance(first.object_id, plate_id=second_plate.id, offset=(15.0, 0.0, 0.0))

        self.assertTrue(scene.delete_plate(second_plate.id))
        self.assertNotIn(int(second.id), scene.instances)
        self.assertIn(int(first.id), scene.instances)
        self.assertEqual(scene.get_plate_ids(), [1])


if __name__ == "__main__":
    unittest.main()
