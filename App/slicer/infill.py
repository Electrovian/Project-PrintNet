"""Infill pattern generation."""

import math
from typing import List, Sequence, Tuple

from .geometry import Island2D, LineSegment2D, Point2D, clip_lines_to_island

def _rotate_point(point: Point2D, angle_rad: float) -> Point2D:
    x, y = point
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)

def _rotate_points(points: Sequence[Point2D], angle_rad: float) -> List[Point2D]:
    return [_rotate_point(p, angle_rad) for p in points]

def _rotate_lines(lines: Sequence[LineSegment2D], angle_rad: float) -> List[LineSegment2D]:
    return [(_rotate_point(a, angle_rad), _rotate_point(b, angle_rad)) for a, b in lines]

def _bounds(points: Sequence[Point2D]) -> Tuple[float, float, float, float]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), max(xs), min(ys), max(ys)

def _line_spacing(density: float, extrusion_width: float, directions: int) -> float:
    clamped = max(0.0, min(1.0, float(density)))
    if clamped <= 0.0:
        return 0.0
    return extrusion_width * directions / clamped

def _generate_parallel_lines(polygon: Sequence[Point2D],
                             spacing: float,
                             angle_deg: float) -> List[LineSegment2D]:
    if spacing <= 0.0 or len(polygon) < 3:
        return []

    angle_rad = math.radians(angle_deg)
    rotated = _rotate_points(polygon, -angle_rad)
    minx, maxx, miny, maxy = _bounds(rotated)

    span = max(maxx - minx, maxy - miny)
    margin = span + spacing
    x0 = minx - margin
    x1 = maxx + margin

    lines: List[LineSegment2D] = []
    y = miny - spacing
    ymax = maxy + spacing
    while y <= ymax:
        lines.append(((x0, y), (x1, y)))
        y += spacing

    return _rotate_lines(lines, angle_rad)

def rectilinear_infill(islands: Sequence[Island2D],
                       density: float,
                       angle_deg: float,
                       layer_index: int,
                       extrusion_width: float,
                       alternate: bool = True) -> List[LineSegment2D]:
    spacing = _line_spacing(density, extrusion_width, directions=1)
    if spacing <= 0.0:
        return []
    angle = angle_deg + (layer_index % 2) * 90.0 if alternate else angle_deg

    segments: List[LineSegment2D] = []
    for outer, holes in islands:
        lines = _generate_parallel_lines(outer, spacing, angle)
        segments.extend(clip_lines_to_island(lines, outer, holes))
    return segments

def grid_infill(islands: Sequence[Island2D],
                density: float,
                angle_deg: float,
                layer_index: int,
                extrusion_width: float,
                alternate: bool = True) -> List[LineSegment2D]:
    spacing = _line_spacing(density, extrusion_width, directions=2)
    if spacing <= 0.0:
        return []
    base_angle = angle_deg + (layer_index % 2) * 90.0 if alternate else angle_deg

    segments: List[LineSegment2D] = []
    for angle in (base_angle, base_angle + 90.0):
        for outer, holes in islands:
            lines = _generate_parallel_lines(outer, spacing, angle)
            segments.extend(clip_lines_to_island(lines, outer, holes))
    return segments

def triangle_infill(islands: Sequence[Island2D],
                    density: float,
                    angle_deg: float,
                    layer_index: int,
                    extrusion_width: float,
                    alternate: bool = True) -> List[LineSegment2D]:
    spacing = _line_spacing(density, extrusion_width, directions=3)
    if spacing <= 0.0:
        return []
    base_angle = angle_deg + (layer_index % 2) * 90.0 if alternate else angle_deg
    angles = (base_angle, base_angle + 60.0, base_angle + 120.0)

    segments: List[LineSegment2D] = []
    for angle in angles:
        for outer, holes in islands:
            lines = _generate_parallel_lines(outer, spacing, angle)
            segments.extend(clip_lines_to_island(lines, outer, holes))
    return segments

def generate_infill(islands: Sequence[Island2D],
                    density: float,
                    angle_deg: float,
                    layer_index: int,
                    extrusion_width: float,
                    pattern: str = "rectilinear",
                    alternate: bool = True) -> List[LineSegment2D]:
    name = pattern.strip().lower()
    if name in ("grid", "rect_grid"):
        return grid_infill(islands, density, angle_deg, layer_index, extrusion_width, alternate)
    if name in ("triangle", "triangles"):
        return triangle_infill(islands, density, angle_deg, layer_index, extrusion_width, alternate)
    return rectilinear_infill(islands, density, angle_deg, layer_index, extrusion_width, alternate)
