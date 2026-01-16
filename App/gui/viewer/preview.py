from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Tuple, TYPE_CHECKING

import numpy as np
import pyqtgraph.opengl as gl
from PyQt5 import QtCore, QtGui

from ..widgets.nozzle_item import NozzleItem


class PreviewMixin:
    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any: ...

    # -------------------- gcode preview --------------------

    def set_gcode_preview(self, preview):
        self._preview_data = preview
        if preview is None or not getattr(preview, "layers", None):
            self._preview_layer_index = None
            self._preview_step_index = None
            self._preview_step_layer = None
            self._update_preview_lines()
            return
        self._preview_extrude_bins = []
        self._clear_preview_extrude_items()
        self._preview_layer_index = len(preview.layers) - 1
        self._preview_step_index = None
        self._preview_step_layer = self._preview_layer_index
        self._update_preview_lines()

    def set_preview_settings(self, settings):
        if settings is None:
            return
        try:
            base_width = float(settings.extrusion_width)
        except (TypeError, ValueError, AttributeError):
            base_width = self._preview_base_width
        if base_width <= 0.0:
            try:
                base_width = float(settings.nozzle_diameter)
            except (TypeError, ValueError, AttributeError):
                base_width = self._preview_base_width
        if base_width <= 0.0:
            base_width = self._preview_base_width
        if abs(base_width - self._preview_base_width) < 1e-6:
            return
        self._preview_base_width = base_width
        self._preview_extrude_bins = []
        self._clear_preview_extrude_items()
        self._ensure_preview_items()
        self._update_preview_lines()

    def set_models_visible(self, visible: bool):
        self._models_visible = bool(visible)
        for m in self.models.values():
            item = m.get("item")
            if item is not None:
                wireframe = bool(m.get("wireframe"))
                if self._models_visible:
                    item.setVisible(True)
                    item.opts["drawFaces"] = True
                    item.opts["drawEdges"] = wireframe
                else:
                    if wireframe:
                        item.setVisible(True)
                        item.opts["drawFaces"] = False
                        item.opts["drawEdges"] = True
                        item.meshDataChanged()
                    else:
                        item.setVisible(False)
                item.update()

    def set_platform_visible(self, visible: bool):
        self._platform_visible = bool(visible)
        if getattr(self, "_grid_item", None) is not None:
            self._grid_item.setVisible(self._platform_visible)
        self.update()

    def set_nozzle_visible(self, visible: bool):
        self._nozzle_visible = bool(visible)
        if self._nozzle_visible:
            self._ensure_nozzle_item()
            self._update_nozzle_position()
        if self._nozzle is not None:
            self._nozzle.set_visible(self._nozzle_visible)
        self.update()

    def set_preview_visible(self, visible: bool):
        self._preview_visible = bool(visible)
        for item in self._preview_items.values():
            if item is not None:
                item.setVisible(self._preview_visible)
        for item in self._preview_extrude_items:
            item.setVisible(self._preview_visible)

    def get_preview_nozzle_state(self):
        seg = self._preview_segment_for_nozzle()
        if seg is None:
            return None
        return (seg.end, float(seg.speed), bool(seg.is_extrude))

    def get_preview_progress(self):
        if self._preview_data is None or not getattr(self._preview_data, "layers", None):
            return None
        layers = self._preview_data.layers
        total = sum(len(layer.segments) for layer in layers)
        if total <= 0:
            return (0, 0)
        if self._preview_step_index is not None:
            layer_index = self._preview_step_layer
        else:
            layer_index = self._preview_layer_index
        if layer_index is None:
            layer_index = len(layers) - 1
        layer_index = max(0, min(layer_index, len(layers) - 1))
        completed = sum(len(layers[idx].segments) for idx in range(layer_index))
        layer_segments = len(layers[layer_index].segments)
        if self._preview_step_index is None:
            completed += layer_segments
        else:
            completed += max(0, min(int(self._preview_step_index), layer_segments))
        return (completed, total)

    def _preview_segment_for_nozzle(self):
        if self._preview_data is None or not getattr(self._preview_data, "layers", None):
            return None
        layers = self._preview_data.layers
        layer_index = self._preview_step_layer if self._preview_step_index is not None else self._preview_layer_index
        if layer_index is None:
            layer_index = len(layers) - 1
        layer_index = max(0, min(layer_index, len(layers) - 1))
        layer = layers[layer_index]
        segments = layer.segments
        if not segments:
            return None
        if self._preview_step_index is not None:
            idx = max(0, min(self._preview_step_index - 1, len(segments) - 1))
        else:
            idx = len(segments) - 1
        return segments[idx]

    def clear_gcode_preview(self):
        self._preview_data = None
        self._preview_layer_index = None
        self._preview_step_index = None
        self._preview_step_layer = None
        self._update_preview_lines()

    def set_preview_layer_index(self, index: int):
        if self._preview_data is None or not self._preview_data.layers:
            return
        idx = max(0, min(int(index), len(self._preview_data.layers) - 1))
        if self._preview_layer_index == idx:
            return
        self._preview_layer_index = idx
        self._preview_step_index = None
        self._preview_step_layer = idx
        self._update_preview_lines()

    def set_preview_step_index(self, step_count: int | None):
        if self._preview_data is None or not self._preview_data.layers:
            return
        layer_index = self._preview_layer_index
        if layer_index is None:
            layer_index = len(self._preview_data.layers) - 1
        layer_index = max(0, min(layer_index, len(self._preview_data.layers) - 1))
        segments = self._preview_data.layers[layer_index].segments
        max_count = len(segments)
        if step_count is None:
            self._preview_step_index = None
        else:
            self._preview_step_index = max(0, min(int(step_count), max_count))
        self._preview_step_layer = layer_index
        self._update_preview_lines()

    def preview_layer_step_count(self, layer_index: int | None = None) -> int:
        if self._preview_data is None or not self._preview_data.layers:
            return 0
        if layer_index is None:
            layer_index = self._preview_layer_index
        if layer_index is None:
            layer_index = len(self._preview_data.layers) - 1
        layer_index = max(0, min(layer_index, len(self._preview_data.layers) - 1))
        return len(self._preview_data.layers[layer_index].segments)

    def set_preview_color_mode(self, mode: str):
        mode = (mode or "").strip().lower()
        if mode not in ("feature", "speed", "flow", "width"):
            mode = "feature"
        if self._preview_color_mode == mode:
            return
        self._preview_color_mode = mode
        self._update_preview_lines()

    def set_preview_feature_filter(self, features: Optional[Sequence[str]]):
        if not features:
            self._preview_feature_filter = None
        else:
            self._preview_feature_filter = set(features)
        self._update_preview_lines()

    def _ensure_preview_items(self):
        if self._preview_items["travel"] is None:
            item = gl.GLLinePlotItem(pos=np.zeros((0, 3), dtype=float), mode="lines", width=1)
            item.setGLOptions("translucent")
            self.addItem(item)
            item.setVisible(self._preview_visible)
            self._preview_items["travel"] = item
        if not self._preview_extrude_bins:
            self._preview_extrude_bins = self._preview_width_bins()
        if not self._preview_extrude_items or \
                len(self._preview_extrude_items) != len(self._preview_extrude_bins):
            self._clear_preview_extrude_items()
            for _min_w, _max_w, line_width in self._preview_extrude_bins:
                item = gl.GLLinePlotItem(pos=np.zeros((0, 3), dtype=float),
                                         mode="lines",
                                         width=line_width)
                item.setGLOptions("opaque")
                self.addItem(item)
                item.setVisible(self._preview_visible)
                self._preview_extrude_items.append(item)

    def _preview_width_bins(self) -> List[Tuple[float, float, int]]:
        base = self._preview_base_width if self._preview_base_width > 0.0 else 0.4
        preview = self._preview_data
        min_width = float(getattr(preview, "min_width", 0.0) or 0.0)
        max_width = float(getattr(preview, "max_width", 0.0) or 0.0)

        def line_width_for(width_value: float) -> int:
            if base <= 0.0:
                return 2
            scale = max(1.0, (width_value / base) * 2.0)
            return max(1, min(8, int(round(scale))))

        if min_width <= 0.0 or max_width <= 0.0 or max_width <= min_width:
            return [
                (0.0, base * 0.75, 1),
                (base * 0.75, base * 1.05, 2),
                (base * 1.05, base * 1.4, 3),
                (base * 1.4, float("inf"), 4),
            ]

        span = max(max_width - min_width, base * 0.25)
        step = span / 4.0
        edges = [min_width + step * i for i in range(5)]
        bins: List[Tuple[float, float, int]] = []
        for idx in range(4):
            low = edges[idx]
            high = edges[idx + 1] if idx < 3 else float("inf")
            mid = (edges[idx] + edges[idx + 1]) / 2.0 if idx < 3 else max_width
            bins.append((low, high, line_width_for(mid)))
        return bins

    def _bucket_for_width(self, width: float) -> int:
        bins = self._preview_extrude_bins or self._preview_width_bins()
        for idx, (min_w, max_w, _line_width) in enumerate(bins):
            if width >= min_w and width < max_w:
                return idx
        return max(0, len(bins) - 1)

    def _clear_preview_extrude_items(self):
        for item in self._preview_extrude_items:
            try:
                self.removeItem(item)
            except Exception:
                continue
        self._preview_extrude_items = []

    def _preview_feature_color(self, feature: str):
        colors = {
            "outer_wall": (1.0, 0.6, 0.2, 1.0),
            "inner_wall": (1.0, 0.75, 0.35, 1.0),
            "sparse_infill": (0.2, 0.8, 0.3, 1.0),
            "solid_infill": (0.35, 0.85, 0.4, 1.0),
            "top_surface": (0.95, 0.75, 0.2, 1.0),
            "bottom_surface": (0.85, 0.55, 0.15, 1.0),
            "perimeter": (1.0, 0.6, 0.2, 1.0),
            "infill": (0.2, 0.8, 0.3, 1.0),
            "top": (0.95, 0.75, 0.2, 1.0),
            "bottom": (0.85, 0.55, 0.15, 1.0),
            "bridge": (0.95, 0.3, 0.3, 1.0),
            "gap_infill": (0.8, 0.6, 0.3, 1.0),
            "thin_wall": (0.9, 0.5, 0.2, 1.0),
            "support": (0.2, 0.6, 0.9, 1.0),
            "support_interface": (0.2, 0.5, 0.8, 1.0),
            "skirt": (0.7, 0.5, 0.2, 1.0),
            "brim": (0.7, 0.4, 0.2, 1.0),
            "raft": (0.5, 0.5, 0.5, 1.0),
            "ironing": (0.9, 0.9, 0.2, 1.0),
            "travel": (0.7, 0.7, 0.7, 0.2),
            "retract": (0.7, 0.7, 0.7, 0.2),
            "other": (0.8, 0.8, 0.8, 0.9),
        }
        return colors.get(feature, colors["other"])

    def _preview_color_from_scalar(self, value: float, min_val: float, max_val: float):
        if max_val <= min_val:
            return (0.2, 0.6, 0.9, 1.0)
        t = (value - min_val) / (max_val - min_val)
        t = max(0.0, min(1.0, t))
        return (t, 0.2 + (1.0 - t) * 0.6, 1.0 - t, 1.0)

    def _normalize_gl_color(self, color) -> Tuple[float, float, float, float]:
        if isinstance(color, QtGui.QColor):
            r, g, b, a = color.getRgbF()
            return (float(r), float(g), float(b), float(a))
        if isinstance(color, str):
            q = QtGui.QColor(color)
            r, g, b, a = q.getRgbF()
            return (float(r), float(g), float(b), float(a))
        if isinstance(color, (list, tuple, np.ndarray)):
            values = list(color)
            if len(values) < 3:
                return (1.0, 1.0, 1.0, 1.0)
            if len(values) == 3:
                values.append(1.0)
            vals = [float(v) for v in values[:4]]
            if max(vals[:3]) > 1.0:
                vals = [v / 255.0 for v in vals]
            return (vals[0], vals[1], vals[2], vals[3])
        return (1.0, 1.0, 1.0, 1.0)

    def _color_array(self, color, count: int) -> np.ndarray:
        count = max(0, int(count))
        rgba = self._normalize_gl_color(color)
        if count == 0:
            return np.zeros((0, 4), dtype=float)
        return np.tile(np.array(rgba, dtype=float), (count, 1))

    def _update_preview_lines(self):
        if self._preview_data is None or not getattr(self._preview_data, "layers", None):
            for item in self._preview_items.values():
                if item is not None:
                    item.setData(pos=np.zeros((0, 3), dtype=float))
            for item in self._preview_extrude_items:
                item.setData(pos=np.zeros((0, 3), dtype=float))
            self._update_nozzle_position()
            return

        self._ensure_preview_items()
        layer_index = self._preview_layer_index
        if layer_index is None:
            layer_index = len(self._preview_data.layers) - 1
        layer_index = max(0, min(layer_index, len(self._preview_data.layers) - 1))
        self._update_nozzle_position(layer_index)

        extrude_points: List[List[Tuple[float, float, float]]] = [
            [] for _ in self._preview_extrude_bins
        ]
        extrude_colors: List[List[Tuple[float, float, float, float]]] = [
            [] for _ in self._preview_extrude_bins
        ]
        travel_points = []
        travel_colors = []

        for idx, layer in enumerate(self._preview_data.layers[: layer_index + 1]):
            segments = layer.segments
            if idx == layer_index and self._preview_step_layer == layer_index:
                if self._preview_step_index is not None:
                    segments = segments[: self._preview_step_index]
            for seg in segments:
                if self._preview_feature_filter is not None and seg.feature not in self._preview_feature_filter:
                    continue
                if self._preview_color_mode == "feature":
                    color = self._preview_feature_color(seg.feature if seg.is_extrude else "travel")
                elif self._preview_color_mode == "speed":
                    color = self._preview_color_from_scalar(seg.speed,
                                                            self._preview_data.min_speed,
                                                            self._preview_data.max_speed)
                elif self._preview_color_mode == "width":
                    if seg.is_extrude:
                        width_value = seg.width if seg.width > 0.0 else self._preview_base_width
                        color = self._preview_color_from_scalar(width_value,
                                                                self._preview_data.min_width,
                                                                self._preview_data.max_width)
                    else:
                        color = self._preview_feature_color("travel")
                else:
                    if seg.is_extrude:
                        color = self._preview_color_from_scalar(seg.flow,
                                                                self._preview_data.min_flow,
                                                                self._preview_data.max_flow)
                    else:
                        color = self._preview_feature_color("travel")

                if seg.is_extrude:
                    width_value = seg.width if seg.width > 0.0 else self._preview_base_width
                    bucket = self._bucket_for_width(width_value)
                    extrude_points[bucket].extend([seg.start, seg.end])
                    extrude_colors[bucket].extend([color, color])
                else:
                    travel_points.extend([seg.start, seg.end])
                    travel_colors.extend([color, color])

        travel_item = self._preview_items["travel"]
        for item, points, colors in zip(self._preview_extrude_items, extrude_points, extrude_colors):
            if points and colors:
                item.setData(
                    pos=np.array(points, dtype=float),
                    color=np.array(colors, dtype=float),
                )
            else:
                item.setData(
                    pos=np.zeros((0, 3), dtype=float),
                    color=np.zeros((0, 4), dtype=float),
                )
        if travel_item is not None:
            if travel_points and travel_colors:
                travel_item.setData(
                    pos=np.array(travel_points, dtype=float),
                    color=np.array(travel_colors, dtype=float),
                )
            else:
                travel_item.setData(
                    pos=np.zeros((0, 3), dtype=float),
                    color=np.zeros((0, 4), dtype=float),
                )

    def _ensure_nozzle_item(self):
        if self._nozzle is not None:
            return
        nozzle = NozzleItem()
        nozzle.set_visible(self._nozzle_visible)
        self.addItem(nozzle.item)
        self._nozzle = nozzle

    def _update_nozzle_position(self, layer_index: int | None = None):
        if not self._nozzle_visible:
            return
        if self._nozzle is None:
            return
        seg = self._preview_segment_for_nozzle()
        if seg is not None:
            x = float(seg.end[0])
            y = float(seg.end[1])
            z = float(seg.end[2])
        else:
            x = 0.0
            y = 0.0
            if self._selected_model_id is not None:
                bounds = self.get_model_bounds(self._selected_model_id)
                if bounds is not None:
                    mn, mx = bounds
                    x = float((mn[0] + mx[0]) / 2.0)
                    y = float((mn[1] + mx[1]) / 2.0)
            z = 0.0
            if self._preview_data is not None and getattr(self._preview_data, "layers", None):
                if layer_index is None:
                    layer_index = self._preview_layer_index
                if layer_index is None:
                    layer_index = len(self._preview_data.layers) - 1
                if 0 <= layer_index < len(self._preview_data.layers):
                    z = float(self._preview_data.layers[layer_index].z)
        self._nozzle.update_position(x, y, z, tip_offset=2.0)

