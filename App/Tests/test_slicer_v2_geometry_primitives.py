import math
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.errors import SlicerV2GeometryError  # noqa: E402
from slicer_v2.geometry import (  # noqa: E402
    AABB,
    Island,
    Point2,
    Polygon,
    bounds_for_polygons,
    island_from_tuples,
    polygon_from_tuples,
    polyline_length,
)


class TestSlicerV2GeometryPrimitives(unittest.TestCase):
    def test_point_distance_and_translate(self) -> None:
        a = Point2(0.0, 0.0)
        b = Point2(3.0, 4.0)
        c = a.translated(3.0, 4.0)
        self.assertAlmostEqual(a.distance_to(b), 5.0)
        self.assertEqual(c.as_tuple(), (3.0, 4.0))

    def test_polygon_area_perimeter_centroid_and_winding(self) -> None:
        poly = polygon_from_tuples([(0, 0), (10, 0), (10, 10), (0, 10)])
        self.assertAlmostEqual(poly.area, 100.0)
        self.assertAlmostEqual(poly.perimeter, 40.0)
        centroid = poly.centroid
        self.assertAlmostEqual(centroid.x, 5.0)
        self.assertAlmostEqual(centroid.y, 5.0)
        self.assertFalse(poly.is_clockwise)
        self.assertTrue(poly.with_winding(clockwise=True).is_clockwise)

    def test_polygon_contains_point_and_boundary(self) -> None:
        poly = polygon_from_tuples([(0, 0), (10, 0), (10, 10), (0, 10)])
        self.assertTrue(poly.contains_point(Point2(1.0, 1.0)))
        self.assertFalse(poly.contains_point(Point2(11.0, 11.0)))
        self.assertTrue(poly.contains_point(Point2(0.0, 5.0), include_boundary=True))
        self.assertFalse(poly.contains_point(Point2(0.0, 5.0), include_boundary=False))

    def test_island_contains_hole_exclusion(self) -> None:
        island = island_from_tuples(
            [(0, 0), (10, 0), (10, 10), (0, 10)],
            [[(2, 2), (8, 2), (8, 8), (2, 8)]],
        )
        self.assertTrue(island.contains_point(Point2(1.0, 1.0)))
        self.assertFalse(island.contains_point(Point2(5.0, 5.0)))
        self.assertAlmostEqual(island.area, 64.0)

    def test_aabb_intersection_union_and_padding(self) -> None:
        a = AABB(0.0, 0.0, 10.0, 10.0)
        b = AABB(5.0, 5.0, 15.0, 15.0)
        c = AABB(20.0, 20.0, 25.0, 25.0)
        self.assertTrue(a.intersects(b))
        self.assertFalse(a.intersects(c))
        union = a.union(b)
        self.assertEqual((union.min_x, union.min_y, union.max_x, union.max_y), (0.0, 0.0, 15.0, 15.0))
        padded = a.padded(2.0)
        self.assertEqual((padded.min_x, padded.min_y, padded.max_x, padded.max_y), (-2.0, -2.0, 12.0, 12.0))

    def test_polyline_and_bounds(self) -> None:
        length = polyline_length([Point2(0, 0), Point2(3, 4), Point2(6, 8)])
        self.assertAlmostEqual(length, 10.0)
        a = polygon_from_tuples([(0, 0), (2, 0), (2, 2), (0, 2)])
        b = polygon_from_tuples([(5, 5), (8, 5), (8, 8), (5, 8)])
        bounds = bounds_for_polygons([a, b])
        self.assertEqual((bounds.min_x, bounds.min_y, bounds.max_x, bounds.max_y), (0.0, 0.0, 8.0, 8.0))

    def test_invalid_polygon_rejected(self) -> None:
        with self.assertRaises(SlicerV2GeometryError):
            Polygon((Point2(0, 0), Point2(0, 0), Point2(0, 0)))


if __name__ == "__main__":
    unittest.main()
