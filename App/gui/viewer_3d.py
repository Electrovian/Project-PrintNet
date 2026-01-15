import os
import math
from numbers import Real
from typing import Dict, List, Optional, Sequence, Tuple
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5 import QtCore, QtGui, QtWidgets
import trimesh

from slicer.geometry import arrange_rectangles, lowest_planar_face

from .widgets.view_cube_overlay import ViewCubeOverlay
from .widgets.nozzle_item import NozzleItem, make_cone_mesh
from .auto_orient import (
    face_normals_and_areas,
    orientation_metrics,
    pick_best_orientation,
    rotation_from_to,
    select_candidate_normals,
)
from .arrange_utils import positions_fit, spacing_candidates, spacing_with_base
from .selection_utils import rect_from_points, rect_intersects, rect_size
from .theme import theme_value, theme_qcolor
from config.defaults import DEFAULTS


class Viewer3D(gl.GLViewWidget):
    modelPicked = QtCore.pyqtSignal(int)
    modelMoved = QtCore.pyqtSignal(int, float, float)
    modelRotated = QtCore.pyqtSignal(int, float, float, float)
    selectionChanged = QtCore.pyqtSignal(list)
    simplifyRequested = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackgroundColor(theme_value("view_bg", (20, 22, 26)))

        # pyqtgraph expects a scalar here; guard it
        self._default_view = dict(DEFAULTS["viewer"]["default_view"])
        self.opts["distance"] = self._default_view["distance"] # pyright: ignore[reportArgumentType]
        if "elevation" not in self.opts:
            self.opts["elevation"] = float(self._default_view["elevation"]) # pyright: ignore[reportArgumentType]
        if "azimuth" not in self.opts:
            self.opts["azimuth"] = float(self._default_view["azimuth"]) # pyright: ignore[reportArgumentType]
        self._coerce_distance()

        self.models = {}
        self._next_model_id = 1

        self._selected_model_id = None
        self._selected_model_ids: List[int] = []
        self._dragging = False
        self._drag_start_world = None
        self._drag_start_offsets = None
        self._drag_plane_z = 0.0
        self._labels_enabled = False
        self._selection_info = None
        self._interaction_enabled = True
        self._print_stats_panel = None
        self._print_stats_data = None
        self._print_stats_visible = True
        self._preview_object_panel = None
        self._preview_object_label = None
        self._preview_object_visible = False
        self._simplify_warning = None
        self._simplify_warning_label = None
        self._simplify_warning_btn = None
        self._simplify_warning_close = None
        self._simplify_warning_model_id = None
        self._marquee_band = None
        self._marquee_active = False
        self._marquee_origin = None
        self._marquee_additive = False
        self._marquee_min_drag = 4.0

        self._snap_enabled = False
        self._snap_step = 1.0

        self._gizmo_mode = "move"
        self._gizmo_move_lines = {}
        self._gizmo_move_cones = {}
        self._gizmo_rotate_rings = {}
        self._gizmo_rotate_ticks = {}
        self._gizmo_rotate_arrows = {}
        self._gizmo_origin = None
        self._gizmo_size = 20.0
        self._gizmo_model_extent = None
        self._gizmo_drag_axis = None
        self._gizmo_drag_start_param = None
        self._gizmo_drag_start_offsets = None
        self._gizmo_rotate_axis = None
        self._gizmo_rotate_start_angle = None
        self._gizmo_rotate_start_rotation = None
        self._gizmo_rotate_start_rotations = None
        self._gizmo_rotate_start_offsets = None
        self._gizmo_rotate_pivot = None
        self._gizmo_ring_points = {}

        g = gl.GLGridItem()
        grid_size = DEFAULTS["viewer"]["grid_size"]
        grid_spacing = DEFAULTS["viewer"]["grid_spacing"]
        g.setSize(grid_size[0], grid_size[1], grid_size[2])
        g.setSpacing(grid_spacing[0], grid_spacing[1], grid_spacing[2])
        g.translate(0, 0, 0)
        g.setColor(theme_value("grid_color", (80, 80, 80, 255)))
        self._grid_item = g
        self.addItem(g)

        printer_defaults = DEFAULTS.get("printer", {})
        self._bed_size = tuple(printer_defaults.get("bed_size", (200, 200)))
        self._bed_height = float(printer_defaults.get("max_height", 200))
        self._sync_bed_grid()

        self._build_gizmo()
        self._build_view_cube()
        self._build_rotate_hud()
        self._build_selection_info()
        self._build_print_stats_panel()
        self._build_preview_object_panel()
        self._build_simplify_warning()

        self._preview_data = None
        self._preview_layer_index = None
        self._preview_color_mode = "feature"
        self._preview_items: Dict[str, Optional[gl.GLLinePlotItem]] = {
            "travel": None,
        }
        self._preview_extrude_items: List[gl.GLLinePlotItem] = []
        self._preview_extrude_bins: List[Tuple[float, float, int]] = []
        self._preview_base_width = 0.4
        self._preview_feature_filter: Optional[set[str]] = None
        self._preview_step_index = None
        self._preview_step_layer = None
        self._preview_visible = False
        self._models_visible = True
        self._platform_visible = True
        self._nozzle_visible = False
        self._nozzle = None

    # -------------------- hardening --------------------

    def _coerce_distance(self):
        d = self.opts.get("distance", 300.0)
        try:
            self.opts["distance"] = float(d) # pyright: ignore[reportArgumentType]
            return
        except (TypeError, ValueError):
            try:
                self.opts["distance"] = float(d[0])  # type: ignore[index]
                return
            except (TypeError, ValueError, IndexError):
                self.opts["distance"] = 300.0 # pyright: ignore[reportArgumentType]

    def _coerce_float(self, value, default: float) -> float:
        try:
            if isinstance(value, (int, float, np.floating)):
                return float(value)
            if isinstance(value, (list, tuple)) and value:
                return float(value[0])
        except Exception:
            return float(default)
        return float(default)

    def _safe_gl_update(self, func, *args, **kwargs) -> bool:
        try:
            func(*args, **kwargs)
        except Exception:
            return False
        return True

    def _update_gl_line(self, item, color):
        pos = item.pos if item.pos is not None else np.zeros((0, 3), dtype=float)
        color_arr = self._color_array(color, len(pos))
        item.setData(pos=pos, color=color_arr, width=item.width)

    def paintGL(self, *args, **kwargs):
        self._coerce_distance()
        self._sync_view_cube()
        return super().paintGL(*args, **kwargs)

    # -------------------- public helpers --------------------

    def set_selected_model(self, model_id: int | None):
        ids = [model_id] if model_id is not None else []
        self.set_selected_models(ids)

    def set_selected_models(self, model_ids: Sequence[int], emit_signal: bool = True):
        ids = [mid for mid in model_ids if mid in self.models]
        self._selected_model_ids = ids
        self._selected_model_id = ids[0] if ids else None
        self._update_gizmo()
        self._update_selection_info()
        if self._preview_object_visible:
            self._update_preview_object_label()
        self._update_simplify_warning()
        if emit_signal:
            self.selectionChanged.emit(list(self._selected_model_ids))

    def get_selected_model_ids(self) -> List[int]:
        return list(self._selected_model_ids)

    def set_gizmo_mode(self, mode: str):
        self._gizmo_mode = mode
        self._gizmo_drag_axis = None
        self._gizmo_rotate_axis = None
        if mode != "rotate":
            self._hide_rotate_hud()
        self._update_gizmo()

    def set_interaction_enabled(self, enabled: bool):
        self._interaction_enabled = bool(enabled)
        if not self._interaction_enabled:
            self._dragging = False
            self._gizmo_drag_axis = None
            self._gizmo_rotate_axis = None
            self._hide_rotate_hud()
        self._update_gizmo()

    def apply_theme(self):
        self.setBackgroundColor(theme_value("view_bg", (20, 22, 26)))
        if getattr(self, "_grid_item", None) is not None:
            self._grid_item.setColor(theme_value("grid_color", (80, 80, 80, 255)))

        for axis, key in (("x", "gizmo_x"), ("y", "gizmo_y"), ("z", "gizmo_z")):
            line = self._gizmo_move_lines.get(axis)
            if line is not None:
                self._safe_gl_update(self._update_gl_line, line, theme_value(key))
            cone = self._gizmo_move_cones.get(axis)
            if cone is not None:
                self._safe_gl_update(cone.setColor, theme_value(key))

            ring = self._gizmo_rotate_rings.get(axis)
            if ring is not None:
                self._safe_gl_update(self._update_gl_line, ring, theme_value(key))
            ticks = self._gizmo_rotate_ticks.get(axis)
            if ticks is not None:
                self._safe_gl_update(self._update_gl_line, ticks, theme_value("gizmo_tick"))
            arrows = self._gizmo_rotate_arrows.get(axis)
            if arrows is not None:
                self._safe_gl_update(arrows.setColor, theme_value(key))

        for m in self.models.values():
            self._apply_model_color(m)

        if hasattr(self, "_view_cube") and self._view_cube is not None:
            self._view_cube.apply_theme()
        self._update_rotate_hud_style()
        self._update_selection_info_style()
        self._update_print_stats_style()
        self._update_preview_object_style()
        self._update_simplify_warning_style()
        self._update_marquee_style()
        self._update_gizmo()
        self._update_preview_lines()

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
                item.setVisible(self._models_visible)

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
        panel = QtWidgets.QFrame(self)
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
        panel = QtWidgets.QFrame(self)
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
        panel = QtWidgets.QFrame(self)
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
        panel = QtWidgets.QFrame(self)
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
        if triangles <= 100000:
            self._simplify_warning.setVisible(False)
            return
        name = (model.get("name") or "").strip() or f"Model {model_id}"
        if triangles >= 1000000:
            msg = (f"Processing model '{name}' with more than 1M triangles could be slow. "
                   "It is highly recommended to simplify the model.")
        else:
            msg = (f"Model '{name}' has {triangles:,} triangles. "
                   "Simplifying can improve performance.")
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

    # -------------------- marquee selection --------------------

    def _ensure_marquee_band(self):
        if self._marquee_band is None:
            band = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
            band.hide()
            self._marquee_band = band
            self._update_marquee_style()

    def _update_marquee_style(self):
        if self._marquee_band is None:
            return
        accent = theme_qcolor("topbar_accent")
        border = QtGui.QColor(accent)
        border.setAlpha(220)
        fill = QtGui.QColor(accent)
        fill.setAlpha(60)
        self._marquee_band.setStyleSheet(
            "QRubberBand {"
            f"border: 1px solid rgba({border.red()}, {border.green()}, {border.blue()}, {border.alpha()});"
            f"background-color: rgba({fill.red()}, {fill.green()}, {fill.blue()}, {fill.alpha()});"
            "}"
        )

    def _marquee_rect(self, pos: QtCore.QPoint) -> QtCore.QRect:
        if self._marquee_origin is None:
            return QtCore.QRect()
        rect = rect_from_points(
            (float(self._marquee_origin.x()), float(self._marquee_origin.y())),
            (float(pos.x()), float(pos.y())),
        )
        return QtCore.QRect(int(rect[0]), int(rect[1]),
                            int(rect[2] - rect[0]), int(rect[3] - rect[1]))

    def _start_marquee(self, pos: QtCore.QPoint, additive: bool):
        self._ensure_marquee_band()
        self._marquee_active = True
        self._marquee_origin = QtCore.QPoint(pos)
        self._marquee_additive = bool(additive)
        if self._marquee_band is not None:
            self._marquee_band.setGeometry(self._marquee_rect(pos))
            self._marquee_band.show()

    def _update_marquee(self, pos: QtCore.QPoint):
        if not self._marquee_active or self._marquee_band is None:
            return
        self._marquee_band.setGeometry(self._marquee_rect(pos))

    def _finish_marquee(self, pos: QtCore.QPoint):
        if not self._marquee_active:
            return
        origin = self._marquee_origin
        if origin is None:
            return
        rect_tuple = rect_from_points(
            (float(origin.x()), float(origin.y())),
            (float(pos.x()), float(pos.y())),
        )
        if self._marquee_band is not None:
            self._marquee_band.hide()
        self._marquee_active = False
        self._marquee_origin = None

        width, height = rect_size(rect_tuple)
        if width < self._marquee_min_drag and height < self._marquee_min_drag:
            picked = self._pick_model_at(pos)
            if picked is None:
                if not self._marquee_additive:
                    self.set_selected_models([])
                return
            if self._marquee_additive:
                selected = set(self._selected_model_ids)
                if picked in selected:
                    selected.remove(picked)
                else:
                    selected.add(picked)
                self.set_selected_models(list(selected))
            else:
                self.set_selected_models([picked])
            self.modelPicked.emit(picked)
            return

        self._select_models_in_rect(rect_tuple, additive=self._marquee_additive)

    def _project_bounds_to_screen_rect(self, bounds) -> Tuple[float, float, float, float] | None:
        if bounds is None:
            return None
        mn, mx = bounds
        try:
            mn = np.array(mn, dtype=float).reshape(3)
            mx = np.array(mx, dtype=float).reshape(3)
        except Exception:
            return None
        if not np.all(np.isfinite(mn)) or not np.all(np.isfinite(mx)):
            return None
        if np.any(mx < mn):
            mn, mx = np.minimum(mn, mx), np.maximum(mn, mx)
        corners = np.array(
            [
                [mn[0], mn[1], mn[2]],
                [mn[0], mn[1], mx[2]],
                [mn[0], mx[1], mn[2]],
                [mn[0], mx[1], mx[2]],
                [mx[0], mn[1], mn[2]],
                [mx[0], mn[1], mx[2]],
                [mx[0], mx[1], mn[2]],
                [mx[0], mx[1], mx[2]],
            ],
            dtype=float,
        )
        proj = [self._project_world_to_screen(c) for c in corners]
        proj = [p for p in proj if p is not None]
        if len(proj) < 4:
            return None
        xs = [p[0] for p in proj]
        ys = [p[1] for p in proj]
        return (float(min(xs)), float(min(ys)), float(max(xs)), float(max(ys)))

    def _select_models_in_rect(self, rect: Tuple[float, float, float, float], additive: bool = False):
        selected = set(self._selected_model_ids) if additive else set()
        if not self._models_visible:
            self.set_selected_models(list(selected))
            return
        for mid, m in self.models.items():
            screen_rect = self._project_bounds_to_screen_rect(m.get("bounds"))
            if screen_rect is None:
                continue
            if rect_intersects(rect, screen_rect):
                selected.add(mid)
        self.set_selected_models(list(selected))

    # -------------------- model management --------------------

    def add_model_from_data(self, name: str, path: str, vertices, faces):
        model_id = self._next_model_id
        self._next_model_id += 1

        safe_name = (name or "").strip() or os.path.basename(path) or f"Model {model_id}"

        v = np.asarray(vertices, dtype=float)
        f = np.asarray(faces, dtype=int)

        base_mn = v.min(axis=0)
        base_mx = v.max(axis=0)
        pivot = (base_mn + base_mx) / 2.0

        self.models[model_id] = {
            "id": model_id,
            "path": path,
            "name": safe_name,
            "base_vertices": v,
            "faces": f,
            "base_volume": None,
            "item": None,
            "scale": 1.0,
            "rotation": np.array([0.0, 0.0, 0.0], dtype=float),
            "offset": np.array([0.0, 0.0, 0.0], dtype=float),
            "pivot": np.array(pivot, dtype=float),
            "bounds": None,
            "out_of_bounds": False,
            "wireframe": False,
        }

        self._create_or_update_mesh_item(model_id)

        mn = v.min(axis=0)
        mx = v.max(axis=0)
        size = float(np.max(mx - mn))
        bed_span = max(float(self._bed_size[0]), float(self._bed_size[1]), size)

        self.opts["center"] = pg.Vector(0.0, 0.0, 0.0) # pyright: ignore[reportArgumentType]
        self.opts["distance"] = float(max(bed_span * 2.0, 200.0)) # pyright: ignore[reportArgumentType]
        self._coerce_distance()
        self.update()
        return model_id

    def replace_model_mesh(self, model_id: int, vertices, faces) -> bool:
        m = self.models.get(model_id)
        if not m:
            return False
        v = np.asarray(vertices, dtype=float)
        f = np.asarray(faces, dtype=int)
        if v.size == 0 or f.size == 0:
            return False
        m["base_vertices"] = v
        m["faces"] = f
        m["base_volume"] = None
        self._create_or_update_mesh_item(model_id)
        self._update_selection_info()
        self.update()
        return True

    def remove_model(self, model_id: int):
        m = self.models.get(model_id)
        if not m:
            return
        if m.get("item") is not None:
            self.removeItem(m["item"])
        del self.models[model_id]
        if model_id in self._selected_model_ids:
            self._selected_model_ids = [mid for mid in self._selected_model_ids if mid != model_id]
        if self._selected_model_id == model_id:
            self._selected_model_id = self._selected_model_ids[0] if self._selected_model_ids else None
        self._update_gizmo()
        self._update_selection_info()
        self.update()

    def clear_all_models(self):
        for mid in list(self.models.keys()):
            self.remove_model(mid)

    def get_model_ids(self):
        return list(self.models.keys())

    def get_model_name(self, model_id: int):
        m = self.models.get(model_id)
        return m["name"] if m else None

    def get_model_path(self, model_id: int):
        m = self.models.get(model_id)
        return m["path"] if m else None

    def get_model_transform(self, model_id: int):
        m = self.models.get(model_id)
        if not m:
            return None
        scale_vec = self._normalize_scale(m.get("scale", 1.0))
        return scale_vec, np.array(m.get("offset", [0.0, 0.0, 0.0]), dtype=float)

    def get_model_bounds(self, model_id: int):
        m = self.models.get(model_id)
        if not m:
            return None
        return m.get("bounds")

    def get_model_rotation(self, model_id: int):
        m = self.models.get(model_id)
        if not m:
            return None
        rot = m.get("rotation")
        if rot is None:
            return np.array([0.0, 0.0, 0.0], dtype=float)
        return np.array(rot, dtype=float)

    def set_model_wireframe(self, model_id: int, enabled: bool):
        m = self.models.get(model_id)
        if m is None:
            return
        item = m.get("item")
        if item is None:
            return
        m["wireframe"] = bool(enabled)
        item.opts["drawEdges"] = bool(enabled)
        item.opts["drawFaces"] = True
        item.update()

    def get_model_mesh_data(self, model_id: int):
        m = self.models.get(model_id)
        if not m:
            return None
        result = self._compute_transformed_vertices(m)
        if result is None:
            return None
        v, off, mn, mx = result
        if not np.allclose(off, np.array(m.get("offset", [0.0, 0.0, 0.0]), dtype=float)):
            m["offset"] = off
        m["bounds"] = (mn, mx)
        self._update_bed_state(model_id)
        return v, m.get("faces")

    # -------------------- transforms --------------------

    def _normalize_scale(self, scale) -> np.ndarray:
        if isinstance(scale, np.ndarray):
            vec = scale.astype(float)
            if vec.shape == (3,):
                return vec
            if vec.size == 1:
                s = float(vec.reshape(-1)[0])
                return np.array([s, s, s], dtype=float)
        if isinstance(scale, (list, tuple)) and len(scale) == 3:
            return np.array([float(scale[0]), float(scale[1]), float(scale[2])], dtype=float)
        if isinstance(scale, Real):
            s = float(scale)
            return np.array([s, s, s], dtype=float)
        return np.array([1.0, 1.0, 1.0], dtype=float)

    def _normalize_vec3(self, value, default=None):
        if value is None:
            return default
        try:
            arr = np.asarray(value, dtype=float).reshape(-1)
        except Exception:
            return default
        if arr.size != 3:
            return default
        return arr.astype(float)

    def _normalize_vec2(self, value, default=None):
        if value is None:
            return default
        try:
            arr = np.asarray(value, dtype=float).reshape(-1)
        except Exception:
            return default
        if arr.size != 2:
            return default
        return arr.astype(float)

    def set_model_transform(
        self,
        model_id: int,
        scale: float | tuple[float, float, float] | list[float] | np.ndarray | None = None,
        offset_xy: tuple[float, float] | list[float] | np.ndarray | None = None,
        offset_xyz: tuple[float, float, float] | list[float] | np.ndarray | None = None,
        rotation_xyz: tuple[float, float, float] | list[float] | np.ndarray | None = None,
    ):
        m = self.models.get(model_id)
        if not m:
            return

        changed = False

        if scale is not None:
            new_scale = self._normalize_scale(scale)
            cur_vec = self._normalize_scale(m.get("scale", 1.0))
            if not np.allclose(cur_vec, new_scale):
                m["scale"] = new_scale
                changed = True

        if rotation_xyz is not None:
            cur_rot = np.array(m.get("rotation", [0.0, 0.0, 0.0]), dtype=float)
            new_rot = self._normalize_vec3(rotation_xyz, default=cur_rot)
            if new_rot is None:
                new_rot = cur_rot
            if not np.allclose(cur_rot, new_rot):
                m["rotation"] = new_rot
                changed = True

        if offset_xyz is not None:
            new_offset = self._normalize_vec3(offset_xyz)
        elif offset_xy is not None:
            xy = self._normalize_vec2(offset_xy)
            if xy is not None:
                z = float(m["offset"][2]) if m.get("offset") is not None else 0.0
                new_offset = np.array([xy[0], xy[1], z], dtype=float)
            else:
                new_offset = None
        else:
            new_offset = None

        if new_offset is not None:
            cur_offset = np.array(m.get("offset", [0.0, 0.0, 0.0]), dtype=float)
            if not np.allclose(cur_offset, new_offset):
                m["offset"] = new_offset
                changed = True

        if not changed:
            return

        self._create_or_update_mesh_item(model_id)
        if self._selected_model_id == model_id:
            self._update_gizmo()
            self._update_selection_info()
        self.update()

    # -------------------- mouse interaction --------------------

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        if not self._interaction_enabled:
            super().mousePressEvent(ev)
            return
        if ev.button() == QtCore.Qt.MiddleButton:
            self._cancel_interaction()
            super().mousePressEvent(ev)
            return
        if ev.button() == QtCore.Qt.LeftButton:
            ctrl_down = bool(ev.modifiers() & QtCore.Qt.ControlModifier)
            shift_down = bool(ev.modifiers() & QtCore.Qt.ShiftModifier)
            if shift_down:
                self._start_marquee(ev.pos(), additive=ctrl_down)
                ev.accept()
                return
            if self._gizmo_mode == "move":
                axis = self._pick_gizmo_axis(ev.pos())
                if axis is not None:
                    if self._begin_gizmo_drag(axis, ev.pos()):
                        ev.accept()
                        return
            elif self._gizmo_mode == "rotate":
                axis = self._pick_rotate_axis(ev.pos())
                if axis is not None:
                    if self._begin_rotate_drag(axis, ev.pos()):
                        ev.accept()
                        return

            # 1) Try to pick a model under cursor
            picked = self._pick_model_at(ev.pos())
            if picked is not None:
                if ctrl_down:
                    selected = set(self._selected_model_ids)
                    if picked in selected:
                        selected.remove(picked)
                    else:
                        selected.add(picked)
                    self.set_selected_models(list(selected))
                else:
                    if picked in self._selected_model_ids:
                        ordered = [picked] + [mid for mid in self._selected_model_ids if mid != picked]
                        self.set_selected_models(ordered)
                    else:
                        self.set_selected_models([picked])
                self.modelPicked.emit(picked)

            # 2) Allow drag of selected model even if pick missed (Bambu-like)
            if self._selected_model_id is not None:
                plane_z = 0.0
                bounds_list = [self.models[mid].get("bounds") for mid in self._selected_model_ids if mid in self.models]
                bounds_list = [b for b in bounds_list if b is not None]
                if bounds_list:
                    try:
                        plane_z = float(min(b[0][2] for b in bounds_list))
                    except Exception:
                        plane_z = 0.0
                hit = self._mouse_to_plane(ev.pos(), plane_z)
                if hit is None:
                    hit = self._mouse_to_plane_z0(ev.pos())
                if hit is not None:
                    self._dragging = True
                    self._drag_start_world = hit
                    self._drag_plane_z = plane_z

                    offsets = {}
                    for mid in self._selected_model_ids or [self._selected_model_id]:
                        m = self.models.get(mid)
                        if m is not None:
                            offsets[mid] = np.array(m.get("offset", [0.0, 0.0, 0.0]), dtype=float)
                    self._drag_start_offsets = offsets if offsets else None

                    ev.accept()
                    return

        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent):
        if not self._interaction_enabled:
            super().mouseMoveEvent(ev)
            return
        if bool(ev.buttons() & QtCore.Qt.MiddleButton):
            self._cancel_interaction()
            super().mouseMoveEvent(ev)
            return
        if self._marquee_active and bool(ev.buttons() & QtCore.Qt.LeftButton):
            self._update_marquee(ev.pos())
            ev.accept()
            return
        if self._gizmo_rotate_axis is not None and bool(ev.buttons() & QtCore.Qt.LeftButton):
            if self._selected_model_id is None:
                ev.accept()
                return
            angle = self._rotate_angle_from_mouse(ev.pos(), self._gizmo_rotate_axis)
            if angle is None or self._gizmo_rotate_start_angle is None or self._gizmo_rotate_start_rotation is None:
                ev.accept()
                return
            delta = float(angle - self._gizmo_rotate_start_angle)
            delta_deg = math.degrees(delta)
            axis_idx = {"x": 0, "y": 1, "z": 2}[self._gizmo_rotate_axis]
            rotations = self._gizmo_rotate_start_rotations or {}
            offsets = self._gizmo_rotate_start_offsets or {}
            pivot = self._gizmo_rotate_pivot
            multi = len(rotations) > 1 and pivot is not None

            if self._gizmo_rotate_axis == "x":
                rot_delta = self._rotation_matrix(delta_deg, 0.0, 0.0)
            elif self._gizmo_rotate_axis == "y":
                rot_delta = self._rotation_matrix(0.0, delta_deg, 0.0)
            else:
                rot_delta = self._rotation_matrix(0.0, 0.0, delta_deg)

            for mid, start_rot in rotations.items():
                rot = np.array(start_rot, dtype=float)
                rot[axis_idx] = rot[axis_idx] + delta_deg
                new_offset = None
                if multi and mid in offsets:
                    vec = offsets[mid] - pivot
                    vec_rot = vec @ rot_delta.T
                    new_offset = pivot + vec_rot
                if new_offset is not None:
                    self.set_model_transform(mid, rotation_xyz=rot, offset_xyz=new_offset)
                else:
                    self.set_model_transform(mid, rotation_xyz=rot)
                if mid == self._selected_model_id:
                    self.modelRotated.emit(mid, float(rot[0]), float(rot[1]), float(rot[2]))
            axis_label = self._gizmo_rotate_axis.upper()
            primary_rot = rotations.get(self._selected_model_id, self._gizmo_rotate_start_rotation)
            if primary_rot is not None:
                value = float(np.array(primary_rot, dtype=float)[axis_idx] + delta_deg)
                self._show_rotate_hud(ev.pos(), axis_label, value)
            ev.accept()
            return

        if self._gizmo_drag_axis is not None and bool(ev.buttons() & QtCore.Qt.LeftButton):
            if self._selected_model_id is None:
                ev.accept()
                return

            if self._gizmo_origin is None:
                ev.accept()
                return

            axis_dir = self._gizmo_axis_direction(self._gizmo_drag_axis)
            if axis_dir is None:
                ev.accept()
                return

            param = self._axis_param_from_mouse(ev.pos(), self._gizmo_origin, axis_dir)
            if param is None or self._gizmo_drag_start_param is None or self._gizmo_drag_start_offsets is None:
                ev.accept()
                return

            delta = float(param - self._gizmo_drag_start_param)
            axis_idx = {"x": 0, "y": 1, "z": 2}[self._gizmo_drag_axis]
            for mid, start_offset in self._gizmo_drag_start_offsets.items():
                new_offset = np.array(start_offset, dtype=float) + axis_dir * delta
                if self._snap_enabled:
                    step = self._snap_step
                    new_offset[axis_idx] = round(float(new_offset[axis_idx]) / step) * step
                self.set_model_transform(mid, offset_xyz=new_offset)
                if mid == self._selected_model_id:
                    self.modelMoved.emit(mid, float(new_offset[0]), float(new_offset[1]))
            ev.accept()
            return

        if self._dragging and bool(ev.buttons() & QtCore.Qt.LeftButton):
            if self._selected_model_id is None:
                ev.accept()
                return

            hit = self._mouse_to_plane(ev.pos(), self._drag_plane_z)
            if hit is None:
                hit = self._mouse_to_plane_z0(ev.pos())
            if hit is None or self._drag_start_world is None or self._drag_start_offsets is None:
                ev.accept()
                return

            dx = float(hit[0] - self._drag_start_world[0])
            dy = float(hit[1] - self._drag_start_world[1])

            for mid, start_offset in self._drag_start_offsets.items():
                new_x = float(start_offset[0]) + dx
                new_y = float(start_offset[1]) + dy
                if self._snap_enabled:
                    step = self._snap_step
                    new_x = round(new_x / step) * step
                    new_y = round(new_y / step) * step
                self.set_model_transform(mid, offset_xy=(new_x, new_y))
                if mid == self._selected_model_id:
                    self.modelMoved.emit(mid, float(new_x), float(new_y))
            ev.accept()
            return

        super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        if not self._interaction_enabled:
            super().mouseReleaseEvent(ev)
            return
        if ev.button() == QtCore.Qt.MiddleButton:
            self._cancel_interaction()
            super().mouseReleaseEvent(ev)
            return
        if ev.button() == QtCore.Qt.LeftButton and self._marquee_active:
            self._finish_marquee(ev.pos())
            ev.accept()
            return
        if ev.button() == QtCore.Qt.LeftButton and self._dragging:
            self._dragging = False
            self._drag_start_world = None
            self._drag_start_offsets = None
            self._drag_plane_z = 0.0
            ev.accept()
            return
        if ev.button() == QtCore.Qt.LeftButton and self._gizmo_rotate_axis is not None:
            self._gizmo_rotate_axis = None
            self._gizmo_rotate_start_angle = None
            self._gizmo_rotate_start_rotation = None
            self._gizmo_rotate_start_rotations = None
            self._gizmo_rotate_start_offsets = None
            self._gizmo_rotate_pivot = None
            self._hide_rotate_hud()
            self._update_gizmo()
            ev.accept()
            return
        if ev.button() == QtCore.Qt.LeftButton and self._gizmo_drag_axis is not None:
            self._gizmo_drag_axis = None
            self._gizmo_drag_start_param = None
            self._gizmo_drag_start_offsets = None
            ev.accept()
            return
        super().mouseReleaseEvent(ev)

    # -------------------- mesh rebuild + bounds --------------------

    def _create_or_update_mesh_item(self, model_id: int):
        m = self.models[model_id]
        result = self._compute_transformed_vertices(m)
        if result is None:
            m["bounds"] = None
            return
        v, off, mn, mx = result
        m["offset"] = off
        m["bounds"] = (mn, mx)
        self._update_bed_state(model_id)

        md = gl.MeshData(vertexes=v, faces=m["faces"])
        base_color = theme_value("mesh_color", (0.0, 0.9, 0.4, 0.9))
        warn_color = theme_value("mesh_warning", (1.0, 0.25, 0.2, 0.95))
        color = warn_color if m.get("out_of_bounds") else base_color

        item = m.get("item")
        if item is None:
            item = gl.GLMeshItem(meshdata=md, smooth=False, color=color, shader="shaded")
            self.addItem(item)
            item.setVisible(self._models_visible)
            m["item"] = item
        else:
            item.setMeshData(meshdata=md)
            self._apply_model_color(m)
            item.setVisible(self._models_visible)
        if m.get("wireframe"):
            item.opts["drawEdges"] = True
            item.opts["drawFaces"] = True

    def _compute_transformed_vertices(self, model: dict):
        v0 = model.get("base_vertices")
        if v0 is None or len(v0) == 0:
            return None
        s = self._normalize_scale(model.get("scale", 1.0))
        off = np.array(model.get("offset", [0.0, 0.0, 0.0]), dtype=float)
        rot = np.array(model.get("rotation", [0.0, 0.0, 0.0]), dtype=float)
        pivot = model.get("pivot", np.zeros(3, dtype=float))

        v = (v0 - pivot) * s
        R = self._rotation_matrix(float(rot[0]), float(rot[1]), float(rot[2]))
        v = v @ R.T
        v = v + pivot + off

        mn = v.min(axis=0)
        if float(mn[2]) < 0.0:
            lift = -float(mn[2])
            off = np.array([float(off[0]), float(off[1]), float(off[2]) + lift], dtype=float)
            v = (v0 - pivot) * s
            v = v @ R.T
            v = v + pivot + off
            mn = v.min(axis=0)
        mx = v.max(axis=0)
        return v, off, mn, mx

    def _rotation_matrix(self, rx_deg: float, ry_deg: float, rz_deg: float):
        rx = np.deg2rad(rx_deg)
        ry = np.deg2rad(ry_deg)
        rz = np.deg2rad(rz_deg)

        cx, sx = float(np.cos(rx)), float(np.sin(rx))
        cy, sy = float(np.cos(ry)), float(np.sin(ry))
        cz, sz = float(np.cos(rz)), float(np.sin(rz))

        Rx = np.array(
            [
                [1.0, 0.0, 0.0],
                [0.0, cx, -sx],
                [0.0, sx, cx],
            ],
            dtype=float,
        )
        Ry = np.array(
            [
                [cy, 0.0, sy],
                [0.0, 1.0, 0.0],
                [-sy, 0.0, cy],
            ],
            dtype=float,
        )
        Rz = np.array(
            [
                [cz, -sz, 0.0],
                [sz, cz, 0.0],
                [0.0, 0.0, 1.0],
            ],
            dtype=float,
        )

        return Rz @ Ry @ Rx

    # -------------------- view cube --------------------

    def _build_view_cube(self):
        self._view_cube = ViewCubeOverlay(self)
        self._view_cube.viewRequested.connect(self._set_view_from_cube)
        self._view_cube.homeRequested.connect(self.reset_view)
        self._position_view_cube()
        self._sync_view_cube()

    def set_view_cube_visible(self, visible: bool):
        if hasattr(self, "_view_cube") and self._view_cube is not None:
            self._view_cube.setVisible(bool(visible))
            if visible:
                self._position_view_cube()

    # -------------------- arrange / lay on face --------------------

    def arrange_models(
        self,
        model_ids: list[int],
        spacing: float,
        auto_rotate: bool = False,
        align_y: bool = False,
    ) -> bool:
        ids = [mid for mid in model_ids if mid in self.models]
        if not ids:
            return False

        base_spacing = float(DEFAULTS["popups"]["arrange"].get("spacing_base", 3.0))
        extra_spacing = max(0.0, float(spacing))

        model_info = []
        for mid in ids:
            m = self.models.get(mid)
            if m is None:
                continue
            bounds = m.get("bounds")
            if bounds is None:
                continue
            mn, mx = bounds
            width = float(mx[0] - mn[0])
            depth = float(mx[1] - mn[1])

            if auto_rotate and width > depth:
                rot = np.array(m.get("rotation", [0.0, 0.0, 0.0]), dtype=float)
                rot[2] = (rot[2] + 90.0) % 360.0
                self.set_model_transform(mid, rotation_xyz=rot, offset_xyz=m.get("offset", [0.0, 0.0, 0.0]))
                m = self.models.get(mid)
                bounds = m.get("bounds") if m is not None else None
                if bounds is None:
                    continue
                mn, mx = bounds
                width = float(mx[0] - mn[0])
                depth = float(mx[1] - mn[1])

            if m is None:
                continue
            center = (mn + mx) / 2.0
            offset = np.array(m.get("offset", [0.0, 0.0, 0.0]), dtype=float)
            center_offset = np.array([center[0] - offset[0], center[1] - offset[1]], dtype=float)
            model_info.append((mid, width, depth, center_offset, float(offset[2])))

        if not model_info:
            return False

        sizes = [(mid, w, d) for mid, w, d, _center_offset, _z in model_info]
        bed_bounds = self._bed_bounds()
        spacing_values = spacing_candidates(extra_spacing, step=0.5)
        align_candidates = [align_y]
        if len(model_info) > 1:
            align_candidates.append(not align_y)

        positions = None
        fit_found = False
        for align in align_candidates:
            for extra in spacing_values:
                spacing_val = spacing_with_base(base_spacing, extra)
                attempt = arrange_rectangles(sizes, spacing_val, align_y=align)
                if positions is None:
                    positions = attempt
                if positions_fit(attempt, sizes, bed_bounds):
                    positions = attempt
                    fit_found = True
                    break
            if fit_found:
                break

        if positions is None:
            return False

        info_map = {mid: (center_offset, z) for mid, _w, _d, center_offset, z in model_info}
        for mid, (x, y) in positions.items():
            m = self.models.get(mid)
            if m is None:
                continue
            center_offset, z = info_map.get(mid, (np.zeros(2, dtype=float), 0.0))
            new_x = float(x - center_offset[0])
            new_y = float(y - center_offset[1])
            self.set_model_transform(mid, offset_xyz=(new_x, new_y, z))

        return True

    def lay_on_face(self, model_id: int) -> bool:
        m = self.models.get(model_id)
        if m is None:
            return False
        v0 = m.get("base_vertices")
        faces = m.get("faces")
        if v0 is None or faces is None or len(faces) == 0:
            return False

        scale = self._normalize_scale(m.get("scale", 1.0))
        rot = np.array(m.get("rotation", [0.0, 0.0, 0.0]), dtype=float)
        pivot = m.get("pivot", np.zeros(3, dtype=float))
        R_current = self._rotation_matrix(float(rot[0]), float(rot[1]), float(rot[2]))

        verts = (v0 - pivot) * scale
        verts = verts @ R_current.T

        best = lowest_planar_face(verts, faces)
        if best is None:
            best_area = 0.0
            best_normal = None
            for tri in faces:
                a = verts[tri[0]]
                b = verts[tri[1]]
                c = verts[tri[2]]
                normal = np.cross(b - a, c - a)
                area = float(np.linalg.norm(normal) * 0.5)
                if area > best_area:
                    best_area = area
                    best_normal = normal
            if best_normal is None or best_area <= 1e-6:
                return False
            n = best_normal / max(1e-9, float(np.linalg.norm(best_normal)))
        else:
            n = np.array(best[0], dtype=float)

        target = np.array([0.0, 0.0, -1.0], dtype=float)
        R_align = self._rotation_from_to(n, target)
        R_new = R_align @ R_current
        rx, ry, rz = self._euler_from_matrix(R_new)
        self.set_model_transform(model_id, rotation_xyz=(rx, ry, rz))
        bounds = self.get_model_bounds(model_id)
        if bounds is not None:
            mn, _mx = bounds
            if abs(float(mn[2])) > 1e-6:
                off = np.array(m.get("offset", [0.0, 0.0, 0.0]), dtype=float)
                off[2] = float(off[2]) - float(mn[2])
                self.set_model_transform(model_id, offset_xyz=off)
        return True

    def auto_orient_model(self, model_id: int, mode: str = "default", overhang_angle: float = 45.0) -> bool:
        m = self.models.get(model_id)
        if m is None:
            return False
        v0 = m.get("base_vertices")
        faces = m.get("faces")
        if v0 is None or faces is None or len(faces) == 0:
            return False

        scale = self._normalize_scale(m.get("scale", 1.0))
        rot = np.array(m.get("rotation", [0.0, 0.0, 0.0]), dtype=float)
        pivot = m.get("pivot", np.zeros(3, dtype=float))
        verts = (v0 - pivot) * scale

        normals_base, areas = face_normals_and_areas(verts, faces)
        if normals_base.size == 0:
            return False

        R_current = self._rotation_matrix(float(rot[0]), float(rot[1]), float(rot[2]))
        normals_current = normals_base @ R_current.T
        candidates = select_candidate_normals(normals_current, areas)
        if not candidates:
            return False

        target = np.array([0.0, 0.0, -1.0], dtype=float)
        metrics = []
        rotations = []
        for n in candidates:
            R_align = rotation_from_to(n, target)
            R_candidate = R_align @ R_current
            support, height = orientation_metrics(
                verts,
                faces,
                normals_base,
                areas,
                R_candidate,
                overhang_angle,
            )
            rotations.append(R_candidate)
            metrics.append({"support": support, "height": height})

        best_idx = pick_best_orientation(metrics, mode)
        if best_idx is None:
            return False

        R_best = rotations[best_idx]
        rx, ry, rz = self._euler_from_matrix(R_best)
        self.set_model_transform(model_id, rotation_xyz=(rx, ry, rz))
        bounds = self.get_model_bounds(model_id)
        if bounds is not None:
            mn, _mx = bounds
            if abs(float(mn[2])) > 1e-6:
                off = np.array(m.get("offset", [0.0, 0.0, 0.0]), dtype=float)
                off[2] = float(off[2]) - float(mn[2])
                self.set_model_transform(model_id, offset_xyz=off)
        return True

    def _build_rotate_hud(self):
        self._rotate_hud = QtWidgets.QLabel(self)
        self._rotate_hud.setVisible(False)
        self._rotate_hud.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self._rotate_hud.setAlignment(QtCore.Qt.AlignCenter)
        self._update_rotate_hud_style()

    def _position_view_cube(self):
        if not hasattr(self, "_view_cube") or self._view_cube is None:
            return
        margin = 12
        size = self._view_cube.sizeHint()
        x = max(0, self.width() - size.width() - margin)
        y = margin
        self._view_cube.setGeometry(x, y, size.width(), size.height())

    def _sync_view_cube(self):
        if not hasattr(self, "_view_cube") or self._view_cube is None:
            return
        az = self._coerce_float(self.opts.get("azimuth"), float(self._default_view["azimuth"]))
        el = self._coerce_float(self.opts.get("elevation"), float(self._default_view["elevation"]))
        self._view_cube.set_camera(az, el)

    def _set_view_from_cube(self, face: str):
        invert_x = getattr(self._view_cube, "invert_x", False)
        invert_y = getattr(self._view_cube, "invert_y", False)
        invert_z = getattr(self._view_cube, "invert_z", False)

        def invert_view(azimuth: float, elevation: float):
            az = float(azimuth) + 180.0
            el = -float(elevation)
            if az > 180.0:
                az -= 360.0
            return az, el

        if face.startswith("iso:"):
            parts = face.split(":")
            if len(parts) == 4:
                x_name, y_name, z_name = parts[1], parts[2], parts[3]
                x_sign = self._view_cube._face_sign("x", x_name)
                y_sign = self._view_cube._face_sign("y", y_name)
                z_sign = self._view_cube._face_sign("z", z_name)
                if x_sign is None or y_sign is None or z_sign is None:
                    return
                az = math.degrees(math.atan2(y_sign, x_sign))
                el = math.degrees(math.atan2(z_sign, math.hypot(x_sign, y_sign)))
                az, el = invert_view(az, el)
                self.set_view(az, el)
            return

        if face.startswith("edge:"):
            parts = face.split(":")
            if len(parts) == 3:
                a_name, b_name = parts[1], parts[2]
                signs = {"x": 0.0, "y": 0.0, "z": 0.0}

                for axis in ("x", "y", "z"):
                    sign = self._view_cube._face_sign(axis, a_name)
                    if sign is not None:
                        signs[axis] = sign
                        break
                for axis in ("x", "y", "z"):
                    sign = self._view_cube._face_sign(axis, b_name)
                    if sign is not None and signs[axis] == 0.0:
                        signs[axis] = sign
                        break

                x_sign = signs["x"]
                y_sign = signs["y"]
                z_sign = signs["z"]
                if x_sign == 0.0 and y_sign == 0.0:
                    return
                az = math.degrees(math.atan2(y_sign, x_sign))
                el = math.degrees(math.atan2(z_sign, math.hypot(x_sign, y_sign)))
                az, el = invert_view(az, el)
                self.set_view(az, el)
            return

        views = {
            "front": (90.0, 0.0),
            "back": (-90.0, 0.0),
            "right": (0.0, 0.0),
            "left": (180.0, 0.0),
            "top": (0.0, 90.0),
            "bottom": (0.0, -90.0),
        }
        if invert_x:
            views["left"], views["right"] = views["right"], views["left"]
        if invert_y:
            views["front"], views["back"] = views["back"], views["front"]
        if invert_z:
            views["top"], views["bottom"] = views["bottom"], views["top"]
        view = views.get(face)
        if view is None:
            return
        az, el = invert_view(view[0], view[1])
        self.set_view(az, el)

    def resizeEvent(self, e: QtGui.QResizeEvent):
        super().resizeEvent(e)
        self._position_bottom_left_panels()
        self._position_view_cube()

    # -------------------- gizmo --------------------

    def _build_gizmo(self):
        for axis, key in (("x", "gizmo_x"), ("y", "gizmo_y"), ("z", "gizmo_z")):
            line = gl.GLLinePlotItem(
                color=theme_value(key, (1.0, 0.1, 0.1, 1.0)),
                width=2.5,
                antialias=True,
            )
            line.setVisible(False)
            self._gizmo_move_lines[axis] = line
            self.addItem(line)

            cone = gl.GLMeshItem(
                meshdata=gl.MeshData(),
                smooth=False,
                color=theme_value(key, (1.0, 0.1, 0.1, 1.0)),
                shader="shaded",
            )
            cone.setVisible(False)
            self._gizmo_move_cones[axis] = cone
            self.addItem(cone)

            ring = gl.GLLinePlotItem(
                color=theme_value(key, (1.0, 0.1, 0.1, 1.0)),
                width=2.0,
                antialias=True,
            )
            ring.setVisible(False)
            self._gizmo_rotate_rings[axis] = ring
            self.addItem(ring)

            ticks = gl.GLLinePlotItem(
                color=theme_value("gizmo_tick", (1.0, 1.0, 1.0, 1.0)),
                width=1.0,
                antialias=True,
            )
            ticks.setVisible(False)
            self._gizmo_rotate_ticks[axis] = ticks
            self.addItem(ticks)

            arrows = gl.GLMeshItem(
                meshdata=gl.MeshData(),
                smooth=False,
                color=theme_value(key, (1.0, 0.1, 0.1, 1.0)),
                shader="shaded",
            )
            arrows.setVisible(False)
            self._gizmo_rotate_arrows[axis] = arrows
            self.addItem(arrows)

    def _update_gizmo(self):
        if not self._interaction_enabled:
            self._set_gizmo_visible(False)
            return
        if self._gizmo_mode not in {"move", "rotate", "scale"}:
            self._set_gizmo_visible(False)
            return
        selected_ids = self._selected_model_ids or ([self._selected_model_id] if self._selected_model_id is not None else [])
        if not selected_ids:
            self._set_gizmo_visible(False)
            return

        bounds_list = []
        for mid in selected_ids:
            m = self.models.get(mid)
            if m is None or m.get("bounds") is None:
                continue
            bounds_list.append(m.get("bounds"))
        if not bounds_list:
            self._set_gizmo_visible(False)
            return
        mn = np.min([b[0] for b in bounds_list], axis=0)
        mx = np.max([b[1] for b in bounds_list], axis=0)
        center = (mn + mx) / 2.0
        model_extent = float(np.max(mx - mn))
        size = max(10.0, min(80.0, model_extent * 0.25))

        self._gizmo_origin = np.array(center, dtype=float)
        self._gizmo_size = size
        self._gizmo_model_extent = model_extent

        if self._gizmo_mode == "move":
            self._update_move_gizmo()
            self._set_gizmo_visible(True, mode="move")
        elif self._gizmo_mode == "rotate":
            self._update_rotate_gizmo()
            self._set_gizmo_visible(True, mode="rotate")
        else:
            self._set_gizmo_visible(False)

    def _set_gizmo_visible(self, visible: bool, mode: str | None = None):
        show_move = bool(visible and mode == "move")
        show_rotate = bool(visible and mode == "rotate")
        rotate_axis = self._gizmo_rotate_axis if show_rotate else None
        for item in self._gizmo_move_lines.values():
            item.setVisible(show_move)
        for item in self._gizmo_move_cones.values():
            item.setVisible(show_move)
        for axis, item in self._gizmo_rotate_rings.items():
            item.setVisible(show_rotate and (rotate_axis is None or axis == rotate_axis))
        for axis, item in self._gizmo_rotate_ticks.items():
            item.setVisible(show_rotate and (rotate_axis is None or axis == rotate_axis))
        for axis, item in self._gizmo_rotate_arrows.items():
            item.setVisible(show_rotate and (rotate_axis is None or axis == rotate_axis))

    def _gizmo_axes(self):
        return {
            "x": np.array([1.0, 0.0, 0.0], dtype=float),
            "y": np.array([0.0, 1.0, 0.0], dtype=float),
            "z": np.array([0.0, 0.0, 1.0], dtype=float),
        }

    def _gizmo_axis_direction(self, axis: str):
        return self._gizmo_axes().get(axis)

    def _pick_gizmo_axis(self, pos: QtCore.QPoint):
        if self._selected_model_id is None or self._gizmo_origin is None:
            return None
        if self._gizmo_mode != "move":
            return None
        origin = self._gizmo_origin

        click_x = float(pos.x())
        click_y = float(pos.y())
        threshold = 8.0

        best_axis = None
        best_dist = None

        for axis, direction in self._gizmo_axes().items():
            p0 = origin
            line_length = getattr(self, "_gizmo_move_line_length", self._gizmo_size)
            p1 = origin + direction * float(line_length)
            s0 = self._project_world_to_screen(p0)
            s1 = self._project_world_to_screen(p1)
            if s0 is None or s1 is None:
                continue
            dist = self._distance_point_to_segment(
                click_x, click_y, s0[0], s0[1], s1[0], s1[1]
            )
            if dist <= threshold and (best_dist is None or dist < best_dist):
                best_dist = dist
                best_axis = axis

        return best_axis

    def _pick_rotate_axis(self, pos: QtCore.QPoint):
        if self._selected_model_id is None or self._gizmo_origin is None:
            return None
        if self._gizmo_mode != "rotate":
            return None

        click_x = float(pos.x())
        click_y = float(pos.y())
        threshold = 10.0
        best_axis = None
        best_dist = None

        for axis, points in self._gizmo_ring_points.items():
            proj = [self._project_world_to_screen(p) for p in points]
            proj = [p for p in proj if p is not None]
            if len(proj) < 2:
                continue
            for i in range(len(proj) - 1):
                s0 = proj[i]
                s1 = proj[i + 1]
                dist = self._distance_point_to_segment(
                    click_x, click_y, s0[0], s0[1], s1[0], s1[1]
                )
                if dist <= threshold and (best_dist is None or dist < best_dist):
                    best_dist = dist
                    best_axis = axis

        return best_axis

    def _begin_gizmo_drag(self, axis: str, pos: QtCore.QPoint):
        if self._selected_model_id is None or self._gizmo_origin is None:
            return False
        axis_dir = self._gizmo_axis_direction(axis)
        if axis_dir is None:
            return False
        param = self._axis_param_from_mouse(pos, self._gizmo_origin, axis_dir)
        if param is None:
            return False

        self._gizmo_drag_axis = axis
        self._gizmo_drag_start_param = float(param)
        offsets = {}
        for mid in self._selected_model_ids or [self._selected_model_id]:
            m = self.models.get(mid)
            if m is not None:
                offsets[mid] = np.array(m.get("offset", [0.0, 0.0, 0.0]), dtype=float)
        self._gizmo_drag_start_offsets = offsets if offsets else None
        return True

    def _begin_rotate_drag(self, axis: str, pos: QtCore.QPoint):
        if self._selected_model_id is None or self._gizmo_origin is None:
            return False
        angle = self._rotate_angle_from_mouse(pos, axis)
        if angle is None:
            return False
        m = self.models.get(self._selected_model_id)
        if m is None:
            return False
        self._gizmo_rotate_axis = axis
        self._gizmo_rotate_start_angle = float(angle)
        self._gizmo_rotate_start_rotation = np.array(m.get("rotation", [0.0, 0.0, 0.0]), dtype=float)
        rotations = {}
        offsets = {}
        for mid in self._selected_model_ids or [self._selected_model_id]:
            m = self.models.get(mid)
            if m is None:
                continue
            rotations[mid] = np.array(m.get("rotation", [0.0, 0.0, 0.0]), dtype=float)
            offsets[mid] = np.array(m.get("offset", [0.0, 0.0, 0.0]), dtype=float)
        self._gizmo_rotate_start_rotations = rotations if rotations else None
        self._gizmo_rotate_start_offsets = offsets if offsets else None
        self._gizmo_rotate_pivot = np.array(self._gizmo_origin, dtype=float)
        self._update_gizmo()
        return True

    def _axis_param_from_mouse(self, pos: QtCore.QPoint, origin: np.ndarray, axis_dir: np.ndarray):
        o, d = self._mouse_ray(pos)
        if o is None or d is None:
            return None

        A = np.stack([axis_dir, -d], axis=1)
        b = o - origin
        try:
            sol, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        except np.linalg.LinAlgError:
            return None
        return float(sol[0])

    def _rotate_angle_from_mouse(self, pos: QtCore.QPoint, axis: str):
        o, d = self._mouse_ray(pos)
        if o is None or d is None:
            return None
        axis_dir = self._gizmo_axis_direction(axis)
        if axis_dir is None:
            return None
        origin = self._gizmo_origin
        if origin is None:
            return None

        denom = float(np.dot(axis_dir, d))
        if abs(denom) < 1e-6:
            return None
        t = float(np.dot(axis_dir, (origin - o)) / denom)
        if t < 0:
            return None
        hit = o + d * t
        v = hit - origin

        basis1, basis2 = self._ring_basis(axis)
        x = float(np.dot(v, basis1))
        y = float(np.dot(v, basis2))
        if abs(x) < 1e-6 and abs(y) < 1e-6:
            return None
        return math.atan2(y, x)

    def _ring_basis(self, axis: str):
        if axis == "x":
            return np.array([0.0, 1.0, 0.0], dtype=float), np.array([0.0, 0.0, 1.0], dtype=float)
        if axis == "y":
            return np.array([1.0, 0.0, 0.0], dtype=float), np.array([0.0, 0.0, 1.0], dtype=float)
        return np.array([1.0, 0.0, 0.0], dtype=float), np.array([0.0, 1.0, 0.0], dtype=float)

    def _ring_points_for_axis(self, axis: str, radius: float, segments: int = 64):
        origin = self._gizmo_origin
        if origin is None:
            return np.zeros((0, 3), dtype=float)
        basis1, basis2 = self._ring_basis(axis)
        theta = np.linspace(0.0, 2.0 * math.pi, segments, endpoint=True)
        points = []
        for t in theta:
            points.append(origin + basis1 * (radius * math.cos(t)) + basis2 * (radius * math.sin(t)))
        return np.array(points, dtype=float)

    def _tick_points_for_axis(self, axis: str, radius: float, tick_count: int = 60):
        origin = self._gizmo_origin
        if origin is None:
            return np.zeros((0, 3), dtype=float)
        basis1, basis2 = self._ring_basis(axis)
        points = []
        tick_len = radius * 0.08
        for i in range(tick_count):
            t = (2.0 * math.pi * i) / tick_count
            dir_vec = basis1 * math.cos(t) + basis2 * math.sin(t)
            p0 = origin + dir_vec * radius
            p1 = origin + dir_vec * (radius + tick_len)
            points.append(p0)
            points.append(p1)
        return np.array(points, dtype=float)

    def _distance_point_to_segment(self, px, py, x0, y0, x1, y1):
        vx = x1 - x0
        vy = y1 - y0
        wx = px - x0
        wy = py - y0
        denom = (vx * vx + vy * vy)
        if denom <= 1e-9:
            return float(np.hypot(wx, wy))
        t = max(0.0, min(1.0, (wx * vx + wy * vy) / denom))
        cx = x0 + t * vx
        cy = y0 + t * vy
        return float(np.hypot(px - cx, py - cy))

    def _update_move_gizmo(self):
        origin = self._gizmo_origin
        if origin is None:
            return
        line_length = max(12.0, self._gizmo_size * 1.0)
        self._gizmo_move_line_length = line_length
        cone_height = max(4.0, line_length * 0.25)
        cone_radius = cone_height * 0.35
        for axis, direction in self._gizmo_axes().items():
            color = theme_value(f"gizmo_{axis}", (1.0, 0.1, 0.1, 1.0))
            p0 = origin
            p1 = origin + direction * (line_length - cone_height * 0.2)
            pos = np.array([p0, p1], dtype=float)
            self._gizmo_move_lines[axis].setData(pos=pos, color=self._color_array(color, len(pos)))

            base = origin + direction * (line_length - cone_height)
            verts, faces = make_cone_mesh(cone_height, cone_radius, 18)
            R = self._axis_rotation_matrix(axis)
            verts = verts @ R.T
            verts = verts + base
            md = gl.MeshData(vertexes=verts, faces=faces)
            self._gizmo_move_cones[axis].setMeshData(meshdata=md)
            self._safe_gl_update(self._gizmo_move_cones[axis].setColor, color)

    def _update_rotate_gizmo(self):
        self._gizmo_ring_points = {}
        model_extent = float(self._gizmo_model_extent or (self._gizmo_size * 4.0))
        radius = max(16.0, model_extent * 0.6)
        tick_color = theme_value("gizmo_tick", (1.0, 1.0, 1.0, 1.0))
        arrow_len = max(6.0, radius * 0.12)
        arrow_radius = arrow_len * 0.35
        for axis in ("x", "y", "z"):
            color = theme_value(f"gizmo_{axis}", (1.0, 0.1, 0.1, 1.0))
            ring_points = self._ring_points_for_axis(axis, radius, 96)
            self._gizmo_rotate_rings[axis].setData(pos=ring_points,
                                                   mode="line_strip",
                                                   color=self._color_array(color, len(ring_points)))
            self._gizmo_ring_points[axis] = ring_points

            tick_points = self._tick_points_for_axis(axis, radius, 60)
            self._gizmo_rotate_ticks[axis].setData(pos=tick_points,
                                                   mode="lines",
                                                   color=self._color_array(tick_color, len(tick_points)))
            self._update_rotate_arrows(axis, radius, arrow_len, arrow_radius, color)

    def _update_rotate_arrows(self, axis: str, radius: float, height: float, cone_radius: float, color):
        arrows = self._gizmo_rotate_arrows.get(axis)
        if arrows is None:
            return
        origin = self._gizmo_origin
        if origin is None:
            return
        basis1, basis2 = self._ring_basis(axis)
        direction = basis2 / max(1e-6, float(np.linalg.norm(basis2)))
        ring_point = origin + basis1 * radius
        verts, faces = make_cone_mesh(height, cone_radius, 18)
        rot = self._rotation_from_z(direction)

        tip0 = ring_point
        base0 = tip0 - direction * height
        verts0 = (verts @ rot.T) + base0

        tip1 = ring_point - direction * (height * 1.2)
        base1 = tip1 - direction * height
        verts1 = (verts @ rot.T) + base1

        all_verts = np.vstack([verts0, verts1])
        faces_1 = faces + len(verts0)
        all_faces = np.vstack([faces, faces_1])
        arrows.setMeshData(meshdata=gl.MeshData(vertexes=all_verts, faces=all_faces))
        self._safe_gl_update(arrows.setColor, color)


    def _axis_rotation_matrix(self, axis: str):
        if axis == "x":
            return self._rotation_matrix(0.0, 90.0, 0.0)
        if axis == "y":
            return self._rotation_matrix(-90.0, 0.0, 0.0)
        return np.eye(3, dtype=float)

    def _rotation_from_z(self, direction: np.ndarray):
        z_axis = np.array([0.0, 0.0, 1.0], dtype=float)
        v = np.array(direction, dtype=float)
        norm = float(np.linalg.norm(v))
        if norm < 1e-6:
            return np.eye(3, dtype=float)
        v = v / norm
        dot = float(np.dot(z_axis, v))
        if abs(dot - 1.0) < 1e-6:
            return np.eye(3, dtype=float)
        if abs(dot + 1.0) < 1e-6:
            return self._rotation_matrix(180.0, 0.0, 0.0)
        axis = np.cross(z_axis, v)
        axis_norm = float(np.linalg.norm(axis))
        if axis_norm < 1e-6:
            return np.eye(3, dtype=float)
        axis = axis / axis_norm
        angle = math.acos(max(-1.0, min(1.0, dot)))
        kx, ky, kz = axis
        c = float(math.cos(angle))
        s = float(math.sin(angle))
        v1 = 1.0 - c
        return np.array(
            [
                [kx * kx * v1 + c, kx * ky * v1 - kz * s, kx * kz * v1 + ky * s],
                [ky * kx * v1 + kz * s, ky * ky * v1 + c, ky * kz * v1 - kx * s],
                [kz * kx * v1 - ky * s, kz * ky * v1 + kx * s, kz * kz * v1 + c],
            ],
            dtype=float,
        )

    def _rotation_from_to(self, source: np.ndarray, target: np.ndarray):
        a = np.array(source, dtype=float)
        b = np.array(target, dtype=float)
        a_norm = float(np.linalg.norm(a))
        b_norm = float(np.linalg.norm(b))
        if a_norm < 1e-9 or b_norm < 1e-9:
            return np.eye(3, dtype=float)
        a = a / a_norm
        b = b / b_norm
        c = float(np.dot(a, b))
        if c > 0.9999:
            return np.eye(3, dtype=float)
        if c < -0.9999:
            axis = np.array([1.0, 0.0, 0.0], dtype=float)
            if abs(a[0]) > 0.9:
                axis = np.array([0.0, 1.0, 0.0], dtype=float)
            axis = axis - a * float(np.dot(axis, a))
            axis_norm = float(np.linalg.norm(axis))
            if axis_norm < 1e-9:
                return np.eye(3, dtype=float)
            axis = axis / axis_norm
            return self._rotation_axis_angle(axis, math.pi)

        v = np.cross(a, b)
        s = float(np.linalg.norm(v))
        axis = v / max(1e-9, s)
        angle = math.atan2(s, c)
        return self._rotation_axis_angle(axis, angle)

    def _rotation_axis_angle(self, axis: np.ndarray, angle: float):
        kx, ky, kz = axis
        c = float(math.cos(angle))
        s = float(math.sin(angle))
        v1 = 1.0 - c
        return np.array(
            [
                [kx * kx * v1 + c, kx * ky * v1 - kz * s, kx * kz * v1 + ky * s],
                [ky * kx * v1 + kz * s, ky * ky * v1 + c, ky * kz * v1 - kx * s],
                [kz * kx * v1 - ky * s, kz * ky * v1 + kx * s, kz * kz * v1 + c],
            ],
            dtype=float,
        )

    def _euler_from_matrix(self, R: np.ndarray):
        r20 = float(R[2, 0])
        if abs(r20) < 0.999999:
            ry = math.asin(-r20)
            cy = math.cos(ry)
            rx = math.atan2(float(R[2, 1]) / cy, float(R[2, 2]) / cy)
            rz = math.atan2(float(R[1, 0]) / cy, float(R[0, 0]) / cy)
        else:
            ry = math.pi / 2 if r20 <= -0.999999 else -math.pi / 2
            rx = 0.0
            rz = math.atan2(-float(R[0, 1]), float(R[1, 1]))
        return math.degrees(rx), math.degrees(ry), math.degrees(rz)

    # -------------------- matrices / unproject --------------------

    def _view_projection_matrix(self):
        """
        pyqtgraph version indexes `region` and `viewport` like sequences:
          region[0], region[1], region[2], region[3]
        so BOTH must be 4-tuples (x0, y0, w, h).
        """
        w = max(1, int(self.width()))
        h = max(1, int(self.height()))

        region = (0.0, 0.0, float(w), float(h))  # tuple, not QRectF
        viewport = (0, 0, w, h)                  # tuple, not QRect

        view = self.viewMatrix()
        proj = self.projectionMatrix(region, viewport)

        viewproj = QtGui.QMatrix4x4(proj)
        viewproj = viewproj * view  # type: ignore[reportOperatorIssue]

        inv, ok = viewproj.inverted()
        if not ok:
            return None, None
        return viewproj, inv

    def _unproject(self, pos: QtCore.QPoint, ndc_z: float):
        _vp, inv = self._view_projection_matrix()
        if inv is None:
            return None

        w = max(1, int(self.width()))
        h = max(1, int(self.height()))

        x = (2.0 * float(pos.x()) / float(w)) - 1.0
        y = 1.0 - (2.0 * float(pos.y()) / float(h))
        z = float(ndc_z)

        v = QtGui.QVector4D(x, y, z, 1.0)
        world = inv.map(v)
        if abs(world.w()) < 1e-9:
            return None

        return np.array([world.x() / world.w(), world.y() / world.w(), world.z() / world.w()], dtype=float)

    def _mouse_ray(self, pos: QtCore.QPoint):
        p_near = self._unproject(pos, -1.0)
        p_far = self._unproject(pos, 1.0)
        if p_near is None or p_far is None:
            return None, None

        d = p_far - p_near
        n = float(np.linalg.norm(d))
        if n < 1e-9:
            return None, None
        d /= n
        return p_near, d

    def _mouse_to_plane(self, pos: QtCore.QPoint, plane_z: float):
        o, d = self._mouse_ray(pos)
        if o is None or d is None:
            return None
        if abs(d[2]) < 1e-8:
            return None

        t = (float(plane_z) - float(o[2])) / float(d[2])
        if t < 0:
            return None

        p = o + t * d
        p[2] = float(plane_z)
        return p

    def _mouse_to_plane_z0(self, pos: QtCore.QPoint):
        return self._mouse_to_plane(pos, 0.0)

    # -------------------- picking (AABB projection) --------------------

    def _project_world_to_screen(self, world_xyz: np.ndarray):
        viewproj, _inv = self._view_projection_matrix()
        if viewproj is None:
            return None

        v = QtGui.QVector4D(float(world_xyz[0]), float(world_xyz[1]), float(world_xyz[2]), 1.0)
        clip = viewproj.map(v)
        if abs(clip.w()) < 1e-9:
            return None

        ndc_x = clip.x() / clip.w()
        ndc_y = clip.y() / clip.w()
        ndc_z = clip.z() / clip.w()

        w = max(1, int(self.width()))
        h = max(1, int(self.height()))

        px = (ndc_x + 1.0) * 0.5 * w
        py = (1.0 - (ndc_y + 1.0) * 0.5) * h
        return float(px), float(py), float(ndc_z)

    def _pick_model_at(self, pos: QtCore.QPoint):
        if not self.models:
            return None

        click_x = float(pos.x())
        click_y = float(pos.y())

        best_id = None
        best_depth = None

        for mid, m in self.models.items():
            bounds = m.get("bounds")
            if bounds is None:
                continue
            mn, mx = bounds
            try:
                mn = np.array(mn, dtype=float).reshape(3)
                mx = np.array(mx, dtype=float).reshape(3)
            except Exception:
                continue
            if not np.all(np.isfinite(mn)) or not np.all(np.isfinite(mx)):
                continue
            if np.any(mx < mn):
                mn, mx = np.minimum(mn, mx), np.maximum(mn, mx)

            corners = np.array(
                [
                    [mn[0], mn[1], mn[2]],
                    [mn[0], mn[1], mx[2]],
                    [mn[0], mx[1], mn[2]],
                    [mn[0], mx[1], mx[2]],
                    [mx[0], mn[1], mn[2]],
                    [mx[0], mn[1], mx[2]],
                    [mx[0], mx[1], mn[2]],
                    [mx[0], mx[1], mx[2]],
                ],
                dtype=float,
            )

            proj = [self._project_world_to_screen(c) for c in corners]
            proj = [p for p in proj if p is not None]
            if len(proj) < 4:
                continue

            xs = [p[0] for p in proj]
            ys = [p[1] for p in proj]
            zs = [p[2] for p in proj]

            minx, maxx = min(xs), max(xs)
            miny, maxy = min(ys), max(ys)

            if (minx <= click_x <= maxx) and (miny <= click_y <= maxy):
                depth = float(min(zs))
                if best_depth is None or depth < best_depth:
                    best_depth = depth
                    best_id = mid

        return best_id
