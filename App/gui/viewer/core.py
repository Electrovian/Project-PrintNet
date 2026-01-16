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

from ..auto_orient import (
    face_normals_and_areas,
    orientation_metrics,
    pick_best_orientation,
    rotation_from_to,
    select_candidate_normals,
)
from ..arrange_utils import positions_fit, spacing_candidates, spacing_with_base
from ..theme import theme_value, theme_qcolor
from config.defaults import DEFAULTS
from .gizmos import GizmoMixin
from .panels import PanelMixin
from .preview import PreviewMixin
from .selection import SelectionMixin


class Viewer3D(PreviewMixin, GizmoMixin, PanelMixin, SelectionMixin, gl.GLViewWidget):
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
        self._gizmo_drag_start_offsets: Dict[int, np.ndarray] | None = None
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
        enable_edges = bool(enabled)
        m["wireframe"] = enable_edges
        item.opts["drawEdges"] = enable_edges
        item.opts["drawFaces"] = True
        if enable_edges:
            item.meshDataChanged()
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
            item.meshDataChanged()

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

    
