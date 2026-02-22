from __future__ import annotations

from typing import Any, TYPE_CHECKING


class WireframeMixin:
    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any: ...

    def get_wireframe_enabled(self) -> bool:
        return bool(getattr(self, "_wireframe_default", False))

    def set_wireframe_enabled(self, enabled: bool):
        self._wireframe_default = bool(enabled)
        models = getattr(self, "models", {})
        for model in models.values():
            model["wireframe"] = self._wireframe_default
        if hasattr(self, "set_models_visible"):
            self.set_models_visible(bool(getattr(self, "_models_visible", True)))
            return
        for model_id in list(models.keys()):
            self.set_model_wireframe(model_id, self._wireframe_default)

    def set_model_wireframe(self, model_id: int, enabled: bool):
        m = getattr(self, "models", {}).get(model_id)
        if m is None:
            return
        item = m.get("item")
        if item is None:
            return
        enable_edges = bool(enabled)
        m["wireframe"] = enable_edges
        if enable_edges and m.get("meshdata_wireframe") is None and hasattr(self, "_ensure_model_wireframe_meshdata"):
            self._ensure_model_wireframe_meshdata(model_id)
        if enable_edges and m.get("meshdata_wireframe") is not None:
            item.setMeshData(meshdata=m["meshdata_wireframe"])
            if hasattr(self, "_apply_model_color"):
                self._apply_model_color(m)
        elif m.get("meshdata_full") is not None:
            item.setMeshData(meshdata=m["meshdata_full"])
            if hasattr(self, "_apply_model_color"):
                self._apply_model_color(m)
        models_visible = bool(getattr(self, "_models_visible", True))
        if models_visible:
            item.setVisible(True)
            self._apply_wireframe_to_item(item, enable_edges, draw_faces=True)
        else:
            if enable_edges:
                item.setVisible(True)
                self._apply_wireframe_to_item(item, True, draw_faces=False)
            else:
                item.setVisible(False)

    def _apply_wireframe_to_item(self, item, enable_edges: bool, draw_faces: bool):
        item.opts["drawEdges"] = bool(enable_edges)
        item.opts["drawFaces"] = bool(draw_faces)
        if enable_edges and getattr(item, "edges", None) is None:
            item.meshDataChanged()
        item.update()
