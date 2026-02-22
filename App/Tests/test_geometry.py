import math
import os
import sys
import unittest

import numpy as np
import trimesh

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2 import legacy_geometry as geometry

def polygon_area(points):
    if len(points) < 3:
        return 0.0
    area = 0.0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        area += x1 * y2 - x2 * y1
    return 0.5 * area

def is_closed(points, tol=1e-8):
    if len(points) < 3:
        return False
    return (math.isclose(points[0][0], points[-1][0], abs_tol=tol)
            and math.isclose(points[0][1], points[-1][1], abs_tol=tol))

class GeometryValidationTests(unittest.TestCase):
    def test_ensure_winding(self):
        square = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
        cw = geometry.ensure_winding(square, clockwise=True)
        ccw = geometry.ensure_winding(square, clockwise=False)
        self.assertTrue(is_closed(cw))
        self.assertTrue(is_closed(ccw))
        self.assertLess(polygon_area(cw), 0.0)
        self.assertGreater(polygon_area(ccw), 0.0)

    def test_clean_polygons_simplifies_short_edges(self):
        poly = [(0.0, 0.0), (1e-7, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
        cleaned = geometry.clean_polygons([poly], tolerance=1e-5)
        self.assertEqual(len(cleaned), 1)
        cleaned_poly = cleaned[0]
        self.assertTrue(is_closed(cleaned_poly))
        for i in range(len(cleaned_poly) - 1):
            dx = cleaned_poly[i + 1][0] - cleaned_poly[i][0]
            dy = cleaned_poly[i + 1][1] - cleaned_poly[i][1]
            self.assertGreater(math.hypot(dx, dy), 1e-6)

    def test_clean_polygons_simplify_self_intersection(self):
        bowtie = [(0.0, 0.0), (1.0, 1.0), (0.0, 1.0), (1.0, 0.0)]
        cleaned = geometry.clean_polygons([bowtie], tolerance=1e-5)
        self.assertGreaterEqual(len(cleaned), 1)
        for poly in cleaned:
            self.assertTrue(is_closed(poly))
            self.assertNotEqual(polygon_area(poly), 0.0)

    def test_offset_islands_inset(self):
        square = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0), (0.0, 0.0)]
        islands = geometry.polygons_with_holes([square])
        inset = geometry.offset_islands(islands, distance=-0.2)
        self.assertEqual(len(inset), 1)
        outer, holes = inset[0]
        self.assertEqual(len(holes), 0)
        self.assertTrue(is_closed(outer))
        self.assertLess(abs(polygon_area(outer)), abs(polygon_area(square)))

    def test_lowest_planar_face(self):
        mesh = trimesh.creation.box(extents=(1.0, 2.0, 3.0))
        result = geometry.lowest_planar_face(mesh.vertices, mesh.faces)
        self.assertIsNotNone(result)
        assert result is not None
        normal, _ = result
        normal = np.array(normal, dtype=float)
        self.assertAlmostEqual(abs(normal[2]), 1.0, places=4)

    def test_arrange_rectangles_centered(self):
        sizes = [(1, 10.0, 5.0), (2, 8.0, 6.0), (3, 4.0, 4.0)]
        positions = geometry.arrange_rectangles(sizes, spacing=2.0)
        self.assertEqual(len(positions), 3)
        xs = [positions[mid][0] for mid, _w, _d in sizes]
        ys = [positions[mid][1] for mid, _w, _d in sizes]
        self.assertAlmostEqual(sum(xs) / len(xs), 0.0, places=3)
        self.assertAlmostEqual(sum(ys) / len(ys), 0.0, places=3)

    def test_slice_mesh_preserves_translation(self):
        mesh = trimesh.creation.box(extents=(2.0, 4.0, 2.0))
        translation = np.array([10.0, -5.0, 0.0], dtype=float)
        mesh.apply_translation(translation)
        loops = geometry.slice_mesh(mesh, z_height=0.0)
        self.assertGreater(len(loops), 0)
        xs = []
        ys = []
        for loop in loops:
            for x, y in loop[:-1]:
                xs.append(x)
                ys.append(y)
        self.assertGreater(len(xs), 0)
        self.assertGreater(len(ys), 0)
        center_x = (min(xs) + max(xs)) / 2.0
        center_y = (min(ys) + max(ys)) / 2.0
        self.assertAlmostEqual(center_x, translation[0], places=3)
        self.assertAlmostEqual(center_y, translation[1], places=3)

    def test_thin_wall_lines(self):
        thin_rect = [(0.0, 0.0), (0.3, 0.0), (0.3, 5.0), (0.0, 5.0), (0.0, 0.0)]
        islands = geometry.polygons_with_holes([thin_rect])
        lines = geometry.thin_wall_lines(islands, extrusion_width=0.4)
        self.assertGreater(len(lines), 0)

    def test_gap_fill_lines(self):
        rect = [(0.0, 0.0), (5.0, 0.0), (5.0, 2.0), (0.0, 2.0), (0.0, 0.0)]
        islands = geometry.polygons_with_holes([rect])
        lines = geometry.gap_fill_lines(islands, extrusion_width=0.4, perimeter_spacing=0.2)
        self.assertGreater(len(lines), 0)

    def test_compensate_holes_expands_circle(self):
        outer = [(-2.0, -2.0), (2.0, -2.0), (2.0, 2.0), (-2.0, 2.0), (-2.0, -2.0)]
        circle = []
        for step in range(16):
            angle = (2.0 * math.pi * step) / 16.0
            circle.append((math.cos(angle), math.sin(angle)))
        circle.append(circle[0])
        islands = geometry.polygons_with_holes([outer, circle])
        self.assertEqual(len(islands), 1)
        _, holes = islands[0]
        self.assertEqual(len(holes), 1)
        original_area = abs(polygon_area(holes[0]))
        compensated = geometry.compensate_holes(islands, compensation_mm=0.2)
        _, new_holes = compensated[0]
        self.assertEqual(len(new_holes), 1)
        new_area = abs(polygon_area(new_holes[0]))
        self.assertGreater(new_area, original_area)

    def test_compensate_holes_skips_non_circular(self):
        outer = [(-2.0, -2.0), (2.0, -2.0), (2.0, 2.0), (-2.0, 2.0), (-2.0, -2.0)]
        rect_hole = [(-0.6, -0.3), (0.6, -0.3), (0.6, 0.3), (-0.6, 0.3), (-0.6, -0.3)]
        islands = geometry.polygons_with_holes([outer, rect_hole])
        original_area = abs(polygon_area(islands[0][1][0]))
        compensated = geometry.compensate_holes(islands, compensation_mm=0.2)
        new_area = abs(polygon_area(compensated[0][1][0]))
        self.assertAlmostEqual(new_area, original_area, places=4)

if __name__ == "__main__":
    unittest.main()

