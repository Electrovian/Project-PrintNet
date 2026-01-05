import os
import sys
import unittest
import math

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
TESTS = os.path.abspath(os.path.dirname(__file__))
if TESTS not in sys.path:
    sys.path.insert(0, TESTS)

from slicer import path_planner
from harness import BaseTestCase, circle_points


class PathPlannerExtraTests(BaseTestCase):
    def test_circle_from_points_colinear(self):
        p1 = (0.0, 0.0)
        p2 = (1.0, 0.0)
        p3 = (2.0, 0.0)
        self.assertIsNone(path_planner._circle_from_points(p1, p2, p3))

    def test_circle_from_points_valid(self):
        p1 = (1.0, 0.0)
        p2 = (0.0, 1.0)
        p3 = (-1.0, 0.0)
        circle = path_planner._circle_from_points(p1, p2, p3)
        self.assertIsNotNone(circle)
        center, radius = circle
        self.assertPointClose(center, (0.0, 0.0))
        self.assertAlmostEqual(radius, 1.0, places=4)

    def test_fit_arc_full_circle(self):
        pts = circle_points(5.0, 16)
        pts.append(pts[0])
        fit = path_planner.fit_arc(pts, tolerance=0.05, require_closed=True)
        self.assertIsNotNone(fit)
        self.assertTrue(fit.is_full_circle)
        self.assertAlmostEqual(fit.radius, 5.0, places=2)
        self.assertTrue(math.isfinite(fit.angle))

    def test_apply_seam_placement_random(self):
        loop = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]
        out = path_planner.apply_seam_placement(loop, mode="random")
        self.assertEqual(out[0], out[-1])
        self.assertEqual(len(out), len(loop))

    def test_apply_seam_placement_rear(self):
        loop = [(0.0, 0.0), (2.0, 0.0), (2.0, 1.0), (0.0, 1.0), (0.0, 0.0)]
        out = path_planner.apply_seam_placement(loop, mode="rear", rear_angle=180.0)
        self.assertEqual(out[0], out[-1])
        self.assertEqual(len(out), len(loop))


if __name__ == "__main__":
    unittest.main()
