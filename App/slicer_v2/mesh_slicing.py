from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import struct
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .errors import SlicerV2MeshSlicingError
from .geometry import EPSILON, Point2, Polygon, polygon_from_tuples
from .polygon_pipeline import cleanup_polygon

try:
    import trimesh
except Exception:  # pragma: no cover - optional dependency in minimal environments
    trimesh = None


MAX_TRIANGLE_COUNT = 2_000_000


@dataclass(frozen=True)
class Point3:
    x: float
    y: float
    z: float


Triangle3 = tuple[Point3, Point3, Point3]
Segment2 = tuple[Point2, Point2]


@dataclass(frozen=True)
class MeshData:
    mesh_path: str
    source_format: str
    triangles: tuple[Triangle3, ...]
    z_min_mm: float = 0.0
    z_max_mm: float = 0.0
    x_min_mm: float = 0.0
    x_max_mm: float = 0.0
    y_min_mm: float = 0.0
    y_max_mm: float = 0.0


@dataclass
class LayerContourSet:
    layer_index: int
    z_height_mm: float
    segment_count: int
    contour_count: int
    contours: list[Polygon] = field(default_factory=list)


@dataclass
class MeshSlicingReport:
    generated_at_utc: str
    mesh_path: str
    source_format: str
    triangle_count: int
    layer_count: int
    segment_count_total: int
    contour_count_total: int
    warning_count: int
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _point2_close(a: Point2, b: Point2, tolerance: float) -> bool:
    return abs(a.x - b.x) <= tolerance and abs(a.y - b.y) <= tolerance


def _point2_key(point: Point2, tolerance: float) -> tuple[int, int]:
    tol = max(tolerance, EPSILON)
    return (int(round(point.x / tol)), int(round(point.y / tol)))


def _segment_key(segment: Segment2, tolerance: float) -> tuple[tuple[int, int], tuple[int, int]]:
    a_key = _point2_key(segment[0], tolerance)
    b_key = _point2_key(segment[1], tolerance)
    if a_key <= b_key:
        return (a_key, b_key)
    return (b_key, a_key)


def _parse_ascii_stl(data: bytes) -> tuple[Triangle3, ...]:
    text = data.decode("utf-8", errors="ignore")
    vertices: list[Point3] = []
    lines = text.splitlines()
    max_lines = min(len(lines), 5_000_000)
    for idx in range(max_lines):
        line = lines[idx].strip()
        if not line.lower().startswith("vertex "):
            continue
        parts = line.split()
        if len(parts) < 4:
            continue
        try:
            x = float(parts[1])
            y = float(parts[2])
            z = float(parts[3])
        except (TypeError, ValueError):
            continue
        vertices.append(Point3(x, y, z))

    triangle_count = len(vertices) // 3
    if triangle_count <= 0:
        return ()
    triangles: list[Triangle3] = []
    for idx in range(triangle_count):
        base = idx * 3
        triangles.append((vertices[base], vertices[base + 1], vertices[base + 2]))
    return tuple(triangles)


def _parse_binary_stl(data: bytes) -> tuple[Triangle3, ...]:
    if len(data) < 84:
        return ()
    tri_count = int(struct.unpack("<I", data[80:84])[0])
    if tri_count <= 0:
        return ()
    if tri_count > MAX_TRIANGLE_COUNT:
        raise SlicerV2MeshSlicingError(f"TRIANGLE_COUNT_TOO_LARGE:{tri_count}")

    expected_size = 84 + tri_count * 50
    if len(data) < expected_size:
        raise SlicerV2MeshSlicingError("BINARY_STL_TRUNCATED")

    triangles: list[Triangle3] = []
    for idx in range(tri_count):
        offset = 84 + idx * 50
        chunk = data[offset : offset + 50]
        unpacked = struct.unpack("<12fH", chunk)
        p1 = Point3(unpacked[3], unpacked[4], unpacked[5])
        p2 = Point3(unpacked[6], unpacked[7], unpacked[8])
        p3 = Point3(unpacked[9], unpacked[10], unpacked[11])
        triangles.append((p1, p2, p3))
    return tuple(triangles)


def _build_mesh_data(mesh_path: Path, source_format: str, triangles: tuple[Triangle3, ...]) -> MeshData:
    x_min = min(point.x for tri in triangles for point in tri)
    x_max = max(point.x for tri in triangles for point in tri)
    y_min = min(point.y for tri in triangles for point in tri)
    y_max = max(point.y for tri in triangles for point in tri)
    z_min = min(point.z for tri in triangles for point in tri)
    z_max = max(point.z for tri in triangles for point in tri)
    if z_max < z_min:
        raise SlicerV2MeshSlicingError("MESH_Z_BOUNDS_INVALID")

    return MeshData(
        mesh_path=str(mesh_path.resolve()),
        source_format=source_format,
        triangles=triangles,
        x_min_mm=float(x_min),
        x_max_mm=float(x_max),
        y_min_mm=float(y_min),
        y_max_mm=float(y_max),
        z_min_mm=float(z_min),
        z_max_mm=float(z_max),
    )


def _coerce_trimesh_mesh(raw_mesh: object) -> object | None:
    if trimesh is None:
        return None

    if isinstance(raw_mesh, trimesh.Trimesh):
        return raw_mesh

    if isinstance(raw_mesh, trimesh.Scene):
        geometries = [geom for geom in raw_mesh.geometry.values() if isinstance(geom, trimesh.Trimesh)]
        if not geometries:
            return None
        return trimesh.util.concatenate(geometries)

    dump = getattr(raw_mesh, "dump", None)
    if callable(dump):
        dumped = dump()
        if isinstance(dumped, trimesh.Trimesh):
            return dumped
        try:
            return trimesh.util.concatenate(dumped)
        except Exception:
            return None
    return None


def _repair_trimesh_mesh(mesh_obj: object) -> object:
    repaired = mesh_obj.copy()
    process = getattr(repaired, "process", None)
    if callable(process):
        try:
            process(validate=True)
        except Exception:
            pass

    for method_name in (
        "remove_duplicate_faces",
        "remove_degenerate_faces",
        "remove_infinite_values",
        "remove_unreferenced_vertices",
    ):
        method = getattr(repaired, method_name, None)
        if callable(method):
            try:
                method()
            except Exception:
                continue
    return repaired


def _load_with_trimesh(mesh_path: Path) -> MeshData | None:
    if trimesh is None:
        return None

    try:
        raw_mesh = trimesh.load(str(mesh_path), force="mesh", process=False)
    except Exception:
        return None

    mesh_obj = _coerce_trimesh_mesh(raw_mesh)
    if mesh_obj is None:
        return None

    mesh_obj = _repair_trimesh_mesh(mesh_obj)
    faces = getattr(mesh_obj, "faces", None)
    vertices = getattr(mesh_obj, "vertices", None)
    if faces is None or vertices is None:
        return None
    if len(faces) <= 0:
        return None

    triangle_count = int(len(faces))
    if triangle_count > MAX_TRIANGLE_COUNT:
        raise SlicerV2MeshSlicingError(f"TRIANGLE_COUNT_TOO_LARGE:{triangle_count}")

    triangles: list[Triangle3] = []
    try:
        for face in faces:
            p1 = vertices[int(face[0])]
            p2 = vertices[int(face[1])]
            p3 = vertices[int(face[2])]
            triangles.append(
                (
                    Point3(float(p1[0]), float(p1[1]), float(p1[2])),
                    Point3(float(p2[0]), float(p2[1]), float(p2[2])),
                    Point3(float(p3[0]), float(p3[1]), float(p3[2])),
                )
            )
    except Exception:
        return None

    if not triangles:
        return None

    suffix = mesh_path.suffix.lower().lstrip(".") or "mesh"
    return _build_mesh_data(mesh_path, f"trimesh-{suffix}", tuple(triangles))


def load_mesh_file(mesh_path: str) -> MeshData:
    path = Path(mesh_path).expanduser()
    if not path.exists():
        raise SlicerV2MeshSlicingError(f"MESH_PATH_MISSING:{path}")
    if not path.is_file():
        raise SlicerV2MeshSlicingError(f"MESH_PATH_NOT_FILE:{path}")

    data = path.read_bytes()
    if not data:
        raise SlicerV2MeshSlicingError("MESH_FILE_EMPTY")

    triangles: tuple[Triangle3, ...] = ()
    source_format = "unknown"

    suffix = path.suffix.lower()
    should_try_stl_parse = suffix in {".stl", ""}
    if should_try_stl_parse and data[:5].lower() == b"solid":
        triangles = _parse_ascii_stl(data)
        if triangles:
            source_format = "ascii-stl"

    if should_try_stl_parse and not triangles:
        try:
            triangles = _parse_binary_stl(data)
        except SlicerV2MeshSlicingError:
            triangles = ()
        if triangles:
            source_format = "binary-stl"

    if not triangles:
        fallback = _load_with_trimesh(path)
        if fallback is not None:
            return fallback
        raise SlicerV2MeshSlicingError("MESH_TRIANGLES_NOT_FOUND")

    return _build_mesh_data(path, source_format, triangles)


def slice_triangle_at_z(triangle: Triangle3, z_height: float, tolerance: float = 1e-6) -> Segment2 | None:
    z = float(z_height)
    tol = max(float(tolerance), EPSILON)
    points = [triangle[0], triangle[1], triangle[2]]
    intersections: list[Point2] = []

    def add_point(x: float, y: float) -> None:
        point = Point2(x, y)
        for existing in intersections:
            if _point2_close(existing, point, tol):
                return
        intersections.append(point)

    edges = ((0, 1), (1, 2), (2, 0))
    for edge in edges:
        a = points[edge[0]]
        b = points[edge[1]]
        d_a = a.z - z
        d_b = b.z - z

        on_a = abs(d_a) <= tol
        on_b = abs(d_b) <= tol

        if on_a:
            add_point(a.x, a.y)
        if on_b:
            add_point(b.x, b.y)

        if d_a * d_b < -(tol * tol):
            t = d_a / (d_a - d_b)
            x = a.x + (b.x - a.x) * t
            y = a.y + (b.y - a.y) * t
            add_point(x, y)

    if len(intersections) < 2:
        return None
    if len(intersections) == 2:
        if intersections[0].distance_to(intersections[1]) <= tol:
            return None
        return (intersections[0], intersections[1])

    best: Segment2 | None = None
    best_dist = -1.0
    for i in range(len(intersections)):
        for j in range(i + 1, len(intersections)):
            d = intersections[i].distance_to(intersections[j])
            if d > best_dist:
                best_dist = d
                best = (intersections[i], intersections[j])
    if best is None or best_dist <= tol:
        return None
    return best


def slice_mesh_at_z(mesh: MeshData, z_height: float, tolerance: float = 1e-6) -> list[Segment2]:
    z = float(z_height)
    tol = max(float(tolerance), EPSILON)
    unique_segments: dict[tuple[tuple[int, int], tuple[int, int]], Segment2] = {}
    for triangle in mesh.triangles:
        segment = slice_triangle_at_z(triangle, z, tolerance=tol)
        if segment is None:
            continue
        key = _segment_key(segment, tol)
        if key not in unique_segments:
            unique_segments[key] = segment
    return list(unique_segments.values())


def assemble_contours_from_segments(
    segments: Iterable[Segment2],
    *,
    join_tolerance: float = 1e-4,
    min_area: float = 1e-6,
) -> list[Polygon]:
    seg_list = list(segments)
    if not seg_list:
        return []

    tol = max(float(join_tolerance), EPSILON)
    used = [False] * len(seg_list)
    polygons: list[Polygon] = []
    max_outer = len(seg_list)

    for start_idx in range(max_outer):
        if used[start_idx]:
            continue
        seg = seg_list[start_idx]
        chain: list[Point2] = [seg[0], seg[1]]
        used[start_idx] = True

        max_steps = len(seg_list) + 2
        for _step in range(max_steps):
            if len(chain) >= 3 and _point2_close(chain[-1], chain[0], tol):
                break
            end_point = chain[-1]
            next_idx = -1
            next_point: Point2 | None = None
            for cand_idx in range(len(seg_list)):
                if used[cand_idx]:
                    continue
                cand = seg_list[cand_idx]
                if _point2_close(cand[0], end_point, tol):
                    next_idx = cand_idx
                    next_point = cand[1]
                    break
                if _point2_close(cand[1], end_point, tol):
                    next_idx = cand_idx
                    next_point = cand[0]
                    break
            if next_idx < 0 or next_point is None:
                break
            used[next_idx] = True
            if not _point2_close(next_point, chain[-1], tol):
                chain.append(next_point)

        if len(chain) < 3:
            continue
        if not _point2_close(chain[-1], chain[0], tol):
            continue

        tuples = [point.as_tuple() for point in chain]
        try:
            polygon = polygon_from_tuples(tuples)
        except Exception:
            continue
        cleaned = cleanup_polygon(polygon, min_area=min_area)
        if cleaned is None:
            continue
        polygons.append(cleaned.with_winding(clockwise=False))

    return polygons


def slice_mesh_to_contours(
    mesh: MeshData,
    layer_z_values: Iterable[float],
    *,
    join_tolerance: float = 1e-4,
    min_area: float = 1e-6,
    max_workers: int = 1,
) -> tuple[list[LayerContourSet], MeshSlicingReport]:
    layers = list(layer_z_values)
    warnings: list[str] = []

    def _slice_one(idx: int) -> tuple[LayerContourSet, str | None]:
        z = float(layers[idx])
        segments = slice_mesh_at_z(mesh, z)
        contours = assemble_contours_from_segments(
            segments,
            join_tolerance=join_tolerance,
            min_area=min_area,
        )
        warning: str | None = None
        if segments and not contours:
            warning = f"layer_{idx}:segments_without_contours:{len(segments)}"
        return (
            LayerContourSet(
                layer_index=idx,
                z_height_mm=z,
                segment_count=len(segments),
                contour_count=len(contours),
                contours=contours,
            ),
            warning,
        )

    layer_sets: list[LayerContourSet] = []
    worker_count = max(1, min(int(max_workers), len(layers) if layers else 1))
    if worker_count > 1 and len(layers) > 1:
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            results = list(executor.map(_slice_one, range(len(layers))))
    else:
        results = [_slice_one(idx) for idx in range(len(layers))]

    for layer_set, warning in results:
        layer_sets.append(layer_set)
        if warning:
            warnings.append(warning)

    segment_total = sum(layer.segment_count for layer in layer_sets)
    contour_total = sum(layer.contour_count for layer in layer_sets)

    report = MeshSlicingReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        mesh_path=mesh.mesh_path,
        source_format=mesh.source_format,
        triangle_count=len(mesh.triangles),
        layer_count=len(layer_sets),
        segment_count_total=segment_total,
        contour_count_total=contour_total,
        warning_count=len(warnings),
        warnings=warnings,
    )
    return layer_sets, report
