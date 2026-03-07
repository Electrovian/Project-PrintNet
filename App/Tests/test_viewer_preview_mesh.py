import os
import sys

import numpy as np


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui.viewer.preview import PreviewMixin  # noqa: E402


class _PreviewHarness(PreviewMixin):
    def __init__(self) -> None:
        self._preview_base_width = 0.4
        self._preview_layer_height = 0.2
        self._preview_empty_mesh = None


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
