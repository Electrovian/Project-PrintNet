from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .errors import SlicerV2GeometryError
from .geometry import EPSILON, Island, Point2, Polygon


@dataclass(frozen=True)
class SplitLineJunction:
    p: Point2
    clipped: bool
    src_idx: int

    def is_src(self) -> bool:
        return self.src_idx >= 0

    def get_src_index(self) -> int:
        if self.src_idx >= 0:
            return self.src_idx
        return -self.src_idx - 1


SplittedLine = list[SplitLineJunction]


def _cross(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx


def _segment_intersection(a1: Point2, a2: Point2, b1: Point2, b2: Point2) -> tuple[float, Point2] | None:
    r_x = a2.x - a1.x
    r_y = a2.y - a1.y
    s_x = b2.x - b1.x
    s_y = b2.y - b1.y
    denom = _cross(r_x, r_y, s_x, s_y)
    if abs(denom) <= EPSILON:
        return None
    qp_x = b1.x - a1.x
    qp_y = b1.y - a1.y
    t = _cross(qp_x, qp_y, s_x, s_y) / denom
    u = _cross(qp_x, qp_y, r_x, r_y) / denom
    if t < -EPSILON or t > 1.0 + EPSILON:
        return None
    if u < -EPSILON or u > 1.0 + EPSILON:
        return None
    x = a1.x + (t * r_x)
    y = a1.y + (t * r_y)
    return (max(0.0, min(1.0, t)), Point2(x, y))


def _iter_clip_edges(polygons: Sequence[Polygon]) -> list[tuple[Point2, Point2]]:
    edges: list[tuple[Point2, Point2]] = []
    for polygon in polygons:
        points = list(polygon.points)
        for index in range(len(points)):
            edges.append((points[index], points[(index + 1) % len(points)]))
    return edges


def _to_clip_polygons(clip: Sequence[Polygon | Island]) -> list[Polygon]:
    polygons: list[Polygon] = []
    for item in clip:
        if isinstance(item, Polygon):
            polygons.append(item)
        elif isinstance(item, Island):
            polygons.append(item.outer)
            polygons.extend(item.holes)
        else:
            raise SlicerV2GeometryError("LINE_SPLIT_CLIP_TYPE_INVALID")
    return polygons


def _inside_clip(point: Point2, clip: Sequence[Polygon | Island]) -> bool:
    for item in clip:
        if isinstance(item, Polygon):
            if item.contains_point(point, include_boundary=True):
                return True
        elif isinstance(item, Island):
            if item.contains_point(point, include_boundary=True):
                return True
    return False


def _dedupe_events(events: list[tuple[float, Point2, int]]) -> list[tuple[float, Point2, int]]:
    if not events:
        return []
    out: list[tuple[float, Point2, int]] = []
    events.sort(key=lambda item: item[0])
    for event in events:
        if not out:
            out.append(event)
            continue
        prev = out[-1]
        if abs(prev[0] - event[0]) <= EPSILON and prev[1].distance_to(event[1]) <= EPSILON:
            continue
        out.append(event)
    return out


def split_line(
    path: Iterable[Point2 | tuple[float, float]],
    clip: Sequence[Polygon | Island],
    closed: bool = False,
) -> SplittedLine:
    points_raw = list(path)
    if len(points_raw) < 2:
        return []

    points: list[Point2] = []
    for item in points_raw:
        if isinstance(item, Point2):
            points.append(item)
        else:
            points.append(Point2(float(item[0]), float(item[1])))

    if closed and points[0].distance_to(points[-1]) > EPSILON:
        points.append(points[0])

    clip_polygons = _to_clip_polygons(clip)
    clip_edges = _iter_clip_edges(clip_polygons)

    junctions: SplittedLine = []
    segment_count = len(points) - 1
    for seg_index in range(segment_count):
        start = points[seg_index]
        end = points[seg_index + 1]
        events: list[tuple[float, Point2, int]] = [(0.0, start, seg_index), (1.0, end, seg_index + 1)]
        for edge_start, edge_end in clip_edges:
            hit = _segment_intersection(start, end, edge_start, edge_end)
            if hit is None:
                continue
            t_value, hit_point = hit
            events.append((t_value, hit_point, -(seg_index + 1)))

        events = _dedupe_events(events)
        for piece_index in range(len(events) - 1):
            current_t, current_point, src_idx = events[piece_index]
            next_t, next_point, _next_src = events[piece_index + 1]
            if next_t - current_t <= EPSILON:
                continue
            mid = Point2((current_point.x + next_point.x) * 0.5, (current_point.y + next_point.y) * 0.5)
            clipped = _inside_clip(mid, clip)
            if junctions and junctions[-1].p.distance_to(current_point) <= EPSILON:
                junctions[-1] = SplitLineJunction(p=junctions[-1].p, clipped=clipped, src_idx=junctions[-1].src_idx)
            else:
                junctions.append(SplitLineJunction(p=current_point, clipped=clipped, src_idx=src_idx))

    if junctions:
        junctions.append(SplitLineJunction(p=points[-1], clipped=False, src_idx=segment_count))
    return junctions
