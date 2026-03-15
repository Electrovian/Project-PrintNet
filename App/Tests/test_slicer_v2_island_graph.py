import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.geometry import polygon_from_tuples  # noqa: E402
from slicer_v2.island_graph import (  # noqa: E402
    build_island_graph_report,
    build_layer_island_graph,
    build_vertical_adjacency,
)
from slicer_v2.islands import run as run_islands_stage  # noqa: E402
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


class TestSlicerV2IslandGraph(unittest.TestCase):
    def test_single_island_graph(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 10.0)], layer_index=0, z_height_mm=0.2)
        self.assertEqual(graph.island_count, 1)
        self.assertEqual(graph.hole_count, 0)
        self.assertEqual(graph.nesting_max_depth, 0)

    def test_island_with_hole(self) -> None:
        outer = _square(0.0, 0.0, 20.0)
        hole = _square(5.0, 5.0, 5.0)
        graph = build_layer_island_graph([outer, hole], layer_index=0, z_height_mm=0.2)
        self.assertEqual(graph.island_count, 1)
        self.assertEqual(graph.hole_count, 1)
        self.assertGreaterEqual(graph.nesting_max_depth, 1)

    def test_nested_island_inside_hole(self) -> None:
        outer = _square(0.0, 0.0, 20.0)
        hole = _square(4.0, 4.0, 10.0)
        inner_island = _square(6.0, 6.0, 2.0)
        graph = build_layer_island_graph([outer, hole, inner_island], layer_index=0, z_height_mm=0.2)
        self.assertEqual(graph.island_count, 2)
        self.assertEqual(graph.hole_count, 1)
        self.assertGreaterEqual(graph.nesting_max_depth, 2)

    def test_layer_adjacency_edges(self) -> None:
        first = _square(0.0, 0.0, 5.0)
        second = _square(4.0, 4.0, 5.0)
        graph = build_layer_island_graph([first, second], layer_index=0, z_height_mm=0.2)
        self.assertEqual(graph.island_count, 2)
        self.assertGreaterEqual(len(graph.adjacency_edges), 1)

    def test_vertical_adjacency_and_report(self) -> None:
        lower = build_layer_island_graph([_square(0.0, 0.0, 5.0)], layer_index=0, z_height_mm=0.2)
        upper = build_layer_island_graph([_square(0.5, 0.5, 5.0)], layer_index=1, z_height_mm=0.4)
        vertical_edges = build_vertical_adjacency([lower, upper])
        report = build_island_graph_report([lower, upper], vertical_edges)
        self.assertGreaterEqual(len(vertical_edges), 1)
        self.assertEqual(report.layer_count, 2)
        self.assertGreaterEqual(report.island_count_total, 2)
        self.assertGreaterEqual(report.vertical_edge_count, 1)

    def test_islands_stage_artifact(self) -> None:
        context = SlicerContext(
            job_id="islands-stage",
            mesh_path="stage.stl",
            resolved_settings={"layer_height": 0.2},
        )
        context.stage_artifacts["slice_grid"] = {
            "layer_count": 2,
            "layer_z_values_mm": [0.1, 0.3],
        }
        context.stage_artifacts["regions"] = {
            "layer_count": 2,
            "layer_contours": [
                [_square(0.0, 0.0, 8.0)],
                [_square(0.2, 0.2, 8.0)],
            ],
        }
        artifact = run_islands_stage(context)
        self.assertEqual(artifact["layer_count"], 2)
        self.assertGreaterEqual(artifact["island_count_total"], 2)
        self.assertGreaterEqual(artifact["vertical_edge_count"], 1)


if __name__ == "__main__":
    unittest.main()

