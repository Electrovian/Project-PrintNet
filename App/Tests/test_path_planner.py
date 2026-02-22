import os
import random
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2 import legacy_path_planner as path_planner
from slicer_v2.legacy_geometry import polygons_with_holes, point_in_island

class PathPlannerTests(unittest.TestCase):
    def test_order_islands_nearest(self):
        first = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]
        second = [(10.0, 0.0), (11.0, 0.0), (11.0, 1.0), (10.0, 1.0), (10.0, 0.0)]
        islands = polygons_with_holes([second, first])
        ordered = path_planner.order_islands_nearest(islands, start=(0.0, 0.0))
        outer_first, _ = ordered[0]
        points = outer_first[:-1] if len(outer_first) > 1 else outer_first
        cx = sum(p[0] for p in points) / len(points)
        self.assertLess(cx, 5.0)

    def test_order_toolpaths_perimeters_first(self):
        tp_perimeter = path_planner.Toolpath(
            kind="perimeter",
            points=[(0.0, 0.0, 0.2), (1.0, 0.0, 0.2)],
            speed=30.0,
            extrusion_multiplier=1.0,
        )
        tp_infill = path_planner.Toolpath(
            kind="infill",
            points=[(5.0, 0.0, 0.2), (6.0, 0.0, 0.2)],
            speed=50.0,
            extrusion_multiplier=1.0,
        )
        ordered = path_planner.order_toolpaths([tp_infill, tp_perimeter], start=(0.0, 0.0, 0.2))
        self.assertEqual(ordered[0].kind, "perimeter")

    def test_apply_seam_placement_aligned(self):
        loop = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0), (0.0, 0.0)]
        aligned = path_planner.apply_seam_placement(loop, mode="aligned", anchor=(2.0, 0.0))
        self.assertEqual(aligned[0], (2.0, 0.0))

    def test_apply_seam_placement_random(self):
        loop = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0), (0.0, 0.0)]
        rng = random.Random(42)
        randomized = path_planner.apply_seam_placement(loop, mode="random", rng=rng)
        self.assertNotEqual(randomized[0], loop[0])

    def test_combing_path_inside_island(self):
        square = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0), (0.0, 0.0)]
        island = polygons_with_holes([square])[0]
        path = path_planner.comb_travel((1.0, 1.0), (9.0, 9.0), island)
        for point in path:
            self.assertTrue(point_in_island(point, island))

    def test_plan_travel_z_hop(self):
        start = (0.0, 0.0, 0.2)
        end = (10.0, 0.0, 0.2)
        points = path_planner.plan_travel(start, end, retracted=True, z_hop_height=0.4)
        self.assertGreaterEqual(len(points), 4)
        self.assertAlmostEqual(points[1][2], 0.6)

    def test_plan_travel_no_hop_inside_island(self):
        square = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0), (0.0, 0.0)]
        island = polygons_with_holes([square])[0]
        start = (1.0, 1.0, 0.2)
        end = (9.0, 9.0, 0.2)
        points = path_planner.plan_travel(start,
                                          end,
                                          retracted=True,
                                          z_hop_height=0.4,
                                          comb_island=island,
                                          z_hop_only_outside=True)
        self.assertTrue(all(abs(p[2] - 0.2) < 1e-6 for p in points))

if __name__ == "__main__":
    unittest.main()

