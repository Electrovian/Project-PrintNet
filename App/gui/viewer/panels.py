from __future__ import annotations

from typing import Any, Dict, List, Tuple, TYPE_CHECKING, cast

import os

import numpy as np
import trimesh

from PyQt5 import QtCore, QtGui, QtWidgets

from ..theme import theme_qcolor, theme_value
from ..widgets.view_cube_overlay import ViewCubeOverlay


class PanelMixin:
    def _rgba_css(self, color: QtGui.QColor, alpha: int | None = None):
        c = QtGui.QColor(color)
        if alpha is not None:
            c.setAlpha(int(alpha))
        return f"rgba({c.red()}, {c.green()}, {c.blue()}, {c.alpha()})"

    def _update_rotate_hud_style(self):
        if not hasattr(self, "_rotate_hud") or self._rotate_hud is None:
            return
        bg = theme_qcolor("popup_bg")
        text = theme_qcolor("popup_text")
        bg_css = self._rgba_css(bg, 220)
        text_css = self._rgba_css(text, 255)
        self._rotate_hud.setStyleSheet(
            "QLabel {"
            f"background-color: {bg_css};"
            f"color: {text_css};"
            "padding: 2px 6px;"
            "border-radius: 4px;"
            "font-weight: 600;"
            "}"
        )

    def _show_rotate_hud(self, pos: QtCore.QPoint, axis: str, value: float):
        if not hasattr(self, "_rotate_hud") or self._rotate_hud is None:
            return
        self._rotate_hud.setText(f"{axis}: {value:.2f}")
        self._rotate_hud.adjustSize()
        offset = QtCore.QPoint(12, -28)
        target = pos + offset
        x = min(max(0, target.x()), max(0, self.width() - self._rotate_hud.width()))
        y = min(max(0, target.y()), max(0, self.height() - self._rotate_hud.height()))
        self._rotate_hud.move(x, y)
        self._rotate_hud.setVisible(True)

    def _hide_rotate_hud(self):
        if hasattr(self, "_rotate_hud") and self._rotate_hud is not None:
            self._rotate_hud.setVisible(False)

    def _build_selection_info(self):
        parent = cast(QtWidgets.QWidget, self)
        panel = QtWidgets.QFrame(parent)
        panel.setObjectName("SelectionInfo")
        panel_layout = QtWidgets.QVBoxLayout(panel)
        panel_layout.setContentsMargins(8, 6, 8, 6)
        panel_layout.setSpacing(4)

        title = QtWidgets.QLabel(panel)
        title.setObjectName("SelectionInfoTitle")
        title.setWordWrap(True)

        details = QtWidgets.QLabel(panel)
        details.setObjectName("SelectionInfoDetails")
        details.setWordWrap(True)

        panel_layout.addWidget(title)
        panel_layout.addWidget(details)

        self._selection_info = panel
        self._selection_info_title = title
        self._selection_info_details = details
        self._update_selection_info_style()
        panel.hide()

    def _build_print_stats_panel(self):
        parent = cast(QtWidgets.QWidget, self)
        panel = QtWidgets.QFrame(parent)
        panel.setObjectName("PrintStats")
        panel_layout = QtWidgets.QVBoxLayout(panel)
        panel_layout.setContentsMargins(8, 6, 8, 6)
        panel_layout.setSpacing(4)

        title = QtWidgets.QLabel("Slice Estimate", panel)
        title.setObjectName("PrintStatsTitle")
        title.setWordWrap(True)

        details = QtWidgets.QLabel("No stats yet.", panel)
        details.setObjectName("PrintStatsDetails")
        details.setWordWrap(True)

        panel_layout.addWidget(title)
        panel_layout.addWidget(details)

        self._print_stats_panel = panel
        self._print_stats_title = title
        self._print_stats_details = details
        self._update_print_stats_style()
        panel.hide()

    def _build_preview_object_panel(self):
        parent = cast(QtWidgets.QWidget, self)
        panel = QtWidgets.QFrame(parent)
        panel.setObjectName("PreviewObject")
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)

        label = QtWidgets.QLabel(panel)
        label.setObjectName("PreviewObjectLabel")
        label.setWordWrap(True)
        layout.addWidget(label)

        self._preview_object_panel = panel
        self._preview_object_label = label
        self._update_preview_object_style()
        panel.hide()

    def _build_simplify_warning(self):
        parent = cast(QtWidgets.QWidget, self)
        panel = QtWidgets.QFrame(parent)
        panel.setObjectName("SimplifyWarning")
        layout = QtWidgets.QHBoxLayout(panel)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(8)

        label = QtWidgets.QLabel(panel)
        label.setObjectName("SimplifyWarningLabel")
        label.setWordWrap(True)
        layout.addWidget(label, 1)

        link = QtWidgets.QToolButton(panel)
        link.setObjectName("SimplifyWarningLink")
        link.setText("Simplify model")
        link.setCursor(QtCore.Qt.PointingHandCursor)
        link.setAutoRaise(True)
        layout.addWidget(link)

        close_btn = QtWidgets.QToolButton(panel)
        close_btn.setObjectName("SimplifyWarningClose")
        close_btn.setText("×")
        close_btn.setCursor(QtCore.Qt.PointingHandCursor)
        close_btn.setAutoRaise(True)
        layout.addWidget(close_btn)

        link.clicked.connect(self._emit_simplify_warning)
        close_btn.clicked.connect(self._hide_simplify_warning)

        self._simplify_warning = panel
        self._simplify_warning_label = label
        self._simplify_warning_btn = link
        self._simplify_warning_close = close_btn
        self._update_simplify_warning_style()
        panel.hide()

    def _update_selection_info_style(self):
        if not hasattr(self, "_selection_info") or self._selection_info is None:
            return
        bg = theme_qcolor("popup_bg")
        border = theme_qcolor("popup_border")
        text = theme_qcolor("popup_text")
        muted = theme_qcolor("popup_muted_text")
        self._selection_info.setStyleSheet(
            "QFrame#SelectionInfo {"
            f"background-color: {self._rgba_css(bg, 220)};"
            f"border: 1px solid {self._rgba_css(border, 240)};"
            "border-radius: 6px;"
            "}"
            "QLabel#SelectionInfoTitle {"
            f"color: {self._rgba_css(text, 255)};"
            "font-weight: 600;"
            "}"
            "QLabel#SelectionInfoDetails {"
            f"color: {self._rgba_css(muted, 255)};"
            "}"
        )

    def _update_print_stats_style(self):
        if not hasattr(self, "_print_stats_panel") or self._print_stats_panel is None:
            return
        bg = theme_qcolor("popup_bg")
        border = theme_qcolor("popup_border")
        text = theme_qcolor("popup_text")
        muted = theme_qcolor("popup_muted_text")
        self._print_stats_panel.setStyleSheet(
            "QFrame#PrintStats {"
            f"background-color: {self._rgba_css(bg, 220)};"
            f"border: 1px solid {self._rgba_css(border, 240)};"
            "border-radius: 6px;"
            "}"
            "QLabel#PrintStatsTitle {"
            f"color: {self._rgba_css(text, 255)};"
            "font-weight: 600;"
            "}"
            "QLabel#PrintStatsDetails {"
            f"color: {self._rgba_css(muted, 255)};"
            "}"
        )

    def _update_preview_object_style(self):
        if self._preview_object_panel is None:
            return
        bg = theme_qcolor("popup_bg")
        border = theme_qcolor("popup_border")
        text = theme_qcolor("popup_text")
        self._preview_object_panel.setStyleSheet(
            "QFrame#PreviewObject {"
            f"background-color: {self._rgba_css(bg, 200)};"
            f"border: 1px solid {self._rgba_css(border, 220)};"
            "border-radius: 6px;"
            "}"
            "QLabel#PreviewObjectLabel {"
            f"color: {self._rgba_css(text, 255)};"
            "font-weight: 600;"
            "}"
        )

    def _update_simplify_warning_style(self):
        if self._simplify_warning is None:
            return
        bg = theme_qcolor("popup_bg")
        border = theme_qcolor("popup_border")
        text = theme_qcolor("popup_text")
        accent = theme_qcolor("topbar_accent")
        muted = theme_qcolor("popup_muted_text")
        self._simplify_warning.setStyleSheet(
            "QFrame#SimplifyWarning {"
            f"background-color: {self._rgba_css(bg, 240)};"
            f"border: 1px solid {self._rgba_css(border, 240)};"
            f"border-left: 4px solid {self._rgba_css(accent, 255)};"
            "border-radius: 8px;"
            "}"
            "QLabel#SimplifyWarningLabel {"
            f"color: {self._rgba_css(text, 255)};"
            "}"
            "QToolButton#SimplifyWarningLink {"
            f"color: {self._rgba_css(accent, 255)};"
            "font-weight: 600;"
            "padding: 2px 6px;"
            "}"
            "QToolButton#SimplifyWarningClose {"
            f"color: {self._rgba_css(muted, 255)};"
            "font-size: 16px;"
            "padding: 0 6px;"
            "}"
        )

    def _position_selection_info(self):
        self._position_bottom_left_panels()

    def _position_bottom_left_panels(self):
        margin = 12
        y = self.height() - margin
        if self._preview_object_panel is not None and self._preview_object_panel.isVisible():
            self._preview_object_panel.adjustSize()
            y = max(margin, y - self._preview_object_panel.height())
            self._preview_object_panel.move(margin, y)
            y -= margin
        if self._print_stats_panel is not None and self._print_stats_panel.isVisible():
            self._print_stats_panel.adjustSize()
            y = max(margin, y - self._print_stats_panel.height())
            self._print_stats_panel.move(margin, y)
            y -= margin
        if self._selection_info is not None and self._selection_info.isVisible():
            self._selection_info.adjustSize()
            y = max(margin, y - self._selection_info.height())
            self._selection_info.move(margin, y)
            y -= margin
        if self._simplify_warning is not None and self._simplify_warning.isVisible():
            self._simplify_warning.adjustSize()
            y = max(margin, y - self._simplify_warning.height())
            self._simplify_warning.move(margin, y)

    def set_labels_visible(self, visible: bool):
        self._labels_enabled = bool(visible)
        self._update_selection_info()

    def _update_selection_info(self):
        if not hasattr(self, "_selection_info") or self._selection_info is None:
            return
        if not self._labels_enabled:
            self._selection_info.setVisible(False)
            return
        selected_ids = self._selected_model_ids or ([self._selected_model_id] if self._selected_model_id is not None else [])
        if not selected_ids:
            self._selection_info.setVisible(False)
            return
        if len(selected_ids) == 1:
            m = self.models.get(selected_ids[0])
            if not m:
                self._selection_info.setVisible(False)
                return
            name = (m.get("name") or "").strip() or f"Model {selected_ids[0]}"
            path = m.get("path") or ""
            ext = os.path.splitext(path)[1].lstrip(".").lower() if path else ""
            ext = ext if ext else "unknown"

            bounds = m.get("bounds")
            size_line = "Size: n/a"
            if bounds is not None:
                mn, mx = bounds
                size = np.abs(np.array(mx) - np.array(mn))
                size_line = f"Size: {size[0]:.2f} x {size[1]:.2f} x {size[2]:.2f} mm"

            volume = self._model_volume(m)
            volume_line = "Volume: n/a"
            if volume is not None:
                volume_line = f"Volume: {volume:.2f} mm^3"

            faces = m.get("faces")
            triangles = int(len(faces)) if faces is not None else 0

            self._selection_info_title.setText(f"Object name: {name}")
        else:
            bounds_list = [self.models[mid].get("bounds") for mid in selected_ids if mid in self.models]
            bounds_list = [b for b in bounds_list if b is not None]
            size_line = "Size: n/a"
            if bounds_list:
                mn = np.min([b[0] for b in bounds_list], axis=0)
                mx = np.max([b[1] for b in bounds_list], axis=0)
                size = np.abs(np.array(mx) - np.array(mn))
                size_line = f"Size: {size[0]:.2f} x {size[1]:.2f} x {size[2]:.2f} mm"
            volume_vals = [self._model_volume(self.models[mid]) for mid in selected_ids if mid in self.models]
            volume_vals = [v for v in volume_vals if v is not None]
            volume_line = "Volume: n/a"
            if volume_vals:
                volume_line = f"Volume: {sum(volume_vals):.2f} mm^3"
            triangles = 0
            for mid in selected_ids:
                if mid not in self.models:
                    continue
                faces = self.models[mid].get("faces")
                if faces is None:
                    continue
                triangles += int(len(faces))
            ext = "mixed"
            self._selection_info_title.setText(f"Selected models: {len(selected_ids)}")
        self._selection_info_details.setText(
            "\n".join(
                [
                    f"Type: {ext}",
                    size_line,
                    volume_line,
                    f"Triangles: {triangles}",
                ]
            )
        )
        self._selection_info.setVisible(True)
        self._update_simplify_warning()
        self._position_bottom_left_panels()

    def _model_triangle_count(self, model: dict) -> int:
        faces = model.get("faces")
        if faces is None:
            return 0
        try:
            return int(np.asarray(faces).shape[0])
        except Exception:
            return 0

    def _update_simplify_warning(self):
        if self._simplify_warning is None or self._simplify_warning_label is None:
            return
        model_id = self._selected_model_id
        if model_id is None and self.models:
            model_id = next(iter(self.models.keys()))
        if model_id is None:
            self._simplify_warning.setVisible(False)
            return
        model = self.models.get(model_id)
        if model is None:
            self._simplify_warning.setVisible(False)
            return
        triangles = self._model_triangle_count(model)
        if triangles < 1_000_000:
            self._simplify_warning.setVisible(False)
            return
        name = (model.get("name") or "").strip() or f"Model {model_id}"
        msg = (f"Processing model '{name}' with more than 1M triangles could be slow. "
               "It is highly recommended to simplify the model.")
        self._simplify_warning_label.setText(msg)
        self._simplify_warning_model_id = model_id
        self._simplify_warning.setVisible(True)
        self._position_bottom_left_panels()

    def _emit_simplify_warning(self):
        model_id = self._simplify_warning_model_id
        if model_id is None:
            return
        self.simplifyRequested.emit(int(model_id))

    def _hide_simplify_warning(self):
        if self._simplify_warning is None:
            return
        self._simplify_warning_model_id = None
        self._simplify_warning.setVisible(False)

    def set_print_stats(self, stats: dict | None):
        if self._print_stats_panel is None:
            return
        self._print_stats_data = stats
        if not stats or not self._print_stats_visible:
            self._print_stats_panel.setVisible(False)
            return
        time_val = stats.get("time", "n/a")
        length_val = stats.get("length", "n/a")
        weight_val = stats.get("weight", "n/a")
        self._print_stats_details.setText(
            "\n".join(
                [
                    f"Time: {time_val}",
                    f"Length: {length_val}",
                    f"Weight: {weight_val}",
                ]
            )
        )
        self._print_stats_panel.setVisible(True)
        self._position_bottom_left_panels()

    def clear_print_stats(self):
        if self._print_stats_panel is not None:
            self._print_stats_panel.setVisible(False)
        self._print_stats_data = None

    def set_print_stats_visible(self, visible: bool):
        self._print_stats_visible = bool(visible)
        if not self._print_stats_visible and self._print_stats_panel is not None:
            self._print_stats_panel.setVisible(False)
        if self._print_stats_visible and self._print_stats_data:
            self.set_print_stats(self._print_stats_data)
        self._position_bottom_left_panels()

    def set_preview_object_visible(self, visible: bool):
        self._preview_object_visible = bool(visible)
        if self._preview_object_panel is not None:
            self._preview_object_panel.setVisible(self._preview_object_visible)
        if self._preview_object_visible:
            self._update_preview_object_label()
        self._position_bottom_left_panels()

    def _update_preview_object_label(self):
        if self._preview_object_label is None:
            return
        model_id = self._selected_model_id
        if model_id is None and self.models:
            model_id = next(iter(self.models.keys()))
        name = "Object"
        if model_id is not None:
            m = self.models.get(model_id)
            if m:
                name = (m.get("name") or "").strip() or f"Model {model_id}"
        self._preview_object_label.setText(f"{name}")
        if self._preview_object_panel is not None:
            self._preview_object_panel.adjustSize()
        self._position_bottom_left_panels()

    def set_bed_limits(self, bed_size: Tuple[float, float], max_height: float):
        self._bed_size = (float(bed_size[0]), float(bed_size[1]))
        self._bed_height = float(max_height)
        self._sync_bed_grid()
        for mid in self.models:
            self._update_bed_state(mid)
        self.update()

    def _sync_bed_grid(self):
        if getattr(self, "_grid_item", None) is None:
            return
        size_x = float(self._bed_size[0]) if self._bed_size else 0.0
        size_y = float(self._bed_size[1]) if self._bed_size else 0.0
        self._safe_gl_update(self._grid_item.setSize, size_x, size_y, 0)

    def get_out_of_bounds_models(self) -> List[int]:
        return [mid for mid, model in self.models.items() if model.get("out_of_bounds")]

    def _bed_bounds(self) -> Tuple[float, float, float, float]:
        half_w = float(self._bed_size[0]) / 2.0
        half_d = float(self._bed_size[1]) / 2.0
        return (-half_w, half_w, -half_d, half_d)

    def _is_outside_bed(self, bounds) -> bool:
        if bounds is None:
            return False
        mn, mx = bounds
        min_x, max_x, min_y, max_y = self._bed_bounds()
        if mn[0] < min_x or mx[0] > max_x:
            return True
        if mn[1] < min_y or mx[1] > max_y:
            return True
        if mx[2] > self._bed_height:
            return True
        return False

    def _update_bed_state(self, model_id: int) -> bool:
        m = self.models.get(model_id)
        if m is None:
            return False
        out_of_bounds = self._is_outside_bed(m.get("bounds"))
        m["out_of_bounds"] = out_of_bounds
        self._apply_model_color(m)
        return out_of_bounds

    def _apply_model_color(self, model: dict):
        item = model.get("item")
        if item is None:
            return
        base_color = theme_value("mesh_color", (0.0, 0.9, 0.4, 0.9))
        warn_color = theme_value("mesh_warning", (1.0, 0.25, 0.2, 0.95))
        color = warn_color if model.get("out_of_bounds") else base_color
        self._safe_gl_update(item.setColor, color)

    def _model_volume(self, model: dict):
        base = model.get("base_volume")
        if base is None:
            try:
                mesh = trimesh.Trimesh(vertices=model["base_vertices"], faces=model["faces"], process=False)
                base = float(mesh.volume)
            except Exception:
                base = None
            model["base_volume"] = base
        if base is None or not np.isfinite(base):
            return None
        scale = self._normalize_scale(model.get("scale", 1.0))
        factor = abs(float(scale[0] * scale[1] * scale[2]))
        volume = abs(float(base)) * factor
        if not np.isfinite(volume) or volume <= 0.0:
            return None
        return volume

    def reset_view(self):
        self.opts["distance"] = self._default_view["distance"] # pyright: ignore[reportArgumentType]
        self.opts["elevation"] = self._default_view["elevation"] # pyright: ignore[reportArgumentType]
        self.opts["azimuth"] = self._default_view["azimuth"] # pyright: ignore[reportArgumentType]
        self._coerce_distance()
        self._sync_view_cube()
        self.update()

    def set_view(self, azimuth: float, elevation: float, distance: float | None = None):
        self.opts["azimuth"] = float(azimuth) # pyright: ignore[reportArgumentType]
        self.opts["elevation"] = float(elevation) # pyright: ignore[reportArgumentType]
        if distance is not None:
            self.opts["distance"] = float(distance) # pyright: ignore[reportArgumentType]
        self._coerce_distance()
        self._sync_view_cube()
        self.update()

    def set_snap(self, enabled: bool, step_mm: float):
        self._snap_enabled = bool(enabled)
        self._snap_step = max(0.001, float(step_mm))

    def _cancel_interaction(self):
        self._dragging = False
        self._drag_start_world = None
        self._drag_start_offsets = None
        self._drag_plane_z = 0.0
        self._gizmo_drag_axis = None
        self._gizmo_drag_start_param = None
        self._gizmo_drag_start_offsets = None
        if self._gizmo_rotate_axis is not None:
            self._gizmo_rotate_axis = None
            self._gizmo_rotate_start_angle = None
            self._gizmo_rotate_start_rotation = None
            self._gizmo_rotate_start_rotations = None
            self._gizmo_rotate_start_offsets = None
            self._gizmo_rotate_pivot = None
            self._hide_rotate_hud()
        if self._marquee_active:
            if self._marquee_band is not None:
                self._marquee_band.hide()
            self._marquee_active = False
            self._marquee_origin = None
        self._update_gizmo()

    # -------------------- view cube --------------------

    def _build_view_cube(self):
        self._view_cube = ViewCubeOverlay(cast(QtWidgets.QWidget, self))
        self._view_cube.viewRequested.connect(self._set_view_from_cube)
        self._view_cube.homeRequested.connect(self.reset_view)
        self._position_view_cube()
        self._sync_view_cube()

    def set_view_cube_visible(self, visible: bool):
        if hasattr(self, "_view_cube") and self._view_cube is not None:
            self._view_cube.setVisible(bool(visible))
            if visible:
                self._position_view_cube()

    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any:
            ...
