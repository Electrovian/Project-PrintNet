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

from slicer import geometry
from harness import BaseTestCase, square_points


@unittest.skipIf(geometry.pyclipper is None, "pyclipper not available")
class GeometryClipTests(BaseTestCase):
    def test_point_in_polygon(self):
        square = square_points(2.0)
        self.assertTrue(geometry.point_in_polygon((0.0, 0.0), square))
        self.assertFalse(geometry.point_in_polygon((2.0, 2.0), square))

    def test_point_in_island_with_hole(self):
        outer = square_points(4.0)
        hole = square_points(1.0)
        islands = geometry.polygons_with_holes([outer, hole])
        island = islands[0]
        self.assertTrue(geometry.point_in_island((1.5, 0.0), island))
        self.assertFalse(geometry.point_in_island((0.0, 0.0), island))

    def test_line_inside_island(self):
        outer = square_points(4.0)
        hole = square_points(1.0)
        island = (outer, [hole])
        inside = ((-1.5, 0.0), (-1.0, 0.2))
        crosses_hole = ((-2.0, 0.0), (2.0, 0.0))
        self.assertTrue(geometry.line_inside_island(inside, island))
        self.assertFalse(geometry.line_inside_island(crosses_hole, island))

    def test_clip_lines_to_polygon(self):
        square = square_points(2.0)
        lines = [((-3.0, 0.0), (3.0, 0.0))]
        clipped = geometry.clip_lines_to_polygon(lines, square)
        self.assertGreaterEqual(len(clipped), 1)
        xs = [p[0] for p in square[:-1]]
        ys = [p[1] for p in square[:-1]]
        minx, maxx = min(xs), max(xs)
        miny, maxy = min(ys), max(ys)
        for seg in clipped:
            for pt in seg:
                self.assertGreaterEqual(pt[0], minx - 1e-6)
                self.assertLessEqual(pt[0], maxx + 1e-6)
                self.assertGreaterEqual(pt[1], miny - 1e-6)
                self.assertLessEqual(pt[1], maxy + 1e-6)

    def test_offset_polygon_expands(self):
        square = square_points(2.0)
        area_before = abs(geometry._polygon_area(square[:-1]))
        offset = geometry.offset_polygon(square, distance=0.5)
        self.assertTrue(offset)
        area_after = abs(geometry._polygon_area(offset[0]))
        self.assertGreater(area_after, area_before)


if __name__ == "__main__":
    unittest.main()
