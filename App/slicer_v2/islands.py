from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from .geometry import Polygon
from .island_graph import build_island_graph_report, build_layer_island_graph, build_vertical_adjacency
from .runtime import resolve_worker_count
from .types import SlicerContext


STAGE_NAME = "islands"


def _get_layer_contours(raw_value: object, layer_index: int) -> list[Polygon]:
    if not isinstance(raw_value, list):
        return []
    if layer_index < 0 or layer_index >= len(raw_value):
        return []
    item = raw_value[layer_index]
    if not isinstance(item, list):
        return []
    contours: list[Polygon] = []
    for candidate in item:
        if isinstance(candidate, Polygon):
            contours.append(candidate)
    return contours


def run(context: SlicerContext) -> dict:
    regions_artifact = context.stage_artifacts.get("regions", {})
    grid_artifact = context.stage_artifacts.get("slice_grid", {})

    layer_count_regions = int(regions_artifact.get("layer_count", 0))
    layer_contours_raw = regions_artifact.get("layer_contours", [])
    layer_z_values = grid_artifact.get("layer_z_values_mm", [])

    layer_count = layer_count_regions
    if isinstance(layer_contours_raw, list):
        layer_count = max(layer_count, len(layer_contours_raw))
    if isinstance(layer_z_values, list):
        layer_count = max(layer_count, len(layer_z_values))
    layer_count = max(0, layer_count)

    def _build_one(layer_index: int):
        contours = _get_layer_contours(layer_contours_raw, layer_index)
        z_height = float(layer_z_values[layer_index]) if isinstance(layer_z_values, list) and layer_index < len(layer_z_values) else float(layer_index)
        return build_layer_island_graph(
            contours,
            layer_index=layer_index,
            z_height_mm=z_height,
        )

    worker_count = resolve_worker_count(context.runtime_settings, layer_count, default=1)
    if worker_count > 1 and layer_count > 1:
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            layer_graphs = list(executor.map(_build_one, range(layer_count)))
    else:
        layer_graphs = [_build_one(layer_index) for layer_index in range(layer_count)]

    vertical_edges = build_vertical_adjacency(layer_graphs)
    report = build_island_graph_report(layer_graphs, vertical_edges)

    artifact = {
        "island_strategy": "contour-graph",
        "layer_count": report.layer_count,
        "layer_island_counts": [graph.island_count for graph in layer_graphs],
        "layer_hole_counts": [graph.hole_count for graph in layer_graphs],
        "layer_adjacency_counts": [len(graph.adjacency_edges) for graph in layer_graphs],
        "island_count_total": report.island_count_total,
        "hole_count_total": report.hole_count_total,
        "intra_layer_edge_count": report.intra_layer_edge_count,
        "vertical_edge_count": report.vertical_edge_count,
        "nesting_max_depth": report.nesting_max_depth,
        "warning_count": report.warning_count,
        "warnings": report.warnings,
        "report": report.to_dict(),
        "layer_graphs": layer_graphs,
        "vertical_edges": vertical_edges,
    }
    context.stage_artifacts[STAGE_NAME] = artifact
    return artifact
