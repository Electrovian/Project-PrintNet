import os
import struct
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.errors import SlicerV2MeshSlicingError  # noqa: E402
from slicer_v2.geometry import Point2  # noqa: E402
from slicer_v2.mesh_slicing import (  # noqa: E402
    MeshData,
    Point3,
    assemble_contours_from_segments,
    load_mesh_file,
    slice_mesh_at_z,
    slice_mesh_to_contours,
    slice_triangle_at_z,
)


def _write_ascii_stl(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "solid eon",
                "facet normal 0 0 1",
                "outer loop",
                "vertex 0 0 0",
                "vertex 1 0 1",
                "vertex 0 1 1",
                "endloop",
                "endfacet",
                "endsolid eon",
            ]
        ),
        encoding="utf-8",
    )


def _write_binary_stl(path: Path) -> None:
    header = b"EON-BINARY-STL".ljust(80, b"\x00")
    tri_count = struct.pack("<I", 1)
    # normal + 3 vertices + attribute count
    chunk = struct.pack(
        "<12fH",
        0.0,
        0.0,
        1.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        1.0,
        0.0,
        1.0,
        1.0,
        0,
    )
    path.write_bytes(header + tri_count + chunk)


def _write_obj(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "o eon",
                "v 0 0 0",
                "v 1 0 0",
                "v 0 1 1",
                "f 1 2 3",
            ]
        ),
        encoding="utf-8",
    )


def _build_box_mesh() -> MeshData:
    # Unit cube [0,1]^3 with 12 triangles.
    v = [
        Point3(0, 0, 0),
        Point3(1, 0, 0),
        Point3(1, 1, 0),
        Point3(0, 1, 0),
        Point3(0, 0, 1),
        Point3(1, 0, 1),
        Point3(1, 1, 1),
        Point3(0, 1, 1),
    ]
    triangles = (
        (v[0], v[1], v[2]),
        (v[0], v[2], v[3]),
        (v[4], v[5], v[6]),
        (v[4], v[6], v[7]),
        (v[0], v[1], v[5]),
        (v[0], v[5], v[4]),
        (v[1], v[2], v[6]),
        (v[1], v[6], v[5]),
        (v[2], v[3], v[7]),
        (v[2], v[7], v[6]),
        (v[3], v[0], v[4]),
        (v[3], v[4], v[7]),
    )
    return MeshData(
        mesh_path="box",
        source_format="synthetic",
        triangles=triangles,
        z_min_mm=0.0,
        z_max_mm=1.0,
    )


class TestSlicerV2MeshSlicing(unittest.TestCase):
    def test_load_ascii_mesh(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ascii.stl"
            _write_ascii_stl(path)
            mesh = load_mesh_file(str(path))
            self.assertEqual(mesh.source_format, "ascii-stl")
            self.assertEqual(len(mesh.triangles), 1)
            self.assertGreater(mesh.z_max_mm, mesh.z_min_mm)

    def test_load_binary_mesh(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "binary.stl"
            _write_binary_stl(path)
            mesh = load_mesh_file(str(path))
            self.assertEqual(mesh.source_format, "binary-stl")
            self.assertEqual(len(mesh.triangles), 1)

    def test_load_obj_mesh_uses_trimesh_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mesh.obj"
            _write_obj(path)
            mesh = load_mesh_file(str(path))
            self.assertEqual(mesh.source_format, "trimesh-obj")
            self.assertEqual(len(mesh.triangles), 1)

    def test_slice_triangle_at_z(self) -> None:
        triangle = (
            Point3(0.0, 0.0, 0.0),
            Point3(2.0, 0.0, 2.0),
            Point3(0.0, 2.0, 2.0),
        )
        segment = slice_triangle_at_z(triangle, 1.0)
        self.assertIsNotNone(segment)
        assert segment is not None
        self.assertAlmostEqual(segment[0].y + segment[1].y, 1.0, places=5)
        self.assertGreater(segment[0].distance_to(segment[1]), 1.0)

    def test_assemble_square_contour_from_segments(self) -> None:
        segments = [
            (Point2(0, 0), Point2(1, 0)),
            (Point2(1, 0), Point2(1, 1)),
            (Point2(1, 1), Point2(0, 1)),
            (Point2(0, 1), Point2(0, 0)),
        ]
        contours = assemble_contours_from_segments(segments)
        self.assertEqual(len(contours), 1)
        self.assertAlmostEqual(contours[0].area, 1.0)

    def test_slice_mesh_to_contours_box(self) -> None:
        mesh = _build_box_mesh()
        layers, report = slice_mesh_to_contours(mesh, [0.5])
        self.assertEqual(len(layers), 1)
        self.assertGreaterEqual(layers[0].segment_count, 4)
        self.assertGreaterEqual(layers[0].contour_count, 1)
        self.assertGreaterEqual(report.segment_count_total, 4)
        self.assertGreaterEqual(report.contour_count_total, 1)

    def test_slice_mesh_at_z_for_box(self) -> None:
        mesh = _build_box_mesh()
        segments = slice_mesh_at_z(mesh, 0.5)
        self.assertGreaterEqual(len(segments), 4)

    def test_missing_mesh_path_fails(self) -> None:
        with self.assertRaises(SlicerV2MeshSlicingError):
            load_mesh_file("C:/path/does/not/exist.stl")


if __name__ == "__main__":
    unittest.main()
