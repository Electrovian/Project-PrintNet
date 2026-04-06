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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TYPE_CHECKING

import numpy as np
import trimesh
from PyQt5 import QtCore, QtGui, QtWidgets

from ...i18n import tr
from ...theme import export_theme, get_theme_name, register_theme, set_theme
from ...workers import Worker
from config.bootstrap import user_cache_dir
from config.defaults import DEFAULTS
from config.printer_profile_lookup import resolve_printer_plate_config
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


_FILES_VIEW_CACHE_VERSION = 1


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _files_view_cache_path() -> Path:
    return user_cache_dir().joinpath("files_view_cache.json")


def _normalize_files_view_model(value: object) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    identifier = value.get("id")
    try:
        identifier = int(identifier)
    except (TypeError, ValueError):
        identifier = str(identifier or "").strip()
    return {
        "id": identifier,
        "name": str(value.get("name", "")).strip(),
        "path": str(value.get("path", "")).strip(),
        "plate": str(value.get("plate", "")).strip(),
    }


def _load_files_view_cache(path: Path | None = None) -> dict[str, Any]:
    cache_path = path or _files_view_cache_path()
    try:
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
    except Exception:
        return {"available": False, "models": []}
    if not isinstance(payload, dict):
        return {"available": False, "models": []}
    if payload.get("version") != _FILES_VIEW_CACHE_VERSION:
        return {"available": False, "models": []}
    raw_models = payload.get("models")
    if not isinstance(raw_models, list):
        return {"available": False, "models": []}
    models: list[dict[str, Any]] = []
    for item in raw_models:
        normalized = _normalize_files_view_model(item)
        if normalized is not None:
            models.append(normalized)
    return {"available": True, "models": models}


def _save_files_view_cache(models: list[dict[str, Any]], path: Path | None = None) -> None:
    cache_path = path or _files_view_cache_path()
    normalized_models: list[dict[str, Any]] = []
    for item in list(models or []):
        normalized = _normalize_files_view_model(item)
        if normalized is not None:
            normalized_models.append(normalized)
    payload = {
        "version": _FILES_VIEW_CACHE_VERSION,
        "saved_at_utc": _utc_now_iso(),
        "models": normalized_models,
    }
    try:
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = cache_path.with_suffix(cache_path.suffix + ".tmp")
        temp_path.write_text(json.dumps(payload, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
        temp_path.replace(cache_path)
    except Exception:
        return


class UiMixin(UiMixinBase):
    def __getattr__(self, name: str) -> Any:
        # MainController owns the runtime __getattr__ proxy; this keeps type checkers quiet.
        raise AttributeError(name)

    def _dialog_parent(self):
        parent = getattr(self, "main", None)
        return parent if isinstance(parent, QtWidgets.QWidget) else None

    def _panel_item_model_id(self, item) -> int | None:
        if item is None:
            return None
        value = None
        try:
            value = item.data(0, QtCore.Qt.UserRole + 1)
        except TypeError:
            try:
                value = item.data(QtCore.Qt.UserRole)
            except TypeError:
                value = None
        if value is None:
            try:
                value = item.data(QtCore.Qt.UserRole)
            except TypeError:
                value = None
        if value is None:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

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
        # Legacy WinForms dialog is opt-in. Native Qt dialog stays default.
        default_flag = "0"
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
        try:
            path, selected_filter = QtWidgets.QFileDialog.getOpenFileName(
                self._dialog_parent(),
                caption,
                directory,
                file_filter,
                options=self._qt_file_dialog_options(),
            )
            return str(path or ""), str(selected_filter or "")
        except Exception:
            pass
        ps_path = self._ps_open_file_name(caption, directory, file_filter)
        if ps_path is not None:
            return str(ps_path), str(file_filter or "")
        tk_path = self._tk_open_file_name(caption, directory, file_filter)
        if tk_path is not None:
            return tk_path, str(file_filter or "")
        return "", str(file_filter or "")

    def _safe_get_open_file_names(
        self,
        caption: str,
        directory: str,
        file_filter: str,
    ) -> tuple[list[str], str]:
        try:
            paths, selected_filter = QtWidgets.QFileDialog.getOpenFileNames(
                self._dialog_parent(),
                caption,
                directory,
                file_filter,
                options=self._qt_file_dialog_options(),
            )
            return [str(path) for path in (paths or [])], str(selected_filter or "")
        except Exception:
            pass
        ps_paths = self._ps_open_file_names(caption, directory, file_filter)
        if ps_paths is not None:
            return [str(path) for path in ps_paths], str(file_filter or "")
        tk_paths = self._tk_open_file_names(caption, directory, file_filter)
        if tk_paths is not None:
            return tk_paths, str(file_filter or "")
        return [], str(file_filter or "")

    def _safe_get_save_file_name(
        self,
        caption: str,
        directory: str,
        file_filter: str,
    ) -> tuple[str, str]:
        try:
            path, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
                self._dialog_parent(),
                caption,
                directory,
                file_filter,
                options=self._qt_file_dialog_options(),
            )
            return str(path or ""), str(selected_filter or "")
        except Exception:
            pass
        ps_path = self._ps_save_file_name(caption, directory, file_filter)
        if ps_path is not None:
            return str(ps_path), str(file_filter or "")
        tk_path = self._tk_save_file_name(caption, directory, file_filter)
        if tk_path is not None:
            return tk_path, str(file_filter or "")
        return "", str(file_filter or "")

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
        self._update_prepare_action_state()

    def _on_model_selection_changed(self, model_ids: list):
        ids = [int(mid) for mid in model_ids] if model_ids else []
        if not ids:
            self.current_model_id = None
            self.viewer.set_selected_models([], emit_signal=False)
            self.statusBar().showMessage("Selection cleared")
            self._sync_popups()
            self._update_prepare_action_state()
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
        self._update_prepare_action_state()

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
            model_id = self.viewer.add_scene_object(
                f"{name} Copy {idx + 1}",
                payload.get("path", ""),
                payload.get("parts", []),
                plate_id=payload.get("plate_id"),
                object_metadata=dict(payload.get("object_metadata") or {}),
                instance_metadata=dict(payload.get("instance_metadata") or {}),
            )
            self.viewer.set_model_transform(
                model_id,
                scale=payload["scale"],
                rotation_xyz=payload["rotation"],
                offset_xyz=offset,
            )
            new_ids.append(model_id)

        if new_ids:
            if hasattr(self.model_panel, "refresh_from_viewer"):
                self.model_panel.refresh_from_viewer(self.viewer)
            self.current_model_id = new_ids[-1]
            self.viewer.set_selected_model(self.current_model_id)
            self._select_model_in_panel(self.current_model_id)
            self._sync_popups()
            self._update_bed_warnings()
            self._push_undo_state()
            self._refresh_files_view()

    def _clear_all_models(self):
        model_ids = self.viewer.get_all_model_ids() if hasattr(self.viewer, "get_all_model_ids") else self.viewer.get_model_ids()
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

    def _on_viewer_scene_changed(self):
        if hasattr(self.model_panel, "refresh_from_viewer"):
            self.model_panel.refresh_from_viewer(self.viewer)
        self._refresh_files_view(prefer_cache=False)
        self._update_prepare_action_state()
        if hasattr(self, "_invalidate_slice_cache"):
            self._invalidate_slice_cache(clear_preview=False)
        measure_payload = getattr(getattr(self.viewer, "scene_state", None), "tool_state", None)
        measure_data = getattr(measure_payload, "measure_payload", {}) if measure_payload is not None else {}
        points = list(dict(measure_data or {}).get("points", []) or [])
        if len(points) >= 2:
            distance = float(dict(measure_data or {}).get("distance_mm", 0.0) or 0.0)
            delta = list(dict(measure_data or {}).get("delta_xyz_mm", []) or [])
            if len(delta) == 3:
                self.statusBar().showMessage(
                    f"Measure: {distance:.2f} mm  (dX {float(delta[0]):.2f}, dY {float(delta[1]):.2f}, dZ {float(delta[2]):.2f})"
                )

    def _update_prepare_action_state(self):
        toolbar = getattr(self, "transform_toolbar", None)
        if toolbar is None or not hasattr(toolbar, "set_action_enabled"):
            return
        all_ids = self.viewer.get_all_model_ids() if hasattr(self.viewer, "get_all_model_ids") else self.viewer.get_model_ids()
        plate_ids = self.viewer.get_model_ids()
        selected_ids = self._selected_model_ids()
        has_any = bool(all_ids)
        has_plate = bool(plate_ids)
        has_selection = bool(selected_ids or self.current_model_id is not None)
        selection_count = len(selected_ids) if selected_ids else (1 if self.current_model_id is not None else 0)
        enabled_map = {
            "add_plate": True,
            "add_model": True,
            "auto_orient": has_plate,
            "arrange": has_plate,
            "add_instance": has_selection,
            "remove_instance": has_selection,
            "split_objects": has_selection,
            "split_parts": has_selection,
            "variable_layer": has_selection,
            "move": has_selection,
            "rotate": has_selection,
            "scale": has_selection,
            "lay_on_face": has_selection,
            "cut": has_selection,
            "mesh_boolean": selection_count >= 2,
            "support_paint": has_selection,
            "seam_paint": has_selection,
            "fuzzy_paint": has_selection,
            "emboss": has_selection,
            "measure": has_any,
            "brim_ears": has_selection,
            "assembly_view": has_any,
        }
        for action_id, enabled in enabled_map.items():
            toolbar.set_action_enabled(action_id, enabled)

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
                item_model_id = self._panel_item_model_id(item)
                if item_model_id in ids:
                    item.setSelected(True)
                    if item_model_id == self.current_model_id:
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
        self._update_prepare_action_state()

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

    def _effective_bed_limits(self) -> tuple[tuple[float, float], float, str]:
        state = self.__dict__.get("runtime_printer_state")
        if isinstance(state, RuntimePrinterState):
            return (
                (float(state.bed_x), float(state.bed_y)),
                float(state.bed_z),
                str(state.name),
            )

        fallback = runtime_printer_state_from_defaults(DEFAULTS.get("printer", {}))
        self.runtime_printer_state = fallback
        return (
            (float(fallback.bed_x), float(fallback.bed_y)),
            float(fallback.bed_z),
            str(fallback.name),
        )

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
        resolved_plate = resolve_printer_plate_config(printer)
        bed_x = float(resolved_plate.get("bed_x") or self.runtime_printer_state.bed_x)
        bed_y = float(resolved_plate.get("bed_y") or self.runtime_printer_state.bed_y)
        bed_z = float(resolved_plate.get("bed_z") or self.runtime_printer_state.bed_z)
        self.runtime_printer_state = RuntimePrinterState(
            name=self.runtime_printer_state.name,
            bed_x=bed_x,
            bed_y=bed_y,
            bed_z=bed_z,
            source=source or "runtime",
        )

        main = self.__dict__.get("main")
        viewer = self.__dict__.get("viewer")
        if viewer is None and main is not None:
            viewer = main.__dict__.get("viewer")
        if viewer is not None and hasattr(viewer, "set_bed_limits"):
            viewer.set_bed_limits((bed_x, bed_y), bed_z)
        if viewer is not None and hasattr(viewer, "set_bed_visuals"):
            viewer.set_bed_visuals(
                texture_path=str(resolved_plate.get("bed_texture_path", "") or ""),
                model_path=str(resolved_plate.get("bed_model_path", "") or ""),
            )
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
    def _set_prepare_tool(self, tool_id: str, status_message: str | None = None):
        if hasattr(self.viewer, "set_prepare_tool"):
            self.viewer.set_prepare_tool(tool_id)
        if hasattr(self, "transform_toolbar") and hasattr(self.transform_toolbar, "set_active_tool"):
            self.transform_toolbar.set_active_tool(tool_id)
        if status_message:
            self.statusBar().showMessage(status_message)

    def _handle_prepare_action(self, action_id: str):
        action = str(action_id or "").strip()
        if not action:
            return
        if action == "add_model":
            self.open_stl_dialog()
            return
        if action == "add_plate":
            plate_id = self.viewer.add_plate() if hasattr(self.viewer, "add_plate") else None
            if plate_id is not None:
                if hasattr(self.model_panel, "refresh_from_viewer"):
                    self.model_panel.refresh_from_viewer(self.viewer)
                self.statusBar().showMessage(f"Added plate {int(plate_id):02d}")
                self._push_undo_state()
            return
        if action == "auto_orient":
            self._on_auto_orient_tool()
            return
        if action == "arrange":
            self._on_arrange_tool()
            return
        if action == "add_instance":
            self._add_instance_for_selection()
            return
        if action == "remove_instance":
            model_ids = self._selected_model_ids()
            if not model_ids and self.current_model_id is not None:
                model_ids = [self.current_model_id]
            self._remove_models(model_ids)
            return
        if action == "split_objects":
            self._split_selected_to_objects()
            return
        if action == "split_parts":
            self._split_selected_to_parts()
            return
        if action == "variable_layer":
            self._open_variable_layer_dialog()
            return
        if action == "move":
            self._on_move_tool()
            return
        if action == "rotate":
            self._on_rotate_tool()
            return
        if action == "scale":
            self._on_scale_tool()
            return
        if action == "lay_on_face":
            self._lay_on_face()
            return
        if action == "cut":
            self._open_cut_dialog()
            return
        if action == "mesh_boolean":
            self._open_boolean_dialog()
            return
        if action == "support_paint":
            self._enable_annotation_mode("support_paint", "Support painting: click faces to toggle support regions.")
            return
        if action == "seam_paint":
            self._enable_annotation_mode("seam_paint", "Seam painting: click faces to mark preferred seam regions.")
            return
        if action == "fuzzy_paint":
            self._enable_annotation_mode("fuzzy_paint", "Fuzzy skin painting: click faces to mark fuzzy regions.")
            return
        if action == "emboss":
            self._open_emboss_dialog()
            return
        if action == "measure":
            self._enable_measure_mode()
            return
        if action == "brim_ears":
            self._open_brim_ears_dialog()
            return
        if action == "assembly_view":
            self._toggle_assembly_view()
            return

    def _on_move_tool(self):
        self._set_prepare_tool("move")
        self._enable_move_gizmo()
        self._toggle_popup(self._popup_move, self.transform_toolbar.move_action)

    def _on_rotate_tool(self):
        self._set_prepare_tool("rotate")
        self._enable_rotate_gizmo()
        self._toggle_popup(self._popup_rotate, self.transform_toolbar.rotate_action)

    def _on_scale_tool(self):
        self._set_prepare_tool("scale")
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

    def _add_instance_for_selection(self):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self.main, "Add instance", "Select an object first.")
            return
        new_id = self.viewer.add_instance_for_model(self.current_model_id) if hasattr(self.viewer, "add_instance_for_model") else None
        if new_id is None:
            QtWidgets.QMessageBox.warning(self.main, "Add instance", "Unable to create another instance.")
            return
        if hasattr(self.model_panel, "refresh_from_viewer"):
            self.model_panel.refresh_from_viewer(self.viewer)
        self.current_model_id = int(new_id)
        self.viewer.set_selected_model(int(new_id))
        self._select_model_in_panel(int(new_id))
        self._sync_popups()
        self._push_undo_state()

    def _split_selected_to_objects(self):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self.main, "Split", "Select an object first.")
            return
        new_ids = self.viewer.split_model_to_objects(self.current_model_id) if hasattr(self.viewer, "split_model_to_objects") else []
        if not new_ids:
            QtWidgets.QMessageBox.warning(self.main, "Split", "The selected object could not be split into separate objects.")
            return
        if hasattr(self.model_panel, "refresh_from_viewer"):
            self.model_panel.refresh_from_viewer(self.viewer)
        self.current_model_id = int(new_ids[0])
        self.viewer.set_selected_models(new_ids, emit_signal=False)
        self._select_model_in_panel(new_ids)
        self._sync_popups()
        self._push_undo_state()

    def _split_selected_to_parts(self):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self.main, "Split", "Select an object first.")
            return
        ok = self.viewer.split_model_to_parts(self.current_model_id) if hasattr(self.viewer, "split_model_to_parts") else False
        if not ok:
            QtWidgets.QMessageBox.warning(self.main, "Split", "The selected object could not be split into parts.")
            return
        if hasattr(self.model_panel, "refresh_from_viewer"):
            self.model_panel.refresh_from_viewer(self.viewer)
        self._sync_popups()
        self._push_undo_state()

    def _open_variable_layer_dialog(self):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self.main, "Variable layer height", "Select an object first.")
            return
        bounds = self.viewer.get_model_bounds(self.current_model_id)
        if bounds is None:
            QtWidgets.QMessageBox.warning(self.main, "Variable layer height", "Selected object bounds are unavailable.")
            return
        mn, mx = bounds
        dlg = QtWidgets.QDialog(self.main)
        dlg.setWindowTitle("Variable layer height")
        layout = QtWidgets.QFormLayout(dlg)
        z_min_spin = QtWidgets.QDoubleSpinBox(dlg)
        z_min_spin.setRange(float(mn[2]), float(mx[2]))
        z_min_spin.setDecimals(3)
        z_min_spin.setValue(float(mn[2]))
        z_max_spin = QtWidgets.QDoubleSpinBox(dlg)
        z_max_spin.setRange(float(mn[2]), float(mx[2]))
        z_max_spin.setDecimals(3)
        z_max_spin.setValue(float(mx[2]))
        height_spin = QtWidgets.QDoubleSpinBox(dlg)
        height_spin.setRange(0.02, 1.0)
        height_spin.setDecimals(3)
        height_spin.setValue(0.12)
        layout.addRow("Z min (mm)", z_min_spin)
        layout.addRow("Z max (mm)", z_max_spin)
        layout.addRow("Layer height (mm)", height_spin)
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, parent=dlg)
        layout.addRow(buttons)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        if dlg.exec_() != QtWidgets.QDialog.Accepted:
            return
        key = str(int(self.current_model_id))
        tool_state = self.viewer.scene_state.tool_state
        ranges = list(tool_state.adaptive_layer_ranges.get(key, []) or [])
        ranges.append(
            {
                "z_min_mm": float(z_min_spin.value()),
                "z_max_mm": float(z_max_spin.value()),
                "layer_height_mm": float(height_spin.value()),
            }
        )
        tool_state.adaptive_layer_ranges[key] = ranges
        if hasattr(self.viewer, "sceneChanged"):
            self.viewer.sceneChanged.emit()
        self._push_undo_state()

    def _open_cut_dialog(self):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self.main, "Cut", "Select an object first.")
            return
        dlg = QtWidgets.QDialog(self.main)
        dlg.setWindowTitle("Cut")
        layout = QtWidgets.QFormLayout(dlg)
        axis_combo = QtWidgets.QComboBox(dlg)
        axis_combo.addItems(["X", "Y", "Z"])
        position_spin = QtWidgets.QDoubleSpinBox(dlg)
        position_spin.setRange(0.0, 100.0)
        position_spin.setDecimals(1)
        position_spin.setValue(50.0)
        keep_combo = QtWidgets.QComboBox(dlg)
        keep_combo.addItems(["both", "upper", "lower"])
        layout.addRow("Axis", axis_combo)
        layout.addRow("Position (%)", position_spin)
        layout.addRow("Keep", keep_combo)
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, parent=dlg)
        layout.addRow(buttons)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        if dlg.exec_() != QtWidgets.QDialog.Accepted:
            return
        new_ids = self.viewer.cut_model(
            self.current_model_id,
            axis=str(axis_combo.currentText()).strip().lower(),
            position_ratio=float(position_spin.value()) / 100.0,
            keep_mode=str(keep_combo.currentText()).strip().lower(),
        ) if hasattr(self.viewer, "cut_model") else []
        if not new_ids:
            QtWidgets.QMessageBox.warning(self.main, "Cut", "The cut operation failed.")
            return
        if hasattr(self.model_panel, "refresh_from_viewer"):
            self.model_panel.refresh_from_viewer(self.viewer)
        self.current_model_id = int(new_ids[0])
        self.viewer.set_selected_models(new_ids, emit_signal=False)
        self._select_model_in_panel(new_ids)
        self._push_undo_state()

    def _open_boolean_dialog(self):
        model_ids = self._selected_model_ids()
        if len(model_ids) < 2:
            QtWidgets.QMessageBox.warning(self.main, "Mesh Boolean", "Select at least two objects on the same plate.")
            return
        operation, ok = QtWidgets.QInputDialog.getItem(
            self.main,
            "Mesh Boolean",
            "Operation",
            ["union", "difference", "intersection"],
            0,
            False,
        )
        if not ok:
            return
        new_id = self.viewer.boolean_models(model_ids, operation=str(operation or "union")) if hasattr(self.viewer, "boolean_models") else None
        if new_id is None:
            QtWidgets.QMessageBox.warning(self.main, "Mesh Boolean", "The boolean operation failed.")
            return
        if hasattr(self.model_panel, "refresh_from_viewer"):
            self.model_panel.refresh_from_viewer(self.viewer)
        self.current_model_id = int(new_id)
        self.viewer.set_selected_model(int(new_id))
        self._select_model_in_panel(int(new_id))
        self._push_undo_state()

    def _enable_annotation_mode(self, tool_id: str, status_message: str):
        self._hide_all_popups()
        self._set_prepare_tool(tool_id, status_message)

    def _enable_measure_mode(self):
        if hasattr(self.viewer, "scene_state"):
            self.viewer.scene_state.tool_state.measure_payload = {"points": []}
        self._hide_all_popups()
        self._set_prepare_tool("measure", "Measure: click two surface points to inspect distance and XYZ delta.")
        if hasattr(self.viewer, "sceneChanged"):
            self.viewer.sceneChanged.emit()

    def _open_emboss_dialog(self):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self.main, "Emboss", "Select an object first.")
            return
        text, ok = QtWidgets.QInputDialog.getText(self.main, "Emboss", "Text", text="Embossed text")
        if not ok or not str(text or "").strip():
            return
        bounds = self.viewer.get_model_bounds(self.current_model_id)
        if bounds is None:
            QtWidgets.QMessageBox.warning(self.main, "Emboss", "Selected object bounds are unavailable.")
            return
        mn, mx = bounds
        depth, ok = QtWidgets.QInputDialog.getDouble(self.main, "Emboss", "Depth (mm)", value=1.0, min=0.2, max=10.0, decimals=2)
        if not ok:
            return
        operation, ok = QtWidgets.QInputDialog.getItem(self.main, "Emboss", "Operation", ["join", "cut"], 0, False)
        if not ok:
            return
        width = max(8.0, min(float(mx[0] - mn[0]) * 0.75, 80.0))
        height = max(4.0, min(float(mx[1] - mn[1]) * 0.18, 20.0))
        box = trimesh.creation.box(extents=(width, height, float(depth)))
        center = np.array(
            [
                float((mn[0] + mx[0]) * 0.5),
                float((mn[1] + mx[1]) * 0.5),
                float(mx[2] - (depth * 0.5 if str(operation).strip().lower() == "cut" else 0.0)),
            ],
            dtype=float,
        )
        box.apply_translation(center)
        plate_id = int(self.viewer.models.get(self.current_model_id, {}).get("plate_id", self.viewer.get_current_plate_id()))
        plate_origin = np.asarray(self.viewer._plate_origin(plate_id), dtype=float)
        emboss_id = self.viewer.add_scene_object(
            str(text).strip(),
            "",
            [
                {
                    "name": str(text).strip(),
                    "vertices": np.asarray(box.vertices, dtype=float) - plate_origin,
                    "faces": np.asarray(box.faces, dtype=int),
                    "metadata": {"emboss_text": str(text).strip(), "operation": str(operation).strip().lower()},
                }
            ],
            plate_id=plate_id,
            object_metadata={"emboss_text": str(text).strip(), "operation": str(operation).strip().lower()},
        )
        self.viewer.scene_state.tool_state.emboss_payloads[str(int(emboss_id))] = [
            {"text": str(text).strip(), "depth": float(depth), "operation": str(operation).strip().lower()}
        ]
        result_id = emboss_id
        if str(operation).strip().lower() == "cut":
            boolean_id = self.viewer.boolean_models([self.current_model_id, emboss_id], operation="difference")
            if boolean_id is not None:
                result_id = int(boolean_id)
        if hasattr(self.model_panel, "refresh_from_viewer"):
            self.model_panel.refresh_from_viewer(self.viewer)
        self.current_model_id = int(result_id)
        self.viewer.set_selected_model(int(result_id))
        self._select_model_in_panel(int(result_id))
        self._push_undo_state()

    def _open_brim_ears_dialog(self):
        if self.current_model_id is None:
            QtWidgets.QMessageBox.warning(self.main, "Brim Ears", "Select an object first.")
            return
        diameter, ok = QtWidgets.QInputDialog.getDouble(self.main, "Brim Ears", "Head diameter (mm)", value=5.0, min=1.0, max=40.0, decimals=2)
        if not ok:
            return
        bounds = self.viewer.get_model_bounds(self.current_model_id)
        if bounds is None:
            QtWidgets.QMessageBox.warning(self.main, "Brim Ears", "Selected object bounds are unavailable.")
            return
        mn, mx = bounds
        points = [
            [float(mn[0]), float(mn[1]), 0.0],
            [float(mx[0]), float(mn[1]), 0.0],
            [float(mx[0]), float(mx[1]), 0.0],
            [float(mn[0]), float(mx[1]), 0.0],
        ]
        annotation = dict(self.viewer.scene_state.tool_state.annotations.get(str(int(self.current_model_id)), {}) or {})
        annotation["brim_ears"] = {"points": points, "head_diameter_mm": float(diameter)}
        self.viewer.scene_state.tool_state.annotations[str(int(self.current_model_id))] = annotation
        if hasattr(self.viewer, "sceneChanged"):
            self.viewer.sceneChanged.emit()
        self.statusBar().showMessage(f"Brim ears staged for {len(points)} points at {float(diameter):.1f} mm.")
        self._push_undo_state()

    def _toggle_assembly_view(self):
        if not hasattr(self.viewer, "scene_state"):
            return
        tool_state = self.viewer.scene_state.tool_state
        enabled = not bool(tool_state.assembly_mode)
        tool_state.assembly_mode = enabled
        if enabled:
            explosion, ok = QtWidgets.QInputDialog.getDouble(
                self.main,
                "Assembly View",
                "Explosion ratio",
                value=1.6,
                min=1.0,
                max=5.0,
                decimals=2,
            )
            if not ok:
                tool_state.assembly_mode = False
                if hasattr(self.transform_toolbar, "set_active_tool"):
                    self.transform_toolbar.set_active_tool("move")
                return
            tool_state.assembly_explosion_ratio = float(explosion)
            selected = self._selected_model_ids() or self.viewer.get_model_ids()
            centers = []
            for model_id in selected:
                bounds = self.viewer.get_model_bounds(model_id)
                if bounds is None:
                    continue
                mn, mx = bounds
                centers.append(((mn + mx) / 2.0, int(model_id)))
            if centers:
                mean = np.mean([center for center, _mid in centers], axis=0)
                offsets = {}
                for center, model_id in centers:
                    delta = (np.asarray(center, dtype=float) - mean) * max(0.0, float(explosion) - 1.0)
                    offsets[str(int(model_id))] = [float(delta[0]), float(delta[1]), float(delta[2])]
                tool_state.assembly_offsets = offsets
            self._set_prepare_tool("assembly_view", "Assembly view enabled. Trigger Assembly View again to return.")
        else:
            tool_state.assembly_offsets = {}
            self._set_prepare_tool("move", "Assembly view disabled.")
        if hasattr(self.viewer, "sceneChanged"):
            self.viewer.sceneChanged.emit()
        self.viewer.update()

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

    def _on_plate_remove_requested(self):
        if not hasattr(self.viewer, "get_plate_ids") or len(self.viewer.get_plate_ids()) <= 1:
            QtWidgets.QMessageBox.information(
                self.main,
                tr("viewer.plate.remove.title", "Plate"),
                tr(
                    "viewer.plate.remove.single_plate_only",
                    "Single-plate mode is active. The current plate cannot be removed.",
                ),
            )
            return
        removed = self.viewer.delete_current_plate() if hasattr(self.viewer, "delete_current_plate") else False
        if not removed:
            QtWidgets.QMessageBox.warning(self.main, tr("viewer.plate.remove.title", "Plate"), "Unable to remove the current plate.")
            return
        if hasattr(self.model_panel, "refresh_from_viewer"):
            self.model_panel.refresh_from_viewer(self.viewer)
        self._refresh_files_view()
        self._push_undo_state()

    def _on_plate_lock_changed(self, locked: bool):
        if bool(locked):
            self.statusBar().showMessage(
                tr("viewer.plate.locked_status", "Current plate is locked.")
            )
        else:
            self.statusBar().showMessage(
                tr("viewer.plate.unlocked_status", "Current plate is unlocked.")
            )

    def _on_plate_name_changed(self, plate_name: str):
        text = str(plate_name or "").strip() or "01"
        self.statusBar().showMessage(
            tr("viewer.plate.renamed_status", "Plate renamed to {name}.", name=text)
        )
        if hasattr(self, "_invalidate_slice_cache"):
            self._invalidate_slice_cache(clear_preview=False)

    def _set_labels_visible(self, visible: bool):
        self._labels_visible = bool(visible)
        self.viewer.set_labels_visible(self._labels_visible)
        state = "on" if self._labels_visible else "off"
        self.statusBar().showMessage(f"Labels {state}")

    def _on_mode_tab_changed(self, button):
        if button is None:
            return
        mode_key = str(button.property("mode_key") or "").strip().lower()
        if not mode_key:
            mode_key = button.text().strip().lower()
        if mode_key:
            self._activate_mode(mode_key)

    def _activate_mode(self, mode: str):
        mode = (mode or "").strip().lower()
        if not mode:
            return
        mode = {
            "project": "files",
            "calibration": "control",
            "layout": "prepare",
        }.get(mode, mode)
        viewer_visible_mode = mode in {"prepare", "preview"}
        if hasattr(self.viewer, "setUpdatesEnabled"):
            self.viewer.setUpdatesEnabled(bool(viewer_visible_mode))
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
            if hasattr(self.viewer, "set_plate_overlay_visible"):
                self.viewer.set_plate_overlay_visible(True)
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
            if viewer_visible_mode and hasattr(self.viewer, "update"):
                self.viewer.update()
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
            if hasattr(self.viewer, "set_plate_overlay_visible"):
                self.viewer.set_plate_overlay_visible(False)
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
            if viewer_visible_mode and hasattr(self.viewer, "update"):
                self.viewer.update()
            QtCore.QTimer.singleShot(0, self.preview_view.position_panels)
        elif mode == "device":
            self.prepare_view.hide()
            self.preview_view.hide()
            self._central_stack.setCurrentWidget(self.device_view)
            if hasattr(self.viewer, "set_interaction_enabled"):
                self.viewer.set_interaction_enabled(False)
            if hasattr(self.viewer, "set_plate_overlay_visible"):
                self.viewer.set_plate_overlay_visible(False)
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
            if hasattr(self.viewer, "set_plate_overlay_visible"):
                self.viewer.set_plate_overlay_visible(False)
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
            if hasattr(self.viewer, "set_plate_overlay_visible"):
                self.viewer.set_plate_overlay_visible(False)
            if hasattr(self.viewer, "set_preview_visible"):
                self.viewer.set_preview_visible(False)
            if hasattr(self.viewer, "set_models_visible"):
                self.viewer.set_models_visible(False)
            if hasattr(self.viewer, "set_print_stats_visible"):
                self.viewer.set_print_stats_visible(False)
            if hasattr(self.viewer, "set_preview_object_visible"):
                self.viewer.set_preview_object_visible(False)
            self._refresh_files_view(prefer_cache=True)
        elif mode == "activity":
            self.prepare_view.hide()
            self.preview_view.hide()
            self._central_stack.setCurrentWidget(self.activity_view)
            if hasattr(self.viewer, "set_interaction_enabled"):
                self.viewer.set_interaction_enabled(False)
            if hasattr(self.viewer, "set_plate_overlay_visible"):
                self.viewer.set_plate_overlay_visible(False)
            if hasattr(self.viewer, "set_preview_visible"):
                self.viewer.set_preview_visible(False)
            if hasattr(self.viewer, "set_models_visible"):
                self.viewer.set_models_visible(False)
            if hasattr(self.viewer, "set_print_stats_visible"):
                self.viewer.set_print_stats_visible(False)
            if hasattr(self.viewer, "set_preview_object_visible"):
                self.viewer.set_preview_object_visible(False)
            if hasattr(self, "_request_activity_refresh"):
                self._request_activity_refresh(force=True)
        else:
            return
        self._active_mode = mode
        if hasattr(self, "_persist_active_mode"):
            self._persist_active_mode(mode)

    def _resolve_files_view_cache_file(self) -> Path:
        override = getattr(self, "_files_view_cache_file", None)
        if isinstance(override, Path):
            return override
        return _files_view_cache_path()

    def _remember_files_view_models(self, models: list[dict[str, Any]]) -> None:
        _save_files_view_cache(models, self._resolve_files_view_cache_file())

    def _restore_files_view_from_cache(self) -> bool:
        if not hasattr(self, "files_view") or not hasattr(self.files_view, "set_models"):
            return False
        payload = _load_files_view_cache(self._resolve_files_view_cache_file())
        if not bool(payload.get("available", False)):
            return False
        models = [dict(item) for item in payload.get("models", []) if isinstance(item, dict)]
        if not models:
            return False
        self.files_view.set_models(models)
        return True

    def _refresh_files_view(self, prefer_cache: bool = False):
        if not hasattr(self, "files_view"):
            return
        if hasattr(self.files_view, "refresh_from_viewer"):
            self.files_view.refresh_from_viewer(self.viewer)
        models = []
        if hasattr(self.files_view, "models_snapshot"):
            snapshot = self.files_view.models_snapshot()
            if isinstance(snapshot, list):
                models = [dict(item) for item in snapshot if isinstance(item, dict)]
        if models:
            self._remember_files_view_models(models)
            return
        if bool(prefer_cache) and self._restore_files_view_from_cache():
            return
        self._remember_files_view_models([])

    def _auto_slice_prepare(self):
        if not self.viewer.get_model_ids():
            return
        if hasattr(self, "_settings_with_slice_defaults"):
            settings = self._settings_with_slice_defaults()
        else:
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
                mode_key = str(btn.property("mode_key") or "").strip().lower()
                label_key = btn.text().strip().lower()
                if mode_key == "device" or label_key == "device":
                    btn.setChecked(True)
                    break
        self._activate_mode("device")

    def _refresh_printer_views(self):
        manager = getattr(self, "printer_manager", None)
        if manager is None:
            return
        printers = [dict(item) for item in getattr(manager, "printers", []) if isinstance(item, dict)]
        connected = [row for row in printers if not bool(row.get("catalog_only", False))]
        if hasattr(self, "main"):
            self.main.printers = [dict(item) for item in printers]
            self.main.connected_printers = connected
        if hasattr(self, "settings_panel") and hasattr(self.settings_panel, "set_printers"):
            self.settings_panel.set_printers(printers)
        if hasattr(self, "preview_view") and hasattr(self.preview_view, "set_printers"):
            self.preview_view.set_printers(printers)
        if hasattr(self, "device_view"):
            self.device_view.set_printers(connected)
        if hasattr(self, "control_view"):
            self.control_view.set_printers(connected)
        active_printer = getattr(manager, "active_printer", None)
        if isinstance(active_printer, dict):
            self._apply_printer_profile(active_printer, source="refresh")
            return
        state = getattr(self, "runtime_printer_state", None)
        if isinstance(state, RuntimePrinterState):
            self._sync_printer_selection({"name": str(state.name)}, source=None)

    def _run_background_task(
        self,
        *,
        title: str,
        label: str,
        fn,
        args: tuple = (),
        kwargs: dict | None = None,
        on_finished=None,
        on_error=None,
    ):
        dialog = self._busy_dialog(title, label)
        dialog.show()

        worker = Worker(fn, *(args or ()), **(kwargs or {}))

        def _finish(result):
            dialog.close()
            if callable(on_finished):
                on_finished(result)

        def _error(message: str):
            dialog.close()
            if callable(on_error):
                on_error(message)
                return
            QtWidgets.QMessageBox.warning(
                self.main,
                tr("onboarding.error.title", "Add Printer"),
                str(message or tr("onboarding.error.unknown", "Unable to save printer.")),
            )

        worker.signals.finished.connect(_finish)
        worker.signals.error.connect(_error)
        self._start_worker(worker)

    def _submit_onboarding_add_printer(self, manager, printer: dict):
        self._run_background_task(
            title=tr("onboarding.title", "Add Printer"),
            label=tr("onboarding.saving", "Saving printer..."),
            fn=manager.onboarding_add_printer,
            args=(dict(printer or {}),),
            on_finished=lambda result: self._finalize_onboarding_result(
                result,
                success_message=tr("onboarding.saved", "Printer saved."),
            ),
            on_error=lambda message: QtWidgets.QMessageBox.warning(
                self.main,
                tr("onboarding.error.title", "Add Printer"),
                str(message or tr("onboarding.error.unknown", "Unable to save printer.")),
            ),
        )

    def _on_device_add_printer_requested(self):
        manager = getattr(self, "printer_manager", None)
        if manager is None:
            QtWidgets.QMessageBox.warning(
                self.main,
                tr("onboarding.error.title", "Add Printer"),
                tr("onboarding.error.manager_missing", "Printer manager is unavailable."),
            )
            return

        methods = [
            ("wifi", tr("onboarding.method.wifi", "Wi-Fi scan")),
            ("bluetooth", tr("onboarding.method.bluetooth", "Bluetooth pairing")),
            ("manual", tr("onboarding.method.manual", "Manual endpoint")),
        ]
        labels = [label for _key, label in methods]
        selection, ok = QtWidgets.QInputDialog.getItem(
            self.main,
            tr("onboarding.title", "Add Printer"),
            tr("onboarding.prompt.method", "Choose onboarding method:"),
            labels,
            0,
            False,
        )
        if not ok:
            return
        selected_key = methods[labels.index(selection)][0]
        if selected_key == "wifi":
            self._run_wifi_onboarding(manager)
            return
        if selected_key == "bluetooth":
            self._run_bluetooth_onboarding(manager)
            return
        self._run_manual_onboarding(manager)

    def _run_wifi_onboarding(self, manager):
        default_cidr = str(os.environ.get("EON_WIFI_SCAN_CIDR", "192.168.1.0/24")).strip() or "192.168.1.0/24"
        cidr, ok = QtWidgets.QInputDialog.getText(
            self.main,
            tr("onboarding.wifi.title", "Wi-Fi Scan"),
            tr("onboarding.wifi.prompt_cidr", "Enter network CIDR:"),
            text=default_cidr,
        )
        if not ok:
            return
        cidr_value = str(cidr).strip()

        def _on_discovery_finished(report):
            payload = report if isinstance(report, dict) else {}
            if not bool(payload.get("ok", False)):
                QtWidgets.QMessageBox.warning(
                    self.main,
                    tr("onboarding.error.title", "Add Printer"),
                    str(payload.get("message", tr("onboarding.error.unknown", "Wi-Fi scan failed."))),
                )
                return
            discovered = [dict(item) for item in payload.get("printers", []) if isinstance(item, dict)]
            if not discovered:
                QtWidgets.QMessageBox.information(
                    self.main,
                    tr("onboarding.wifi.title", "Wi-Fi Scan"),
                    tr("onboarding.wifi.none_found", "No compatible printers were detected."),
                )
                return
            labels = [str(item.get("name", "Printer")) for item in discovered]
            choice, selected = QtWidgets.QInputDialog.getItem(
                self.main,
                tr("onboarding.wifi.title", "Wi-Fi Scan"),
                tr("onboarding.wifi.select_printer", "Select discovered printer:"),
                labels,
                0,
                False,
            )
            if not selected:
                return
            printer = discovered[labels.index(choice)]
            self._submit_onboarding_add_printer(manager, printer)

        self._run_background_task(
            title=tr("onboarding.wifi.title", "Wi-Fi Scan"),
            label=tr("onboarding.wifi.scanning", "Scanning local network..."),
            fn=manager.discover_local_wifi_printers_from_cidr,
            args=(cidr_value,),
            kwargs={"host_limit": 64, "max_targets": 256},
            on_finished=_on_discovery_finished,
            on_error=lambda message: QtWidgets.QMessageBox.warning(
                self.main,
                tr("onboarding.error.title", "Add Printer"),
                str(message or tr("onboarding.error.unknown", "Wi-Fi scan failed.")),
            ),
        )

    def _run_bluetooth_onboarding(self, manager):
        def _on_discovery_finished(report):
            payload = report if isinstance(report, dict) else {}
            if not bool(payload.get("ok", False)):
                message = str(payload.get("message", tr("onboarding.bluetooth.unavailable", "Bluetooth unavailable.")))
                QtWidgets.QMessageBox.warning(self.main, tr("onboarding.bluetooth.title", "Bluetooth Pairing"), message)
                return
            devices = [dict(item) for item in payload.get("devices", []) if isinstance(item, dict)]
            if not devices:
                QtWidgets.QMessageBox.information(
                    self.main,
                    tr("onboarding.bluetooth.title", "Bluetooth Pairing"),
                    tr("onboarding.bluetooth.none_found", "No Bluetooth devices were discovered."),
                )
                return
            labels = [f"{item.get('name', 'Device')} ({item.get('id', '')})" for item in devices]
            choice, selected = QtWidgets.QInputDialog.getItem(
                self.main,
                tr("onboarding.bluetooth.title", "Bluetooth Pairing"),
                tr("onboarding.bluetooth.select_device", "Select Bluetooth device:"),
                labels,
                0,
                False,
            )
            if not selected:
                return
            device = devices[labels.index(choice)]
            self._run_background_task(
                title=tr("onboarding.bluetooth.title", "Bluetooth Pairing"),
                label=tr("onboarding.bluetooth.pairing", "Pairing device..."),
                fn=manager.pair_bluetooth_printer,
                kwargs={"device_id": str(device.get("id", "")).strip()},
                on_finished=lambda pair_result: (
                    QtWidgets.QMessageBox.information(
                        self.main,
                        tr("onboarding.bluetooth.title", "Bluetooth Pairing"),
                        tr("onboarding.bluetooth.paired", "Device paired successfully."),
                    )
                    if bool((pair_result or {}).get("ok", False))
                    else QtWidgets.QMessageBox.warning(
                        self.main,
                        tr("onboarding.bluetooth.title", "Bluetooth Pairing"),
                        str((pair_result or {}).get("message", tr("onboarding.bluetooth.pair_failed", "Unable to pair device."))),
                    )
                ),
                on_error=lambda message: QtWidgets.QMessageBox.warning(
                    self.main,
                    tr("onboarding.bluetooth.title", "Bluetooth Pairing"),
                    str(message or tr("onboarding.bluetooth.pair_failed", "Unable to pair device.")),
                ),
            )

        self._run_background_task(
            title=tr("onboarding.bluetooth.title", "Bluetooth Pairing"),
            label=tr("onboarding.bluetooth.scanning", "Scanning Bluetooth devices..."),
            fn=manager.discover_bluetooth_printers,
            kwargs={"timeout_s": 6.0},
            on_finished=_on_discovery_finished,
            on_error=lambda message: QtWidgets.QMessageBox.warning(
                self.main,
                tr("onboarding.bluetooth.title", "Bluetooth Pairing"),
                str(message or tr("onboarding.bluetooth.unavailable", "Bluetooth unavailable.")),
            ),
        )

    def _run_manual_onboarding(self, manager):
        name, ok = QtWidgets.QInputDialog.getText(
            self.main,
            tr("onboarding.manual.title", "Manual Printer"),
            tr("onboarding.manual.prompt_name", "Printer name:"),
            text=tr("onboarding.manual.default_name", "Manual Printer"),
        )
        if not ok:
            return
        connector_types = ["octoprint", "moonraker", "prusalink", "bambu_lan", "creality", "local_file"]
        connector, ok = QtWidgets.QInputDialog.getItem(
            self.main,
            tr("onboarding.manual.title", "Manual Printer"),
            tr("onboarding.manual.prompt_connector", "Connector type:"),
            connector_types,
            0,
            False,
        )
        if not ok:
            return
        endpoint, ok = QtWidgets.QInputDialog.getText(
            self.main,
            tr("onboarding.manual.title", "Manual Printer"),
            tr("onboarding.manual.prompt_endpoint", "Endpoint URL:"),
            text="http://",
        )
        if not ok:
            return
        token, _ = QtWidgets.QInputDialog.getText(
            self.main,
            tr("onboarding.manual.title", "Manual Printer"),
            tr("onboarding.manual.prompt_token", "API token (optional):"),
            QtWidgets.QLineEdit.Normal,
            "",
        )
        printer = {
            "name": str(name).strip() or tr("onboarding.manual.default_name", "Manual Printer"),
            "connector_type": str(connector).strip().lower(),
            "endpoint": str(endpoint).strip(),
            "api_key": str(token).strip(),
        }

        def _on_test_done(test_result):
            payload = test_result if isinstance(test_result, dict) else {}
            if not bool(payload.get("ok", False)):
                QtWidgets.QMessageBox.warning(
                    self.main,
                    tr("onboarding.manual.title", "Manual Printer"),
                    str(payload.get("message", tr("onboarding.manual.health_failed", "Health test failed."))),
                )
                return
            self._submit_onboarding_add_printer(manager, printer)

        self._run_background_task(
            title=tr("onboarding.manual.title", "Manual Printer"),
            label=tr("onboarding.manual.testing", "Testing endpoint..."),
            fn=manager.test_manual_endpoint,
            kwargs={
                "connector_type": connector,
                "endpoint": str(endpoint).strip(),
                "name": str(name).strip(),
                "credentials": {"api_key": str(token).strip()},
            },
            on_finished=_on_test_done,
            on_error=lambda message: QtWidgets.QMessageBox.warning(
                self.main,
                tr("onboarding.manual.title", "Manual Printer"),
                str(message or tr("onboarding.manual.health_failed", "Health test failed.")),
            ),
        )

    def _finalize_onboarding_result(self, result, *, success_message: str):
        if not isinstance(result, dict):
            QtWidgets.QMessageBox.warning(
                self.main,
                tr("onboarding.error.title", "Add Printer"),
                tr("onboarding.error.unknown", "Unable to save printer."),
            )
            return
        if not bool(result.get("ok", False)):
            diagnostic = result.get("diagnostic", {})
            if isinstance(diagnostic, dict) and diagnostic.get("message"):
                message = str(diagnostic.get("message"))
            else:
                message = str(result.get("message", tr("onboarding.error.unknown", "Unable to save printer.")))
            QtWidgets.QMessageBox.warning(self.main, tr("onboarding.error.title", "Add Printer"), message)
            return
        self._refresh_printer_views()
        QtWidgets.QMessageBox.information(
            self.main,
            tr("onboarding.title", "Add Printer"),
            success_message,
        )

    def _on_device_diagnostics_requested(self, printer: dict | None):
        manager = getattr(self, "printer_manager", None)
        if manager is None or not isinstance(printer, dict):
            return
        report = manager.run_connection_diagnostics(printer)
        ok = bool(report.get("ok", False))
        message = str(report.get("message", "")).strip()
        if not message and ok:
            message = tr("diagnostics.ok", "Connection diagnostics passed.")
        if not message:
            message = tr("diagnostics.failed", "Connection diagnostics failed.")
        hints = []
        upper = message.upper()
        if "API_KEY_REQUIRED" in upper or "TOKEN_REQUIRED" in upper:
            hints.append(tr("diagnostics.hint.credentials", "Check API token credentials and keychain entries."))
        if "REQUEST_FAILED" in upper or "UNREACHABLE" in upper or "HTTP_" in upper:
            hints.append(tr("diagnostics.hint.network", "Verify network reachability, firewall, and endpoint URL."))
        if "CONNECTOR_UNSUPPORTED" in upper:
            hints.append(tr("diagnostics.hint.connector", "Select a supported connector/protocol."))
        detail_lines = [message]
        for hint in hints:
            detail_lines.append(f"- {hint}")
        detail = "\n".join(detail_lines)
        if ok:
            QtWidgets.QMessageBox.information(self.main, tr("diagnostics.title", "Connection Diagnostics"), detail)
        else:
            QtWidgets.QMessageBox.warning(self.main, tr("diagnostics.title", "Connection Diagnostics"), detail)

    def _on_device_download_installer_requested(self):
        url = "https://github.com/Electrovian/Project-PrintNet/releases/latest"
        reply = QtWidgets.QMessageBox.question(
            self.main,
            tr("installer.download.title", "Download Installer"),
            tr("installer.download.prompt", "Open installer download page in your browser?"),
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if reply != QtWidgets.QMessageBox.Yes:
            return
        self._open_url(url, tr("installer.download.title", "Download Installer"))

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
        model_id = self._panel_item_model_id(item)
        self.current_model_id = model_id
        self.viewer.set_selected_models(self._selected_model_ids(), emit_signal=False)
        self.statusBar().showMessage("Selected all models")

    def _selected_model_ids(self):
        lw = self.model_panel.list_widget
        selected = []
        for row in range(lw.count()):
            item = lw.item(row)
            if item is not None and item.isSelected():
                model_id = self._panel_item_model_id(item)
                if model_id is not None:
                    selected.append(model_id)
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
        parts = []
        object_id = int(m.get("object_id", 0))
        if hasattr(self.viewer, "scene_state") and object_id:
            obj = self.viewer.scene_state.objects.get(object_id)
            if obj is not None:
                for part_id in obj.part_ids:
                    part = self.viewer.scene_state.parts.get(int(part_id))
                    if part is None:
                        continue
                    parts.append(
                        {
                            "name": str(part.name or f"Part {part_id}"),
                            "vertices": np.asarray(part.vertices, dtype=float).copy(),
                            "faces": np.asarray(part.faces, dtype=int).copy(),
                            "source_path": str(part.source_path or ""),
                            "metadata": dict(part.metadata or {}),
                        }
                    )
        return {
            "name": m.get("name", f"Model {model_id}"),
            "path": m.get("path", ""),
            "base_vertices": np.asarray(m.get("base_vertices", []), dtype=float).copy(),
            "faces": np.asarray(m.get("faces", []), dtype=int).copy(),
            "parts": parts or [
                {
                    "name": m.get("name", f"Model {model_id}"),
                    "vertices": np.asarray(m.get("base_vertices", []), dtype=float).copy(),
                    "faces": np.asarray(m.get("faces", []), dtype=int).copy(),
                    "source_path": m.get("path", ""),
                    "metadata": {},
                }
            ],
            "scale": self._scale_to_vec(m.get("scale", 1.0)),
            "rotation": self._vec3(m.get("rotation", [0.0, 0.0, 0.0])),
            "offset": self._vec3(m.get("offset", [0.0, 0.0, 0.0])),
            "plate_id": int(m.get("plate_id", getattr(self.viewer, "get_current_plate_id", lambda: 1)())),
            "object_metadata": dict(m.get("object_metadata") or {}),
            "instance_metadata": dict(m.get("metadata") or {}),
        }

    def _apply_model_payloads(self, payloads, offset_step=(0.0, 0.0, 0.0)):
        if not payloads:
            return []
        new_ids = []
        for idx, payload in enumerate(payloads):
            target_plate_id = getattr(self.viewer, "get_current_plate_id", lambda: payload.get("plate_id"))()
            model_id = self.viewer.add_scene_object(
                payload["name"],
                payload["path"],
                payload.get("parts", []),
                plate_id=target_plate_id,
                object_metadata=dict(payload.get("object_metadata") or {}),
                instance_metadata=dict(payload.get("instance_metadata") or {}),
            )
            delta = np.array(offset_step, dtype=float) * float(idx + 1)
            offset = np.array(payload["offset"], dtype=float) + delta
            self.viewer.set_model_transform(
                model_id,
                scale=payload["scale"],
                rotation_xyz=payload["rotation"],
                offset_xyz=offset,
            )
            new_ids.append(model_id)
        if new_ids:
            if hasattr(self.model_panel, "refresh_from_viewer"):
                self.model_panel.refresh_from_viewer(self.viewer)
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
            if hasattr(self.model_panel, "refresh_from_viewer"):
                self.model_panel.refresh_from_viewer(self.viewer)
        finally:
            lw.blockSignals(block)

        remaining = self.viewer.get_model_ids()
        if not remaining and hasattr(self.viewer, "get_all_model_ids"):
            remaining = self.viewer.get_all_model_ids()
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
                mid = self._panel_item_model_id(item)
                if mid in current_set:
                    item.setSelected(True)
                    if mid == (ids[0] if ids else None):
                        lw.setCurrentItem(item)
        finally:
            lw.blockSignals(block)

    def _selected_model_index(self):
        model_ids = list(self.viewer.get_all_model_ids() if hasattr(self.viewer, "get_all_model_ids") else self.viewer.models.keys())
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
        if hasattr(self.viewer, "serialize_scene"):
            return {
                "scene": self.viewer.serialize_scene(),
            }
        model_ids = list(self.viewer.models.keys())
        return {
            "models": self._capture_models_payload(model_ids),
            "selected_index": self._selected_model_index(),
        }

    def _state_signature(self, state) -> tuple:
        scene = state.get("scene")
        if isinstance(scene, dict):
            try:
                return ("scene_v2", json.dumps(scene, sort_keys=True, default=str))
            except Exception:
                return ("scene_v2", str(scene))
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
            scene = state.get("scene")
            if isinstance(scene, dict) and hasattr(self.viewer, "restore_scene"):
                self.viewer.restore_scene(scene)
                if hasattr(self.model_panel, "refresh_from_viewer"):
                    self.model_panel.refresh_from_viewer(self.viewer)
                selected_ids = list(scene.get("selected_entity_ids", []) or [])
                self.current_model_id = selected_ids[0] if selected_ids else None
                self.viewer.set_selected_models(selected_ids, emit_signal=False)
                if selected_ids:
                    self._select_model_in_panel(selected_ids)
                else:
                    self.model_panel.list_widget.clearSelection()
            else:
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
        normalized = "ortho" if str(mode or "").strip().lower() == "ortho" else "perspective"
        if hasattr(self.viewer, "set_projection_mode"):
            normalized = str(self.viewer.set_projection_mode(normalized))
        else:
            if normalized == "ortho":
                self.viewer.opts["fov"] = 0  # pyright: ignore[reportArgumentType]
            else:
                self.viewer.opts["fov"] = 60  # pyright: ignore[reportArgumentType]
            self.viewer.update()
        self._sync_projection_action_state(normalized)

    def _sync_projection_action_state(self, mode: str):
        normalized = "ortho" if str(mode or "").strip().lower() == "ortho" else "perspective"
        perspective_action = getattr(self, "_perspective_action", None)
        ortho_action = getattr(self, "_ortho_action", None)
        if perspective_action is not None:
            block = perspective_action.blockSignals(True)
            perspective_action.setChecked(normalized == "perspective")
            perspective_action.blockSignals(block)
        if ortho_action is not None:
            block = ortho_action.blockSignals(True)
            ortho_action.setChecked(normalized == "ortho")
            ortho_action.blockSignals(block)

    def _on_viewer_projection_mode_changed(self, mode: str):
        self._sync_projection_action_state(mode)

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
        url = "https://github.com/Electrovian/Project-PrintNet/releases"
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
        current = os.path.abspath(os.path.dirname(__file__))
        for _ in range(10):
            if os.path.isdir(os.path.join(current, ".git")):
                return current
            has_app = os.path.isdir(os.path.join(current, "App"))
            has_website = os.path.isdir(os.path.join(current, "Website"))
            if has_app and has_website:
                return current
            parent = os.path.dirname(current)
            if parent == current:
                break
            current = parent
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))

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
