from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from math import atan2, ceil, cos, degrees, hypot, radians, sin
from typing import Sequence

from .errors import SlicerV2SolidBridgeError
from .geometry import EPSILON, Island, Point2, Polygon
from .island_graph import LayerIslandGraph, VerticalAdjacencyEdge
from .line_split import split_line
from .region_expansion import RegionExpansionParameters, propagate_waves_from_polygons


SOLID_CLASS_BOTTOM = "bottom"
SOLID_CLASS_TOP = "top"
SOLID_CLASS_INTERNAL = "internal"
ALLOWED_SOLID_CLASSES = {SOLID_CLASS_BOTTOM, SOLID_CLASS_TOP, SOLID_CLASS_INTERNAL}


@dataclass
class BridgeSpanNode:
    layer_index: int
    island_index: int
    node_index: int
    offset_start_mm: float
    offset_end_mm: float
    span_length_mm: float
    center_x_mm: float
    center_y_mm: float
    support_ratio: float
    candidate_ratio: float
    path_count: int
    path_length_mm: float
    line_start_x_mm: float = 0.0
    line_start_y_mm: float = 0.0
    line_end_x_mm: float = 0.0
    line_end_y_mm: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class BridgeSpanEdge:
    layer_index: int
    island_index: int
    src_node_index: int
    dst_node_index: int
    continuity_ratio: float
    shared_candidate_ratio: float
    strip_overlap_ratio: float = 0.0
    strip_intersection_length_mm: float = 0.0
    strip_alignment_ratio: float = 0.0
    direction_weight: float = 0.0
    graph_weight: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class BridgeSpanComponent:
    layer_index: int
    component_id: int
    island_indices: list[int]
    region_count: int
    node_count: int
    edge_count: int
    inter_island_edge_count: int
    candidate_ratio: float
    candidate_area_mm2: float
    path_count: int
    path_length_mm: float
    connectivity_weight: float = 0.0
    strip_overlap_ratio: float = 0.0
    strip_intersection_length_mm: float = 0.0
    direction_alignment_ratio: float = 0.0
    dominant_angle_deg: float = 0.0
    dominant_angle_confidence: float = 0.0
    direction_vote_weight: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class BridgeRegionPlan:
    layer_index: int
    island_index: int
    angle_deg: float
    path_count: int
    path_length_mm: float
    span_major_mm: float
    span_minor_mm: float
    anchor_ratio: float = 0.0
    candidate_ratio: float = 0.0
    candidate_area_mm2: float = 0.0
    candidate_depth_layers: int = 1
    support_surface_ratio: float = 0.0
    unsupported_surface_area_mm2: float = 0.0
    span_component_id: int | None = None
    span_component_region_count: int = 1
    span_component_node_count: int = 0
    span_component_inter_island_edge_count: int = 0
    direction_vote_angle_deg: float = 0.0
    direction_vote_confidence: float = 0.0
    direction_angle_source: str = "local"
    span_nodes: list[BridgeSpanNode] = field(default_factory=list)
    span_edges: list[BridgeSpanEdge] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class SolidLayerPlan:
    layer_index: int
    z_height_mm: float
    classification: str
    is_solid: bool
    island_count: int
    solid_path_count: int
    solid_path_length_mm: float
    bridge_region_count: int
    bridge_path_count: int
    bridge_path_length_mm: float
    bridge_span_component_count: int = 0
    bridge_span_inter_island_edge_count: int = 0
    bridge_span_node_count: int = 0
    bridge_span_edge_count: int = 0
    bridge_span_components: list[BridgeSpanComponent] = field(default_factory=list)
    bridge_regions: list[BridgeRegionPlan] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["path_count"] = self.solid_path_count + self.bridge_path_count
        return payload


@dataclass
class SolidBridgeReport:
    generated_at_utc: str
    layer_count: int
    island_count_total: int
    top_layers_requested: int
    bottom_layers_requested: int
    solid_layer_count: int
    bottom_solid_layer_count: int
    top_solid_layer_count: int
    solid_path_count_total: int
    solid_path_length_mm_total: float
    bridge_enabled: bool
    bridge_region_count_total: int
    bridge_path_count_total: int
    bridge_path_length_mm_total: float
    bridge_span_component_count_total: int
    bridge_span_inter_island_edge_count_total: int
    bridge_flow_ratio: float
    bridge_speed_ratio: float
    warning_count: int
    bridge_span_node_count_total: int = 0
    bridge_span_edge_count_total: int = 0
    bridge_candidate_ratio_avg: float = 0.0
    bridge_support_surface_ratio_avg: float = 0.0
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _validate_layer_graphs(layer_graphs: Sequence[LayerIslandGraph]) -> list[LayerIslandGraph]:
    graphs = list(layer_graphs)
    for index, graph in enumerate(graphs):
        if not isinstance(graph, LayerIslandGraph):
            raise SlicerV2SolidBridgeError(f"SOLID_BRIDGE_LAYER_GRAPH_INVALID:{index}")
    return graphs


def _validate_vertical_edges(vertical_edges: Sequence[VerticalAdjacencyEdge]) -> list[VerticalAdjacencyEdge]:
    edges = list(vertical_edges)
    for index, edge in enumerate(edges):
        if not isinstance(edge, VerticalAdjacencyEdge):
            raise SlicerV2SolidBridgeError(f"SOLID_BRIDGE_VERTICAL_EDGE_INVALID:{index}")
    return edges


def _validate_layers_count(value: int, label: str) -> int:
    count = int(value)
    if count < 0:
        raise SlicerV2SolidBridgeError(f"SOLID_BRIDGE_LAYER_COUNT_NEGATIVE:{label}")
    if count > 200:
        raise SlicerV2SolidBridgeError(f"SOLID_BRIDGE_LAYER_COUNT_EXCESSIVE:{label}")
    return count


def _validate_width(width_mm: float) -> float:
    width = float(width_mm)
    if width <= EPSILON:
        raise SlicerV2SolidBridgeError("SOLID_BRIDGE_EXTRUSION_WIDTH_INVALID")
    return width


def _validate_ratio(value: float, code: str, minimum: float, maximum: float) -> float:
    ratio = float(value)
    if ratio < minimum or ratio > maximum:
        raise SlicerV2SolidBridgeError(code)
    return ratio


def _validate_sample_count(value: int, code: str, minimum: int, maximum: int) -> int:
    count = int(value)
    if count < minimum or count > maximum:
        raise SlicerV2SolidBridgeError(code)
    return count


def _normalize_angle(angle_deg: float) -> float:
    value = float(angle_deg)
    while value < 0.0:
        value += 360.0
    while value >= 360.0:
        value -= 360.0
    return value


def _layer_classification(layer_index: int, layer_count: int, bottom_layers: int, top_layers: int) -> str:
    if layer_index < bottom_layers:
        return SOLID_CLASS_BOTTOM
    top_start = max(0, layer_count - top_layers)
    if layer_index >= top_start:
        return SOLID_CLASS_TOP
    return SOLID_CLASS_INTERNAL


def _supported_islands_by_layer(vertical_edges: Sequence[VerticalAdjacencyEdge]) -> dict[int, set[int]]:
    supported: dict[int, set[int]] = {}
    for edge in vertical_edges:
        upper_layer = int(edge.upper_layer_index)
        upper_island = int(edge.upper_island_index)
        if upper_layer not in supported:
            supported[upper_layer] = set()
        supported[upper_layer].add(upper_island)
    return supported


def _layer_lookup(layer_graphs: Sequence[LayerIslandGraph]) -> dict[int, LayerIslandGraph]:
    out: dict[int, LayerIslandGraph] = {}
    for graph in layer_graphs:
        out[int(graph.layer_index)] = graph
    return out


def _solid_path_estimate(span_major_mm: float, span_minor_mm: float, extrusion_width_mm: float) -> tuple[int, float]:
    if span_major_mm <= EPSILON or span_minor_mm <= EPSILON:
        return 0, 0.0
    line_count = max(1, int(ceil(span_minor_mm / extrusion_width_mm)))
    path_length = float(line_count * span_major_mm)
    return line_count, path_length


def _clipped_length(start: Point2, end: Point2, clip: Sequence[Polygon | Island]) -> float:
    split = split_line((start, end), clip, closed=False)
    if len(split) < 2:
        return 0.0
    length = 0.0
    for index in range(len(split) - 1):
        a = split[index]
        b = split[index + 1]
        if not a.clipped:
            continue
        seg = a.p.distance_to(b.p)
        if seg > EPSILON:
            length += seg
    return float(length)


def _bridge_span_metrics(island: Island) -> tuple[float, float, float]:
    bounds = island.bounds
    min_x = float(bounds.min_x)
    max_x = float(bounds.max_x)
    min_y = float(bounds.min_y)
    max_y = float(bounds.max_y)
    center_x = (min_x + max_x) * 0.5
    center_y = (min_y + max_y) * 0.5
    pad = 0.5

    horizontal = _clipped_length(
        Point2(min_x - pad, center_y),
        Point2(max_x + pad, center_y),
        [island],
    )
    vertical = _clipped_length(
        Point2(center_x, min_y - pad),
        Point2(center_x, max_y + pad),
        [island],
    )

    horizontal = horizontal if horizontal > EPSILON else max_x - min_x
    vertical = vertical if vertical > EPSILON else max_y - min_y

    if horizontal <= vertical:
        return (0.0, float(horizontal), max(EPSILON, max_y - min_y))
    return (90.0, float(vertical), max(EPSILON, max_x - min_x))


def _bridge_anchor_ratio(island: Island, angle_deg: float, support_clip: Sequence[Polygon], span_mm: float) -> float:
    if not support_clip or span_mm <= EPSILON:
        return 0.0

    bounds = island.bounds
    min_x = float(bounds.min_x)
    max_x = float(bounds.max_x)
    min_y = float(bounds.min_y)
    max_y = float(bounds.max_y)
    center_x = (min_x + max_x) * 0.5
    center_y = (min_y + max_y) * 0.5
    pad = 0.5

    if abs((angle_deg % 180.0) - 90.0) <= 45.0:
        start = Point2(center_x, min_y - pad)
        end = Point2(center_x, max_y + pad)
    else:
        start = Point2(min_x - pad, center_y)
        end = Point2(max_x + pad, center_y)
    supported_length = _clipped_length(start, end, support_clip)
    return max(0.0, min(1.0, float(supported_length / span_mm)))


def _bridge_support_clip(
    island: Island,
    lower_boundaries: Sequence[Polygon],
    extrusion_width_mm: float,
) -> list[Polygon]:
    if not lower_boundaries:
        return []
    expansion = max(0.2, extrusion_width_mm * 0.75)
    step = max(0.1, expansion * 0.5)
    try:
        params = RegionExpansionParameters.build(expansion, step, 4)
        expanded = propagate_waves_from_polygons([island.outer], lower_boundaries, params)
    except Exception:
        return list(lower_boundaries)
    if not expanded:
        return list(lower_boundaries)
    return [region.polygon for region in expanded]


def _coerce_layer_bool_map(values: Sequence[object]) -> dict[int, bool]:
    out: dict[int, bool] = {}
    for index, value in enumerate(values):
        out[int(index)] = bool(value)
    return out


def _coerce_layer_int_map(values: Sequence[object], *, minimum: int, fallback: int) -> dict[int, int]:
    out: dict[int, int] = {}
    for index, value in enumerate(values):
        parsed = fallback
        if isinstance(value, bool):
            parsed = fallback
        elif isinstance(value, int):
            parsed = int(value)
        elif isinstance(value, float):
            parsed = int(value)
        else:
            text = str(value).strip()
            if text:
                try:
                    parsed = int(float(text))
                except (TypeError, ValueError, OverflowError):
                    parsed = fallback
        out[int(index)] = max(minimum, parsed)
    return out


def _coerce_layer_float_map(values: Sequence[object], *, minimum: float, maximum: float, fallback: float) -> dict[int, float]:
    out: dict[int, float] = {}
    for index, value in enumerate(values):
        parsed = float(fallback)
        if isinstance(value, bool):
            parsed = float(fallback)
        elif isinstance(value, (int, float)):
            parsed = float(value)
        else:
            text = str(value).strip()
            if text:
                try:
                    parsed = float(text)
                except (TypeError, ValueError, OverflowError):
                    parsed = float(fallback)
        out[int(index)] = max(float(minimum), min(float(maximum), float(parsed)))
    return out


def _bridge_void_depth_layers(
    layer_index: int,
    *,
    infill_void_layers: dict[int, bool],
    infill_thickness_layers: dict[int, int],
    infill_void_depth_layers: dict[int, int] | None = None,
) -> int:
    if layer_index <= 0:
        return 1
    lower_layer = int(layer_index) - 1
    metadata_depth = 1
    if infill_void_depth_layers:
        metadata_depth = max(1, int(infill_void_depth_layers.get(lower_layer, 1)))
    if not infill_void_layers.get(lower_layer, False):
        return metadata_depth

    depth = max(1, int(infill_thickness_layers.get(lower_layer, 1)) - 1)
    depth = max(depth, metadata_depth)
    probe = lower_layer - 1
    while probe >= 0 and infill_void_layers.get(probe, False):
        depth += 1
        probe -= 1
    return max(1, depth)


def _bridge_support_coverage_scale(
    layer_index: int,
    *,
    infill_void_layers: dict[int, bool],
    infill_combined_into_layers: dict[int, int],
    infill_thickness_layers: dict[int, int],
    infill_surface_ratios: dict[int, float] | None = None,
) -> float:
    if layer_index <= 0:
        return 1.0
    lower_layer = int(layer_index) - 1
    metadata_scale = 1.0
    if infill_surface_ratios:
        metadata_scale = max(0.05, min(1.0, float(infill_surface_ratios.get(lower_layer, 1.0))))

    thickness = max(1, int(infill_thickness_layers.get(lower_layer, 1)))
    if infill_void_layers.get(lower_layer, False):
        base = max(0.05, min(0.35, 0.35 / thickness))
        return max(0.02, min(1.0, base * metadata_scale))

    combine_target = int(infill_combined_into_layers.get(lower_layer, lower_layer))
    if combine_target > lower_layer and thickness > 1:
        layer_gap = max(1, combine_target - lower_layer)
        attenuation = min(0.45, 0.1 * layer_gap)
        base = max(0.55, 1.0 - attenuation)
        return max(0.02, min(1.0, base * metadata_scale))
    return max(0.02, min(1.0, 1.0 * metadata_scale))


def _bridge_candidate_ratio_geometry(
    island: Island,
    support_clip: Sequence[Polygon],
    *,
    sample_count: int,
    support_coverage_scale: float,
) -> tuple[float, float]:
    island_area = max(0.0, float(island.area))
    if island_area <= EPSILON:
        return 0.0, 0.0
    if not support_clip:
        return 1.0, island_area

    coverage_scale = max(0.0, min(1.0, float(support_coverage_scale)))
    bounds = island.bounds
    min_x = float(bounds.min_x)
    max_x = float(bounds.max_x)
    min_y = float(bounds.min_y)
    max_y = float(bounds.max_y)
    span_x = max_x - min_x
    span_y = max_y - min_y
    if span_x <= EPSILON or span_y <= EPSILON:
        return 1.0, island_area

    pad = 0.5
    samples = max(3, int(sample_count))
    sampled_total = 0.0
    sampled_supported = 0.0
    for sample_index in range(samples):
        t = (sample_index + 0.5) / samples

        horizontal_y = min_y + (span_y * t)
        h_start = Point2(min_x - pad, horizontal_y)
        h_end = Point2(max_x + pad, horizontal_y)
        h_inside = _clipped_length(h_start, h_end, [island])
        if h_inside > EPSILON:
            sampled_total += h_inside
            supported_h = _clipped_length(h_start, h_end, support_clip) * coverage_scale
            sampled_supported += min(h_inside, max(0.0, supported_h))

        vertical_x = min_x + (span_x * t)
        v_start = Point2(vertical_x, min_y - pad)
        v_end = Point2(vertical_x, max_y + pad)
        v_inside = _clipped_length(v_start, v_end, [island])
        if v_inside > EPSILON:
            sampled_total += v_inside
            supported_v = _clipped_length(v_start, v_end, support_clip) * coverage_scale
            sampled_supported += min(v_inside, max(0.0, supported_v))

    if sampled_total <= EPSILON:
        unsupported_ratio = 1.0 - coverage_scale
    else:
        unsupported_ratio = 1.0 - (sampled_supported / sampled_total)
    unsupported_ratio = max(0.0, min(1.0, float(unsupported_ratio)))
    return unsupported_ratio, float(island_area * unsupported_ratio)


def _bridge_span_graph(
    *,
    layer_index: int,
    island_index: int,
    island: Island,
    support_clip: Sequence[Polygon],
    angle_deg: float,
    spacing_mm: float,
    sample_count: int,
    support_coverage_scale: float,
) -> tuple[list[BridgeSpanNode], list[BridgeSpanEdge], float, float]:
    bounds = island.bounds
    min_x = float(bounds.min_x)
    max_x = float(bounds.max_x)
    min_y = float(bounds.min_y)
    max_y = float(bounds.max_y)
    span_x = max_x - min_x
    span_y = max_y - min_y
    island_area = max(0.0, float(island.area))
    if span_x <= EPSILON or span_y <= EPSILON:
        return [], [], 0.0, island_area

    vertical = abs((_normalize_angle(angle_deg) % 180.0) - 90.0) <= 45.0
    span_minor = span_x if vertical else span_y
    span_major = span_y if vertical else span_x
    pad = max(0.5, float(spacing_mm))
    lines = max(1, int(max(sample_count, ceil(span_minor / max(spacing_mm, EPSILON)))))
    line_step = span_minor / float(lines)
    coverage_scale = max(0.0, min(1.0, float(support_coverage_scale)))

    nodes: list[BridgeSpanNode] = []
    total_supported = 0.0
    total_measured = 0.0
    for node_index in range(lines):
        offset_start = node_index * line_step
        offset_end = (node_index + 1) * line_step
        if vertical:
            x = min_x + ((node_index + 0.5) * line_step)
            start = Point2(x, min_y - pad)
            end = Point2(x, max_y + pad)
            center_x = x
            center_y = (min_y + max_y) * 0.5
        else:
            y = min_y + ((node_index + 0.5) * line_step)
            start = Point2(min_x - pad, y)
            end = Point2(max_x + pad, y)
            center_x = (min_x + max_x) * 0.5
            center_y = y

        inside_length = _clipped_length(start, end, [island])
        if inside_length <= EPSILON:
            continue
        supported_length = _clipped_length(start, end, support_clip) * coverage_scale
        supported_length = max(0.0, min(inside_length, supported_length))
        support_ratio = max(0.0, min(1.0, supported_length / inside_length))
        candidate_ratio = 1.0 - support_ratio
        node_path_count = 1 if candidate_ratio > EPSILON else 0
        node_path_length = float(inside_length * candidate_ratio)

        nodes.append(
            BridgeSpanNode(
                layer_index=layer_index,
                island_index=island_index,
                node_index=len(nodes),
                offset_start_mm=float(offset_start),
                offset_end_mm=float(offset_end),
                span_length_mm=float(inside_length),
                center_x_mm=float(center_x),
                center_y_mm=float(center_y),
                support_ratio=float(support_ratio),
                candidate_ratio=float(candidate_ratio),
                path_count=node_path_count,
                path_length_mm=node_path_length,
                line_start_x_mm=float(start.x),
                line_start_y_mm=float(start.y),
                line_end_x_mm=float(end.x),
                line_end_y_mm=float(end.y),
            )
        )
        total_supported += supported_length
        total_measured += inside_length

    edges: list[BridgeSpanEdge] = []
    for index in range(len(nodes) - 1):
        src = nodes[index]
        dst = nodes[index + 1]
        continuity = 1.0 - abs(src.candidate_ratio - dst.candidate_ratio)
        shared = min(src.candidate_ratio, dst.candidate_ratio)
        strip_overlap, strip_intersection_length, strip_alignment = _bridge_edge_strip_metrics(
            node_a=src,
            island_a=island,
            node_b=dst,
            island_b=island,
        )
        strip_intersection_ratio = max(
            0.0,
            min(
                1.0,
                float(strip_intersection_length / max(EPSILON, min(src.span_length_mm, dst.span_length_mm))),
            ),
        )
        direction_weight = max(
            0.0,
            min(
                1.0,
                float(
                    (0.48 * (1.0 - (abs(src.candidate_ratio - dst.candidate_ratio) * 0.6)))
                    + (0.30 * strip_alignment)
                    + (0.22 * strip_intersection_ratio)
                ),
            ),
        )
        graph_weight = max(
            0.0,
            min(
                1.0,
                float(
                    (0.38 * continuity)
                    + (0.21 * shared)
                    + (0.18 * strip_overlap)
                    + (0.12 * strip_intersection_ratio)
                    + (0.11 * direction_weight)
                ),
            ),
        )
        edges.append(
            BridgeSpanEdge(
                layer_index=layer_index,
                island_index=island_index,
                src_node_index=int(src.node_index),
                dst_node_index=int(dst.node_index),
                continuity_ratio=max(0.0, min(1.0, float(continuity))),
                shared_candidate_ratio=max(0.0, min(1.0, float(shared))),
                strip_overlap_ratio=max(0.0, min(1.0, float(strip_overlap))),
                strip_intersection_length_mm=float(max(0.0, strip_intersection_length)),
                strip_alignment_ratio=float(max(0.0, min(1.0, strip_alignment))),
                direction_weight=float(direction_weight),
                graph_weight=float(graph_weight),
            )
        )

    support_surface_ratio = (total_supported / total_measured) if total_measured > EPSILON else 0.0
    support_surface_ratio = max(0.0, min(1.0, float(support_surface_ratio)))
    unsupported_surface_area = float(island_area * (1.0 - support_surface_ratio))
    return nodes, edges, support_surface_ratio, unsupported_surface_area


def _bridge_angle_distance_deg(angle_a_deg: float, angle_b_deg: float) -> float:
    a = _normalize_angle(angle_a_deg) % 180.0
    b = _normalize_angle(angle_b_deg) % 180.0
    delta = abs(a - b)
    return min(delta, 180.0 - delta)


def _bridge_node_line(node: BridgeSpanNode) -> tuple[Point2, Point2]:
    return (
        Point2(float(node.line_start_x_mm), float(node.line_start_y_mm)),
        Point2(float(node.line_end_x_mm), float(node.line_end_y_mm)),
    )


def _bridge_node_angle_deg(node: BridgeSpanNode, fallback_angle_deg: float) -> float:
    start, end = _bridge_node_line(node)
    dx = float(end.x - start.x)
    dy = float(end.y - start.y)
    if hypot(dx, dy) <= EPSILON:
        return _normalize_angle(fallback_angle_deg)
    return _normalize_angle(degrees(atan2(dy, dx)))


def _bridge_orientation_vote_from_nodes(
    nodes: Sequence[dict[str, object]],
    edge_refs: Sequence[dict[str, object]] = (),
) -> tuple[float, float, float]:
    vote_x = 0.0
    vote_y = 0.0
    vote_weight = 0.0
    for ref in nodes:
        node = ref.get("node")
        if not isinstance(node, BridgeSpanNode):
            continue
        path_length = max(EPSILON, float(ref.get("path_length_mm", 0.0)))
        span_length = max(EPSILON, float(ref.get("span_length_mm", 0.0)))
        candidate_ratio = max(0.0, min(1.0, float(ref.get("candidate_ratio", 0.0))))
        support_ratio = max(0.0, min(1.0, float(node.support_ratio)))
        weight = path_length * max(0.25, candidate_ratio) * max(0.2, support_ratio + 0.15) * max(0.2, span_length)
        angle = _bridge_node_angle_deg(node, float(ref.get("angle_deg", 0.0))) % 180.0
        theta = radians(angle * 2.0)
        vote_x += cos(theta) * weight
        vote_y += sin(theta) * weight
        vote_weight += weight
    for edge_ref in edge_refs:
        src = edge_ref.get("src")
        dst = edge_ref.get("dst")
        metrics = edge_ref.get("metrics")
        if not isinstance(src, dict) or not isinstance(dst, dict) or not isinstance(metrics, dict):
            continue
        src_node = src.get("node")
        dst_node = dst.get("node")
        if not isinstance(src_node, BridgeSpanNode) or not isinstance(dst_node, BridgeSpanNode):
            continue
        src_angle = _bridge_node_angle_deg(src_node, float(src.get("angle_deg", 0.0)))
        dst_angle = _bridge_node_angle_deg(dst_node, float(dst.get("angle_deg", 0.0)))
        edge_angle = _normalize_angle((src_angle + dst_angle) * 0.5) % 180.0
        graph_weight = max(0.0, min(1.0, float(metrics.get("graph_weight", 0.0))))
        strip_overlap = max(0.0, min(1.0, float(metrics.get("strip_overlap_ratio", 0.0))))
        strip_alignment = max(0.0, min(1.0, float(metrics.get("strip_alignment_ratio", 0.0))))
        strip_intersection_length = max(0.0, float(metrics.get("strip_intersection_length_mm", 0.0)))
        edge_weight = (
            graph_weight
            * max(0.15, strip_overlap)
            * max(0.15, strip_alignment)
            * max(0.2, strip_intersection_length)
        )
        theta = radians(edge_angle * 2.0)
        vote_x += cos(theta) * edge_weight
        vote_y += sin(theta) * edge_weight
        vote_weight += edge_weight
    if vote_weight <= EPSILON:
        return 0.0, 0.0, 0.0
    dominant = 0.5 * degrees(atan2(vote_y, vote_x))
    dominant = _normalize_angle(dominant)
    if dominant >= 180.0:
        dominant -= 180.0
    confidence = max(0.0, min(1.0, float(hypot(vote_x, vote_y) / vote_weight)))
    return float(dominant), float(confidence), float(vote_weight)


def _bridge_edge_strip_metrics(
    *,
    node_a: BridgeSpanNode,
    island_a: Island,
    node_b: BridgeSpanNode,
    island_b: Island,
) -> tuple[float, float, float]:
    a_start, a_end = _bridge_node_line(node_a)
    b_start, b_end = _bridge_node_line(node_b)

    def _expanded_line(start: Point2, end: Point2, extension_mm: float) -> tuple[Point2, Point2]:
        dx = float(end.x - start.x)
        dy = float(end.y - start.y)
        length = hypot(dx, dy)
        if length <= EPSILON:
            return start, end
        ux = dx / length
        uy = dy / length
        return (
            Point2(float(start.x - (ux * extension_mm)), float(start.y - (uy * extension_mm))),
            Point2(float(end.x + (ux * extension_mm)), float(end.y + (uy * extension_mm))),
        )

    extension = max(1.0, max(float(node_a.span_length_mm), float(node_b.span_length_mm)) * 2.5)
    a_start, a_end = _expanded_line(a_start, a_end, extension)
    b_start, b_end = _expanded_line(b_start, b_end, extension)

    inside_a = max(EPSILON, float(node_a.span_length_mm))
    inside_b = max(EPSILON, float(node_b.span_length_mm))
    a_against_b = _clipped_length(a_start, a_end, [island_b])
    b_against_a = _clipped_length(b_start, b_end, [island_a])
    intersection_length = max(0.0, float((a_against_b + b_against_a) * 0.5))
    overlap_a = max(0.0, min(1.0, float(a_against_b / inside_a)))
    overlap_b = max(0.0, min(1.0, float(b_against_a / inside_b)))
    overlap_ratio = max(0.0, min(1.0, float((overlap_a + overlap_b) * 0.5)))

    a_dir_x = float(node_a.line_end_x_mm - node_a.line_start_x_mm)
    a_dir_y = float(node_a.line_end_y_mm - node_a.line_start_y_mm)
    b_dir_x = float(node_b.line_end_x_mm - node_b.line_start_x_mm)
    b_dir_y = float(node_b.line_end_y_mm - node_b.line_start_y_mm)
    a_len = hypot(a_dir_x, a_dir_y)
    b_len = hypot(b_dir_x, b_dir_y)
    if a_len > EPSILON and b_len > EPSILON:
        direction_dot = ((a_dir_x * b_dir_x) + (a_dir_y * b_dir_y)) / (a_len * b_len)
        direction_dot = max(-1.0, min(1.0, float(direction_dot)))
        direction_alignment = abs(float(direction_dot))
    else:
        direction_alignment = 1.0

    if a_len > EPSILON:
        unit_x = a_dir_x / a_len
        unit_y = a_dir_y / a_len
    elif b_len > EPSILON:
        unit_x = b_dir_x / b_len
        unit_y = b_dir_y / b_len
    else:
        unit_x = 1.0
        unit_y = 0.0
    normal_x = -unit_y
    normal_y = unit_x
    center_dx = float(node_a.center_x_mm - node_b.center_x_mm)
    center_dy = float(node_a.center_y_mm - node_b.center_y_mm)
    lateral_gap = abs((center_dx * normal_x) + (center_dy * normal_y))
    parallel_gap = abs((center_dx * unit_x) + (center_dy * unit_y))
    min_span = max(EPSILON, min(inside_a, inside_b))
    max_span = max(EPSILON, max(inside_a, inside_b))
    lateral_ratio = max(0.0, min(1.0, float(1.0 - (lateral_gap / max(0.5, min_span * 0.4)))))
    parallel_ratio = max(0.0, min(1.0, float(1.0 - (parallel_gap / max(0.5, max_span * 1.15)))))
    strip_alignment = max(
        0.0,
        min(
            1.0,
            float((0.55 * direction_alignment) + (0.25 * lateral_ratio) + (0.20 * parallel_ratio)),
        ),
    )
    return float(overlap_ratio), float(intersection_length), float(strip_alignment)


def _bridge_strip_overlap_ratio(
    *,
    node_a: BridgeSpanNode,
    island_a: Island,
    node_b: BridgeSpanNode,
    island_b: Island,
) -> float:
    overlap_ratio, _intersection_length, _strip_alignment = _bridge_edge_strip_metrics(
        node_a=node_a,
        island_a=island_a,
        node_b=node_b,
        island_b=island_b,
    )
    return float(overlap_ratio)


def _build_bridge_span_components(
    *,
    layer_index: int,
    bridge_regions: Sequence[BridgeRegionPlan],
    layer_islands: Sequence[Island],
    extrusion_width_mm: float,
) -> tuple[list[BridgeSpanComponent], int]:
    regions = list(bridge_regions)
    if not regions:
        return [], 0

    island_lookup: dict[int, Island] = {index: island for index, island in enumerate(layer_islands)}
    node_refs: list[dict[str, object]] = []
    key_to_global: dict[tuple[int, int], int] = {}
    region_to_nodes: dict[int, list[int]] = {}
    for region_index, region in enumerate(regions):
        local_nodes: list[int] = []
        for node in region.span_nodes:
            if node.path_length_mm <= EPSILON or node.candidate_ratio <= EPSILON:
                continue
            global_index = len(node_refs)
            key_to_global[(region_index, int(node.node_index))] = global_index
            node_refs.append(
                {
                    "region_index": int(region_index),
                    "island_index": int(region.island_index),
                    "node_index": int(node.node_index),
                    "x_mm": float(node.center_x_mm),
                    "y_mm": float(node.center_y_mm),
                    "candidate_ratio": float(node.candidate_ratio),
                    "span_length_mm": float(node.span_length_mm),
                    "path_length_mm": float(node.path_length_mm),
                    "angle_deg": float(region.angle_deg),
                    "node": node,
                }
            )
            local_nodes.append(global_index)
        if local_nodes:
            region_to_nodes[int(region_index)] = local_nodes

    components: list[BridgeSpanComponent] = []
    if not node_refs:
        component_id = 1
        for region in regions:
            components.append(
                BridgeSpanComponent(
                    layer_index=int(layer_index),
                    component_id=component_id,
                    island_indices=[int(region.island_index)],
                    region_count=1,
                    node_count=0,
                    edge_count=0,
                    inter_island_edge_count=0,
                    candidate_ratio=float(region.candidate_ratio),
                    candidate_area_mm2=float(region.candidate_area_mm2),
                    path_count=int(region.path_count),
                    path_length_mm=float(region.path_length_mm),
                    connectivity_weight=0.0,
                    strip_overlap_ratio=0.0,
                    strip_intersection_length_mm=0.0,
                    direction_alignment_ratio=0.0,
                    dominant_angle_deg=float(_normalize_angle(region.angle_deg) % 180.0),
                    dominant_angle_confidence=0.0,
                    direction_vote_weight=0.0,
                )
            )
            region.span_component_id = int(component_id)
            region.span_component_region_count = 1
            region.span_component_node_count = 0
            region.span_component_inter_island_edge_count = 0
            region.direction_vote_angle_deg = float(_normalize_angle(region.angle_deg))
            region.direction_vote_confidence = 0.0
            component_id += 1
        return components, 0

    edges: dict[tuple[int, int], dict[str, object]] = {}
    for region_index, region in enumerate(regions):
        for edge in region.span_edges:
            src = key_to_global.get((region_index, int(edge.src_node_index)))
            dst = key_to_global.get((region_index, int(edge.dst_node_index)))
            if src is None or dst is None or src == dst:
                continue
            pair = (src, dst) if src < dst else (dst, src)
            continuity = max(0.0, min(1.0, float(edge.continuity_ratio)))
            shared = max(0.0, min(1.0, float(edge.shared_candidate_ratio)))
            strip_overlap = max(0.0, min(1.0, float(edge.strip_overlap_ratio)))
            strip_intersection_length = max(0.0, float(edge.strip_intersection_length_mm))
            strip_alignment = max(0.0, min(1.0, float(edge.strip_alignment_ratio)))
            direction_weight = max(0.0, min(1.0, float(edge.direction_weight)))
            graph_weight = float(edge.graph_weight)
            if graph_weight <= EPSILON:
                strip_intersection_ratio = max(
                    0.0,
                    min(
                        1.0,
                        float(
                            strip_intersection_length
                            / max(EPSILON, min(float(node_refs[src]["span_length_mm"]), float(node_refs[dst]["span_length_mm"])))
                        ),
                    ),
                )
                graph_weight = (
                    (0.38 * continuity)
                    + (0.21 * shared)
                    + (0.18 * strip_overlap)
                    + (0.12 * strip_intersection_ratio)
                    + (0.11 * direction_weight)
                )
            graph_weight = max(0.0, min(1.0, float(graph_weight)))
            previous = edges.get(pair)
            if previous is None or graph_weight > float(previous["graph_weight"]):
                edges[pair] = {
                    "graph_weight": float(graph_weight),
                    "strip_overlap_ratio": float(strip_overlap),
                    "strip_intersection_length_mm": float(strip_intersection_length),
                    "strip_alignment_ratio": float(strip_alignment),
                    "direction_weight": float(direction_weight),
                    "inter_island": False,
                }

    merge_distance = max(0.8, float(extrusion_width_mm) * 3.0)
    for src_index in range(len(node_refs)):
        src = node_refs[src_index]
        for dst_index in range(src_index + 1, len(node_refs)):
            dst = node_refs[dst_index]
            if int(src["region_index"]) == int(dst["region_index"]):
                continue
            angle_delta = _bridge_angle_distance_deg(float(src["angle_deg"]), float(dst["angle_deg"]))
            if angle_delta > 95.0:
                continue
            candidate_gap = abs(float(src["candidate_ratio"]) - float(dst["candidate_ratio"]))
            if candidate_gap > 0.6:
                continue
            src_island_index = int(src["island_index"])
            dst_island_index = int(dst["island_index"])
            src_island = island_lookup.get(src_island_index)
            dst_island = island_lookup.get(dst_island_index)
            if src_island is None or dst_island is None:
                continue
            src_node = src["node"]
            dst_node = dst["node"]
            if not isinstance(src_node, BridgeSpanNode) or not isinstance(dst_node, BridgeSpanNode):
                continue
            strip_overlap, strip_intersection_length, strip_alignment = _bridge_edge_strip_metrics(
                node_a=src_node,
                island_a=src_island,
                node_b=dst_node,
                island_b=dst_island,
            )
            if strip_overlap <= 0.02:
                continue
            horizontal_bridge = abs((_normalize_angle(float(src["angle_deg"])) % 180.0) - 90.0) > 45.0
            if horizontal_bridge:
                parallel_delta = abs(float(src["x_mm"]) - float(dst["x_mm"]))
                orthogonal_delta = abs(float(src["y_mm"]) - float(dst["y_mm"]))
            else:
                parallel_delta = abs(float(src["y_mm"]) - float(dst["y_mm"]))
                orthogonal_delta = abs(float(src["x_mm"]) - float(dst["x_mm"]))
            orthogonal_limit = max(
                merge_distance * (0.55 + (strip_overlap * 0.9)),
                min(float(src["span_length_mm"]), float(dst["span_length_mm"])) * (0.15 + (strip_overlap * 0.2)),
            )
            parallel_limit = max(
                merge_distance * (1.2 + strip_overlap),
                min(float(src["span_length_mm"]), float(dst["span_length_mm"])) * (0.9 + (0.55 * strip_overlap)),
            )
            if orthogonal_delta > orthogonal_limit or parallel_delta > parallel_limit:
                continue
            distance = hypot(float(src["x_mm"]) - float(dst["x_mm"]), float(src["y_mm"]) - float(dst["y_mm"]))
            if distance > (parallel_limit + orthogonal_limit):
                continue
            angle_alignment = max(0.0, min(1.0, float(1.0 - (angle_delta / 90.0))))
            direction_alignment = max(
                0.0,
                min(1.0, float((0.58 * angle_alignment) + (0.42 * strip_alignment))),
            )
            continuity = max(0.0, min(1.0, float(1.0 - candidate_gap)))
            strip_intersection_ratio = max(
                0.0,
                min(
                    1.0,
                    float(
                        strip_intersection_length
                        / max(EPSILON, min(float(src["span_length_mm"]), float(dst["span_length_mm"])))
                    ),
                ),
            )
            graph_weight = float(
                (0.34 * strip_overlap)
                + (0.19 * strip_intersection_ratio)
                + (0.20 * direction_alignment)
                + (0.18 * continuity)
                + (0.09 * max(0.0, min(1.0, float(1.0 - (distance / max(parallel_limit + orthogonal_limit, EPSILON))))))
            )
            if graph_weight <= 0.08:
                continue
            pair = (src_index, dst_index) if src_index < dst_index else (dst_index, src_index)
            previous = edges.get(pair)
            graph_weight = max(0.0, min(1.0, graph_weight))
            if previous is None or graph_weight > float(previous["graph_weight"]):
                edges[pair] = {
                    "graph_weight": float(graph_weight),
                    "strip_overlap_ratio": float(max(0.0, min(1.0, strip_overlap))),
                    "strip_intersection_length_mm": float(max(0.0, strip_intersection_length)),
                    "strip_alignment_ratio": float(max(0.0, min(1.0, strip_alignment))),
                    "direction_weight": float(max(0.0, min(1.0, direction_alignment))),
                    "inter_island": bool(src_island_index != dst_island_index),
                }

    adjacency: dict[int, list[int]] = {}
    for src, dst in edges.keys():
        adjacency.setdefault(src, []).append(dst)
        adjacency.setdefault(dst, []).append(src)

    node_component_id: dict[int, int] = {}
    component_id = 1
    for start_index in range(len(node_refs)):
        if start_index in node_component_id:
            continue
        stack = [start_index]
        visited_nodes: list[int] = []
        while stack:
            current = stack.pop()
            if current in node_component_id:
                continue
            node_component_id[current] = int(component_id)
            visited_nodes.append(current)
            for neighbor in adjacency.get(current, ()):
                if neighbor not in node_component_id:
                    stack.append(neighbor)

        node_set = set(visited_nodes)
        region_indices: set[int] = set()
        island_indices: set[int] = set()
        weighted_candidate = 0.0
        weighted_length = 0.0
        path_count = 0
        path_length = 0.0
        for node_idx in visited_nodes:
            ref = node_refs[node_idx]
            region_indices.add(int(ref["region_index"]))
            island_indices.add(int(ref["island_index"]))
            length_mm = max(EPSILON, float(ref["path_length_mm"]))
            weighted_candidate += float(ref["candidate_ratio"]) * length_mm
            weighted_length += length_mm
            path_count += 1
            path_length += float(ref["path_length_mm"])

        edge_count = 0
        inter_island_edge_count = 0
        connectivity_acc = 0.0
        strip_acc = 0.0
        strip_intersection_acc = 0.0
        direction_acc = 0.0
        edge_refs: list[dict[str, object]] = []
        for src, dst in edges.keys():
            if src not in node_set or dst not in node_set:
                continue
            edge_count += 1
            src_island = int(node_refs[src]["island_index"])
            dst_island = int(node_refs[dst]["island_index"])
            if src_island != dst_island:
                inter_island_edge_count += 1
            metrics = edges[(src, dst)]
            connectivity_acc += float(metrics["graph_weight"])
            strip_acc += float(metrics["strip_overlap_ratio"])
            strip_intersection_acc += float(metrics["strip_intersection_length_mm"])
            direction_acc += float(metrics["direction_weight"])
            edge_refs.append(
                {
                    "src": node_refs[src],
                    "dst": node_refs[dst],
                    "metrics": metrics,
                }
            )

        candidate_area_mm2 = float(sum(regions[idx].candidate_area_mm2 for idx in sorted(region_indices)))
        component_refs = [node_refs[idx] for idx in visited_nodes]
        dominant_angle_deg, dominant_confidence, direction_vote_weight = _bridge_orientation_vote_from_nodes(
            component_refs,
            edge_refs=edge_refs,
        )
        components.append(
            BridgeSpanComponent(
                layer_index=int(layer_index),
                component_id=int(component_id),
                island_indices=sorted(island_indices),
                region_count=len(region_indices),
                node_count=len(visited_nodes),
                edge_count=int(edge_count),
                inter_island_edge_count=int(inter_island_edge_count),
                candidate_ratio=float(weighted_candidate / weighted_length) if weighted_length > EPSILON else 0.0,
                candidate_area_mm2=float(candidate_area_mm2),
                path_count=int(path_count),
                path_length_mm=float(path_length),
                connectivity_weight=float(connectivity_acc / edge_count) if edge_count > 0 else 0.0,
                strip_overlap_ratio=float(strip_acc / edge_count) if edge_count > 0 else 0.0,
                strip_intersection_length_mm=float(strip_intersection_acc),
                direction_alignment_ratio=float(direction_acc / edge_count) if edge_count > 0 else 0.0,
                dominant_angle_deg=float(dominant_angle_deg),
                dominant_angle_confidence=float(dominant_confidence),
                direction_vote_weight=float(direction_vote_weight),
            )
        )
        component_id += 1

    component_by_id: dict[int, BridgeSpanComponent] = {item.component_id: item for item in components}
    for region_index, region in enumerate(regions):
        component_votes: dict[int, int] = {}
        for node_idx in region_to_nodes.get(region_index, ()):
            vote_component_id = node_component_id.get(node_idx)
            if vote_component_id is None:
                continue
            component_votes[vote_component_id] = component_votes.get(vote_component_id, 0) + 1
        if component_votes:
            ordered = sorted(component_votes.items(), key=lambda item: (-item[1], item[0]))
            chosen_component = int(ordered[0][0])
        else:
            chosen_component = int(component_id)
            fallback = BridgeSpanComponent(
                layer_index=int(layer_index),
                component_id=chosen_component,
                island_indices=[int(region.island_index)],
                region_count=1,
                node_count=0,
                edge_count=0,
                inter_island_edge_count=0,
                candidate_ratio=float(region.candidate_ratio),
                candidate_area_mm2=float(region.candidate_area_mm2),
                path_count=int(region.path_count),
                path_length_mm=float(region.path_length_mm),
                connectivity_weight=0.0,
                strip_overlap_ratio=0.0,
                strip_intersection_length_mm=0.0,
                direction_alignment_ratio=0.0,
                dominant_angle_deg=float(_normalize_angle(region.angle_deg) % 180.0),
                dominant_angle_confidence=0.0,
                direction_vote_weight=0.0,
            )
            components.append(fallback)
            component_by_id[chosen_component] = fallback
            component_id += 1
        metadata = component_by_id[chosen_component]
        region.span_component_id = int(chosen_component)
        region.span_component_region_count = int(metadata.region_count)
        region.span_component_node_count = int(metadata.node_count)
        region.span_component_inter_island_edge_count = int(metadata.inter_island_edge_count)
        region.direction_vote_angle_deg = float(metadata.dominant_angle_deg)
        region.direction_vote_confidence = float(metadata.dominant_angle_confidence)

    components.sort(key=lambda item: int(item.component_id))
    inter_island_edges_total = sum(item.inter_island_edge_count for item in components)
    return components, int(inter_island_edges_total)


def _bridge_region_estimate(
    *,
    layer_index: int,
    island_index: int,
    island: Island,
    support_clip: Sequence[Polygon],
    extrusion_width_mm: float,
    bridge_flow_ratio: float,
    bridge_density_ratio: float,
    candidate_ratio: float,
    candidate_area_mm2: float,
    candidate_depth_layers: int = 1,
    min_candidate_ratio: float = 0.0,
    support_surface_ratio: float = 0.0,
    unsupported_surface_area_mm2: float = 0.0,
    span_nodes: Sequence[BridgeSpanNode] = (),
    span_edges: Sequence[BridgeSpanEdge] = (),
    preferred_angle_deg: float | None = None,
    angle_source: str = "local",
    thick_bridge: bool = False,
) -> BridgeRegionPlan:
    angle_deg, bridge_span_mm, sweep_span_mm = _bridge_span_metrics(island)
    if preferred_angle_deg is not None:
        angle_deg = _normalize_angle(preferred_angle_deg)
    anchor_ratio = _bridge_anchor_ratio(island, angle_deg, support_clip, bridge_span_mm)
    normalized_candidate_ratio = max(0.0, min(1.0, float(candidate_ratio)))
    normalized_candidate_area = max(0.0, float(candidate_area_mm2))
    candidate_depth = max(1, int(candidate_depth_layers))
    surface_support_ratio = max(0.0, min(1.0, float(support_surface_ratio)))
    unsupported_surface_area = max(0.0, float(unsupported_surface_area_mm2))
    span_nodes_list = list(span_nodes)
    span_edges_list = list(span_edges)
    min_ratio = max(0.0, min(1.0, float(min_candidate_ratio)))
    if bridge_density_ratio <= EPSILON or normalized_candidate_ratio < min_ratio:
        return BridgeRegionPlan(
            layer_index=layer_index,
            island_index=island_index,
            angle_deg=angle_deg,
            path_count=0,
            path_length_mm=0.0,
            span_major_mm=sweep_span_mm,
            span_minor_mm=bridge_span_mm,
            anchor_ratio=float(anchor_ratio),
            candidate_ratio=normalized_candidate_ratio,
            candidate_area_mm2=normalized_candidate_area,
            candidate_depth_layers=candidate_depth,
            support_surface_ratio=surface_support_ratio,
            unsupported_surface_area_mm2=unsupported_surface_area,
            direction_angle_source=str(angle_source),
            span_nodes=span_nodes_list,
            span_edges=span_edges_list,
        )
    width_scale = 1.25 if thick_bridge else 1.0
    effective_width = extrusion_width_mm * max(0.25, bridge_flow_ratio) * width_scale
    span_ratio = normalized_candidate_ratio
    if span_nodes_list:
        weighted_sum = sum(node.candidate_ratio * max(node.span_length_mm, EPSILON) for node in span_nodes_list)
        weighted_len = sum(max(node.span_length_mm, EPSILON) for node in span_nodes_list)
        if weighted_len > EPSILON:
            span_ratio = max(0.0, min(1.0, weighted_sum / weighted_len))
    effective_density = max(0.05, min(2.0, float(bridge_density_ratio))) * max(0.05, span_ratio)
    depth_boost = 1.0 + (0.08 * max(0, candidate_depth - 1))
    line_count = max(1, int(ceil((sweep_span_mm / effective_width) * effective_density * depth_boost)))
    stretch = 1.05 + ((1.0 - anchor_ratio) * 0.15)
    path_length = float(line_count * bridge_span_mm * stretch * max(0.25, span_ratio))
    return BridgeRegionPlan(
        layer_index=layer_index,
        island_index=island_index,
        angle_deg=angle_deg,
        path_count=line_count,
        path_length_mm=path_length,
        span_major_mm=sweep_span_mm,
        span_minor_mm=bridge_span_mm,
        anchor_ratio=float(anchor_ratio),
        candidate_ratio=normalized_candidate_ratio,
        candidate_area_mm2=normalized_candidate_area,
        candidate_depth_layers=candidate_depth,
        support_surface_ratio=surface_support_ratio,
        unsupported_surface_area_mm2=unsupported_surface_area,
        direction_angle_source=str(angle_source),
        span_nodes=span_nodes_list,
        span_edges=span_edges_list,
    )


def build_solid_layers_and_bridges(
    layer_graphs: Sequence[LayerIslandGraph],
    *,
    vertical_edges: Sequence[VerticalAdjacencyEdge] = (),
    top_layers: int,
    bottom_layers: int,
    extrusion_width_mm: float,
    bridge_enabled: bool,
    bridge_flow_ratio: float = 1.0,
    bridge_speed_ratio: float = 0.8,
    bridge_density_percent: float = 100.0,
    internal_bridge_flow_ratio: float = 1.0,
    internal_bridge_density_percent: float = 100.0,
    internal_bridge_angle_deg: float = 0.0,
    thick_bridges: bool = False,
    thick_internal_bridges: bool = False,
    extra_bridge_layer_enabled: bool = False,
    bridge_over_infill_enabled: bool = True,
    bridge_over_infill_min_candidate_ratio: float = 0.05,
    bridge_over_infill_sample_count: int = 7,
    layer_infill_void_flags: Sequence[bool] = (),
    layer_infill_void_depth_layers: Sequence[int] = (),
    layer_infill_combined_into_layers: Sequence[int] = (),
    layer_infill_thickness_layers: Sequence[int] = (),
    layer_infill_support_surface_ratios: Sequence[float] = (),
    layer_anchor_angles_deg: Sequence[float] = (),
    max_workers: int = 1,
) -> tuple[list[SolidLayerPlan], SolidBridgeReport]:
    graphs = _validate_layer_graphs(layer_graphs)
    edges = _validate_vertical_edges(vertical_edges)
    top_count = _validate_layers_count(top_layers, "top")
    bottom_count = _validate_layers_count(bottom_layers, "bottom")
    width = _validate_width(extrusion_width_mm)
    flow_ratio = _validate_ratio(bridge_flow_ratio, "SOLID_BRIDGE_FLOW_RATIO_INVALID", 0.2, 3.0)
    speed_ratio = _validate_ratio(bridge_speed_ratio, "SOLID_BRIDGE_SPEED_RATIO_INVALID", 0.1, 3.0)
    density_ratio = _validate_ratio(bridge_density_percent / 100.0, "SOLID_BRIDGE_DENSITY_INVALID", 0.0, 2.0)
    internal_flow = _validate_ratio(internal_bridge_flow_ratio, "SOLID_INTERNAL_BRIDGE_FLOW_RATIO_INVALID", 0.2, 3.0)
    internal_density = _validate_ratio(
        internal_bridge_density_percent / 100.0,
        "SOLID_INTERNAL_BRIDGE_DENSITY_INVALID",
        0.0,
        2.0,
    )
    internal_angle = _validate_ratio(internal_bridge_angle_deg, "SOLID_INTERNAL_BRIDGE_ANGLE_INVALID", 0.0, 360.0)
    candidate_min_ratio = _validate_ratio(
        bridge_over_infill_min_candidate_ratio,
        "SOLID_BRIDGE_CANDIDATE_RATIO_INVALID",
        0.0,
        1.0,
    )
    candidate_sample_count = _validate_sample_count(
        bridge_over_infill_sample_count,
        "SOLID_BRIDGE_CANDIDATE_SAMPLE_COUNT_INVALID",
        1,
        128,
    )

    warnings: list[str] = []
    if not graphs:
        warnings.append("solid_bridges:no_layers")

    if top_count + bottom_count > len(graphs) and len(graphs) > 0:
        warnings.append("solid_bridges:top_bottom_overlap")

    supported_map = _supported_islands_by_layer(edges)
    graph_lookup = _layer_lookup(graphs)
    anchor_lookup: dict[int, float] = {}
    for index, value in enumerate(layer_anchor_angles_deg):
        anchor_lookup[int(index)] = _normalize_angle(float(value))
    if layer_anchor_angles_deg:
        warnings.append("solid_bridges:anchor_guided_direction")

    infill_void_lookup = _coerce_layer_bool_map(layer_infill_void_flags)
    infill_void_depth_lookup = _coerce_layer_int_map(
        layer_infill_void_depth_layers,
        minimum=1,
        fallback=1,
    )
    infill_combined_into_lookup = _coerce_layer_int_map(
        layer_infill_combined_into_layers,
        minimum=0,
        fallback=0,
    )
    infill_thickness_lookup = _coerce_layer_int_map(
        layer_infill_thickness_layers,
        minimum=1,
        fallback=1,
    )
    infill_surface_ratio_lookup = _coerce_layer_float_map(
        layer_infill_support_surface_ratios,
        minimum=0.0,
        maximum=1.0,
        fallback=1.0,
    )
    if infill_void_lookup:
        warnings.append("solid_bridges:combine_infill_metadata_consumed")
    if infill_surface_ratio_lookup:
        warnings.append("solid_bridges:infill_support_surface_metadata_consumed")
    if bridge_over_infill_enabled:
        warnings.append("solid_bridges:bridge_over_infill_candidate_split")

    layer_count = len(graphs)
    def _build_layer(graph: LayerIslandGraph) -> tuple[SolidLayerPlan, list[str]]:
        layer_warnings: list[str] = []
        classification = _layer_classification(graph.layer_index, layer_count, bottom_count, top_count)
        if classification not in ALLOWED_SOLID_CLASSES:
            raise SlicerV2SolidBridgeError(f"SOLID_BRIDGE_CLASSIFICATION_INVALID:{classification}")

        is_solid = classification in {SOLID_CLASS_BOTTOM, SOLID_CLASS_TOP}

        solid_path_count = 0
        solid_path_length = 0.0
        bridge_regions: list[BridgeRegionPlan] = []
        bridge_region_contexts: list[dict[str, object]] = []
        supported_islands = supported_map.get(graph.layer_index, set())
        lower_graph = graph_lookup.get(int(graph.layer_index) - 1)
        lower_boundaries: list[Polygon] = [island.outer for island in lower_graph.islands] if lower_graph is not None else []
        layer_anchor_angle = anchor_lookup.get(int(graph.layer_index) - 1)

        for island_index, island in enumerate(graph.islands):
            span_major = max(float(island.bounds.width), float(island.bounds.height))
            span_minor = min(float(island.bounds.width), float(island.bounds.height))
            if span_major <= EPSILON or span_minor <= EPSILON:
                layer_warnings.append(f"layer_{graph.layer_index}:island_{island_index}:degenerate_bounds")
                continue

            if is_solid:
                paths, length = _solid_path_estimate(span_major, span_minor, width)
                solid_path_count += paths
                solid_path_length += length

            layer_index = int(graph.layer_index)
            anchor_angle = layer_anchor_angle
            unsupported_by_adjacency = island_index not in supported_islands
            support_clip: list[Polygon] = []
            candidate_ratio = 0.0
            candidate_area_mm2 = 0.0
            candidate_depth_layers = 1
            span_nodes: list[BridgeSpanNode] = []
            span_edges: list[BridgeSpanEdge] = []
            support_surface_ratio = 0.0
            unsupported_surface_area_mm2 = float(max(0.0, island.area))
            if bridge_enabled and layer_index > 0:
                support_clip = _bridge_support_clip(island, lower_boundaries, width)
                coverage_scale = 1.0
                if bridge_over_infill_enabled:
                    coverage_scale = _bridge_support_coverage_scale(
                        layer_index,
                        infill_void_layers=infill_void_lookup,
                        infill_combined_into_layers=infill_combined_into_lookup,
                        infill_thickness_layers=infill_thickness_lookup,
                        infill_surface_ratios=infill_surface_ratio_lookup,
                    )
                candidate_depth_layers = _bridge_void_depth_layers(
                    layer_index,
                    infill_void_layers=infill_void_lookup,
                    infill_thickness_layers=infill_thickness_lookup,
                    infill_void_depth_layers=infill_void_depth_lookup,
                )
                candidate_ratio, candidate_area_mm2 = _bridge_candidate_ratio_geometry(
                    island,
                    support_clip,
                    sample_count=candidate_sample_count,
                    support_coverage_scale=coverage_scale,
                )
                span_nodes, span_edges, support_surface_ratio, unsupported_surface_area_mm2 = _bridge_span_graph(
                    layer_index=layer_index,
                    island_index=island_index,
                    island=island,
                    support_clip=support_clip,
                    angle_deg=(
                        internal_angle
                        if internal_angle > EPSILON
                        else (
                            _normalize_angle(anchor_angle + 90.0)
                            if anchor_angle is not None
                            else _bridge_span_metrics(island)[0]
                        )
                    ),
                    spacing_mm=max(width, width * max(0.5, internal_density)),
                    sample_count=candidate_sample_count,
                    support_coverage_scale=coverage_scale,
                )
            should_bridge = bridge_enabled and layer_index > 0 and (
                unsupported_by_adjacency or (bridge_over_infill_enabled and candidate_ratio >= candidate_min_ratio)
            )
            if should_bridge:
                preferred_angle: float | None = None
                preferred_angle_source = "local"
                if internal_angle > EPSILON:
                    preferred_angle = internal_angle
                    preferred_angle_source = "internal"
                elif anchor_angle is not None:
                    preferred_angle = _normalize_angle(anchor_angle + 90.0)
                    preferred_angle_source = "anchor"

                min_ratio = 0.0 if unsupported_by_adjacency else candidate_min_ratio
                flow_for_region = internal_flow if graph.layer_index > 0 else flow_ratio
                density_for_region = internal_density if graph.layer_index > 0 else density_ratio
                thick_for_region = bool(thick_internal_bridges if graph.layer_index > 0 else thick_bridges)
                bridge_region = _bridge_region_estimate(
                    layer_index=graph.layer_index,
                    island_index=island_index,
                    island=island,
                    support_clip=support_clip,
                    extrusion_width_mm=width,
                    bridge_flow_ratio=flow_for_region,
                    bridge_density_ratio=density_for_region,
                    candidate_ratio=candidate_ratio,
                    candidate_area_mm2=candidate_area_mm2,
                    candidate_depth_layers=candidate_depth_layers,
                    min_candidate_ratio=min_ratio,
                    support_surface_ratio=support_surface_ratio,
                    unsupported_surface_area_mm2=unsupported_surface_area_mm2,
                    span_nodes=span_nodes,
                    span_edges=span_edges,
                    preferred_angle_deg=preferred_angle,
                    angle_source=preferred_angle_source,
                    thick_bridge=thick_for_region,
                )
                bridge_regions.append(bridge_region)
                bridge_region_contexts.append(
                    {
                        "island": island,
                        "support_clip": support_clip,
                        "bridge_flow_ratio": float(flow_for_region),
                        "bridge_density_ratio": float(density_for_region),
                        "candidate_ratio": float(candidate_ratio),
                        "candidate_area_mm2": float(candidate_area_mm2),
                        "candidate_depth_layers": int(candidate_depth_layers),
                        "min_candidate_ratio": float(min_ratio),
                        "support_surface_ratio": float(support_surface_ratio),
                        "unsupported_surface_area_mm2": float(unsupported_surface_area_mm2),
                        "span_nodes": list(span_nodes),
                        "span_edges": list(span_edges),
                        "thick_bridge": bool(thick_for_region),
                    }
                )
                if bridge_region.anchor_ratio <= EPSILON and bridge_region.path_count > 0:
                    layer_warnings.append(f"layer_{graph.layer_index}:island_{island_index}:bridge_anchor_weak")
                if bridge_over_infill_enabled and unsupported_by_adjacency:
                    layer_warnings.append(
                        f"layer_{graph.layer_index}:island_{island_index}:bridge_candidate_ratio={bridge_region.candidate_ratio:.3f}"
                    )
            elif not bridge_enabled and graph.layer_index > 0 and island_index not in supported_islands:
                layer_warnings.append(f"layer_{graph.layer_index}:island_{island_index}:bridge_skipped_disabled")

        bridge_span_components, inter_island_edge_count = _build_bridge_span_components(
            layer_index=int(graph.layer_index),
            bridge_regions=bridge_regions,
            layer_islands=graph.islands,
            extrusion_width_mm=width,
        )
        direction_voted_region_count = 0
        if bridge_regions and bridge_span_components and internal_angle <= EPSILON and layer_anchor_angle is None:
            component_by_id = {int(component.component_id): component for component in bridge_span_components}
            for region_index, region in enumerate(bridge_regions):
                if region.path_count <= 0:
                    continue
                if region_index >= len(bridge_region_contexts):
                    continue
                metadata = component_by_id.get(int(region.span_component_id or 0))
                if metadata is None:
                    continue
                if metadata.region_count < 2:
                    continue
                if metadata.dominant_angle_confidence < 0.30:
                    continue
                target_angle = float(metadata.dominant_angle_deg)
                if _bridge_angle_distance_deg(region.angle_deg, target_angle) < 4.0:
                    continue
                context = bridge_region_contexts[region_index]
                island_obj = context.get("island")
                if not isinstance(island_obj, Island):
                    continue
                support_clip_obj = context.get("support_clip")
                if not isinstance(support_clip_obj, list):
                    support_clip_obj = []
                rerouted = _bridge_region_estimate(
                    layer_index=int(region.layer_index),
                    island_index=int(region.island_index),
                    island=island_obj,
                    support_clip=support_clip_obj,
                    extrusion_width_mm=width,
                    bridge_flow_ratio=float(context.get("bridge_flow_ratio", internal_flow)),
                    bridge_density_ratio=float(context.get("bridge_density_ratio", internal_density)),
                    candidate_ratio=float(context.get("candidate_ratio", region.candidate_ratio)),
                    candidate_area_mm2=float(context.get("candidate_area_mm2", region.candidate_area_mm2)),
                    candidate_depth_layers=int(context.get("candidate_depth_layers", region.candidate_depth_layers)),
                    min_candidate_ratio=float(context.get("min_candidate_ratio", 0.0)),
                    support_surface_ratio=float(context.get("support_surface_ratio", region.support_surface_ratio)),
                    unsupported_surface_area_mm2=float(
                        context.get("unsupported_surface_area_mm2", region.unsupported_surface_area_mm2)
                    ),
                    span_nodes=(context.get("span_nodes", region.span_nodes) if isinstance(context.get("span_nodes"), list) else region.span_nodes),
                    span_edges=(context.get("span_edges", region.span_edges) if isinstance(context.get("span_edges"), list) else region.span_edges),
                    preferred_angle_deg=target_angle,
                    angle_source="component_vote",
                    thick_bridge=bool(context.get("thick_bridge", False)),
                )
                bridge_regions[region_index] = rerouted
                direction_voted_region_count += 1
            if direction_voted_region_count > 0:
                bridge_span_components, inter_island_edge_count = _build_bridge_span_components(
                    layer_index=int(graph.layer_index),
                    bridge_regions=bridge_regions,
                    layer_islands=graph.islands,
                    extrusion_width_mm=width,
                )
                layer_warnings.append(
                    f"layer_{graph.layer_index}:bridge_direction_voted_regions={direction_voted_region_count}"
                )

        bridge_region_count = len(bridge_regions)
        bridge_path_count = sum(region.path_count for region in bridge_regions)
        bridge_path_length = float(sum(region.path_length_mm for region in bridge_regions))
        bridge_span_node_count = sum(len(region.span_nodes) for region in bridge_regions)
        bridge_span_edge_count = sum(len(region.span_edges) for region in bridge_regions)
        if bridge_span_components:
            layer_warnings.append(
                f"layer_{graph.layer_index}:bridge_span_components={len(bridge_span_components)}"
            )

        return (
            SolidLayerPlan(
                layer_index=graph.layer_index,
                z_height_mm=float(graph.z_height_mm),
                classification=classification,
                is_solid=is_solid,
                island_count=graph.island_count,
                solid_path_count=solid_path_count,
                solid_path_length_mm=float(solid_path_length),
                bridge_region_count=bridge_region_count,
                bridge_path_count=bridge_path_count,
                bridge_path_length_mm=bridge_path_length,
                bridge_span_component_count=len(bridge_span_components),
                bridge_span_inter_island_edge_count=int(inter_island_edge_count),
                bridge_span_node_count=int(bridge_span_node_count),
                bridge_span_edge_count=int(bridge_span_edge_count),
                bridge_span_components=bridge_span_components,
                bridge_regions=bridge_regions,
            ),
            layer_warnings,
        )

    worker_count = max(1, min(int(max_workers), len(graphs) if graphs else 1))
    if worker_count > 1 and len(graphs) > 1:
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            results = list(executor.map(_build_layer, graphs))
    else:
        results = [_build_layer(graph) for graph in graphs]

    if extra_bridge_layer_enabled:
        by_index: dict[int, SolidLayerPlan] = {}
        for plan, _warnings in results:
            by_index[int(plan.layer_index)] = plan
        for layer_index in sorted(by_index.keys()):
            src = by_index[layer_index]
            dst = by_index.get(layer_index + 1)
            if dst is None:
                continue
            if not src.bridge_regions:
                continue
            if dst.classification != SOLID_CLASS_INTERNAL:
                continue
            for region in src.bridge_regions:
                mirrored_nodes: list[BridgeSpanNode] = []
                for node in region.span_nodes:
                    mirrored_nodes.append(
                        BridgeSpanNode(
                            layer_index=int(dst.layer_index),
                            island_index=int(node.island_index),
                            node_index=int(node.node_index),
                            offset_start_mm=float(node.offset_start_mm),
                            offset_end_mm=float(node.offset_end_mm),
                            span_length_mm=float(node.span_length_mm),
                            center_x_mm=float(node.center_x_mm),
                            center_y_mm=float(node.center_y_mm),
                            support_ratio=float(node.support_ratio),
                            candidate_ratio=float(node.candidate_ratio),
                            path_count=max(0, int(round(node.path_count * 0.6))),
                            path_length_mm=float(node.path_length_mm * 0.6),
                            line_start_x_mm=float(node.line_start_x_mm),
                            line_start_y_mm=float(node.line_start_y_mm),
                            line_end_x_mm=float(node.line_end_x_mm),
                            line_end_y_mm=float(node.line_end_y_mm),
                        )
                    )
                mirrored_edges: list[BridgeSpanEdge] = []
                for edge in region.span_edges:
                    mirrored_edges.append(
                        BridgeSpanEdge(
                            layer_index=int(dst.layer_index),
                            island_index=int(edge.island_index),
                            src_node_index=int(edge.src_node_index),
                            dst_node_index=int(edge.dst_node_index),
                            continuity_ratio=float(edge.continuity_ratio),
                            shared_candidate_ratio=float(edge.shared_candidate_ratio),
                            strip_overlap_ratio=float(edge.strip_overlap_ratio),
                            strip_intersection_length_mm=float(edge.strip_intersection_length_mm),
                            strip_alignment_ratio=float(edge.strip_alignment_ratio),
                            direction_weight=float(edge.direction_weight),
                            graph_weight=float(edge.graph_weight),
                        )
                    )
                mirrored = BridgeRegionPlan(
                    layer_index=int(dst.layer_index),
                    island_index=int(region.island_index),
                    angle_deg=float(region.angle_deg),
                    path_count=max(1, int(round(region.path_count * 0.6))),
                    path_length_mm=float(region.path_length_mm * 0.6),
                    span_major_mm=float(region.span_major_mm),
                    span_minor_mm=float(region.span_minor_mm),
                    anchor_ratio=float(region.anchor_ratio),
                    candidate_ratio=float(region.candidate_ratio),
                    candidate_area_mm2=float(region.candidate_area_mm2 * 0.6),
                    candidate_depth_layers=int(max(1, region.candidate_depth_layers)),
                    support_surface_ratio=float(region.support_surface_ratio),
                    unsupported_surface_area_mm2=float(region.unsupported_surface_area_mm2 * 0.6),
                    span_component_id=None,
                    span_component_region_count=1,
                    span_component_node_count=0,
                    span_component_inter_island_edge_count=0,
                    direction_vote_angle_deg=float(region.direction_vote_angle_deg),
                    direction_vote_confidence=float(region.direction_vote_confidence),
                    direction_angle_source=str(region.direction_angle_source),
                    span_nodes=mirrored_nodes,
                    span_edges=mirrored_edges,
                )
                dst.bridge_regions.append(mirrored)
            dst.bridge_region_count = len(dst.bridge_regions)
            dst.bridge_path_count = sum(item.path_count for item in dst.bridge_regions)
            dst.bridge_path_length_mm = float(sum(item.path_length_mm for item in dst.bridge_regions))
            components, inter_island_edges = _build_bridge_span_components(
                layer_index=int(dst.layer_index),
                bridge_regions=dst.bridge_regions,
                layer_islands=(graph_lookup.get(int(dst.layer_index)).islands if graph_lookup.get(int(dst.layer_index)) else ()),
                extrusion_width_mm=width,
            )
            dst.bridge_span_component_count = len(components)
            dst.bridge_span_inter_island_edge_count = int(inter_island_edges)
            dst.bridge_span_node_count = int(sum(len(item.span_nodes) for item in dst.bridge_regions))
            dst.bridge_span_edge_count = int(sum(len(item.span_edges) for item in dst.bridge_regions))
            dst.bridge_span_components = components
        warnings.append("solid_bridges:extra_bridge_layer_applied")

    layer_plans: list[SolidLayerPlan] = []
    island_count_total = 0
    solid_layer_count = 0
    bottom_solid_layer_count = 0
    top_solid_layer_count = 0
    solid_path_count_total = 0
    solid_path_length_total = 0.0
    bridge_region_count_total = 0
    bridge_path_count_total = 0
    bridge_path_length_total = 0.0
    bridge_span_component_count_total = 0
    bridge_span_inter_island_edge_count_total = 0
    bridge_span_node_count_total = 0
    bridge_span_edge_count_total = 0
    bridge_candidate_ratio_acc = 0.0
    bridge_support_surface_ratio_acc = 0.0

    for layer_plan, layer_warnings in results:
        layer_plans.append(layer_plan)
        warnings.extend(layer_warnings)
        island_count_total += layer_plan.island_count
        if layer_plan.is_solid:
            solid_layer_count += 1
        if layer_plan.classification == SOLID_CLASS_BOTTOM:
            bottom_solid_layer_count += 1
        if layer_plan.classification == SOLID_CLASS_TOP:
            top_solid_layer_count += 1
        solid_path_count_total += layer_plan.solid_path_count
        solid_path_length_total += layer_plan.solid_path_length_mm
        bridge_region_count_total += layer_plan.bridge_region_count
        bridge_path_count_total += layer_plan.bridge_path_count
        bridge_path_length_total += layer_plan.bridge_path_length_mm
        bridge_span_component_count_total += int(layer_plan.bridge_span_component_count)
        bridge_span_inter_island_edge_count_total += int(layer_plan.bridge_span_inter_island_edge_count)
        bridge_span_node_count_total += int(layer_plan.bridge_span_node_count)
        bridge_span_edge_count_total += int(layer_plan.bridge_span_edge_count)
        for region in layer_plan.bridge_regions:
            bridge_candidate_ratio_acc += float(region.candidate_ratio)
            bridge_support_surface_ratio_acc += float(region.support_surface_ratio)

    layer_plans.sort(key=lambda plan: int(plan.layer_index))

    report = SolidBridgeReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        layer_count=layer_count,
        island_count_total=island_count_total,
        top_layers_requested=top_count,
        bottom_layers_requested=bottom_count,
        solid_layer_count=solid_layer_count,
        bottom_solid_layer_count=bottom_solid_layer_count,
        top_solid_layer_count=top_solid_layer_count,
        solid_path_count_total=solid_path_count_total,
        solid_path_length_mm_total=float(solid_path_length_total),
        bridge_enabled=bool(bridge_enabled),
        bridge_region_count_total=bridge_region_count_total,
        bridge_path_count_total=bridge_path_count_total,
        bridge_path_length_mm_total=float(bridge_path_length_total),
        bridge_span_component_count_total=int(bridge_span_component_count_total),
        bridge_span_inter_island_edge_count_total=int(bridge_span_inter_island_edge_count_total),
        bridge_flow_ratio=float(internal_flow if bridge_enabled else flow_ratio),
        bridge_speed_ratio=float(speed_ratio),
        warning_count=len(warnings),
        bridge_span_node_count_total=int(bridge_span_node_count_total),
        bridge_span_edge_count_total=int(bridge_span_edge_count_total),
        bridge_candidate_ratio_avg=(
            float(bridge_candidate_ratio_acc / bridge_region_count_total) if bridge_region_count_total > 0 else 0.0
        ),
        bridge_support_surface_ratio_avg=(
            float(bridge_support_surface_ratio_acc / bridge_region_count_total) if bridge_region_count_total > 0 else 0.0
        ),
        warnings=warnings,
    )
    return layer_plans, report
