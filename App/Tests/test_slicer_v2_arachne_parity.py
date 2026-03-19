import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.geometry import polygon_from_tuples  # noqa: E402
from slicer_v2.island_graph import build_layer_island_graph  # noqa: E402
from slicer_v2.perimeter_variable import PERIMETER_MODE_VARIABLE_WIDTH, build_variable_width_perimeters  # noqa: E402
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


class TestSlicerV2ArachneParity(unittest.TestCase):
    def test_cross_island_carryover_metadata_is_reported(self) -> None:
        graph = build_layer_island_graph(
            [
                _square(0.0, 0.0, 20.0),
                _square(28.0, 0.0, 16.0),
            ],
            layer_index=0,
            z_height_mm=0.2,
        )
        layer_plans, report = build_variable_width_perimeters(
            [graph],
            perimeter_count=3,
            base_line_width_mm=0.42,
            min_line_width_mm=0.3,
            max_line_width_mm=0.58,
            transition_smoothing=0.55,
            carryover_cross_island_enabled=True,
            carryover_strength=-1.0,
        )
        self.assertGreaterEqual(report.junction_carryover_cross_island_event_count_total, 0)
        self.assertGreaterEqual(report.junction_carryover_source_island_count_total, 0)
        self.assertEqual(len(layer_plans), 1)
        self.assertGreaterEqual(layer_plans[0].junction_carryover_cross_island_event_count, 0)
        self.assertGreaterEqual(layer_plans[0].junction_carryover_source_island_count, 0)
        self.assertTrue(all(loop.carryover_strength >= 0.0 for loop in layer_plans[0].loops))

    def test_perimeters_stage_exposes_new_arachne_parity_fields(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        context = SlicerContext(
            job_id="arachne-parity-stage",
            mesh_path="arachne-parity.stl",
            resolved_settings=normalize_settings(
                {
                    "perimeter_mode": PERIMETER_MODE_VARIABLE_WIDTH,
                    "perimeter_count": 3,
                    "extrusion_width": 0.42,
                    "variable_line_width_min": 0.3,
                    "variable_line_width_max": 0.58,
                    "arachne_carryover_cross_island": True,
                    "arachne_carry_strength": 0.4,
                }
            ),
        )
        context.stage_artifacts["regions"] = {"region_count": 1}
        context.stage_artifacts["islands"] = {"layer_graphs": [graph]}
        artifact = run_perimeters_stage(context)
        self.assertTrue(artifact["arachne_carryover_cross_island_enabled"])
        self.assertEqual(artifact["arachne_carryover_strength"], 0.4)
        self.assertIn("perimeter_junction_carryover_cross_island_event_count_total", artifact)
        self.assertIn("perimeter_junction_carryover_source_island_count_total", artifact)
        self.assertIn("layer_junction_carryover_cross_island_event_counts", artifact)
        self.assertIn("layer_junction_carryover_source_island_counts", artifact)


if __name__ == "__main__":
    unittest.main()
