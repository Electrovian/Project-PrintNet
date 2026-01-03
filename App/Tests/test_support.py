import math
import os
import sys
import unittest

import trimesh

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer.gcode import SliceSettings
from slicer.mesh import MeshModel
from slicer import support

class SupportTests(unittest.TestCase):
    def test_support_plan_has_columns(self):
        mesh = trimesh.creation.box(extents=(1.0, 1.0, 0.2))
        mesh.apply_translation((0.0, 0.0, 1.0))
        model = MeshModel(path="<memory>", mesh=mesh)
        settings = SliceSettings(overhang_angle=45.0,
                                 support_spacing=0.5,
                                 support_z_gap=0.2,
                                 support_xy_gap=0.1,
                                 support_style="pillars",
                                 interface_layers=2,
                                 interface_density=0.9)
        z_heights = [0.2, 0.4, 0.6, 0.8, 1.0]
        plan = support.generate_support_plan(model, z_heights, settings)
        self.assertGreaterEqual(len(plan.columns), 1)
        self.assertGreaterEqual(len(plan.interface_layers), 1)
        self.assertEqual(len(plan.tree_branches), 0)

    def test_tree_support_branches_respect_angle(self):
        mesh = trimesh.creation.box(extents=(1.0, 1.0, 0.2))
        mesh.apply_translation((0.0, 0.0, 1.0))
        model = MeshModel(path="<memory>", mesh=mesh)
        settings = SliceSettings(overhang_angle=45.0,
                                 support_spacing=0.5,
                                 support_z_gap=0.2,
                                 support_xy_gap=0.1,
                                 support_style="tree",
                                 tree_branch_angle=30.0,
                                 tree_merge_distance=0.5)
        branches = support.generate_tree_supports(model, settings)
        max_dx = math.tan(math.radians(settings.tree_branch_angle)) * settings.layer_height + 1e-6
        for branch in branches:
            points = branch.points
            for i in range(1, len(points)):
                dx = points[i][0] - points[i - 1][0]
                dy = points[i][1] - points[i - 1][1]
                dz = points[i][2] - points[i - 1][2]
                if dz <= 0.0:
                    continue
                self.assertLessEqual(math.hypot(dx, dy), max_dx)

if __name__ == "__main__":
    unittest.main()
