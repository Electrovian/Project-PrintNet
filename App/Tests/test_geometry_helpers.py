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
from harness import BaseTestCase, circle_points, square_points


class GeometryHelperTests(BaseTestCase):
    def test_points_close(self):
        self.assertTrue(geometry._points_close((0.0, 0.0), (1e-7, -1e-7)))
        self.assertFalse(geometry._points_close((0.0, 0.0), (1e-2, 0.0), tol=1e-3))

    def test_dedupe_points(self):
        points = [(0.0, 0.0), (0.0, 0.0), (1.0, 0.0), (1.0, 0.0), (0.0, 0.0)]
        cleaned = geometry._dedupe_points(points)
        self.assertEqual(cleaned[0], (0.0, 0.0))
        self.assertEqual(cleaned[-1], (1.0, 0.0))
        self.assertEqual(len(cleaned), 2)

    def test_normalize_polygon_strips_close(self):
        square = square_points(2.0)
        normalized = geometry._normalize_polygon(square)
        self.assertEqual(len(normalized), len(square) - 1)
        self.assertEqual(normalized[0], square[0])

    def test_close_polygon_appends(self):
        tri = [(0.0, 0.0), (1.0, 0.0), (0.5, 1.0)]
        closed = geometry._close_polygon(tri)
        self.assertEqual(closed[0], closed[-1])
        self.assertEqual(len(closed), len(tri) + 1)

    def test_polygon_area_and_clockwise(self):
        square = square_points(2.0)
        area = geometry._polygon_area(square[:-1])
        self.assertAlmostEqual(area, 4.0, places=4)
        self.assertFalse(geometry._is_clockwise(square[:-1]))
        self.assertTrue(geometry._is_clockwise(list(reversed(square[:-1]))))

    def test_polygon_perimeter(self):
        square = square_points(2.0)
        perimeter = geometry._polygon_perimeter(square[:-1])
        self.assertAlmostEqual(perimeter, 8.0, places=4)

    def test_polygon_centroid(self):
        square = square_points(2.0)
        centroid = geometry._polygon_centroid(square)
        self.assertPointClose(centroid, (0.0, 0.0))

    def test_is_circular_polygon(self):
        circle = circle_points(1.0, 24)
        circle.append(circle[0])
        self.assertTrue(geometry._is_circular_polygon(circle, circularity_threshold=0.7, radius_variation=0.1))
        square = square_points(2.0)
        self.assertFalse(geometry._is_circular_polygon(square, circularity_threshold=0.9, radius_variation=0.05))

    def test_compute_bounding_square(self):
        bounds = ((-2.0, -1.0, 0.0), (3.0, 4.0, 5.0))
        square = geometry.compute_bounding_square(bounds)
        self.assertEqual(square[0], (-2.0, -1.0))
        self.assertEqual(square[2], (3.0, 4.0))
        self.assertEqual(square[0], square[-1])


if __name__ == "__main__":
    unittest.main()
