import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.errors import SlicerV2PolygonPipelineError  # noqa: E402
from slicer_v2.geometry import Polygon, polygon_from_tuples  # noqa: E402
from slicer_v2.polygon_pipeline import (  # noqa: E402
    cleanup_and_offset_polygons,
    cleanup_polygon,
    offset_polygon,
)


class TestSlicerV2PolygonOffsetCleanup(unittest.TestCase):
    def test_cleanup_removes_collinear_vertices(self) -> None:
        poly = polygon_from_tuples([(0, 0), (5, 0), (10, 0), (10, 10), (0, 10)])
        cleaned = cleanup_polygon(poly)
        self.assertIsNotNone(cleaned)
        assert cleaned is not None
        self.assertEqual(len(cleaned.points), 4)
        self.assertAlmostEqual(cleaned.area, 100.0)

    def test_cleanup_drops_tiny_polygon(self) -> None:
        poly = polygon_from_tuples([(0, 0), (0.001, 0), (0.001, 0.001), (0, 0.001)])
        cleaned = cleanup_polygon(poly, min_area=0.01)
        self.assertIsNone(cleaned)

    def test_offset_rectangle_outward_increases_area(self) -> None:
        poly = polygon_from_tuples([(0, 0), (10, 0), (10, 10), (0, 10)])
        out = offset_polygon(poly, 1.0)
        self.assertIsNotNone(out)
        assert out is not None
        self.assertGreater(out.area, poly.area)

    def test_offset_rectangle_inward_decreases_area(self) -> None:
        poly = polygon_from_tuples([(0, 0), (10, 0), (10, 10), (0, 10)])
        inside = offset_polygon(poly, -1.0)
        self.assertIsNotNone(inside)
        assert inside is not None
        self.assertLess(inside.area, poly.area)

    def test_offset_can_drop_polygon_when_too_large_inward(self) -> None:
        poly = polygon_from_tuples([(0, 0), (4, 0), (4, 4), (0, 4)])
        inside = offset_polygon(poly, -5.0)
        self.assertIsNone(inside)

    def test_cleanup_offset_report_counts(self) -> None:
        p1 = polygon_from_tuples([(0, 0), (10, 0), (10, 10), (0, 10)])
        p2 = polygon_from_tuples([(0, 0), (0.001, 0), (0.001, 0.001), (0, 0.001)])
        result, report = cleanup_and_offset_polygons([p1, p2], offset_distance=0.5, min_area=0.01)
        self.assertEqual(report.input_count, 2)
        self.assertEqual(report.cleaned_count, 1)
        self.assertEqual(report.output_count, 1)
        self.assertEqual(len(result), 1)

    def test_strict_mode_fails_on_warnings(self) -> None:
        p1 = polygon_from_tuples([(0, 0), (1, 0), (1, 1), (0, 1)])
        p2 = polygon_from_tuples([(0, 0), (0.001, 0), (0.001, 0.001), (0, 0.001)])
        with self.assertRaises(SlicerV2PolygonPipelineError):
            cleanup_and_offset_polygons([p1, p2], offset_distance=0.25, min_area=0.01, strict=True)


if __name__ == "__main__":
    unittest.main()
