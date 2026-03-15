from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Sequence

from .errors import SlicerV2TravelPlanningError
from .geometry import EPSILON, Island, Point2, Polygon
from .island_graph import LayerIslandGraph
from .line_split import split_line


@dataclass
class TravelMovePlan:
    layer_index: int
    move_index: int
    length_mm: float
    combed: bool
    crosses_wall: bool
    retract: bool
    z_hop: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class LayerTravelPlan:
    layer_index: int
    z_height_mm: float
    perimeter_path_count: int
    infill_path_count: int
    support_path_count: int
    feature_transition_count: int
    move_count: int
    combed_move_count: int
    fallback_move_count: int
    retract_count: int
    z_hop_count: int
    travel_length_mm: float
    moves: list[TravelMovePlan] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class TravelPlanningReport:
    generated_at_utc: str
    layer_count: int
    move_count_total: int
    combed_move_count_total: int
    fallback_move_count_total: int
    retract_count_total: int
    z_hop_count_total: int
    travel_length_mm_total: float
    travel_speed_mm_s: float
    combing_enabled: bool
    combing_max_detour_ratio: float
    retract_enabled: bool
    retract_min_travel_mm: float
    z_hop_enabled: bool
    z_hop_mm: float
    warning_count: int
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _validate_layer_graphs(layer_graphs: Sequence[LayerIslandGraph]) -> list[LayerIslandGraph]:
    graphs = list(layer_graphs)
    for index, graph in enumerate(graphs):
        if not isinstance(graph, LayerIslandGraph):
            raise SlicerV2TravelPlanningError(f"TRAVEL_LAYER_GRAPH_INVALID:{index}")
    return graphs


def _validate_counts(values: Sequence[int], label: str) -> list[int]:
    counts = [int(value) for value in values]
    for index, count in enumerate(counts):
        if count < 0:
            raise SlicerV2TravelPlanningError(f"TRAVEL_FEATURE_COUNT_NEGATIVE:{label}:{index}")
    return counts


def _validate_ratio(value: float, *, code: str, minimum: float, maximum: float) -> float:
    parsed = float(value)
    if parsed < minimum or parsed > maximum:
        raise SlicerV2TravelPlanningError(code)
    return parsed


def _validate_non_negative(value: float, *, code: str) -> float:
    parsed = float(value)
    if parsed < 0.0:
        raise SlicerV2TravelPlanningError(code)
    return parsed


def _base_move_length_mm(layer_index: int, move_index: int) -> float:
    layer_component = float((layer_index % 4) * 0.15)
    move_component = float((move_index % 5) * 0.12)
    return 1.5 + layer_component + move_component


def _feature_points(graph: LayerIslandGraph | None, feature_count: int, layer_index: int) -> list[Point2]:
    count = max(0, int(feature_count))
    if count <= 0:
        return []

    seeds: list[Point2] = []
    if graph is not None and graph.islands:
        for island in graph.islands:
            seeds.append(island.outer.centroid)
        for island in graph.islands:
            bounds = island.bounds
            seeds.extend(
                [
                    Point2(bounds.min_x, bounds.min_y),
                    Point2(bounds.max_x, bounds.min_y),
                    Point2(bounds.max_x, bounds.max_y),
                    Point2(bounds.min_x, bounds.max_y),
                ]
            )

    if not seeds:
        base_x = float(layer_index * 2.3)
        base_y = float(layer_index * 1.7)
        seeds = [
            Point2(base_x, base_y),
            Point2(base_x + 1.5, base_y + 0.8),
            Point2(base_x + 2.0, base_y + 1.6),
        ]

    points: list[Point2] = []
    for index in range(count):
        seed = seeds[index % len(seeds)]
        ring = index // len(seeds)
        if ring <= 0:
            points.append(seed)
            continue
        offset = 0.05 * float(ring)
        points.append(Point2(seed.x + offset, seed.y - offset))
    return points


def _clip_lengths(start: Point2, end: Point2, clip: Sequence[Island | Polygon]) -> tuple[float, float]:
    direct = start.distance_to(end)
    if direct <= EPSILON:
        return (0.0, 0.0)
    if not clip:
        return (0.0, float(direct))

    split = split_line((start, end), clip, closed=False)
    if len(split) < 2:
        return (0.0, float(direct))

    inside = 0.0
    outside = 0.0
    for index in range(len(split) - 1):
        a = split[index]
        b = split[index + 1]
        length = a.p.distance_to(b.p)
        if length <= EPSILON:
            continue
        if a.clipped:
            inside += length
        else:
            outside += length

    measured = inside + outside
    if measured <= EPSILON:
        return (0.0, float(direct))
    scale = direct / measured
    return (float(inside * scale), float(outside * scale))


def _compute_layer_count(
    graphs: Sequence[LayerIslandGraph],
    perimeters: Sequence[int],
    infill: Sequence[int],
    support: Sequence[int],
) -> int:
    return max(len(graphs), len(perimeters), len(infill), len(support))


def _count_or_zero(values: Sequence[int], index: int) -> int:
    if index < 0 or index >= len(values):
        return 0
    return int(values[index])


def build_travel_plan(
    layer_graphs: Sequence[LayerIslandGraph],
    *,
    layer_perimeter_counts: Sequence[int],
    layer_infill_counts: Sequence[int],
    layer_support_counts: Sequence[int],
    travel_speed_mm_s: float,
    combing_enabled: bool,
    combing_max_detour_ratio: float,
    retract_enabled: bool,
    retract_min_travel_mm: float,
    z_hop_enabled: bool,
    z_hop_mm: float,
    max_workers: int = 1,
) -> tuple[list[LayerTravelPlan], TravelPlanningReport]:
    graphs = _validate_layer_graphs(layer_graphs)
    perimeter_counts = _validate_counts(layer_perimeter_counts, "perimeter")
    infill_counts = _validate_counts(layer_infill_counts, "infill")
    support_counts = _validate_counts(layer_support_counts, "support")

    speed_mm_s = _validate_ratio(travel_speed_mm_s, code="TRAVEL_SPEED_INVALID", minimum=1.0, maximum=1000.0)
    detour_ratio = _validate_ratio(
        combing_max_detour_ratio,
        code="TRAVEL_COMBING_DETOUR_RATIO_INVALID",
        minimum=1.0,
        maximum=5.0,
    )
    retract_min = _validate_non_negative(retract_min_travel_mm, code="TRAVEL_RETRACT_MIN_INVALID")
    z_hop_height = _validate_non_negative(z_hop_mm, code="TRAVEL_Z_HOP_HEIGHT_INVALID")

    warnings: list[str] = []
    if not graphs:
        warnings.append("travel_planning:no_layer_graphs")
    if combing_enabled and not graphs:
        warnings.append("travel_planning:combing_requested_without_graphs")
    if z_hop_enabled and z_hop_height <= EPSILON:
        warnings.append("travel_planning:z_hop_enabled_with_zero_height")

    layer_count = _compute_layer_count(graphs, perimeter_counts, infill_counts, support_counts)

    def _build_layer(layer_index: int) -> LayerTravelPlan:
        graph = graphs[layer_index] if layer_index < len(graphs) else None
        perimeter_count = _count_or_zero(perimeter_counts, layer_index)
        infill_count = _count_or_zero(infill_counts, layer_index)
        support_count = _count_or_zero(support_counts, layer_index)

        feature_count = perimeter_count + infill_count + support_count
        transitions = max(0, feature_count - 1)

        adjacency_count = 0
        z_height_mm = float(layer_index)
        if graph is not None:
            adjacency_count = len(graph.adjacency_edges)
            z_height_mm = float(graph.z_height_mm)

        clip: list[Island | Polygon] = []
        if graph is not None:
            clip = list(graph.islands)
        points = _feature_points(graph, feature_count, layer_index)

        moves: list[TravelMovePlan] = []
        combed_count = 0
        fallback_count = 0
        retract_count = 0
        z_hop_count = 0
        layer_length_mm = 0.0

        for move_index in range(transitions):
            start = points[move_index] if move_index < len(points) else Point2(float(layer_index), float(move_index))
            end_idx = move_index + 1
            end = points[end_idx] if end_idx < len(points) else Point2(float(layer_index + 1), float(move_index + 1))

            direct_length = start.distance_to(end)
            if direct_length <= EPSILON:
                direct_length = _base_move_length_mm(layer_index, move_index)

            inside_length, outside_length = _clip_lengths(start, end, clip)
            if inside_length <= EPSILON and outside_length <= EPSILON:
                outside_length = direct_length
            total_clip_length = inside_length + outside_length
            outside_ratio = outside_length / max(total_clip_length, EPSILON)
            inside_ratio = inside_length / max(total_clip_length, EPSILON)
            crosses_wall = outside_ratio > 0.01

            combed = False
            length_mm = direct_length
            if combing_enabled:
                if crosses_wall:
                    if adjacency_count > 0 and inside_ratio >= 0.2:
                        combed = True
                        adjacency_factor = 1.1 + (0.04 * float(adjacency_count % 4)) + (0.12 * outside_ratio)
                        length_mm = direct_length * min(detour_ratio, adjacency_factor)
                    elif inside_ratio >= 0.7:
                        combed = True
                        length_mm = direct_length * min(detour_ratio, 1.05 + (0.08 * outside_ratio))
                    else:
                        length_mm = direct_length * 1.05
                else:
                    combed = True
                    length_mm = direct_length * min(detour_ratio, 1.03)

            retract = bool(retract_enabled and crosses_wall and length_mm >= retract_min)
            z_hop = bool(z_hop_enabled and retract and z_hop_height > EPSILON)

            if combed:
                combed_count += 1
            else:
                fallback_count += 1
            if retract:
                retract_count += 1
            if z_hop:
                z_hop_count += 1

            layer_length_mm += length_mm
            moves.append(
                TravelMovePlan(
                    layer_index=layer_index,
                    move_index=move_index,
                    length_mm=float(length_mm),
                    combed=combed,
                    crosses_wall=crosses_wall,
                    retract=retract,
                    z_hop=z_hop,
                )
            )

        return LayerTravelPlan(
            layer_index=layer_index,
            z_height_mm=z_height_mm,
            perimeter_path_count=perimeter_count,
            infill_path_count=infill_count,
            support_path_count=support_count,
            feature_transition_count=transitions,
            move_count=transitions,
            combed_move_count=combed_count,
            fallback_move_count=fallback_count,
            retract_count=retract_count,
            z_hop_count=z_hop_count,
            travel_length_mm=float(layer_length_mm),
            moves=moves,
        )

    worker_count = max(1, min(int(max_workers), layer_count if layer_count > 0 else 1))
    if worker_count > 1 and layer_count > 1:
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            layer_plans = list(executor.map(_build_layer, range(layer_count)))
    else:
        layer_plans = [_build_layer(layer_index) for layer_index in range(layer_count)]

    layer_plans.sort(key=lambda plan: int(plan.layer_index))
    move_count_total = sum(plan.move_count for plan in layer_plans)
    combed_move_count_total = sum(plan.combed_move_count for plan in layer_plans)
    fallback_move_count_total = sum(plan.fallback_move_count for plan in layer_plans)
    retract_count_total = sum(plan.retract_count for plan in layer_plans)
    z_hop_count_total = sum(plan.z_hop_count for plan in layer_plans)
    travel_length_mm_total = sum(plan.travel_length_mm for plan in layer_plans)

    report = TravelPlanningReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        layer_count=layer_count,
        move_count_total=move_count_total,
        combed_move_count_total=combed_move_count_total,
        fallback_move_count_total=fallback_move_count_total,
        retract_count_total=retract_count_total,
        z_hop_count_total=z_hop_count_total,
        travel_length_mm_total=float(travel_length_mm_total),
        travel_speed_mm_s=float(speed_mm_s),
        combing_enabled=bool(combing_enabled),
        combing_max_detour_ratio=float(detour_ratio),
        retract_enabled=bool(retract_enabled),
        retract_min_travel_mm=float(retract_min),
        z_hop_enabled=bool(z_hop_enabled),
        z_hop_mm=float(z_hop_height),
        warning_count=len(warnings),
        warnings=warnings,
    )
    return layer_plans, report
