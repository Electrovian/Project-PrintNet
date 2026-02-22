from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from math import atan2, ceil, cos, radians, sin
from typing import Sequence

from .errors import SlicerV2SupportPlanningError
from .geometry import EPSILON, Island, Point2, Polygon
from .island_graph import LayerIslandGraph, VerticalAdjacencyEdge
from .line_split import split_line
from .polygon_pipeline import offset_polygon
from .region_expansion import RegionExpansionParameters, merge_expansions_into_polygons, propagate_waves_from_polygons


SUPPORT_TYPE_NORMAL = "normal"
SUPPORT_TYPE_TREE = "tree"
ALLOWED_SUPPORT_TYPES = {SUPPORT_TYPE_NORMAL, SUPPORT_TYPE_TREE}


@dataclass
class SupportRegionPlan:
    layer_index: int
    island_index: int
    pattern: str
    angle_deg: float
    path_count: int
    path_length_mm: float
    interface_path_count: int
    span_major_mm: float
    span_minor_mm: float
    footprint_polygon_count: int = 0
    footprint_area_mm2: float = 0.0
    center_x_mm: float = 0.0
    center_y_mm: float = 0.0
    tree_primary_branch_id: int | None = None
    tree_branch_count: int = 0
    tree_merge_count: int = 0
    tree_growth_depth_layers: int = 0
    tree_collision_avoided: bool = False
    tree_route_waypoint_count: int = 0
    tree_route_detour_mm: float = 0.0
    tree_pruned: bool = False

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class TreeSupportBranchPlan:
    branch_id: int
    parent_branch_id: int | None
    root_layer_index: int
    tip_layer_index: int
    x_mm: float
    y_mm: float
    radius_mm: float
    length_mm: float
    connected_region_count: int
    waypoint_count: int = 0
    collision_avoidance_count: int = 0
    blocked_collision_count: int = 0
    pruned: bool = False
    prune_layer_index: int | None = None
    load_score: float = 0.0
    reroute_cost_mm: float = 0.0
    selection_score: float = 0.0
    trunk_assignment: str = "root"
    merged_branch_ids: list[int] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class LayerSupportPlan:
    layer_index: int
    z_height_mm: float
    island_count: int
    unsupported_island_count: int
    support_region_count: int
    support_path_count: int
    support_path_length_mm: float
    interface_path_count: int
    tree_branch_count: int
    tree_merge_count: int
    tree_collision_avoid_count: int
    tree_pruned_branch_count: int
    tree_parent_assignment_count: int
    tree_trunk_count: int
    support_regions: list[SupportRegionPlan] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class SupportPlanningReport:
    generated_at_utc: str
    layer_count: int
    island_count_total: int
    unsupported_island_count_total: int
    support_enabled: bool
    support_type: str
    support_density_percent: float
    support_spacing_mm: float
    support_xy_gap_mm: float
    support_z_gap_mm: float
    support_interface_layers: int
    support_region_count_total: int
    support_path_count_total: int
    support_path_length_mm_total: float
    interface_path_count_total: int
    tree_branch_count_total: int
    tree_merge_count_total: int
    tree_collision_avoid_count_total: int
    tree_pruned_branch_count_total: int
    tree_parent_assignment_count_total: int
    tree_trunk_count_total: int
    tree_branch_load_score_avg: float = 0.0
    tree_branch_selection_score_avg: float = 0.0
    tree_branch_reroute_cost_mm_total: float = 0.0
    tree_branch_trunk_assignment_counts: dict[str, int] = field(default_factory=dict)
    warning_count: int = 0
    warnings: list[str] = field(default_factory=list)
    tree_branches: list[TreeSupportBranchPlan] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _validate_layer_graphs(layer_graphs: Sequence[LayerIslandGraph]) -> list[LayerIslandGraph]:
    graphs = list(layer_graphs)
    for index, graph in enumerate(graphs):
        if not isinstance(graph, LayerIslandGraph):
            raise SlicerV2SupportPlanningError(f"SUPPORT_LAYER_GRAPH_INVALID:{index}")
    return graphs


def _validate_vertical_edges(vertical_edges: Sequence[VerticalAdjacencyEdge]) -> list[VerticalAdjacencyEdge]:
    edges = list(vertical_edges)
    for index, edge in enumerate(edges):
        if not isinstance(edge, VerticalAdjacencyEdge):
            raise SlicerV2SupportPlanningError(f"SUPPORT_VERTICAL_EDGE_INVALID:{index}")
    return edges


def _validate_support_type(value: str) -> str:
    text = str(value).strip().lower()
    if text not in ALLOWED_SUPPORT_TYPES:
        raise SlicerV2SupportPlanningError(f"SUPPORT_TYPE_UNSUPPORTED:{value}")
    return text


def _validate_ratio(value: float, *, code: str, minimum: float, maximum: float) -> float:
    parsed = float(value)
    if parsed < minimum or parsed > maximum:
        raise SlicerV2SupportPlanningError(code)
    return parsed


def _validate_positive(value: float, *, code: str) -> float:
    parsed = float(value)
    if parsed <= EPSILON:
        raise SlicerV2SupportPlanningError(code)
    return parsed


def _validate_non_negative(value: float, *, code: str) -> float:
    parsed = float(value)
    if parsed < 0.0:
        raise SlicerV2SupportPlanningError(code)
    return parsed


def _validate_interface_layers(value: int) -> int:
    parsed = int(value)
    if parsed < 0:
        raise SlicerV2SupportPlanningError("SUPPORT_INTERFACE_LAYER_COUNT_INVALID")
    if parsed > 20:
        raise SlicerV2SupportPlanningError("SUPPORT_INTERFACE_LAYER_COUNT_EXCESSIVE")
    return parsed


def _supported_islands_by_layer(vertical_edges: Sequence[VerticalAdjacencyEdge]) -> dict[int, set[int]]:
    supported: dict[int, set[int]] = {}
    for edge in vertical_edges:
        upper_layer = int(edge.upper_layer_index)
        upper_island = int(edge.upper_island_index)
        if upper_layer not in supported:
            supported[upper_layer] = set()
        supported[upper_layer].add(upper_island)
    return supported


def _resolve_spacing(
    *,
    support_spacing_mm: float,
    support_density_ratio: float,
    extrusion_width_mm: float,
    support_type: str,
) -> float:
    density_scale = max(0.2, 1.0 - (support_density_ratio * 0.75))
    spacing = max(extrusion_width_mm, support_spacing_mm * density_scale)
    if support_type == SUPPORT_TYPE_TREE:
        spacing = spacing * 1.3
    return max(extrusion_width_mm, spacing)


def _layer_lookup(layer_graphs: Sequence[LayerIslandGraph]) -> dict[int, LayerIslandGraph]:
    out: dict[int, LayerIslandGraph] = {}
    for graph in layer_graphs:
        out[int(graph.layer_index)] = graph
    return out


def _line_metrics(start: Point2, end: Point2, clip: Sequence[Polygon | Island]) -> tuple[int, float]:
    split = split_line((start, end), clip, closed=False)
    if len(split) < 2:
        return (0, 0.0)

    segment_count = 0
    path_length_mm = 0.0
    for index in range(len(split) - 1):
        a = split[index]
        b = split[index + 1]
        length = a.p.distance_to(b.p)
        if length <= EPSILON:
            continue
        if not a.clipped:
            continue
        path_length_mm += length
        if index == 0 or not split[index - 1].clipped:
            segment_count += 1
    return (segment_count, float(path_length_mm))


def _scanline_fill_metrics(polygons: Sequence[Polygon], spacing_mm: float, angle_deg: float) -> tuple[int, float, float, float]:
    if not polygons:
        return (0, 0.0, 0.0, 0.0)

    min_x = min(poly.bounds.min_x for poly in polygons)
    min_y = min(poly.bounds.min_y for poly in polygons)
    max_x = max(poly.bounds.max_x for poly in polygons)
    max_y = max(poly.bounds.max_y for poly in polygons)
    width = max(0.0, max_x - min_x)
    height = max(0.0, max_y - min_y)
    if width <= EPSILON or height <= EPSILON:
        return (0, 0.0, max(width, height), min(width, height))

    vertical = abs((angle_deg % 180.0) - 90.0) <= 45.0
    span_major = height if vertical else width
    span_minor = width if vertical else height
    spacing = max(spacing_mm, EPSILON)
    line_count = max(1, int(ceil(span_minor / spacing)))
    pad = max(spacing, 0.25)

    path_count = 0
    path_length_mm = 0.0
    if line_count == 1:
        centers = [0.5 * (min_x + max_x) if vertical else 0.5 * (min_y + max_y)]
    else:
        step = span_minor / float(line_count)
        centers = []
        for index in range(line_count):
            centers.append((min_x + ((index + 0.5) * step)) if vertical else (min_y + ((index + 0.5) * step)))

    for center in centers:
        if vertical:
            start = Point2(float(center), float(min_y - pad))
            end = Point2(float(center), float(max_y + pad))
        else:
            start = Point2(float(min_x - pad), float(center))
            end = Point2(float(max_x + pad), float(center))
        segments, length_mm = _line_metrics(start, end, polygons)
        path_count += segments
        path_length_mm += length_mm

    if path_count <= 0 or path_length_mm <= EPSILON:
        path_count = line_count
        path_length_mm = float(line_count * span_major)
    return (path_count, float(path_length_mm), float(span_major), float(span_minor))


def _expand_support_footprint(
    *,
    island: Island,
    xy_gap_mm: float,
    support_spacing_mm: float,
    extrusion_width_mm: float,
    boundary_polygons: Sequence[Polygon],
) -> list[Polygon]:
    base = island.outer
    if xy_gap_mm > EPSILON:
        shrunken = offset_polygon(base, -xy_gap_mm, min_area=1e-8)
        if shrunken is not None:
            base = shrunken

    src = [base]
    if not boundary_polygons:
        return src

    full_expansion = max(extrusion_width_mm * 0.5, min(support_spacing_mm, 4.0))
    expansion_step = max(extrusion_width_mm * 0.25, full_expansion / 3.0)
    try:
        params = RegionExpansionParameters.build(full_expansion, expansion_step, 8)
        expanded = propagate_waves_from_polygons(src, boundary_polygons, params)
        merged = merge_expansions_into_polygons(src, expanded)
    except Exception:
        return src
    return merged if merged else src


def _estimate_region(
    *,
    layer_index: int,
    island_index: int,
    polygons: Sequence[Polygon],
    support_type: str,
    support_interface_layers: int,
    support_spacing_mm: float,
    support_density_ratio: float,
    extrusion_width_mm: float,
) -> SupportRegionPlan:
    if not polygons:
        raise SlicerV2SupportPlanningError("SUPPORT_REGION_POLYGONS_EMPTY")

    width_mm = max(poly.bounds.max_x for poly in polygons) - min(poly.bounds.min_x for poly in polygons)
    height_mm = max(poly.bounds.max_y for poly in polygons) - min(poly.bounds.min_y for poly in polygons)
    span_major = max(width_mm, height_mm)
    span_minor = min(width_mm, height_mm)
    spacing = _resolve_spacing(
        support_spacing_mm=support_spacing_mm,
        support_density_ratio=support_density_ratio,
        extrusion_width_mm=extrusion_width_mm,
        support_type=support_type,
    )
    angle = 0.0 if width_mm >= height_mm else 90.0
    if layer_index % 2 == 1:
        angle = (angle + 90.0) % 180.0

    path_count, path_length, span_major, span_minor = _scanline_fill_metrics(polygons, spacing, angle)
    if support_type == SUPPORT_TYPE_TREE:
        path_count = max(1, int(ceil(path_count * 0.7)))
        path_length = float(path_length * 0.75)

    interface_path_count = min(path_count, support_interface_layers * 2) if support_interface_layers > 0 else 0
    pattern = "lines" if support_type == SUPPORT_TYPE_NORMAL else "tree_branch"
    area_mm2 = float(sum(poly.area for poly in polygons))

    return SupportRegionPlan(
        layer_index=layer_index,
        island_index=island_index,
        pattern=pattern,
        angle_deg=angle,
        path_count=path_count,
        path_length_mm=path_length,
        interface_path_count=interface_path_count,
        span_major_mm=span_major,
        span_minor_mm=span_minor,
        footprint_polygon_count=len(polygons),
        footprint_area_mm2=area_mm2,
        center_x_mm=float(sum((poly.centroid.x * max(poly.area, EPSILON)) for poly in polygons) / max(area_mm2, EPSILON)),
        center_y_mm=float(sum((poly.centroid.y * max(poly.area, EPSILON)) for poly in polygons) / max(area_mm2, EPSILON)),
    )


def _layer_height_lookup(graphs: Sequence[LayerIslandGraph], layer_index: int, fallback: float) -> float:
    if not graphs:
        return float(fallback)
    for idx, graph in enumerate(graphs):
        if int(graph.layer_index) != int(layer_index):
            continue
        if idx > 0:
            dz = float(graph.z_height_mm) - float(graphs[idx - 1].z_height_mm)
            if dz > EPSILON:
                return dz
        if idx + 1 < len(graphs):
            dz = float(graphs[idx + 1].z_height_mm) - float(graph.z_height_mm)
            if dz > EPSILON:
                return dz
    return float(fallback)


def _tree_distance(a_x: float, a_y: float, b_x: float, b_y: float) -> float:
    dx = float(a_x) - float(b_x)
    dy = float(a_y) - float(b_y)
    return (dx * dx + dy * dy) ** 0.5


def _clamp_unit(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _branch_load_score(
    branch: TreeSupportBranchPlan,
    *,
    support_spacing_mm: float,
    min_branch_radius_mm: float,
) -> float:
    spacing = max(EPSILON, float(support_spacing_mm))
    min_radius = max(EPSILON, float(min_branch_radius_mm))
    radius_cap = max(min_radius, spacing * 1.8)
    radius_norm = _clamp_unit((float(branch.radius_mm) - min_radius) / max(EPSILON, radius_cap - min_radius))
    length_norm = _clamp_unit(float(branch.length_mm) / max(EPSILON, spacing * 6.0))
    connection_norm = _clamp_unit(float(branch.connected_region_count) / 6.0)
    waypoint_burden = float(branch.waypoint_count) / max(1.0, float(branch.connected_region_count))
    waypoint_penalty = _clamp_unit(waypoint_burden / 6.0)
    blocked_penalty = _clamp_unit(float(branch.blocked_collision_count) / 6.0)
    collision_bonus = _clamp_unit(
        float(branch.collision_avoidance_count) / max(1.0, float(branch.connected_region_count) + 1.0)
    )
    score = (
        (0.38 * connection_norm)
        + (0.27 * radius_norm)
        + (0.19 * length_norm)
        + (0.10 * collision_bonus)
        - (0.10 * waypoint_penalty)
        - (0.12 * blocked_penalty)
    )
    if branch.pruned:
        score -= 0.35
    return float(max(0.0, score))


def _route_efficiency_score(
    *,
    direct_distance_mm: float,
    routed_distance_mm: float,
    waypoint_count: int,
    collision_avoided: bool,
    support_spacing_mm: float,
) -> float:
    direct = max(0.0, float(direct_distance_mm))
    routed = max(EPSILON, float(routed_distance_mm))
    spacing = max(EPSILON, float(support_spacing_mm))
    efficiency = _clamp_unit(direct / routed) if direct > EPSILON else 1.0
    detour = max(0.0, routed - direct)
    detour_ratio = detour / max(EPSILON, direct + (spacing * 0.75))
    detour_penalty = _clamp_unit(detour_ratio / 2.5)
    waypoint_penalty = _clamp_unit(float(max(0, waypoint_count)) / 8.0)
    collision_penalty = 0.08 if collision_avoided else 0.0
    score = (0.64 * efficiency) + (0.26 * (1.0 - detour_penalty)) + (0.10 * (1.0 - waypoint_penalty)) - collision_penalty
    return float(max(0.0, min(1.0, score)))


def _parent_candidate_score(
    branch: TreeSupportBranchPlan,
    *,
    direct_distance_mm: float,
    routed_distance_mm: float,
    waypoint_count: int,
    collision_avoided: bool,
    support_spacing_mm: float,
    min_branch_radius_mm: float,
    route_weight: float = 0.56,
    load_weight: float = 0.40,
    root_bonus_weight: float = 0.06,
) -> float:
    load_score = _branch_load_score(
        branch,
        support_spacing_mm=support_spacing_mm,
        min_branch_radius_mm=min_branch_radius_mm,
    )
    route_score = _route_efficiency_score(
        direct_distance_mm=direct_distance_mm,
        routed_distance_mm=routed_distance_mm,
        waypoint_count=waypoint_count,
        collision_avoided=collision_avoided,
        support_spacing_mm=support_spacing_mm,
    )
    route_w = max(0.0, float(route_weight))
    load_w = max(0.0, float(load_weight))
    bonus_w = max(0.0, float(root_bonus_weight))
    root_bonus = bonus_w if branch.parent_branch_id is None else 0.0
    score = (route_w * route_score) + (load_w * load_score) + root_bonus
    return float(max(0.0, score))


def _trunk_candidate_score(
    branch: TreeSupportBranchPlan,
    *,
    support_spacing_mm: float,
    min_branch_radius_mm: float,
    root_bonus_weight: float = 0.08,
    depth_bonus_weight: float = 0.07,
) -> float:
    load_score = _branch_load_score(
        branch,
        support_spacing_mm=support_spacing_mm,
        min_branch_radius_mm=min_branch_radius_mm,
    )
    root_bonus = max(0.0, float(root_bonus_weight)) if branch.parent_branch_id is None else 0.0
    depth_bonus = _clamp_unit(float(branch.connected_region_count) / 8.0) * max(0.0, float(depth_bonus_weight))
    score = load_score + root_bonus + depth_bonus
    return float(max(0.0, score))


def _resolve_merge_replacement(merged_into: dict[int, int], branch_id: int) -> int:
    current = int(branch_id)
    safety = len(merged_into) + 4
    while current in merged_into and safety > 0:
        nxt = int(merged_into[current])
        if nxt == current:
            break
        current = nxt
        safety -= 1
    return int(current)


def _would_create_parent_cycle(
    branches: dict[int, TreeSupportBranchPlan],
    *,
    child_branch_id: int,
    parent_branch_id: int,
) -> bool:
    if child_branch_id == parent_branch_id:
        return True
    current: int | None = int(parent_branch_id)
    safety = len(branches) + 4
    while current is not None and safety > 0:
        if current == int(child_branch_id):
            return True
        branch = branches.get(int(current))
        if branch is None or branch.parent_branch_id is None:
            return False
        current = int(branch.parent_branch_id)
        safety -= 1
    return False


def _point_on_segment(point: Point2, start: Point2, end: Point2) -> bool:
    cross = ((point.y - start.y) * (end.x - start.x)) - ((point.x - start.x) * (end.y - start.y))
    if abs(cross) > EPSILON:
        return False
    dot = ((point.x - start.x) * (end.x - start.x)) + ((point.y - start.y) * (end.y - start.y))
    if dot < -EPSILON:
        return False
    length_sq = ((end.x - start.x) ** 2) + ((end.y - start.y) ** 2)
    if dot - length_sq > EPSILON:
        return False
    return True


def _orientation(a: Point2, b: Point2, c: Point2) -> float:
    return ((b.y - a.y) * (c.x - b.x)) - ((b.x - a.x) * (c.y - b.y))


def _segments_intersect(a1: Point2, a2: Point2, b1: Point2, b2: Point2) -> bool:
    o1 = _orientation(a1, a2, b1)
    o2 = _orientation(a1, a2, b2)
    o3 = _orientation(b1, b2, a1)
    o4 = _orientation(b1, b2, a2)

    if ((o1 > EPSILON and o2 < -EPSILON) or (o1 < -EPSILON and o2 > EPSILON)) and (
        (o3 > EPSILON and o4 < -EPSILON) or (o3 < -EPSILON and o4 > EPSILON)
    ):
        return True

    if abs(o1) <= EPSILON and _point_on_segment(b1, a1, a2):
        return True
    if abs(o2) <= EPSILON and _point_on_segment(b2, a1, a2):
        return True
    if abs(o3) <= EPSILON and _point_on_segment(a1, b1, b2):
        return True
    if abs(o4) <= EPSILON and _point_on_segment(a2, b1, b2):
        return True
    return False


def _segment_intersects_polygon(start: Point2, end: Point2, polygon: Polygon) -> bool:
    if polygon.contains_point(start, include_boundary=True) or polygon.contains_point(end, include_boundary=True):
        return True
    points = list(polygon.points)
    for index, edge_start in enumerate(points):
        edge_end = points[(index + 1) % len(points)]
        if _segments_intersect(start, end, edge_start, edge_end):
            return True
    return False


def _point_collides_model(point: Point2, polygons: Sequence[Polygon]) -> bool:
    for polygon in polygons:
        if polygon.contains_point(point, include_boundary=True):
            return True
    return False


def _segment_collides_model(start: Point2, end: Point2, polygons: Sequence[Polygon]) -> bool:
    if not polygons:
        return False
    for polygon in polygons:
        if _segment_intersects_polygon(start, end, polygon):
            return True
    return False


def _path_length(points: Sequence[Point2]) -> float:
    if len(points) < 2:
        return 0.0
    total = 0.0
    for index in range(len(points) - 1):
        total += float(points[index].distance_to(points[index + 1]))
    return float(total)


def _append_unique_point(points: list[Point2], candidate: Point2, *, tolerance_mm: float) -> None:
    tol = max(EPSILON, float(tolerance_mm))
    for point in points:
        if point.distance_to(candidate) <= tol:
            return
    points.append(candidate)


def _route_branch_connection(
    *,
    start: Point2,
    target: Point2,
    obstacles: Sequence[Polygon],
    base_step_mm: float,
) -> tuple[list[Point2], bool, bool, float]:
    direct_distance = start.distance_to(target)
    if direct_distance <= EPSILON:
        return [start, target], False, False, 0.0
    if not _segment_collides_model(start, target, obstacles):
        return [start, target], False, False, direct_distance

    base_step = max(0.25, float(base_step_mm))
    direction_angle = atan2(float(target.y - start.y), float(target.x - start.x))
    normal_angle = direction_angle + radians(90.0)

    max_radius = max(base_step * 2.0, min(direct_distance * 0.95, base_step * 9.0))
    raw_radii = [base_step, base_step * 1.5, base_step * 2.2, base_step * 3.0, base_step * 4.1, base_step * 5.6, base_step * 7.0]
    radii: list[float] = []
    for radius in raw_radii:
        if radius <= max_radius + EPSILON:
            radii.append(float(radius))
    if not radii:
        radii = [float(max_radius)]
    angle_offsets_deg = [0.0, 25.0, -25.0, 45.0, -45.0, 70.0, -70.0, 95.0, -95.0, 135.0, -135.0, 180.0]

    nodes: list[Point2] = [start, target]
    dedupe_tolerance = max(0.05, base_step * 0.25)

    for anchor_point, anchor_angle in (
        (start, direction_angle),
        (target, direction_angle + radians(180.0)),
    ):
        for radius in radii:
            for offset_deg in angle_offsets_deg:
                angle = anchor_angle + radians(float(offset_deg))
                candidate = Point2(
                    float(anchor_point.x + (cos(angle) * radius)),
                    float(anchor_point.y + (sin(angle) * radius)),
                )
                if _point_collides_model(candidate, obstacles):
                    continue
                _append_unique_point(nodes, candidate, tolerance_mm=dedupe_tolerance)

    corridor_t = [0.25, 0.4, 0.5, 0.6, 0.75]
    corridor_offsets = [1.0, 1.8, 2.8, 4.0]
    for t in corridor_t:
        base_x = float(start.x + ((target.x - start.x) * t))
        base_y = float(start.y + ((target.y - start.y) * t))
        for sign in (-1.0, 1.0):
            for offset_mul in corridor_offsets:
                offset = base_step * float(offset_mul) * sign
                candidate = Point2(
                    float(base_x + (cos(normal_angle) * offset)),
                    float(base_y + (sin(normal_angle) * offset)),
                )
                if _point_collides_model(candidate, obstacles):
                    continue
                _append_unique_point(nodes, candidate, tolerance_mm=dedupe_tolerance)

    adjacency: dict[int, list[tuple[int, float]]] = {}
    for src_index in range(len(nodes)):
        src = nodes[src_index]
        for dst_index in range(src_index + 1, len(nodes)):
            dst = nodes[dst_index]
            if _segment_collides_model(src, dst, obstacles):
                continue
            distance = float(src.distance_to(dst))
            if distance <= EPSILON:
                continue
            adjacency.setdefault(src_index, []).append((dst_index, distance))
            adjacency.setdefault(dst_index, []).append((src_index, distance))

    if 0 not in adjacency or 1 not in adjacency:
        return [], False, True, direct_distance

    node_count = len(nodes)
    costs = [float("inf")] * node_count
    previous = [-1] * node_count
    visited = [False] * node_count
    costs[0] = 0.0

    for _ in range(node_count):
        current = -1
        current_cost = float("inf")
        for index in range(node_count):
            if visited[index]:
                continue
            if costs[index] < current_cost:
                current_cost = costs[index]
                current = index
        if current < 0:
            break
        if current == 1:
            break
        visited[current] = True
        for neighbor, segment_distance in adjacency.get(current, ()):
            if visited[neighbor]:
                continue
            waypoint_penalty = 0.04 * base_step if neighbor not in (0, 1) else 0.0
            candidate_cost = float(costs[current] + segment_distance + waypoint_penalty)
            if candidate_cost + EPSILON < costs[neighbor]:
                costs[neighbor] = candidate_cost
                previous[neighbor] = current

    if costs[1] == float("inf"):
        return [], False, True, direct_distance

    path_indices: list[int] = []
    current_index = 1
    safety = node_count + 4
    while current_index >= 0 and safety > 0:
        path_indices.append(current_index)
        if current_index == 0:
            break
        current_index = previous[current_index]
        safety -= 1
    if not path_indices or path_indices[-1] != 0:
        return [], False, True, direct_distance
    path_indices.reverse()
    path = [nodes[index] for index in path_indices]
    path_length = _path_length(path)
    if path_length <= EPSILON:
        return [], False, True, direct_distance
    if path_length > max(direct_distance * 6.0, direct_distance + (base_step * 28.0)):
        return [], False, True, direct_distance
    collision_avoided = len(path) > 2
    return path, bool(collision_avoided), False, float(path_length)


def _apply_tree_branch_heuristics(
    *,
    layer_plans: Sequence[LayerSupportPlan],
    layer_graphs: Sequence[LayerIslandGraph],
    support_spacing_mm: float,
    branch_merge_distance_ratio: float,
    branch_growth_ratio: float,
    min_branch_radius_mm: float,
    parent_weight_route: float,
    parent_weight_load: float,
    parent_root_bonus: float,
    trunk_root_bonus: float,
    trunk_depth_bonus: float,
    strict_parity_mode: bool,
) -> tuple[list[TreeSupportBranchPlan], list[str]]:
    warnings: list[str] = []
    if not layer_plans:
        return [], warnings

    merge_ratio = max(0.5, min(4.0, float(branch_merge_distance_ratio)))
    growth_ratio = max(1.0, min(2.0, float(branch_growth_ratio)))
    min_radius = max(0.05, float(min_branch_radius_mm))
    merge_distance = max(min_radius, float(support_spacing_mm) * merge_ratio)
    route_weight = max(0.0, float(parent_weight_route))
    load_weight = max(0.0, float(parent_weight_load))
    root_bonus_weight = max(0.0, float(parent_root_bonus))
    trunk_root_bonus_weight = max(0.0, float(trunk_root_bonus))
    trunk_depth_bonus_weight = max(0.0, float(trunk_depth_bonus))
    strict_mode = bool(strict_parity_mode)

    by_layer: dict[int, LayerSupportPlan] = {int(plan.layer_index): plan for plan in layer_plans}
    graph_by_layer: dict[int, LayerIslandGraph] = {int(graph.layer_index): graph for graph in layer_graphs}
    sorted_layers = sorted(by_layer.keys(), reverse=True)
    active_ids: list[int] = []
    branches: dict[int, TreeSupportBranchPlan] = {}
    next_branch_id = 1

    for layer_index in sorted_layers:
        layer_plan = by_layer[layer_index]
        layer_step = _layer_height_lookup(layer_graphs, layer_index, 0.2)
        current_branch_ids: list[int] = []
        layer_graph = graph_by_layer.get(layer_index)
        blocked_merges = 0

        for region in layer_plan.support_regions:
            if region.path_count <= 0:
                continue
            region_point = Point2(float(region.center_x_mm), float(region.center_y_mm))
            obstacles: list[Polygon] = []
            if layer_graph is not None:
                for obstacle_index, island in enumerate(layer_graph.islands):
                    if obstacle_index == int(region.island_index):
                        continue
                    obstacles.append(island.outer)

            best_id: int | None = None
            best_dist = float("inf")
            best_path: list[Point2] = []
            best_path_length = float("inf")
            best_path_collision_avoided = False
            best_parent_score = float("-inf")
            for branch_id in active_ids:
                branch = branches[branch_id]
                dist = _tree_distance(region.center_x_mm, region.center_y_mm, branch.x_mm, branch.y_mm)
                if dist > merge_distance:
                    continue
                target_point = Point2(float(branch.x_mm), float(branch.y_mm))
                path, collision_avoided, blocked, path_length = _route_branch_connection(
                    start=region_point,
                    target=target_point,
                    obstacles=obstacles,
                    base_step_mm=max(min_radius, support_spacing_mm * 0.6),
                )
                if blocked:
                    branch.blocked_collision_count = int(branch.blocked_collision_count + 1)
                    continue
                waypoint_count = max(0, len(path) - 2)
                parent_score = _parent_candidate_score(
                    branch,
                    direct_distance_mm=float(dist),
                    routed_distance_mm=float(path_length),
                    waypoint_count=int(waypoint_count),
                    collision_avoided=bool(collision_avoided),
                    support_spacing_mm=float(support_spacing_mm),
                    min_branch_radius_mm=float(min_radius),
                    route_weight=route_weight,
                    load_weight=load_weight,
                    root_bonus_weight=root_bonus_weight,
                )
                if (
                    parent_score > best_parent_score + EPSILON
                    or (
                        abs(parent_score - best_parent_score) <= EPSILON
                        and path_length < best_path_length - EPSILON
                    )
                ):
                    best_parent_score = float(parent_score)
                    best_path_length = float(path_length)
                    best_path_collision_avoided = bool(collision_avoided)
                    best_path = path
                    best_dist = dist
                    best_id = branch_id

            if best_id is not None:
                parent_branch = branches[best_id]
                parent_branch.tip_layer_index = int(min(parent_branch.tip_layer_index, layer_index))
                parent_branch.length_mm = float(parent_branch.length_mm + max(layer_step * 0.5, 0.0))
                parent_branch.radius_mm = float(
                    max(min_radius, min(parent_branch.radius_mm * growth_ratio, support_spacing_mm * 1.8))
                )
                parent_branch.connected_region_count = int(parent_branch.connected_region_count + 1)
                parent_branch.selection_score = float(max(parent_branch.selection_score, best_parent_score))
                if best_dist < float("inf"):
                    parent_branch.reroute_cost_mm = float(
                        max(parent_branch.reroute_cost_mm, max(0.0, float(best_path_length - best_dist)))
                    )
                if parent_branch.parent_branch_id is None:
                    parent_branch.trunk_assignment = "trunk"

                should_spawn_child = (
                    best_dist >= (merge_distance * 0.55)
                    or best_path_collision_avoided
                    or len(best_path) > 2
                    or best_parent_score < 0.5
                )
                if should_spawn_child:
                    branch_id = next_branch_id
                    next_branch_id += 1
                    parent_branch_id: int | None = int(best_id)
                    if _would_create_parent_cycle(
                        branches,
                        child_branch_id=int(branch_id),
                        parent_branch_id=int(best_id),
                    ):
                        parent_branch_id = None
                    child_branch = TreeSupportBranchPlan(
                        branch_id=branch_id,
                        parent_branch_id=parent_branch_id,
                        root_layer_index=int(layer_index),
                        tip_layer_index=int(layer_index),
                        x_mm=float(region.center_x_mm),
                        y_mm=float(region.center_y_mm),
                        radius_mm=float(max(min_radius, parent_branch.radius_mm * 0.8)),
                        length_mm=float(max(layer_step, best_path_length * 0.4)),
                        connected_region_count=1,
                        waypoint_count=max(0, len(best_path) - 2),
                        collision_avoidance_count=1 if best_path_collision_avoided else 0,
                        blocked_collision_count=0,
                        pruned=False,
                        prune_layer_index=None,
                        selection_score=float(max(0.0, best_parent_score)),
                        reroute_cost_mm=float(max(0.0, best_path_length - max(0.0, float(best_dist)))),
                        trunk_assignment="child" if parent_branch_id is not None else "root",
                        merged_branch_ids=[],
                    )
                    child_branch.load_score = _branch_load_score(
                        child_branch,
                        support_spacing_mm=float(support_spacing_mm),
                        min_branch_radius_mm=float(min_radius),
                    )
                    branches[branch_id] = child_branch
                    region.tree_primary_branch_id = int(branch_id)
                    region.tree_branch_count = 1
                    region.tree_growth_depth_layers = 1
                    current_branch_ids.append(branch_id)
                    if parent_branch_id is not None:
                        layer_plan.tree_parent_assignment_count = int(layer_plan.tree_parent_assignment_count + 1)
                else:
                    parent_branch.length_mm = float(parent_branch.length_mm + max(layer_step, best_path_length))
                    parent_branch.x_mm = float(region.center_x_mm)
                    parent_branch.y_mm = float(region.center_y_mm)
                    if best_path_collision_avoided:
                        parent_branch.collision_avoidance_count = int(parent_branch.collision_avoidance_count + 1)
                        parent_branch.waypoint_count = int(parent_branch.waypoint_count + max(0, len(best_path) - 2))
                    region.tree_primary_branch_id = int(best_id)
                    region.tree_branch_count = 1
                    region.tree_growth_depth_layers = int(max(1, parent_branch.root_layer_index - layer_index + 1))
                    parent_branch.load_score = _branch_load_score(
                        parent_branch,
                        support_spacing_mm=float(support_spacing_mm),
                        min_branch_radius_mm=float(min_radius),
                    )
                    if parent_branch.parent_branch_id is None:
                        parent_branch.trunk_assignment = "trunk"
                    else:
                        parent_branch.trunk_assignment = "child"
                    current_branch_ids.append(best_id)

                if best_path_collision_avoided:
                    layer_plan.tree_collision_avoid_count = int(layer_plan.tree_collision_avoid_count + 1)
                if best_dist < float("inf"):
                    direct_length = max(0.0, float(best_dist))
                    region.tree_route_detour_mm = float(max(0.0, best_path_length - direct_length))
                region.tree_collision_avoided = bool(best_path_collision_avoided)
                region.tree_route_waypoint_count = max(0, len(best_path) - 2)
                region.tree_pruned = False
            else:
                branch_id = next_branch_id
                next_branch_id += 1
                branch = TreeSupportBranchPlan(
                    branch_id=branch_id,
                    parent_branch_id=None,
                    root_layer_index=int(layer_index),
                    tip_layer_index=int(layer_index),
                    x_mm=float(region.center_x_mm),
                    y_mm=float(region.center_y_mm),
                    radius_mm=float(max(min_radius, support_spacing_mm * 0.25)),
                    length_mm=float(max(layer_step, min_radius)),
                    connected_region_count=1,
                    waypoint_count=0,
                    collision_avoidance_count=0,
                    blocked_collision_count=0,
                    pruned=False,
                    prune_layer_index=None,
                    trunk_assignment="root",
                    merged_branch_ids=[],
                )
                branch.load_score = _branch_load_score(
                    branch,
                    support_spacing_mm=float(support_spacing_mm),
                    min_branch_radius_mm=float(min_radius),
                )
                branch.selection_score = float(branch.load_score)
                branches[branch_id] = branch
                region.tree_primary_branch_id = int(branch_id)
                region.tree_branch_count = 1
                region.tree_growth_depth_layers = 1
                region.tree_collision_avoided = False
                region.tree_route_waypoint_count = 0
                region.tree_route_detour_mm = 0.0
                region.tree_pruned = False
                current_branch_ids.append(branch_id)

        unique_current = sorted(set(current_branch_ids))
        merged_ids: set[int] = set()
        merged_into: dict[int, int] = {}
        merge_obstacles = [island.outer for island in layer_graph.islands] if layer_graph is not None else []
        for index, seed_branch_id in enumerate(unique_current):
            if seed_branch_id in merged_ids:
                continue
            trunk_id = int(seed_branch_id)
            trunk = branches[trunk_id]
            for other_id in unique_current[index + 1 :]:
                if other_id in merged_ids:
                    continue
                if other_id == trunk_id:
                    continue
                other = branches[other_id]
                dist = _tree_distance(trunk.x_mm, trunk.y_mm, other.x_mm, other.y_mm)
                if dist > merge_distance * 0.7:
                    continue
                trunk_point = Point2(float(trunk.x_mm), float(trunk.y_mm))
                other_point = Point2(float(other.x_mm), float(other.y_mm))
                merge_path, merge_collision_avoided, merge_blocked, merge_path_length = _route_branch_connection(
                    start=trunk_point,
                    target=other_point,
                    obstacles=merge_obstacles,
                    base_step_mm=max(min_radius, support_spacing_mm * 0.55),
                )
                if merge_blocked:
                    trunk.blocked_collision_count = int(trunk.blocked_collision_count + 1)
                    other.blocked_collision_count = int(other.blocked_collision_count + 1)
                    blocked_merges += 1
                    continue
                if merge_path_length > (dist * 2.35) + max(min_radius, support_spacing_mm * 0.6):
                    trunk.blocked_collision_count = int(trunk.blocked_collision_count + 1)
                    other.blocked_collision_count = int(other.blocked_collision_count + 1)
                    blocked_merges += 1
                    continue

                trunk_score = _trunk_candidate_score(
                    trunk,
                    support_spacing_mm=float(support_spacing_mm),
                    min_branch_radius_mm=float(min_radius),
                    root_bonus_weight=trunk_root_bonus_weight,
                    depth_bonus_weight=trunk_depth_bonus_weight,
                )
                other_score = _trunk_candidate_score(
                    other,
                    support_spacing_mm=float(support_spacing_mm),
                    min_branch_radius_mm=float(min_radius),
                    root_bonus_weight=trunk_root_bonus_weight,
                    depth_bonus_weight=trunk_depth_bonus_weight,
                )
                if other_score > trunk_score + 0.03:
                    old_trunk_id = int(trunk_id)
                    trunk_id = int(other_id)
                    trunk = branches[trunk_id]
                    other = branches[old_trunk_id]
                    trunk_score, other_score = other_score, trunk_score

                trunk.radius_mm = float(min(support_spacing_mm * 2.0, trunk.radius_mm + (other.radius_mm * 0.35)))
                trunk.length_mm = float(max(trunk.length_mm, other.length_mm) + (layer_step * 0.5))
                trunk.connected_region_count += int(other.connected_region_count)
                trunk.waypoint_count = int(trunk.waypoint_count + other.waypoint_count)
                trunk.collision_avoidance_count = int(trunk.collision_avoidance_count + other.collision_avoidance_count)
                trunk.selection_score = float(max(trunk.selection_score, trunk_score, other_score))
                trunk.reroute_cost_mm = float(max(trunk.reroute_cost_mm, max(0.0, merge_path_length - dist)))
                trunk.trunk_assignment = "trunk"
                other.selection_score = float(max(other.selection_score, other_score))
                other.reroute_cost_mm = float(max(other.reroute_cost_mm, max(0.0, merge_path_length - dist)))
                other.trunk_assignment = "merged"
                if merge_collision_avoided:
                    trunk.collision_avoidance_count = int(trunk.collision_avoidance_count + 1)
                    trunk.waypoint_count = int(trunk.waypoint_count + max(0, len(merge_path) - 2))
                    layer_plan.tree_collision_avoid_count = int(layer_plan.tree_collision_avoid_count + 1)
                if other.parent_branch_id != int(trunk.branch_id) and not _would_create_parent_cycle(
                    branches,
                    child_branch_id=int(other.branch_id),
                    parent_branch_id=int(trunk.branch_id),
                ):
                    other.parent_branch_id = int(trunk.branch_id)
                    layer_plan.tree_parent_assignment_count = int(layer_plan.tree_parent_assignment_count + 1)
                trunk.merged_branch_ids.append(int(other.branch_id))
                merged_ids.add(int(other.branch_id))
                merged_into[int(other.branch_id)] = int(trunk.branch_id)
                layer_plan.tree_merge_count += 1

        for region in layer_plan.support_regions:
            branch_id = region.tree_primary_branch_id
            if branch_id is None:
                continue
            if int(branch_id) in merged_ids or int(branch_id) in merged_into:
                replacement = _resolve_merge_replacement(merged_into, int(branch_id))
                if replacement not in merged_ids:
                    region.tree_primary_branch_id = int(replacement)
            if layer_plan.tree_merge_count > 0:
                region.tree_merge_count = int(layer_plan.tree_merge_count)

        surviving = [branch_id for branch_id in unique_current if branch_id not in merged_ids]
        stale_from_previous = [branch_id for branch_id in active_ids if branch_id not in unique_current and branch_id not in merged_ids]
        next_active: list[int] = list(surviving)
        for branch_id in stale_from_previous:
            branch = branches[branch_id]
            if branch.pruned:
                continue
            low_signal = branch.connected_region_count <= 1 and branch.length_mm <= (support_spacing_mm * 1.5)
            collision_saturated = branch.blocked_collision_count >= 2
            child_redundant = (
                branch.parent_branch_id is not None
                and branch.connected_region_count <= 1
                and branch.blocked_collision_count >= 1
            )
            if active_ids:
                nearest_parent: int | None = None
                nearest_parent_dist = float("inf")
                nearest_parent_path_length = float("inf")
                nearest_parent_collision_avoided = False
                nearest_parent_score = float("-inf")
                blocked_reparent_attempts = 0
                for candidate_id in active_ids:
                    if candidate_id == branch_id:
                        continue
                    candidate_branch = branches[candidate_id]
                    if candidate_branch.pruned:
                        continue
                    distance = _tree_distance(branch.x_mm, branch.y_mm, candidate_branch.x_mm, candidate_branch.y_mm)
                    if distance > (merge_distance * 1.9):
                        continue
                    reparent_path, reparent_collision_avoided, reparent_blocked, reparent_path_length = _route_branch_connection(
                        start=Point2(float(branch.x_mm), float(branch.y_mm)),
                        target=Point2(float(candidate_branch.x_mm), float(candidate_branch.y_mm)),
                        obstacles=merge_obstacles,
                        base_step_mm=max(min_radius, support_spacing_mm * 0.55),
                    )
                    if reparent_blocked:
                        blocked_reparent_attempts += 1
                        continue
                    if reparent_path_length > (distance * 2.6) + max(min_radius, support_spacing_mm * 0.8):
                        blocked_reparent_attempts += 1
                        continue
                    waypoint_count = max(0, len(reparent_path) - 2)
                    parent_score = _parent_candidate_score(
                        candidate_branch,
                        direct_distance_mm=float(distance),
                        routed_distance_mm=float(reparent_path_length),
                        waypoint_count=int(waypoint_count),
                        collision_avoided=bool(reparent_collision_avoided),
                        support_spacing_mm=float(support_spacing_mm),
                        min_branch_radius_mm=float(min_radius),
                        route_weight=route_weight,
                        load_weight=load_weight,
                        root_bonus_weight=root_bonus_weight,
                    )
                    if (
                        parent_score > nearest_parent_score + EPSILON
                        or (
                            abs(parent_score - nearest_parent_score) <= EPSILON
                            and reparent_path_length < nearest_parent_path_length - EPSILON
                        )
                    ):
                        nearest_parent_score = float(parent_score)
                        nearest_parent_path_length = float(reparent_path_length)
                        nearest_parent_dist = distance
                        nearest_parent = candidate_id
                        nearest_parent_collision_avoided = bool(reparent_collision_avoided)
                if blocked_reparent_attempts > 0:
                    branch.blocked_collision_count = int(branch.blocked_collision_count + blocked_reparent_attempts)
                if (
                    nearest_parent is not None
                    and nearest_parent_dist <= (merge_distance * 1.9)
                    and nearest_parent_score >= 0.42
                ):
                    if branch.parent_branch_id != int(nearest_parent) and not _would_create_parent_cycle(
                        branches,
                        child_branch_id=int(branch.branch_id),
                        parent_branch_id=int(nearest_parent),
                    ):
                        branch.parent_branch_id = int(nearest_parent)
                        layer_plan.tree_parent_assignment_count = int(layer_plan.tree_parent_assignment_count + 1)
                    branch.selection_score = float(max(branch.selection_score, nearest_parent_score))
                    branch.reroute_cost_mm = float(
                        max(branch.reroute_cost_mm, max(0.0, nearest_parent_path_length - nearest_parent_dist))
                    )
                    branch.trunk_assignment = "child"
                    if nearest_parent_collision_avoided:
                        branch.collision_avoidance_count = int(branch.collision_avoidance_count + 1)
                        layer_plan.tree_collision_avoid_count = int(layer_plan.tree_collision_avoid_count + 1)
            if low_signal or collision_saturated or child_redundant:
                branch.pruned = True
                branch.prune_layer_index = int(layer_index)
                branch.trunk_assignment = "pruned"
                layer_plan.tree_pruned_branch_count = int(layer_plan.tree_pruned_branch_count + 1)
                continue
            branch.length_mm = float(branch.length_mm + max(layer_step * 0.5, 0.0))
            branch.load_score = _branch_load_score(
                branch,
                support_spacing_mm=float(support_spacing_mm),
                min_branch_radius_mm=float(min_radius),
            )
            next_active.append(branch_id)

        active_ids = sorted(set(next_active))
        layer_plan.tree_branch_count = len(active_ids)
        for region in layer_plan.support_regions:
            branch_id = region.tree_primary_branch_id
            if branch_id is None:
                continue
            branch = branches.get(int(branch_id))
            if branch is None:
                continue
            region.tree_pruned = bool(branch.pruned)
        for active_branch_id in active_ids:
            active_branch = branches[active_branch_id]
            if active_branch.pruned:
                active_branch.trunk_assignment = "pruned"
            elif active_branch.parent_branch_id is None:
                active_branch.trunk_assignment = "trunk"
            else:
                active_branch.trunk_assignment = "child"
        layer_plan.tree_trunk_count = sum(
            1 for branch_id in active_ids if branches[branch_id].parent_branch_id is None and not branches[branch_id].pruned
        )
        parent_count = sum(
            1 for branch_id in active_ids if branches[branch_id].parent_branch_id is not None and not branches[branch_id].pruned
        )
        if parent_count > layer_plan.tree_parent_assignment_count:
            layer_plan.tree_parent_assignment_count = int(parent_count)
        if layer_plan.tree_branch_count > 0:
            warnings.append(f"layer_{layer_index}:tree_support_branches={layer_plan.tree_branch_count}")
        if layer_plan.tree_parent_assignment_count > 0:
            warnings.append(f"layer_{layer_index}:tree_parent_assignments={layer_plan.tree_parent_assignment_count}")
        if layer_plan.tree_trunk_count > 0:
            warnings.append(f"layer_{layer_index}:tree_trunks={layer_plan.tree_trunk_count}")
        if layer_plan.tree_collision_avoid_count > 0:
            warnings.append(f"layer_{layer_index}:tree_collision_avoided={layer_plan.tree_collision_avoid_count}")
        if layer_plan.tree_pruned_branch_count > 0:
            warnings.append(f"layer_{layer_index}:tree_pruned_branches={layer_plan.tree_pruned_branch_count}")
        if blocked_merges > 0:
            warnings.append(f"layer_{layer_index}:tree_merge_blocked_by_collision={blocked_merges}")

    for branch in branches.values():
        branch.load_score = _branch_load_score(
            branch,
            support_spacing_mm=float(support_spacing_mm),
            min_branch_radius_mm=float(min_radius),
        )
        if branch.pruned:
            branch.trunk_assignment = "pruned"
        elif branch.trunk_assignment == "merged":
            branch.trunk_assignment = "merged"
        elif branch.parent_branch_id is None:
            branch.trunk_assignment = "trunk" if strict_mode else branch.trunk_assignment
        else:
            branch.trunk_assignment = "child"

    out: list[TreeSupportBranchPlan] = []
    for branch_id in sorted(branches.keys()):
        out.append(branches[branch_id])
    return out, warnings


def build_support_plan(
    layer_graphs: Sequence[LayerIslandGraph],
    *,
    vertical_edges: Sequence[VerticalAdjacencyEdge] = (),
    support_enabled: bool,
    support_type: str,
    support_density_percent: float,
    support_spacing_mm: float,
    support_xy_gap_mm: float,
    support_z_gap_mm: float,
    support_interface_layers: int,
    extrusion_width_mm: float,
    tree_branch_merge_distance_ratio: float = 1.2,
    tree_branch_growth_ratio: float = 1.08,
    tree_min_branch_radius_mm: float = 0.3,
    tree_parent_weight_route: float = 0.56,
    tree_parent_weight_load: float = 0.40,
    tree_parent_root_bonus: float = 0.06,
    tree_trunk_root_bonus: float = 0.08,
    tree_trunk_depth_bonus: float = 0.07,
    tree_support_strict_parity_mode: bool = False,
    max_workers: int = 1,
) -> tuple[list[LayerSupportPlan], SupportPlanningReport]:
    graphs = _validate_layer_graphs(layer_graphs)
    edges = _validate_vertical_edges(vertical_edges)
    normalized_type = _validate_support_type(support_type)
    density_percent = _validate_ratio(
        support_density_percent,
        code="SUPPORT_DENSITY_PERCENT_INVALID",
        minimum=0.0,
        maximum=100.0,
    )
    spacing_mm = _validate_positive(support_spacing_mm, code="SUPPORT_SPACING_INVALID")
    xy_gap_mm = _validate_non_negative(support_xy_gap_mm, code="SUPPORT_XY_GAP_INVALID")
    z_gap_mm = _validate_non_negative(support_z_gap_mm, code="SUPPORT_Z_GAP_INVALID")
    interface_layers = _validate_interface_layers(support_interface_layers)
    width_mm = _validate_positive(extrusion_width_mm, code="SUPPORT_EXTRUSION_WIDTH_INVALID")
    branch_merge_ratio = _validate_ratio(
        tree_branch_merge_distance_ratio,
        code="SUPPORT_TREE_BRANCH_MERGE_RATIO_INVALID",
        minimum=0.5,
        maximum=4.0,
    )
    branch_growth_ratio = _validate_ratio(
        tree_branch_growth_ratio,
        code="SUPPORT_TREE_BRANCH_GROWTH_RATIO_INVALID",
        minimum=1.0,
        maximum=2.0,
    )
    min_branch_radius_mm = _validate_positive(tree_min_branch_radius_mm, code="SUPPORT_TREE_MIN_BRANCH_RADIUS_INVALID")
    parent_weight_route = _validate_ratio(
        tree_parent_weight_route,
        code="SUPPORT_TREE_PARENT_ROUTE_WEIGHT_INVALID",
        minimum=0.0,
        maximum=2.0,
    )
    parent_weight_load = _validate_ratio(
        tree_parent_weight_load,
        code="SUPPORT_TREE_PARENT_LOAD_WEIGHT_INVALID",
        minimum=0.0,
        maximum=2.0,
    )
    parent_root_bonus = _validate_ratio(
        tree_parent_root_bonus,
        code="SUPPORT_TREE_PARENT_ROOT_BONUS_INVALID",
        minimum=0.0,
        maximum=1.0,
    )
    trunk_root_bonus = _validate_ratio(
        tree_trunk_root_bonus,
        code="SUPPORT_TREE_TRUNK_ROOT_BONUS_INVALID",
        minimum=0.0,
        maximum=1.0,
    )
    trunk_depth_bonus = _validate_ratio(
        tree_trunk_depth_bonus,
        code="SUPPORT_TREE_TRUNK_DEPTH_BONUS_INVALID",
        minimum=0.0,
        maximum=1.0,
    )

    warnings: list[str] = []
    if not graphs:
        warnings.append("support_planning:no_layers")
    if normalized_type == SUPPORT_TYPE_TREE:
        warnings.append("support_planning:tree_mode_mvp_estimate")
        warnings.append("support_planning:tree_branch_graph_enabled")
        if bool(tree_support_strict_parity_mode):
            warnings.append("support_planning:tree_strict_parity_mode")

    density_ratio = density_percent / 100.0
    if support_enabled and density_ratio <= EPSILON:
        warnings.append("support_planning:density_zero")

    supported_map = _supported_islands_by_layer(edges)
    graph_lookup = _layer_lookup(graphs)

    def _build_layer(graph: LayerIslandGraph) -> tuple[LayerSupportPlan, list[str]]:
        layer_warnings: list[str] = []
        unsupported_indices: list[int] = []
        if graph.layer_index > 0:
            supported_indices = supported_map.get(graph.layer_index, set())
            for island_index in range(graph.island_count):
                if island_index not in supported_indices:
                    unsupported_indices.append(island_index)

        regions: list[SupportRegionPlan] = []
        lower_graph = graph_lookup.get(int(graph.layer_index) - 1)
        lower_boundaries: list[Polygon] = [island.outer for island in lower_graph.islands] if lower_graph is not None else []
        if support_enabled and density_ratio > EPSILON:
            for island_index in unsupported_indices:
                island = graph.islands[island_index]
                width = float(island.bounds.width)
                height = float(island.bounds.height)
                if width <= EPSILON or height <= EPSILON:
                    layer_warnings.append(f"layer_{graph.layer_index}:island_{island_index}:degenerate_bounds")
                    continue
                region_polygons = _expand_support_footprint(
                    island=island,
                    xy_gap_mm=xy_gap_mm,
                    support_spacing_mm=spacing_mm,
                    extrusion_width_mm=width_mm,
                    boundary_polygons=lower_boundaries,
                )
                if not region_polygons:
                    layer_warnings.append(f"layer_{graph.layer_index}:island_{island_index}:footprint_empty")
                    continue
                regions.append(
                    _estimate_region(
                        layer_index=graph.layer_index,
                        island_index=island_index,
                        polygons=region_polygons,
                        support_type=normalized_type,
                        support_interface_layers=interface_layers,
                        support_spacing_mm=spacing_mm,
                        support_density_ratio=density_ratio,
                        extrusion_width_mm=width_mm,
                    )
                )
        elif support_enabled and density_ratio <= EPSILON and unsupported_indices:
            layer_warnings.append(
                f"layer_{graph.layer_index}:unsupported_islands_without_density:{len(unsupported_indices)}"
            )

        support_region_count = len(regions)
        support_path_count = sum(region.path_count for region in regions)
        support_path_length = float(sum(region.path_length_mm for region in regions))
        interface_path_count = sum(region.interface_path_count for region in regions)

        return (
            LayerSupportPlan(
                layer_index=graph.layer_index,
                z_height_mm=float(graph.z_height_mm),
                island_count=graph.island_count,
                unsupported_island_count=len(unsupported_indices),
                support_region_count=support_region_count,
                support_path_count=support_path_count,
                support_path_length_mm=support_path_length,
                interface_path_count=interface_path_count,
                tree_branch_count=0,
                tree_merge_count=0,
                tree_collision_avoid_count=0,
                tree_pruned_branch_count=0,
                tree_parent_assignment_count=0,
                tree_trunk_count=0,
                support_regions=regions,
            ),
            layer_warnings,
        )

    worker_count = max(1, min(int(max_workers), len(graphs) if graphs else 1))
    if worker_count > 1 and len(graphs) > 1:
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            results = list(executor.map(_build_layer, graphs))
    else:
        results = [_build_layer(graph) for graph in graphs]

    layer_plans: list[LayerSupportPlan] = []
    island_count_total = 0
    unsupported_island_count_total = 0
    support_region_count_total = 0
    support_path_count_total = 0
    support_path_length_mm_total = 0.0
    interface_path_count_total = 0
    tree_branch_count_total = 0
    tree_merge_count_total = 0
    tree_collision_avoid_count_total = 0
    tree_pruned_branch_count_total = 0
    tree_parent_assignment_count_total = 0
    tree_trunk_count_total = 0

    for layer_plan, layer_warnings in results:
        layer_plans.append(layer_plan)
        warnings.extend(layer_warnings)
        island_count_total += layer_plan.island_count
        unsupported_island_count_total += layer_plan.unsupported_island_count
        support_region_count_total += layer_plan.support_region_count
        support_path_count_total += layer_plan.support_path_count
        support_path_length_mm_total += layer_plan.support_path_length_mm
        interface_path_count_total += layer_plan.interface_path_count

    layer_plans.sort(key=lambda plan: int(plan.layer_index))

    tree_branches: list[TreeSupportBranchPlan] = []
    if support_enabled and density_ratio > EPSILON and normalized_type == SUPPORT_TYPE_TREE:
        tree_branches, tree_warnings = _apply_tree_branch_heuristics(
            layer_plans=layer_plans,
            layer_graphs=graphs,
            support_spacing_mm=spacing_mm,
            branch_merge_distance_ratio=branch_merge_ratio,
            branch_growth_ratio=branch_growth_ratio,
            min_branch_radius_mm=min_branch_radius_mm,
            parent_weight_route=parent_weight_route,
            parent_weight_load=parent_weight_load,
            parent_root_bonus=parent_root_bonus,
            trunk_root_bonus=trunk_root_bonus,
            trunk_depth_bonus=trunk_depth_bonus,
            strict_parity_mode=bool(tree_support_strict_parity_mode),
        )
        warnings.extend(tree_warnings)

    for layer_plan in layer_plans:
        tree_branch_count_total += int(layer_plan.tree_branch_count)
        tree_merge_count_total += int(layer_plan.tree_merge_count)
        tree_collision_avoid_count_total += int(layer_plan.tree_collision_avoid_count)
        tree_pruned_branch_count_total += int(layer_plan.tree_pruned_branch_count)
        tree_parent_assignment_count_total += int(layer_plan.tree_parent_assignment_count)
        tree_trunk_count_total += int(layer_plan.tree_trunk_count)

    branch_load_score_avg = 0.0
    branch_selection_score_avg = 0.0
    branch_reroute_cost_mm_total = 0.0
    branch_trunk_assignment_counts: dict[str, int] = {}
    if tree_branches:
        branch_load_score_avg = float(sum(max(0.0, branch.load_score) for branch in tree_branches) / len(tree_branches))
        branch_selection_score_avg = float(
            sum(max(0.0, branch.selection_score) for branch in tree_branches) / len(tree_branches)
        )
        branch_reroute_cost_mm_total = float(sum(max(0.0, branch.reroute_cost_mm) for branch in tree_branches))
        for branch in tree_branches:
            label = str(branch.trunk_assignment or "unknown")
            branch_trunk_assignment_counts[label] = int(branch_trunk_assignment_counts.get(label, 0) + 1)

    report = SupportPlanningReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        layer_count=len(graphs),
        island_count_total=island_count_total,
        unsupported_island_count_total=unsupported_island_count_total,
        support_enabled=bool(support_enabled),
        support_type=normalized_type,
        support_density_percent=float(density_percent),
        support_spacing_mm=float(spacing_mm),
        support_xy_gap_mm=float(xy_gap_mm),
        support_z_gap_mm=float(z_gap_mm),
        support_interface_layers=interface_layers,
        support_region_count_total=support_region_count_total,
        support_path_count_total=support_path_count_total,
        support_path_length_mm_total=float(support_path_length_mm_total),
        interface_path_count_total=interface_path_count_total,
        tree_branch_count_total=int(tree_branch_count_total),
        tree_merge_count_total=int(tree_merge_count_total),
        tree_collision_avoid_count_total=int(tree_collision_avoid_count_total),
        tree_pruned_branch_count_total=int(tree_pruned_branch_count_total),
        tree_parent_assignment_count_total=int(tree_parent_assignment_count_total),
        tree_trunk_count_total=int(tree_trunk_count_total),
        tree_branch_load_score_avg=float(branch_load_score_avg),
        tree_branch_selection_score_avg=float(branch_selection_score_avg),
        tree_branch_reroute_cost_mm_total=float(branch_reroute_cost_mm_total),
        tree_branch_trunk_assignment_counts=branch_trunk_assignment_counts,
        warning_count=len(warnings),
        warnings=warnings,
        tree_branches=tree_branches,
    )
    return layer_plans, report
