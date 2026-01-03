import json
import json
import math
import os
from dataclasses import asdict
import numpy as np
import trimesh

from PyQt5 import QtWidgets, QtGui, QtCore

from ..workers import Worker
from ..theme import export_theme, get_theme_name, register_theme, set_theme
from config.defaults import DEFAULTS
from slicer.slicer import slice_trimesh
from slicer.gcode import SliceSettings, estimate_gcode_file, parse_gcode_preview_file


class MainController(QtCore.QObject):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main = main_window
        self.current_model_id = None
        self._current_project_path = None
        self._last_gcode_path = None
        self._last_slice_signature = None
        self._slice_in_progress = False
        self._labels_visible = True
        self._model_clipboard = []
        self._undo_stack = []
        self._redo_stack = []
        self._undo_stack_limit = 50
        self._undo_in_progress = False
        self._bed_warning_active = False
        self._undo_timer = QtCore.QTimer(self)
        self._undo_timer.setSingleShot(True)
        self._undo_timer.timeout.connect(self._finalize_undo_snapshot)
        self._pending_undo_snapshot = False

    def __getattr__(self, name):
        main = self.__dict__.get("main")
        if main is not None:
            if name in main.__dict__:
                return main.__dict__[name]
            if getattr(type(main), name, None) is not None:
                return object.__getattribute__(main, name)
        raise AttributeError(f"{type(self).__name__} has no attribute {name!r}")

    def initialize(self):
        self._apply_theme()
        self._connect_signals()
        self.viewer.set_snap(
            DEFAULTS["viewer"]["snap_enabled"],
            DEFAULTS["viewer"]["snap_step"],
        )

        self.current_model_id = None
        self._current_project_path = None
        self._last_gcode_path = None
        self._labels_visible = True
        self._model_clipboard = []
        self._undo_stack = []
        self._redo_stack = []
        self._undo_stack_limit = 50
        self._undo_in_progress = False
        self._bed_warning_active = False
        self._undo_timer = QtCore.QTimer(self)
        self._undo_timer.setSingleShot(True)
        self._undo_timer.timeout.connect(self._finalize_undo_snapshot)
        self._pending_undo_snapshot = False
        self._push_undo_state()
        self.viewer.set_labels_visible(self._labels_visible)
        if hasattr(self, "_labels_action"):
            self._labels_action.setChecked(self._labels_visible)

        self._activate_mode("prepare")
        self.statusBar().showMessage(DEFAULTS["app"]["status_ready"])

    def _connect_signals(self):
        self.model_panel.model_selected.connect(self._on_model_selected)
        self.model_panel.request_remove.connect(self._on_model_remove)
        self.model_panel.duplicate_requested.connect(self._on_duplicate_requested)
        self.job_queue_panel.add_btn.clicked.connect(self._add_current_model_to_queue)
        self.viewer.modelPicked.connect(self._on_viewer_model_picked)
        self.viewer.modelMoved.connect(self._on_viewer_model_moved)
        self.viewer.modelRotated.connect(self._on_viewer_model_rotated)

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

    # -------------------------------------------------- Model selection/removal
    def _on_model_selected(self, model_id: int):
        self.current_model_id = model_id
        self.viewer.set_selected_model(model_id)

        name = self.viewer.get_model_name(model_id) or "Model"
        self.statusBar().showMessage(f"Selected {name}")

        self.viewer.set_gizmo_mode("move")
        self._sync_popups()

    def _on_model_remove(self, model_id: int):
        self._remove_models([model_id])

    def _on_duplicate_requested(self, count: int, rows: int, cols: int):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self.main, "Duplicate", "Select a model first.")
            return
        payload = self._capture_model_payload(self.current_model_id)
        if payload is None:
            return
        bounds = self.viewer.get_model_bounds(self.current_model_id)
        if bounds is None:
            QtWidgets.QMessageBox.warning(self.main, "Duplicate", "Model bounds unavailable.")
            return
        mn, mx = bounds
        width = float(mx[0] - mn[0])
        depth = float(mx[1] - mn[1])
        spacing = float(DEFAULTS["popups"]["arrange"]["auto_spacing"])
        dx = width + spacing
        dy = depth + spacing
        if dx <= 0.0 or dy <= 0.0:
            return

        count = max(1, int(count))
        rows = max(1, int(rows))
        cols = max(1, int(cols))
        if rows * cols < count:
            rows = int(math.ceil(count / cols))

        base_offset = np.array(payload["offset"], dtype=float)
        name = payload.get("name", "Model")
        new_ids = []
        for idx in range(count):
            row = idx // cols
            col = idx % cols
            offset = base_offset + np.array([(col + 1) * dx, row * dy, 0.0], dtype=float)
            model_id = self.viewer.add_model_from_data(
                f"{name} Copy {idx + 1}",
                payload["path"],
                payload["base_vertices"],
                payload["faces"],
            )
            self.viewer.set_model_transform(
                model_id,
                scale=payload["scale"],
                rotation_xyz=payload["rotation"],
                offset_xyz=offset,
            )
            self.model_panel.add_model(f"{name} Copy {idx + 1}", model_id)
            new_ids.append(model_id)

        if new_ids:
            self.current_model_id = new_ids[-1]
            self.viewer.set_selected_model(self.current_model_id)
            self._select_model_in_panel(self.current_model_id)
            self._sync_popups()
            self._update_bed_warnings()
            self._push_undo_state()

    def _clear_all_models(self):
        model_ids = self.viewer.get_model_ids()
        if not model_ids:
            self.current_model_id = None
            self.viewer.set_selected_model(None)
            self.model_panel.list_widget.clearSelection()
            self._clear_preview()
            self._sync_popups()
            return
        self._remove_models(model_ids)
        self._clear_preview()
        self.statusBar().showMessage("Cleared all models")

    # ------------------------------------------------------------ transforms (toolbar -> viewer)
    def _enable_move_gizmo(self):
        self.viewer.set_gizmo_mode("move")

    def _enable_rotate_gizmo(self):
        self.viewer.set_gizmo_mode("rotate")

    def _prompt_scale_model(self):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self.main, "No model selected", "Select a model first.")
            return
        m = self.viewer.models.get(self.current_model_id)
        if m is None:
            return
        scale_val = m.get("scale", 1.0)
        if isinstance(scale_val, (list, tuple, np.ndarray)):
            current_pct = float(scale_val[0]) * 100.0
        else:
            current_pct = float(scale_val) * 100.0
        val, ok = QtWidgets.QInputDialog.getDouble(
            self.main,
            "Scale Model",
            "Scale (%)",
            value=current_pct,
            min=1.0,
            max=500.0,
            decimals=2,
        )
        if not ok:
            return
        new_scale = float(val) / 100.0
        self.viewer.set_model_transform(
            self.current_model_id,
            scale=(new_scale, new_scale, new_scale),
            offset_xyz=m["offset"],
        )
        self.statusBar().showMessage(f"Scale applied: {new_scale:.3f}")
        self._schedule_undo_snapshot()

    def _lay_on_face(self):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self.main, "No model", "Select a model first.")
            return
        ok = self.viewer.lay_on_face(self.current_model_id)
        if not ok:
            QtWidgets.QMessageBox.warning(self.main, "Lay on Face", "Unable to orient model.")
            return
        self._sync_popups()
        self._update_bed_warnings()
        self._schedule_undo_snapshot()

    # ------------------------------------------------------------ transforms (viewer -> panel)
    def _on_viewer_model_picked(self, model_id: int):
        # Make viewer click behave like selecting in the Models panel
        self.current_model_id = model_id
        self.viewer.set_selected_model(model_id)

        # Select in model panel list (without emitting loops)
        lw = self.model_panel.list_widget
        block = lw.blockSignals(True)
        try:
            for row in range(lw.count()):
                item = lw.item(row)
                if item is None:
                    continue
                if item.data(QtCore.Qt.UserRole) == model_id:
                    lw.setCurrentItem(item)
                    break
        finally:
            lw.blockSignals(block)

        self.viewer.set_gizmo_mode("move")

    def _on_viewer_model_moved(self, model_id: int, x: float, y: float):
        if self.current_model_id != model_id:
            self.current_model_id = model_id
            self.viewer.set_selected_model(model_id)

        self.statusBar().showMessage(f"Moved model {model_id}: x={x:.2f} y={y:.2f}")
        self._sync_popups()
        self._update_bed_warnings()
        self._schedule_undo_snapshot()

    def _on_viewer_model_rotated(self, model_id: int, x: float, y: float, z: float):
        if self.current_model_id != model_id:
            self.current_model_id = model_id
            self.viewer.set_selected_model(model_id)
        self.statusBar().showMessage(f"Rotated model {model_id}: x={x:.2f} y={y:.2f} z={z:.2f}")
        self._sync_popups()
        self._update_bed_warnings()
        self._schedule_undo_snapshot()

    def _update_bed_warnings(self):
        if not hasattr(self.viewer, "get_out_of_bounds_models"):
            return
        ids = self.viewer.get_out_of_bounds_models()
        if not ids:
            if self._bed_warning_active:
                self.statusBar().showMessage(DEFAULTS["app"]["status_ready"])
                self._bed_warning_active = False
            return
        names = []
        for mid in ids:
            name = self.viewer.get_model_name(mid) or f"Model {mid}"
            names.append(name)
        bed = DEFAULTS.get("printer", {}).get("bed_size", (0, 0))
        max_height = DEFAULTS.get("printer", {}).get("max_height", 0)
        bed_str = f"{bed[0]}x{bed[1]} mm"
        msg = "Warning: " + ", ".join(names) + f" exceed bed {bed_str} or height {max_height} mm."
        self.statusBar().showMessage(msg)
        self._bed_warning_active = True

    # ------------------------------------------------------------- async load
    def _add_model_from_path_async(self, path: str):
        dlg = self._busy_dialog("Loading", f"Loading STL:\n{os.path.basename(path)}")
        dlg.show()

        def load_mesh(p):
            mesh = trimesh.load(p, force="mesh")
            if isinstance(mesh, trimesh.Scene):
                mesh = trimesh.util.concatenate(mesh.dump())
            elif not isinstance(mesh, trimesh.Trimesh):
                # fallback: concatenate any geometry collection into a Trimesh
                mesh = trimesh.util.concatenate(mesh)  # type: ignore[arg-type]
            vertices = np.array(mesh.vertices, dtype=float)
            faces = np.array(mesh.faces, dtype=int)
            return {"path": p, "name": os.path.basename(p), "v": vertices, "f": faces}

        worker = Worker(load_mesh, path)

        def on_done(payload):
            dlg.close()
            model_id = self.viewer.add_model_from_data(payload["name"], payload["path"], payload["v"], payload["f"])
            self.model_panel.add_model(payload["name"], model_id)

            self.current_model_id = model_id
            self.viewer.set_selected_model(model_id)

            self.statusBar().showMessage(f"Loaded {payload['name']}")
            self._update_bed_warnings()
            self._push_undo_state()

        def on_err(msg):
            dlg.close()
            QtWidgets.QMessageBox.critical(self.main, "Load error", msg)

        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self.pool.start(worker)

    # ----------------------------------------------------------- slice/print
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

    def _build_slice_signature(self, settings: SliceSettings):
        if self.current_model_id is None:
            return None
        scale_offset = self.viewer.get_model_transform(self.current_model_id)
        rotation = self.viewer.get_model_rotation(self.current_model_id)
        if scale_offset is None or rotation is None:
            return None
        scale, offset = scale_offset
        payload = {
            "model_id": int(self.current_model_id),
            "scale": [float(v) for v in np.asarray(scale).reshape(-1)],
            "offset": [float(v) for v in np.asarray(offset).reshape(-1)],
            "rotation": [float(v) for v in np.asarray(rotation).reshape(-1)],
            "settings": asdict(settings),
        }
        return json.dumps(payload, sort_keys=True, default=str)

    def _slice_model(self,
                     settings: SliceSettings,
                     activate_preview: bool,
                     show_dialog: bool,
                     show_errors: bool = True):
        stl_path = self._get_current_stl_path()
        if not stl_path:
            if show_dialog:
                QtWidgets.QMessageBox.warning(self.main, "No model", "Load and select an STL first.")
            return
        mesh = self._get_current_mesh()
        if mesh is None:
            if show_dialog:
                QtWidgets.QMessageBox.warning(self.main, "No model", "Model data unavailable for slicing.")
            return
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

        worker = Worker(slice_trimesh,
                        mesh,
                        output_gcode_path=None,
                        settings=settings,
                        source_path=stl_path)
        worker.signals.finished.connect(on_done)
        worker.signals.error.connect(on_err)
        self.pool.start(worker)

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
        self.pool.start(worker)

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
        self.pool.start(worker)

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
        self.pool.start(worker)

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
        preview_text, total_lines = self._read_gcode_preview(gcode_path)
        self.preview_view.set_gcode_text(preview_text)
        self.preview_view.update_stats(stats)
        if hasattr(self.viewer, "set_print_stats"):
            self.viewer.set_print_stats(stats)
        preview = parse_gcode_preview_file(gcode_path)
        if hasattr(self.viewer, "set_gcode_preview"):
            self.viewer.set_gcode_preview(preview)
        self.preview_view.set_preview_data(preview)

    def _clear_preview(self):
        self._last_gcode_path = None
        self._last_slice_signature = None
        self._slice_in_progress = False
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

    # -------------------------------------------------------------- job queue
    def _add_current_model_to_queue(self):
        stl_path = self._get_current_stl_path()
        if not stl_path:
            QtWidgets.QMessageBox.warning(self.main, "No model", "Select a model before adding to queue.")
            return
        desc = f"Local: {os.path.basename(stl_path)}"
        payload = {"stl_path": stl_path}
        self.job_queue_panel.add_job(desc, payload)

    # ------------------------------------------------------ toolbar popups
    def _on_move_tool(self):
        self._enable_move_gizmo()
        self._toggle_popup(self._popup_move, self.transform_toolbar.move_action)

    def _on_rotate_tool(self):
        self._enable_rotate_gizmo()
        self._toggle_popup(self._popup_rotate, self.transform_toolbar.rotate_action)

    def _on_scale_tool(self):
        self._toggle_popup(self._popup_scale, self.transform_toolbar.scale_action)

    def _on_auto_orient_tool(self):
        self._toggle_popup(self._popup_auto_orient, self.transform_toolbar.auto_orient_action)

    def _on_arrange_tool(self):
        self._toggle_popup(self._popup_arrange, self.transform_toolbar.auto_arrange_action)

    def _toggle_popup(self, popup, action=None):
        if popup.isVisible():
            popup.hide()
            return
        self._hide_all_popups(except_popup=popup)
        if action is not None:
            popup._anchor_action = action
        self._position_popup(popup)
        self._sync_popups()
        popup.show()
        popup.raise_()

    def _hide_all_popups(self, except_popup=None):
        for popup in (
            self._popup_move,
            self._popup_rotate,
            self._popup_scale,
            self._popup_auto_orient,
            self._popup_arrange,
        ):
            if popup is not except_popup:
                popup.hide()

    def _position_popup(self, popup):
        if not hasattr(self, "transform_toolbar"):
            return
        toolbar = self.transform_toolbar
        action = getattr(popup, "_anchor_action", None)
        popup.adjustSize()
        if action is not None:
            btn = toolbar.widgetForAction(action)
            if btn is not None:
                anchor = btn.mapTo(self.main, QtCore.QPoint(btn.width() // 2, btn.height()))
                x = anchor.x() - popup.width() // 2
                x = max(8, min(x, self.main.width() - popup.width() - 8))
                y = anchor.y() + 6
                popup.move(QtCore.QPoint(x, y))
                return

        pos = toolbar.mapTo(self.main, QtCore.QPoint(8, toolbar.height() + 6))
        popup.move(pos)

    def _sync_popups(self):
        if self.current_model_id is None:
            self._popup_move.set_position(0.0, 0.0, 0.0)
            self._popup_rotate.set_rotation(0.0, 0.0, 0.0)
            self._popup_scale.set_scale(100.0, 100.0, 100.0)
            self._popup_scale.set_size(0.0, 0.0, 0.0)
            self._popup_move.center_btn.setEnabled(False)
            return

        transform = self.viewer.get_model_transform(self.current_model_id)
        if transform is None:
            return
        scale, offset = transform
        self._popup_move.set_position(float(offset[0]), float(offset[1]), float(offset[2]))
        self._popup_move.center_btn.setEnabled(True)
        scale_pct = np.array(scale, dtype=float) * 100.0
        self._popup_scale.set_scale(float(scale_pct[0]), float(scale_pct[1]), float(scale_pct[2]))

        rotation = self.viewer.get_model_rotation(self.current_model_id)
        if rotation is not None:
            self._popup_rotate.set_rotation(float(rotation[0]), float(rotation[1]), float(rotation[2]))

        bounds = self.viewer.get_model_bounds(self.current_model_id)
        if bounds is not None:
            mn, mx = bounds
            size = (float(mx[0] - mn[0]), float(mx[1] - mn[1]), float(mx[2] - mn[2]))
            self._popup_scale.set_size(size[0], size[1], size[2])

    def _apply_theme(self):
        if hasattr(self, "prepare_view"):
            self.prepare_view.apply_theme()
        if hasattr(self, "preview_view"):
            self.preview_view.apply_theme()
        if hasattr(self, "device_view"):
            self.device_view.apply_theme()
        if hasattr(self, "shared_view"):
            self.shared_view.apply_theme()

    def _on_theme_selected(self):
        action = self.sender()
        if action is None or not isinstance(action, QtWidgets.QAction):
            return
        name = action.data()
        if name:
            set_theme(str(name))
            self._apply_theme()
            self._set_theme_checked(str(name))

    def _set_theme_checked(self, name: str):
        if not hasattr(self, "_theme_group"):
            return
        for action in self._theme_group.actions():
            if action.data() == name:
                action.setChecked(True)
                break

    def _ensure_theme_action(self, name: str):
        if not hasattr(self, "_theme_group"):
            return None
        for action in self._theme_group.actions():
            if action.data() == name:
                return action
        if not hasattr(self, "_theme_menu"):
            return None
        label = name.capitalize()
        action = QtWidgets.QAction(label, self)
        action.setCheckable(True)
        action.setData(name)
        action.triggered.connect(self._on_theme_selected)
        self._theme_group.addAction(action)
        if hasattr(self, "_theme_menu_separator") and self._theme_menu_separator is not None:
            self._theme_menu.insertAction(self._theme_menu_separator, action)
        else:
            self._theme_menu.addAction(action)
        return action

    def _open_theme_editor(self):
        theme = export_theme()
        if theme is None:
            QtWidgets.QMessageBox.warning(self.main, "Theme", "No theme data available.")
            return

        dlg = QtWidgets.QDialog(self.main)
        dlg.setWindowTitle("Customize Theme")
        dlg.setModal(True)

        layout = QtWidgets.QVBoxLayout(dlg)
        editor = QtWidgets.QTextEdit(dlg)
        editor.setPlainText(json.dumps(theme, indent=2, ensure_ascii=True))
        layout.addWidget(editor)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.Close,
            parent=dlg,
        )
        layout.addWidget(buttons)

        def apply_changes():
            try:
                data = json.loads(editor.toPlainText())
            except json.JSONDecodeError as exc:
                QtWidgets.QMessageBox.warning(self.main, "Theme", f"Invalid JSON: {exc}")
                return
            if not isinstance(data, dict):
                QtWidgets.QMessageBox.warning(self.main, "Theme", "Theme data must be a JSON object.")
                return
            theme_data = register_theme("custom", data)
            if theme_data is None:
                QtWidgets.QMessageBox.warning(self.main, "Theme", "Theme data must be a JSON object.")
                return
            set_theme("custom")
            self._apply_theme()
            self._ensure_theme_action("custom")
            self._set_theme_checked("custom")
            self.statusBar().showMessage("Custom theme applied")

        buttons.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(apply_changes)
        buttons.rejected.connect(dlg.close)

        dlg.resize(720, 560)
        dlg.exec_()

    def _load_theme_from_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.main,
            "Load Theme",
            "",
            "Theme JSON (*.json);;All files (*.*)",
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except Exception as exc:
            QtWidgets.QMessageBox.warning(self.main, "Theme", str(exc))
            return

        theme_name = os.path.splitext(os.path.basename(path))[0]
        theme_payload = data
        if isinstance(data, dict) and "theme" in data:
            theme_payload = data.get("theme")
            name_value = data.get("name")
            if isinstance(name_value, str) and name_value:
                theme_name = name_value
        if not isinstance(theme_payload, dict):
            QtWidgets.QMessageBox.warning(self.main, "Theme", "Theme data must be a JSON object.")
            return

        theme_data = register_theme(theme_name, theme_payload)
        if theme_data is None:
            QtWidgets.QMessageBox.warning(self.main, "Theme", "Theme data must be a JSON object.")
            return
        set_theme(theme_name)
        self._apply_theme()
        self._ensure_theme_action(theme_name)
        self._set_theme_checked(theme_name)
        self.statusBar().showMessage(f"Loaded theme: {theme_name}")

    def _save_theme_to_file(self):
        theme = export_theme()
        if theme is None:
            QtWidgets.QMessageBox.warning(self.main, "Theme", "No theme data available.")
            return
        default_name = f"{get_theme_name()}.json"
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.main,
            "Save Theme",
            default_name,
            "Theme JSON (*.json);;All files (*.*)",
        )
        if not path:
            return
        if not path.lower().endswith(".json"):
            path = f"{path}.json"
        payload = {"name": get_theme_name(), "theme": theme}
        try:
            with open(path, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, ensure_ascii=True)
        except Exception as exc:
            QtWidgets.QMessageBox.warning(self.main, "Theme", str(exc))
            return
        self.statusBar().showMessage(f"Saved theme to {path}")

    def _on_transform_position_changed(self, x: float, y: float, z: float):
        if self.current_model_id is None:
            return
        self.viewer.set_model_transform(self.current_model_id, offset_xyz=(x, y, z))
        self._schedule_undo_snapshot()

    def _on_transform_rotation_changed(self, x: float, y: float, z: float):
        if self.current_model_id is None:
            return
        self.viewer.set_model_transform(self.current_model_id, rotation_xyz=(x, y, z))
        self._sync_popups()
        self._schedule_undo_snapshot()

    def _on_transform_rotation_reset(self):
        if self.current_model_id is None:
            return
        self.viewer.set_model_transform(self.current_model_id, rotation_xyz=(0.0, 0.0, 0.0))
        self._sync_popups()
        self._schedule_undo_snapshot()

    def _on_transform_center_requested(self):
        if self.current_model_id is None:
            return
        self.viewer.set_model_transform(self.current_model_id, offset_xyz=(0.0, 0.0, 0.0))
        self._sync_popups()
        self._update_bed_warnings()
        self._schedule_undo_snapshot()

    def _on_transform_scale_changed(self, x: float, y: float, z: float):
        if self.current_model_id is None:
            return
        scale = np.array([x, y, z], dtype=float) / 100.0
        scale = np.maximum(scale, 0.01)
        m = self.viewer.models.get(self.current_model_id)
        if m is None:
            return
        self.viewer.set_model_transform(self.current_model_id, scale=scale, offset_xyz=m["offset"])
        self._sync_popups()
        self._update_bed_warnings()
        self._schedule_undo_snapshot()

    def _on_auto_orient_requested(self, mode: str):
        _ = mode
        QtWidgets.QMessageBox.information(self.main, "Auto Orient", "Auto orient is not implemented yet.")

    def _on_auto_orient_reset(self):
        QtWidgets.QMessageBox.information(self.main, "Auto Orient", "Auto orient is not implemented yet.")

    def _on_arrange_requested(self):
        opts = self._popup_arrange.get_options()
        model_ids = self.viewer.get_model_ids()
        if not model_ids:
            QtWidgets.QMessageBox.warning(self.main, "Arrange", "Load models first.")
            return
        ok = self.viewer.arrange_models(
            model_ids,
            spacing=opts["spacing"],
            auto_rotate=opts["auto_rotate"],
            align_y=opts["align_y"],
        )
        if not ok:
            QtWidgets.QMessageBox.warning(self.main, "Arrange", "Unable to arrange models.")
            return
        self._sync_popups()
        self._update_bed_warnings()
        self._push_undo_state()

    def _on_arrange_selected_requested(self):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self.main, "Arrange", "Select a model first.")
            return
        opts = self._popup_arrange.get_options()
        ok = self.viewer.arrange_models(
            [self.current_model_id],
            spacing=opts["spacing"],
            auto_rotate=opts["auto_rotate"],
            align_y=opts["align_y"],
        )
        if not ok:
            QtWidgets.QMessageBox.warning(self.main, "Arrange", "Unable to arrange model.")
            return
        self._sync_popups()
        self._update_bed_warnings()
        self._push_undo_state()

    def _on_arrange_reset(self):
        self._sync_popups()

    def _new_project(self):
        self._current_project_path = None
        self._clear_all_models()

    def _not_implemented(self):
        QtWidgets.QMessageBox.information(self.main, "Not implemented", "This feature is not implemented yet.")

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
        out_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.main,
            "Save Project",
            suggested,
            "OpenSlicer Project (*.osproj);;All files (*.*)",
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
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.main,
            "Open Project",
            start_dir,
            "OpenSlicer Project (*.osproj);;All files (*.*)",
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

        models = data.get("models", [])
        if not isinstance(models, list):
            QtWidgets.QMessageBox.warning(self.main, "Open error", "Project models list is invalid.")
            return

        missing = []
        new_ids = []

        self._undo_in_progress = True
        try:
            lw = self.model_panel.list_widget
            block = lw.blockSignals(True)
            try:
                self.viewer.clear_all_models()
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

                    if not use_path:
                        if vertices is None or faces is None:
                            missing.append(model_path or name or "Unnamed model")
                            continue
                    model_id = self.viewer.add_model_from_data(
                        name,
                        resolved_path if use_path else model_path,
                        vertices,
                        faces,
                    )
                    self.model_panel.add_model(name, model_id)

                    self.viewer.set_model_transform(
                        model_id,
                        scale=entry.get("scale"),
                        rotation_xyz=entry.get("rotation"),
                        offset_xyz=entry.get("offset"),
                    )
                    new_ids.append(model_id)
            finally:
                lw.blockSignals(block)
        finally:
            self._undo_in_progress = False

        selected_index = data.get("selected_index")
        selected_id = None
        if new_ids:
            if isinstance(selected_index, int) and 0 <= selected_index < len(new_ids):
                selected_id = new_ids[selected_index]
            else:
                selected_id = new_ids[-1]
        self.current_model_id = selected_id
        self.viewer.set_selected_model(selected_id)
        if selected_id is not None:
            self._select_model_in_panel(selected_id)
        else:
            self.model_panel.list_widget.clearSelection()
        self._sync_popups()

        self._undo_stack.clear()
        self._redo_stack.clear()
        self._push_undo_state()

        if missing:
            QtWidgets.QMessageBox.warning(
                self,
                "Open warning",
                "Some models could not be loaded:\n" + "\n".join(missing),
            )

    def _serialize_project(self) -> dict:
        models = []
        for m in self.viewer.models.values():
            scale = self._scale_to_vec(m.get("scale", 1.0))
            rotation = self._vec3(m.get("rotation", [0.0, 0.0, 0.0]))
            offset = self._vec3(m.get("offset", [0.0, 0.0, 0.0]))
            entry = {
                "name": m.get("name", ""),
                "path": m.get("path", ""),
                "scale": [float(v) for v in scale],
                "rotation": [float(v) for v in rotation],
                "offset": [float(v) for v in offset],
            }
            if not entry["path"]:
                entry["vertices"] = np.asarray(m.get("base_vertices", []), dtype=float).tolist()
                entry["faces"] = np.asarray(m.get("faces", []), dtype=int).tolist()
            models.append(entry)

        settings = self.settings_panel.to_settings()
        return {
            "version": 1,
            "models": models,
            "settings": asdict(settings),
            "selected_index": self._selected_model_index(),
        }

    def _set_labels_visible(self, visible: bool):
        self._labels_visible = bool(visible)
        self.viewer.set_labels_visible(self._labels_visible)
        state = "on" if self._labels_visible else "off"
        self.statusBar().showMessage(f"Labels {state}")

    def _on_mode_tab_changed(self, button):
        if button is None:
            return
        label = button.text().strip().lower()
        if label:
            self._activate_mode(label)

    def _activate_mode(self, mode: str):
        mode = (mode or "").strip().lower()
        if not mode:
            return
        if mode == "prepare":
            self.prepare_view.show()
            self.preview_view.hide()
            self._central_stack.setCurrentWidget(self.viewer)
            if hasattr(self.viewer, "set_interaction_enabled"):
                self.viewer.set_interaction_enabled(True)
            if hasattr(self.viewer, "set_labels_visible"):
                self.viewer.set_labels_visible(self._labels_visible)
            if hasattr(self.viewer, "set_preview_visible"):
                self.viewer.set_preview_visible(False)
            if hasattr(self.viewer, "set_models_visible"):
                self.viewer.set_models_visible(True)
            if hasattr(self.viewer, "set_platform_visible"):
                self.viewer.set_platform_visible(True)
            if hasattr(self.viewer, "set_nozzle_visible"):
                self.viewer.set_nozzle_visible(False)
            if hasattr(self.viewer, "set_print_stats_visible"):
                self.viewer.set_print_stats_visible(True)
            if hasattr(self.viewer, "set_preview_object_visible"):
                self.viewer.set_preview_object_visible(False)
            self._auto_slice_prepare()
            QtCore.QTimer.singleShot(0, self.prepare_view.position_panels)
        elif mode == "preview":
            self.prepare_view.hide()
            self.preview_view.show()
            self._central_stack.setCurrentWidget(self.viewer)
            if hasattr(self.viewer, "set_interaction_enabled"):
                self.viewer.set_interaction_enabled(False)
            if hasattr(self.viewer, "set_labels_visible"):
                self.viewer.set_labels_visible(False)
            if hasattr(self.viewer, "set_preview_visible"):
                self.viewer.set_preview_visible(True)
            if hasattr(self.viewer, "set_models_visible"):
                self.viewer.set_models_visible(False)
            if hasattr(self.viewer, "set_print_stats_visible"):
                self.viewer.set_print_stats_visible(False)
            if hasattr(self.viewer, "set_preview_object_visible"):
                self.viewer.set_preview_object_visible(True)
            if hasattr(self.preview_view, "sync_preview_toggles"):
                self.preview_view.sync_preview_toggles()
            QtCore.QTimer.singleShot(0, self.preview_view.position_panels)
        elif mode == "device":
            self.prepare_view.hide()
            self.preview_view.hide()
            self._central_stack.setCurrentWidget(self.device_view)
            if hasattr(self.viewer, "set_interaction_enabled"):
                self.viewer.set_interaction_enabled(False)
            if hasattr(self.viewer, "set_preview_visible"):
                self.viewer.set_preview_visible(False)
            if hasattr(self.viewer, "set_models_visible"):
                self.viewer.set_models_visible(False)
            if hasattr(self.viewer, "set_print_stats_visible"):
                self.viewer.set_print_stats_visible(False)
            if hasattr(self.viewer, "set_preview_object_visible"):
                self.viewer.set_preview_object_visible(False)
        else:
            return
        self._active_mode = mode

    def _auto_slice_prepare(self):
        if self.current_model_id is None:
            return
        settings = self.settings_panel.to_settings()
        signature = self._build_slice_signature(settings)
        if signature and signature == self._last_slice_signature and self._last_gcode_path:
            return
        self._slice_model(settings,
                          activate_preview=False,
                          show_dialog=False,
                          show_errors=False)

    def _open_device_view(self):
        if hasattr(self, "_mode_tabs"):
            for btn in self._mode_tabs:
                if btn.text().strip().lower() == "device":
                    btn.setChecked(True)
                    break
        self._activate_mode("device")

    def _switch_mode_tab(self):
        if not hasattr(self, "_mode_tabs"):
            return
        enabled_tabs = [btn for btn in self._mode_tabs if btn.isEnabled()]
        if not enabled_tabs:
            return
        current_idx = 0
        for idx, btn in enumerate(enabled_tabs):
            if btn.isChecked():
                current_idx = idx
                break
        next_idx = (current_idx + 1) % len(enabled_tabs)
        enabled_tabs[next_idx].setChecked(True)
        self._on_mode_tab_changed(enabled_tabs[next_idx])

    def _select_all_models(self):
        lw = self.model_panel.list_widget
        if lw.count() == 0:
            return
        lw.selectAll()
        item = lw.currentItem() or lw.item(0)
        if item is None:
            return
        model_id = item.data(QtCore.Qt.UserRole)
        self.current_model_id = model_id
        self.viewer.set_selected_model(model_id)
        self.statusBar().showMessage("Selected all models")

    def _selected_model_ids(self):
        lw = self.model_panel.list_widget
        selected = []
        for row in range(lw.count()):
            item = lw.item(row)
            if item is not None and item.isSelected():
                selected.append(item.data(QtCore.Qt.UserRole))
        if not selected and self.current_model_id is not None:
            selected.append(self.current_model_id)
        return selected

    def _copy_selected(self):
        model_ids = self._selected_model_ids()
        if not model_ids:
            return
        payloads = self._capture_models_payload(model_ids)
        if not payloads:
            return
        self._model_clipboard = payloads
        self.statusBar().showMessage(f"Copied {len(payloads)} model(s)")

    def _cut_selected(self):
        model_ids = self._selected_model_ids()
        if not model_ids:
            return
        payloads = self._capture_models_payload(model_ids)
        if not payloads:
            return
        self._model_clipboard = payloads
        self._remove_models(model_ids)
        self.statusBar().showMessage(f"Cut {len(payloads)} model(s)")

    def _paste_clipboard(self):
        if not self._model_clipboard:
            return
        new_ids = self._apply_model_payloads(self._model_clipboard, offset_step=(10.0, 10.0, 0.0))
        if new_ids:
            self._push_undo_state()
            self.statusBar().showMessage(f"Pasted {len(new_ids)} model(s)")

    def _clone_selected(self):
        model_ids = self._selected_model_ids()
        if not model_ids:
            return
        payloads = self._capture_models_payload(model_ids)
        if not payloads:
            return
        new_ids = self._apply_model_payloads(payloads, offset_step=(10.0, 10.0, 0.0))
        if new_ids:
            self._push_undo_state()
            self.statusBar().showMessage(f"Cloned {len(new_ids)} model(s)")

    def _capture_models_payload(self, model_ids):
        payloads = []
        for model_id in model_ids:
            payload = self._capture_model_payload(model_id)
            if payload is not None:
                payloads.append(payload)
        return payloads

    def _capture_model_payload(self, model_id: int):
        m = self.viewer.models.get(model_id)
        if not m:
            return None
        return {
            "name": m.get("name", f"Model {model_id}"),
            "path": m.get("path", ""),
            "base_vertices": np.asarray(m.get("base_vertices", []), dtype=float).copy(),
            "faces": np.asarray(m.get("faces", []), dtype=int).copy(),
            "scale": self._scale_to_vec(m.get("scale", 1.0)),
            "rotation": self._vec3(m.get("rotation", [0.0, 0.0, 0.0])),
            "offset": self._vec3(m.get("offset", [0.0, 0.0, 0.0])),
        }

    def _apply_model_payloads(self, payloads, offset_step=(0.0, 0.0, 0.0)):
        if not payloads:
            return []
        new_ids = []
        for idx, payload in enumerate(payloads):
            model_id = self.viewer.add_model_from_data(
                payload["name"],
                payload["path"],
                payload["base_vertices"],
                payload["faces"],
            )
            delta = np.array(offset_step, dtype=float) * float(idx + 1)
            offset = np.array(payload["offset"], dtype=float) + delta
            self.viewer.set_model_transform(
                model_id,
                scale=payload["scale"],
                rotation_xyz=payload["rotation"],
                offset_xyz=offset,
            )
            self.model_panel.add_model(payload["name"], model_id)
            new_ids.append(model_id)
        if new_ids:
            self._select_model_in_panel(new_ids[-1])
            self.current_model_id = new_ids[-1]
            self.viewer.set_selected_model(new_ids[-1])
            self._sync_popups()
        return new_ids

    def _remove_models(self, model_ids):
        model_ids = [mid for mid in model_ids if mid in self.viewer.models]
        if not model_ids:
            return
        lw = self.model_panel.list_widget
        block = lw.blockSignals(True)
        try:
            for model_id in model_ids:
                self.viewer.remove_model(model_id)
                self.model_panel.remove_model(model_id)
        finally:
            lw.blockSignals(block)

        remaining = self.viewer.get_model_ids()
        self.current_model_id = remaining[0] if remaining else None
        self.viewer.set_selected_model(self.current_model_id)
        if self.current_model_id is not None:
            self._select_model_in_panel(self.current_model_id)
        else:
            self.model_panel.list_widget.clearSelection()
        if len(model_ids) == 1:
            self.statusBar().showMessage("Model removed")
        else:
            self.statusBar().showMessage(f"Removed {len(model_ids)} models")
        self._sync_popups()
        self._push_undo_state()
        self._clear_preview()

    def _select_model_in_panel(self, model_id: int):
        lw = self.model_panel.list_widget
        block = lw.blockSignals(True)
        try:
            for row in range(lw.count()):
                item = lw.item(row)
                if item is None:
                    continue
                if item.data(QtCore.Qt.UserRole) == model_id:
                    lw.setCurrentItem(item)
                    break
        finally:
            lw.blockSignals(block)

    def _selected_model_index(self):
        model_ids = list(self.viewer.models.keys())
        if self.current_model_id in model_ids:
            return model_ids.index(self.current_model_id)
        return None

    def _vec3(self, value, default=(0.0, 0.0, 0.0)) -> np.ndarray:
        if value is None:
            return np.array(default, dtype=float)
        try:
            arr = np.asarray(value, dtype=float).reshape(-1)
        except Exception:
            return np.array(default, dtype=float)
        if arr.size != 3:
            return np.array(default, dtype=float)
        return arr.astype(float)

    def _scale_to_vec(self, scale) -> np.ndarray:
        if isinstance(scale, np.ndarray):
            arr = scale.astype(float).reshape(-1)
            if arr.size == 3:
                return arr
            if arr.size == 1:
                val = float(arr[0])
                return np.array([val, val, val], dtype=float)
        if isinstance(scale, (list, tuple)) and len(scale) == 3:
            return np.array([float(scale[0]), float(scale[1]), float(scale[2])], dtype=float)
        try:
            val = float(scale)
        except Exception:
            val = 1.0
        return np.array([val, val, val], dtype=float)

    def _capture_state(self):
        model_ids = list(self.viewer.models.keys())
        selected_index = self._selected_model_index()
        payloads = self._capture_models_payload(model_ids)
        return {
            "models": payloads,
            "selected_index": selected_index,
        }

    def _state_signature(self, state) -> tuple:
        model_sigs = []
        for payload in state.get("models", []):
            scale = tuple(float(v) for v in np.asarray(payload["scale"], dtype=float).reshape(-1))
            rotation = tuple(float(v) for v in np.asarray(payload["rotation"], dtype=float).reshape(-1))
            offset = tuple(float(v) for v in np.asarray(payload["offset"], dtype=float).reshape(-1))
            verts_shape = np.asarray(payload["base_vertices"]).shape
            faces_shape = np.asarray(payload["faces"]).shape
            model_sigs.append(
                (
                    payload.get("name", ""),
                    payload.get("path", ""),
                    scale,
                    rotation,
                    offset,
                    verts_shape,
                    faces_shape,
                )
            )
        return (state.get("selected_index"), tuple(model_sigs))

    def _push_undo_state(self):
        if self._undo_in_progress:
            return
        if self._pending_undo_snapshot:
            self._undo_timer.stop()
            self._pending_undo_snapshot = False
        state = self._capture_state()
        signature = self._state_signature(state)
        if self._undo_stack and self._undo_stack[-1].get("signature") == signature:
            return
        state["signature"] = signature
        self._undo_stack.append(state)
        if len(self._undo_stack) > self._undo_stack_limit:
            self._undo_stack.pop(0)
        self._redo_stack.clear()
        self._update_undo_redo_state()

    def _schedule_undo_snapshot(self, delay_ms: int = 250):
        if self._undo_in_progress:
            return
        self._pending_undo_snapshot = True
        self._undo_timer.start(delay_ms)

    def _finalize_undo_snapshot(self):
        if not self._pending_undo_snapshot:
            return
        self._pending_undo_snapshot = False
        self._push_undo_state()

    def _restore_state(self, state):
        self._undo_in_progress = True
        try:
            lw = self.model_panel.list_widget
            block = lw.blockSignals(True)
            try:
                self.viewer.clear_all_models()
                self.model_panel.list_widget.clear()
                new_ids = []
                for payload in state.get("models", []):
                    model_id = self.viewer.add_model_from_data(
                        payload["name"],
                        payload["path"],
                        payload["base_vertices"],
                        payload["faces"],
                    )
                    self.model_panel.add_model(payload["name"], model_id)
                    self.viewer.set_model_transform(
                        model_id,
                        scale=payload["scale"],
                        rotation_xyz=payload["rotation"],
                        offset_xyz=payload["offset"],
                    )
                    new_ids.append(model_id)
            finally:
                lw.blockSignals(block)

            selected_index = state.get("selected_index")
            selected_id = None
            if new_ids:
                if selected_index is not None and 0 <= selected_index < len(new_ids):
                    selected_id = new_ids[selected_index]
                else:
                    selected_id = new_ids[-1]
            self.current_model_id = selected_id
            self.viewer.set_selected_model(selected_id)
            if selected_id is not None:
                self._select_model_in_panel(selected_id)
            else:
                self.model_panel.list_widget.clearSelection()
            self._sync_popups()
        finally:
            self._undo_in_progress = False
        self._update_undo_redo_state()

    def _undo(self):
        if len(self._undo_stack) <= 1:
            return
        current = self._undo_stack.pop()
        self._redo_stack.append(current)
        self._restore_state(self._undo_stack[-1])

    def _redo(self):
        if not self._redo_stack:
            return
        state = self._redo_stack.pop()
        self._undo_stack.append(state)
        self._restore_state(state)

    def _update_undo_redo_state(self):
        can_undo = len(self._undo_stack) > 1
        can_redo = bool(self._redo_stack)
        if hasattr(self, "_undo_action"):
            self._undo_action.setEnabled(can_undo)
        if hasattr(self, "_redo_action"):
            self._redo_action.setEnabled(can_redo)
        if hasattr(self, "_undo_btn"):
            self._undo_btn.setEnabled(can_undo)
        if hasattr(self, "_redo_btn"):
            self._redo_btn.setEnabled(can_redo)

    def _delete_selected_model(self):
        model_ids = self._selected_model_ids()
        if not model_ids:
            return
        self._remove_models(model_ids)

    def _deselect_all_models(self):
        self.current_model_id = None
        self.viewer.set_selected_model(None)
        self.model_panel.list_widget.clearSelection()
        self._sync_popups()

    def _show_settings_panel(self):
        if hasattr(self, "_settings_dock"):
            self._settings_dock.show()
            self._settings_dock.raise_()
            self.settings_panel.setFocus(QtCore.Qt.OtherFocusReason)

    def _set_view_preset(self, azimuth: float, elevation: float):
        self.viewer.set_view(float(azimuth), float(elevation))

    def _set_projection_mode(self, mode: str):
        if mode == "ortho":
            self.viewer.opts["fov"] = 0  # pyright: ignore[reportArgumentType]
        else:
            self.viewer.opts["fov"] = 60  # pyright: ignore[reportArgumentType]
        self.viewer.update()

    def _toggle_view_cube(self, checked: bool):
        self.viewer.set_view_cube_visible(bool(checked))

    def _reset_window_layout(self):
        if hasattr(self, "_model_dock"):
            self._model_dock.show()
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self._model_dock)
        if hasattr(self, "_settings_dock"):
            self._settings_dock.show()
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self._settings_dock)
        if hasattr(self, "_job_dock"):
            self._job_dock.show()
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self._job_dock)

    def _busy_dialog(self, title: str, label: str):
        dlg = QtWidgets.QProgressDialog(label, "", 0, 0, self.main)
        dlg.setWindowTitle(title)
        dlg.setWindowModality(QtCore.Qt.ApplicationModal)
        dlg.setAutoClose(True)
        dlg.setAutoReset(True)
        dlg.setRange(0, 0)
        return dlg

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        for popup in (
            self._popup_move,
            self._popup_rotate,
            self._popup_scale,
            self._popup_auto_orient,
            self._popup_arrange,
        ):
            if popup.isVisible():
                self._position_popup(popup)
        if hasattr(self, "prepare_view"):
            self.prepare_view.position_panels()
        if hasattr(self, "preview_view"):
            self.preview_view.position_panels()
