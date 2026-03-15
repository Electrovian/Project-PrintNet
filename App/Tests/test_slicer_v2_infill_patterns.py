import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.geometry import polygon_from_tuples  # noqa: E402
from slicer_v2.infill import run as run_infill_stage  # noqa: E402
from slicer_v2.infill_patterns import (  # noqa: E402
    INFILL_PATTERN_3D_HONEYCOMB,
    INFILL_PATTERN_CONCENTRIC,
    INFILL_PATTERN_CROSS_HATCH,
    INFILL_PATTERN_GRID,
    INFILL_PATTERN_GYROID,
    INFILL_PATTERN_HONEYCOMB,
    INFILL_PATTERN_LIGHTNING,
    INFILL_PATTERN_RECTILINEAR,
    INFILL_PATTERN_TPMS_D,
    INFILL_PATTERN_TPMS_F_K,
    build_infill_patterns,
)
from slicer_v2.island_graph import build_layer_island_graph  # noqa: E402
from slicer_v2.settings import normalize_settings  # noqa: E402
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


class TestSlicerV2InfillPatterns(unittest.TestCase):
    def test_rectilinear_generates_paths(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        layer_plans, report = build_infill_patterns(
            [graph],
            infill_pattern=INFILL_PATTERN_RECTILINEAR,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
        )
        self.assertEqual(report.pattern, INFILL_PATTERN_RECTILINEAR)
        self.assertEqual(len(layer_plans), 1)
        self.assertGreater(layer_plans[0].path_count, 0)
        self.assertGreater(layer_plans[0].island_area_mm2, 0.0)
        self.assertGreater(layer_plans[0].effective_infill_area_mm2, 0.0)
        self.assertGreater(layer_plans[0].support_surface_ratio, 0.0)
        self.assertEqual(layer_plans[0].void_depth_layers, 1)
        self.assertGreater(report.path_count_total, 0)
        self.assertEqual(report.void_layer_count, 0)
        self.assertGreater(report.support_surface_ratio_avg, 0.0)

    def test_grid_has_more_paths_than_rectilinear(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        rect_plans, rect_report = build_infill_patterns(
            [graph],
            infill_pattern=INFILL_PATTERN_RECTILINEAR,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
        )
        grid_plans, grid_report = build_infill_patterns(
            [graph],
            infill_pattern=INFILL_PATTERN_GRID,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
        )
        self.assertGreaterEqual(grid_plans[0].path_count, rect_plans[0].path_count)
        self.assertGreaterEqual(grid_report.path_count_total, rect_report.path_count_total)

    def test_gyroid_generates_paths(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        layer_plans, report = build_infill_patterns(
            [graph],
            infill_pattern=INFILL_PATTERN_GYROID,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
        )
        self.assertEqual(report.pattern, INFILL_PATTERN_GYROID)
        self.assertGreater(layer_plans[0].path_count, 0)
        self.assertGreater(layer_plans[0].path_length_mm, 0.0)

    def test_lightning_pattern_generates_paths(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        layer_plans, report = build_infill_patterns(
            [graph],
            infill_pattern=INFILL_PATTERN_LIGHTNING,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
        )
        self.assertEqual(report.pattern, INFILL_PATTERN_LIGHTNING)
        self.assertGreater(layer_plans[0].path_count, 0)

    def test_extended_patterns_generate_paths(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        for pattern in (
            INFILL_PATTERN_CONCENTRIC,
            INFILL_PATTERN_HONEYCOMB,
            INFILL_PATTERN_3D_HONEYCOMB,
            INFILL_PATTERN_CROSS_HATCH,
            INFILL_PATTERN_TPMS_D,
            INFILL_PATTERN_TPMS_F_K,
        ):
            layer_plans, report = build_infill_patterns(
                [graph],
                infill_pattern=pattern,
                infill_percent=20.0,
                extrusion_width_mm=0.4,
            )
            self.assertEqual(report.pattern, pattern)
            self.assertGreater(layer_plans[0].path_count, 0)

    def test_geometry_clip_reduces_paths_for_holes(self) -> None:
        outer = _square(0.0, 0.0, 20.0)
        inner = _square(6.0, 6.0, 8.0)
        solid_graph = build_layer_island_graph([outer], layer_index=0, z_height_mm=0.2)
        hole_graph = build_layer_island_graph([outer, inner], layer_index=0, z_height_mm=0.2)

        solid_layers, _solid_report = build_infill_patterns(
            [solid_graph],
            infill_pattern=INFILL_PATTERN_RECTILINEAR,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
        )
        hole_layers, _hole_report = build_infill_patterns(
            [hole_graph],
            infill_pattern=INFILL_PATTERN_RECTILINEAR,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
        )
        self.assertGreater(solid_layers[0].path_length_mm, hole_layers[0].path_length_mm)

    def test_angle_alternation(self) -> None:
        graph0 = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        graph1 = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=1, z_height_mm=0.4)
        graph2 = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=2, z_height_mm=0.6)
        layer_plans, _report = build_infill_patterns(
            [graph0, graph1, graph2],
            infill_pattern=INFILL_PATTERN_RECTILINEAR,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
            angle_start_deg=30.0,
            angle_step_deg=90.0,
        )
        self.assertEqual(layer_plans[0].angle_deg, 30.0)
        self.assertEqual(layer_plans[1].angle_deg, 120.0)
        self.assertEqual(layer_plans[2].angle_deg, 210.0)

    def test_angle_template_sequence(self) -> None:
        graph0 = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        graph1 = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=1, z_height_mm=0.4)
        graph2 = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=2, z_height_mm=0.6)
        layer_plans, _report = build_infill_patterns(
            [graph0, graph1, graph2],
            infill_pattern=INFILL_PATTERN_RECTILINEAR,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
            angle_start_deg=12.0,
            angle_step_deg=90.0,
            angle_template="0,90",
            layer_height_mm=0.2,
        )
        self.assertEqual(layer_plans[0].angle_deg, 0.0)
        self.assertEqual(layer_plans[1].angle_deg, 90.0)
        self.assertEqual(layer_plans[2].angle_deg, 0.0)

    def test_zero_density_results_in_zero_paths(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        layer_plans, report = build_infill_patterns(
            [graph],
            infill_pattern=INFILL_PATTERN_RECTILINEAR,
            infill_percent=0.0,
            extrusion_width_mm=0.4,
        )
        self.assertEqual(layer_plans[0].path_count, 0)
        self.assertEqual(report.path_count_total, 0)

    def test_anchor_length_increases_path_length(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        no_anchor, _report0 = build_infill_patterns(
            [graph],
            infill_pattern=INFILL_PATTERN_RECTILINEAR,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
            infill_anchor=0.0,
            infill_anchor_max=1000.0,
        )
        anchored, _report1 = build_infill_patterns(
            [graph],
            infill_pattern=INFILL_PATTERN_RECTILINEAR,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
            infill_anchor="30%",
            infill_anchor_max=1000.0,
        )
        self.assertGreater(anchored[0].path_length_mm, no_anchor[0].path_length_mm)

    def test_overlap_settings_increase_infill_path_estimates(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        base_layers, _base_report = build_infill_patterns(
            [graph],
            infill_pattern=INFILL_PATTERN_RECTILINEAR,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
            infill_wall_overlap_percent=0.0,
            top_bottom_infill_wall_overlap_percent=0.0,
        )
        overlap_layers, _overlap_report = build_infill_patterns(
            [graph],
            infill_pattern=INFILL_PATTERN_RECTILINEAR,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
            infill_wall_overlap_percent=30.0,
            top_bottom_infill_wall_overlap_percent=0.0,
        )
        self.assertGreaterEqual(overlap_layers[0].path_count, base_layers[0].path_count)
        self.assertGreater(overlap_layers[0].path_length_mm, base_layers[0].path_length_mm)
        self.assertGreater(overlap_layers[0].effective_infill_area_mm2, base_layers[0].effective_infill_area_mm2)
        self.assertGreater(overlap_layers[0].overlap_geometric_offset_mm, 0.0)
        self.assertTrue(overlap_layers[0].overlap_geometric_applied)

    def test_top_bottom_overlap_applies_extra_multiplier_on_shell_layers(self) -> None:
        graphs = [
            build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2),
            build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=1, z_height_mm=0.4),
            build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=2, z_height_mm=0.6),
        ]
        layer_plans, _report = build_infill_patterns(
            graphs,
            infill_pattern=INFILL_PATTERN_RECTILINEAR,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
            infill_wall_overlap_percent=10.0,
            top_bottom_infill_wall_overlap_percent=20.0,
            bottom_shell_layers=1,
            top_shell_layers=1,
        )
        self.assertGreater(layer_plans[0].overlap_multiplier, layer_plans[1].overlap_multiplier)
        self.assertGreater(layer_plans[2].overlap_multiplier, layer_plans[1].overlap_multiplier)

    def test_infill_combination_zeros_non_top_layers(self) -> None:
        graphs = [
            build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2),
            build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=1, z_height_mm=0.4),
            build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=2, z_height_mm=0.6),
        ]
        layer_plans, report = build_infill_patterns(
            graphs,
            infill_pattern=INFILL_PATTERN_RECTILINEAR,
            infill_percent=20.0,
            extrusion_width_mm=0.4,
            combine_infill_enabled=True,
            combine_max_layer_height_mm=0.45,
        )
        self.assertEqual(len(layer_plans), 3)
        self.assertIn("infill_combination:enabled", report.warnings)
        self.assertEqual(layer_plans[1].path_count, 0)
        self.assertGreater(layer_plans[2].path_count, 0)
        self.assertFalse(layer_plans[0].is_void_layer)
        self.assertTrue(layer_plans[1].is_void_layer)
        self.assertEqual(layer_plans[1].combined_into_layer_index, 2)
        self.assertEqual(layer_plans[1].combined_thickness_layers, 2)
        self.assertEqual(layer_plans[1].void_depth_layers, 1)
        self.assertEqual(layer_plans[1].support_surface_ratio, 0.0)
        self.assertGreater(layer_plans[2].support_surface_ratio, 0.0)
        self.assertEqual(layer_plans[2].combined_layer_count, 2)
        self.assertEqual(report.void_layer_count, 1)
        self.assertGreaterEqual(report.support_surface_ratio_avg, 0.0)

    def test_infill_stage_uses_islands(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        context = SlicerContext(
            job_id="infill-stage",
            mesh_path="infill.stl",
            resolved_settings=normalize_settings(
                {
                    "infill_percent": 20.0,
                    "infill_pattern": "grid",
                    "infill_angle_start": 15.0,
                    "infill_angle_step": 90.0,
                    "extrusion_width": 0.4,
                }
            ),
        )
        context.stage_artifacts["regions"] = {"region_count": 1}
        context.stage_artifacts["islands"] = {"layer_graphs": [graph]}
        artifact = run_infill_stage(context)
        self.assertEqual(artifact["infill_pattern"], INFILL_PATTERN_GRID)
        self.assertGreater(artifact["infill_path_count"], 0)
        self.assertEqual(artifact["layer_infill_angles_deg"], [15.0])
        self.assertIn("infill_wall_overlap_percent", artifact)
        self.assertIn("top_bottom_infill_wall_overlap_percent", artifact)
        self.assertIn("layer_infill_overlap_multipliers", artifact)
        self.assertIn("layer_infill_overlap_geometric_offsets_mm", artifact)
        self.assertIn("layer_infill_overlap_top_bottom_offsets_mm", artifact)
        self.assertIn("layer_infill_overlap_geometric_applied", artifact)
        self.assertIn("layer_infill_overlap_geometric_fallback_used", artifact)
        self.assertEqual(len(artifact["layer_infill_anchor_angles_deg"]), 1)
        self.assertEqual(artifact["layer_infill_void_flags"], [False])
        self.assertEqual(artifact["layer_infill_void_depth_layers"], [1])
        self.assertEqual(len(artifact["layer_infill_support_surface_ratios"]), 1)
        self.assertEqual(len(artifact["layer_infill_island_areas_mm2"]), 1)
        self.assertEqual(len(artifact["layer_infill_effective_areas_mm2"]), 1)
        self.assertEqual(artifact["layer_infill_combined_into_layers"], [0])
        self.assertTrue(artifact["infill_antivibration_enabled"])


if __name__ == "__main__":
    unittest.main()
