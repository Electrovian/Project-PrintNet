import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer import path_planner
from slicer.geometry import polygons_with_holes

class BridgeDetectionTests(unittest.TestCase):
    def test_detect_bridge_islands(self):
        current = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0), (0.0, 0.0)]
        below = [(2.0, 2.0), (8.0, 2.0), (8.0, 8.0), (2.0, 8.0), (2.0, 2.0)]
        current_islands = polygons_with_holes([current])
        below_islands = polygons_with_holes([below])
        bridges = path_planner.detect_bridge_islands(current_islands, below_islands)
        self.assertEqual(len(bridges), 1)
        outer, holes = bridges[0]
        self.assertGreater(len(outer), 3)
        self.assertEqual(len(holes), 1)

    def test_bridge_direction(self):
        square = [(0.0, 0.0), (5.0, 0.0), (5.0, 5.0), (0.0, 5.0), (0.0, 0.0)]
        island = polygons_with_holes([square])[0]
        angle = path_planner.bridge_direction(island)
        self.assertGreaterEqual(angle, 0.0)
        self.assertLess(angle, 180.0)

if __name__ == "__main__":
    unittest.main()
