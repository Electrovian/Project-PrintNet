# pyright: reportAttributeAccessIssue=false
# pyright: reportCallIssue=false
# pyright: reportArgumentType=false
from __future__ import annotations

import json
import math
import os
import re
import subprocess
import sys
from typing import Any, TYPE_CHECKING

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from ...theme import export_theme, get_theme_name, register_theme, set_theme
from config.defaults import DEFAULTS
from config.runtime_printer_state import (
    RuntimePrinterState,
    runtime_printer_state_from_defaults,
    runtime_printer_state_from_profile,
)
from slicer_v2.legacy_gcode_writer import (
    SliceSettings,
    generate_flow_rate_test,
    generate_max_flowrate_test,
    generate_pressure_advance_pattern,
    generate_retraction_tower,
    generate_temperature_tower,
    generate_tolerance_test,
)

if TYPE_CHECKING:
    UiMixinBase = QtCore.QObject
else:
    UiMixinBase = object


class UiMixin(UiMixinBase):
    def __getattr__(self, name: str) -> Any:
        # MainController owns the runtime __getattr__ proxy; this keeps type checkers quiet.
        raise AttributeError(name)

    def _dialog_parent(self):
        parent = getattr(self, "main", None)
        return parent if isinstance(parent, QtWidgets.QWidget) else None

    def _use_tk_file_dialog(self) -> bool:
        if os.name != "nt":
            return False
        # Tk dialogs are opt-in; they may still crash on some Windows Python builds.
        default_flag = "0"
        flag = str(os.environ.get("EON_USE_TK_FILE_DIALOG", default_flag)).strip().lower()
        return flag in ("1", "true", "yes", "on")

    def _use_powershell_file_dialog(self) -> bool:
        if os.name != "nt":
            return False
        # Use a WinForms dialog through powershell on Python 3.13 Windows.
        default_flag = "1" if sys.version_info[:2] >= (3, 13) else "0"
        flag = str(os.environ.get("EON_USE_PS_FILE_DIALOG", default_flag)).strip().lower()
        return flag in ("1", "true", "yes", "on")

    def _use_native_qt_file_dialog(self) -> bool:
        # Windows should use the native Explorer-style file dialog by default.
        default_flag = "1" if os.name == "nt" else "0"
        flag = str(os.environ.get("EON_USE_NATIVE_FILE_DIALOG", default_flag)).strip().lower()
        return flag in ("1", "true", "yes", "on")

    def _qt_file_dialog_options(self):
        options = QtWidgets.QFileDialog.Options()
        if not self._use_native_qt_file_dialog():
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
        return options

    def _qt_filter_to_tk(self, file_filter: str):
        value = str(file_filter or "").strip()
        if not value:
            return [("All files", "*.*")]
        chunks = [part.strip() for part in value.split(";;") if part.strip()]
        rows = []
        for chunk in chunks:
            match = re.match(r"^([^()]+)\(([^()]+)\)$", chunk)
            if match is None:
                rows.append((chunk, "*.*"))
                continue
            label = match.group(1).strip() or "Files"
            patterns_raw = match.group(2).strip()
            patterns = [part.strip() for part in patterns_raw.split() if part.strip()]
            if not patterns:
                patterns = ["*.*"]
            rows.append((label, " ".join(patterns)))
        if not rows:
            rows.append(("All files", "*.*"))
        return rows

    def _qt_filter_to_winforms(self, file_filter: str) -> str:
        value = str(file_filter or "").strip()
        if not value:
            return "All files|*.*"
        chunks = [part.strip() for part in value.split(";;") if part.strip()]
        entries: list[str] = []
        for chunk in chunks:
            match = re.match(r"^([^()]+)\(([^()]+)\)$", chunk)
            if match is None:
                label = chunk or "Files"
                pattern = "*.*"
            else:
                label = match.group(1).strip() or "Files"
                patterns_raw = match.group(2).strip()
                parts = [part.strip() for part in patterns_raw.split() if part.strip()]
                pattern = ";".join(parts) if parts else "*.*"
            entries.extend([label, pattern])
        if not entries:
            entries = ["All files", "*.*"]
        return "|".join(entries)

    def _ps_open_file_names(self, caption: str, directory: str, file_filter: str):
        if not self._use_powershell_file_dialog():
            return None
        init_dir = str(directory or os.getcwd())
        wf_filter = self._qt_filter_to_winforms(file_filter)
        script = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "$d=New-Object System.Windows.Forms.OpenFileDialog; "
            "$d.Title=$args[0]; "
            "$d.InitialDirectory=$args[1]; "
            "$d.Filter=$args[2]; "
            "$d.Multiselect=$true; "
            "$d.CheckFileExists=$true; "
            "$d.RestoreDirectory=$true; "
            "if($d.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK){"
            "$d.FileNames | ForEach-Object { $_ }"
            "}"
        )
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-STA", "-Command", script, str(caption or ""), init_dir, wf_filter],
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
        except Exception:
            return None
        if int(result.returncode) != 0:
            return None
        paths = [line.strip() for line in str(result.stdout or "").splitlines() if line.strip()]
        return paths

    def _ps_open_file_name(self, caption: str, directory: str, file_filter: str):
        if not self._use_powershell_file_dialog():
            return None
        paths = self._ps_open_file_names(caption, directory, file_filter)
        if paths is None:
            return None
        return str(paths[0]) if paths else ""

    def _ps_save_file_name(self, caption: str, directory: str, file_filter: str):
        if not self._use_powershell_file_dialog():
            return None
        init_dir = str(directory or os.getcwd())
        wf_filter = self._qt_filter_to_winforms(file_filter)
        script = (
            "Add-Type -AssemblyName System.Windows.Forms; "
            "$d=New-Object System.Windows.Forms.SaveFileDialog; "
            "$d.Title=$args[0]; "
            "$d.InitialDirectory=$args[1]; "
            "$d.Filter=$args[2]; "
            "$d.RestoreDirectory=$true; "
            "if($d.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK){"
            "$d.FileName"
            "}"
        )
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-STA", "-Command", script, str(caption or ""), init_dir, wf_filter],
                capture_output=True,
                text=True,
                timeout=120,
                check=False,
            )
        except Exception:
            return None
        if int(result.returncode) != 0:
            return None
        value = str(result.stdout or "").strip()
        return value if value else ""

    def _tk_open_file_names(self, caption: str, directory: str, file_filter: str):
        if not self._use_tk_file_dialog():
            return None
        try:
            import tkinter as tk
            from tkinter import filedialog
        except Exception:
            return None
        root = tk.Tk()
        try:
            root.withdraw()
            root.attributes("-topmost", True)
            root.update()
            selected = filedialog.askopenfilenames(
                parent=root,
                title=str(caption or ""),
                initialdir=str(directory or os.getcwd()),
                filetypes=self._qt_filter_to_tk(file_filter),
            )
        finally:
            root.destroy()
        paths = [str(path) for path in (selected or []) if str(path).strip()]
        return paths

    def _tk_open_file_name(self, caption: str, directory: str, file_filter: str):
        if not self._use_tk_file_dialog():
            return None
        try:
            import tkinter as tk
            from tkinter import filedialog
        except Exception:
            return None
        root = tk.Tk()
        try:
            root.withdraw()
            root.attributes("-topmost", True)
            root.update()
            selected = filedialog.askopenfilename(
                parent=root,
                title=str(caption or ""),
                initialdir=str(directory or os.getcwd()),
                filetypes=self._qt_filter_to_tk(file_filter),
            )
        finally:
            root.destroy()
        value = str(selected or "").strip()
        return value if value else ""

    def _tk_save_file_name(self, caption: str, directory: str, file_filter: str):
        if not self._use_tk_file_dialog():
            return None
        try:
            import tkinter as tk
            from tkinter import filedialog
        except Exception:
            return None
        root = tk.Tk()
        try:
            root.withdraw()
            root.attributes("-topmost", True)
            root.update()
            selected = filedialog.asksaveasfilename(
                parent=root,
                title=str(caption or ""),
                initialdir=str(directory or os.getcwd()),
                filetypes=self._qt_filter_to_tk(file_filter),
            )
        finally:
            root.destroy()
        value = str(selected or "").strip()
        return value if value else ""

    def _safe_get_open_file_name(
        self,
        caption: str,
        directory: str,
        file_filter: str,
    ) -> tuple[str, str]:
        ps_path = self._ps_open_file_name(caption, directory, file_filter)
        if ps_path is not None:
            return str(ps_path), str(file_filter or "")
        tk_path = self._tk_open_file_name(caption, directory, file_filter)
        if tk_path is not None:
            return tk_path, str(file_filter or "")
        path, selected_filter = QtWidgets.QFileDialog.getOpenFileName(
            self._dialog_parent(),
            caption,
            directory,
            file_filter,
            options=self._qt_file_dialog_options(),
        )
        return str(path or ""), str(selected_filter or "")

    def _safe_get_open_file_names(
        self,
        caption: str,
        directory: str,
        file_filter: str,
    ) -> tuple[list[str], str]:
        ps_paths = self._ps_open_file_names(caption, directory, file_filter)
        if ps_paths is not None:
            return [str(path) for path in ps_paths], str(file_filter or "")
        tk_paths = self._tk_open_file_names(caption, directory, file_filter)
        if tk_paths is not None:
            return tk_paths, str(file_filter or "")
        paths, selected_filter = QtWidgets.QFileDialog.getOpenFileNames(
            self._dialog_parent(),
            caption,
            directory,
            file_filter,
            options=self._qt_file_dialog_options(),
        )
        return [str(path) for path in (paths or [])], str(selected_filter or "")

    def _safe_get_save_file_name(
        self,
        caption: str,
        directory: str,
        file_filter: str,
    ) -> tuple[str, str]:
        ps_path = self._ps_save_file_name(caption, directory, file_filter)
        if ps_path is not None:
            return str(ps_path), str(file_filter or "")
        tk_path = self._tk_save_file_name(caption, directory, file_filter)
        if tk_path is not None:
            return tk_path, str(file_filter or "")
        path, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self._dialog_parent(),
            caption,
            directory,
            file_filter,
            options=self._qt_file_dialog_options(),
        )
        return str(path or ""), str(selected_filter or "")

    # -------------------------------------------------- Model selection/removal
    def _on_model_selected(self, model_id: int):
        if model_id is None:
            return
        self.current_model_id = model_id
        selected = self._selected_model_ids()
        if model_id not in selected:
            selected = [model_id]
        self.viewer.set_selected_models(selected, emit_signal=False)
        if len(selected) == 1:
            name = self.viewer.get_model_name(model_id) or "Model"
            self.statusBar().showMessage(f"Selected {name}")
        else:
            self.statusBar().showMessage(f"Selected {len(selected)} models")
        self.viewer.set_gizmo_mode("move")
        self._sync_popups()

    def _on_model_selection_changed(self, model_ids: list):
        ids = [int(mid) for mid in model_ids] if model_ids else []
        if not ids:
            self.current_model_id = None
            self.viewer.set_selected_models([], emit_signal=False)
            self.statusBar().showMessage("Selection cleared")
            self._sync_popups()
            return
        self.current_model_id = ids[0]
        self.viewer.set_selected_models(ids, emit_signal=False)
        if len(ids) == 1:
            name = self.viewer.get_model_name(ids[0]) or "Model"
            self.statusBar().showMessage(f"Selected {name}")
        else:
            self.statusBar().showMessage(f"Selected {len(ids)} models")
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
            cols = int(math.ceil(count / rows))

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
            self._refresh_files_view()

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
        _ = model_id
        selected = self.viewer.get_selected_model_ids() if hasattr(self.viewer, "get_selected_model_ids") else []
        if not selected:
            selected = [model_id]
        self._sync_selection_from_viewer(selected)
        self.viewer.set_gizmo_mode("move")

    def _on_viewer_selection_changed(self, model_ids: list):
        self._sync_selection_from_viewer(model_ids)

    def _sync_selection_from_viewer(self, model_ids: list):
        ids = [int(mid) for mid in model_ids] if model_ids else []
        self.current_model_id = ids[0] if ids else None
        lw = self.model_panel.list_widget
        block = lw.blockSignals(True)
        try:
            lw.clearSelection()
            for row in range(lw.count()):
                item = lw.item(row)
                if item is None:
                    continue
                if item.data(QtCore.Qt.UserRole) in ids:
                    item.setSelected(True)
                    if item.data(QtCore.Qt.UserRole) == self.current_model_id:
                        lw.setCurrentItem(item)
        finally:
            lw.blockSignals(block)
        if ids:
            if len(ids) == 1:
                name = self.viewer.get_model_name(ids[0]) or "Model"
                self.statusBar().showMessage(f"Selected {name}")
            else:
                self.statusBar().showMessage(f"Selected {len(ids)} models")
        else:
            self.statusBar().showMessage("Selection cleared")

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
        bed, max_height, _printer_name = self._effective_bed_limits()
        bed_str = f"{bed[0]}x{bed[1]} mm"
        msg = "Warning: " + ", ".join(names) + f" exceed bed {bed_str} or height {max_height} mm."
        self.statusBar().showMessage(msg)
        self._bed_warning_active = True

    def _effective_bed_limits(self) -> tuple[tuple[float, float], float, str]:
        state = getattr(self, "runtime_printer_state", None)
        if isinstance(state, RuntimePrinterState):
            return state.bed_size, float(state.bed_z), str(state.name)
        defaults = DEFAULTS.get("printer", {})
        bed_defaults = defaults.get("bed_size", (200.0, 200.0))
        if not isinstance(bed_defaults, (list, tuple)) or len(bed_defaults) < 2:
            bed_defaults = (200.0, 200.0)
        bed_x = float(bed_defaults[0])
        bed_y = float(bed_defaults[1])
        bed_z = float(defaults.get("max_height", 200.0))
        name = str(defaults.get("name", "Printer")).strip() or "Printer"
        return (bed_x, bed_y), bed_z, name

    def _apply_printer_profile(self, printer: dict | None, source: str | None = None):
        if printer is None:
            return
        if hasattr(self, "printer_manager"):
            self.printer_manager.set_active_printer(printer)
        existing_state = getattr(self, "runtime_printer_state", None)
        if not isinstance(existing_state, RuntimePrinterState):
            existing_state = runtime_printer_state_from_defaults(DEFAULTS.get("printer", {}))
        self.runtime_printer_state = runtime_printer_state_from_profile(
            printer,
            fallback_state=existing_state,
            source=source or "runtime",
        )
        bed_x, bed_y = self.runtime_printer_state.bed_size
        bed_z = float(self.runtime_printer_state.bed_z)

        main = self.__dict__.get("main")
        viewer = main.__dict__.get("viewer") if main is not None else None
        if viewer is not None and hasattr(viewer, "set_bed_limits"):
            viewer.set_bed_limits((bed_x, bed_y), bed_z)
        if viewer is not None:
            self._update_bed_warnings()
        self._sync_printer_selection(printer, source=source)

    def _sync_printer_selection(self, printer: dict, source: str | None = None):
        name = str(printer.get("name", "")).strip()
        if not name:
            state = getattr(self, "runtime_printer_state", None)
            if isinstance(state, RuntimePrinterState):
                name = str(state.name).strip()
        if not name:
            return
        if source != "settings" and hasattr(self, "settings_panel"):
            self.settings_panel.select_printer_by_name(name, emit=False)
        if source != "device" and hasattr(self, "device_view"):
            self.device_view.select_printer_by_name(name, emit=False)
        if source != "control" and hasattr(self, "control_view"):
            self.control_view.select_printer_by_name(name, emit=False)
        if source != "preview" and hasattr(self, "preview_view"):
            self.preview_view.select_printer_by_name(name, emit=False)

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
        if hasattr(self, "files_view"):
            self.files_view.apply_theme()
        if hasattr(self, "activity_view"):
            self.activity_view.apply_theme()
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
        path, _ = self._safe_get_open_file_name(
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
        path, _ = self._safe_get_save_file_name(
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
        model_ids = []
        if self.current_model_id is not None:
            model_ids = [self.current_model_id]
        else:
            model_ids = self.viewer.get_model_ids()
        if not model_ids:
            QtWidgets.QMessageBox.warning(self.main, "Auto Orient", "Load models first.")
            return

        overhang_angle = SliceSettings().overhang_angle
        failed = []
        for mid in model_ids:
            ok = self.viewer.auto_orient_model(mid, mode=mode, overhang_angle=overhang_angle)
            if not ok:
                failed.append(mid)
        if failed:
            QtWidgets.QMessageBox.warning(
                self.main,
                "Auto Orient",
                "Unable to auto orient one or more models.",
            )
        self._sync_popups()
        self._update_bed_warnings()
        self._schedule_undo_snapshot()

    def _on_auto_orient_reset(self):
        model_ids = []
        if self.current_model_id is not None:
            model_ids = [self.current_model_id]
        else:
            model_ids = self.viewer.get_model_ids()
        if not model_ids:
            QtWidgets.QMessageBox.warning(self.main, "Auto Orient", "Load models first.")
            return
        for mid in model_ids:
            self.viewer.set_model_transform(mid, rotation_xyz=(0.0, 0.0, 0.0))
        self._sync_popups()
        self._update_bed_warnings()
        self._schedule_undo_snapshot()

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
        if mode != "preview":
            prev = getattr(self, "_preview_wireframe_prev", None)
            if prev is not None and hasattr(self.viewer, "set_wireframe_enabled"):
                self.viewer.set_wireframe_enabled(prev)
            self._preview_wireframe_prev = None
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
            if hasattr(self.viewer, "set_models_preview_alpha"):
                self.viewer.set_models_preview_alpha(1.0)
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
            self._auto_slice_prepare()
            if hasattr(self.viewer, "get_wireframe_enabled"):
                if getattr(self, "_preview_wireframe_prev", None) is None:
                    self._preview_wireframe_prev = self.viewer.get_wireframe_enabled()
            if hasattr(self.viewer, "set_wireframe_enabled"):
                # Keep preview focused on emitted toolpaths, not model mesh edges.
                self.viewer.set_wireframe_enabled(False)
            if hasattr(self.viewer, "set_interaction_enabled"):
                self.viewer.set_interaction_enabled(False)
            if hasattr(self.viewer, "set_labels_visible"):
                self.viewer.set_labels_visible(False)
            if hasattr(self.viewer, "set_preview_visible"):
                self.viewer.set_preview_visible(True)
            if hasattr(self.viewer, "set_models_visible"):
                self.viewer.set_models_visible(False)
            if hasattr(self.viewer, "set_models_preview_alpha"):
                self.viewer.set_models_preview_alpha(1.0)
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
        elif mode == "control":
            self.prepare_view.hide()
            self.preview_view.hide()
            self._central_stack.setCurrentWidget(self.control_view)
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
        elif mode == "files":
            self.prepare_view.hide()
            self.preview_view.hide()
            self._central_stack.setCurrentWidget(self.files_view)
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
            self._refresh_files_view()
        elif mode == "activity":
            self.prepare_view.hide()
            self.preview_view.hide()
            self._central_stack.setCurrentWidget(self.activity_view)
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

    def _refresh_files_view(self):
        if hasattr(self, "files_view") and hasattr(self.files_view, "refresh_from_viewer"):
            self.files_view.refresh_from_viewer(self.viewer)

    def _auto_slice_prepare(self):
        if not self.viewer.get_model_ids():
            return
        settings = self.settings_panel.to_settings()
        reusable = None
        if hasattr(self, "_resolve_reusable_gcode_path"):
            reusable = self._resolve_reusable_gcode_path(settings)
        if reusable:
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
        self.viewer.set_selected_models(self._selected_model_ids(), emit_signal=False)
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
            self._select_model_in_panel(new_ids)
            self.current_model_id = new_ids[0]
            self.viewer.set_selected_models(new_ids, emit_signal=False)
            self._sync_popups()
        self._refresh_files_view()
        if hasattr(self, "_invalidate_slice_cache"):
            self._invalidate_slice_cache(clear_preview=True)
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
        selected = [self.current_model_id] if self.current_model_id is not None else []
        self.viewer.set_selected_models(selected, emit_signal=False)
        if selected:
            self._select_model_in_panel(selected)
        else:
            self.model_panel.list_widget.clearSelection()
        if len(model_ids) == 1:
            self.statusBar().showMessage("Model removed")
        else:
            self.statusBar().showMessage(f"Removed {len(model_ids)} models")
        self._sync_popups()
        self._push_undo_state()
        self._clear_preview()
        self._refresh_files_view()

    def _select_model_in_panel(self, model_ids):
        if model_ids is None:
            ids = []
        elif isinstance(model_ids, (list, tuple, set)):
            ids = list(model_ids)
        else:
            ids = [model_ids]
        lw = self.model_panel.list_widget
        block = lw.blockSignals(True)
        try:
            lw.clearSelection()
            current_set = set(ids)
            for row in range(lw.count()):
                item = lw.item(row)
                if item is None:
                    continue
                mid = item.data(QtCore.Qt.UserRole)
                if mid in current_set:
                    item.setSelected(True)
                    if mid == (ids[0] if ids else None):
                        lw.setCurrentItem(item)
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
        if isinstance(scale, (int, float, np.floating)):
            val = float(scale)
        else:
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
        if hasattr(self, "_invalidate_slice_cache"):
            self._invalidate_slice_cache(clear_preview=True)

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
        self._refresh_files_view()
        if hasattr(self, "_invalidate_slice_cache"):
            self._invalidate_slice_cache(clear_preview=True)

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
        self.viewer.set_selected_models([], emit_signal=False)
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

    def _toggle_wireframe(self, checked: bool):
        enabled = bool(checked)
        if hasattr(self.viewer, "set_wireframe_enabled"):
            self.viewer.set_wireframe_enabled(enabled)
        state = "on" if enabled else "off"
        self.statusBar().showMessage(f"Wireframe {state}")

    def _show_3dconnexion_dialog(self):
        url = "https://3dconnexion.com/us/drivers/"
        reply = QtWidgets.QMessageBox.question(
            self.main,
            "3Dconnexion",
            "3Dconnexion devices use the system driver.\n"
            "Open the driver download page?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def _toggle_overhang(self, checked: bool):
        try:
            settings = self.settings_panel.to_settings()
            angle = float(getattr(settings, "overhang_angle", 45.0))
        except Exception:
            angle = SliceSettings().overhang_angle
        if hasattr(self.viewer, "set_overhang_visible"):
            self.viewer.set_overhang_visible(bool(checked), angle=angle)
        state = "on" if checked else "off"
        self.statusBar().showMessage(f"Overhang view {state}")

    def _open_config_folder(self):
        path = self._app_config_dir()
        os.makedirs(path, exist_ok=True)
        self._open_path(path, "Configuration Folder")

    def _check_for_updates(self):
        url = "https://github.com/Electrovian/Project-EON-OpenSlicer/releases"
        self._open_url(url, "Updates")

    def _open_log_view(self):
        if hasattr(self.main, "activity_logger") and self.main.activity_logger is not None:
            path = self.main.activity_logger.log_dir
        else:
            path = os.path.join(self._project_root(), "logs")
        os.makedirs(path, exist_ok=True)
        self._open_path(path, "Logs")

    def _open_user_guide(self):
        base_dir = self._project_root()
        candidates = [
            os.path.join(base_dir, "README.md"),
            os.path.join(base_dir, "Mobile", "MOBILE_DEPLOYMENT.md"),
        ]
        self._open_first_existing(candidates, "User Guide")

    def _open_user_course(self):
        base_dir = self._project_root()
        candidates = [
            os.path.join(base_dir, "Research", "Read.me"),
            os.path.join(base_dir, "README.md"),
        ]
        self._open_first_existing(candidates, "User Course")

    def _open_about_dialog(self):
        version = self._read_version()
        if not version:
            version = "0.0.0"
        QtWidgets.QMessageBox.information(
            self.main,
            "About EON-OpenSlicer",
            f"EON-OpenSlicer\nVersion {version}\n\n"
            "A centralized 3D printing lab management system.",
        )

    def _open_calibration_tutorial(self):
        self._open_user_guide()

    def _calibrate_temperature(self):
        fields = [
            {"key": "start_temp", "label": "Start temp (C)", "value": 220, "min": 120, "max": 320, "step": 5, "decimals": 0},
            {"key": "end_temp", "label": "End temp (C)", "value": 190, "min": 120, "max": 320, "step": 5, "decimals": 0},
            {"key": "step", "label": "Step (C)", "value": -5, "min": -30, "max": 30, "step": 1, "decimals": 0},
            {"key": "block_height", "label": "Block height (mm)", "value": 5.0, "min": 1.0, "max": 30.0, "step": 0.5, "decimals": 1},
            {"key": "tower_size", "label": "Tower size (mm)", "value": 20.0, "min": 5.0, "max": 60.0, "step": 1.0, "decimals": 1},
        ]
        params = self._prompt_calibration_params("Temperature Tower", fields)
        if params is None:
            return
        settings = self.settings_panel.to_settings()
        gcode = generate_temperature_tower(
            settings,
            params["start_temp"],
            params["end_temp"],
            params["step"],
            params["block_height"],
            params["tower_size"],
        )
        self._write_calibration_gcode("temperature_tower.gcode", gcode, settings)

    def _calibrate_flow_rate(self):
        fields = [
            {"key": "start_percent", "label": "Start flow (%)", "value": 90, "min": 50, "max": 150, "step": 1, "decimals": 0},
            {"key": "end_percent", "label": "End flow (%)", "value": 110, "min": 50, "max": 150, "step": 1, "decimals": 0},
            {"key": "step", "label": "Step (%)", "value": 5, "min": 1, "max": 20, "step": 1, "decimals": 0},
            {"key": "block_height", "label": "Block height (mm)", "value": 2.0, "min": 0.4, "max": 10.0, "step": 0.2, "decimals": 1},
            {"key": "square_size", "label": "Square size (mm)", "value": 20.0, "min": 5.0, "max": 60.0, "step": 1.0, "decimals": 1},
        ]
        params = self._prompt_calibration_params("Flow Rate Test", fields)
        if params is None:
            return
        settings = self.settings_panel.to_settings()
        gcode = generate_flow_rate_test(
            settings,
            params["start_percent"],
            params["end_percent"],
            params["step"],
            params["block_height"],
            params["square_size"],
        )
        self._write_calibration_gcode("flow_rate_test.gcode", gcode, settings)

    def _calibrate_pressure_advance(self):
        fields = [
            {"key": "start_value", "label": "Start value", "value": 0.0, "min": 0.0, "max": 1.0, "step": 0.01, "decimals": 3},
            {"key": "end_value", "label": "End value", "value": 0.2, "min": 0.0, "max": 1.0, "step": 0.01, "decimals": 3},
            {"key": "step", "label": "Step", "value": 0.02, "min": 0.005, "max": 0.2, "step": 0.005, "decimals": 3},
            {"key": "line_length", "label": "Line length (mm)", "value": 80.0, "min": 20.0, "max": 200.0, "step": 5.0, "decimals": 1},
            {"key": "line_count", "label": "Line count", "value": 5, "min": 1, "max": 20, "step": 1, "decimals": 0},
            {"key": "spacing", "label": "Spacing (mm)", "value": 5.0, "min": 1.0, "max": 20.0, "step": 1.0, "decimals": 1},
        ]
        params = self._prompt_calibration_params("Pressure Advance", fields)
        if params is None:
            return
        settings = self.settings_panel.to_settings()
        gcode = generate_pressure_advance_pattern(
            settings,
            params["start_value"],
            params["end_value"],
            params["step"],
            params["line_length"],
            int(params["line_count"]),
            params["spacing"],
        )
        self._write_calibration_gcode("pressure_advance.gcode", gcode, settings)

    def _calibrate_retraction(self):
        fields = [
            {"key": "start_distance", "label": "Start distance (mm)", "value": 0.4, "min": 0.0, "max": 10.0, "step": 0.1, "decimals": 2},
            {"key": "end_distance", "label": "End distance (mm)", "value": 2.0, "min": 0.0, "max": 10.0, "step": 0.1, "decimals": 2},
            {"key": "step", "label": "Step (mm)", "value": 0.2, "min": 0.05, "max": 2.0, "step": 0.05, "decimals": 2},
            {"key": "block_height", "label": "Block height (mm)", "value": 5.0, "min": 1.0, "max": 30.0, "step": 0.5, "decimals": 1},
            {"key": "tower_size", "label": "Tower size (mm)", "value": 20.0, "min": 5.0, "max": 60.0, "step": 1.0, "decimals": 1},
        ]
        params = self._prompt_calibration_params("Retraction Test", fields)
        if params is None:
            return
        settings = self.settings_panel.to_settings()
        gcode = generate_retraction_tower(
            settings,
            params["start_distance"],
            params["end_distance"],
            params["step"],
            params["block_height"],
            params["tower_size"],
        )
        self._write_calibration_gcode("retraction_tower.gcode", gcode, settings)

    def _calibrate_tolerance(self):
        fields = [
            {"key": "sizes", "label": "Sizes (comma-separated mm)", "value": "5, 10, 15", "type": "text"},
            {"key": "spacing", "label": "Spacing (mm)", "value": 5.0, "min": 1.0, "max": 30.0, "step": 1.0, "decimals": 1},
        ]
        params = self._prompt_calibration_params("Tolerance Test", fields)
        if params is None:
            return
        try:
            sizes = [float(val.strip()) for val in str(params["sizes"]).split(",") if val.strip()]
        except Exception:
            QtWidgets.QMessageBox.warning(self.main, "Tolerance Test", "Invalid sizes list.")
            return
        if not sizes:
            QtWidgets.QMessageBox.warning(self.main, "Tolerance Test", "Enter at least one size.")
            return
        settings = self.settings_panel.to_settings()
        gcode = generate_tolerance_test(settings, sizes, params["spacing"])
        self._write_calibration_gcode("tolerance_test.gcode", gcode, settings)

    def _calibrate_max_flowrate(self):
        fields = [
            {"key": "start_speed", "label": "Start speed (mm/s)", "value": 30, "min": 5, "max": 300, "step": 5, "decimals": 0},
            {"key": "end_speed", "label": "End speed (mm/s)", "value": 120, "min": 5, "max": 300, "step": 5, "decimals": 0},
            {"key": "step", "label": "Step (mm/s)", "value": 10, "min": 1, "max": 100, "step": 1, "decimals": 0},
            {"key": "line_length", "label": "Line length (mm)", "value": 80.0, "min": 20.0, "max": 200.0, "step": 5.0, "decimals": 1},
            {"key": "line_count", "label": "Line count", "value": 5, "min": 1, "max": 20, "step": 1, "decimals": 0},
            {"key": "spacing", "label": "Spacing (mm)", "value": 5.0, "min": 1.0, "max": 20.0, "step": 1.0, "decimals": 1},
        ]
        params = self._prompt_calibration_params("Max Flowrate Test", fields)
        if params is None:
            return
        settings = self.settings_panel.to_settings()
        gcode = generate_max_flowrate_test(
            settings,
            params["start_speed"],
            params["end_speed"],
            params["step"],
            params["line_length"],
            int(params["line_count"]),
            params["spacing"],
        )
        self._write_calibration_gcode("max_flowrate_test.gcode", gcode, settings)

    def _prompt_calibration_params(self, title: str, fields: list[dict]):
        dlg = QtWidgets.QDialog(self.main)
        dlg.setWindowTitle(title)
        dlg.setModal(True)
        layout = QtWidgets.QVBoxLayout(dlg)
        form = QtWidgets.QFormLayout()
        layout.addLayout(form)

        widgets = {}
        for field in fields:
            key = field.get("key")
            label = field.get("label", key)
            field_type = field.get("type", "float")
            if field_type == "text":
                widget = QtWidgets.QLineEdit(dlg)
                widget.setText(str(field.get("value", "")))
            else:
                if field.get("decimals", 0) == 0:
                    widget = QtWidgets.QSpinBox(dlg)
                    widget.setRange(int(field.get("min", 0)), int(field.get("max", 9999)))
                    widget.setSingleStep(int(field.get("step", 1)))
                    widget.setValue(int(field.get("value", 0)))
                else:
                    widget = QtWidgets.QDoubleSpinBox(dlg)
                    widget.setDecimals(int(field.get("decimals", 2)))
                    widget.setRange(float(field.get("min", -9999)), float(field.get("max", 9999)))
                    widget.setSingleStep(float(field.get("step", 1.0)))
                    widget.setValue(float(field.get("value", 0.0)))
            form.addRow(QtWidgets.QLabel(str(label)), widget)
            widgets[key] = widget

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, parent=dlg
        )
        layout.addWidget(buttons)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)

        if dlg.exec_() != QtWidgets.QDialog.Accepted:
            return None
        values = {}
        for field in fields:
            key = field.get("key")
            widget = widgets.get(key)
            if widget is None:
                continue
            if isinstance(widget, QtWidgets.QLineEdit):
                values[key] = widget.text().strip()
            else:
                values[key] = widget.value()
        return values

    def _write_calibration_gcode(self, filename: str, gcode: str, settings: SliceSettings):
        suggested_dir = os.getcwd()
        if self._last_gcode_path:
            suggested_dir = os.path.dirname(self._last_gcode_path)
        suggested = os.path.join(suggested_dir, filename)
        out_path, _ = self._safe_get_save_file_name(
            "Save Calibration G-code",
            suggested,
            "G-code files (*.gcode);;All files (*.*)",
        )
        if not out_path:
            return
        if not out_path.lower().endswith(".gcode"):
            out_path = f"{out_path}.gcode"
        try:
            with open(out_path, "w", encoding="utf-8") as handle:
                handle.write(gcode)
        except Exception as exc:
            QtWidgets.QMessageBox.critical(self.main, "Calibration", f"Failed to write gcode:\n{exc}")
            return
        self._last_gcode_path = out_path
        if hasattr(self, "_analyze_gcode") and hasattr(self, "_update_preview_from_gcode"):
            stats = self._analyze_gcode(out_path, settings)
            self._update_preview_from_gcode(out_path, stats)
            self._activate_mode("preview")
        self.statusBar().showMessage(f"Saved calibration G-code to {out_path}")

    def _open_url(self, url: str, title: str):
        ok = QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
        if not ok:
            QtWidgets.QMessageBox.warning(self.main, title, f"Unable to open:\n{url}")

    def _open_path(self, path: str, title: str):
        ok = QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(path))
        if not ok:
            QtWidgets.QMessageBox.warning(self.main, title, f"Unable to open:\n{path}")

    def _open_first_existing(self, paths: list[str], title: str):
        for path in paths:
            if os.path.exists(path):
                return self._open_path(os.path.abspath(path), title)
        QtWidgets.QMessageBox.warning(self.main, title, "No documentation found.")

    def _app_config_dir(self) -> str:
        base = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.AppConfigLocation)
        if not base:
            base = os.path.join(os.path.expanduser("~"), ".eon_openslicer")
        return os.path.join(base, "EON-OpenSlicer")

    def _project_root(self) -> str:
        here = os.path.abspath(__file__)
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(here))))

    def _read_version(self) -> str | None:
        init_path = os.path.join(self._project_root(), "App", "__init__.py")
        if not os.path.exists(init_path):
            return None
        try:
            with open(init_path, "r", encoding="utf-8") as handle:
                for line in handle:
                    if line.strip().startswith("__version__"):
                        parts = line.split("=", 1)
                        if len(parts) > 1:
                            return parts[1].strip().strip("\"' ")
        except Exception:
            return None
        return None

    def _reset_window_layout(self):
        if hasattr(self, "_model_dock"):
            self._model_dock.show()
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self._model_dock)
        if hasattr(self, "_settings_dock"):
            self._settings_dock.show()
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self._settings_dock)
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
        dlg.setMinimumDuration(0)
        dlg.setLayoutDirection(QtCore.Qt.LeftToRight)
        dlg.setWindowFlags(dlg.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        return dlg

    def _loading_dialog(self, filename: str):
        dlg = QtWidgets.QProgressDialog(self.main)
        dlg.setWindowTitle("Loading...")
        dlg.setLabelText(f"Loading file: {filename}")
        dlg.setCancelButtonText("Cancel")
        dlg.setWindowModality(QtCore.Qt.ApplicationModal)
        dlg.setAutoClose(False)
        dlg.setAutoReset(False)
        dlg.setRange(0, 100)
        dlg.setValue(0)
        dlg.setMinimumDuration(0)
        dlg.setLayoutDirection(QtCore.Qt.LeftToRight)
        dlg.setWindowFlags(dlg.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
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
