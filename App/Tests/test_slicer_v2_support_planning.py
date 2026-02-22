import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.errors import SlicerV2SupportPlanningError  # noqa: E402
from slicer_v2.geometry import Point2, polygon_from_tuples  # noqa: E402
from slicer_v2.island_graph import build_layer_island_graph, build_vertical_adjacency  # noqa: E402
from slicer_v2.settings import normalize_settings  # noqa: E402
from slicer_v2.support_planning import (  # noqa: E402
    SUPPORT_TYPE_NORMAL,
    SUPPORT_TYPE_TREE,
    TreeSupportBranchPlan,
    _parent_candidate_score,
    _route_branch_connection,
    _trunk_candidate_score,
    build_support_plan,
)
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


class TestSlicerV2SupportPlanning(unittest.TestCase):
    def test_weighted_parent_score_balances_load_and_reroute_cost(self) -> None:
        high_load = TreeSupportBranchPlan(
            branch_id=1,
            parent_branch_id=None,
            root_layer_index=5,
            tip_layer_index=3,
            x_mm=0.0,
            y_mm=0.0,
            radius_mm=0.8,
            length_mm=12.0,
            connected_region_count=6,
            waypoint_count=1,
            collision_avoidance_count=2,
            blocked_collision_count=0,
        )
        low_load = TreeSupportBranchPlan(
            branch_id=2,
            parent_branch_id=None,
            root_layer_index=5,
            tip_layer_index=4,
            x_mm=0.0,
            y_mm=0.0,
            radius_mm=0.3,
            length_mm=2.0,
            connected_region_count=1,
            waypoint_count=0,
            collision_avoidance_count=0,
            blocked_collision_count=0,
        )
        high_load_score = _parent_candidate_score(
            high_load,
            direct_distance_mm=3.0,
            routed_distance_mm=3.8,
            waypoint_count=1,
            collision_avoided=False,
            support_spacing_mm=2.0,
            min_branch_radius_mm=0.25,
        )
        low_load_score = _parent_candidate_score(
            low_load,
            direct_distance_mm=3.0,
            routed_distance_mm=3.2,
            waypoint_count=0,
            collision_avoided=False,
            support_spacing_mm=2.0,
            min_branch_radius_mm=0.25,
        )
        self.assertGreater(high_load_score, low_load_score)

    def test_weighted_trunk_score_prefers_loaded_root(self) -> None:
        loaded_root = TreeSupportBranchPlan(
            branch_id=1,
            parent_branch_id=None,
            root_layer_index=6,
            tip_layer_index=2,
            x_mm=0.0,
            y_mm=0.0,
            radius_mm=0.9,
            length_mm=14.0,
            connected_region_count=7,
            waypoint_count=1,
            collision_avoidance_count=2,
            blocked_collision_count=0,
        )
        light_child = TreeSupportBranchPlan(
            branch_id=2,
            parent_branch_id=1,
            root_layer_index=5,
            tip_layer_index=4,
            x_mm=1.0,
            y_mm=0.0,
            radius_mm=0.35,
            length_mm=3.0,
            connected_region_count=1,
            waypoint_count=2,
            collision_avoidance_count=0,
            blocked_collision_count=1,
        )
        self.assertGreater(
            _trunk_candidate_score(
                loaded_root,
                support_spacing_mm=2.0,
                min_branch_radius_mm=0.25,
            ),
            _trunk_candidate_score(
                light_child,
                support_spacing_mm=2.0,
                min_branch_radius_mm=0.25,
            ),
        )

    def test_tree_route_graph_handles_target_side_detour(self) -> None:
        obstacle = polygon_from_tuples(
            [
                (3.0, -3.0),
                (7.0, -3.0),
                (7.0, 3.0),
                (3.0, 3.0),
            ]
        )
        start = Point2(0.0, 0.0)
        target = Point2(10.0, 0.0)
        path, collision_avoided, blocked, path_length = _route_branch_connection(
            start=start,
            target=target,
            obstacles=[obstacle],
            base_step_mm=1.0,
        )
        self.assertFalse(blocked)
        self.assertTrue(collision_avoided)
        self.assertGreaterEqual(len(path), 4)
        self.assertGreater(path_length, start.distance_to(target))

    def test_support_disabled_no_paths(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        layer_plans, report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=False,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.5,
            support_xy_gap_mm=0.25,
            support_z_gap_mm=0.2,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        self.assertEqual(len(layer_plans), 2)
        self.assertEqual(report.support_region_count_total, 0)
        self.assertEqual(report.support_path_count_total, 0)

    def test_unsupported_island_generates_support(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        _layer_plans, report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.5,
            support_xy_gap_mm=0.25,
            support_z_gap_mm=0.2,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        self.assertEqual(report.unsupported_island_count_total, 1)
        self.assertGreater(report.support_region_count_total, 0)
        self.assertGreater(report.support_path_count_total, 0)
        self.assertGreater(report.support_path_length_mm_total, 0.0)

    def test_tree_mode_has_mvp_warning(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        _layer_plans, report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_TREE,
            support_density_percent=20.0,
            support_spacing_mm=2.5,
            support_xy_gap_mm=0.25,
            support_z_gap_mm=0.2,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        self.assertIn("support_planning:tree_mode_mvp_estimate", report.warnings)
        self.assertGreater(report.support_path_count_total, 0)
        self.assertGreaterEqual(report.tree_branch_count_total, 1)
        self.assertGreaterEqual(len(report.tree_branches), 1)
        self.assertGreaterEqual(report.tree_collision_avoid_count_total, 0)
        self.assertGreaterEqual(report.tree_pruned_branch_count_total, 0)
        self.assertGreaterEqual(report.tree_parent_assignment_count_total, 0)
        self.assertGreaterEqual(report.tree_trunk_count_total, 0)

    def test_supports_stage_integration(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        context = SlicerContext(
            job_id="support-stage",
            mesh_path="support.stl",
            resolved_settings=normalize_settings(
                {
                    "support_enable": "on",
                    "support_style": "normal",
                    "support_density": "25%",
                    "support_spacing": 2.0,
                    "support_xy_gap": 0.2,
                    "support_z_gap": 0.2,
                    "support_interface_layer_count": 2,
                    "extrusion_width": 0.4,
                }
            ),
        )
        context.stage_artifacts["regions"] = {"region_count": 2}
        context.stage_artifacts["islands"] = {"layer_graphs": graphs, "vertical_edges": vertical_edges}
        artifact = run_supports_stage(context)
        self.assertTrue(artifact["support_enabled"])
        self.assertEqual(artifact["support_type"], SUPPORT_TYPE_NORMAL)
        self.assertEqual(artifact["support_density_percent"], 25.0)
        self.assertGreaterEqual(artifact["support_region_count"], 1)
        self.assertGreaterEqual(artifact["support_path_count"], 1)
        self.assertGreaterEqual(artifact["support_path_length_mm_total"], 0.0)
        self.assertIn("tree_branch_count_total", artifact)
        self.assertIn("layer_tree_branch_counts", artifact)
        self.assertIn("tree_collision_avoid_count_total", artifact)
        self.assertIn("tree_pruned_branch_count_total", artifact)
        self.assertIn("tree_parent_assignment_count_total", artifact)
        self.assertIn("tree_trunk_count_total", artifact)
        self.assertIn("layer_tree_collision_avoid_counts", artifact)
        self.assertIn("layer_tree_pruned_branch_counts", artifact)
        self.assertIn("layer_tree_parent_assignment_counts", artifact)
        self.assertIn("layer_tree_trunk_counts", artifact)

    def test_invalid_support_density_rejected(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        with self.assertRaises(SlicerV2SupportPlanningError):
            build_support_plan(
                [graph],
                vertical_edges=(),
                support_enabled=True,
                support_type=SUPPORT_TYPE_NORMAL,
                support_density_percent=120.0,
                support_spacing_mm=2.5,
                support_xy_gap_mm=0.25,
                support_z_gap_mm=0.2,
                support_interface_layers=2,
                extrusion_width_mm=0.4,
            )

    def test_support_xy_gap_reduces_footprint(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        no_gap_plans, _no_gap_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.0,
            support_z_gap_mm=0.2,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        with_gap_plans, _with_gap_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.8,
            support_z_gap_mm=0.2,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        no_gap_region = no_gap_plans[1].support_regions[0]
        with_gap_region = with_gap_plans[1].support_regions[0]
        self.assertGreater(no_gap_region.footprint_area_mm2, with_gap_region.footprint_area_mm2)

    def test_tree_branch_growth_and_merge_heuristics(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 10.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 12.0), _square(34.0, 0.0, 6.0)], layer_index=1, z_height_mm=0.4)
        layer2 = build_layer_island_graph([_square(20.5, 0.0, 10.0), _square(33.5, 0.0, 5.0)], layer_index=2, z_height_mm=0.6)
        graphs = [layer0, layer1, layer2]
        vertical_edges = build_vertical_adjacency(graphs)

        layer_plans, report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_TREE,
            support_density_percent=25.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.2,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
            tree_branch_merge_distance_ratio=1.5,
            tree_branch_growth_ratio=1.1,
            tree_min_branch_radius_mm=0.25,
        )
        self.assertGreaterEqual(report.tree_branch_count_total, 1)
        self.assertGreaterEqual(len(report.tree_branches), 1)
        self.assertGreaterEqual(sum(plan.tree_branch_count for plan in layer_plans), 1)
        self.assertGreaterEqual(report.tree_collision_avoid_count_total, 0)
        self.assertGreaterEqual(report.tree_pruned_branch_count_total, 0)
        self.assertGreaterEqual(report.tree_parent_assignment_count_total, 0)
        self.assertGreaterEqual(report.tree_trunk_count_total, 0)

    def test_tree_parent_child_trunk_assignment(self) -> None:
        layer0 = build_layer_island_graph([_square(-30.0, -30.0, 4.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(0.0, 0.0, 4.0)], layer_index=1, z_height_mm=0.4)
        layer2 = build_layer_island_graph([_square(6.0, 0.0, 4.0)], layer_index=2, z_height_mm=0.6)
        graphs = [layer0, layer1, layer2]
        vertical_edges = build_vertical_adjacency(graphs)

        layer_plans, report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_TREE,
            support_density_percent=25.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.2,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
            tree_branch_merge_distance_ratio=4.0,
            tree_branch_growth_ratio=1.1,
            tree_min_branch_radius_mm=0.25,
        )
        self.assertGreaterEqual(report.tree_parent_assignment_count_total, 1)
        self.assertGreaterEqual(report.tree_trunk_count_total, 1)
        self.assertTrue(any(branch.parent_branch_id is not None for branch in report.tree_branches))
        self.assertTrue(any(plan.tree_parent_assignment_count > 0 for plan in layer_plans))

    def test_tree_collision_aware_routing_and_pruning(self) -> None:
        layer0 = build_layer_island_graph([_square(-30.0, -30.0, 4.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph(
            [_square(8.0, 0.0, 6.0), _square(4.0, 0.0, 4.0)],
            layer_index=1,
            z_height_mm=0.4,
        )
        layer2 = build_layer_island_graph([_square(0.0, 2.0, 2.0)], layer_index=2, z_height_mm=0.6)
        graphs = [layer0, layer1, layer2]
        vertical_edges = build_vertical_adjacency(graphs)

        layer_plans, report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_TREE,
            support_density_percent=25.0,
            support_spacing_mm=2.5,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.2,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
            tree_branch_merge_distance_ratio=4.0,
            tree_branch_growth_ratio=1.1,
            tree_min_branch_radius_mm=0.25,
        )
        self.assertGreaterEqual(report.tree_collision_avoid_count_total, 1)
        self.assertGreaterEqual(report.tree_pruned_branch_count_total, 1)
        self.assertTrue(any(plan.tree_collision_avoid_count > 0 for plan in layer_plans))
        self.assertTrue(any(plan.tree_pruned_branch_count > 0 for plan in layer_plans))
        self.assertTrue(any(branch.pruned for branch in report.tree_branches))


if __name__ == "__main__":
    unittest.main()
