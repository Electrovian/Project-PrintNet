import os
import sys
import unittest


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
TESTS = os.path.abspath(os.path.dirname(__file__))
if TESTS not in sys.path:
    sys.path.insert(0, TESTS)

from slicer_v2 import legacy_geometry as geometry
from slicer_v2 import legacy_support as support
from slicer_v2.legacy_gcode_writer import SliceSettings
from harness import BaseTestCase, square_points


@unittest.skipIf(geometry.pyclipper is None, "pyclipper not available")
class SupportExtraTests(BaseTestCase):
    def test_cluster_points(self):
        points = [(0.0, 0.0, 1.0), (0.1, 0.1, 2.0), (2.0, 2.0, 3.0)]
        clusters = support._cluster_points(points, radius=0.5)
        self.assertEqual(len(clusters), 2)

    def test_cluster_nodes(self):
        nodes = [
            support._TreeNode(x=0.0, y=0.0, z=1.0),
            support._TreeNode(x=0.2, y=0.0, z=1.5),
            support._TreeNode(x=2.0, y=2.0, z=2.0),
        ]
        clusters = support._cluster_nodes(nodes, radius=0.5)
        self.assertEqual(len(clusters), 2)

    def test_islands_union_and_intersection(self):
        outer_a = square_points(4.0)
        outer_b = [(x + 1.0, y) for x, y in outer_a]
        islands_a = geometry.polygons_with_holes([outer_a])
        islands_b = geometry.polygons_with_holes([outer_b])
        merged = geometry.islands_union(islands_a + islands_b)
        self.assertGreaterEqual(len(merged), 1)
        overlap = geometry.islands_intersection(islands_a, islands_b)
        self.assertGreaterEqual(len(overlap), 1)

    def test_generate_support_interfaces(self):
        outer = square_points(4.0)
        islands = geometry.polygons_with_holes([outer])
        settings = SliceSettings(
            support_enabled=True,
            interface_layers=1,
            interface_density=0.5,
            infill_angle=0.0,
            extrusion_width=0.4,
            layer_height=0.2,
        )
        z_heights = [0.2, 0.4]
        layer_islands = [[], islands]
        plan = support.generate_support_plan(None, z_heights, settings, layer_islands=layer_islands)
        self.assertGreaterEqual(len(plan.layers), 1)
        self.assertTrue(any(layer.interface_lines for layer in plan.layers))


if __name__ == "__main__":
    unittest.main()

