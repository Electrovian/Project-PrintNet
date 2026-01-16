import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
TESTS = os.path.abspath(os.path.dirname(__file__))
if TESTS not in sys.path:
    sys.path.insert(0, TESTS)

from slicer import geometry
from slicer import infill
from harness import BaseTestCase, square_points


@unittest.skipIf(geometry.pyclipper is None, "pyclipper not available")
class InfillExtraTests(BaseTestCase):
    def test_line_spacing(self):
        self.assertEqual(infill._line_spacing(0.0, 0.4, 1), 0.0)
        self.assertAlmostEqual(infill._line_spacing(1.0, 0.4, 2), 0.8, places=4)

    def test_generate_infill_default_pattern(self):
        outer = square_points(2.0)
        islands = geometry.polygons_with_holes([outer])
        segments = infill.generate_infill(
            islands,
            density=0.5,
            angle_deg=0.0,
            layer_index=0,
            extrusion_width=0.4,
            pattern="unknown",
        )
        self.assertGreaterEqual(len(segments), 1)

    def test_grid_infill_alternate(self):
        outer = square_points(2.0)
        islands = geometry.polygons_with_holes([outer])
        seg_a = infill.grid_infill(islands, density=0.5, angle_deg=0.0, layer_index=0, extrusion_width=0.4)
        seg_b = infill.grid_infill(islands, density=0.5, angle_deg=0.0, layer_index=1, extrusion_width=0.4)
        self.assertNotEqual(len(seg_a), 0)
        self.assertNotEqual(len(seg_b), 0)


if __name__ == "__main__":
    unittest.main()
