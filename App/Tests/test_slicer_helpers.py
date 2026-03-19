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

from slicer_v2 import legacy_slicer as slicer_module
from slicer_v2.legacy_gcode_writer import SliceSettings
from slicer_v2.legacy_mesh import MeshModel
from harness import BaseTestCase


class SlicerHelperTests(BaseTestCase):
    def test_normalize_height_ranges(self):
        ranges = [
            {"start": 0.0, "end": 1.0, "height": 0.1},
            {"z_min": 1.0, "z_max": 2.0, "layer_height": 0.2},
            (2.0, 3.0, 0.3),
            {"start": 3.0, "end": 3.0, "height": 0.1},
            ("bad", 4.0, 0.1),
        ]
        cleaned = slicer_module._normalize_height_ranges(ranges)
        self.assertEqual(len(cleaned), 3)
        self.assertEqual(cleaned[0], (0.0, 1.0, 0.1))

    def test_build_z_heights_empty_mesh(self):
        mesh = trimesh.creation.box(extents=(1.0, 1.0, 0.0))
        model = MeshModel(path="<memory>", mesh=mesh)
        settings = SliceSettings(layer_height=0.2)
        heights = slicer_module.build_z_heights(model, settings)
        self.assertEqual(heights, [])

    def test_wrap_islands(self):
        islands = [([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)], [])]
        wrapped = slicer_module._wrap_islands(islands)
        self.assertEqual(len(wrapped), 1)
        self.assertEqual(len(wrapped[0].holes), 0)


if __name__ == "__main__":
    unittest.main()

