import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.geometry import polygon_from_tuples  # noqa: E402
from slicer_v2.island_graph import build_layer_island_graph  # noqa: E402
from slicer_v2.perimeter_classic import WALL_SEQUENCE_INNER_TO_OUTER  # noqa: E402
from slicer_v2.perimeter_variable import (  # noqa: E402
    PERIMETER_MODE_VARIABLE_WIDTH,
    _JunctionCarryState,
    _resample_carryover_deltas,
    build_variable_width_perimeters,
)
from slicer_v2.perimeters import run as run_perimeters_stage  # noqa: E402
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


class TestSlicerV2PerimeterVariable(unittest.TestCase):
    def test_variable_width_plan_respects_width_bounds(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        layer_plans, report = build_variable_width_perimeters(
            [graph],
            perimeter_count=3,
            base_line_width_mm=0.4,
            min_line_width_mm=0.3,
            max_line_width_mm=0.55,
        )
        self.assertEqual(report.loop_count_total, 3)
        self.assertGreater(report.path_length_mm_total, 0.0)
        for loop in layer_plans[0].loops:
            self.assertGreaterEqual(loop.width_mm, 0.3)
            self.assertLessEqual(loop.width_mm, 0.55)

    def test_first_layer_single_wall(self) -> None:
        graph0 = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        graph1 = build_layer_island_graph([_square(0.1, 0.1, 20.0)], layer_index=1, z_height_mm=0.4)
        layer_plans, report = build_variable_width_perimeters(
            [graph0, graph1],
            perimeter_count=3,
            base_line_width_mm=0.4,
            min_line_width_mm=0.3,
            max_line_width_mm=0.55,
            first_layer_single_wall=True,
        )
        self.assertEqual(layer_plans[0].loop_count, 1)
        self.assertEqual(layer_plans[1].loop_count, 3)
        self.assertEqual(report.loop_count_total, 4)

    def test_wall_sequence_inner_to_outer(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        layer_plans, _report = build_variable_width_perimeters(
            [graph],
            perimeter_count=3,
            base_line_width_mm=0.4,
            min_line_width_mm=0.3,
            max_line_width_mm=0.55,
            wall_sequence=WALL_SEQUENCE_INNER_TO_OUTER,
        )
        first_shell = layer_plans[0].loops[0].shell_index
        last_shell = layer_plans[0].loops[-1].shell_index
        self.assertEqual(first_shell, 2)
        self.assertEqual(last_shell, 0)

    def test_variable_width_transitions_and_junctions(self) -> None:
        graph = build_layer_island_graph(
            [
                polygon_from_tuples(
                    [
                        (0.0, 0.0),
                        (25.0, 0.0),
                        (25.0, 10.0),
                        (15.0, 10.0),
                        (15.0, 20.0),
                        (0.0, 20.0),
                    ]
                )
            ],
            layer_index=0,
            z_height_mm=0.2,
        )
        layer_plans, report = build_variable_width_perimeters(
            [graph],
            perimeter_count=3,
            base_line_width_mm=0.4,
            min_line_width_mm=0.3,
            max_line_width_mm=0.55,
            transition_smoothing=0.5,
            junction_compensation_enabled=True,
            junction_sharp_angle_deg=130.0,
        )
        self.assertGreater(report.transition_count_total, 0)
        self.assertGreater(report.junction_count_total, 0)
        self.assertGreater(report.half_edge_bead_count_total, 0)
        self.assertGreater(report.half_edge_redistribution_mm_total, 0.0)
        self.assertGreater(report.junction_carryover_event_count_total, 0)
        self.assertGreater(report.junction_carryover_ratio_avg, 0.0)
        self.assertGreater(layer_plans[0].transition_count, 0)
        self.assertGreater(layer_plans[0].junction_count, 0)
        self.assertGreater(layer_plans[0].half_edge_bead_count, 0)
        self.assertGreater(layer_plans[0].half_edge_redistribution_mm, 0.0)
        self.assertGreater(layer_plans[0].junction_carryover_event_count, 0)
        self.assertGreater(layer_plans[0].junction_carryover_ratio_avg, 0.0)
        self.assertTrue(
            any(abs(bead.width_mm - bead.base_width_mm) > 1e-6 for bead in layer_plans[0].half_edge_beads)
        )
        self.assertTrue(any(loop.junction_carryover_ratio > 0.0 for loop in layer_plans[0].loops))

    def test_carryover_resampling_interpolates_and_aligns(self) -> None:
        state = _JunctionCarryState(
            fractions=(0.0, 0.5),
            deltas=(0.0, 1.0),
        )
        target_fractions = [0.25, 0.75]
        target_sharpness = [1.0, 0.0]
        sampled = _resample_carryover_deltas(
            state,
            target_fractions,
            target_sharpness,
        )
        self.assertEqual(len(sampled), 2)
        self.assertGreater(sampled[0], sampled[1])
        self.assertGreater(sampled[0], 0.4)

    def test_half_edge_bead_mass_conservation(self) -> None:
        graph = build_layer_island_graph(
            [
                polygon_from_tuples(
                    [
                        (0.0, 0.0),
                        (30.0, 0.0),
                        (30.0, 8.0),
                        (18.0, 8.0),
                        (18.0, 22.0),
                        (0.0, 22.0),
                    ]
                )
            ],
            layer_index=0,
            z_height_mm=0.2,
        )
        layer_plans, _report = build_variable_width_perimeters(
            [graph],
            perimeter_count=3,
            base_line_width_mm=0.42,
            min_line_width_mm=0.3,
            max_line_width_mm=0.58,
            transition_smoothing=0.7,
            junction_compensation_enabled=True,
            junction_sharp_angle_deg=125.0,
        )
        layer = layer_plans[0]
        self.assertGreater(len(layer.half_edge_beads), 0)
        for loop in layer.loops:
            shell_beads = [
                bead
                for bead in layer.half_edge_beads
                if bead.island_index == loop.island_index
                and bead.role == loop.role
                and bead.shell_index == loop.shell_index
            ]
            self.assertTrue(shell_beads)
            total_edge_length = sum(max(1e-6, float(bead.edge_length_mm)) for bead in shell_beads)
            weighted_width = sum(
                float(bead.width_mm) * max(1e-6, float(bead.edge_length_mm)) for bead in shell_beads
            )
            self.assertAlmostEqual(weighted_width / total_edge_length, loop.width_mm, delta=0.04)

    def test_perimeters_stage_variable_mode(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        context = SlicerContext(
            job_id="perimeter-variable-stage",
            mesh_path="perimeter-variable.stl",
            resolved_settings=normalize_settings(
                {
                    "perimeter_mode": PERIMETER_MODE_VARIABLE_WIDTH,
                    "perimeter_count": 3,
                    "extrusion_width": 0.4,
                    "variable_line_width_min": 0.3,
                    "variable_line_width_max": 0.55,
                }
            ),
        )
        context.stage_artifacts["regions"] = {"region_count": 1}
        context.stage_artifacts["islands"] = {"layer_graphs": [graph]}
        artifact = run_perimeters_stage(context)
        self.assertEqual(artifact["perimeter_mode"], PERIMETER_MODE_VARIABLE_WIDTH)
        self.assertEqual(artifact["perimeter_path_count"], 3)
        self.assertEqual(artifact["layer_perimeter_counts"], [3])
        self.assertEqual(len(artifact["layer_min_widths_mm"]), 1)
        self.assertEqual(len(artifact["layer_max_widths_mm"]), 1)
        self.assertEqual(len(artifact["layer_transition_counts"]), 1)
        self.assertEqual(len(artifact["layer_junction_counts"]), 1)
        self.assertEqual(len(artifact["layer_half_edge_bead_counts"]), 1)
        self.assertEqual(len(artifact["layer_junction_carryover_event_counts"]), 1)
        self.assertIn("perimeter_half_edge_bead_count_total", artifact)
        self.assertIn("perimeter_half_edge_redistribution_mm_total", artifact)
        self.assertIn("perimeter_junction_carryover_event_count_total", artifact)
        self.assertIn("perimeter_junction_carryover_ratio_avg", artifact)

    def test_settings_normalize_perimeter_mode_and_width_swap(self) -> None:
        normalized = normalize_settings(
            {
                "perimeter_generator": "arachne",
                "line_width_min": "0.6",
                "line_width_max": "0.3",
            }
        )
        self.assertEqual(normalized["perimeter_mode"], PERIMETER_MODE_VARIABLE_WIDTH)
        self.assertLessEqual(normalized["variable_line_width_min"], normalized["variable_line_width_max"])


if __name__ == "__main__":
    unittest.main()
