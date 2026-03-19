from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from math import sqrt
from typing import Iterable

from .errors import SlicerV2PolygonPipelineError
from .geometry import EPSILON, Point2, Polygon


def _cross(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx


def _line_intersection(
    a1: Point2,
    a2: Point2,
    b1: Point2,
    b2: Point2,
) -> Point2 | None:
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
    return Point2(a1.x + t * r_x, a1.y + t * r_y)


def _edge_outward_normal(start: Point2, end: Point2) -> tuple[float, float]:
    dx = end.x - start.x
    dy = end.y - start.y
    length = sqrt(dx * dx + dy * dy)
    if length <= EPSILON:
        raise SlicerV2PolygonPipelineError("EDGE_LENGTH_ZERO")
    return (dy / length, -dx / length)


def _remove_collinear_points(points: list[Point2]) -> list[Point2]:
    if len(points) < 3:
        return points
    cleaned: list[Point2] = []
    count = len(points)
    for idx in range(count):
        prev = points[(idx - 1) % count]
        curr = points[idx]
        nxt = points[(idx + 1) % count]
        v1x = curr.x - prev.x
        v1y = curr.y - prev.y
        v2x = nxt.x - curr.x
        v2y = nxt.y - curr.y
        cross = _cross(v1x, v1y, v2x, v2y)
        if abs(cross) <= EPSILON:
            continue
        cleaned.append(curr)
    return cleaned


@dataclass
class PolygonOffsetCleanupReport:
    generated_at_utc: str
    input_count: int
    cleaned_count: int
    output_count: int
    dropped_count: int
    offset_distance: float
    warning_count: int
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def cleanup_polygon(
    polygon: Polygon,
    *,
    remove_collinear: bool = True,
    min_area: float = 1e-6,
) -> Polygon | None:
    if min_area < 0:
        raise SlicerV2PolygonPipelineError("MIN_AREA_NEGATIVE")
    points = list(polygon.points)
    if remove_collinear:
        points = _remove_collinear_points(points)
    if len(points) < 3:
        return None
    try:
        cleaned = Polygon(tuple(points))
    except Exception:
        return None
    if cleaned.area < max(min_area, EPSILON):
        return None
    return cleaned


def cleanup_polygons(
    polygons: Iterable[Polygon],
    *,
    remove_collinear: bool = True,
    min_area: float = 1e-6,
) -> list[Polygon]:
    result: list[Polygon] = []
    for polygon in polygons:
        cleaned = cleanup_polygon(
            polygon,
            remove_collinear=remove_collinear,
            min_area=min_area,
        )
        if cleaned is not None:
            result.append(cleaned)
    return result


def offset_polygon(
    polygon: Polygon,
    distance: float,
    *,
    min_area: float = 1e-6,
) -> Polygon | None:
    if abs(distance) <= EPSILON:
        return cleanup_polygon(polygon, min_area=min_area)

    base = polygon.with_winding(clockwise=False)
    points = list(base.points)
    count = len(points)
    if count < 3:
        return None

    normals: list[tuple[float, float]] = []
    for idx in range(count):
        start = points[idx]
        end = points[(idx + 1) % count]
        normals.append(_edge_outward_normal(start, end))

    shifted_a: list[Point2] = []
    shifted_b: list[Point2] = []
    for idx in range(count):
        start = points[idx]
        end = points[(idx + 1) % count]
        n_x, n_y = normals[idx]
        shifted_a.append(Point2(start.x + n_x * distance, start.y + n_y * distance))
        shifted_b.append(Point2(end.x + n_x * distance, end.y + n_y * distance))

    output_points: list[Point2] = []
    for idx in range(count):
        prev_idx = (idx - 1) % count
        curr_idx = idx
        intersection = _line_intersection(
            shifted_a[prev_idx],
            shifted_b[prev_idx],
            shifted_a[curr_idx],
            shifted_b[curr_idx],
        )
        if intersection is None:
            p = points[idx]
            n1_x, n1_y = normals[prev_idx]
            n2_x, n2_y = normals[curr_idx]
            avg_x = n1_x + n2_x
            avg_y = n1_y + n2_y
            length = sqrt(avg_x * avg_x + avg_y * avg_y)
            if length <= EPSILON:
                intersection = Point2(p.x + normals[curr_idx][0] * distance, p.y + normals[curr_idx][1] * distance)
            else:
                intersection = Point2(p.x + (avg_x / length) * distance, p.y + (avg_y / length) * distance)
        output_points.append(intersection)

    try:
        offset = Polygon(tuple(output_points))
    except Exception:
        return None

    cleaned = cleanup_polygon(offset, min_area=min_area)
    if cleaned is None:
        return None
    if distance < 0.0 and cleaned.area >= base.area - EPSILON:
        return None
    if distance > 0.0 and cleaned.area <= base.area + EPSILON:
        return None
    return cleaned


def offset_polygons(
    polygons: Iterable[Polygon],
    distance: float,
    *,
    min_area: float = 1e-6,
) -> list[Polygon]:
    result: list[Polygon] = []
    for polygon in polygons:
        offset = offset_polygon(polygon, distance, min_area=min_area)
        if offset is not None:
            result.append(offset)
    return result


def cleanup_and_offset_polygons(
    polygons: Iterable[Polygon],
    *,
    offset_distance: float,
    min_area: float = 1e-6,
    strict: bool = False,
) -> tuple[list[Polygon], PolygonOffsetCleanupReport]:
    input_polygons = list(polygons)
    warnings: list[str] = []
    cleaned = cleanup_polygons(input_polygons, min_area=min_area)
    dropped_cleanup = len(input_polygons) - len(cleaned)
    if dropped_cleanup > 0:
        warnings.append(f"dropped_in_cleanup:{dropped_cleanup}")

    offset = offset_polygons(cleaned, offset_distance, min_area=min_area)
    dropped_offset = len(cleaned) - len(offset)
    if dropped_offset > 0:
        warnings.append(f"dropped_in_offset:{dropped_offset}")

    report = PolygonOffsetCleanupReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        input_count=len(input_polygons),
        cleaned_count=len(cleaned),
        output_count=len(offset),
        dropped_count=len(input_polygons) - len(offset),
        offset_distance=float(offset_distance),
        warning_count=len(warnings),
        warnings=warnings,
    )

    if strict and report.warning_count > 0:
        raise SlicerV2PolygonPipelineError(
            f"STRICT_POLYGON_PIPELINE_WARNING_FAILURE: {report.warning_count} warning(s)"
        )

    return offset, report
