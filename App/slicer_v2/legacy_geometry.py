"""Geometric helper utilities.

For now this is intentionally tiny. As you extend the slicer, this is
where you can put plane/triangle intersections, polygon offset
operations, etc.
"""

import math
from typing import (Any, Dict, Iterable, List, Protocol, Sequence, Tuple, TYPE_CHECKING,
                    cast)

import numpy as np
try:
    import pyclipper  # type: ignore[import-not-found]
except Exception:  # pragma: no cover - optional dependency in type checkers
    pyclipper = None  # type: ignore[assignment]
import trimesh
from trimesh.transformations import transform_points

if TYPE_CHECKING:
    class _MeshLike(Protocol):
        mesh: trimesh.Trimesh
else:  # pragma: no cover - used for type checking only
    class _MeshLike:
        pass

Point2D = Tuple[float, float]
Polygon2D = List[Point2D]
LineSegment2D = Tuple[Point2D, Point2D]
Island2D = Tuple[Polygon2D, List[Polygon2D]]

_CLIPPER_SCALE = 1_000_000
_CLIPPER_EPS = 1.0 / _CLIPPER_SCALE
_MIN_LOOP_AREA = _CLIPPER_EPS * _CLIPPER_EPS

def _points_close(a: Point2D, b: Point2D, tol: float = _CLIPPER_EPS) -> bool:
    return abs(a[0] - b[0]) <= tol and abs(a[1] - b[1]) <= tol

def _dedupe_points(points: Sequence[Point2D]) -> Polygon2D:
    cleaned: Polygon2D = []
    for x, y in points:
        point = (float(x), float(y))
        if not cleaned or not _points_close(point, cleaned[-1]):
            cleaned.append(point)
    if len(cleaned) > 1 and _points_close(cleaned[0], cleaned[-1]):
        cleaned = cleaned[:-1]
    return cleaned

def _normalize_polygon(polygon: Sequence[Point2D]) -> Polygon2D:
    points = [(float(x), float(y)) for x, y in polygon]
    if len(points) > 1 and _points_close(points[0], points[-1]):
        points = points[:-1]
    return points

def _close_polygon(points: Sequence[Point2D]) -> Polygon2D:
    if not points:
        return []
    closed = list(points)
    if not _points_close(closed[0], closed[-1]):
        closed.append(closed[0])
    return closed

def _polygon_area(points: Sequence[Point2D]) -> float:
    if len(points) < 3:
        return 0.0
    area = 0.0
    x1, y1 = points[-1]
    for x2, y2 in points:
        area += x1 * y2 - x2 * y1
        x1, y1 = x2, y2
    return 0.5 * area

def _require_pyclipper() -> Any:
    if pyclipper is None:
        raise RuntimeError("pyclipper is required for geometry operations. Install it via requirements.txt.")
    return pyclipper

def _polygon_perimeter(points: Sequence[Point2D]) -> float:
    if len(points) < 2:
        return 0.0
    perimeter = 0.0
    count = len(points)
    for i in range(count):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % count]
        perimeter += math.hypot(x2 - x1, y2 - y1)
    return perimeter

def _polygon_centroid(points: Sequence[Point2D]) -> Point2D:
    base = _normalize_polygon(points)
    if len(base) < 3:
        if not base:
            return (0.0, 0.0)
        avg_x = sum(p[0] for p in base) / len(base)
        avg_y = sum(p[1] for p in base) / len(base)
        return (avg_x, avg_y)

    area2 = 0.0
    cx = 0.0
    cy = 0.0
    x1, y1 = base[-1]
    for x2, y2 in base:
        cross = x1 * y2 - x2 * y1
        area2 += cross
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross
        x1, y1 = x2, y2

    if abs(area2) < 1e-9:
        avg_x = sum(p[0] for p in base) / len(base)
        avg_y = sum(p[1] for p in base) / len(base)
        return (avg_x, avg_y)

    scale = 1.0 / (3.0 * area2)
    return (cx * scale, cy * scale)

def _is_circular_polygon(points: Sequence[Point2D],
                         circularity_threshold: float,
                         radius_variation: float) -> bool:
    base = _normalize_polygon(points)
    if len(base) < 5:
        return False
    area = abs(_polygon_area(base))
    perimeter = _polygon_perimeter(base)
    if area <= 0.0 or perimeter <= 0.0:
        return False
    circularity = 4.0 * math.pi * area / (perimeter * perimeter)
    if circularity < circularity_threshold:
        return False
    cx, cy = _polygon_centroid(base)
    radii = [math.hypot(x - cx, y - cy) for x, y in base]
    mean_radius = sum(radii) / len(radii)
    if mean_radius <= 1e-6:
        return False
    variance = sum((r - mean_radius) ** 2 for r in radii) / len(radii)
    std_norm = math.sqrt(variance) / mean_radius
    return std_norm <= radius_variation

def _is_clockwise(points: Sequence[Point2D]) -> bool:
    return _polygon_area(points) < 0.0

def lowest_planar_face(vertices: np.ndarray,
                       faces: np.ndarray,
                       up_axis: Tuple[float, float, float] = (0.0, 0.0, 1.0),
                       normal_threshold: float = 0.9) -> Tuple[np.ndarray, np.ndarray] | None:
    """Return (normal, centroid) for the lowest mostly-planar face."""
    if vertices is None or faces is None:
        return None
    verts = np.asarray(vertices, dtype=float)
    fac = np.asarray(faces, dtype=int)
    if verts.size == 0 or fac.size == 0:
        return None
    axis = np.array(up_axis, dtype=float)
    axis_norm = float(np.linalg.norm(axis))
    if axis_norm < 1e-9:
        axis = np.array([0.0, 0.0, 1.0], dtype=float)
    else:
        axis = axis / axis_norm

    best = None
    for tri in fac:
        try:
            a, b, c = verts[tri]
        except Exception:
            continue
        n = np.cross(b - a, c - a)
        n_norm = float(np.linalg.norm(n))
        if n_norm <= 1e-9:
            continue
        area = n_norm * 0.5
        n_unit = n / max(1e-9, n_norm)
        dot = float(np.dot(n_unit, axis))
        if abs(dot) < normal_threshold:
            continue
        centroid = (a + b + c) / 3.0
        height = float(np.dot(centroid, axis))
        if best is None or height < best[0] or (abs(height - best[0]) < 1e-6 and area > best[2]):
            best = (height, centroid, area, n_unit)

    if best is None:
        return None
    _height, centroid, _area, normal = best
    if float(np.dot(normal, axis)) > 0.0:
        normal = -normal
    return normal, centroid

def arrange_rectangles(sizes: Sequence[Tuple[int, float, float]],
                       spacing: float,
                       align_y: bool = False) -> Dict[int, Tuple[float, float]]:
    """Arrange rectangles (id, width, depth) with spacing and center the layout."""
    spacing_val = max(0.0, float(spacing))
    if not sizes:
        return {}

    positions: Dict[int, Tuple[float, float]] = {}
    sizes_list = [(mid, float(w), float(d)) for mid, w, d in sizes]

    if align_y:
        total_depth = sum(d for _mid, _w, d in sizes_list) + spacing_val * (len(sizes_list) - 1)
        y_cursor = -total_depth / 2.0
        for mid, w, d in sizes_list:
            y = y_cursor + d / 2.0
            positions[mid] = (0.0, y)
            y_cursor += d + spacing_val
    else:
        total_area = sum(w * d for _mid, w, d in sizes_list)
        target_width = math.sqrt(total_area) if total_area > 0.0 else 0.0
        x_cursor = 0.0
        y_cursor = 0.0
        row_depth = 0.0

        for mid, w, d in sizes_list:
            if x_cursor > 0.0 and target_width > 0.0 and (x_cursor + w) > target_width:
                x_cursor = 0.0
                y_cursor += row_depth + spacing_val
                row_depth = 0.0
            x = x_cursor + w / 2.0
            y = y_cursor + d / 2.0
            positions[mid] = (x, y)
            x_cursor += w + spacing_val
            row_depth = max(row_depth, d)

        if positions:
            cx = sum(pos[0] for pos in positions.values()) / len(positions)
            cy = sum(pos[1] for pos in positions.values()) / len(positions)
            for mid in positions:
                x, y = positions[mid]
                positions[mid] = (x - cx, y - cy)

    return positions

def _clean_loop(points: Sequence[Point2D]) -> Polygon2D:
    cleaned = _dedupe_points(points)
    if len(cleaned) < 3:
        return []
    if abs(_polygon_area(cleaned)) < _MIN_LOOP_AREA:
        return []
    return _close_polygon(cleaned)

def _simplify_polygon(polygon: Sequence[Point2D], tolerance: float) -> List[Polygon2D]:
    pc = _require_pyclipper()
    base = _normalize_polygon(polygon)
    if len(base) < 3:
        return []

    path = _to_clip_path(base)
    if tolerance > 0.0:
        clean_distance = int(round(tolerance * _CLIPPER_SCALE))
        path = pc.CleanPolygon(path, clean_distance)

    if not path or len(path) < 3:
        return []

    simplified = pc.SimplifyPolygon(path, pc.PFT_NONZERO)
    if not simplified:
        simplified = [path]

    loops: List[Polygon2D] = []
    for simp in simplified:
        cleaned = _clean_loop(_from_clip_path(simp))
        if cleaned:
            loops.append(cleaned)
    return loops

def clean_polygons(polygons: Sequence[Sequence[Point2D]],
                   tolerance: float = _CLIPPER_EPS) -> List[Polygon2D]:
    """Clean and simplify polygons, splitting self-intersections when possible."""
    cleaned: List[Polygon2D] = []
    for polygon in polygons:
        cleaned.extend(_simplify_polygon(polygon, tolerance))
    return cleaned

def ensure_winding(polygon: Sequence[Point2D], clockwise: bool) -> Polygon2D:
    """Return a closed polygon with a consistent winding direction."""
    base = _normalize_polygon(polygon)
    if len(base) < 3:
        return []
    is_clockwise = _is_clockwise(base)
    if is_clockwise != clockwise:
        base = list(reversed(base))
    return _close_polygon(base)

def _to_clip_path(points: Sequence[Point2D]) -> List[Tuple[int, int]]:
    return [
        (int(round(x * _CLIPPER_SCALE)), int(round(y * _CLIPPER_SCALE)))
        for x, y in points
    ]

def _from_clip_path(path: Iterable[Tuple[int, int]]) -> Polygon2D:
    return [(x / _CLIPPER_SCALE, y / _CLIPPER_SCALE) for x, y in path]

def slice_mesh(mesh: trimesh.Trimesh | _MeshLike,
               z_height: float,
               tolerance: float = _CLIPPER_EPS) -> List[Polygon2D]:
    """Slice a mesh at a Z plane and return closed 2D loops in XY."""
    mesh_obj = cast(_MeshLike, mesh).mesh if hasattr(mesh, "mesh") else mesh
    if not isinstance(mesh_obj, trimesh.Trimesh):
        raise TypeError("slice_mesh expects a trimesh.Trimesh or a wrapper with .mesh")

    section = mesh_obj.section(plane_origin=(0.0, 0.0, float(z_height)),
                               plane_normal=(0.0, 0.0, 1.0))
    if section is None:
        return []

    if hasattr(section, "to_2D"):
        planar, transform = section.to_2D()
    else:
        planar, transform = section.to_planar()
    loops = []
    for loop in planar.discrete:
        coords = np.asarray(loop, dtype=float)
        if coords.size == 0:
            continue
        coords3 = np.column_stack([coords, np.zeros(len(coords))])
        world = transform_points(coords3, transform)
        loops.append([(float(x), float(y)) for x, y, _z in world])
    try:
        tol = max(0.0, float(tolerance))
    except (TypeError, ValueError):
        tol = _CLIPPER_EPS
    return clean_polygons(loops, tolerance=tol or _CLIPPER_EPS)

def polygons_with_holes(polygons: Sequence[Sequence[Point2D]]) -> List[Island2D]:
    """Group loops into islands with holes using nesting."""
    _require_pyclipper()
    cleaned_polygons = clean_polygons(polygons, tolerance=_CLIPPER_EPS)
    if not cleaned_polygons:
        return []

    loop_data = []
    for loop in cleaned_polygons:
        base = _normalize_polygon(loop)
        if len(base) < 3:
            continue
        area = _polygon_area(base)
        abs_area = abs(area)
        if abs_area <= _MIN_LOOP_AREA:
            continue
        centroid = _polygon_centroid(base)
        loop_data.append(
            {
                "loop": loop,
                "base": base,
                "abs_area": abs_area,
                "centroid": centroid,
            }
        )

    if not loop_data:
        return []

    parents = [-1 for _ in loop_data]
    for i, data in enumerate(loop_data):
        best_parent = -1
        best_area = None
        for j, other in enumerate(loop_data):
            if i == j:
                continue
            if other["abs_area"] <= data["abs_area"] + 1e-9:
                continue
            if point_in_polygon(data["centroid"], other["base"]):
                if best_area is None or other["abs_area"] < best_area:
                    best_area = other["abs_area"]
                    best_parent = j
        parents[i] = best_parent

    depths = [0 for _ in loop_data]
    for i in range(len(loop_data)):
        depth = 0
        parent = parents[i]
        while parent != -1:
            depth += 1
            parent = parents[parent]
        depths[i] = depth

    children: Dict[int, List[int]] = {i: [] for i in range(len(loop_data))}
    for idx, parent in enumerate(parents):
        if parent != -1:
            children[parent].append(idx)

    islands: List[Island2D] = []
    for i, data in enumerate(loop_data):
        if depths[i] % 2 != 0:
            continue
        outer = ensure_winding(data["loop"], clockwise=True)
        if not outer:
            continue
        holes: List[Polygon2D] = []
        for child in children.get(i, []):
            if depths[child] % 2 == 1:
                hole = ensure_winding(loop_data[child]["loop"], clockwise=False)
                if hole:
                    holes.append(hole)
        islands.append((outer, holes))

    return islands

def islands_difference(subject: Sequence[Island2D],
                       clip: Sequence[Island2D]) -> List[Island2D]:
    """Return subject islands with clip islands removed."""
    pc = _require_pyclipper()
    subject_paths = _islands_to_paths(subject)
    if not subject_paths:
        return []
    if not clip:
        return list(subject)

    clip_paths = _islands_to_paths(clip)
    clipper = pc.Pyclipper()
    clipper.AddPaths(subject_paths, pc.PT_SUBJECT, True)
    if clip_paths:
        clipper.AddPaths(clip_paths, pc.PT_CLIP, True)
    tree = clipper.Execute2(pc.CT_DIFFERENCE,
                            pc.PFT_NONZERO,
                            pc.PFT_NONZERO)
    return _polytree_to_islands(tree)

def islands_union(islands: Sequence[Island2D]) -> List[Island2D]:
    """Return a union of all islands."""
    pc = _require_pyclipper()
    paths = _islands_to_paths(islands)
    if not paths:
        return []
    clipper = pc.Pyclipper()
    clipper.AddPaths(paths, pc.PT_SUBJECT, True)
    tree = clipper.Execute2(pc.CT_UNION,
                            pc.PFT_NONZERO,
                            pc.PFT_NONZERO)
    return _polytree_to_islands(tree)

def islands_intersection(subject: Sequence[Island2D],
                         clip: Sequence[Island2D]) -> List[Island2D]:
    """Return subject islands clipped to clip islands."""
    pc = _require_pyclipper()
    subject_paths = _islands_to_paths(subject)
    if not subject_paths:
        return []
    clip_paths = _islands_to_paths(clip)
    if not clip_paths:
        return []
    clipper = pc.Pyclipper()
    clipper.AddPaths(subject_paths, pc.PT_SUBJECT, True)
    clipper.AddPaths(clip_paths, pc.PT_CLIP, True)
    tree = clipper.Execute2(pc.CT_INTERSECTION,
                            pc.PFT_NONZERO,
                            pc.PFT_NONZERO)
    return _polytree_to_islands(tree)

def _islands_to_paths(islands: Sequence[Island2D]) -> List[List[Tuple[int, int]]]:
    paths: List[List[Tuple[int, int]]] = []
    for outer, holes in islands:
        outer_oriented = ensure_winding(outer, clockwise=True)
        if outer_oriented:
            paths.append(_to_clip_path(_normalize_polygon(outer_oriented)))
        for hole in holes:
            hole_oriented = ensure_winding(hole, clockwise=False)
            if hole_oriented:
                paths.append(_to_clip_path(_normalize_polygon(hole_oriented)))
    return paths

def _polytree_to_islands(tree: Any) -> List[Island2D]:
    islands: List[Island2D] = []

    def walk(node: Any) -> None:
        for child in node.Childs:
            if not child.IsHole:
                outer = _clean_loop(_from_clip_path(child.Contour))
                holes: List[Polygon2D] = []
                for hole in child.Childs:
                    if hole.IsHole:
                        cleaned_hole = _clean_loop(_from_clip_path(hole.Contour))
                        if cleaned_hole:
                            holes.append(cleaned_hole)
                if outer:
                    oriented_outer = ensure_winding(outer, clockwise=True)
                    oriented_holes = [ensure_winding(h, clockwise=False) for h in holes]
                    islands.append((oriented_outer, oriented_holes))
            walk(child)

    walk(tree)
    return islands

def offset_islands(islands: Sequence[Island2D], distance: float) -> List[Island2D]:
    """Offset island polygons (outer + holes) by a signed distance."""
    pc = _require_pyclipper()
    if not islands:
        return []

    result: List[Island2D] = []
    for outer, holes in islands:
        offsetter = pc.PyclipperOffset()
        oriented_outer = ensure_winding(outer, clockwise=True)
        if oriented_outer:
            offsetter.AddPath(_to_clip_path(_normalize_polygon(oriented_outer)),
                              pc.JT_MITER,
                              pc.ET_CLOSEDPOLYGON)
        for hole in holes:
            oriented_hole = ensure_winding(hole, clockwise=False)
            if oriented_hole:
                offsetter.AddPath(_to_clip_path(_normalize_polygon(oriented_hole)),
                                  pc.JT_MITER,
                                  pc.ET_CLOSEDPOLYGON)

        paths = offsetter.Execute(distance * _CLIPPER_SCALE)
        if not paths:
            continue
        loops = [_from_clip_path(path) for path in paths]
        result.extend(polygons_with_holes(loops))
    return result

def offset_polygon(polygon: Sequence[Point2D], distance: float) -> List[Polygon2D]:
    """Offset a polygon by a signed distance, returning zero or more polygons."""
    pc = _require_pyclipper()
    loops = clean_polygons([polygon], tolerance=_CLIPPER_EPS)
    if not loops:
        return []

    offsetter = pc.PyclipperOffset()
    for loop in loops:
        base = _normalize_polygon(loop)
        if len(base) < 3:
            continue
        offsetter.AddPath(_to_clip_path(base), pc.JT_MITER, pc.ET_CLOSEDPOLYGON)
    paths = offsetter.Execute(distance * _CLIPPER_SCALE)

    result: List[Polygon2D] = []
    for path in paths:
        points = _from_clip_path(path)
        cleaned = _clean_loop(points)
        if cleaned:
            result.append(cleaned)
    return result

def clip_lines_to_polygon(lines: Sequence[LineSegment2D],
                          polygon: Sequence[Point2D]) -> List[LineSegment2D]:
    """Clip line segments to a polygon boundary."""
    return _clip_lines_to_paths(lines, [polygon])

def clip_lines_to_island(lines: Sequence[LineSegment2D],
                         outer: Sequence[Point2D],
                         holes: Sequence[Sequence[Point2D]]) -> List[LineSegment2D]:
    """Clip line segments to an island (outer polygon with holes)."""
    if not lines:
        return []
    paths: List[Sequence[Point2D]] = []
    outer_oriented = ensure_winding(outer, clockwise=True)
    if outer_oriented:
        paths.append(outer_oriented)
    for hole in holes:
        hole_oriented = ensure_winding(hole, clockwise=False)
        if hole_oriented:
            paths.append(hole_oriented)
    if not paths:
        return []
    return _clip_lines_to_paths(lines, paths)

def _clip_lines_to_paths(lines: Sequence[LineSegment2D],
                         paths: Sequence[Sequence[Point2D]]) -> List[LineSegment2D]:
    pc = _require_pyclipper()
    clipper = pc.Pyclipper()
    clip_added = False
    for path in paths:
        base = _normalize_polygon(path)
        if len(base) < 3:
            continue
        clipper.AddPath(_to_clip_path(base), pc.PT_CLIP, True)
        clip_added = True

    if not clip_added:
        return []

    subject_paths: List[List[Tuple[int, int]]] = []
    for line in lines:
        if len(line) != 2:
            continue
        subject_paths.append(_to_clip_path(line))

    if not subject_paths:
        return []

    clipper.AddPaths(subject_paths, pc.PT_SUBJECT, False)
    solution_tree = clipper.Execute2(pc.CT_INTERSECTION,
                                     pc.PFT_NONZERO,
                                     pc.PFT_NONZERO)

    try:
        open_paths = pc.OpenPathsFromPolyTree(solution_tree)
    except AttributeError:
        open_paths = getattr(solution_tree, "OpenPaths", []) or []

    clipped: List[LineSegment2D] = []
    for path in open_paths:
        if len(path) < 2:
            continue
        points = _from_clip_path(path)
        for i in range(len(points) - 1):
            if _points_close(points[i], points[i + 1]):
                continue
            clipped.append((points[i], points[i + 1]))
    return clipped

def point_in_polygon(point: Point2D, polygon: Sequence[Point2D]) -> bool:
    pc = _require_pyclipper()
    base = _normalize_polygon(polygon)
    if len(base) < 3:
        return False
    path = _to_clip_path(base)
    pt = (int(round(point[0] * _CLIPPER_SCALE)), int(round(point[1] * _CLIPPER_SCALE)))
    return pc.PointInPolygon(pt, path) > 0

def point_in_island(point: Point2D, island: Island2D) -> bool:
    outer, holes = island
    if not point_in_polygon(point, outer):
        return False
    for hole in holes:
        if point_in_polygon(point, hole):
            return False
    return True

def line_inside_island(segment: LineSegment2D,
                       island: Island2D,
                       samples: int = 8) -> bool:
    start, end = segment
    if not point_in_island(start, island) or not point_in_island(end, island):
        return False
    for step in range(1, max(1, samples)):
        t = step / samples
        x = start[0] + (end[0] - start[0]) * t
        y = start[1] + (end[1] - start[1]) * t
        if not point_in_island((x, y), island):
            return False
    return True

def path_inside_island(points: Sequence[Point2D],
                       island: Island2D,
                       samples: int = 8) -> bool:
    if len(points) < 2:
        return False
    for i in range(len(points) - 1):
        if not line_inside_island((points[i], points[i + 1]), island, samples=samples):
            return False
    return True

def _loops_to_lines(loops: Sequence[Sequence[Point2D]]) -> List[LineSegment2D]:
    segments: List[LineSegment2D] = []
    for loop in loops:
        if len(loop) < 2:
            continue
        points = list(loop)
        if points[0] != points[-1]:
            points.append(points[0])
        for i in range(len(points) - 1):
            if _points_close(points[i], points[i + 1]):
                continue
            segments.append((points[i], points[i + 1]))
    return segments

def thin_wall_lines(islands: Sequence[Island2D],
                    extrusion_width: float) -> List[LineSegment2D]:
    """Approximate thin walls as centerline paths."""
    width = max(0.0, float(extrusion_width))
    if width <= 0.0:
        return []
    lines: List[LineSegment2D] = []
    for outer, holes in islands:
        offset = offset_polygon(outer, -width)
        if offset:
            lines.extend(_loops_to_lines(offset))
        else:
            center = offset_polygon(outer, -width * 0.5)
            if center:
                lines.extend(_loops_to_lines(center))
            else:
                base = _normalize_polygon(outer)
                if base:
                    xs = [p[0] for p in base]
                    ys = [p[1] for p in base]
                    min_x, max_x = min(xs), max(xs)
                    min_y, max_y = min(ys), max(ys)
                    span_x = max_x - min_x
                    span_y = max_y - min_y
                    if min(span_x, span_y) <= width and max(span_x, span_y) > 0.0:
                        if span_x <= span_y:
                            x = (min_x + max_x) / 2.0
                            lines.append(((x, min_y), (x, max_y)))
                        else:
                            y = (min_y + max_y) / 2.0
                            lines.append(((min_x, y), (max_x, y)))
        for hole in holes:
            offset_hole = offset_polygon(hole, -width)
            if offset_hole:
                lines.extend(_loops_to_lines(offset_hole))
            else:
                center = offset_polygon(hole, -width * 0.5)
                if center:
                    lines.extend(_loops_to_lines(center))
    return lines

def gap_fill_lines(islands: Sequence[Island2D],
                   extrusion_width: float,
                   perimeter_spacing: float) -> List[LineSegment2D]:
    """Detect narrow gaps between perimeters and return fill lines."""
    spacing = max(0.0, float(perimeter_spacing))
    width = max(0.0, float(extrusion_width))
    if spacing <= 0.0 or width <= 0.0 or not islands:
        return []

    inset = offset_islands(islands, -spacing)
    if not inset:
        return []
    gaps = islands_difference(islands, inset)
    if not gaps:
        return []

    lines: List[LineSegment2D] = []
    for outer, holes in gaps:
        offset = offset_polygon(outer, -width)
        if offset:
            lines.extend(_loops_to_lines(offset))
        else:
            center = offset_polygon(outer, -width * 0.5)
            if center:
                lines.extend(_loops_to_lines(center))
        for hole in holes:
            offset_hole = offset_polygon(hole, -width)
            if offset_hole:
                lines.extend(_loops_to_lines(offset_hole))
            else:
                center = offset_polygon(hole, -width * 0.5)
                if center:
                    lines.extend(_loops_to_lines(center))
    return lines

def _best_offset_loops(polygon: Sequence[Point2D],
                       distance: float) -> List[Polygon2D]:
    if distance == 0.0:
        return offset_polygon(polygon, distance)
    candidates: List[Tuple[float, List[Polygon2D]]] = []
    for delta in (distance, -distance):
        loops = offset_polygon(polygon, delta)
        if not loops:
            continue
        area_sum = sum(abs(_polygon_area(_normalize_polygon(loop))) for loop in loops)
        candidates.append((area_sum, loops))
    if not candidates:
        return []
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]

def compensate_holes(islands: Sequence[Island2D],
                     compensation_mm: float,
                     circularity_threshold: float = 0.8,
                     radius_variation: float = 0.2) -> List[Island2D]:
    """Expand circular holes to compensate for shrinkage."""
    distance = max(0.0, float(compensation_mm))
    if distance <= 0.0 or not islands:
        return list(islands)

    result: List[Island2D] = []
    for outer, holes in islands:
        adjusted: List[Polygon2D] = []
        for hole in holes:
            if _is_circular_polygon(hole, circularity_threshold, radius_variation):
                loops = _best_offset_loops(hole, distance)
                if loops:
                    for loop in loops:
                        oriented = ensure_winding(loop, clockwise=False)
                        if oriented:
                            adjusted.append(oriented)
                    continue
            oriented_hole = ensure_winding(hole, clockwise=False)
            if oriented_hole:
                adjusted.append(oriented_hole)
        result.append((outer, adjusted))
    return result

def compute_bounding_square(bounds: Tuple[Tuple[float, float, float], Tuple[float, float, float]]):
    """Return a simple XY square that covers the mesh bounds.

    Args:
        bounds: ((minx, miny, minz), (maxx, maxy, maxz))

    Returns:
        List of (x, y) points in order around the square.
    """
    (minx, miny, _), (maxx, maxy, _) = bounds
    return [
        (minx, miny),
        (maxx, miny),
        (maxx, maxy),
        (minx, maxy),
        (minx, miny),
    ]
