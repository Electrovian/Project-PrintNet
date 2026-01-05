"""Path planning helpers."""

from dataclasses import dataclass
import math
import random
from typing import List, Optional, Sequence, Tuple

import numpy as np

from .geometry import (Island2D, LineSegment2D, Point2D, islands_difference,
                       line_inside_island, path_inside_island, point_in_island)
from . import infill

Point3D = Tuple[float, float, float]

@dataclass
class Toolpath:
    kind: str
    points: List[Point3D]
    speed: float
    extrusion_multiplier: float = 1.0

    @property
    def start(self) -> Point3D:
        return self.points[0] if self.points else (0.0, 0.0, 0.0)

    @property
    def end(self) -> Point3D:
        return self.points[-1] if self.points else (0.0, 0.0, 0.0)

@dataclass
class BridgeRegion:
    angle: float
    lines: List[LineSegment2D]

@dataclass
class ArcFit:
    center: Point2D
    radius: float
    clockwise: bool
    start: Point2D
    end: Point2D
    angle: float
    is_full_circle: bool

def _circle_from_points(p1: Point2D, p2: Point2D, p3: Point2D) -> Optional[Tuple[Point2D, float]]:
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    d = 2.0 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(d) < 1e-9:
        return None
    x1_sq = x1 * x1 + y1 * y1
    x2_sq = x2 * x2 + y2 * y2
    x3_sq = x3 * x3 + y3 * y3
    ux = (x1_sq * (y2 - y3) + x2_sq * (y3 - y1) + x3_sq * (y1 - y2)) / d
    uy = (x1_sq * (x3 - x2) + x2_sq * (x1 - x3) + x3_sq * (x2 - x1)) / d
    radius = math.hypot(x1 - ux, y1 - uy)
    if radius <= 0.0 or not math.isfinite(radius):
        return None
    return (float(ux), float(uy)), float(radius)

def fit_arc(points: Sequence[Point2D],
            tolerance: float = 0.05,
            require_closed: bool = True) -> Optional[ArcFit]:
    """Detect circular paths and return an arc fit if points are near a circle."""
    if not points or len(points) < 5:
        return None
    pts = list(points)
    was_closed = pts[0] == pts[-1]
    if was_closed:
        pts = pts[:-1]
    if len(pts) < 5:
        return None
    if require_closed and not was_closed:
        return None
    is_closed = was_closed

    start = pts[0]
    end = pts[-1]
    mid = pts[len(pts) // 2]
    circle = _circle_from_points(start, mid, end)
    if circle is None:
        return None
    center, radius = circle
    if radius <= 0.0:
        return None

    max_dev = 0.0
    for x, y in pts:
        dist = math.hypot(x - center[0], y - center[1])
        max_dev = max(max_dev, abs(dist - radius))
    if max_dev > max(tolerance, tolerance * radius):
        return None

    area = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        area += x1 * y2 - x2 * y1
    clockwise = area < 0.0

    if is_closed:
        angle = 2.0 * math.pi
        is_full_circle = True
        end = start
    else:
        a0 = math.atan2(start[1] - center[1], start[0] - center[0])
        a1 = math.atan2(end[1] - center[1], end[0] - center[0])
        if clockwise:
            angle = a0 - a1
            if angle <= 0.0:
                angle += 2.0 * math.pi
        else:
            angle = a1 - a0
            if angle <= 0.0:
                angle += 2.0 * math.pi
        is_full_circle = abs(angle - 2.0 * math.pi) < 1e-3

    return ArcFit(center=center,
                  radius=radius,
                  clockwise=clockwise,
                  start=start,
                  end=end,
                  angle=angle,
                  is_full_circle=is_full_circle)

def apply_seam_placement(loop: Sequence[Point2D],
                         mode: str,
                         anchor: Optional[Point2D] = None,
                         rear_angle: float = 180.0,
                         rng: Optional[random.Random] = None) -> List[Point2D]:
    """Return a closed loop reordered to match the requested seam placement."""
    points = list(loop)
    if len(points) < 3:
        return points
    if points[0] == points[-1]:
        points = points[:-1]

    mode_norm = mode.strip().lower()
    index = 0
    if mode_norm == "random":
        rng = rng or random.Random()
        if len(points) > 1:
            index = rng.randrange(1, len(points))
        else:
            index = 0
    elif mode_norm == "aligned" and anchor is not None:
        ax, ay = anchor
        best_dist = float("inf")
        for i, (x, y) in enumerate(points):
            dist = (x - ax) ** 2 + (y - ay) ** 2
            if dist < best_dist:
                best_dist = dist
                index = i
    elif mode_norm == "rear":
        cx = sum(p[0] for p in points) / len(points)
        cy = sum(p[1] for p in points) / len(points)
        target = math.radians(rear_angle)
        best_dist = float("inf")
        for i, (x, y) in enumerate(points):
            angle = math.atan2(y - cy, x - cx)
            delta = abs((angle - target + math.pi) % (2 * math.pi) - math.pi)
            if delta < best_dist:
                best_dist = delta
                index = i

    ordered = points[index:] + points[:index]
    ordered.append(ordered[0])
    return ordered

def comb_travel(start: Point2D,
                end: Point2D,
                island: Island2D) -> List[Point2D]:
    """Route travel inside an island when possible.

    Limitations: uses straight or L-shaped segments with simple sampling and
    does not account for narrow gaps or complex hole geometries.
    """
    if not point_in_island(start, island) or not point_in_island(end, island):
        return [start, end]

    direct = [start, end]
    if line_inside_island((start, end), island):
        return direct

    candidate_a = (end[0], start[1])
    candidate_b = (start[0], end[1])
    paths = []
    for mid in (candidate_a, candidate_b):
        path = [start, mid, end]
        if point_in_island(mid, island) and line_inside_island((start, mid), island) and \
                line_inside_island((mid, end), island):
            paths.append(path)
    if not paths:
        return direct
    paths.sort(key=lambda p: (p[0][0] - p[1][0]) ** 2 + (p[0][1] - p[1][1]) ** 2 +
               (p[1][0] - p[2][0]) ** 2 + (p[1][1] - p[2][1]) ** 2)
    return paths[0]

def plan_travel(start: Point3D,
                end: Point3D,
                retracted: bool,
                z_hop_height: float,
                comb_island: Optional[Island2D] = None,
                z_hop_only_outside: bool = False) -> List[Point3D]:
    """Return travel points with optional combing and Z-hop."""
    path_2d = [ (start[0], start[1]), (end[0], end[1]) ]
    if comb_island is not None:
        path_2d = comb_travel(path_2d[0], path_2d[-1], comb_island)

    hop = max(0.0, float(z_hop_height))
    use_hop = retracted and hop > 0.0
    if use_hop and z_hop_only_outside and comb_island is not None:
        if path_inside_island(path_2d, comb_island):
            use_hop = False

    points: List[Point3D] = []
    z = start[2]
    if use_hop:
        points.append((start[0], start[1], z))
        points.append((start[0], start[1], z + hop))
        for x, y in path_2d[1:-1]:
            points.append((x, y, z + hop))
        points.append((end[0], end[1], z + hop))
        points.append((end[0], end[1], z))
    else:
        points.append((start[0], start[1], z))
        for x, y in path_2d[1:-1]:
            points.append((x, y, z))
        points.append((end[0], end[1], z))
    return points

def order_islands_nearest(islands: Sequence[Island2D],
                          start: Point2D) -> List[Island2D]:
    """Order islands by nearest neighbor using centroids."""
    remaining = list(islands)
    ordered: List[Island2D] = []
    current = (float(start[0]), float(start[1]))
    while remaining:
        best_index = 0
        best_dist = float("inf")
        for index, island in enumerate(remaining):
            outer, _ = island
            points = outer[:-1] if len(outer) > 1 else outer
            if not points:
                continue
            cx = sum(p[0] for p in points) / len(points)
            cy = sum(p[1] for p in points) / len(points)
            dist = (cx - current[0]) ** 2 + (cy - current[1]) ** 2
            if dist < best_dist:
                best_dist = dist
                best_index = index
        chosen = remaining.pop(best_index)
        ordered.append(chosen)
        outer, _ = chosen
        points = outer[:-1] if len(outer) > 1 else outer
        if points:
            current = (points[0][0], points[0][1])
    return ordered

def order_toolpaths(toolpaths: Sequence[Toolpath],
                    start: Point3D = (0.0, 0.0, 0.0)) -> List[Toolpath]:
    """Order toolpaths by nearest neighbor, keeping perimeters before infill."""
    perimeters = [tp for tp in toolpaths if tp.kind == "perimeter"]
    others = [tp for tp in toolpaths if tp.kind != "perimeter"]

    def order_list(paths: List[Toolpath], current: Point3D) -> List[Toolpath]:
        ordered: List[Toolpath] = []
        remaining = list(paths)
        current_point = current
        while remaining:
            best_index = 0
            best_dist = float("inf")
            for index, path in enumerate(remaining):
                sx, sy, _ = path.start
                dist = (sx - current_point[0]) ** 2 + (sy - current_point[1]) ** 2
                if dist < best_dist:
                    best_dist = dist
                    best_index = index
            chosen = remaining.pop(best_index)
            ordered.append(chosen)
            current_point = chosen.end
        return ordered

    ordered_perimeters = order_list(perimeters, start)
    last_point = ordered_perimeters[-1].end if ordered_perimeters else start
    ordered_others = order_list(others, last_point)
    return ordered_perimeters + ordered_others

def plan_sequential_print(object_bounds: Sequence[Tuple[int, Tuple[Point3D, Point3D]]],
                          nozzle_clearance: float,
                          max_height: Optional[float] = None) -> Tuple[List[int], List[str]]:
    """Plan by-object printing order and warn if clearance is unsafe."""
    clearance = max(0.0, float(nozzle_clearance))
    warnings: List[str] = []
    if not object_bounds:
        return [], warnings

    def expand(bounds: Tuple[Point3D, Point3D], margin: float):
        (mn_x, mn_y, mn_z), (mx_x, mx_y, mx_z) = bounds
        return (
            (mn_x - margin, mn_y - margin, mn_z),
            (mx_x + margin, mx_y + margin, mx_z),
        )

    expanded = [(oid, expand(bounds, clearance)) for oid, bounds in object_bounds]
    for i in range(len(expanded)):
        oid_a, bounds_a = expanded[i]
        for j in range(i + 1, len(expanded)):
            oid_b, bounds_b = expanded[j]
            if _bounds_overlap_xy(bounds_a, bounds_b):
                warnings.append(
                    f"Objects {oid_a} and {oid_b} are too close for sequential printing."
                )

    if max_height is not None:
        max_h = float(max_height)
        for oid, bounds in object_bounds:
            _mn, mx = bounds
            if mx[2] > max_h:
                warnings.append(f"Object {oid} exceeds max height for sequential printing.")

    # Simple ordering: front-to-back, then left-to-right
    ordered = sorted(object_bounds,
                     key=lambda item: (item[1][0][1], item[1][0][0]))
    return [oid for oid, _bounds in ordered], warnings

def _bounds_overlap_xy(bounds_a: Tuple[Point3D, Point3D],
                       bounds_b: Tuple[Point3D, Point3D]) -> bool:
    (ax0, ay0, _az0), (ax1, ay1, _az1) = bounds_a
    (bx0, by0, _bz0), (bx1, by1, _bz1) = bounds_b
    overlap_x = ax0 <= bx1 and ax1 >= bx0
    overlap_y = ay0 <= by1 and ay1 >= by0
    return overlap_x and overlap_y

def detect_bridge_islands(current: List[Island2D],
                          below: List[Island2D]) -> List[Island2D]:
    """Return regions on the current layer lacking support below."""
    return islands_difference(current, below)

def bridge_direction(island: Island2D) -> float:
    """Compute a bridge direction aligned with the shortest span."""
    outer, _ = island
    points = outer[:-1] if len(outer) > 1 else outer
    if len(points) < 3:
        return 0.0
    pts = np.asarray(points, dtype=float)
    center = pts.mean(axis=0)
    centered = pts - center
    cov = np.cov(centered, rowvar=False)
    if cov.shape != (2, 2):
        return 0.0
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    minor_axis = eigenvectors[:, 0]
    angle = math.degrees(math.atan2(minor_axis[1], minor_axis[0]))
    angle = angle % 180.0
    return angle

def generate_bridge_infill(islands: List[Island2D],
                           layer_index: int,
                           extrusion_width: float) -> List[BridgeRegion]:
    regions: List[BridgeRegion] = []
    for island in islands:
        angle = bridge_direction(island)
        lines = infill.rectilinear_infill([island],
                                          density=1.0,
                                          angle_deg=angle,
                                          layer_index=layer_index,
                                          extrusion_width=extrusion_width,
                                          alternate=False)
        if lines:
            regions.append(BridgeRegion(angle=angle, lines=lines))
    return regions
