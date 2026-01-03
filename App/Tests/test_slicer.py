import math
import os
import sys
import unittest

import trimesh

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer.mesh import MeshModel
from slicer.gcode import SliceSettings
from slicer.slicer import build_z_heights, generate_layer_perimeters, generate_layer_plans

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

class LayerPerimeterTests(unittest.TestCase):
    def test_generate_layer_perimeters_box(self):
        mesh = trimesh.creation.box(extents=(1.0, 1.0, 1.0))
        model = MeshModel(path="<memory>", mesh=mesh)
        settings = SliceSettings(perimeter_count=1, extrusion_width=0.2)
        layers = generate_layer_perimeters(model, [0.0], settings=settings)
        self.assertEqual(len(layers), 1)
        layer = layers[0]
        self.assertEqual(layer.z, 0.0)
        self.assertEqual(len(layer.shells), 1)
        shell = layer.shells[0]
        self.assertEqual(shell.index, 0)
        self.assertEqual(len(shell.islands), 1)
        island = shell.islands[0]
        self.assertEqual(len(island.holes), 0)
        self.assertTrue(is_closed(island.outer))
        self.assertLess(polygon_area(island.outer), 0.0)

    def test_generate_layer_perimeters_multi_shell(self):
        mesh = trimesh.creation.box(extents=(2.0, 2.0, 1.0))
        model = MeshModel(path="<memory>", mesh=mesh)
        settings = SliceSettings(perimeter_count=3, extrusion_width=0.2)
        layers = generate_layer_perimeters(model, [0.0], settings=settings)
        self.assertEqual(len(layers), 1)
        layer = layers[0]
        self.assertEqual(len(layer.shells), 3)

    def test_generate_layer_plans_top_bottom(self):
        mesh = trimesh.creation.box(extents=(2.0, 2.0, 1.0))
        model = MeshModel(path="<memory>", mesh=mesh)
        settings = SliceSettings(infill_density=0.2,
                                 infill_angle=30.0,
                                 infill_pattern="rectilinear",
                                 extrusion_width=0.2,
                                 ironing_enabled=True,
                                 ironing_speed=15.0,
                                 ironing_flow=0.1,
                                 top_layers=1,
                                 bottom_layers=1)
        z_heights = [0.0, 0.2, 0.4]
        plan = generate_layer_plans(model, z_heights, settings=settings)
        self.assertEqual(len(plan.layers), 3)
        self.assertTrue(plan.layers[0].infill.is_solid)
        self.assertTrue(plan.layers[-1].infill.is_solid)
        self.assertFalse(plan.layers[1].infill.is_solid)
        self.assertEqual(plan.layers[0].infill.pattern, "rectilinear")
        self.assertEqual(plan.layers[-1].infill.pattern, "rectilinear")
        self.assertIsNotNone(plan.layers[-1].ironing)

    def test_brim_skirt_and_raft(self):
        mesh = trimesh.creation.box(extents=(1.0, 1.0, 1.0))
        model = MeshModel(path="<memory>", mesh=mesh)
        settings = SliceSettings(extrusion_width=0.2,
                                 brim_width=0.6,
                                 skirt_loops=2,
                                 skirt_distance=3.0,
                                 raft_layers=2,
                                 raft_margin=1.0)
        z_heights = [0.0, 0.2]
        plan = generate_layer_plans(model, z_heights, settings=settings)
        self.assertEqual(len(plan.raft_layers), 2)
        self.assertIsNotNone(plan.brim)
        self.assertIsNotNone(plan.skirt)
        self.assertGreater(len(plan.brim.loops), 0)
        self.assertGreater(len(plan.skirt.loops), 0)
        self.assertGreater(plan.layers[0].z, z_heights[0])

    def test_build_z_heights_manual_ranges(self):
        mesh = trimesh.creation.box(extents=(1.0, 1.0, 1.0))
        mesh.apply_translation((0.0, 0.0, 0.5))
        model = MeshModel(path="<memory>", mesh=mesh)
        settings = SliceSettings(layer_height=0.2,
                                 min_layer_height=0.1,
                                 max_layer_height=0.3,
                                 adaptive_overhang_enabled=False,
                                 layer_height_ranges=[(0.0, 0.4, 0.1)])
        heights = build_z_heights(model, settings)
        self.assertGreater(len(heights), 0)
        deltas = [heights[0]] + [heights[i] - heights[i - 1] for i in range(1, len(heights))]
        for delta in deltas[:4]:
            self.assertAlmostEqual(delta, 0.1, places=4)
        self.assertAlmostEqual(heights[-1], 1.0, places=4)

    def test_build_z_heights_adaptive_override(self):
        mesh = trimesh.creation.box(extents=(1.0, 1.0, 1.0))
        mesh.apply_translation((0.0, 0.0, 0.5))
        model = MeshModel(path="<memory>", mesh=mesh)
        settings = SliceSettings(layer_height=0.2,
                                 min_layer_height=0.1,
                                 max_layer_height=0.3,
                                 adaptive_overhang_enabled=True,
                                 adaptive_overhang_threshold=0.0,
                                 adaptive_overhang_height=0.1)
        heights = build_z_heights(model, settings)
        deltas = [heights[0]] + [heights[i] - heights[i - 1] for i in range(1, len(heights))]
        for delta in deltas:
            self.assertAlmostEqual(delta, 0.1, places=4)

if __name__ == "__main__":
    unittest.main()
