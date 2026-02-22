# pyright: reportAttributeAccessIssue=false
# pyright: reportArgumentType=false
from __future__ import annotations

import importlib.util
import os
import threading

import numpy as np
import trimesh
from PyQt5 import QtCore, QtGui, QtWidgets

from ...workers import Worker
from ..simplify import SimplifyDialog


class _ProgressFile:
    def __init__(self, path: str, on_progress):
        self._file = open(path, "rb")
        try:
            self._size = os.path.getsize(path)
        except OSError:
            self._size = 0
        self._read = 0
        self._on_progress = on_progress

    def _emit(self):
        if self._size <= 0 or self._on_progress is None:
            return
        value = int(min(95, (self._read / self._size) * 95))
        self._on_progress(value)

    def read(self, size: int = -1):
        if size is None or size < 0:
            chunks = []
            chunk_size = 1024 * 1024
            while True:
                chunk = self._file.read(chunk_size)
                if not chunk:
                    break
                chunks.append(chunk)
                self._read += len(chunk)
                self._emit()
            return b"".join(chunks)
        data = self._file.read(size)
        self._read += len(data)
        self._emit()
        return data

    def seek(self, offset: int, whence: int = 0):
        result = self._file.seek(offset, whence)
        try:
            self._read = self._file.tell()
        except OSError:
            pass
        self._emit()
        return result

    def tell(self):
        return self._file.tell()

    def close(self):
        return self._file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


def _sanitize_mesh_arrays(vertices: np.ndarray, faces: np.ndarray):
    v = np.asarray(vertices, dtype=float)
    f = np.asarray(faces, dtype=int)
    if v.ndim != 2 or v.shape[1] != 3:
        raise ValueError("Invalid vertex array")
    if f.ndim != 2 or f.shape[1] != 3:
        raise ValueError("Invalid face array")
    if v.size == 0 or f.size == 0:
        raise ValueError("Empty mesh")

    finite_mask = np.isfinite(v).all(axis=1)
    if not finite_mask.all():
        remap = np.full(len(v), -1, dtype=int)
        remap[finite_mask] = np.arange(int(finite_mask.sum()))
        f = remap[f]
        v = v[finite_mask]

    max_index = len(v)
    valid = (f >= 0).all(axis=1) & (f < max_index).all(axis=1)
    if valid.any():
        f = f[valid]
    else:
        raise ValueError("All faces invalid")

    non_degenerate = (f[:, 0] != f[:, 1]) & (f[:, 0] != f[:, 2]) & (f[:, 1] != f[:, 2])
    f = f[non_degenerate]
    if f.size == 0:
        raise ValueError("Degenerate faces")

    p0 = v[f[:, 0]]
    p1 = v[f[:, 1]]
    p2 = v[f[:, 2]]
    area = np.linalg.norm(np.cross(p1 - p0, p2 - p0), axis=1)
    f = f[area > 1e-12]
    if f.size == 0:
        raise ValueError("Zero-area faces")

    return v, f


def _format_extent_triplet(extents: np.ndarray) -> str:
    e = np.asarray(extents, dtype=float).reshape(-1)
    if e.size != 3:
        return "unknown"
    return f"{e[0]:.2f} x {e[1]:.2f} x {e[2]:.2f} mm"


def _infer_import_unit_scale(mesh: trimesh.Trimesh):
    # Mirror historical slicer volume-based checks and add a conservative fallback for
    # ultra-detailed tiny imports that are commonly authored in inches.
    volume = 0.0
    try:
        volume = abs(float(mesh.volume))
    except Exception:
        volume = 0.0

    extents = np.asarray(getattr(mesh, "extents", np.zeros(3, dtype=float)), dtype=float).reshape(-1)
    if extents.size != 3:
        extents = np.zeros(3, dtype=float)
    bbox_volume = float(extents[0] * extents[1] * extents[2]) if np.isfinite(extents).all() else 0.0
    max_dim = float(np.max(extents)) if extents.size == 3 else 0.0
    face_count = 0
    try:
        face_count = int(len(mesh.faces))
    except Exception:
        face_count = 0

    if 0.0 < volume < 0.008:
        return 1000.0, "meters", extents
    if 0.0 < volume < 8.0:
        return 25.4, "inches", extents
    if face_count >= 100000 and 0.0 < max_dim <= 12.0 and 0.0 < bbox_volume < 800.0:
        return 25.4, "inches", extents
    return 1.0, "", extents


class LoadMixin:
    def _prefer_manual_stl_entry(self) -> bool:
        if os.name != "nt":
            return False
        force_manual = str(os.environ.get("EON_FORCE_MANUAL_STL_ENTRY", "0")).strip().lower()
        if force_manual in ("1", "true", "yes", "on"):
            return True
        prefer_manual = str(os.environ.get("EON_PREFER_MANUAL_STL_ENTRY", "0")).strip().lower()
        return prefer_manual in ("1", "true", "yes", "on")

    def _prompt_stl_paths_fallback(self):
        initial_text = ""
        try:
            clipboard = QtWidgets.QApplication.clipboard()
            clip_text = str(clipboard.text() if clipboard is not None else "").strip()
            if clip_text.lower().endswith(".stl"):
                initial_text = clip_text
        except Exception:
            initial_text = ""
        text, ok = QtWidgets.QInputDialog.getMultiLineText(
            self.main,
            "Open STL files",
            "Paste full STL path(s), one per line.\n"
            "Example: C:\\Users\\Elect\\Downloads\\part.stl",
            initial_text,
        )
        if not ok:
            return []
        paths = []
        invalid = []
        for raw in str(text or "").splitlines():
            candidate = str(raw).strip().strip('"')
            if not candidate:
                continue
            if not candidate.lower().endswith(".stl"):
                invalid.append(candidate)
                continue
            if not os.path.isfile(candidate):
                invalid.append(candidate)
                continue
            paths.append(candidate)
        if invalid:
            preview = "\n".join(invalid[:5])
            extra = "\n..." if len(invalid) > 5 else ""
            QtWidgets.QMessageBox.warning(
                self.main,
                "Invalid STL path(s)",
                f"These paths were ignored:\n{preview}{extra}",
            )
        return paths

    def _simplify_prompt_triangle_threshold(self) -> int:
        raw = str(os.environ.get("EON_SIMPLIFY_PROMPT_TRIANGLES", "100000")).strip()
        try:
            value = int(raw)
        except (TypeError, ValueError):
            value = 100000
        return max(1000, value)

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent):
        event = a0
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(".stl"):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, a0: QtGui.QDropEvent):
        event = a0
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.lower().endswith(".stl"):
                self._add_model_from_path_async(path)

    # -------------------------------------------------------------- open
    def open_stl_dialog(self):
        status_bar = getattr(self, "statusBar", None)
        if callable(status_bar):
            status_bar().showMessage("Opening model file dialog...")
        paths = []
        if self._prefer_manual_stl_entry():
            paths = self._prompt_stl_paths_fallback()
        else:
            try:
                paths, _ = self._safe_get_open_file_names("Open STL files", "", "STL files (*.stl)")
            except Exception as exc:
                QtWidgets.QMessageBox.warning(
                    self.main,
                    "Open STL files",
                    "File picker failed. Use manual path entry fallback.\n\n"
                    f"Reason: {exc}",
                )
                paths = self._prompt_stl_paths_fallback()
        if not paths and callable(status_bar):
            status_bar().showMessage("No STL selected")
            return
        for path in paths:
            self._add_model_from_path_async(path)

    # ------------------------------------------------------------- async load
    def _add_model_from_path_async(self, path: str):
        filename = os.path.basename(path)
        dlg = self._loading_dialog(filename)
        dlg.show()
        cancelled = {"value": False}
        closing = {"value": False}
        progress_active = {"value": True}
        progress_state = {"value": 0}
        progress_lock = threading.Lock()

        progress_timer = QtCore.QTimer(self.main)
        progress_timer.setInterval(50)

        def close_dialog():
            progress_active["value"] = False
            if progress_timer.isActive():
                progress_timer.stop()
            closing["value"] = True
            # QProgressDialog can emit canceled on close; block signals here.
            dlg.blockSignals(True)
            dlg.close()
            dlg.blockSignals(False)
            closing["value"] = False

        def update_progress(value: int):
            if cancelled["value"]:
                return
            dlg.setValue(max(0, min(100, int(value))))

        def poll_progress():
            if not progress_active["value"]:
                return
            with progress_lock:
                value = progress_state["value"]
            update_progress(value)

        progress_timer.timeout.connect(poll_progress)
        progress_timer.start()

        def on_cancel():
            if closing["value"]:
                return
            cancelled["value"] = True
            self.statusBar().showMessage("Load canceled")
            close_dialog()

        def load_mesh(p, report_progress):
            def emit_progress(value: int):
                if cancelled["value"]:
                    return
                if report_progress is None:
                    return
                report_progress(int(value))

            try:
                with _ProgressFile(p, emit_progress) as handle:
                    mesh = trimesh.load(handle, file_type="stl", force="mesh")
            except Exception:
                mesh = trimesh.load(p, force="mesh")
            if isinstance(mesh, trimesh.Scene):
                mesh = trimesh.util.concatenate(mesh.dump())
            elif not isinstance(mesh, trimesh.Trimesh):
                # fallback: concatenate any geometry collection into a Trimesh
                mesh = trimesh.util.concatenate(mesh)  # type: ignore[arg-type]
            try:
                mesh.process(validate=True)
            except Exception:
                pass
            vertices = np.array(mesh.vertices, dtype=float)
            faces = np.array(mesh.faces, dtype=int)
            vertices, faces = _sanitize_mesh_arrays(vertices, faces)
            unit_scale, unit_source, extents = _infer_import_unit_scale(mesh)
            return {
                "path": p,
                "name": os.path.basename(p),
                "v": vertices,
                "f": faces,
                "unit_scale_hint": float(unit_scale),
                "unit_source_hint": unit_source,
                "raw_extents": np.asarray(extents, dtype=float),
            }

        def report_progress(value: int):
            if cancelled["value"] or not progress_active["value"]:
                return
            with progress_lock:
                progress_state["value"] = int(value)

        worker = Worker(load_mesh, path, report_progress)

        def on_done(payload):
            dlg.setValue(100)
            close_dialog()
            if cancelled["value"]:
                return
            try:
                unit_scale = float(payload.get("unit_scale_hint", 1.0))
            except (TypeError, ValueError):
                unit_scale = 1.0
            unit_source = str(payload.get("unit_source_hint", "") or "").strip().lower()
            if unit_scale > 1.0 and unit_source in ("meters", "inches"):
                raw_extents = np.asarray(payload.get("raw_extents", np.zeros(3, dtype=float)), dtype=float)
                converted_extents = raw_extents * unit_scale
                answer = QtWidgets.QMessageBox.question(
                    self.main,
                    "Convert import units",
                    f"{payload['name']} appears to be authored in {unit_source}.\n\n"
                    f"Current size: {_format_extent_triplet(raw_extents)}\n"
                    f"Converted size: {_format_extent_triplet(converted_extents)}\n\n"
                    "Convert to millimeters?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    QtWidgets.QMessageBox.Yes,
                )
                if answer == QtWidgets.QMessageBox.Yes:
                    payload["v"] = np.asarray(payload["v"], dtype=float) * unit_scale
            try:
                model_id = self.viewer.add_model_from_data(
                    payload["name"],
                    payload["path"],
                    payload["v"],
                    payload["f"],
                )
            except Exception as exc:
                on_err(str(exc))
                return
            self.model_panel.add_model(payload["name"], model_id)

            self.current_model_id = model_id
            self.viewer.set_selected_model(model_id)

            self.statusBar().showMessage(f"Loaded {payload['name']}")
            self._update_bed_warnings()
            self._push_undo_state()
            self._refresh_files_view()
            if hasattr(self, "_invalidate_slice_cache"):
                self._invalidate_slice_cache(clear_preview=True)
            try:
                self._open_simplify_dialog(model_id)
            except Exception:
                # Never block load completion on simplify prompt failures.
                pass

        def on_err(msg):
            close_dialog()
            if cancelled["value"]:
                return
            QtWidgets.QMessageBox.critical(self.main, "Load error", msg)

        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        dlg.canceled.connect(on_cancel)
        self._start_worker(worker)

    def _open_simplify_dialog(self, model_id: int):
        model = self.viewer.models.get(model_id) if hasattr(self.viewer, "models") else None
        if not model:
            return
        name = (model.get("name") or "").strip() or f"Model {model_id}"
        faces = model.get("faces")
        triangles = int(len(faces)) if faces is not None else 0
        if triangles <= 0:
            return
        threshold = self._simplify_prompt_triangle_threshold()
        if triangles < threshold:
            return
        dlg = SimplifyDialog(name, triangles, parent=self.main)
        dlg.setModal(False)
        dlg.setWindowModality(QtCore.Qt.NonModal)
        prev_wireframe = bool(model.get("wireframe"))

        def on_closed(_result):
            self.viewer.set_model_wireframe(model_id, prev_wireframe)
            if getattr(self, "_simplify_dialog", None) is dlg:
                self._simplify_dialog = None

        dlg.wireframeChanged.connect(lambda enabled: self.viewer.set_model_wireframe(model_id, enabled))
        dlg.applyRequested.connect(lambda target: self._simplify_model(model_id, target))
        dlg.finished.connect(on_closed)
        self.viewer.set_model_wireframe(model_id, prev_wireframe)
        self._simplify_dialog = dlg
        dlg.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        dlg.show()
        dlg.raise_()
        dlg.activateWindow()

    def _simplify_model(self, model_id: int, target_faces: int):
        model = self.viewer.models.get(model_id) if hasattr(self.viewer, "models") else None
        if not model:
            return
        faces = model.get("faces")
        vertices = model.get("base_vertices")
        if faces is None or vertices is None:
            return
        current_faces = int(len(faces))
        target_faces = max(4, min(int(target_faces), current_faces))
        if target_faces >= current_faces:
            return

        dlg = self._busy_dialog("Simplify", "Simplifying mesh...\nPlease wait.")
        dlg.setModal(False)
        dlg.setWindowModality(QtCore.Qt.NonModal)
        dlg.show()

        def decimate(v, f, target):
            mesh = trimesh.Trimesh(vertices=np.asarray(v, dtype=float),
                                   faces=np.asarray(f, dtype=int),
                                   process=False)
            simplify_attr = None
            if hasattr(mesh, "simplify_quadric_decimation"):
                simplify_attr = "simplify_quadric_decimation"
            elif hasattr(mesh, "simplify_quadratic_decimation"):
                simplify_attr = "simplify_quadratic_decimation"
            if simplify_attr is None:
                raise RuntimeError("Simplification not supported by this trimesh build.")
            if importlib.util.find_spec("fast_simplification") is None:
                raise RuntimeError(
                    "Simplification requires fast_simplification. "
                    "Install it with: pip install fast_simplification"
                )
            simplify_fn = getattr(mesh, simplify_attr)
            try:
                sig = getattr(simplify_fn, "__signature__", None)
            except Exception:
                sig = None
            kwargs = {}
            if sig is None:
                try:
                    import inspect
                    sig = inspect.signature(simplify_fn)
                except Exception:
                    sig = None
            if sig is not None and "face_count" in sig.parameters:
                kwargs["face_count"] = int(target)
            else:
                current = max(1, int(len(mesh.faces)))
                kwargs["percent"] = max(0.0, min(1.0, float(target) / float(current)))
            simplified = simplify_fn(**kwargs)
            if simplified is None:
                raise RuntimeError("Simplification failed.")
            if simplified.is_empty:
                raise RuntimeError("Simplification produced an empty mesh.")
            return {
                "v": np.asarray(simplified.vertices, dtype=float),
                "f": np.asarray(simplified.faces, dtype=int),
            }

        worker = Worker(decimate, vertices, faces, target_faces)

        def on_done(payload):
            dlg.close()
            replaced = self.viewer.replace_model_mesh(model_id, payload["v"], payload["f"])
            if replaced:
                self.statusBar().showMessage(f"Simplified to {len(payload['f'])} triangles")
                self._update_bed_warnings()
                self._push_undo_state()
                if hasattr(self, "_invalidate_slice_cache"):
                    self._invalidate_slice_cache(clear_preview=True)

        def on_err(msg):
            dlg.close()
            QtWidgets.QMessageBox.critical(self.main, "Simplify error", msg)

        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self._start_worker(worker)

    
