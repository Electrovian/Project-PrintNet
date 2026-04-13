from __future__ import annotations

import json
import os
from dataclasses import asdict, is_dataclass
from typing import TYPE_CHECKING, Any

import numpy as np
import trimesh
from PyQt5 import QtCore, QtGui, QtWidgets


def _settings_to_dict(settings: Any) -> dict[str, Any]:
    if settings is None:
        return {}
    if is_dataclass(settings):
        return asdict(settings)
    if isinstance(settings, dict):
        return dict(settings)
    try:
        return dict(settings)
    except Exception:
        pass
    try:
        return {
            str(key): value
            for key, value in vars(settings).items()
            if not str(key).startswith("_")
        }
    except Exception:
        return {}


class ProjectMixin:
    if TYPE_CHECKING:
        viewer: Any
        model_panel: Any
        settings_panel: Any
        _current_project_path: str | None
        _undo_in_progress: bool
        _undo_stack: list[Any]
        _redo_stack: list[Any]

        def statusBar(self) -> QtWidgets.QStatusBar: ...
        def _clear_all_models(self) -> None: ...
        def _get_current_stl_path(self) -> str | None: ...
        def _select_model_in_panel(self, model_ids: Any) -> None: ...
        def _sync_popups(self) -> None: ...
        def _push_undo_state(self) -> None: ...
        def _refresh_files_view(self) -> None: ...
        def _scale_to_vec(self, scale: Any) -> Any: ...
        def _vec3(self, value: Any, default: Any = (0, 0, 0)) -> Any: ...
        def _selected_model_index(self) -> int | None: ...
        def _safe_get_open_file_name(self, caption: str, directory: str, file_filter: str) -> tuple[str, str]: ...
        def _safe_get_save_file_name(self, caption: str, directory: str, file_filter: str) -> tuple[str, str]: ...
        def __getattr__(self, name: str) -> Any: ...
    def _new_project(self):
        self._current_project_path = None
        self._clear_all_models()

    def _open_feedback(self):
        url = "https://github.com/Electrovian/Project-PrintNet/issues"
        reply = QtWidgets.QMessageBox.question(
            self.main,
            "User Feedback",
            "Open the feedback page in your browser?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def _save_project(self):
        if self._current_project_path:
            self._write_project_file(self._current_project_path)
            return
        self._save_project_as()

    def _save_project_as(self):
        suggested = self._current_project_path or ""
        if not suggested:
            stl_path = self._get_current_stl_path()
            if stl_path:
                base = os.path.splitext(os.path.basename(stl_path))[0]
                suggested = os.path.join(os.path.dirname(stl_path), f"{base}.osproj")
        out_path, _ = self._safe_get_save_file_name(
            "Save Project",
            suggested,
            "EON-OpenSlicer Project (*.osproj);;All files (*.*)",
        )
        if not out_path:
            return
        if not out_path.lower().endswith(".osproj"):
            out_path = f"{out_path}.osproj"
        self._write_project_file(out_path)

    def _open_project(self):
        start_dir = ""
        if self._current_project_path:
            start_dir = os.path.dirname(self._current_project_path)
        path, _ = self._safe_get_open_file_name(
            "Open Project",
            start_dir,
            "EON-OpenSlicer Project (*.osproj);;All files (*.*)",
        )
        if not path:
            return
        self._load_project_file(path)

    def _write_project_file(self, path: str):
        payload = self._serialize_project()
        try:
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, ensure_ascii=True)
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self.main, "Save error", str(exc))
            return
        self._current_project_path = path
        self.statusBar().showMessage(f"Saved project to {path}")

    def _load_project_file(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self.main, "Open error", str(exc))
            return
        self._current_project_path = path
        base_dir = os.path.dirname(path)
        self._load_project_data(data, base_dir)
        self.statusBar().showMessage(f"Loaded project from {path}")

    def _load_project_data(self, data: dict, base_dir: str):
        if not isinstance(data, dict):
            QtWidgets.QMessageBox.warning(self.main, "Open error", "Invalid project file.")
            return

        if "settings" in data:
            self.settings_panel.apply_settings(data.get("settings") or {})
        version = int(data.get("version", 1) or 1)
        missing = []

        self._undo_in_progress = True
        try:
            if version >= 2 and isinstance(data.get("plates"), list):
                payload = {
                    "version": 2,
                    "plates": data.get("plates", []),
                    "objects": data.get("objects", []),
                    "parts": data.get("parts", []),
                    "instances": data.get("instances", []),
                    "selected_plate_id": data.get("selected_plate_id"),
                    "selected_entity_ids": data.get("selected_entity_ids", []),
                    "tool_state": data.get("tool_state", {}),
                }
                self.viewer.restore_scene(payload)
                if hasattr(self.model_panel, "refresh_from_viewer"):
                    self.model_panel.refresh_from_viewer(self.viewer)
            else:
                models = data.get("models", [])
                if not isinstance(models, list):
                    QtWidgets.QMessageBox.warning(self.main, "Open error", "Project models list is invalid.")
                    return
                self.viewer.clear_all_models()
                if hasattr(self.model_panel, "list_widget"):
                    self.model_panel.list_widget.clear()
                for entry in models:
                    if not isinstance(entry, dict):
                        continue
                    name = entry.get("name", "")
                    model_path = entry.get("path", "")
                    vertices = entry.get("vertices")
                    faces = entry.get("faces")

                    resolved_path = model_path
                    if model_path and base_dir and not os.path.isabs(model_path):
                        resolved_path = os.path.join(base_dir, model_path)

                    use_path = bool(resolved_path and os.path.exists(resolved_path))
                    if use_path:
                        try:
                            mesh = trimesh.load(resolved_path, force="mesh")
                            if isinstance(mesh, trimesh.Scene):
                                mesh = trimesh.util.concatenate(mesh.dump())
                            elif not isinstance(mesh, trimesh.Trimesh):
                                mesh = trimesh.util.concatenate(mesh)  # type: ignore[arg-type]
                            vertices = np.array(mesh.vertices, dtype=float)
                            faces = np.array(mesh.faces, dtype=int)
                        except Exception:
                            use_path = False

                    if not use_path and (vertices is None or faces is None):
                        missing.append(model_path or name or "Unnamed model")
                        continue

                    model_id = self.viewer.add_model_from_data(
                        name,
                        resolved_path if use_path else model_path,
                        vertices,
                        faces,
                    )
                    self.viewer.set_model_transform(
                        model_id,
                        scale=entry.get("scale"),
                        rotation_xyz=entry.get("rotation"),
                        offset_xyz=entry.get("offset"),
                    )
                if hasattr(self.model_panel, "refresh_from_viewer"):
                    self.model_panel.refresh_from_viewer(self.viewer)
        finally:
            self._undo_in_progress = False

        selected = []
        if version >= 2:
            selected = list(data.get("selected_entity_ids", []) or [])
        else:
            model_ids = self.viewer.get_all_model_ids() if hasattr(self.viewer, "get_all_model_ids") else self.viewer.get_model_ids()
            selected_index = data.get("selected_index")
            if model_ids:
                if isinstance(selected_index, int) and 0 <= selected_index < len(model_ids):
                    selected = [model_ids[selected_index]]
                else:
                    selected = [model_ids[-1]]
        self.current_model_id = selected[0] if selected else None
        self.viewer.set_selected_models(selected, emit_signal=False)
        if selected:
            self._select_model_in_panel(selected)
        elif hasattr(self.model_panel, "clear_selection"):
            self.model_panel.clear_selection()
        else:
            self.model_panel.list_widget.clearSelection()
        self._sync_popups()

        self._undo_stack.clear()
        self._redo_stack.clear()
        self._push_undo_state()
        self._refresh_files_view()

        if missing:
            QtWidgets.QMessageBox.warning(
                self.main,
                "Open warning",
                "Some models could not be loaded:\n" + "\n".join(missing),
            )

    def _serialize_project(self) -> dict:
        settings = self.settings_panel.to_settings()
        payload = self.viewer.serialize_scene() if hasattr(self.viewer, "serialize_scene") else {"version": 1, "models": []}
        payload["settings"] = _settings_to_dict(settings)
        return payload

