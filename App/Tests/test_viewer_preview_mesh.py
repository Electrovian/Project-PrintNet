import os
import sys

import numpy as np


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui.viewer.preview import PreviewMixin  # noqa: E402
from slicer_v2.legacy_gcode_preview import GCodePreview, PreviewLayer, PreviewSegment  # noqa: E402


class _PreviewHarness(PreviewMixin):
    def __init__(self) -> None:
        self._preview_base_width = 0.4
        self._preview_layer_height = 0.2
        self._preview_bed_x = 0.0
        self._preview_bed_y = 0.0
        self._preview_empty_mesh = None
        self._preview_data = None
        self._preview_layer_index = None
        self._preview_step_index = None


def test_preview_mesh_builder_returns_empty_mesh_for_no_segments():
    harness = _PreviewHarness()
    mesh = harness._preview_mesh_for_segments([], [])
    vertices = np.asarray(mesh.vertexes(), dtype=float)
    faces = np.asarray(mesh.faces(), dtype=np.int32)
    assert vertices.shape == (0, 3)
    assert faces.shape == (0, 3)


def test_preview_mesh_builder_extends_caps_to_reduce_corner_gaps():
    harness = _PreviewHarness()
    mesh = harness._preview_mesh_for_segments(
        [
            ((0.0, 0.0, 0.2), (10.0, 0.0, 0.2)),
            ((10.0, 0.0, 0.2), (10.0, 10.0, 0.2)),
        ],
        [0.4, 0.4],
    )

    vertices = np.asarray(mesh.vertexes(), dtype=float)
    assert vertices.shape[0] == 16

    first_segment_vertices = vertices[:8]
    second_segment_vertices = vertices[8:16]

    # Corner continuity: first segment extends beyond the nominal X end.
    assert float(first_segment_vertices[:, 0].max()) > 10.0
    # Corner continuity: second segment extends before the nominal Y start.
    assert float(second_segment_vertices[:, 1].min()) < 0.0


def test_preview_nozzle_state_is_recentered_from_bed_space():
    harness = _PreviewHarness()
    harness._preview_bed_x = 300.0
    harness._preview_bed_y = 280.0
    harness._preview_data = GCodePreview(
        layers=[
            PreviewLayer(
                z=0.2,
                segments=[
                    PreviewSegment(
                        start=(150.0, 140.0, 0.2),
                        end=(160.0, 145.0, 0.2),
                        speed=30.0,
                        extrusion=0.5,
                        flow=1.0,
                        width=0.4,
                        feature="outer_wall",
                        is_extrude=True,
                    )
                ],
            )
        ],
        min_speed=0.0,
        max_speed=30.0,
        min_flow=0.0,
        max_flow=1.0,
        min_width=0.0,
        max_width=0.4,
        min_layer_height=0.0,
        max_layer_height=0.2,
        min_layer_time=0.0,
        max_layer_time=1.0,
        min_fan=0.0,
        max_fan=0.0,
        min_temp=0.0,
        max_temp=0.0,
    )
    harness._preview_layer_index = 0

    pos, speed, is_extrude = harness.get_preview_nozzle_state()

    assert pos == (10.0, 5.0, 0.2)
    assert speed == 30.0
    assert is_extrude is True


def test_preview_segment_pair_is_recentered_for_mesh_rendering():
    harness = _PreviewHarness()
    harness._preview_bed_x = 300.0
    harness._preview_bed_y = 280.0
    segment = PreviewSegment(
        start=(150.0, 140.0, 0.2),
        end=(160.0, 145.0, 0.2),
        speed=30.0,
        extrusion=0.5,
        flow=1.0,
        width=0.4,
        feature="outer_wall",
        is_extrude=True,
    )

    start, end = harness._preview_segment_pair(segment)

    assert start == (0.0, 0.0, 0.2)
    assert end == (10.0, 5.0, 0.2)
