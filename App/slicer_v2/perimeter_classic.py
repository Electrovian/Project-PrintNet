from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from math import hypot
from typing import Sequence

from .errors import SlicerV2PerimeterClassicError
from .geometry import EPSILON, Point2, Polygon
from .island_graph import LayerIslandGraph


WALL_SEQUENCE_OUTER_TO_INNER = "outer_to_inner"
WALL_SEQUENCE_INNER_TO_OUTER = "inner_to_outer"
ALLOWED_WALL_SEQUENCES = {WALL_SEQUENCE_OUTER_TO_INNER, WALL_SEQUENCE_INNER_TO_OUTER}


@dataclass
class PerimeterLoopPlan:
    layer_index: int
    island_index: int
    role: str
    shell_index: int
    point_count: int
    path_length_mm: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class LayerPerimeterPlan:
    layer_index: int
    z_height_mm: float
    loop_count: int
    path_length_mm: float
    loops: list[PerimeterLoopPlan] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["path_count"] = self.loop_count
        return payload


@dataclass
class PerimeterClassicReport:
    generated_at_utc: str
    layer_count: int
    island_count_total: int
    perimeter_count_requested: int
    wall_sequence: str
    loop_count_total: int
    path_length_mm_total: float
    warning_count: int
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _validate_perimeter_count(perimeter_count: int) -> int:
    if perimeter_count < 1:
        raise SlicerV2PerimeterClassicError("PERIMETER_CLASSIC_COUNT_INVALID")
    if perimeter_count > 20:
        raise SlicerV2PerimeterClassicError("PERIMETER_CLASSIC_COUNT_EXCESSIVE")
    return perimeter_count


def _validate_line_width(line_width_mm: float) -> float:
    if line_width_mm <= EPSILON:
        raise SlicerV2PerimeterClassicError("PERIMETER_CLASSIC_LINE_WIDTH_INVALID")
    return line_width_mm


def _validate_wall_sequence(wall_sequence: str) -> str:
    if wall_sequence not in ALLOWED_WALL_SEQUENCES:
        raise SlicerV2PerimeterClassicError(f"PERIMETER_CLASSIC_WALL_SEQUENCE_INVALID:{wall_sequence}")
    return wall_sequence


def _validate_layer_graphs(layer_graphs: Sequence[LayerIslandGraph]) -> list[LayerIslandGraph]:
    graphs = list(layer_graphs)
    for index, graph in enumerate(graphs):
        if not isinstance(graph, LayerIslandGraph):
            raise SlicerV2PerimeterClassicError(f"PERIMETER_CLASSIC_LAYER_GRAPH_INVALID:{index}")
    return graphs


def _radial_offset_polygon(polygon: Polygon, delta_mm: float) -> Polygon | None:
    if abs(delta_mm) <= EPSILON:
        return polygon

    center = polygon.centroid
    shifted_points: list[Point2] = []
    for point in polygon.points:
        dx = point.x - center.x
        dy = point.y - center.y
        distance = hypot(dx, dy)
        if distance <= EPSILON:
            return None
        scaled_distance = distance + delta_mm
        if scaled_distance <= EPSILON:
            return None
        scale = scaled_distance / distance
        shifted_points.append(Point2(center.x + dx * scale, center.y + dy * scale))

    try:
        return Polygon(tuple(shifted_points)).with_winding(clockwise=polygon.is_clockwise)
    except Exception:
        return None


def _shell_indices(shell_count: int, wall_sequence: str) -> list[int]:
    if wall_sequence == WALL_SEQUENCE_INNER_TO_OUTER:
        return list(range(shell_count - 1, -1, -1))
    return list(range(shell_count))


def _build_loops_for_polygon(
    *,
    layer_index: int,
    island_index: int,
    role: str,
    polygon: Polygon,
    shell_count: int,
    line_width_mm: float,
    wall_sequence: str,
    warnings: list[str],
) -> list[PerimeterLoopPlan]:
    loops: list[PerimeterLoopPlan] = []
    indices = _shell_indices(shell_count, wall_sequence)
    for shell_index in indices:
        if role == "outer":
            delta_mm = -float(shell_index) * line_width_mm
        elif role == "hole":
            delta_mm = float(shell_index) * line_width_mm
        else:
            raise SlicerV2PerimeterClassicError(f"PERIMETER_CLASSIC_ROLE_INVALID:{role}")

        offset_polygon = _radial_offset_polygon(polygon, delta_mm)
        if offset_polygon is None:
            warnings.append(
                f"layer_{layer_index}:island_{island_index}:{role}:shell_{shell_index}:offset_failed"
            )
            continue
        loops.append(
            PerimeterLoopPlan(
                layer_index=layer_index,
                island_index=island_index,
                role=role,
                shell_index=shell_index,
                point_count=len(offset_polygon.points),
                path_length_mm=float(offset_polygon.perimeter),
            )
        )
    return loops


def build_classic_perimeters(
    layer_graphs: Sequence[LayerIslandGraph],
    *,
    perimeter_count: int,
    line_width_mm: float,
    wall_sequence: str = WALL_SEQUENCE_OUTER_TO_INNER,
    first_layer_single_wall: bool = False,
    max_workers: int = 1,
) -> tuple[list[LayerPerimeterPlan], PerimeterClassicReport]:
    shells_requested = _validate_perimeter_count(int(perimeter_count))
    width = _validate_line_width(float(line_width_mm))
    sequence = _validate_wall_sequence(str(wall_sequence))
    graphs = _validate_layer_graphs(layer_graphs)

    def _build_layer(layer_graph: LayerIslandGraph) -> tuple[LayerPerimeterPlan, list[str], int]:
        layer_warnings: list[str] = []
        shell_count_for_layer = shells_requested
        if first_layer_single_wall and layer_graph.layer_index == 0:
            shell_count_for_layer = 1

        loops_for_layer: list[PerimeterLoopPlan] = []
        for island_index, island in enumerate(layer_graph.islands):
            loops_for_layer.extend(
                _build_loops_for_polygon(
                    layer_index=layer_graph.layer_index,
                    island_index=island_index,
                    role="outer",
                    polygon=island.outer,
                    shell_count=shell_count_for_layer,
                    line_width_mm=width,
                    wall_sequence=sequence,
                    warnings=layer_warnings,
                )
            )
            for hole in island.holes:
                loops_for_layer.extend(
                    _build_loops_for_polygon(
                        layer_index=layer_graph.layer_index,
                        island_index=island_index,
                        role="hole",
                        polygon=hole,
                        shell_count=shell_count_for_layer,
                        line_width_mm=width,
                        wall_sequence=sequence,
                        warnings=layer_warnings,
                    )
                )

        layer_length = sum(loop.path_length_mm for loop in loops_for_layer)
        return (
            LayerPerimeterPlan(
                layer_index=layer_graph.layer_index,
                z_height_mm=float(layer_graph.z_height_mm),
                loop_count=len(loops_for_layer),
                path_length_mm=float(layer_length),
                loops=loops_for_layer,
            ),
            layer_warnings,
            int(layer_graph.island_count),
        )

    worker_count = max(1, min(int(max_workers), len(graphs) if graphs else 1))
    if worker_count > 1 and len(graphs) > 1:
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            results = list(executor.map(_build_layer, graphs))
    else:
        results = [_build_layer(layer_graph) for layer_graph in graphs]

    layer_plans: list[LayerPerimeterPlan] = []
    warnings: list[str] = []
    island_count_total = 0
    loop_count_total = 0
    path_length_mm_total = 0.0
    for layer_plan, layer_warnings, island_count in results:
        layer_plans.append(layer_plan)
        warnings.extend(layer_warnings)
        island_count_total += island_count
        loop_count_total += layer_plan.loop_count
        path_length_mm_total += layer_plan.path_length_mm

    layer_plans.sort(key=lambda plan: int(plan.layer_index))

    report = PerimeterClassicReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        layer_count=len(layer_plans),
        island_count_total=island_count_total,
        perimeter_count_requested=shells_requested,
        wall_sequence=sequence,
        loop_count_total=loop_count_total,
        path_length_mm_total=float(path_length_mm_total),
        warning_count=len(warnings),
        warnings=warnings,
    )
    return layer_plans, report
