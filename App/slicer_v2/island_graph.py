from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Sequence

from .errors import SlicerV2IslandGraphError
from .geometry import EPSILON, Island, Point2, Polygon


MAX_NESTING_DEPTH = 128


@dataclass(frozen=True)
class LayerAdjacencyEdge:
    src_island_index: int
    dst_island_index: int


@dataclass(frozen=True)
class VerticalAdjacencyEdge:
    lower_layer_index: int
    lower_island_index: int
    upper_layer_index: int
    upper_island_index: int


@dataclass
class LayerIslandGraph:
    layer_index: int
    z_height_mm: float
    islands: tuple[Island, ...]
    contour_count_input: int
    filtered_count: int
    nesting_max_depth: int
    adjacency_edges: tuple[LayerAdjacencyEdge, ...] = ()
    warnings: list[str] = field(default_factory=list)

    @property
    def island_count(self) -> int:
        return len(self.islands)

    @property
    def hole_count(self) -> int:
        return sum(len(island.holes) for island in self.islands)

    @property
    def area_total(self) -> float:
        return sum(island.area for island in self.islands)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["island_count"] = self.island_count
        payload["hole_count"] = self.hole_count
        payload["area_total"] = self.area_total
        payload["adjacency_edge_count"] = len(self.adjacency_edges)
        return payload


@dataclass
class IslandGraphReport:
    generated_at_utc: str
    layer_count: int
    contour_count_input: int
    island_count_total: int
    hole_count_total: int
    intra_layer_edge_count: int
    vertical_edge_count: int
    nesting_max_depth: int
    warning_count: int
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _validate_contours(contours: Sequence[Polygon], layer_index: int) -> None:
    for index, contour in enumerate(contours):
        if not isinstance(contour, Polygon):
            raise SlicerV2IslandGraphError(f"ISLAND_GRAPH_CONTOUR_NOT_POLYGON:layer={layer_index}:index={index}")


def _point_for_contains(polygon: Polygon) -> Point2:
    return polygon.centroid


def _compute_parent_index(
    *,
    polygons: Sequence[Polygon],
    child_index: int,
) -> int | None:
    child = polygons[child_index]
    child_point = _point_for_contains(child)
    child_area = child.area
    parent_index: int | None = None
    parent_area: float | None = None
    for cand_index in range(len(polygons)):
        if cand_index == child_index:
            continue
        candidate = polygons[cand_index]
        if candidate.area <= child_area + EPSILON:
            continue
        if not candidate.bounds.intersects(child.bounds):
            continue
        if not candidate.contains_point(child_point, include_boundary=True):
            continue
        if parent_area is None or candidate.area < parent_area:
            parent_area = candidate.area
            parent_index = cand_index
    return parent_index


def _compute_depths(parent_indices: Sequence[int | None], max_depth: int) -> list[int]:
    depths = [-1] * len(parent_indices)
    for index in range(len(parent_indices)):
        current = index
        depth = 0
        safety = max_depth + 2
        while True:
            if safety <= 0:
                raise SlicerV2IslandGraphError("ISLAND_GRAPH_PARENT_CYCLE_DETECTED")
            safety -= 1
            parent = parent_indices[current]
            if parent is None:
                break
            depth += 1
            current = parent
            if depth > max_depth:
                raise SlicerV2IslandGraphError("ISLAND_GRAPH_MAX_DEPTH_EXCEEDED")
        depths[index] = depth
    return depths


def _build_islands(
    *,
    polygons: Sequence[Polygon],
    parent_indices: Sequence[int | None],
    depths: Sequence[int],
) -> tuple[Island, ...]:
    children_map: dict[int, list[int]] = {}
    for child_index, parent_index in enumerate(parent_indices):
        if parent_index is None:
            continue
        if parent_index not in children_map:
            children_map[parent_index] = []
        children_map[parent_index].append(child_index)

    islands: list[Island] = []
    for index in range(len(polygons)):
        if depths[index] % 2 != 0:
            continue
        hole_indices = children_map.get(index, [])
        holes: list[Polygon] = []
        for child_index in hole_indices:
            if depths[child_index] == depths[index] + 1:
                holes.append(polygons[child_index])
        islands.append(Island(outer=polygons[index], holes=tuple(holes)))
    return tuple(islands)


def _build_layer_adjacency_edges(islands: Sequence[Island]) -> tuple[LayerAdjacencyEdge, ...]:
    edges: list[LayerAdjacencyEdge] = []
    island_count = len(islands)
    for src_index in range(island_count):
        src_bounds = islands[src_index].bounds
        for dst_index in range(src_index + 1, island_count):
            dst_bounds = islands[dst_index].bounds
            if not src_bounds.intersects(dst_bounds):
                continue
            edges.append(LayerAdjacencyEdge(src_island_index=src_index, dst_island_index=dst_index))
    return tuple(edges)


def build_layer_island_graph(
    contours: Sequence[Polygon],
    *,
    layer_index: int,
    z_height_mm: float,
    min_area: float = 1e-6,
    max_nesting_depth: int = MAX_NESTING_DEPTH,
) -> LayerIslandGraph:
    if max_nesting_depth < 1:
        raise SlicerV2IslandGraphError("ISLAND_GRAPH_MAX_DEPTH_INVALID")
    if min_area < 0.0:
        raise SlicerV2IslandGraphError("ISLAND_GRAPH_MIN_AREA_INVALID")

    contour_list = list(contours)
    _validate_contours(contour_list, layer_index)

    filtered: list[Polygon] = []
    filtered_count = 0
    for contour in contour_list:
        if contour.area + EPSILON < min_area:
            filtered_count += 1
            continue
        filtered.append(contour.with_winding(clockwise=False))

    if not filtered:
        return LayerIslandGraph(
            layer_index=layer_index,
            z_height_mm=float(z_height_mm),
            islands=(),
            contour_count_input=len(contour_list),
            filtered_count=filtered_count,
            nesting_max_depth=0,
            adjacency_edges=(),
            warnings=[],
        )

    sorted_polygons = sorted(filtered, key=lambda poly: poly.area, reverse=True)
    parent_indices: list[int | None] = []
    for index in range(len(sorted_polygons)):
        parent_indices.append(_compute_parent_index(polygons=sorted_polygons, child_index=index))
    depths = _compute_depths(parent_indices, max_nesting_depth)
    islands = _build_islands(polygons=sorted_polygons, parent_indices=parent_indices, depths=depths)
    adjacency_edges = _build_layer_adjacency_edges(islands)

    warnings: list[str] = []
    if len(islands) == 0 and len(sorted_polygons) > 0:
        warnings.append(f"layer_{layer_index}:polygons_without_islands:{len(sorted_polygons)}")

    return LayerIslandGraph(
        layer_index=layer_index,
        z_height_mm=float(z_height_mm),
        islands=islands,
        contour_count_input=len(contour_list),
        filtered_count=filtered_count,
        nesting_max_depth=max(depths) if depths else 0,
        adjacency_edges=adjacency_edges,
        warnings=warnings,
    )


def _island_overlaps_vertically(lower: Island, upper: Island) -> bool:
    if not lower.bounds.intersects(upper.bounds):
        return False
    lower_center = lower.outer.centroid
    upper_center = upper.outer.centroid
    if lower.contains_point(upper_center, include_boundary=True):
        return True
    if upper.contains_point(lower_center, include_boundary=True):
        return True
    return False


def build_vertical_adjacency(
    layer_graphs: Sequence[LayerIslandGraph],
    *,
    max_layer_gap: int = 1,
) -> tuple[VerticalAdjacencyEdge, ...]:
    if max_layer_gap < 1:
        raise SlicerV2IslandGraphError("ISLAND_GRAPH_LAYER_GAP_INVALID")

    edges: list[VerticalAdjacencyEdge] = []
    graphs = list(layer_graphs)
    for lower_index in range(len(graphs)):
        lower_graph = graphs[lower_index]
        max_upper = min(len(graphs), lower_index + max_layer_gap + 1)
        for upper_index in range(lower_index + 1, max_upper):
            upper_graph = graphs[upper_index]
            for lower_island_index, lower_island in enumerate(lower_graph.islands):
                for upper_island_index, upper_island in enumerate(upper_graph.islands):
                    if not _island_overlaps_vertically(lower_island, upper_island):
                        continue
                    edges.append(
                        VerticalAdjacencyEdge(
                            lower_layer_index=lower_graph.layer_index,
                            lower_island_index=lower_island_index,
                            upper_layer_index=upper_graph.layer_index,
                            upper_island_index=upper_island_index,
                        )
                    )
    return tuple(edges)


def build_island_graph_report(
    layer_graphs: Sequence[LayerIslandGraph],
    vertical_edges: Sequence[VerticalAdjacencyEdge],
) -> IslandGraphReport:
    graphs = list(layer_graphs)
    warnings: list[str] = []
    contour_count_input = 0
    island_count_total = 0
    hole_count_total = 0
    intra_layer_edge_count = 0
    nesting_max_depth = 0
    for graph in graphs:
        contour_count_input += graph.contour_count_input
        island_count_total += graph.island_count
        hole_count_total += graph.hole_count
        intra_layer_edge_count += len(graph.adjacency_edges)
        nesting_max_depth = max(nesting_max_depth, graph.nesting_max_depth)
        warnings.extend(graph.warnings)

    return IslandGraphReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        layer_count=len(graphs),
        contour_count_input=contour_count_input,
        island_count_total=island_count_total,
        hole_count_total=hole_count_total,
        intra_layer_edge_count=intra_layer_edge_count,
        vertical_edge_count=len(vertical_edges),
        nesting_max_depth=nesting_max_depth,
        warning_count=len(warnings),
        warnings=warnings,
    )

