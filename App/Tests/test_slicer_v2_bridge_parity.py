import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.bridges import run as run_bridges_stage  # noqa: E402
from slicer_v2.geometry import polygon_from_tuples  # noqa: E402
from slicer_v2.island_graph import build_layer_island_graph, build_vertical_adjacency  # noqa: E402
from slicer_v2.settings import normalize_settings  # noqa: E402
from slicer_v2.solid_bridges import build_solid_layers_and_bridges  # noqa: E402
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


class TestSlicerV2BridgeParity(unittest.TestCase):
    def test_bridge_report_exposes_span_graph_totals(self) -> None:
        layer0 = build_layer_island_graph([_square(-50.0, -50.0, 4.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph(
            [_square(20.0, 0.0, 8.0), _square(29.0, 0.0, 8.0)],
            layer_index=1,
            z_height_mm=0.4,
        )
        graphs = [layer0, layer1]
        edges = build_vertical_adjacency(graphs)
        layer_plans, report = build_solid_layers_and_bridges(
            graphs,
            vertical_edges=edges,
            top_layers=1,
            bottom_layers=1,
            extrusion_width_mm=0.42,
            bridge_enabled=True,
            bridge_over_infill_enabled=True,
            bridge_over_infill_min_candidate_ratio=0.01,
            bridge_over_infill_sample_count=9,
        )
        self.assertGreaterEqual(report.bridge_span_node_count_total, 1)
        self.assertGreaterEqual(report.bridge_span_edge_count_total, 0)
        self.assertGreaterEqual(report.bridge_candidate_ratio_avg, 0.0)
        self.assertGreaterEqual(report.bridge_support_surface_ratio_avg, 0.0)
        self.assertTrue(any(plan.bridge_span_node_count >= 1 for plan in layer_plans))

    def test_bridges_stage_consumes_rich_combine_metadata_keys(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 16.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(0.0, 0.0, 16.0)], layer_index=1, z_height_mm=0.4)
        layer2 = build_layer_island_graph([_square(0.0, 0.0, 16.0)], layer_index=2, z_height_mm=0.6)
        graphs = [layer0, layer1, layer2]
        edges = build_vertical_adjacency(graphs)

        context = SlicerContext(
            job_id="bridge-parity-stage",
            mesh_path="bridge-parity.stl",
            resolved_settings=normalize_settings(
                {
                    "bridge_enabled": True,
                    "bridge_over_infill_enabled": True,
                    "bridge_over_infill_min_candidate_ratio": 0.05,
                    "bridge_over_infill_sample_count": 9,
                    "top_layers": 1,
                    "bottom_layers": 1,
                    "extrusion_width": 0.4,
                }
            ),
        )
        context.stage_artifacts["regions"] = {"region_count": 3}
        context.stage_artifacts["islands"] = {"layer_graphs": graphs, "vertical_edges": edges}
        context.stage_artifacts["infill"] = {
            "layer_infill_void_flags": [False, True, False],
            "layer_infill_combine_target_layers": [0, 2, 2],
            "layer_infill_combine_thickness_layers": [1, 2, 2],
            "layer_infill_combine_void_depth_layers": [1, 1, 1],
            "layer_infill_support_surface_ratios": [1.0, 0.0, 1.0],
        }

        artifact = run_bridges_stage(context)
        self.assertIn("bridge_span_node_count_total", artifact)
        self.assertIn("bridge_span_edge_count_total", artifact)
        self.assertIn("bridge_candidate_ratio_avg", artifact)
        self.assertIn("bridge_support_surface_ratio_avg", artifact)
        self.assertIn("layer_infill_combine_target_layers", artifact)
        self.assertIn("layer_infill_combine_thickness_layers", artifact)
        self.assertIn("layer_infill_combine_void_depth_layers", artifact)
        self.assertTrue(artifact["infill_combine_metadata_consumed"])


if __name__ == "__main__":
    unittest.main()
