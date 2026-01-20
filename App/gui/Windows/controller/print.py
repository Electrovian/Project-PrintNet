from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import TYPE_CHECKING, Any

import numpy as np
import trimesh
from PyQt5 import QtCore, QtGui, QtWidgets

from ...workers import Worker
from slicer.ai_checks import run_ai_checks
from slicer.gcode.preview import parse_gcode_preview_file
from slicer.gcode.stats import estimate_gcode_file
from slicer.gcode.writer import SliceSettings
from slicer.slicer.emit import slice_trimesh, slice_trimesh_auto


class PrintMixin:
    if TYPE_CHECKING:
        viewer: Any
        settings_panel: Any
        printer_manager: Any
        preview_view: Any
        device_view: Any
        _mode_tabs: Any
        _slice_in_progress: bool
        _last_gcode_path: str | None
        _last_slice_signature: str | None
        _last_gcode_stats: dict | None
        _last_preview_key: tuple[str, float, int] | None
        _last_preview_data: Any | None
        _last_preview_text: str | None
        _last_slice_meshes: list[trimesh.Trimesh] | None

        def statusBar(self) -> QtWidgets.QStatusBar: ...
        def _busy_dialog(self, title: str, label: str) -> QtWidgets.QProgressDialog: ...
        def _start_worker(self, worker: Worker) -> None: ...
        def _activate_mode(self, mode: str) -> None: ...
        def __getattr__(self, name: str) -> Any: ...
    # ----------------------------------------------------------- slice/print
    def _invalidate_slice_cache(self, clear_preview: bool = False) -> None:
        self._last_gcode_path = None
        self._last_slice_signature = None
        self._last_gcode_stats = None
        self._last_preview_key = None
        self._last_preview_data = None
        self._last_preview_text = None
        self._last_slice_meshes = None
        if clear_preview:
            if hasattr(self, "preview_view") and hasattr(self.preview_view, "set_gcode_text"):
                self.preview_view.set_gcode_text("")
            if hasattr(self, "viewer") and hasattr(self.viewer, "clear_gcode_preview"):
                self.viewer.clear_gcode_preview()

    def _get_current_stl_path(self):
        if self.current_model_id is None:
            return None
        return self.viewer.get_model_path(self.current_model_id)

    def _get_current_mesh(self):
        if self.current_model_id is None:
            return None
        mesh_data = self.viewer.get_model_mesh_data(self.current_model_id)
        if not mesh_data:
            return None
        vertices, faces = mesh_data
        return trimesh.Trimesh(vertices=vertices, faces=faces, process=False)

    def _get_plate_source_path(self):
        model_ids = self.viewer.get_model_ids()
        if not model_ids:
            return None
        for mid in model_ids:
            path = self.viewer.get_model_path(mid)
            if path:
                return path
        return "plate"

    def _get_plate_mesh(self):
        model_ids = self.viewer.get_model_ids()
        if not model_ids:
            return None
        vertices_list = []
        faces_list = []
        vert_offset = 0
        for mid in model_ids:
            mesh_data = self.viewer.get_model_mesh_data(mid)
            if not mesh_data:
                continue
            vertices, faces = mesh_data
            vertices_list.append(np.asarray(vertices, dtype=float))
            faces_list.append(np.asarray(faces, dtype=int) + vert_offset)
            vert_offset += len(vertices)
        if not vertices_list:
            return None
        combined_vertices = np.vstack(vertices_list)
        combined_faces = np.vstack(faces_list) if faces_list else np.zeros((0, 3), dtype=int)
        return trimesh.Trimesh(vertices=combined_vertices, faces=combined_faces, process=False)

    def _get_plate_meshes(self):
        model_ids = self.viewer.get_model_ids()
        if not model_ids:
            return [], None
        meshes = []
        vertices_list = []
        faces_list = []
        vert_offset = 0
        for mid in model_ids:
            mesh_data = self.viewer.get_model_mesh_data(mid)
            if not mesh_data:
                continue
            vertices, faces = mesh_data
            v = np.asarray(vertices, dtype=float)
            f = np.asarray(faces, dtype=int)
            meshes.append(trimesh.Trimesh(vertices=v, faces=f, process=False))
            vertices_list.append(v)
            faces_list.append(f + vert_offset)
            vert_offset += len(v)
        if not meshes:
            return [], None
        combined_vertices = np.vstack(vertices_list)
        combined_faces = np.vstack(faces_list) if faces_list else np.zeros((0, 3), dtype=int)
        combined = trimesh.Trimesh(vertices=combined_vertices, faces=combined_faces, process=False)
        return meshes, combined

    def _build_slice_signature(self, settings: SliceSettings):
        model_ids = sorted(self.viewer.get_model_ids())
        if not model_ids:
            return None
        models_payload = []
        for mid in model_ids:
            scale_offset = self.viewer.get_model_transform(mid)
            rotation = self.viewer.get_model_rotation(mid)
            if scale_offset is None or rotation is None:
                continue
            scale, offset = scale_offset
            models_payload.append(
                {
                    "model_id": int(mid),
                    "path": self.viewer.get_model_path(mid),
                    "scale": [float(v) for v in np.asarray(scale).reshape(-1)],
                    "offset": [float(v) for v in np.asarray(offset).reshape(-1)],
                    "rotation": [float(v) for v in np.asarray(rotation).reshape(-1)],
                }
            )
        if not models_payload:
            return None
        payload = {"models": models_payload, "settings": asdict(settings)}
        return json.dumps(payload, sort_keys=True, default=str)

    def _slice_model(self,
                     settings: SliceSettings,
                     activate_preview: bool,
                     show_dialog: bool,
                     show_errors: bool = True):
        source_path = self._get_plate_source_path()
        if not source_path:
            if show_dialog:
                QtWidgets.QMessageBox.warning(self.main, "No model", "Load model(s) first.")
            return
        meshes, combined = self._get_plate_meshes()
        if not meshes or combined is None:
            if show_dialog:
                QtWidgets.QMessageBox.warning(self.main, "No model", "Model data unavailable for slicing.")
            return
        self._last_slice_meshes = [m for m in meshes]
        if self._slice_in_progress:
            return

        signature = self._build_slice_signature(settings)
        dlg = None
        if show_dialog:
            dlg = self._busy_dialog("Slicing", "Slicing model...\nPlease wait.")
            dlg.show()
        else:
            self.statusBar().showMessage("Slicing model...")
        self._slice_in_progress = True

        def on_done(gcode_path):
            if dlg is not None:
                dlg.close()
            self._slice_in_progress = False
            self._last_gcode_path = gcode_path
            self._last_slice_signature = signature
            stats = self._analyze_gcode(gcode_path, settings)
            self._update_preview_from_gcode(gcode_path, stats)
            self.statusBar().showMessage(f"Sliced to {gcode_path}")
            if hasattr(self, "_mode_tabs"):
                for btn in self._mode_tabs:
                    if btn.text().strip().lower() == "preview":
                        btn.setChecked(True)
                        break
            if activate_preview:
                self._activate_mode("preview")

        def on_err(msg):
            if dlg is not None:
                dlg.close()
            self._slice_in_progress = False
            self.statusBar().showMessage("Slicing failed")
            if show_errors:
                QtWidgets.QMessageBox.critical(self.main, "Slicing error", msg)

        worker = Worker(slice_trimesh_auto,
                        meshes,
                        output_gcode_path=None,
                        settings=settings,
                        source_path=source_path,
                        combined_mesh=combined)
        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self._start_worker(worker)

    def slice_current_model(self):
        settings = self.settings_panel.to_settings()
        self._slice_model(settings, activate_preview=True, show_dialog=True, show_errors=True)

    def print_current_model(self, printer=None):
        stl_path = self._get_current_stl_path()
        if not stl_path:
            QtWidgets.QMessageBox.warning(self.main, "No model", "Load and select a model first.")
            return
        mesh = self._get_current_mesh()
        if mesh is None:
            QtWidgets.QMessageBox.warning(self.main, "No model", "Model data unavailable for slicing.")
            return

        settings = self.settings_panel.to_settings()
        dlg = self._busy_dialog("Print", "Slicing & sending to printer...\nPlease wait.")
        dlg.show()

        def do_print(m, s, source_path):
            if printer is not None and hasattr(self.printer_manager, "set_active_printer"):
                self.printer_manager.set_active_printer(printer)
            gcode_path = slice_trimesh(m, settings=s, source_path=source_path)
            return self.printer_manager.print_gcode(gcode_path, printer=printer)

        worker = Worker(do_print, mesh, settings, stl_path)

        def on_done(msg):
            dlg.close()
            self.statusBar().showMessage(str(msg))
            QtWidgets.QMessageBox.information(self.main, "Print", str(msg))

        def on_err(msg):
            dlg.close()
            self.statusBar().showMessage("Print failed")
            QtWidgets.QMessageBox.critical(self.main, "Print error", msg)

        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self._start_worker(worker)

    def export_gcode(self):
        stl_path = self._get_current_stl_path()
        if not stl_path:
            QtWidgets.QMessageBox.warning(self.main, "No model", "Load and select a model first.")
            return
        mesh = self._get_current_mesh()
        if mesh is None:
            QtWidgets.QMessageBox.warning(self.main, "No model", "Model data unavailable for slicing.")
            return

        base = os.path.splitext(os.path.basename(stl_path))[0]
        suggested = os.path.join(os.path.dirname(stl_path), f"{base}.gcode")
        out_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.main,
            "Export G-code",
            suggested,
            "G-code files (*.gcode);;All files (*.*)",
        )
        if not out_path:
            return
        if not out_path.lower().endswith(".gcode"):
            out_path = f"{out_path}.gcode"

        settings = self.settings_panel.to_settings()
        dlg = self._busy_dialog("Export", "Exporting G-code...\nPlease wait.")
        dlg.show()

        worker = Worker(slice_trimesh,
                        mesh,
                        output_gcode_path=out_path,
                        settings=settings,
                        source_path=stl_path)

        def on_done(gcode_path):
            dlg.close()
            self.statusBar().showMessage(f"Exported G-code to {gcode_path}")
            QtWidgets.QMessageBox.information(self.main, "Export complete", f"G-code written to:\n{gcode_path}")

        def on_err(msg):
            dlg.close()
            self.statusBar().showMessage("Export failed")
            QtWidgets.QMessageBox.critical(self.main, "Export error", msg)

        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self._start_worker(worker)

    def _on_device_send_requested(self, printer):
        gcode_path = self._last_gcode_path
        if gcode_path and os.path.exists(gcode_path):
            self._send_existing_gcode(printer, gcode_path)
            return
        self.print_current_model(printer=printer)

    def _on_device_save_requested(self):
        self.export_gcode()

    def _send_existing_gcode(self, printer, gcode_path: str):
        dlg = self._busy_dialog("Print", "Sending G-code to printer...\nPlease wait.")
        dlg.show()

        def do_send(p, path):
            if hasattr(self.printer_manager, "set_active_printer"):
                self.printer_manager.set_active_printer(p)
            return self.printer_manager.print_gcode(path, printer=p)

        worker = Worker(do_send, printer, gcode_path)

        def on_done(msg):
            dlg.close()
            self.statusBar().showMessage(str(msg))
            QtWidgets.QMessageBox.information(self.main, "Print", str(msg))

        def on_err(msg):
            dlg.close()
            self.statusBar().showMessage("Print failed")
            QtWidgets.QMessageBox.critical(self.main, "Print error", msg)

        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self._start_worker(worker)

    def _read_gcode_preview(self, path: str, max_lines: int = 600) -> tuple[str, int]:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            return "", 0
        total_lines = len(lines)
        if total_lines > max_lines:
            preview = "".join(lines[:max_lines])
            preview += f"\n; ... trimmed {total_lines - max_lines} lines\n"
        else:
            preview = "".join(lines)
        return preview, total_lines

    def _analyze_gcode(self, gcode_path: str, settings: SliceSettings) -> dict:
        return dict(estimate_gcode_file(gcode_path, settings))

    def _update_preview_from_gcode(self, gcode_path: str, stats: dict):
        if not hasattr(self, "preview_view"):
            return
        settings = self.settings_panel.to_settings() if hasattr(self, "settings_panel") else None
        stats = dict(stats or {})
        if settings is not None and self._last_slice_meshes:
            try:
                ai_report = run_ai_checks(self._last_slice_meshes, settings)
                stats["ai_warnings"] = ai_report.warnings
                stats["ai_suggestions"] = ai_report.suggestions
            except Exception:
                stats.setdefault("ai_warnings", [])
                stats.setdefault("ai_suggestions", [])
        self._last_gcode_stats = dict(stats or {})
        preview_text = None
        preview_key = None
        try:
            stat = os.stat(gcode_path)
            preview_key = (gcode_path, float(stat.st_mtime), int(stat.st_size))
        except OSError:
            preview_key = None

        if preview_key is not None and preview_key == getattr(self, "_last_preview_key", None):
            preview_text = getattr(self, "_last_preview_text", None)
            preview = getattr(self, "_last_preview_data", None)
        else:
            preview = None

        if preview_text is None:
            preview_text, _total_lines = self._read_gcode_preview(gcode_path)
        if preview is None:
            preview = parse_gcode_preview_file(gcode_path, settings=settings)

        self.preview_view.set_gcode_text(preview_text)
        self.preview_view.update_stats(stats)
        if hasattr(self.viewer, "set_print_stats"):
            self.viewer.set_print_stats(stats)

        if hasattr(self.preview_view, "set_preview_settings"):
            self.preview_view.set_preview_settings(settings)
        if hasattr(self.viewer, "set_preview_settings"):
            self.viewer.set_preview_settings(settings)
        if hasattr(self.viewer, "set_gcode_preview"):
            self.viewer.set_gcode_preview(preview)
        self.preview_view.set_preview_data(preview)

        self._last_preview_key = preview_key
        self._last_preview_data = preview
        self._last_preview_text = preview_text

    def _clear_preview(self):
        self._last_gcode_path = None
        self._last_slice_signature = None
        self._slice_in_progress = False
        self._last_gcode_stats = None
        self._last_preview_key = None
        self._last_preview_data = None
        self._last_preview_text = None
        self._last_slice_meshes = None
        if not hasattr(self, "preview_view"):
            return
        self.preview_view.set_gcode_text("")
        self.preview_view.update_stats({})
        self.preview_view.set_steps_count(0)
        self.preview_view.set_layer_count(0)
        self.preview_view.set_preview_data(None)
        if hasattr(self.viewer, "clear_gcode_preview"):
            self.viewer.clear_gcode_preview()
        if hasattr(self.viewer, "clear_print_stats"):
            self.viewer.clear_print_stats()

    def _update_device_status(self):
        if not hasattr(self, "device_view") or not hasattr(self, "viewer"):
            return
        head_pos = None
        if hasattr(self.viewer, "get_preview_nozzle_state"):
            state = self.viewer.get_preview_nozzle_state()
            if state is not None:
                head_pos = tuple(float(v) for v in state[0])

        time_left = None
        pla_remaining = None
        pla_low = None
        stats = self._last_gcode_stats or {}
        total_time = stats.get("time_seconds")
        total_len = stats.get("length_mm")

        progress = None
        if hasattr(self.viewer, "get_preview_progress"):
            progress = self.viewer.get_preview_progress()

        if progress and total_time is not None:
            completed, total = progress
            if total > 0:
                ratio = max(0.0, min(1.0, float(completed) / float(total)))
                time_left = max(0.0, float(total_time)) * (1.0 - ratio)
                if total_len is not None:
                    remaining_mm = max(0.0, float(total_len)) * (1.0 - ratio)
                    pla_remaining = remaining_mm / 1000.0
                    pla_low = remaining_mm <= 2000.0

        self.device_view.update_live_status(
            head_pos=head_pos,
            time_left_s=time_left,
            pla_remaining_m=pla_remaining,
            pla_low=pla_low,
        )

