from __future__ import annotations

import bisect
import math
from collections import OrderedDict
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
        self._preview_geometry_key = None
        self._preview_geometry_segments = None
        self._preview_geometry_widths = None
        self._preview_geometry_travel = None
        self._preview_geometry_meshes = None
        self._preview_cached_mode = None
        self._preview_color_cache = OrderedDict()
        self._preview_static_key = None
        self._preview_static_segments = None
        self._preview_static_widths = None
        self._preview_static_travel = None
        self._preview_static_meshes = None
        self._preview_dynamic_key = None
        self._preview_dynamic_segments = None
        self._preview_dynamic_widths = None
        self._preview_dynamic_travel = None
        self._preview_dynamic_meshes = None
        self._preview_color_cache_static = OrderedDict()
        if preview is None or not getattr(preview, "layers", None):
            self._preview_layer_index = None
            self._preview_step_index = None
            self._preview_step_layer = None
            self._preview_step_offsets = []
            self._preview_total_steps = 0
            self._update_preview_lines()
            return
        self._rebuild_preview_step_offsets()
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
        try:
            layer_height = float(settings.layer_height)
        except (TypeError, ValueError, AttributeError):
            layer_height = self._preview_layer_height
        if layer_height <= 0.0:
            layer_height = self._preview_layer_height
        if abs(base_width - self._preview_base_width) < 1e-6 and \
                abs(layer_height - self._preview_layer_height) < 1e-6:
            updated = False
            try:
                filament_color = getattr(settings, "filament_color", None)
                if filament_color:
                    new_color = self._normalize_gl_color(filament_color)
                    if new_color != self._preview_filament_color:
                        self._preview_filament_color = new_color
                        updated = True
            except Exception:
                updated = False
            if updated and self._preview_color_mode == "filament":
                self._preview_cached_mode = None
                self._update_preview_lines()
            return
        self._preview_base_width = base_width
        self._preview_layer_height = layer_height
        try:
            filament_color = getattr(settings, "filament_color", None)
            if filament_color:
                self._preview_filament_color = self._normalize_gl_color(filament_color)
        except Exception:
            pass
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
                    self._apply_wireframe_to_item(item, wireframe, draw_faces=True)
                else:
                    if wireframe:
                        item.setVisible(True)
                        self._apply_wireframe_to_item(item, True, draw_faces=False)
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
        for item in self._all_preview_extrude_items():
            item.setVisible(self._preview_visible)

    def set_models_preview_alpha(self, alpha: float):
        try:
            alpha_val = float(alpha)
        except (TypeError, ValueError):
            alpha_val = 1.0
        alpha_val = max(0.05, min(alpha_val, 1.0))
        self._model_preview_alpha = alpha_val
        gl_mode = "translucent" if alpha_val < 0.999 else "opaque"
        if hasattr(self, "_apply_model_color"):
            for model in self.models.values():
                item = model.get("item")
                if item is not None:
                    try:
                        item.setGLOptions(gl_mode)
                    except Exception:
                        pass
                self._apply_model_color(model)

    def get_preview_nozzle_state(self):
        seg = self._preview_segment_for_nozzle()
        if seg is None:
            return None
        return (seg.end, float(seg.speed), bool(seg.is_extrude))

    def get_preview_progress(self):
        if self._preview_data is None or not getattr(self._preview_data, "layers", None):
            return None
        total = int(getattr(self, "_preview_total_steps", 0))
        if total <= 0:
            total = sum(len(layer.segments) for layer in self._preview_data.layers)
        if total <= 0:
            return (0, 0)
        if self._preview_step_index is None:
            completed = total
        else:
            completed = max(0, min(int(self._preview_step_index), total))
        return (completed, total)

    def _preview_segment_for_nozzle(self):
        if self._preview_data is None or not getattr(self._preview_data, "layers", None):
            return None
        layers = self._preview_data.layers
        if self._preview_step_index is None:
            layer_index = self._preview_layer_index
            if layer_index is None:
                layer_index = len(layers) - 1
            layer_index = max(0, min(layer_index, len(layers) - 1))
            segments = layers[layer_index].segments
            return segments[-1] if segments else None

        step_index = max(0, int(self._preview_step_index))
        if step_index <= 0:
            return None
        if not self._preview_step_offsets:
            self._rebuild_preview_step_offsets()
        total = max(0, int(getattr(self, "_preview_total_steps", 0)))
        if total <= 0:
            return None
        step_index = min(step_index, total)
        target = step_index - 1
        offsets = self._preview_step_offsets
        layer_index = bisect.bisect_right(offsets, target) - 1
        layer_index = max(0, min(layer_index, len(layers) - 1))
        seg_index = target - offsets[layer_index]
        segments = layers[layer_index].segments
        if not segments:
            return None
        if seg_index < 0 or seg_index >= len(segments):
            return None
        return segments[seg_index]

    def clear_gcode_preview(self):
        self._preview_data = None
        self._preview_geometry_key = None
        self._preview_geometry_segments = None
        self._preview_geometry_widths = None
        self._preview_geometry_travel = None
        self._preview_geometry_meshes = None
        self._preview_cached_mode = None
        self._preview_color_cache = OrderedDict()
        self._preview_static_key = None
        self._preview_static_segments = None
        self._preview_static_widths = None
        self._preview_static_travel = None
        self._preview_static_meshes = None
        self._preview_dynamic_key = None
        self._preview_dynamic_segments = None
        self._preview_dynamic_widths = None
        self._preview_dynamic_travel = None
        self._preview_dynamic_meshes = None
        self._preview_color_cache_static = OrderedDict()
        self._preview_layer_index = None
        self._preview_step_index = None
        self._preview_step_layer = None
        self._preview_step_offsets = []
        self._preview_total_steps = 0
        self._update_preview_lines()

    def set_preview_layer_index(self, index: int):
        if self._preview_data is None or not self._preview_data.layers:
            return
        idx = max(0, min(int(index), len(self._preview_data.layers) - 1))
        if self._preview_layer_index == idx:
            return
        self._preview_layer_index = idx
        if not self._preview_step_offsets:
            self._rebuild_preview_step_offsets()
        layer = self._preview_data.layers[idx]
        step_count = self._preview_step_offsets[idx] + len(layer.segments)
        self._preview_step_index = step_count
        self._preview_step_layer = idx
        self._update_preview_lines()

    def set_preview_step_index(self, step_count: int | None):
        if self._preview_data is None or not self._preview_data.layers:
            return
        if step_count is None:
            self._preview_step_index = None
        else:
            if not self._preview_step_offsets:
                self._rebuild_preview_step_offsets()
            total = max(0, int(getattr(self, "_preview_total_steps", 0)))
            self._preview_step_index = max(0, min(int(step_count), total))
        if self._preview_step_index is None:
            layer_index = self._preview_layer_index
        else:
            layer_index, _local = self._preview_layer_slice_for_step(self._preview_step_index)
        if layer_index is None:
            layer_index = len(self._preview_data.layers) - 1
        self._preview_step_layer = layer_index
        self._preview_layer_index = layer_index
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

    def _rebuild_preview_step_offsets(self):
        self._preview_step_offsets = []
        self._preview_total_steps = 0
        if self._preview_data is None or not getattr(self._preview_data, "layers", None):
            return
        total = 0
        for layer in self._preview_data.layers:
            self._preview_step_offsets.append(total)
            total += len(layer.segments)
        self._preview_total_steps = total

    def _preview_layer_slice_for_step(self, step_count: int) -> Tuple[int, int]:
        if self._preview_data is None or not getattr(self._preview_data, "layers", None):
            return (0, 0)
        layers = self._preview_data.layers
        if not self._preview_step_offsets:
            self._rebuild_preview_step_offsets()
        total = max(0, int(getattr(self, "_preview_total_steps", 0)))
        step = max(0, min(int(step_count), total))
        if not layers:
            return (0, 0)
        offsets = self._preview_step_offsets or [0] * len(layers)
        layer_index = bisect.bisect_right(offsets, step) - 1
        layer_index = max(0, min(layer_index, len(layers) - 1))
        local_count = step - offsets[layer_index]
        local_count = max(0, min(local_count, len(layers[layer_index].segments)))
        return (layer_index, local_count)

    def set_preview_color_mode(self, mode: str):
        mode = (mode or "").strip().lower().replace(" ", "_")
        mode_map = {
            "line_type": "feature",
            "line": "feature",
        }
        mode = mode_map.get(mode, mode)
        if mode not in (
            "feature",
            "filament",
            "speed",
            "flow",
            "width",
            "layer_height",
            "layer_time",
            "fan",
            "temperature",
        ):
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
            self._preview_travel_width = 1
            self._preview_items["travel"] = item
        if not self._preview_extrude_bins:
            self._preview_extrude_bins = self._preview_width_bins()
        if not self._preview_extrude_items_static or \
                len(self._preview_extrude_items_static) != len(self._preview_extrude_bins) or \
                len(self._preview_extrude_items_dynamic) != len(self._preview_extrude_bins):
            self._clear_preview_extrude_items()
            for _min_w, _max_w, line_width in self._preview_extrude_bins:
                for target in (self._preview_extrude_items_static, self._preview_extrude_items_dynamic):
                    md = gl.MeshData(
                        vertexes=np.zeros((0, 3), dtype=float),
                        faces=np.zeros((0, 3), dtype=np.int32),
                    )
                    item = gl.GLMeshItem(meshdata=md, smooth=False, drawFaces=True,
                                         drawEdges=False, shader="shaded")
                    item.setGLOptions("opaque")
                    self.addItem(item)
                    item.setVisible(self._preview_visible)
                    target.append(item)

    def _preview_width_bins(self) -> List[Tuple[float, float, float]]:
        base = self._preview_base_width if self._preview_base_width > 0.0 else 0.4
        preview = self._preview_data
        min_width = float(getattr(preview, "min_width", 0.0) or 0.0)
        max_width = float(getattr(preview, "max_width", 0.0) or 0.0)

        if min_width <= 0.0 or max_width <= 0.0 or max_width <= min_width:
            return [
                (0.0, base * 0.75, base * 0.75),
                (base * 0.75, base * 1.05, base),
                (base * 1.05, base * 1.4, base * 1.2),
                (base * 1.4, float("inf"), base * 1.4),
            ]

        span = max(max_width - min_width, base * 0.25)
        step = span / 4.0
        edges = [min_width + step * i for i in range(5)]
        bins: List[Tuple[float, float, float]] = []
        for idx in range(4):
            low = edges[idx]
            high = edges[idx + 1] if idx < 3 else float("inf")
            mid = (edges[idx] + edges[idx + 1]) / 2.0 if idx < 3 else max_width
            bins.append((low, high, float(mid)))
        return bins

    def _bucket_for_width(self, width: float) -> int:
        bins = self._preview_extrude_bins or self._preview_width_bins()
        for idx, (min_w, max_w, _line_width) in enumerate(bins):
            if width >= min_w and width < max_w:
                return idx
        return max(0, len(bins) - 1)

    def _clear_preview_extrude_items(self):
        for item in self._all_preview_extrude_items():
            try:
                self.removeItem(item)
            except Exception:
                continue
        self._preview_extrude_items_static = []
        self._preview_extrude_items_dynamic = []

    def _all_preview_extrude_items(self):
        items = []
        items.extend(getattr(self, "_preview_extrude_items_static", []) or [])
        items.extend(getattr(self, "_preview_extrude_items_dynamic", []) or [])
        return items

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
            "support": (0.4, 0.75, 1.0, 1.0),
            "support_interface": (0.35, 0.7, 0.95, 1.0),
            "skirt": (0.7, 0.5, 0.2, 1.0),
            "brim": (0.7, 0.4, 0.2, 1.0),
            "raft": (0.5, 0.5, 0.5, 1.0),
            "ironing": (0.9, 0.9, 0.2, 1.0),
            "travel": (0.7, 0.7, 0.7, 0.2),
            "retract": (0.7, 0.7, 0.7, 0.2),
            "unretract": (0.2, 0.8, 0.8, 1.0),
            "wipe": (0.95, 0.9, 0.2, 1.0),
            "seams": (0.9, 0.9, 0.9, 1.0),
            "other": (0.3, 0.55, 0.9, 1.0),
        }
        return colors.get(feature, colors["other"])

    def _preview_filter_key(self):
        if self._preview_feature_filter is None:
            return None
        return tuple(sorted(self._preview_feature_filter))

    def _preview_static_state_key(self, layer_index: int):
        return (
            id(self._preview_data),
            layer_index,
            self._preview_filter_key(),
            round(float(self._preview_base_width), 6),
            round(float(self._preview_layer_height), 6),
        )

    def _preview_dynamic_state_key(self, layer_index: int, step_slice: int | None):
        return (
            id(self._preview_data),
            layer_index,
            step_slice,
            self._preview_filter_key(),
            round(float(self._preview_base_width), 6),
            round(float(self._preview_layer_height), 6),
        )

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

    def _preview_geometry_state_key(self, layer_index: int, step_slice: int | None):
        return (id(self._preview_data), layer_index, step_slice, self._preview_filter_key(),
                round(float(self._preview_base_width), 6), round(float(self._preview_layer_height), 6))

    def _preview_color_for_segment(self, seg) -> Tuple[float, float, float, float]:
        mode = self._preview_color_mode
        if mode == "feature":
            return self._preview_feature_color(seg.feature if seg.is_extrude else "travel")
        if mode == "filament":
            if seg.is_extrude:
                return self._preview_filament_color or self._preview_feature_color("outer_wall")
            return self._preview_feature_color("travel")
        if mode == "speed":
            return self._preview_color_from_scalar(seg.speed,
                                                 self._preview_data.min_speed,
                                                 self._preview_data.max_speed)
        if mode == "width":
            if seg.is_extrude:
                width_value = seg.width if seg.width > 0.0 else self._preview_base_width
                return self._preview_color_from_scalar(width_value,
                                                      self._preview_data.min_width,
                                                      self._preview_data.max_width)
            return self._preview_feature_color("travel")
        if mode == "flow":
            if seg.is_extrude:
                return self._preview_color_from_scalar(seg.flow,
                                                      self._preview_data.min_flow,
                                                      self._preview_data.max_flow)
            return self._preview_feature_color("travel")
        if mode == "layer_height":
            if seg.is_extrude:
                return self._preview_color_from_scalar(seg.layer_height,
                                                      self._preview_data.min_layer_height,
                                                      self._preview_data.max_layer_height)
            return self._preview_feature_color("travel")
        if mode == "layer_time":
            if seg.is_extrude:
                return self._preview_color_from_scalar(seg.layer_time,
                                                      self._preview_data.min_layer_time,
                                                      self._preview_data.max_layer_time)
            return self._preview_feature_color("travel")
        if mode == "fan":
            if seg.is_extrude:
                if self._preview_data.max_fan <= 0.0:
                    return self._preview_feature_color(seg.feature)
                return self._preview_color_from_scalar(seg.fan,
                                                      self._preview_data.min_fan,
                                                      self._preview_data.max_fan)
            return self._preview_feature_color("travel")
        if mode == "temperature":
            if seg.is_extrude:
                if self._preview_data.max_temp <= 0.0:
                    return self._preview_feature_color(seg.feature)
                return self._preview_color_from_scalar(seg.temperature,
                                                      self._preview_data.min_temp,
                                                      self._preview_data.max_temp)
            return self._preview_feature_color("travel")
        return self._preview_feature_color(seg.feature if seg.is_extrude else "travel")

    def _collect_layer_geometry(self, layer_index: int, step_slice: int | None):
        extrude_segments: List[List] = [[] for _ in self._preview_extrude_bins]
        extrude_widths: List[List[float]] = [[] for _ in self._preview_extrude_bins]
        travel_points: List[Tuple[float, float, float]] = []
        if self._preview_data is None or not getattr(self._preview_data, "layers", None):
            return extrude_segments, extrude_widths, travel_points
        if layer_index < 0 or layer_index >= len(self._preview_data.layers):
            return extrude_segments, extrude_widths, travel_points
        layer = self._preview_data.layers[layer_index]
        segments = layer.segments
        if step_slice is not None:
            segments = segments[: max(0, min(int(step_slice), len(segments)))]
        for seg in segments:
            if self._preview_feature_filter is not None and seg.feature not in self._preview_feature_filter:
                continue
            if seg.is_extrude:
                width_value = seg.width if seg.width > 0.0 else self._preview_base_width
                bucket = self._bucket_for_width(width_value)
                extrude_segments[bucket].append(seg)
                extrude_widths[bucket].append(width_value)
            else:
                travel_points.extend([seg.start, seg.end])
        return extrude_segments, extrude_widths, travel_points

    def _collect_preview_geometry(self, layer_index: int, step_slice: int | None):
        extrude_segments: List[List] = [[] for _ in self._preview_extrude_bins]
        extrude_widths: List[List[float]] = [[] for _ in self._preview_extrude_bins]
        travel_points: List[Tuple[float, float, float]] = []
        for idx, layer in enumerate(self._preview_data.layers[: layer_index + 1]):
            segments = layer.segments
            if step_slice is not None and idx == layer_index:
                segments = segments[: step_slice]
            for seg in segments:
                if self._preview_feature_filter is not None and seg.feature not in self._preview_feature_filter:
                    continue
                if seg.is_extrude:
                    width_value = seg.width if seg.width > 0.0 else self._preview_base_width
                    bucket = self._bucket_for_width(width_value)
                    extrude_segments[bucket].append(seg)
                    extrude_widths[bucket].append(width_value)
                else:
                    travel_points.extend([seg.start, seg.end])
        return extrude_segments, extrude_widths, travel_points

    def _apply_preview_mesh_colors(self, items, meshes, segments_by_bin, cache: OrderedDict | None = None):
        if cache is None:
            for item, meshdata, segments in zip(items, meshes, segments_by_bin):
                if meshdata is None or item is None:
                    continue
                if segments:
                    colors = [self._preview_color_for_segment(seg) for seg in segments]
                    face_colors = np.repeat(np.array(colors, dtype=float), 12, axis=0)
                    meshdata.setFaceColors(face_colors)
                item.setMeshData(meshdata=meshdata)
                item.setVisible(self._preview_visible and bool(segments))
            return
        if not isinstance(cache, OrderedDict):
            cache = OrderedDict()
        mode = self._preview_color_mode
        cached = cache.get(mode)
        if cached is not None and len(cached) == len(segments_by_bin):
            for item, meshdata, face_colors, segments in zip(items, meshes, cached, segments_by_bin):
                if meshdata is None or item is None:
                    continue
                if segments and face_colors is not None and len(face_colors):
                    meshdata.setFaceColors(face_colors)
                item.setMeshData(meshdata=meshdata)
                item.setVisible(self._preview_visible and bool(segments))
            cache.move_to_end(mode)
            return

        face_cache = []
        for item, meshdata, segments in zip(items, meshes, segments_by_bin):
            if meshdata is None or item is None:
                face_cache.append(np.zeros((0, 4), dtype=float))
                continue
            if segments:
                colors = [self._preview_color_for_segment(seg) for seg in segments]
                face_colors = np.repeat(np.array(colors, dtype=float), 12, axis=0)
                meshdata.setFaceColors(face_colors)
            else:
                face_colors = np.zeros((0, 4), dtype=float)
            face_cache.append(face_colors)
            item.setMeshData(meshdata=meshdata)
            item.setVisible(self._preview_visible and bool(segments))
        cache[mode] = face_cache
        if len(cache) > 4:
            cache.popitem(last=False)

    def _update_preview_lines(self):
        if self._preview_data is None or not getattr(self._preview_data, "layers", None):
            for item in self._preview_items.values():
                if item is not None:
                    item.setData(pos=np.zeros((0, 3), dtype=float))
            for item in self._all_preview_extrude_items():
                item.setMeshData(
                    meshdata=gl.MeshData(
                        vertexes=np.zeros((0, 3), dtype=float),
                        faces=np.zeros((0, 3), dtype=np.int32),
                    )
                )
            self._update_nozzle_position()
            return

        self._preview_extrude_bins = self._preview_width_bins()
        self._ensure_preview_items()
        step_slice = None
        if self._preview_step_index is None:
            layer_index = len(self._preview_data.layers) - 1
        else:
            layer_index, step_slice = self._preview_layer_slice_for_step(self._preview_step_index)
        self._update_nozzle_position(layer_index)
        travel_item = self._preview_items["travel"]
        travel_width = getattr(self, "_preview_travel_width", getattr(travel_item, "width", 1))

        if step_slice is None:
            geometry_key = self._preview_geometry_state_key(layer_index, step_slice)
            if geometry_key != self._preview_geometry_key:
                segments_by_bin, widths_by_bin, travel_points = self._collect_preview_geometry(
                    layer_index, step_slice
                )
                self._preview_geometry_segments = segments_by_bin
                self._preview_geometry_widths = widths_by_bin
                self._preview_geometry_travel = travel_points
                if isinstance(getattr(self, "_preview_color_cache_static", None), OrderedDict):
                    self._preview_color_cache_static.clear()
                meshes = []
                for segments, widths in zip(segments_by_bin, widths_by_bin):
                    segment_pairs = [(seg.start, seg.end) for seg in segments]
                    colors = [self._preview_color_for_segment(seg) for seg in segments]
                    meshes.append(self._preview_mesh_for_segments(segment_pairs, widths, colors))
                self._preview_geometry_meshes = meshes
                self._preview_geometry_key = geometry_key
                self._preview_cached_mode = self._preview_color_mode
                self._apply_preview_mesh_colors(
                    self._preview_extrude_items_static,
                    meshes,
                    segments_by_bin,
                    cache=self._preview_color_cache_static,
                )
                self._apply_preview_mesh_colors(
                    self._preview_extrude_items_dynamic,
                    [gl.MeshData(
                        vertexes=np.zeros((0, 3), dtype=float),
                        faces=np.zeros((0, 3), dtype=np.int32),
                    ) for _ in self._preview_extrude_items_dynamic],
                    [[] for _ in self._preview_extrude_items_dynamic],
                    cache=None,
                )
                if travel_item is not None:
                    if travel_points:
                        travel_color = self._preview_feature_color("travel")
                        travel_item.setData(
                            pos=np.array(travel_points, dtype=float),
                            color=self._color_array(travel_color, len(travel_points)),
                            width=travel_width,
                        )
                    else:
                        travel_item.setData(
                            pos=np.zeros((0, 3), dtype=float),
                            color=np.zeros((0, 4), dtype=float),
                            width=travel_width,
                        )
                return

            if self._preview_geometry_meshes is None or self._preview_geometry_segments is None:
                return
            if self._preview_cached_mode != self._preview_color_mode:
                self._apply_preview_mesh_colors(
                    self._preview_extrude_items_static,
                    self._preview_geometry_meshes,
                    self._preview_geometry_segments,
                    cache=self._preview_color_cache_static,
                )
                self._preview_cached_mode = self._preview_color_mode
            return

        static_layer = layer_index - 1
        static_key = self._preview_static_state_key(static_layer)
        if static_key != self._preview_static_key:
            if static_layer >= 0:
                segments_by_bin, widths_by_bin, travel_points = self._collect_preview_geometry(
                    static_layer, None
                )
            else:
                segments_by_bin = [[] for _ in self._preview_extrude_bins]
                widths_by_bin = [[] for _ in self._preview_extrude_bins]
                travel_points = []
            self._preview_static_segments = segments_by_bin
            self._preview_static_widths = widths_by_bin
            self._preview_static_travel = travel_points
            if isinstance(getattr(self, "_preview_color_cache_static", None), OrderedDict):
                self._preview_color_cache_static.clear()
            meshes = []
            for segments, widths in zip(segments_by_bin, widths_by_bin):
                segment_pairs = [(seg.start, seg.end) for seg in segments]
                colors = [self._preview_color_for_segment(seg) for seg in segments]
                meshes.append(self._preview_mesh_for_segments(segment_pairs, widths, colors))
            self._preview_static_meshes = meshes
            self._preview_static_key = static_key
            self._apply_preview_mesh_colors(
                self._preview_extrude_items_static,
                meshes,
                segments_by_bin,
                cache=self._preview_color_cache_static,
            )

        dynamic_key = self._preview_dynamic_state_key(layer_index, step_slice)
        if dynamic_key != self._preview_dynamic_key:
            segments_by_bin, widths_by_bin, travel_points = self._collect_layer_geometry(
                layer_index, step_slice
            )
            self._preview_dynamic_segments = segments_by_bin
            self._preview_dynamic_widths = widths_by_bin
            self._preview_dynamic_travel = travel_points
            meshes = []
            for segments, widths in zip(segments_by_bin, widths_by_bin):
                segment_pairs = [(seg.start, seg.end) for seg in segments]
                colors = [self._preview_color_for_segment(seg) for seg in segments]
                meshes.append(self._preview_mesh_for_segments(segment_pairs, widths, colors))
            self._preview_dynamic_meshes = meshes
            self._preview_dynamic_key = dynamic_key
            self._apply_preview_mesh_colors(
                self._preview_extrude_items_dynamic,
                meshes,
                segments_by_bin,
                cache=None,
            )
        elif self._preview_cached_mode != self._preview_color_mode:
            if self._preview_dynamic_meshes is not None and self._preview_dynamic_segments is not None:
                self._apply_preview_mesh_colors(
                    self._preview_extrude_items_dynamic,
                    self._preview_dynamic_meshes,
                    self._preview_dynamic_segments,
                    cache=None,
                )

        if self._preview_cached_mode != self._preview_color_mode:
            if self._preview_static_meshes is not None and self._preview_static_segments is not None:
                self._apply_preview_mesh_colors(
                    self._preview_extrude_items_static,
                    self._preview_static_meshes,
                    self._preview_static_segments,
                    cache=self._preview_color_cache_static,
                )
            self._preview_cached_mode = self._preview_color_mode

        if travel_item is not None:
            travel_points = []
            if self._preview_static_travel:
                travel_points.extend(self._preview_static_travel)
            if self._preview_dynamic_travel:
                travel_points.extend(self._preview_dynamic_travel)
            if travel_points:
                travel_color = self._preview_feature_color("travel")
                travel_item.setData(
                    pos=np.array(travel_points, dtype=float),
                    color=self._color_array(travel_color, len(travel_points)),
                    width=travel_width,
                )
            else:
                travel_item.setData(
                    pos=np.zeros((0, 3), dtype=float),
                    color=np.zeros((0, 4), dtype=float),
                    width=travel_width,
                )

    def _preview_mesh_for_segments(
        self,
        segments: Sequence[Tuple[Tuple[float, float, float], Tuple[float, float, float]]],
        widths: Sequence[float],
        colors: Sequence[Tuple[float, float, float, float]],
    ) -> gl.MeshData:
        if not segments:
            return gl.MeshData(
                vertexes=np.zeros((0, 3), dtype=float),
                faces=np.zeros((0, 3), dtype=np.int32),
            )

        vertices: List[List[float]] = []
        faces: List[List[int]] = []
        face_colors: List[Tuple[float, float, float, float]] = []

        for (start, end), width_value, color in zip(segments, widths, colors):
            p0 = np.array(start, dtype=float)
            p1 = np.array(end, dtype=float)
            dxy = p1[:2] - p0[:2]
            length = float(math.hypot(dxy[0], dxy[1]))
            if length < 1e-8:
                continue
            width = float(width_value if width_value > 0.0 else self._preview_base_width)
            height = float(self._preview_layer_height if self._preview_layer_height > 0.0 else 0.2)
            half_w = max(width * 0.5, self._preview_base_width * 0.25)
            half_h = max(height * 0.5, height * 0.25)
            perp = np.array([-dxy[1], dxy[0]], dtype=float) / length * half_w

            z0_low = float(p0[2] - half_h)
            z0_high = float(p0[2] + half_h)
            z1_low = float(p1[2] - half_h)
            z1_high = float(p1[2] + half_h)

            v0 = [float(p0[0] + perp[0]), float(p0[1] + perp[1]), z0_low]
            v1 = [float(p0[0] - perp[0]), float(p0[1] - perp[1]), z0_low]
            v2 = [float(p1[0] - perp[0]), float(p1[1] - perp[1]), z1_low]
            v3 = [float(p1[0] + perp[0]), float(p1[1] + perp[1]), z1_low]
            v4 = [float(p0[0] + perp[0]), float(p0[1] + perp[1]), z0_high]
            v5 = [float(p0[0] - perp[0]), float(p0[1] - perp[1]), z0_high]
            v6 = [float(p1[0] - perp[0]), float(p1[1] - perp[1]), z1_high]
            v7 = [float(p1[0] + perp[0]), float(p1[1] + perp[1]), z1_high]

            base = len(vertices)
            vertices.extend([v0, v1, v2, v3, v4, v5, v6, v7])
            faces.extend([
                [base + 0, base + 1, base + 2],
                [base + 0, base + 2, base + 3],
                [base + 4, base + 6, base + 5],
                [base + 4, base + 7, base + 6],
                [base + 0, base + 3, base + 7],
                [base + 0, base + 7, base + 4],
                [base + 1, base + 2, base + 6],
                [base + 1, base + 6, base + 5],
                [base + 0, base + 4, base + 5],
                [base + 0, base + 5, base + 1],
                [base + 3, base + 2, base + 6],
                [base + 3, base + 6, base + 7],
            ])
            face_colors.extend([color] * 12)

        if not faces:
            return gl.MeshData(
                vertexes=np.zeros((0, 3), dtype=float),
                faces=np.zeros((0, 3), dtype=np.int32),
            )

        mesh = gl.MeshData(
            vertexes=np.array(vertices, dtype=float),
            faces=np.array(faces, dtype=np.int32),
        )
        mesh.setFaceColors(np.array(face_colors, dtype=float))
        return mesh

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

