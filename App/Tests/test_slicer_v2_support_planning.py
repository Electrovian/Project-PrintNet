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
        self.assertIn("support_base_spacing_mm", artifact)
        self.assertIn("support_interface_spacing_mm", artifact)
        self.assertIn("support_bottom_interface_spacing_mm", artifact)
        self.assertIn("support_bottom_z_gap_mm", artifact)
        self.assertIn("support_threshold_angle_deg", artifact)
        self.assertIn("support_threshold_overlap_percent", artifact)
        self.assertIn("support_interface_bottom_layers_effective", artifact)
        self.assertIn("support_critical_regions_only", artifact)
        self.assertIn("support_remove_small_overhang", artifact)
        self.assertIn("tree_support_branch_distance_mm", artifact)
        self.assertIn("tree_support_top_rate_percent", artifact)
        self.assertIn("tree_support_branch_diameter_angle_deg", artifact)
        self.assertIn("tree_support_branch_angle_organic_deg", artifact)
        self.assertIn("tree_support_branch_diameter_organic_mm", artifact)

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

    def test_overlap_threshold_controls_unsupported_classification(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 2.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(1.8, 0.0, 2.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        _lo_plans, lo_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_threshold_overlap_percent=5.0,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        _hi_plans, hi_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_threshold_overlap_percent=30.0,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        self.assertLess(lo_report.unsupported_island_count_total, hi_report.unsupported_island_count_total)

    def test_threshold_angle_impacts_unsupported_classification(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 2.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(0.6, 0.0, 2.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        _shallow_plans, shallow_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_threshold_angle_deg=20.0,
            support_threshold_overlap_percent=35.0,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        _steep_plans, steep_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_threshold_angle_deg=80.0,
            support_threshold_overlap_percent=35.0,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        self.assertLessEqual(shallow_report.unsupported_island_count_total, steep_report.unsupported_island_count_total)

    def test_remove_small_overhang_filters_tiny_regions(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 4.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph(
            [_square(6.0, 0.0, 4.0), _square(12.0, 0.0, 0.35)],
            layer_index=1,
            z_height_mm=0.4,
        )
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        _all_plans, all_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_remove_small_overhang=False,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        _filtered_plans, filtered_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_remove_small_overhang=True,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        self.assertGreater(all_report.unsupported_island_count_total, filtered_report.unsupported_island_count_total)

    def test_critical_regions_only_filters_mild_overhangs(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 1.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph(
            [_square(0.2, 0.0, 1.0), _square(6.0, 0.0, 2.5)],
            layer_index=1,
            z_height_mm=0.4,
        )
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        _all_plans, all_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.1,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_threshold_overlap_percent=85.0,
            support_critical_regions_only=False,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        _critical_plans, critical_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.1,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_threshold_overlap_percent=85.0,
            support_critical_regions_only=True,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        self.assertGreater(all_report.unsupported_island_count_total, critical_report.unsupported_island_count_total)

    def test_top_and_bottom_z_gap_reduce_support_when_large(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        _small_gap_plans, small_gap_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        _large_gap_plans, large_gap_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.8,
            support_bottom_z_gap_mm=0.8,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        self.assertGreater(small_gap_report.support_region_count_total, large_gap_report.support_region_count_total)

    def test_separate_top_bottom_interface_layers_affect_interface_path_count(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        _base_plans, base_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_base_spacing_mm=2.0,
            support_interface_spacing_mm=1.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_interface_layers=2,
            support_interface_top_layers=2,
            support_interface_bottom_layers=0,
            extrusion_width_mm=0.4,
        )
        _more_bottom_plans, more_bottom_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_base_spacing_mm=2.0,
            support_interface_spacing_mm=1.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_interface_layers=2,
            support_interface_top_layers=2,
            support_interface_bottom_layers=3,
            extrusion_width_mm=0.4,
        )
        self.assertGreaterEqual(more_bottom_report.interface_path_count_total, base_report.interface_path_count_total)

    def test_bottom_interface_spacing_changes_interface_path_count(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        _coarse_plans, coarse_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_base_spacing_mm=2.0,
            support_interface_spacing_mm=1.2,
            support_bottom_interface_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_interface_layers=2,
            support_interface_top_layers=2,
            support_interface_bottom_layers=2,
            extrusion_width_mm=0.4,
        )
        _dense_plans, dense_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_base_spacing_mm=2.0,
            support_interface_spacing_mm=1.2,
            support_bottom_interface_spacing_mm=0.8,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_interface_layers=2,
            support_interface_top_layers=2,
            support_interface_bottom_layers=2,
            extrusion_width_mm=0.4,
        )
        self.assertGreaterEqual(dense_report.interface_path_count_total, coarse_report.interface_path_count_total)

    def test_bottom_interface_layers_negative_one_uses_top_layer_count(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        _sentinel_plans, sentinel_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_interface_layers=2,
            support_interface_top_layers=3,
            support_interface_bottom_layers=-1,
            extrusion_width_mm=0.4,
        )
        _explicit_plans, explicit_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_interface_layers=2,
            support_interface_top_layers=3,
            support_interface_bottom_layers=3,
            extrusion_width_mm=0.4,
        )
        self.assertEqual(sentinel_report.support_interface_bottom_layers, -1)
        self.assertEqual(sentinel_report.support_interface_bottom_layers_effective, 3)
        self.assertEqual(sentinel_report.interface_path_count_total, explicit_report.interface_path_count_total)

    def test_build_plate_only_changes_support_target_layer(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        layer2 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=2, z_height_mm=0.6)
        graphs = [layer0, layer1, layer2]
        vertical_edges = build_vertical_adjacency(graphs)

        no_plate_plans, _no_plate_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_build_plate_only=False,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        build_plate_plans, _build_plate_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_NORMAL,
            support_density_percent=20.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_build_plate_only=True,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        no_plate_target_layer = no_plate_plans[2].support_regions[0].layer_index
        build_plate_target_layer = build_plate_plans[2].support_regions[0].layer_index
        self.assertGreater(no_plate_target_layer, build_plate_target_layer)

    def test_tree_geometry_modifiers_change_tree_metrics(self) -> None:
        layer0 = build_layer_island_graph([_square(-30.0, -30.0, 4.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(0.0, 0.0, 6.0)], layer_index=1, z_height_mm=0.4)
        layer2 = build_layer_island_graph([_square(8.0, 0.0, 6.0)], layer_index=2, z_height_mm=0.6)
        graphs = [layer0, layer1, layer2]
        vertical_edges = build_vertical_adjacency(graphs)

        _default_plans, default_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_TREE,
            support_density_percent=25.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
        )
        _heavy_plans, heavy_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_TREE,
            support_density_percent=25.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
            tree_support_branch_angle_deg=30.0,
            tree_support_wall_count=4,
            tree_support_branch_diameter_mm=1.2,
            tree_support_tip_diameter_mm=0.6,
            tree_support_auto_brim=True,
            tree_support_brim_width_mm=6.0,
        )
        self.assertTrue(default_report.tree_branches)
        self.assertTrue(heavy_report.tree_branches)
        default_avg_radius = sum(branch.radius_mm for branch in default_report.tree_branches) / len(default_report.tree_branches)
        heavy_avg_radius = sum(branch.radius_mm for branch in heavy_report.tree_branches) / len(heavy_report.tree_branches)
        self.assertGreaterEqual(heavy_avg_radius, default_avg_radius)
        self.assertIn("tree_support:modifiers", " ".join(heavy_report.warnings))

    def test_tree_organic_overrides_are_style_gated(self) -> None:
        layer0 = build_layer_island_graph([_square(-30.0, -30.0, 4.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(0.0, 0.0, 6.0)], layer_index=1, z_height_mm=0.4)
        layer2 = build_layer_island_graph([_square(8.0, 0.0, 6.0)], layer_index=2, z_height_mm=0.6)
        graphs = [layer0, layer1, layer2]
        vertical_edges = build_vertical_adjacency(graphs)

        _tree_plans, tree_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_TREE,
            support_style="tree",
            support_density_percent=25.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
            tree_support_branch_distance_mm=1.8,
            tree_support_branch_distance_organic_mm=4.2,
            tree_support_top_rate_percent=75.0,
            tree_support_branch_diameter_angle_deg=20.0,
            tree_support_branch_angle_organic_deg=20.0,
            tree_support_branch_diameter_organic_mm=1.4,
        )
        _organic_plans, organic_report = build_support_plan(
            graphs,
            vertical_edges=vertical_edges,
            support_enabled=True,
            support_type=SUPPORT_TYPE_TREE,
            support_style="organic",
            support_density_percent=25.0,
            support_spacing_mm=2.0,
            support_xy_gap_mm=0.2,
            support_z_gap_mm=0.0,
            support_bottom_z_gap_mm=0.0,
            support_interface_layers=2,
            extrusion_width_mm=0.4,
            tree_support_branch_distance_mm=1.8,
            tree_support_branch_distance_organic_mm=4.2,
            tree_support_top_rate_percent=75.0,
            tree_support_branch_diameter_angle_deg=20.0,
            tree_support_branch_angle_organic_deg=20.0,
            tree_support_branch_diameter_organic_mm=1.4,
        )
        self.assertEqual(tree_report.support_style, "tree")
        self.assertEqual(organic_report.support_style, "organic")
        self.assertEqual(organic_report.tree_support_branch_distance_organic_mm, 4.2)
        self.assertEqual(organic_report.tree_support_top_rate_percent, 75.0)
        self.assertEqual(organic_report.tree_support_branch_diameter_angle_deg, 20.0)
        self.assertEqual(organic_report.tree_support_branch_angle_organic_deg, 20.0)
        self.assertEqual(organic_report.tree_support_branch_diameter_organic_mm, 1.4)
        self.assertTrue(tree_report.tree_branches)
        self.assertTrue(organic_report.tree_branches)
        tree_radius = sum(branch.radius_mm for branch in tree_report.tree_branches) / len(tree_report.tree_branches)
        organic_radius = sum(branch.radius_mm for branch in organic_report.tree_branches) / len(organic_report.tree_branches)
        self.assertGreaterEqual(organic_radius, tree_radius)

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
