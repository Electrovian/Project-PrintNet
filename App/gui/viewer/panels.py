from __future__ import annotations

from typing import Any, Dict, List, Tuple, TYPE_CHECKING, cast

import os

import numpy as np
import trimesh
import pyqtgraph.opengl as gl

from PyQt5 import QtCore, QtGui, QtWidgets

from ..i18n import tr
from ..theme import theme_qcolor, theme_value
from ..widgets.view_cube_overlay import ViewCubeOverlay
from config.defaults import DEFAULTS


class PanelMixin:
    @staticmethod
    def _t(key: str, default: str = "", **kwargs: object) -> str:
        return tr(key, default=default, **kwargs)

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
        if hasattr(self, "_view_cube") and self._view_cube is not None and self._view_cube.isVisible():
            y = min(y, max(margin, self._view_cube.y() - margin))
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
        self._sync_bed_texture_item()
        for mid in self.models:
            self._update_bed_state(mid)
        self.update()

    def set_bed_visuals(self, texture_path: str | None = None, model_path: str | None = None):
        texture_value = str(texture_path or "").strip()
        model_value = str(model_path or "").strip()
        if texture_value == getattr(self, "_bed_texture_path", "") and model_value == getattr(self, "_bed_model_path", ""):
            return
        self._bed_texture_path = texture_value
        self._bed_model_path = model_value
        self._sync_bed_texture_item()

    def _clear_bed_texture_item(self):
        items = dict(getattr(self, "_plate_texture_items", {}) or {})
        for item in items.values():
            if item is None:
                continue
            try:
                self.removeItem(item)
            except Exception:
                pass
        self._plate_texture_items = {}
        self._bed_texture_item = None

    def _sync_bed_texture_item(self):
        self._clear_bed_texture_item()
        texture_path = str(getattr(self, "_bed_texture_path", "") or "").strip()
        if not texture_path:
            return

        image = QtGui.QImage(texture_path)
        if image.isNull():
            return
        image = image.convertToFormat(QtGui.QImage.Format_RGBA8888)
        width = int(image.width())
        height = int(image.height())
        if width <= 0 or height <= 0:
            return

        ptr = image.bits()
        ptr.setsize(image.byteCount())
        rgba = np.frombuffer(ptr, dtype=np.uint8).reshape((height, width, 4)).copy()
        rgba = np.transpose(rgba, (1, 0, 2))
        alpha = rgba[:, :, 3].astype(np.uint16)
        alpha = np.clip((alpha * 96) // 255, 20, 120).astype(np.uint8)
        rgba[:, :, 3] = alpha
        rgba = np.ascontiguousarray(rgba)

        scale_x = float(self._bed_size[0]) / max(1.0, float(rgba.shape[0]))
        scale_y = float(self._bed_size[1]) / max(1.0, float(rgba.shape[1]))
        self._plate_texture_items = {}
        for plate_id in getattr(self, "get_plate_ids", lambda: [1])():
            try:
                image_item = gl.GLImageItem(rgba.copy(), smooth=True, glOptions="translucent")
            except Exception:
                continue
            image_item.scale(scale_x, scale_y, 1.0)
            origin = getattr(self, "_plate_origin")(int(plate_id))
            image_item.translate(
                float(origin[0]) - (float(self._bed_size[0]) * 0.5),
                float(origin[1]) - (float(self._bed_size[1]) * 0.5),
                -0.05,
            )
            self._plate_texture_items[int(plate_id)] = image_item
            self.addItem(image_item)
        first_id = next(iter(self._plate_texture_items.keys()), None)
        self._bed_texture_item = self._plate_texture_items.get(first_id) if first_id is not None else None

    def _sync_bed_grid(self):
        size_x = float(self._bed_size[0]) if self._bed_size else 0.0
        size_y = float(self._bed_size[1]) if self._bed_size else 0.0
        spacing = DEFAULTS["viewer"]["grid_spacing"]
        active_color = theme_value("grid_color", (80, 80, 80, 255))
        inactive = QtGui.QColor(theme_qcolor("popup_muted_text"))
        inactive.setAlpha(110)
        inactive_color = (
            inactive.redF(),
            inactive.greenF(),
            inactive.blueF(),
            inactive.alphaF(),
        )
        desired = set(getattr(self, "get_plate_ids", lambda: [1])())
        existing = dict(getattr(self, "_plate_grid_items", {}) or {})
        for plate_id, item in existing.items():
            if plate_id in desired:
                continue
            try:
                self.removeItem(item)
            except Exception:
                pass
        self._plate_grid_items = {}
        current_plate_id = getattr(self, "get_current_plate_id", lambda: 1)()
        for plate_id in desired:
            item = existing.get(int(plate_id))
            if item is None:
                item = gl.GLGridItem()
                self.addItem(item)
            self._safe_gl_update(item.setSize, size_x, size_y, 0)
            self._safe_gl_update(item.setSpacing, spacing[0], spacing[1], spacing[2])
            origin = getattr(self, "_plate_origin")(int(plate_id))
            try:
                item.resetTransform()
            except Exception:
                pass
            item.translate(float(origin[0]), float(origin[1]), 0.0)
            item.setColor(active_color if int(plate_id) == int(current_plate_id) else inactive_color)
            self._plate_grid_items[int(plate_id)] = item
        first_id = next(iter(self._plate_grid_items.keys()), None)
        self._grid_item = self._plate_grid_items.get(first_id) if first_id is not None else None
        self._sync_bed_texture_item()
        self._update_plate_label_texts()

    def get_out_of_bounds_models(self) -> List[int]:
        return [mid for mid, model in self.models.items() if model.get("out_of_bounds")]

    def _bed_bounds(self, plate_id: int | None = None) -> Tuple[float, float, float, float]:
        half_w = float(self._bed_size[0]) / 2.0
        half_d = float(self._bed_size[1]) / 2.0
        origin = (0.0, 0.0, 0.0)
        if hasattr(self, "_plate_origin"):
            resolved_plate = int(plate_id if plate_id is not None else getattr(self, "get_current_plate_id", lambda: 1)())
            origin = getattr(self, "_plate_origin")(resolved_plate)
        return (
            float(origin[0]) - half_w,
            float(origin[0]) + half_w,
            float(origin[1]) - half_d,
            float(origin[1]) + half_d,
        )

    def _is_outside_bed(self, bounds, plate_id: int | None = None) -> bool:
        if bounds is None:
            return False
        mn, mx = bounds
        min_x, max_x, min_y, max_y = self._bed_bounds(plate_id)
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
        plate_id = int(m.get("plate_id", getattr(self, "get_current_plate_id", lambda: 1)()))
        out_of_bounds = self._is_outside_bed(m.get("bounds"), plate_id=plate_id)
        m["out_of_bounds"] = out_of_bounds
        self._apply_model_color(m)
        return out_of_bounds

    def _apply_model_color(self, model: dict):
        item = model.get("item")
        if item is None:
            return
        base_color = theme_value("mesh_color", (0.0, 0.9, 0.4, 0.9))
        edge_color = theme_value("mesh_edge_color", (0.62, 0.64, 0.68, 0.72))
        warn_color = theme_value("mesh_warning", (1.0, 0.25, 0.2, 0.95))
        color = warn_color if model.get("out_of_bounds") else base_color
        alpha_scale = getattr(self, "_model_preview_alpha", 1.0)
        active_plate = int(getattr(self, "get_current_plate_id", lambda: 1)())
        if int(model.get("plate_id", active_plate)) != active_plate:
            alpha_scale *= 0.35
        if isinstance(color, (tuple, list)):
            values = list(color)
            if len(values) == 3:
                values.append(1.0 if max(values) <= 1.0 else 255.0)
            if int(model.get("plate_id", active_plate)) != active_plate:
                muted = float(sum(float(v) for v in values[:3]) / 3.0)
                values[0] = muted
                values[1] = muted
                values[2] = muted
            max_rgb = max(values[:3]) if values[:3] else 1.0
            if max_rgb > 1.0:
                values[3] = max(0.0, min(255.0, float(values[3]) * alpha_scale))
            else:
                values[3] = max(0.0, min(1.0, float(values[3]) * alpha_scale))
            color = tuple(values)
        self._safe_gl_update(item.setColor, color)
        if isinstance(edge_color, (tuple, list)):
            values = list(edge_color)
            if len(values) == 3:
                values.append(1.0 if max(values) <= 1.0 else 255.0)
            edge_color = tuple(values[:4])
        try:
            item.opts["edgeColor"] = edge_color
            item.update()
        except Exception:
            return

    def _apply_plate_visual_theme(self):
        active_color = theme_value("grid_color", (80, 80, 80, 255))
        inactive = QtGui.QColor(theme_qcolor("popup_muted_text"))
        inactive.setAlpha(110)
        inactive_color = (
            inactive.redF(),
            inactive.greenF(),
            inactive.blueF(),
            inactive.alphaF(),
        )
        current_plate_id = int(getattr(self, "get_current_plate_id", lambda: 1)())
        for plate_id, item in dict(getattr(self, "_plate_grid_items", {}) or {}).items():
            item.setColor(active_color if int(plate_id) == current_plate_id else inactive_color)
        self._update_plate_label_texts()

    def _ensure_plate_label(self, plate_id: int, *, number: bool) -> QtWidgets.QLabel:
        attr = "_plate_number_labels" if number else "_plate_name_labels"
        labels = getattr(self, attr, None)
        if labels is None:
            labels = {}
            setattr(self, attr, labels)
        label = labels.get(int(plate_id))
        if label is None:
            label = QtWidgets.QLabel(cast(QtWidgets.QWidget, self))
            label.setObjectName("PlateNumberLabel" if number else "PlateNameLabel")
            label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
            label.show()
            labels[int(plate_id)] = label
        return label

    def _update_plate_label_texts(self):
        if not hasattr(self, "scene_state"):
            return
        plates = getattr(self.scene_state, "plates", {})
        ordered = []
        if hasattr(self, "get_plate_ids"):
            ordered = list(getattr(self, "get_plate_ids")())
        active_plate = int(getattr(self, "get_current_plate_id", lambda: 1)())
        remove_btn = getattr(self, "_plate_remove_btn", None)
        if remove_btn is not None:
            remove_btn.setEnabled(len(ordered) > 1)
        lock_btn = getattr(self, "_plate_lock_btn", None)
        if lock_btn is not None and hasattr(self, "is_plate_locked"):
            prev = lock_btn.blockSignals(True)
            lock_btn.setChecked(bool(self.is_plate_locked()))
            lock_btn.blockSignals(prev)
        for index, plate_id in enumerate(ordered):
            plate = plates.get(int(plate_id))
            if plate is None:
                continue
            name_label = self._ensure_plate_label(int(plate_id), number=False)
            number_label = self._ensure_plate_label(int(plate_id), number=True)
            name_text = str(getattr(plate, "name", "") or f"{index + 1:02d}").strip() or f"{index + 1:02d}"
            number_text = f"{index + 1:02d}"
            text_color = theme_qcolor("topbar_accent") if int(plate_id) == active_plate else theme_qcolor("popup_muted_text")
            style = (
                f"color: rgba({text_color.red()}, {text_color.green()}, {text_color.blue()}, {255 if int(plate_id) == active_plate else 180});"
                "font-weight: 700;"
                "background: transparent;"
            )
            name_label.setStyleSheet(style)
            number_label.setStyleSheet(style)
            name_label.setText(name_text)
            number_label.setText(number_text)
            name_label.adjustSize()
            number_label.adjustSize()
            name_label.setVisible(True)
            number_label.setVisible(True)
        for attr in ("_plate_name_labels", "_plate_number_labels"):
            labels = getattr(self, attr, {})
            for plate_id in list(labels.keys()):
                if plate_id in ordered:
                    continue
                label = labels.pop(plate_id)
                label.hide()
                label.deleteLater()
        if hasattr(self, "_position_plate_labels"):
            self._position_plate_labels()

    def _position_plate_labels(self):
        ordered = list(getattr(self, "get_plate_ids", lambda: [])())
        for plate_id in ordered:
            name_label = getattr(self, "_plate_name_labels", {}).get(int(plate_id))
            number_label = getattr(self, "_plate_number_labels", {}).get(int(plate_id))
            bounds = self._bed_bounds(int(plate_id))
            top_left = self._project_world_to_screen(np.array([bounds[0], bounds[3], 0.0], dtype=float)) if hasattr(self, "_project_world_to_screen") else None
            bottom_right = self._project_world_to_screen(np.array([bounds[1], bounds[2], 0.0], dtype=float)) if hasattr(self, "_project_world_to_screen") else None
            if top_left is None or bottom_right is None:
                if name_label is not None:
                    name_label.hide()
                if number_label is not None:
                    number_label.hide()
                continue
            if name_label is not None:
                name_label.move(int(round(top_left[0])), int(round(top_left[1] - name_label.height())))
                name_label.raise_()
                name_label.show()
            if number_label is not None:
                number_label.move(int(round(bottom_right[0] - number_label.width())), int(round(bottom_right[1])))
                number_label.raise_()
                number_label.show()

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
        self._build_fit_camera_button()
        self._build_plate_action_strip()
        self._sync_overlay_button_metrics()
        self._position_view_cube()
        self._sync_view_cube()

    def set_view_cube_visible(self, visible: bool):
        if hasattr(self, "_view_cube") and self._view_cube is not None:
            self._view_cube.setVisible(bool(visible))
            if visible:
                self._position_view_cube()
        if hasattr(self, "_fit_camera_btn") and self._fit_camera_btn is not None:
            overlay_visible = bool(getattr(self, "_plate_overlay_visible", True))
            self._fit_camera_btn.setVisible(bool(visible) and overlay_visible)

    def set_plate_overlay_visible(self, visible: bool):
        value = bool(visible)
        self._plate_overlay_visible = value
        if hasattr(self, "_plate_actions") and self._plate_actions is not None:
            self._plate_actions.setVisible(value)
        if hasattr(self, "_fit_camera_btn") and self._fit_camera_btn is not None:
            self._fit_camera_btn.setVisible(value and bool(getattr(self, "_view_cube", None) is not None and self._view_cube.isVisible()))
        if value:
            self._position_plate_action_strip()
            self._position_fit_camera_button()

    def _build_fit_camera_button(self):
        parent = cast(QtWidgets.QWidget, self)
        self._fit_camera_btn = QtWidgets.QToolButton(parent)
        self._fit_camera_btn.setObjectName("FitCameraButton")
        self._fit_camera_btn.setAutoRaise(True)
        self._fit_camera_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self._fit_camera_btn.setToolTip(
            self._t(
                "viewer.plate.fit_camera.tooltip",
                "Fit camera to scene or selected object.",
            )
        )
        self._fit_camera_btn.setIcon(self._build_overlay_icon("fit"))
        self._fit_camera_btn.clicked.connect(self.fit_camera_to_scene_or_selection)

    def _build_plate_action_strip(self):
        parent = cast(QtWidgets.QWidget, self)
        panel = QtWidgets.QFrame(parent)
        panel.setObjectName("PlateActions")
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(4)
        self._plate_actions = panel

        remove_btn = self._overlay_tool_button(
            "remove",
            self._t(
                "viewer.plate.remove.tooltip",
                "Remove current plate (if not last one)",
            ),
        )
        auto_orient_btn = self._overlay_tool_button(
            "auto_orient",
            self._t(
                "viewer.plate.auto_orient.tooltip",
                "Auto orient objects on current plate",
            ),
        )
        arrange_btn = self._overlay_tool_button(
            "arrange",
            self._t(
                "viewer.plate.arrange.tooltip",
                "Arrange objects on current plate",
            ),
        )
        lock_btn = self._overlay_tool_button(
            "lock",
            self._t(
                "viewer.plate.lock.tooltip",
                "Lock current plate",
            ),
            checkable=True,
        )
        edit_btn = self._overlay_tool_button(
            "edit",
            self._t(
                "viewer.plate.edit_name.tooltip",
                "Edit current plate name",
            ),
        )

        layout.addWidget(remove_btn)
        layout.addWidget(auto_orient_btn)
        layout.addWidget(arrange_btn)
        layout.addWidget(lock_btn)
        layout.addWidget(edit_btn)

        remove_btn.clicked.connect(self._on_plate_remove_clicked)
        auto_orient_btn.clicked.connect(self._on_plate_auto_orient_clicked)
        arrange_btn.clicked.connect(self._on_plate_arrange_clicked)
        lock_btn.toggled.connect(self._on_plate_lock_toggled)
        edit_btn.clicked.connect(self._on_plate_edit_name_clicked)

        self._plate_remove_btn = remove_btn
        self._plate_auto_orient_btn = auto_orient_btn
        self._plate_arrange_btn = arrange_btn
        self._plate_lock_btn = lock_btn
        self._plate_edit_btn = edit_btn
        if hasattr(self, "is_plate_locked"):
            self._plate_lock_btn.setChecked(bool(self.is_plate_locked()))
        self._apply_plate_overlay_theme()

    def _overlay_tool_button(self, icon_kind: str, tooltip: str, checkable: bool = False):
        btn = QtWidgets.QToolButton(self._plate_actions if hasattr(self, "_plate_actions") and self._plate_actions is not None else cast(QtWidgets.QWidget, self))
        btn.setObjectName("PlateActionButton")
        btn.setAutoRaise(True)
        btn.setCheckable(bool(checkable))
        btn.setCursor(QtCore.Qt.PointingHandCursor)
        btn.setToolTip(str(tooltip or ""))
        btn.setIcon(self._build_overlay_icon(icon_kind))
        return btn

    def _build_overlay_icon(self, kind: str, size: int | None = None) -> QtGui.QIcon:
        size = int(size if size is not None else 18)
        size = max(14, min(40, size))
        pm = QtGui.QPixmap(size, size)
        pm.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pm)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        stroke = QtGui.QPen(theme_qcolor("popup_muted_text"), 1.8)
        stroke.setCapStyle(QtCore.Qt.RoundCap)
        stroke.setJoinStyle(QtCore.Qt.RoundJoin)
        painter.setPen(stroke)
        painter.setBrush(QtCore.Qt.NoBrush)

        if kind == "remove":
            painter.drawLine(4, 4, size - 4, size - 4)
            painter.drawLine(size - 4, 4, 4, size - 4)
        elif kind == "auto_orient":
            rect = QtCore.QRectF(3.5, 3.5, size - 8, size - 8)
            painter.drawArc(rect, 30 * 16, 300 * 16)
            arrow = QtGui.QPolygonF(
                [
                    QtCore.QPointF(size - 5.0, 7.0),
                    QtCore.QPointF(size - 2.0, 7.5),
                    QtCore.QPointF(size - 4.5, 10.0),
                ]
            )
            painter.setBrush(stroke.color())
            painter.drawPolygon(arrow)
        elif kind == "arrange":
            painter.drawRoundedRect(QtCore.QRectF(3.5, 3.5, size - 7, size - 7), 1.5, 1.5)
            painter.drawLine(
                QtCore.QLineF(
                    QtCore.QPointF(3.5, 8.0),
                    QtCore.QPointF(size - 3.5, 8.0),
                )
            )
            painter.drawLine(
                QtCore.QLineF(
                    QtCore.QPointF(3.5, 12.0),
                    QtCore.QPointF(size - 3.5, 12.0),
                )
            )
        elif kind == "lock":
            painter.drawRoundedRect(QtCore.QRectF(4.0, 8.0, size - 8, size - 6), 1.5, 1.5)
            painter.drawArc(QtCore.QRectF(5.0, 2.0, size - 10, 9.0), 0, 180 * 16)
        elif kind == "edit":
            painter.drawLine(
                QtCore.QLineF(
                    QtCore.QPointF(4.0, size - 4.0),
                    QtCore.QPointF(size - 5.0, 5.0),
                )
            )
            painter.drawLine(
                QtCore.QLineF(
                    QtCore.QPointF(5.5, size - 5.5),
                    QtCore.QPointF(size - 3.5, size - 3.5),
                )
            )
            painter.drawLine(
                QtCore.QLineF(
                    QtCore.QPointF(3.5, size - 3.5),
                    QtCore.QPointF(7.0, size - 2.5),
                )
            )
        elif kind == "fit":
            inset = max(2.5, size * 0.16)
            rect = QtCore.QRectF(inset, inset, size - inset * 2, size - inset * 2)
            radius = max(3.0, size * 0.16)
            painter.drawRoundedRect(rect, radius, radius)
            cross_inset = max(2.0, size * 0.14)
            painter.drawLine(
                QtCore.QLineF(
                    QtCore.QPointF(rect.left() + cross_inset, rect.center().y()),
                    QtCore.QPointF(rect.right() - cross_inset, rect.center().y()),
                )
            )
            painter.drawLine(
                QtCore.QLineF(
                    QtCore.QPointF(rect.center().x(), rect.top() + cross_inset),
                    QtCore.QPointF(rect.center().x(), rect.bottom() - cross_inset),
                )
            )
        else:
            painter.drawEllipse(QtCore.QRectF(3.5, 3.5, size - 7, size - 7))

        painter.end()
        return QtGui.QIcon(pm)

    def _overlay_metrics(self) -> Dict[str, int]:
        cube_size = 84
        if hasattr(self, "_view_cube") and self._view_cube is not None:
            try:
                cube_size = int(self._view_cube.sizeHint().width())
            except Exception:
                cube_size = 84
        cube_size = max(96, cube_size)

        action_btn = max(28, min(56, int(round(cube_size * 0.3))))
        action_icon = max(16, min(28, int(round(action_btn * 0.56))))
        fit_btn = max(34, min(64, int(round(cube_size * 0.34))))
        fit_icon = max(16, min(30, int(round(fit_btn * 0.56))))
        spacing = max(4, int(round(action_btn * 0.16)))
        margin = max(3, int(round(action_btn * 0.12)))
        return {
            "action_btn": action_btn,
            "action_icon": action_icon,
            "fit_btn": fit_btn,
            "fit_icon": fit_icon,
            "spacing": spacing,
            "margin": margin,
        }

    def _sync_overlay_button_metrics(self):
        metrics = self._overlay_metrics()
        icon_map = {
            "_plate_remove_btn": "remove",
            "_plate_auto_orient_btn": "auto_orient",
            "_plate_arrange_btn": "arrange",
            "_plate_lock_btn": "lock",
            "_plate_edit_btn": "edit",
        }
        if hasattr(self, "_plate_actions") and self._plate_actions is not None:
            layout = self._plate_actions.layout()
            if isinstance(layout, QtWidgets.QBoxLayout):
                margin = int(metrics["margin"])
                layout.setContentsMargins(margin, margin, margin, margin)
                layout.setSpacing(int(metrics["spacing"]))
            for attr_name, kind in icon_map.items():
                btn = getattr(self, attr_name, None)
                if btn is None:
                    continue
                btn.setFixedSize(int(metrics["action_btn"]), int(metrics["action_btn"]))
                btn.setIconSize(QtCore.QSize(int(metrics["action_icon"]), int(metrics["action_icon"])))
                btn.setIcon(self._build_overlay_icon(kind, size=int(metrics["action_icon"])))
        if hasattr(self, "_fit_camera_btn") and self._fit_camera_btn is not None:
            self._fit_camera_btn.setFixedSize(int(metrics["fit_btn"]), int(metrics["fit_btn"]))
            self._fit_camera_btn.setIconSize(QtCore.QSize(int(metrics["fit_icon"]), int(metrics["fit_icon"])))
            self._fit_camera_btn.setIcon(self._build_overlay_icon("fit", size=int(metrics["fit_icon"])))
        self._apply_plate_overlay_theme()

    def _apply_plate_overlay_theme(self):
        if not hasattr(self, "_plate_actions") or self._plate_actions is None:
            return
        border = theme_qcolor("popup_border")
        bg = theme_qcolor("popup_bg")
        hover = theme_qcolor("menu_hover_bg")
        active = theme_qcolor("topbar_accent")
        panel_radius = max(6, int(round(self._plate_actions.sizeHint().width() * 0.06)))
        btn_radius = 4
        if hasattr(self, "_plate_remove_btn") and self._plate_remove_btn is not None:
            btn_radius = max(4, int(round(self._plate_remove_btn.height() * 0.18)))

        self._plate_actions.setStyleSheet(
            "QFrame#PlateActions {"
            f"background-color: {self._rgba_css(bg, 84)};"
            f"border: 1px solid {self._rgba_css(border, 150)};"
            f"border-radius: {panel_radius}px;"
            "}"
            "QToolButton#PlateActionButton {"
            "border: 1px solid transparent;"
            f"border-radius: {btn_radius}px;"
            "padding: 2px;"
            "}"
            "QToolButton#PlateActionButton:hover {"
            f"background-color: {self._rgba_css(hover, 190)};"
            f"border-color: {self._rgba_css(border, 200)};"
            "}"
            "QToolButton#PlateActionButton:checked {"
            f"background-color: {self._rgba_css(active, 220)};"
            f"border-color: {self._rgba_css(active, 255)};"
            "}"
        )
        if hasattr(self, "_fit_camera_btn") and self._fit_camera_btn is not None:
            fit_radius = max(6, int(round(self._fit_camera_btn.height() * 0.26)))
            self._fit_camera_btn.setStyleSheet(
                "QToolButton#FitCameraButton {"
                f"background-color: {self._rgba_css(bg, 104)};"
                f"border: 1px solid {self._rgba_css(border, 180)};"
                f"border-radius: {fit_radius}px;"
                "padding: 0;"
                "}"
                "QToolButton#FitCameraButton:hover {"
                f"background-color: {self._rgba_css(hover, 190)};"
                f"border-color: {self._rgba_css(active, 220)};"
                "}"
                "QToolButton#FitCameraButton:pressed {"
                f"background-color: {self._rgba_css(active, 170)};"
                f"border-color: {self._rgba_css(active, 255)};"
                "}"
            )

        icon_map = {
            "_plate_remove_btn": "remove",
            "_plate_auto_orient_btn": "auto_orient",
            "_plate_arrange_btn": "arrange",
            "_plate_lock_btn": "lock",
            "_plate_edit_btn": "edit",
        }
        for attr_name, kind in icon_map.items():
            btn = getattr(self, attr_name, None)
            if btn is None:
                continue
            icon_px = max(14, int(btn.iconSize().width()))
            btn.setIcon(self._build_overlay_icon(kind, size=icon_px))
        if hasattr(self, "_fit_camera_btn") and self._fit_camera_btn is not None:
            fit_icon_px = max(14, int(self._fit_camera_btn.iconSize().width()))
            self._fit_camera_btn.setIcon(self._build_overlay_icon("fit", size=fit_icon_px))

    def _position_fit_camera_button(self):
        if not hasattr(self, "_fit_camera_btn") or self._fit_camera_btn is None:
            return
        if not hasattr(self, "_view_cube") or self._view_cube is None:
            return
        margin = max(10, int(round(self._view_cube.sizeHint().width() * 0.1)))
        cube_rect = self._view_cube.geometry()
        x = cube_rect.right() + margin
        y = int(round(cube_rect.center().y() + cube_rect.height() * 0.16 - self._fit_camera_btn.height() * 0.5))
        max_x = max(0, self.width() - self._fit_camera_btn.width())
        max_y = max(0, self.height() - self._fit_camera_btn.height())
        self._fit_camera_btn.move(max(0, min(max_x, x)), max(0, min(max_y, y)))
        self._fit_camera_btn.raise_()

    def _plate_overlay_anchor(self) -> Tuple[float, float, float, float] | None:
        if not hasattr(self, "_project_world_to_screen") or not hasattr(self, "_bed_bounds"):
            return None
        try:
            min_x, max_x, min_y, max_y = self._bed_bounds()
        except Exception:
            return None

        corners = np.array(
            [
                [min_x, min_y, 0.0],
                [max_x, min_y, 0.0],
                [max_x, max_y, 0.0],
                [min_x, max_y, 0.0],
            ],
            dtype=float,
        )
        projected: List[Tuple[float, float]] = []
        for corner in corners:
            point = self._project_world_to_screen(corner)
            if point is None:
                return None
            x, y, _z = point
            if not np.isfinite(x) or not np.isfinite(y):
                return None
            projected.append((float(x), float(y)))

        edges = ((0, 1), (1, 2), (2, 3), (3, 0))
        best_edge = None
        best_score = -float("inf")
        for a, b in edges:
            x1, y1 = projected[a]
            x2, y2 = projected[b]
            mid_x = (x1 + x2) * 0.5
            if mid_x > best_score:
                best_score = mid_x
                best_edge = (x1, y1, x2, y2)

        if best_edge is None:
            return None

        x1, y1, x2, y2 = best_edge
        anchor_x = (x1 + x2) * 0.5
        anchor_y = (y1 + y2) * 0.5

        edge_x = x2 - x1
        edge_y = y2 - y1
        normal_x = edge_y
        normal_y = -edge_x
        normal_len = float(np.hypot(normal_x, normal_y))
        if normal_len <= 1e-6:
            normal_x, normal_y = 1.0, 0.0
        else:
            normal_x /= normal_len
            normal_y /= normal_len

        # Keep strip on the outward right side of the plate in screen space.
        if normal_x < 0.0:
            normal_x = -normal_x
            normal_y = -normal_y

        return float(anchor_x), float(anchor_y), float(normal_x), float(normal_y)

    def _position_plate_action_strip(self):
        if not hasattr(self, "_plate_actions") or self._plate_actions is None:
            return
        self._plate_actions.adjustSize()
        anchor = self._plate_overlay_anchor()
        if anchor is None:
            margin = 18
            x = max(0, self.width() - self._plate_actions.width() - margin)
            y = max(0, (self.height() - self._plate_actions.height()) // 2)
        else:
            anchor_x, anchor_y, normal_x, normal_y = anchor
            gap = float(max(8, int(round(self._plate_actions.width() * 0.18))))
            x = int(round(anchor_x + normal_x * gap))
            y = int(round(anchor_y - (self._plate_actions.height() * 0.5) + normal_y * gap))
            max_x = max(0, self.width() - self._plate_actions.width())
            max_y = max(0, self.height() - self._plate_actions.height())
            x = max(0, min(max_x, x))
            y = max(0, min(max_y, y))
        self._plate_actions.move(x, y)
        self._plate_actions.raise_()

    def _on_plate_remove_clicked(self):
        if hasattr(self, "plateRemoveRequested"):
            self.plateRemoveRequested.emit()

    def _on_plate_auto_orient_clicked(self):
        if hasattr(self, "plateAutoOrientRequested"):
            self.plateAutoOrientRequested.emit()

    def _on_plate_arrange_clicked(self):
        if hasattr(self, "plateArrangeRequested"):
            self.plateArrangeRequested.emit()

    def _on_plate_lock_toggled(self, checked: bool):
        if hasattr(self, "set_plate_locked"):
            self.set_plate_locked(bool(checked))
        if hasattr(self, "plateLockChanged"):
            self.plateLockChanged.emit(bool(checked))

    def _on_plate_edit_name_clicked(self):
        current_name = "01"
        if hasattr(self, "get_current_plate_name"):
            current_name = str(self.get_current_plate_name() or "01")

        dlg = QtWidgets.QDialog(cast(QtWidgets.QWidget, self))
        dlg.setWindowTitle(self._t("viewer.plate.rename.title", "Edit Plate Name"))
        dlg.setModal(True)
        layout = QtWidgets.QVBoxLayout(dlg)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(12)

        row = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(self._t("viewer.plate.rename.label", "Plate name"), dlg)
        edit = QtWidgets.QLineEdit(dlg)
        edit.setText(current_name)
        edit.setClearButtonEnabled(True)
        row.addWidget(label)
        row.addWidget(edit, 1)
        layout.addLayout(row)

        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, parent=dlg)
        buttons.accepted.connect(dlg.accept)
        buttons.rejected.connect(dlg.reject)
        layout.addWidget(buttons)

        if dlg.exec_() != QtWidgets.QDialog.Accepted:
            return
        value = str(edit.text() or "").strip()
        if hasattr(self, "set_current_plate_name"):
            self.set_current_plate_name(value)

    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any:
            ...
