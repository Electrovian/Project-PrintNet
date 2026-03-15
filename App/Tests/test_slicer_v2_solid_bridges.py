import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.bridges import run as run_bridges_stage  # noqa: E402
from slicer_v2.errors import SlicerV2SolidBridgeError  # noqa: E402
from slicer_v2.geometry import polygon_from_tuples  # noqa: E402
from slicer_v2.island_graph import build_layer_island_graph, build_vertical_adjacency  # noqa: E402
from slicer_v2.settings import normalize_settings  # noqa: E402
from slicer_v2.solid_bridges import (  # noqa: E402
    SOLID_CLASS_BOTTOM,
    SOLID_CLASS_TOP,
    build_solid_layers_and_bridges,
)
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


class TestSlicerV2SolidBridges(unittest.TestCase):
    def test_settings_alias_normalizes_bridge_ratios(self) -> None:
        normalized = normalize_settings(
            {
                "bridge_flow_multiplier": "1.2",
                "bridge_speed_multiplier": "0.75",
            }
        )
        self.assertEqual(normalized["bridge_flow_ratio"], 1.2)
        self.assertEqual(normalized["bridge_speed_ratio"], 0.75)

    def test_top_bottom_solid_layer_counts(self) -> None:
        graphs = []
        for layer_index in range(5):
            graph = build_layer_island_graph(
                [_square(float(layer_index) * 0.1, 0.0, 20.0)],
                layer_index=layer_index,
                z_height_mm=(layer_index * 0.2) + 0.2,
            )
            graphs.append(graph)
        vertical_edges = build_vertical_adjacency(graphs)
        layer_plans, report = build_solid_layers_and_bridges(
            graphs,
            vertical_edges=vertical_edges,
            top_layers=1,
            bottom_layers=2,
            extrusion_width_mm=0.4,
            bridge_enabled=True,
        )
        self.assertEqual(len(layer_plans), 5)
        self.assertEqual(report.bottom_solid_layer_count, 2)
        self.assertEqual(report.top_solid_layer_count, 1)
        self.assertEqual(report.solid_layer_count, 3)
        self.assertGreater(report.solid_path_count_total, 0)

    def test_bridge_detection_for_unsupported_island(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)
        _layer_plans, report = build_solid_layers_and_bridges(
            graphs,
            vertical_edges=vertical_edges,
            top_layers=1,
            bottom_layers=1,
            extrusion_width_mm=0.4,
            bridge_enabled=True,
        )
        self.assertEqual(report.bridge_region_count_total, 1)
        self.assertGreater(report.bridge_path_count_total, 0)
        self.assertGreater(report.bridge_path_length_mm_total, 0.0)

    def test_bridge_candidate_ratio_partial_support_geometry(self) -> None:
        layer0 = build_layer_island_graph(
            [polygon_from_tuples([(0.0, 0.0), (8.0, 0.0), (8.0, 20.0), (0.0, 20.0)])],
            layer_index=0,
            z_height_mm=0.2,
        )
        layer1 = build_layer_island_graph(
            [polygon_from_tuples([(0.0, 0.0), (20.0, 0.0), (20.0, 20.0), (0.0, 20.0)])],
            layer_index=1,
            z_height_mm=0.4,
        )
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)
        layer_plans, report = build_solid_layers_and_bridges(
            graphs,
            vertical_edges=vertical_edges,
            top_layers=1,
            bottom_layers=1,
            extrusion_width_mm=0.4,
            bridge_enabled=True,
            bridge_over_infill_enabled=True,
            bridge_over_infill_min_candidate_ratio=0.01,
            bridge_over_infill_sample_count=9,
        )
        self.assertEqual(report.bridge_region_count_total, 1)
        region = layer_plans[1].bridge_regions[0]
        self.assertGreater(region.candidate_ratio, 0.05)
        self.assertLess(region.candidate_ratio, 1.0)
        self.assertGreater(region.candidate_area_mm2, 0.0)
        self.assertIsNotNone(region.span_component_id)
        self.assertGreaterEqual(len(region.span_nodes), 1)
        self.assertGreaterEqual(region.support_surface_ratio, 0.0)
        self.assertGreaterEqual(region.unsupported_surface_area_mm2, 0.0)
        self.assertTrue(
            all(
                edge.graph_weight >= 0.0
                and edge.strip_overlap_ratio >= 0.0
                and edge.strip_intersection_length_mm >= 0.0
                and edge.strip_alignment_ratio >= 0.0
                for edge in region.span_edges
            )
        )

    def test_bridge_span_components_cluster_multi_island_regions(self) -> None:
        layer0 = build_layer_island_graph([_square(-50.0, -50.0, 4.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph(
            [_square(20.0, 0.0, 8.0), _square(29.0, 0.0, 8.0)],
            layer_index=1,
            z_height_mm=0.4,
        )
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)
        layer_plans, report = build_solid_layers_and_bridges(
            graphs,
            vertical_edges=vertical_edges,
            top_layers=1,
            bottom_layers=1,
            extrusion_width_mm=0.4,
            bridge_enabled=True,
            bridge_over_infill_enabled=True,
            bridge_over_infill_min_candidate_ratio=0.01,
            bridge_over_infill_sample_count=9,
        )
        self.assertEqual(report.bridge_region_count_total, 2)
        self.assertGreaterEqual(report.bridge_span_component_count_total, 1)
        self.assertGreaterEqual(report.bridge_span_inter_island_edge_count_total, 1)
        layer = layer_plans[1]
        self.assertEqual(len(layer.bridge_regions), 2)
        self.assertGreaterEqual(layer.bridge_span_component_count, 1)
        self.assertGreaterEqual(layer.bridge_span_inter_island_edge_count, 1)
        multi_region_components = [component for component in layer.bridge_span_components if component.region_count >= 2]
        self.assertTrue(multi_region_components)
        self.assertTrue(
            any(component.strip_overlap_ratio > 0.0 and component.connectivity_weight > 0.0 for component in multi_region_components)
        )
        self.assertTrue(any(component.strip_intersection_length_mm > 0.0 for component in multi_region_components))
        self.assertTrue(
            any(
                component.dominant_angle_deg >= 0.0
                and component.dominant_angle_deg <= 180.0
                and component.dominant_angle_confidence >= 0.0
                and component.dominant_angle_confidence <= 1.0
                for component in multi_region_components
            )
        )
        for region in layer.bridge_regions:
            self.assertIsNotNone(region.span_component_id)
            self.assertGreaterEqual(region.span_component_region_count, 1)
            self.assertGreaterEqual(region.direction_vote_angle_deg, 0.0)
            self.assertLessEqual(region.direction_vote_angle_deg, 180.0)
            self.assertGreaterEqual(region.direction_vote_confidence, 0.0)
            self.assertLessEqual(region.direction_vote_confidence, 1.0)

    def test_bridge_over_infill_void_metadata_triggers_bridge(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 16.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(0.0, 0.0, 16.0)], layer_index=1, z_height_mm=0.4)
        layer2 = build_layer_island_graph([_square(0.0, 0.0, 16.0)], layer_index=2, z_height_mm=0.6)
        graphs = [layer0, layer1, layer2]
        vertical_edges = build_vertical_adjacency(graphs)
        layer_plans, report = build_solid_layers_and_bridges(
            graphs,
            vertical_edges=vertical_edges,
            top_layers=1,
            bottom_layers=1,
            extrusion_width_mm=0.4,
            bridge_enabled=True,
            bridge_over_infill_enabled=True,
            bridge_over_infill_min_candidate_ratio=0.05,
            layer_infill_void_flags=[False, True, False],
            layer_infill_combined_into_layers=[0, 2, 2],
            layer_infill_thickness_layers=[1, 2, 2],
        )
        self.assertIn("solid_bridges:combine_infill_metadata_consumed", report.warnings)
        self.assertEqual(len(layer_plans[2].bridge_regions), 1)
        region = layer_plans[2].bridge_regions[0]
        self.assertGreater(region.candidate_ratio, 0.05)
        self.assertGreater(region.path_count, 0)
        self.assertGreaterEqual(region.candidate_depth_layers, 1)

    def test_bridge_support_surface_ratio_metadata_triggers_candidate_split(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 16.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(0.0, 0.0, 16.0)], layer_index=1, z_height_mm=0.4)
        layer2 = build_layer_island_graph([_square(0.0, 0.0, 16.0)], layer_index=2, z_height_mm=0.6)
        graphs = [layer0, layer1, layer2]
        vertical_edges = build_vertical_adjacency(graphs)

        _baseline_layers, baseline_report = build_solid_layers_and_bridges(
            graphs,
            vertical_edges=vertical_edges,
            top_layers=1,
            bottom_layers=1,
            extrusion_width_mm=0.4,
            bridge_enabled=True,
            bridge_over_infill_enabled=True,
            bridge_over_infill_min_candidate_ratio=0.05,
        )
        self.assertEqual(baseline_report.bridge_region_count_total, 0)

        metadata_layers, metadata_report = build_solid_layers_and_bridges(
            graphs,
            vertical_edges=vertical_edges,
            top_layers=1,
            bottom_layers=1,
            extrusion_width_mm=0.4,
            bridge_enabled=True,
            bridge_over_infill_enabled=True,
            bridge_over_infill_min_candidate_ratio=0.05,
            layer_infill_support_surface_ratios=[1.0, 0.0, 1.0],
        )
        self.assertIn("solid_bridges:infill_support_surface_metadata_consumed", metadata_report.warnings)
        self.assertGreaterEqual(metadata_report.bridge_region_count_total, 1)
        self.assertGreater(metadata_layers[2].bridge_regions[0].candidate_ratio, 0.05)

    def test_bridge_disabled_skips_regions(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)
        _layer_plans, report = build_solid_layers_and_bridges(
            graphs,
            vertical_edges=vertical_edges,
            top_layers=1,
            bottom_layers=1,
            extrusion_width_mm=0.4,
            bridge_enabled=False,
        )
        self.assertEqual(report.bridge_region_count_total, 0)
        self.assertEqual(report.bridge_path_count_total, 0)
        self.assertGreaterEqual(report.warning_count, 1)

    def test_bridges_stage_integration(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        context = SlicerContext(
            job_id="solid-bridge-stage",
            mesh_path="solid-bridge.stl",
            resolved_settings=normalize_settings(
                {
                    "top_layers": 1,
                    "bottom_layers": 1,
                    "bridge_enabled": True,
                    "bridge_flow_ratio": 1.1,
                    "bridge_speed_ratio": 0.8,
                    "extrusion_width": 0.4,
                }
            ),
        )
        context.stage_artifacts["regions"] = {"region_count": 2}
        context.stage_artifacts["islands"] = {"layer_graphs": graphs, "vertical_edges": vertical_edges}

        artifact = run_bridges_stage(context)
        self.assertTrue(artifact["bridge_enabled"])
        self.assertEqual(artifact["top_layers"], 1)
        self.assertEqual(artifact["bottom_layers"], 1)
        self.assertEqual(artifact["layer_classifications"][0], SOLID_CLASS_BOTTOM)
        self.assertEqual(artifact["layer_classifications"][-1], SOLID_CLASS_TOP)
        self.assertGreaterEqual(artifact["bridge_region_count"], 1)
        self.assertGreaterEqual(artifact["bridge_path_count"], 1)
        self.assertEqual(len(artifact["layer_bridge_candidate_ratios"]), 2)
        self.assertEqual(len(artifact["layer_bridge_candidate_areas_mm2"]), 2)
        self.assertEqual(len(artifact["layer_bridge_candidate_depth_layers"]), 2)
        self.assertEqual(len(artifact["layer_bridge_span_node_counts"]), 2)
        self.assertEqual(len(artifact["layer_bridge_span_edge_counts"]), 2)
        self.assertEqual(len(artifact["layer_bridge_span_component_counts"]), 2)
        self.assertEqual(len(artifact["layer_bridge_span_inter_island_edge_counts"]), 2)
        self.assertEqual(len(artifact["layer_bridge_angle_sources"]), 2)
        self.assertEqual(len(artifact["layer_bridge_direction_vote_angles_deg"]), 2)
        self.assertEqual(len(artifact["layer_bridge_direction_vote_confidences"]), 2)
        self.assertIn("bridge_span_component_count_total", artifact)
        self.assertIn("bridge_span_inter_island_edge_count_total", artifact)

    def test_bridges_stage_uses_infill_anchor_angle(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        context = SlicerContext(
            job_id="solid-bridge-stage-anchor",
            mesh_path="solid-bridge-anchor.stl",
            resolved_settings=normalize_settings(
                {
                    "top_layers": 1,
                    "bottom_layers": 1,
                    "bridge_enabled": True,
                    "extrusion_width": 0.4,
                }
            ),
        )
        context.stage_artifacts["regions"] = {"region_count": 2}
        context.stage_artifacts["islands"] = {"layer_graphs": graphs, "vertical_edges": vertical_edges}
        context.stage_artifacts["infill"] = {"layer_infill_anchor_angles_deg": [15.0, 15.0]}

        artifact = run_bridges_stage(context)
        self.assertGreaterEqual(artifact["bridge_region_count"], 1)
        self.assertEqual(artifact["layer_bridge_angles_deg"][1], 105.0)
        self.assertEqual(artifact["layer_bridge_angle_sources"][1], "anchor")

    def test_bridges_stage_consumes_infill_combine_metadata(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 16.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(0.0, 0.0, 16.0)], layer_index=1, z_height_mm=0.4)
        layer2 = build_layer_island_graph([_square(0.0, 0.0, 16.0)], layer_index=2, z_height_mm=0.6)
        graphs = [layer0, layer1, layer2]
        vertical_edges = build_vertical_adjacency(graphs)

        context = SlicerContext(
            job_id="solid-bridge-stage-combine",
            mesh_path="solid-bridge-combine.stl",
            resolved_settings=normalize_settings(
                {
                    "top_layers": 1,
                    "bottom_layers": 1,
                    "bridge_enabled": True,
                    "bridge_over_infill": True,
                    "bridge_over_infill_min_ratio": 0.05,
                    "extrusion_width": 0.4,
                }
            ),
        )
        context.stage_artifacts["regions"] = {"region_count": 3}
        context.stage_artifacts["islands"] = {"layer_graphs": graphs, "vertical_edges": vertical_edges}
        context.stage_artifacts["infill"] = {
            "layer_infill_void_flags": [False, True, False],
            "layer_infill_combined_into_layers": [0, 2, 2],
            "layer_infill_thickness_layers": [1, 2, 2],
        }

        artifact = run_bridges_stage(context)
        self.assertGreaterEqual(artifact["bridge_region_count"], 1)
        self.assertGreater(artifact["layer_bridge_candidate_ratios"][2], 0.05)
        self.assertGreaterEqual(artifact["layer_bridge_candidate_depth_layers"][2], 1)

    def test_invalid_bridge_flow_ratio_rejected(self) -> None:
        graph = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        with self.assertRaises(SlicerV2SolidBridgeError):
            build_solid_layers_and_bridges(
                [graph],
                vertical_edges=(),
                top_layers=1,
                bottom_layers=1,
                extrusion_width_mm=0.4,
                bridge_enabled=True,
                bridge_flow_ratio=5.0,
            )

    def test_bridge_angle_prefers_shorter_span(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 6.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph(
            [
                polygon_from_tuples(
                    [
                        (20.0, 0.0),
                        (40.0, 0.0),
                        (40.0, 8.0),
                        (20.0, 8.0),
                    ]
                )
            ],
            layer_index=1,
            z_height_mm=0.4,
        )
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        layer_plans, report = build_solid_layers_and_bridges(
            graphs,
            vertical_edges=vertical_edges,
            top_layers=1,
            bottom_layers=1,
            extrusion_width_mm=0.4,
            bridge_enabled=True,
        )
        self.assertEqual(report.bridge_region_count_total, 1)
        region = layer_plans[1].bridge_regions[0]
        self.assertEqual(region.angle_deg, 90.0)

    def test_internal_bridge_angle_override(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        layer_plans, report = build_solid_layers_and_bridges(
            graphs,
            vertical_edges=vertical_edges,
            top_layers=1,
            bottom_layers=1,
            extrusion_width_mm=0.4,
            bridge_enabled=True,
            internal_bridge_angle_deg=33.0,
        )
        self.assertEqual(report.bridge_region_count_total, 1)
        self.assertEqual(layer_plans[1].bridge_regions[0].angle_deg, 33.0)
        self.assertEqual(layer_plans[1].bridge_regions[0].direction_angle_source, "internal")

    def test_anchor_guided_bridge_angle_from_previous_infill(self) -> None:
        layer0 = build_layer_island_graph([_square(0.0, 0.0, 8.0)], layer_index=0, z_height_mm=0.2)
        layer1 = build_layer_island_graph([_square(20.0, 0.0, 8.0)], layer_index=1, z_height_mm=0.4)
        graphs = [layer0, layer1]
        vertical_edges = build_vertical_adjacency(graphs)

        layer_plans, _report = build_solid_layers_and_bridges(
            graphs,
            vertical_edges=vertical_edges,
            top_layers=1,
            bottom_layers=1,
            extrusion_width_mm=0.4,
            bridge_enabled=True,
            layer_anchor_angles_deg=[15.0, 15.0],
        )
        self.assertEqual(layer_plans[1].bridge_regions[0].angle_deg, 105.0)
        self.assertEqual(layer_plans[1].bridge_regions[0].direction_angle_source, "anchor")


if __name__ == "__main__":
    unittest.main()
