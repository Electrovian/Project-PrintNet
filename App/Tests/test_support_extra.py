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

from slicer import geometry
from slicer import support
from slicer.gcode import SliceSettings
from slicer.mesh import MeshModel
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

    def test_generate_support_interfaces(self):
        outer = square_points(4.0)
        islands = geometry.polygons_with_holes([outer])
        settings = SliceSettings(
            interface_layers=1,
            interface_density=0.5,
            infill_angle=0.0,
            extrusion_width=0.4,
            layer_height=0.2,
        )
        layers = support.generate_support_interfaces(islands, [0.2, 0.4, 0.6], settings, top_z=0.6)
        self.assertGreaterEqual(len(layers), 1)


if __name__ == "__main__":
    unittest.main()
