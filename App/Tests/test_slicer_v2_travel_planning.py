import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.errors import SlicerV2TravelPlanningError  # noqa: E402
from slicer_v2.geometry import polygon_from_tuples  # noqa: E402
from slicer_v2.island_graph import build_layer_island_graph  # noqa: E402
from slicer_v2.settings import normalize_settings  # noqa: E402
from slicer_v2.travel import run as run_travel_stage  # noqa: E402
from slicer_v2.travel_planning import build_travel_plan  # noqa: E402
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


class TestSlicerV2TravelPlanning(unittest.TestCase):
    def test_combing_enabled_generates_combed_moves(self) -> None:
        graph0 = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        graph1 = build_layer_island_graph(
            [
                _square(0.0, 0.0, 8.0),
                _square(12.0, 0.0, 8.0),
            ],
            layer_index=1,
            z_height_mm=0.4,
        )
        layer_plans, report = build_travel_plan(
            [graph0, graph1],
            layer_perimeter_counts=[2, 4],
            layer_infill_counts=[1, 2],
            layer_support_counts=[0, 1],
            travel_speed_mm_s=150.0,
            combing_enabled=True,
            combing_max_detour_ratio=1.7,
            retract_enabled=True,
            retract_min_travel_mm=2.0,
            z_hop_enabled=True,
            z_hop_mm=0.2,
        )
        self.assertEqual(len(layer_plans), 2)
        self.assertGreater(report.move_count_total, 0)
        self.assertGreater(report.combed_move_count_total, 0)
        self.assertGreater(report.travel_length_mm_total, 0.0)

    def test_combing_disabled_fallback_only(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        _layer_plans, report = build_travel_plan(
            [graph],
            layer_perimeter_counts=[4],
            layer_infill_counts=[2],
            layer_support_counts=[1],
            travel_speed_mm_s=150.0,
            combing_enabled=False,
            combing_max_detour_ratio=1.5,
            retract_enabled=False,
            retract_min_travel_mm=2.0,
            z_hop_enabled=False,
            z_hop_mm=0.2,
        )
        self.assertEqual(report.combed_move_count_total, 0)
        self.assertEqual(report.fallback_move_count_total, report.move_count_total)

    def test_settings_aliases_for_travel_controls(self) -> None:
        normalized = normalize_settings(
            {
                "avoid_crossing_walls": "yes",
                "combing_max_detour_ratio": "2.0",
                "retraction_enable": "true",
                "retract_min_travel": "3.5",
                "z_hop_enable": "1",
                "z_hop_height": "0.35",
            }
        )
        self.assertTrue(normalized["travel_combing_enabled"])
        self.assertEqual(normalized["travel_combing_max_detour_ratio"], 2.0)
        self.assertTrue(normalized["travel_retract_enabled"])
        self.assertEqual(normalized["travel_retract_min_travel_mm"], 3.5)
        self.assertTrue(normalized["travel_z_hop_enabled"])
        self.assertEqual(normalized["travel_z_hop_mm"], 0.35)

    def test_travel_stage_integration(self) -> None:
        graph0 = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        graph1 = build_layer_island_graph(
            [
                _square(0.0, 0.0, 8.0),
                _square(12.0, 0.0, 8.0),
            ],
            layer_index=1,
            z_height_mm=0.4,
        )
        context = SlicerContext(
            job_id="travel-stage",
            mesh_path="travel.stl",
            resolved_settings=normalize_settings(
                {
                    "travel_speed": 180.0,
                    "travel_combing_enabled": True,
                    "travel_combing_max_detour_ratio": 1.7,
                    "travel_retract_enabled": True,
                    "travel_retract_min_travel_mm": 2.0,
                    "travel_z_hop_enabled": True,
                    "travel_z_hop_mm": 0.2,
                }
            ),
        )
        context.stage_artifacts["islands"] = {"layer_graphs": [graph0, graph1]}
        context.stage_artifacts["perimeters"] = {"layer_perimeter_counts": [2, 4], "perimeter_path_count": 6}
        context.stage_artifacts["infill"] = {"layer_infill_counts": [1, 2], "infill_path_count": 3}
        context.stage_artifacts["supports"] = {"layer_support_path_counts": [0, 1], "support_path_count": 1}
        artifact = run_travel_stage(context)
        self.assertEqual(artifact["travel_speed_mm_s"], 180.0)
        self.assertGreaterEqual(artifact["travel_move_count"], 1)
        self.assertGreaterEqual(artifact["travel_combed_move_count"], 1)
        self.assertGreaterEqual(artifact["travel_length_mm_total"], 0.0)

    def test_invalid_detour_ratio_rejected(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        with self.assertRaises(SlicerV2TravelPlanningError):
            build_travel_plan(
                [graph],
                layer_perimeter_counts=[2],
                layer_infill_counts=[1],
                layer_support_counts=[0],
                travel_speed_mm_s=150.0,
                combing_enabled=True,
                combing_max_detour_ratio=0.5,
                retract_enabled=True,
                retract_min_travel_mm=2.0,
                z_hop_enabled=False,
                z_hop_mm=0.2,
            )

    def test_crossing_move_triggers_retract(self) -> None:
        graph = build_layer_island_graph(
            [
                _square(0.0, 0.0, 8.0),
                _square(12.0, 0.0, 8.0),
            ],
            layer_index=0,
            z_height_mm=0.2,
        )
        layer_plans, report = build_travel_plan(
            [graph],
            layer_perimeter_counts=[2],
            layer_infill_counts=[0],
            layer_support_counts=[0],
            travel_speed_mm_s=150.0,
            combing_enabled=True,
            combing_max_detour_ratio=1.5,
            retract_enabled=True,
            retract_min_travel_mm=1.0,
            z_hop_enabled=True,
            z_hop_mm=0.2,
        )
        self.assertEqual(len(layer_plans), 1)
        self.assertEqual(report.move_count_total, 1)
        self.assertGreaterEqual(report.retract_count_total, 1)
        self.assertGreaterEqual(report.z_hop_count_total, 1)


if __name__ == "__main__":
    unittest.main()
