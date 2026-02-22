from __future__ import annotations

from dataclasses import dataclass
from math import hypot, isfinite
from typing import Iterable

from .errors import SlicerV2GeometryError


EPSILON = 1e-9


def _require_finite(value: float, label: str) -> float:
    if not isfinite(value):
        raise SlicerV2GeometryError(f"NON_FINITE_VALUE:{label}:{value}")
    return float(value)


def _points_close(a: "Point2", b: "Point2", tol: float = EPSILON) -> bool:
    dx = abs(a.x - b.x)
    dy = abs(a.y - b.y)
    return dx <= tol and dy <= tol


@dataclass(frozen=True)
class Point2:
    x: float
    y: float

    def __post_init__(self) -> None:
        object.__setattr__(self, "x", _require_finite(float(self.x), "point_x"))
        object.__setattr__(self, "y", _require_finite(float(self.y), "point_y"))

    @staticmethod
    def from_tuple(values: tuple[float, float]) -> "Point2":
        if len(values) != 2:
            raise SlicerV2GeometryError("POINT2_TUPLE_SIZE_INVALID")
        return Point2(values[0], values[1])

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def distance_to(self, other: "Point2") -> float:
        return hypot(other.x - self.x, other.y - self.y)

    def translated(self, dx: float, dy: float) -> "Point2":
        return Point2(self.x + float(dx), self.y + float(dy))


@dataclass(frozen=True)
class AABB:
    min_x: float
    min_y: float
    max_x: float
    max_y: float

    def __post_init__(self) -> None:
        min_x = _require_finite(float(self.min_x), "aabb_min_x")
        min_y = _require_finite(float(self.min_y), "aabb_min_y")
        max_x = _require_finite(float(self.max_x), "aabb_max_x")
        max_y = _require_finite(float(self.max_y), "aabb_max_y")
        if max_x < min_x or max_y < min_y:
            raise SlicerV2GeometryError("AABB_BOUNDS_INVALID")
        object.__setattr__(self, "min_x", min_x)
        object.__setattr__(self, "min_y", min_y)
        object.__setattr__(self, "max_x", max_x)
        object.__setattr__(self, "max_y", max_y)

    @staticmethod
    def from_points(points: Iterable[Point2]) -> "AABB":
        points_list = list(points)
        if not points_list:
            raise SlicerV2GeometryError("AABB_POINTS_EMPTY")
        min_x = min(point.x for point in points_list)
        min_y = min(point.y for point in points_list)
        max_x = max(point.x for point in points_list)
        max_y = max(point.y for point in points_list)
        return AABB(min_x, min_y, max_x, max_y)

    @property
    def width(self) -> float:
        return self.max_x - self.min_x

    @property
    def height(self) -> float:
        return self.max_y - self.min_y

    @property
    def area(self) -> float:
        return self.width * self.height

    def contains(self, point: Point2) -> bool:
        within_x = self.min_x - EPSILON <= point.x <= self.max_x + EPSILON
        within_y = self.min_y - EPSILON <= point.y <= self.max_y + EPSILON
        return bool(within_x and within_y)

    def intersects(self, other: "AABB") -> bool:
        if self.max_x < other.min_x - EPSILON:
            return False
        if other.max_x < self.min_x - EPSILON:
            return False
        if self.max_y < other.min_y - EPSILON:
            return False
        if other.max_y < self.min_y - EPSILON:
            return False
        return True

    def padded(self, padding: float) -> "AABB":
        pad = max(0.0, float(padding))
        return AABB(self.min_x - pad, self.min_y - pad, self.max_x + pad, self.max_y + pad)

    def union(self, other: "AABB") -> "AABB":
        return AABB(
            min(self.min_x, other.min_x),
            min(self.min_y, other.min_y),
            max(self.max_x, other.max_x),
            max(self.max_y, other.max_y),
        )


def _normalize_points(points: Iterable[Point2]) -> tuple[Point2, ...]:
    points_list = list(points)
    if len(points_list) < 3:
        raise SlicerV2GeometryError("POLYGON_POINT_COUNT_INVALID")

    deduped: list[Point2] = []
    for point in points_list:
        if not deduped or not _points_close(point, deduped[-1]):
            deduped.append(point)

    if len(deduped) > 1 and _points_close(deduped[0], deduped[-1]):
        deduped = deduped[:-1]

    if len(deduped) < 3:
        raise SlicerV2GeometryError("POLYGON_DEGENERATE")

    return tuple(deduped)


def _signed_area(points: tuple[Point2, ...]) -> float:
    count = len(points)
    total = 0.0
    for index in range(count):
        a = points[index]
        b = points[(index + 1) % count]
        total += a.x * b.y - b.x * a.y
    return 0.5 * total


def _point_on_segment(point: Point2, start: Point2, end: Point2) -> bool:
    cross = (point.y - start.y) * (end.x - start.x) - (point.x - start.x) * (end.y - start.y)
    if abs(cross) > EPSILON:
        return False
    dot = (point.x - start.x) * (end.x - start.x) + (point.y - start.y) * (end.y - start.y)
    if dot < -EPSILON:
        return False
    length_sq = (end.x - start.x) ** 2 + (end.y - start.y) ** 2
    if dot - length_sq > EPSILON:
        return False
    return True


@dataclass(frozen=True)
class Polygon:
    points: tuple[Point2, ...]

    def __post_init__(self) -> None:
        normalized = _normalize_points(self.points)
        object.__setattr__(self, "points", normalized)
        if abs(_signed_area(normalized)) <= EPSILON:
            raise SlicerV2GeometryError("POLYGON_AREA_ZERO")

    @staticmethod
    def from_tuples(points: Iterable[tuple[float, float]]) -> "Polygon":
        return Polygon(tuple(Point2.from_tuple(item) for item in points))

    def as_tuples(self, *, closed: bool = False) -> list[tuple[float, float]]:
        result = [point.as_tuple() for point in self.points]
        if closed and result:
            result.append(result[0])
        return result

    @property
    def signed_area(self) -> float:
        return _signed_area(self.points)

    @property
    def area(self) -> float:
        return abs(self.signed_area)

    @property
    def is_clockwise(self) -> bool:
        return self.signed_area < 0.0

    @property
    def perimeter(self) -> float:
        total = 0.0
        count = len(self.points)
        for index in range(count):
            total += self.points[index].distance_to(self.points[(index + 1) % count])
        return total

    @property
    def bounds(self) -> AABB:
        return AABB.from_points(self.points)

    @property
    def centroid(self) -> Point2:
        area2 = 0.0
        cx = 0.0
        cy = 0.0
        count = len(self.points)
        for index in range(count):
            a = self.points[index]
            b = self.points[(index + 1) % count]
            cross = a.x * b.y - b.x * a.y
            area2 += cross
            cx += (a.x + b.x) * cross
            cy += (a.y + b.y) * cross

        if abs(area2) <= EPSILON:
            avg_x = sum(point.x for point in self.points) / count
            avg_y = sum(point.y for point in self.points) / count
            return Point2(avg_x, avg_y)

        scale = 1.0 / (3.0 * area2)
        return Point2(cx * scale, cy * scale)

    def with_winding(self, *, clockwise: bool) -> "Polygon":
        if self.is_clockwise == clockwise:
            return self
        return Polygon(tuple(reversed(self.points)))

    def contains_point(self, point: Point2, *, include_boundary: bool = True) -> bool:
        count = len(self.points)
        for index in range(count):
            a = self.points[index]
            b = self.points[(index + 1) % count]
            if _point_on_segment(point, a, b):
                return include_boundary

        inside = False
        for index in range(count):
            a = self.points[index]
            b = self.points[(index + 1) % count]
            intersects = ((a.y > point.y) != (b.y > point.y))
            if not intersects:
                continue
            denom = b.y - a.y
            if abs(denom) <= EPSILON:
                continue
            x_intersect = a.x + (point.y - a.y) * (b.x - a.x) / denom
            if point.x < x_intersect:
                inside = not inside
        return inside


@dataclass(frozen=True)
class Island:
    outer: Polygon
    holes: tuple[Polygon, ...] = ()

    def __post_init__(self) -> None:
        normalized_outer = self.outer.with_winding(clockwise=False)
        normalized_holes = tuple(hole.with_winding(clockwise=True) for hole in self.holes)
        object.__setattr__(self, "outer", normalized_outer)
        object.__setattr__(self, "holes", normalized_holes)

    @property
    def area(self) -> float:
        return self.outer.area - sum(hole.area for hole in self.holes)

    @property
    def bounds(self) -> AABB:
        return self.outer.bounds

    def contains_point(self, point: Point2, *, include_boundary: bool = True) -> bool:
        if not self.outer.contains_point(point, include_boundary=include_boundary):
            return False
        for hole in self.holes:
            if hole.contains_point(point, include_boundary=include_boundary):
                return False
        return True


def polygon_from_tuples(points: Iterable[tuple[float, float]]) -> Polygon:
    return Polygon.from_tuples(points)


def island_from_tuples(
    outer_points: Iterable[tuple[float, float]],
    holes_points: Iterable[Iterable[tuple[float, float]]] | None = None,
) -> Island:
    holes_raw = list(holes_points or [])
    holes = tuple(Polygon.from_tuples(points) for points in holes_raw)
    return Island(outer=Polygon.from_tuples(outer_points), holes=holes)


def polyline_length(points: Iterable[Point2]) -> float:
    points_list = list(points)
    if len(points_list) < 2:
        return 0.0
    total = 0.0
    for index in range(len(points_list) - 1):
        total += points_list[index].distance_to(points_list[index + 1])
    return total


def bounds_for_polygons(polygons: Iterable[Polygon]) -> AABB:
    polygons_list = list(polygons)
    if not polygons_list:
        raise SlicerV2GeometryError("BOUNDS_POLYGONS_EMPTY")
    combined = polygons_list[0].bounds
    for polygon in polygons_list[1:]:
        combined = combined.union(polygon.bounds)
    return combined
