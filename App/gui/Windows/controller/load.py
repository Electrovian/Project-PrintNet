# pyright: reportAttributeAccessIssue=false
# pyright: reportArgumentType=false
from __future__ import annotations

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


class LoadMixin:
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
        paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self.main, "Open STL files", "", "STL files (*.stl)"
        )
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
            vertices = np.array(mesh.vertices, dtype=float)
            faces = np.array(mesh.faces, dtype=int)
            return {"path": p, "name": os.path.basename(p), "v": vertices, "f": faces}

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
            model_id = self.viewer.add_model_from_data(payload["name"], payload["path"], payload["v"], payload["f"])
            self.model_panel.add_model(payload["name"], model_id)

            self.current_model_id = model_id
            self.viewer.set_selected_model(model_id)

            self.statusBar().showMessage(f"Loaded {payload['name']}")
            self._update_bed_warnings()
            self._push_undo_state()
            self._refresh_files_view()

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
        if triangles < 1_000_000:
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
        self.viewer.set_model_wireframe(model_id, dlg.wireframe_enabled())
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
            simplified = mesh.simplify_quadratic_decimation(int(target))
            if simplified is None:
                raise RuntimeError("Simplification failed.")
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

        def on_err(msg):
            dlg.close()
            QtWidgets.QMessageBox.critical(self.main, "Simplify error", msg)

        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self._start_worker(worker)

    
