from __future__ import annotations

from typing import Iterable, Tuple

Rect = Tuple[float, float, float, float]


def rect_from_points(p1: Iterable[float], p2: Iterable[float]) -> Rect:
    x1, y1 = p1
    x2, y2 = p2
    minx = float(min(x1, x2))
    maxx = float(max(x1, x2))
    miny = float(min(y1, y2))
    maxy = float(max(y1, y2))
    return (minx, miny, maxx, maxy)


def rect_size(rect: Rect) -> Tuple[float, float]:
    minx, miny, maxx, maxy = rect
    return (max(0.0, float(maxx - minx)), max(0.0, float(maxy - miny)))


def rect_intersects(a: Rect, b: Rect) -> bool:
    return not (a[2] < b[0] or a[0] > b[2] or a[3] < b[1] or a[1] > b[3])


def rect_contains(outer: Rect, inner: Rect) -> bool:
    return (
        outer[0] <= inner[0]
        and outer[1] <= inner[1]
        and outer[2] >= inner[2]
        and outer[3] >= inner[3]
    )
