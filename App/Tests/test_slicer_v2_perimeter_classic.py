import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.geometry import polygon_from_tuples  # noqa: E402
from slicer_v2.island_graph import build_layer_island_graph  # noqa: E402
from slicer_v2.perimeter_classic import (  # noqa: E402
    WALL_SEQUENCE_INNER_TO_OUTER,
    WALL_SEQUENCE_OUTER_TO_INNER,
    build_classic_perimeters,
)
from slicer_v2.perimeters import run as run_perimeters_stage  # noqa: E402
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


class TestSlicerV2PerimeterClassic(unittest.TestCase):
    def test_classic_perimeter_loops_count(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        layer_plans, report = build_classic_perimeters(
            [graph],
            perimeter_count=3,
            line_width_mm=0.4,
            wall_sequence=WALL_SEQUENCE_OUTER_TO_INNER,
        )
        self.assertEqual(len(layer_plans), 1)
        self.assertEqual(layer_plans[0].loop_count, 3)
        self.assertEqual(report.loop_count_total, 3)
        self.assertGreater(report.path_length_mm_total, 0.0)

    def test_classic_perimeter_loops_keep_vertices(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        layer_plans, _report = build_classic_perimeters(
            [graph],
            perimeter_count=1,
            line_width_mm=0.4,
            wall_sequence=WALL_SEQUENCE_OUTER_TO_INNER,
        )
        loop = layer_plans[0].loops[0]
        self.assertEqual(loop.point_count, len(loop.points))
        self.assertEqual(len(loop.points), 4)
        self.assertEqual(loop.points[0].as_tuple(), (0.0, 0.0))

    def test_first_layer_single_wall_override(self) -> None:
        graph0 = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        graph1 = build_layer_island_graph([_square(0.1, 0.1, 20.0)], layer_index=1, z_height_mm=0.4)
        layer_plans, report = build_classic_perimeters(
            [graph0, graph1],
            perimeter_count=3,
            line_width_mm=0.4,
            first_layer_single_wall=True,
        )
        self.assertEqual(layer_plans[0].loop_count, 1)
        self.assertEqual(layer_plans[1].loop_count, 3)
        self.assertEqual(report.loop_count_total, 4)

    def test_wall_sequence_inner_to_outer(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 15.0)], layer_index=0, z_height_mm=0.2)
        layer_plans, _report = build_classic_perimeters(
            [graph],
            perimeter_count=3,
            line_width_mm=0.4,
            wall_sequence=WALL_SEQUENCE_INNER_TO_OUTER,
        )
        first_shell = layer_plans[0].loops[0].shell_index
        last_shell = layer_plans[0].loops[-1].shell_index
        self.assertEqual(first_shell, 2)
        self.assertEqual(last_shell, 0)

    def test_hole_loops_included(self) -> None:
        outer = _square(0.0, 0.0, 20.0)
        hole = _square(5.0, 5.0, 4.0)
        graph = build_layer_island_graph([outer, hole], layer_index=0, z_height_mm=0.2)
        layer_plans, report = build_classic_perimeters(
            [graph],
            perimeter_count=2,
            line_width_mm=0.4,
        )
        roles = [loop.role for loop in layer_plans[0].loops]
        self.assertIn("outer", roles)
        self.assertIn("hole", roles)
        self.assertEqual(report.loop_count_total, len(layer_plans[0].loops))

    def test_perimeters_stage_uses_islands_artifact(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 20.0)], layer_index=0, z_height_mm=0.2)
        context = SlicerContext(
            job_id="perimeter-stage",
            mesh_path="perimeter.stl",
            resolved_settings={
                "perimeter_count": 3,
                "extrusion_width": 0.4,
                "wall_sequence": WALL_SEQUENCE_OUTER_TO_INNER,
            },
        )
        context.stage_artifacts["regions"] = {"region_count": 1}
        context.stage_artifacts["islands"] = {
            "island_count_total": 1,
            "layer_graphs": [graph],
        }
        artifact = run_perimeters_stage(context)
        self.assertEqual(artifact["perimeter_mode"], "classic")
        self.assertEqual(artifact["perimeter_path_count"], 3)
        self.assertEqual(artifact["layer_perimeter_counts"], [3])


if __name__ == "__main__":
    unittest.main()

