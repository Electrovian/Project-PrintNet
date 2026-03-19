import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.geometry import polygon_from_tuples  # noqa: E402
from slicer_v2.island_graph import build_layer_island_graph, build_vertical_adjacency  # noqa: E402
from slicer_v2.settings import normalize_settings  # noqa: E402
from slicer_v2.support_planning import SUPPORT_TYPE_TREE, build_support_plan  # noqa: E402
from slicer_v2.supports import run as run_supports_stage  # noqa: E402
from slicer_v2.types import SlicerContext  # noqa: E402


def _square(x0: float, y0: float, size: float):
    return polygon_from_tuples(
        [
            (x0, y0),
            (x0 + size, y0),
            (x0 + size, y0 + size),
            (x0, y0 + size),
        ]
    )


class TestSlicerV2TreeSupportParity(unittest.TestCase):
    def test_tree_report_contains_weighted_parent_metadata(self) -> None:
        layer0 = build_layer_island_graph([_square(-30.0, -30.0, 4.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(0.0, 0.0, 6.0)], layer_index=1, z_height_mm=0.4)
        layer2 = build_layer_island_graph([_square(8.0, 0.0, 6.0)], layer_index=2, z_height_mm=0.6)
        graphs = [layer0, layer1, layer2]
        edges = build_vertical_adjacency(graphs)
        _layer_plans, report = build_support_plan(
            graphs,
            vertical_edges=edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_TREE,
            support_density_percent=25.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.2,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
            tree_parent_weight_route=0.56,
            tree_parent_weight_load=0.40,
            tree_parent_root_bonus=0.06,
            tree_trunk_root_bonus=0.08,
            tree_trunk_depth_bonus=0.07,
            tree_support_strict_parity_mode=True,
        )
        self.assertGreaterEqual(report.tree_branch_load_score_avg, 0.0)
        self.assertGreaterEqual(report.tree_branch_selection_score_avg, 0.0)
        self.assertGreaterEqual(report.tree_branch_reroute_cost_mm_total, 0.0)
        self.assertIn("support_planning:tree_strict_parity_mode", report.warnings)
        self.assertTrue(report.tree_branches)
        self.assertTrue(
            all(
                branch.trunk_assignment in {"root", "trunk", "child", "merged", "pruned"}
                for branch in report.tree_branches
            )
        )

    def test_supports_stage_exposes_weighted_tree_artifacts(self) -> None:
        layer0 = build_layer_island_graph([_square(-30.0, -30.0, 4.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(0.0, 0.0, 6.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        edges = build_vertical_adjacency(graphs)
        context = SlicerContext(
            job_id="tree-parity-stage",
            mesh_path="tree-parity.stl",
            resolved_settings=normalize_settings(
                {
                    "support_enabled": True,
                    "support_type": "tree",
                    "support_density_percent": 20.0,
                    "support_spacing_mm": 2.2,
                    "support_xy_gap_mm": 0.2,
                    "support_z_gap_mm": 0.2,
                    "support_interface_layers": 2,
                    "tree_support_parent_weight_route": 0.56,
                    "tree_support_parent_weight_load": 0.40,
                    "tree_support_parent_root_bonus": 0.06,
                    "tree_support_trunk_root_bonus": 0.08,
                    "tree_support_trunk_depth_bonus": 0.07,
                    "tree_support_strict_parity_mode": True,
                }
            ),
        )
        context.stage_artifacts["regions"] = {"region_count": 2}
        context.stage_artifacts["islands"] = {"layer_graphs": graphs, "vertical_edges": edges}
        artifact = run_supports_stage(context)
        self.assertIn("tree_support_parent_weight_route", artifact)
        self.assertIn("tree_support_parent_weight_load", artifact)
        self.assertIn("tree_support_parent_root_bonus", artifact)
        self.assertIn("tree_support_trunk_root_bonus", artifact)
        self.assertIn("tree_support_trunk_depth_bonus", artifact)
        self.assertIn("tree_support_strict_parity_mode", artifact)
        self.assertIn("tree_branch_load_score_avg", artifact)
        self.assertIn("tree_branch_selection_score_avg", artifact)
        self.assertIn("tree_branch_reroute_cost_mm_total", artifact)
        self.assertIn("tree_branch_trunk_assignment_counts", artifact)


if __name__ == "__main__":
    unittest.main()
