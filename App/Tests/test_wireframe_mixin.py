import os
import sys


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui.viewer.wireframe import WireframeMixin  # noqa: E402


class _DummyItem:
    def __init__(self) -> None:
        self.opts: dict[str, object] = {}
        self.edges = object()
        self.updated = False
        self.mesh_data_changed = False

    def update(self) -> None:
        self.updated = True

    def meshDataChanged(self) -> None:
        self.mesh_data_changed = True


class _Harness(WireframeMixin):
    def __init__(self) -> None:
        self._solid_mesh_edges = True


def test_apply_wireframe_uses_subtle_edges_for_solid_faces():
    harness = _Harness()
    item = _DummyItem()
    harness._apply_wireframe_to_item(item, enable_edges=False, draw_faces=True)
    assert item.opts["drawFaces"] is True
    assert item.opts["drawEdges"] is True
    assert item.updated is True


def test_apply_wireframe_honors_explicit_wireframe_mode():
    harness = _Harness()
    item = _DummyItem()
    item.edges = None
    harness._apply_wireframe_to_item(item, enable_edges=True, draw_faces=True)
    assert item.opts["drawFaces"] is True
    assert item.opts["drawEdges"] is True
    assert item.mesh_data_changed is True
