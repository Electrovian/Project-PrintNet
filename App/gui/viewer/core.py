import os
import math
from numbers import Real
from typing import Any, Dict, List, Optional, Sequence, Tuple
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5 import QtCore, QtGui, QtWidgets
import trimesh

from slicer_v2.legacy_geometry import arrange_rectangles, lowest_planar_face
from slicer_v2.legacy_mesh_opt import simplify_mesh, wireframe_target_faces

from ..auto_orient import (
    face_normals_and_areas,
    orientation_metrics,
    pick_best_orientation,
    rotation_from_to,
    select_candidate_normals,
)
from ..arrange_utils import positions_fit, spacing_candidates, spacing_with_base
from ..scene_state import SceneState
from ..theme import theme_value, theme_qcolor
from config.defaults import DEFAULTS
from .gizmos import GizmoMixin
from .panels import PanelMixin
from .preview import PreviewMixin
from .selection import SelectionMixin
from .wireframe import WireframeMixin


class Viewer3D(WireframeMixin, PreviewMixin, GizmoMixin, PanelMixin, SelectionMixin, gl.GLViewWidget):
    modelPicked = QtCore.pyqtSignal(int)
    modelMoved = QtCore.pyqtSignal(int, float, float)
    modelRotated = QtCore.pyqtSignal(int, float, float, float)
    selectionChanged = QtCore.pyqtSignal(list)
    simplifyRequested = QtCore.pyqtSignal(int)
    sceneChanged = QtCore.pyqtSignal()
    plateRemoveRequested = QtCore.pyqtSignal()
    plateAutoOrientRequested = QtCore.pyqtSignal()
    plateArrangeRequested = QtCore.pyqtSignal()
    plateSelectionChanged = QtCore.pyqtSignal(int)
    plateLockChanged = QtCore.pyqtSignal(bool)
    plateNameChanged = QtCore.pyqtSignal(str)

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

        self.scene_state = SceneState()
        self.models: dict[int, dict[str, Any]] = {}
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
        self._interaction_requested = True
        self._plate_overlay_visible = True
        self._plate_grid_items: dict[int, gl.GLGridItem] = {}
        self._plate_texture_items: dict[int, gl.GLImageItem] = {}
        self._plate_name_labels: dict[int, QtWidgets.QLabel] = {}
        self._plate_number_labels: dict[int, QtWidgets.QLabel] = {}
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
        self._gizmo_rotate_rings_outer = {}
        self._gizmo_rotate_ticks_major = {}
        self._gizmo_rotate_ticks_minor = {}
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

        self._grid_item = None

        printer_defaults = DEFAULTS.get("printer", {})
        self._bed_size = tuple(printer_defaults.get("bed_size", (200, 200)))
        self._bed_height = float(printer_defaults.get("max_height", 200))
        self._bed_texture_path = ""
        self._bed_model_path = ""
        self._bed_texture_item = None
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
        self._preview_extrude_items_static: List[gl.GLMeshItem] = []
        self._preview_extrude_items_dynamic: List[gl.GLMeshItem] = []
        self._preview_extrude_bins: List[Tuple[float, float, float]] = []
        self._preview_step_offsets: List[int] = []
        self._preview_total_steps = 0
        self._preview_base_width = 0.4
        self._preview_layer_height = float(
            DEFAULTS.get("settings_panel", {})
            .get("layer_height", {})
            .get("default", 0.2)
        )
        self._preview_feature_filter: Optional[set[str]] = None
        self._preview_step_index = None
        self._preview_step_layer = None
        self._preview_geometry_key = None
        self._preview_geometry_segments = None
        self._preview_geometry_widths = None
        self._preview_geometry_travel = None
        self._preview_geometry_meshes = None
        self._preview_cached_mode = None
        self._preview_color_cache = None
        self._preview_color_cache_static = None
        self._preview_color_cache_dynamic = None
        self._preview_empty_mesh = None
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
        self._preview_filament_color = None
        self._preview_visible = False
        self._models_visible = True
        self._model_preview_alpha = 1.0
        self._wireframe_default = False
        self._solid_mesh_edges = True
        self._overhang_visible = False
        self._overhang_angle = 45.0
        self._platform_visible = True
        self._nozzle_visible = False
        self._nozzle = None
        self._sync_scene_from_state()

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
        if hasattr(self, "_position_plate_action_strip"):
            self._position_plate_action_strip()
        if hasattr(self, "_position_fit_camera_button"):
            self._position_fit_camera_button()
        if hasattr(self, "_position_plate_labels"):
            self._position_plate_labels()
        return super().paintGL(*args, **kwargs)

    # -------------------- public helpers --------------------

    def set_selected_model(self, model_id: int | None):
        ids = [model_id] if model_id is not None else []
        self.set_selected_models(ids)

    def set_selected_models(self, model_ids: Sequence[int], emit_signal: bool = True):
        ids = [mid for mid in model_ids if mid in self.models]
        self._selected_model_ids = ids
        self._selected_model_id = ids[0] if ids else None
        self.scene_state.selected_entity_ids = list(ids)
        if ids:
            instance = self.scene_state.get_instance(ids[0])
            if instance is not None:
                self.scene_state.set_selected_plate(int(instance.plate_id))
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

    def set_prepare_tool(self, tool_id: str):
        resolved = str(tool_id or "move").strip() or "move"
        self.scene_state.tool_state.active_tool = resolved
        if resolved == "move":
            self.set_gizmo_mode("move")
        elif resolved == "rotate":
            self.set_gizmo_mode("rotate")
        else:
            self._gizmo_drag_axis = None
            self._gizmo_rotate_axis = None
            if resolved not in {"rotate"}:
                self._hide_rotate_hud()
            self._update_gizmo()

    def get_prepare_tool(self) -> str:
        return str(self.scene_state.tool_state.active_tool or "move")

    def set_interaction_enabled(self, enabled: bool):
        self._interaction_requested = bool(enabled)
        self._interaction_enabled = bool(enabled) and not self.is_plate_locked()
        if not self._interaction_enabled:
            self._dragging = False
            self._gizmo_drag_axis = None
            self._gizmo_rotate_axis = None
            self._hide_rotate_hud()
        self._update_gizmo()

    def is_plate_locked(self) -> bool:
        plate = self.scene_state.get_plate()
        return bool(plate.locked) if plate is not None else False

    def set_plate_locked(self, locked: bool):
        plate = self.scene_state.get_plate()
        if plate is not None:
            plate.locked = bool(locked)
        if hasattr(self, "_plate_lock_btn") and self._plate_lock_btn is not None:
            prev = self._plate_lock_btn.blockSignals(True)
            self._plate_lock_btn.setChecked(bool(locked))
            self._plate_lock_btn.blockSignals(prev)
        self.set_interaction_enabled(bool(self._interaction_requested))
        self.sceneChanged.emit()

    def get_current_plate_name(self) -> str:
        plate = self.scene_state.get_plate()
        text = str(plate.name if plate is not None else "").strip()
        return text or "01"

    def set_current_plate_name(self, value: str):
        text = str(value or "").strip()
        if not text:
            text = "01"
        text = text[:64]
        plate = self.scene_state.get_plate()
        if plate is None:
            return
        if text == plate.name:
            return
        plate.name = text
        self._update_plate_label_texts()
        self.plateNameChanged.emit(text)
        self.sceneChanged.emit()

    def fit_camera_to_scene_or_selection(self):
        target_ids = self.get_selected_model_ids()
        if not target_ids:
            target_ids = self.get_all_model_ids()
        if not target_ids:
            self.reset_view()
            return

        bounds_list = []
        for mid in target_ids:
            model = self.models.get(mid)
            bounds = model.get("bounds") if model is not None else None
            if bounds is None:
                bounds = self.get_model_bounds(mid)
            if bounds is not None:
                bounds_list.append(bounds)

        if not bounds_list:
            self.reset_view()
            return

        mins = np.array([b[0] for b in bounds_list], dtype=float)
        maxs = np.array([b[1] for b in bounds_list], dtype=float)
        mn = np.min(mins, axis=0)
        mx = np.max(maxs, axis=0)
        center = (mn + mx) / 2.0
        span_vec = np.maximum(mx - mn, np.array([1.0, 1.0, 1.0], dtype=float))
        span = float(np.linalg.norm(span_vec))
        bed_span = max(float(self._bed_size[0]), float(self._bed_size[1]), 1.0)
        distance = float(max(120.0, min(span * 2.4, bed_span * 4.0)))

        self.opts["center"] = pg.Vector(float(center[0]), float(center[1]), float(center[2])) # pyright: ignore[reportArgumentType]
        self.opts["distance"] = distance # pyright: ignore[reportArgumentType]
        self._coerce_distance()
        self._sync_view_cube()
        self.update()

    def apply_theme(self):
        self.setBackgroundColor(theme_value("view_bg", (20, 22, 26)))
        if hasattr(self, "_apply_plate_visual_theme"):
            self._apply_plate_visual_theme()

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
            ring_outer = self._gizmo_rotate_rings_outer.get(axis)
            if ring_outer is not None:
                self._safe_gl_update(self._update_gl_line, ring_outer, theme_value(key))
            ticks_major = self._gizmo_rotate_ticks_major.get(axis)
            if ticks_major is not None:
                self._safe_gl_update(self._update_gl_line, ticks_major, theme_value("gizmo_tick"))
            ticks_minor = self._gizmo_rotate_ticks_minor.get(axis)
            if ticks_minor is not None:
                self._safe_gl_update(self._update_gl_line, ticks_minor, theme_value("gizmo_tick"))
            arrows = self._gizmo_rotate_arrows.get(axis)
            if arrows is not None:
                self._safe_gl_update(arrows.setColor, theme_value(key))

        for m in self.models.values():
            self._apply_model_color(m)

        if hasattr(self, "_view_cube") and self._view_cube is not None:
            self._view_cube.apply_theme()
        if hasattr(self, "_apply_plate_overlay_theme"):
            self._apply_plate_overlay_theme()
        self._update_rotate_hud_style()
        self._update_selection_info_style()
        self._update_print_stats_style()
        self._update_preview_object_style()
        self._update_simplify_warning_style()
        self._update_marquee_style()
        self._update_gizmo()
        self._update_preview_lines()

    # -------------------- scene model --------------------

    def get_current_plate_id(self) -> int:
        return int(self.scene_state.ensure_default_plate())

    def get_plate_ids(self) -> list[int]:
        return self.scene_state.get_plate_ids()

    def _ordered_plates(self):
        plate_ids = self.get_plate_ids()
        return [self.scene_state.plates[plate_id] for plate_id in plate_ids if plate_id in self.scene_state.plates]

    def _plate_origin(self, plate_id: int) -> tuple[float, float, float]:
        plate_ids = self.get_plate_ids()
        if not plate_ids:
            return (0.0, 0.0, 0.0)
        try:
            index = plate_ids.index(int(plate_id))
        except ValueError:
            index = 0
        count = len(plate_ids)
        cols = 2 if count > 1 else 1
        rows = int(math.ceil(count / float(cols)))
        spacing_x = float(self._bed_size[0]) + max(40.0, float(self._bed_size[0]) * 0.2)
        spacing_y = float(self._bed_size[1]) + max(40.0, float(self._bed_size[1]) * 0.2)
        row = index // cols
        col = index % cols
        used_cols = min(cols, count)
        total_width = (used_cols - 1) * spacing_x
        total_height = (rows - 1) * spacing_y
        x = (col * spacing_x) - (total_width * 0.5)
        y = ((rows - 1 - row) * spacing_y) - (total_height * 0.5)
        return (float(x), float(y), 0.0)

    def _pick_plate_at(self, pos: QtCore.QPoint) -> int | None:
        if not hasattr(self, "_project_world_to_screen"):
            return None
        click_x = float(pos.x())
        click_y = float(pos.y())
        best_plate_id = None
        best_area = None
        for plate_id in self.get_plate_ids():
            min_x, max_x, min_y, max_y = self._bed_bounds(int(plate_id))
            corners = (
                np.array([min_x, min_y, 0.0], dtype=float),
                np.array([max_x, min_y, 0.0], dtype=float),
                np.array([max_x, max_y, 0.0], dtype=float),
                np.array([min_x, max_y, 0.0], dtype=float),
            )
            projected = [self._project_world_to_screen(corner) for corner in corners]
            projected = [point for point in projected if point is not None]
            if len(projected) != 4:
                continue
            xs = [float(point[0]) for point in projected]
            ys = [float(point[1]) for point in projected]
            if min(xs) <= click_x <= max(xs) and min(ys) <= click_y <= max(ys):
                area = abs((max(xs) - min(xs)) * (max(ys) - min(ys)))
                if best_area is None or area < best_area:
                    best_area = area
                    best_plate_id = int(plate_id)
        return best_plate_id

    def get_plate_model_ids(self, plate_id: int | None = None) -> list[int]:
        return self.scene_state.get_plate_instance_ids(plate_id)

    def get_all_model_ids(self) -> list[int]:
        return self.scene_state.get_all_instance_ids()

    def get_model_ids(self):
        return self.get_plate_model_ids()

    def select_plate(self, plate_id: int | None, emit_signal: bool = True) -> int | None:
        previous = self.scene_state.selected_plate_id
        selected = self.scene_state.set_selected_plate(plate_id)
        if selected is None:
            return None
        if previous != selected:
            self._update_plate_label_texts()
            self._sync_bed_grid()
            for model in self.models.values():
                self._update_bed_state(int(model["id"]))
                self._apply_model_color(model)
            if emit_signal:
                self.plateSelectionChanged.emit(int(selected))
            self.sceneChanged.emit()
            self.update()
        return int(selected)

    def add_plate(self, name: str | None = None) -> int:
        plate = self.scene_state.create_plate(name=name)
        self._sync_scene_from_state()
        self.select_plate(int(plate.id))
        return int(plate.id)

    def delete_current_plate(self) -> bool:
        plate_id = self.scene_state.selected_plate_id
        if plate_id is None:
            return False
        removed = self.scene_state.delete_plate(int(plate_id))
        if removed:
            current_ids = self.get_model_ids()
            if self._selected_model_id not in current_ids:
                self.set_selected_models(current_ids[:1], emit_signal=True)
            self._sync_scene_from_state()
        return bool(removed)

    def serialize_scene(self) -> dict[str, Any]:
        return self.scene_state.to_dict()

    def restore_scene(self, payload: dict[str, Any]) -> None:
        self.scene_state = SceneState.from_dict(payload)
        self._sync_scene_from_state()
        self.set_selected_models(self.scene_state.selected_entity_ids, emit_signal=False)
        self.select_plate(self.scene_state.selected_plate_id, emit_signal=False)

    def _sync_scene_from_state(self) -> None:
        desired_ids = set(self.scene_state.get_all_instance_ids())
        for model_id in list(self.models.keys()):
            if model_id not in desired_ids:
                self._remove_render_model(model_id)
        for instance_id in desired_ids:
            self._sync_instance_render(instance_id)
        self._next_model_id = max(desired_ids, default=0) + 1
        self._sync_bed_grid()
        self._update_plate_label_texts()
        self.sceneChanged.emit()
        self.update()

    def _remove_render_model(self, model_id: int) -> None:
        m = self.models.get(model_id)
        if not m:
            return
        for item in dict(m.get("annotation_items", {}) or {}).values():
            if item is None:
                continue
            try:
                self.removeItem(item)
            except Exception:
                pass
        if m.get("overhang_item") is not None:
            try:
                self.removeItem(m["overhang_item"])
            except Exception:
                pass
        if m.get("item") is not None:
            try:
                self.removeItem(m["item"])
            except Exception:
                pass
        del self.models[model_id]

    def _sync_instance_render(self, instance_id: int) -> bool:
        instance = self.scene_state.get_instance(instance_id)
        if instance is None:
            self._remove_render_model(instance_id)
            return False
        obj = self.scene_state.get_object(int(instance.object_id))
        if obj is None:
            self._remove_render_model(instance_id)
            return False
        vertices, faces, face_ranges = self.scene_state.object_mesh_arrays(int(obj.id))
        if vertices.size == 0 or faces.size == 0:
            self._remove_render_model(instance_id)
            return False

        base_mn = vertices.min(axis=0)
        base_mx = vertices.max(axis=0)
        pivot = (base_mn + base_mx) / 2.0
        model = self.models.get(instance_id)
        if model is None:
            model = {
                "id": int(instance_id),
                "item": None,
                "overhang_item": None,
                "annotation_items": {},
                "wireframe": self.get_wireframe_enabled(),
            }
            self.models[instance_id] = model

        model.update(
            {
                "id": int(instance_id),
                "path": str(obj.source_path or ""),
                "name": str(instance.name or obj.name or f"Object {int(obj.id)}"),
                "base_vertices": np.asarray(vertices, dtype=float),
                "faces": np.asarray(faces, dtype=int),
                "base_volume": None,
                "scale": np.asarray(instance.scale, dtype=float),
                "rotation": np.asarray(instance.rotation, dtype=float),
                "offset": np.asarray(instance.offset, dtype=float),
                "pivot": np.asarray(pivot, dtype=float),
                "bounds": model.get("bounds"),
                "out_of_bounds": bool(model.get("out_of_bounds", False)),
                "plate_id": int(instance.plate_id),
                "object_id": int(obj.id),
                "instance_id": int(instance.id),
                "part_face_ranges": list(face_ranges),
                "metadata": dict(instance.metadata or {}),
                "object_metadata": dict(obj.metadata or {}),
            }
        )
        self._create_or_update_mesh_item(int(instance_id))
        self._update_annotation_overlays(int(instance_id))
        return True

    def _sync_instances_for_object(self, object_id: int) -> None:
        for instance in list(self.scene_state.instances.values()):
            if int(instance.object_id) == int(object_id):
                self._sync_instance_render(int(instance.id))

    # -------------------- model management --------------------

    def add_scene_object(
        self,
        name: str,
        path: str,
        parts: list[dict[str, Any]],
        *,
        plate_id: int | None = None,
        object_metadata: dict[str, Any] | None = None,
        instance_metadata: dict[str, Any] | None = None,
    ) -> int:
        instance = self.scene_state.add_imported_object(
            name=name,
            source_path=path,
            parts=parts,
            plate_id=plate_id,
            object_metadata=object_metadata,
            instance_metadata=instance_metadata,
        )
        self._sync_scene_from_state()

        model_ids = self.get_all_model_ids()
        if model_ids:
            bounds_list = [self.get_model_bounds(mid) for mid in model_ids if self.get_model_bounds(mid) is not None]
            if bounds_list:
                mins = np.array([b[0] for b in bounds_list], dtype=float)
                maxs = np.array([b[1] for b in bounds_list], dtype=float)
                span = float(np.max(np.max(maxs, axis=0) - np.min(mins, axis=0)))
            else:
                span = max(float(self._bed_size[0]), float(self._bed_size[1]))
            self.opts["center"] = pg.Vector(0.0, 0.0, 0.0) # pyright: ignore[reportArgumentType]
            self.opts["distance"] = float(max(120.0, min(max(span * 2.0, 60.0), max(float(self._bed_size[0]), float(self._bed_size[1])) * 4.0))) # pyright: ignore[reportArgumentType]
            self._coerce_distance()
        return int(instance.id)

    def add_model_from_data(self, name: str, path: str, vertices, faces):
        safe_name = (name or "").strip() or os.path.basename(path) or "Model"
        return self.add_scene_object(
            safe_name,
            path,
            [
                {
                    "name": safe_name,
                    "vertices": np.asarray(vertices, dtype=float),
                    "faces": np.asarray(faces, dtype=int),
                    "source_path": path,
                }
            ],
        )

    def replace_model_mesh(self, model_id: int, vertices, faces) -> bool:
        m = self.models.get(model_id)
        if not m:
            return False
        v = np.asarray(vertices, dtype=float)
        f = np.asarray(faces, dtype=int)
        if v.size == 0 or f.size == 0:
            return False
        object_id = int(m.get("object_id", 0))
        obj = self.scene_state.get_object(object_id)
        if obj is None or not obj.part_ids:
            return False
        first_part_id = int(obj.part_ids[0])
        part = self.scene_state.parts.get(first_part_id)
        if part is None:
            return False
        part.vertices = [[float(x), float(y), float(z)] for x, y, z in v.tolist()]
        part.faces = [[int(a), int(b), int(c)] for a, b, c in f.tolist()]
        for extra_part_id in list(obj.part_ids[1:]):
            self.scene_state.parts.pop(int(extra_part_id), None)
        obj.part_ids = [first_part_id]
        self._sync_instances_for_object(object_id)
        self._update_selection_info()
        self.update()
        return True

    def remove_model(self, model_id: int):
        if model_id not in self.models:
            return
        self.scene_state.remove_instance(model_id, prune_orphans=True)
        self._remove_render_model(model_id)
        if model_id in self._selected_model_ids:
            self._selected_model_ids = [mid for mid in self._selected_model_ids if mid != model_id]
        if self._selected_model_id == model_id:
            self._selected_model_id = self._selected_model_ids[0] if self._selected_model_ids else None
        self._sync_scene_from_state()
        self._update_gizmo()
        self._update_selection_info()
        self.update()

    def clear_all_models(self):
        for model_id in list(self.models.keys()):
            self._remove_render_model(int(model_id))
        self.scene_state = SceneState()
        self._selected_model_id = None
        self._selected_model_ids = []
        self._sync_scene_from_state()

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
            instance = self.scene_state.get_instance(int(model_id))
            if instance is not None:
                instance.offset = (float(off[0]), float(off[1]), float(off[2]))
        m["bounds"] = (mn, mx)
        self._update_bed_state(model_id)
        return v, m.get("faces")

    def add_instance_for_model(self, model_id: int, offset_xyz=(10.0, 10.0, 0.0)) -> int | None:
        model = self.models.get(int(model_id))
        if model is None:
            return None
        instance = self.scene_state.get_instance(int(model_id))
        if instance is None:
            return None
        duplicate = self.scene_state.duplicate_instance(int(model_id), offset=offset_xyz)
        duplicate.name = str(model.get("name") or duplicate.name or f"Instance {duplicate.id}")
        self._sync_scene_from_state()
        return int(duplicate.id)

    def _mesh_for_model(self, model_id: int) -> trimesh.Trimesh | None:
        mesh_data = self.get_model_mesh_data(int(model_id))
        if not mesh_data:
            return None
        vertices, faces = mesh_data
        try:
            return trimesh.Trimesh(vertices=np.asarray(vertices, dtype=float), faces=np.asarray(faces, dtype=int), process=False)
        except Exception:
            return None

    def split_model_to_objects(self, model_id: int) -> list[int]:
        model = self.models.get(int(model_id))
        if model is None:
            return []
        mesh = self._mesh_for_model(int(model_id))
        if mesh is None:
            return []
        components = list(mesh.split(only_watertight=False))
        if len(components) <= 1:
            return []
        plate_id = int(model.get("plate_id", self.get_current_plate_id()))
        plate_origin = np.asarray(self._plate_origin(plate_id), dtype=float)
        source_path = str(model.get("path") or "")
        base_name = str(model.get("name") or f"Object {model_id}")
        self.scene_state.remove_instance(int(model_id), prune_orphans=True)
        self._remove_render_model(int(model_id))
        new_ids: list[int] = []
        for index, component in enumerate(components, start=1):
            local_vertices = np.asarray(component.vertices, dtype=float) - plate_origin
            new_id = self.add_scene_object(
                f"{base_name} {index}",
                source_path,
                [
                    {
                        "name": f"{base_name} {index}",
                        "vertices": local_vertices,
                        "faces": np.asarray(component.faces, dtype=int),
                        "source_path": source_path,
                    }
                ],
                plate_id=plate_id,
            )
            new_ids.append(int(new_id))
        self._sync_scene_from_state()
        return new_ids

    def split_model_to_parts(self, model_id: int) -> bool:
        model = self.models.get(int(model_id))
        if model is None:
            return False
        instance = self.scene_state.get_instance(int(model_id))
        if instance is None:
            return False
        mesh = self._mesh_for_model(int(model_id))
        if mesh is None:
            return False
        components = list(mesh.split(only_watertight=False))
        if len(components) <= 1:
            return False
        plate_id = int(model.get("plate_id", self.get_current_plate_id()))
        plate_origin = np.asarray(self._plate_origin(plate_id), dtype=float)
        source_path = str(model.get("path") or "")
        old_object_id = int(instance.object_id)
        recreated = self.scene_state.create_object(
            name=str(model.get("name") or f"Object {old_object_id}"),
            source_path=source_path,
            parts=[
                {
                    "name": f"Part {index}",
                    "vertices": np.asarray(component.vertices, dtype=float) - plate_origin,
                    "faces": np.asarray(component.faces, dtype=int),
                    "source_path": source_path,
                }
                for index, component in enumerate(components, start=1)
            ],
            metadata=dict(model.get("object_metadata") or {}),
        )
        instance.object_id = int(recreated.id)
        instance.scale = (1.0, 1.0, 1.0)
        instance.rotation = (0.0, 0.0, 0.0)
        instance.offset = (0.0, 0.0, 0.0)
        self.scene_state.prune_orphan_objects()
        self._sync_instances_for_object(int(recreated.id))
        self._sync_scene_from_state()
        return True

    def cut_model(
        self,
        model_id: int,
        *,
        axis: str = "x",
        position_ratio: float = 0.5,
        keep_mode: str = "both",
    ) -> list[int]:
        model = self.models.get(int(model_id))
        if model is None:
            return []
        mesh = self._mesh_for_model(int(model_id))
        if mesh is None:
            return []
        bounds = mesh.bounds
        axis_index = {"x": 0, "y": 1, "z": 2}.get(str(axis).strip().lower(), 0)
        ratio = max(0.0, min(1.0, float(position_ratio)))
        plane_pos = float(bounds[0][axis_index] + ((bounds[1][axis_index] - bounds[0][axis_index]) * ratio))
        plane_origin = np.array(mesh.centroid, dtype=float)
        plane_origin[axis_index] = plane_pos
        normal = np.zeros(3, dtype=float)
        normal[axis_index] = 1.0
        kept_meshes: list[trimesh.Trimesh] = []
        try:
            if keep_mode in {"upper", "both"}:
                upper = mesh.slice_plane(plane_origin=plane_origin, plane_normal=normal, cap=False)
                if upper is not None and not upper.is_empty:
                    kept_meshes.append(upper)
            if keep_mode in {"lower", "both"}:
                lower = mesh.slice_plane(plane_origin=plane_origin, plane_normal=-normal, cap=False)
                if lower is not None and not lower.is_empty:
                    kept_meshes.append(lower)
        except Exception:
            return []
        if not kept_meshes:
            return []
        plate_id = int(model.get("plate_id", self.get_current_plate_id()))
        plate_origin = np.asarray(self._plate_origin(plate_id), dtype=float)
        source_path = str(model.get("path") or "")
        base_name = str(model.get("name") or f"Object {model_id}")
        self.scene_state.remove_instance(int(model_id), prune_orphans=True)
        self._remove_render_model(int(model_id))
        new_ids: list[int] = []
        for index, kept in enumerate(kept_meshes, start=1):
            new_id = self.add_scene_object(
                f"{base_name} Cut {index}",
                source_path,
                [
                    {
                        "name": f"{base_name} Cut {index}",
                        "vertices": np.asarray(kept.vertices, dtype=float) - plate_origin,
                        "faces": np.asarray(kept.faces, dtype=int),
                        "source_path": source_path,
                    }
                ],
                plate_id=plate_id,
            )
            new_ids.append(int(new_id))
        self._sync_scene_from_state()
        return new_ids

    def boolean_models(self, model_ids: Sequence[int], operation: str = "union") -> int | None:
        selected_ids = [int(model_id) for model_id in model_ids if int(model_id) in self.models]
        if len(selected_ids) < 2:
            return None
        plate_ids = {int(self.models[mid].get("plate_id", self.get_current_plate_id())) for mid in selected_ids}
        if len(plate_ids) != 1:
            return None
        meshes = [self._mesh_for_model(mid) for mid in selected_ids]
        meshes = [mesh for mesh in meshes if mesh is not None]
        if len(meshes) < 2:
            return None
        result = None
        try:
            op = str(operation or "union").strip().lower()
            if op == "union":
                result = trimesh.boolean.union(meshes, engine="manifold")
            elif op == "difference":
                result = trimesh.boolean.difference(meshes, engine="manifold")
            else:
                result = trimesh.boolean.intersection(meshes, engine="manifold")
        except Exception:
            try:
                op = str(operation or "union").strip().lower()
                if op == "union":
                    result = trimesh.boolean.union(meshes)
                elif op == "difference":
                    result = trimesh.boolean.difference(meshes)
                else:
                    result = trimesh.boolean.intersection(meshes)
            except Exception:
                result = None
        if result is None:
            return None
        if isinstance(result, list):
            try:
                result = trimesh.util.concatenate(result)
            except Exception:
                return None
        if isinstance(result, trimesh.Scene):
            try:
                result = trimesh.util.concatenate(result.dump())
            except Exception:
                return None
        if not isinstance(result, trimesh.Trimesh) or result.is_empty:
            return None
        plate_id = plate_ids.pop()
        plate_origin = np.asarray(self._plate_origin(plate_id), dtype=float)
        source_path = str(self.models[selected_ids[0]].get("path") or "")
        for model_id in selected_ids:
            self.scene_state.remove_instance(int(model_id), prune_orphans=True)
            self._remove_render_model(int(model_id))
        new_id = self.add_scene_object(
            f"Boolean {str(operation or 'union').title()}",
            source_path,
            [
                {
                    "name": f"Boolean {str(operation or 'union').title()}",
                    "vertices": np.asarray(result.vertices, dtype=float) - plate_origin,
                    "faces": np.asarray(result.faces, dtype=int),
                    "source_path": source_path,
                }
            ],
            plate_id=plate_id,
        )
        self._sync_scene_from_state()
        return int(new_id)

    def set_overhang_visible(self, visible: bool, angle: float | None = None):
        self._overhang_visible = bool(visible)
        if angle is not None:
            try:
                self._overhang_angle = float(angle)
            except (TypeError, ValueError):
                self._overhang_angle = 45.0
        for model_id in list(self.models.keys()):
            self._update_overhang_item(model_id)
        self.update()

    def _update_overhang_item(self, model_id: int, vertices=None, faces=None):
        m = self.models.get(model_id)
        if not m:
            return
        item = m.get("overhang_item")
        if not self._overhang_visible:
            if item is not None:
                item.setVisible(False)
            return
        if vertices is None or faces is None:
            result = self._compute_transformed_vertices(m)
            if result is None:
                return
            vertices, _off, _mn, _mx = result
            faces = m.get("faces")
        if faces is None:
            return
        faces = np.asarray(faces, dtype=int)
        if faces.size == 0:
            return
        mask = self._overhang_face_mask(vertices, faces, self._overhang_angle)
        if mask is None or not mask.any():
            if item is not None:
                item.setVisible(False)
            return
        overhang_faces = faces[mask]
        mesh = gl.MeshData(vertexes=np.array(vertices, dtype=float), faces=overhang_faces)
        color = theme_value("mesh_warning", (1.0, 0.25, 0.2, 0.6))
        if item is None:
            item = gl.GLMeshItem(meshdata=mesh, smooth=False, color=color, shader="shaded")
            item.setGLOptions("translucent")
            self.addItem(item)
            m["overhang_item"] = item
        else:
            item.setMeshData(meshdata=mesh)
            item.setColor(color)
            item.setGLOptions("translucent")
        item.setVisible(True)

    def _overhang_face_mask(self, vertices, faces, angle: float):
        if vertices is None or faces is None:
            return None
        v = np.asarray(vertices, dtype=float)
        f = np.asarray(faces, dtype=int)
        if v.size == 0 or f.size == 0:
            return None
        tri = v[f]
        v0 = tri[:, 0, :]
        v1 = tri[:, 1, :]
        v2 = tri[:, 2, :]
        normals = np.cross(v1 - v0, v2 - v0)
        norm = np.linalg.norm(normals, axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            normals = normals / norm[:, None]
        cos_limit = math.cos(math.radians(float(angle)))
        mask = (normals[:, 2] < cos_limit) & (normals[:, 2] < 0.0)
        return mask

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
        instance = self.scene_state.get_instance(int(model_id))

        changed = False

        if scale is not None:
            new_scale = self._normalize_scale(scale)
            cur_vec = self._normalize_scale(m.get("scale", 1.0))
            if not np.allclose(cur_vec, new_scale):
                m["scale"] = new_scale
                if instance is not None:
                    instance.scale = (float(new_scale[0]), float(new_scale[1]), float(new_scale[2]))
                changed = True

        if rotation_xyz is not None:
            cur_rot = np.array(m.get("rotation", [0.0, 0.0, 0.0]), dtype=float)
            new_rot = self._normalize_vec3(rotation_xyz, default=cur_rot)
            if new_rot is None:
                new_rot = cur_rot
            if not np.allclose(cur_rot, new_rot):
                m["rotation"] = new_rot
                if instance is not None:
                    instance.rotation = (float(new_rot[0]), float(new_rot[1]), float(new_rot[2]))
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
                if instance is not None:
                    instance.offset = (float(new_offset[0]), float(new_offset[1]), float(new_offset[2]))
                changed = True

        if not changed:
            return

        self._create_or_update_mesh_item(model_id)
        self._update_annotation_overlays(model_id)
        if self._selected_model_id == model_id:
            self._update_gizmo()
            self._update_selection_info()
        self.update()

    def _annotation_faces(self, model_id: int, mode: str) -> list[int]:
        annotation = self.scene_state.tool_state.annotations.get(str(int(model_id)), {})
        mode_payload = dict(annotation.get(str(mode), {}) or {})
        faces = mode_payload.get("face_ids", [])
        if not isinstance(faces, list):
            return []
        return [int(face_id) for face_id in faces]

    def _set_annotation_faces(self, model_id: int, mode: str, faces: list[int]) -> None:
        annotation = dict(self.scene_state.tool_state.annotations.get(str(int(model_id)), {}) or {})
        if faces:
            annotation[str(mode)] = {"face_ids": sorted({int(face_id) for face_id in faces})}
            self.scene_state.tool_state.annotations[str(int(model_id))] = annotation
        else:
            annotation.pop(str(mode), None)
            if annotation:
                self.scene_state.tool_state.annotations[str(int(model_id))] = annotation
            else:
                self.scene_state.tool_state.annotations.pop(str(int(model_id)), None)
        self._update_annotation_overlays(int(model_id))
        self.sceneChanged.emit()

    def clear_annotation_mode(self, mode: str, model_id: int | None = None) -> None:
        target_ids = [int(model_id)] if model_id is not None else list(self.models.keys())
        for target_id in target_ids:
            self._set_annotation_faces(int(target_id), str(mode), [])

    def _update_annotation_overlays(self, model_id: int) -> None:
        model = self.models.get(int(model_id))
        if model is None:
            return
        mesh_data = self.get_model_mesh_data(int(model_id))
        if not mesh_data:
            return
        vertices, faces = mesh_data
        vertices = np.asarray(vertices, dtype=float)
        faces = np.asarray(faces, dtype=int)
        item_map = dict(model.get("annotation_items", {}) or {})
        mode_colors = {
            "support": (0.20, 0.62, 1.0, 0.45),
            "seam": (0.95, 0.25, 0.75, 0.45),
            "fuzzy": (1.0, 0.78, 0.20, 0.45),
        }
        for mode, color in mode_colors.items():
            face_ids = self._annotation_faces(int(model_id), mode)
            overlay = item_map.get(mode)
            if not face_ids:
                if overlay is not None:
                    overlay.setVisible(False)
                continue
            valid_ids = [face_id for face_id in face_ids if 0 <= int(face_id) < len(faces)]
            if not valid_ids:
                if overlay is not None:
                    overlay.setVisible(False)
                continue
            selected_faces = faces[np.asarray(valid_ids, dtype=int)]
            meshdata = gl.MeshData(vertexes=vertices.copy(), faces=selected_faces.copy())
            if overlay is None:
                overlay = gl.GLMeshItem(meshdata=meshdata, smooth=False, color=color, shader="shaded")
                overlay.setGLOptions("translucent")
                self.addItem(overlay)
                item_map[mode] = overlay
            else:
                overlay.setMeshData(meshdata=meshdata)
                overlay.setColor(color)
                overlay.setGLOptions("translucent")
            overlay.setVisible(True)
        model["annotation_items"] = item_map

    def _intersect_triangle(self, origin: np.ndarray, direction: np.ndarray, triangle: np.ndarray):
        epsilon = 1e-9
        v0, v1, v2 = triangle
        edge1 = v1 - v0
        edge2 = v2 - v0
        pvec = np.cross(direction, edge2)
        det = float(np.dot(edge1, pvec))
        if abs(det) < epsilon:
            return None
        inv_det = 1.0 / det
        tvec = origin - v0
        u = float(np.dot(tvec, pvec) * inv_det)
        if u < 0.0 or u > 1.0:
            return None
        qvec = np.cross(tvec, edge1)
        v = float(np.dot(direction, qvec) * inv_det)
        if v < 0.0 or (u + v) > 1.0:
            return None
        t = float(np.dot(edge2, qvec) * inv_det)
        if t <= epsilon:
            return None
        point = origin + (direction * t)
        return t, point

    def pick_surface(self, pos: QtCore.QPoint, model_ids: Sequence[int] | None = None):
        origin, direction = self._mouse_ray(pos)
        if origin is None or direction is None:
            return None
        candidates = [mid for mid in (model_ids or self.get_model_ids()) if mid in self.models]
        best = None
        for model_id in candidates:
            mesh_data = self.get_model_mesh_data(int(model_id))
            if not mesh_data:
                continue
            vertices, faces = mesh_data
            triangles = np.asarray(vertices, dtype=float)[np.asarray(faces, dtype=int)]
            for face_index, triangle in enumerate(triangles):
                hit = self._intersect_triangle(np.asarray(origin, dtype=float), np.asarray(direction, dtype=float), np.asarray(triangle, dtype=float))
                if hit is None:
                    continue
                distance, point = hit
                if best is None or float(distance) < float(best["distance"]):
                    best = {
                        "model_id": int(model_id),
                        "face_index": int(face_index),
                        "point": np.asarray(point, dtype=float),
                        "distance": float(distance),
                    }
        return best

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
            active_tool = self.get_prepare_tool()
            if active_tool in {"support_paint", "seam_paint", "fuzzy_paint", "measure"}:
                hit = self.pick_surface(ev.pos(), model_ids=self._selected_model_ids or self.get_model_ids())
                if hit is not None:
                    model_id = int(hit["model_id"])
                    self.select_plate(int(self.models.get(model_id, {}).get("plate_id", self.get_current_plate_id())))
                    self.set_selected_models([model_id], emit_signal=True)
                    if active_tool == "measure":
                        payload = dict(self.scene_state.tool_state.measure_payload or {})
                        points = list(payload.get("points", []) or [])
                        if len(points) >= 2:
                            points = []
                        points.append(
                            {
                                "model_id": model_id,
                                "face_index": int(hit["face_index"]),
                                "point": [float(v) for v in np.asarray(hit["point"], dtype=float).reshape(-1)],
                            }
                        )
                        payload["points"] = points
                        if len(points) == 2:
                            a = np.asarray(points[0]["point"], dtype=float)
                            b = np.asarray(points[1]["point"], dtype=float)
                            delta = b - a
                            payload["distance_mm"] = float(np.linalg.norm(delta))
                            payload["delta_xyz_mm"] = [float(v) for v in delta.reshape(-1)]
                        self.scene_state.tool_state.measure_payload = payload
                        self.sceneChanged.emit()
                    else:
                        mode = {
                            "support_paint": "support",
                            "seam_paint": "seam",
                            "fuzzy_paint": "fuzzy",
                        }[active_tool]
                        faces = self._annotation_faces(model_id, mode)
                        face_index = int(hit["face_index"])
                        if ctrl_down:
                            faces = [face_id for face_id in faces if int(face_id) != face_index]
                        elif face_index in faces:
                            faces = [face_id for face_id in faces if int(face_id) != face_index]
                        else:
                            faces.append(face_index)
                        self._set_annotation_faces(model_id, mode, faces)
                    ev.accept()
                    return
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
                instance = self.scene_state.get_instance(int(picked))
                if instance is not None:
                    self.select_plate(int(instance.plate_id))
            else:
                plate_id = self._pick_plate_at(ev.pos())
                if plate_id is not None:
                    self.select_plate(int(plate_id))
                    if not ctrl_down:
                        self.set_selected_models([], emit_signal=True)
                    ev.accept()
                    return

            # 2) Allow drag of selected model even if pick missed (slicer-like behavior)
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

    def _sanitize_faces_for_render(self, vertices: np.ndarray, faces: np.ndarray):
        v = np.asarray(vertices, dtype=float)
        f = np.asarray(faces, dtype=int)
        if v.ndim != 2 or v.shape[1] != 3:
            return None
        if f.ndim != 2 or f.shape[1] != 3:
            return None
        if v.size == 0 or f.size == 0:
            return None

        max_index = len(v)
        valid = (f >= 0).all(axis=1) & (f < max_index).all(axis=1)
        f = f[valid]
        if f.size == 0:
            return None

        non_degenerate = (f[:, 0] != f[:, 1]) & (f[:, 0] != f[:, 2]) & (f[:, 1] != f[:, 2])
        f = f[non_degenerate]
        if f.size == 0:
            return None

        p0 = v[f[:, 0]]
        p1 = v[f[:, 1]]
        p2 = v[f[:, 2]]
        area = np.linalg.norm(np.cross(p1 - p0, p2 - p0), axis=1)
        finite = np.isfinite(area)
        f = f[finite & (area > 1e-14)]
        if f.size == 0:
            return None
        return f

    def _placeholder_meshdata(self):
        verts = np.array(
            [
                [0.0, 0.0, 0.0],
                [0.001, 0.0, 0.0],
                [0.0, 0.001, 0.0],
            ],
            dtype=float,
        )
        faces = np.array([[0, 1, 2]], dtype=int)
        return gl.MeshData(vertexes=verts, faces=faces)

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

        render_faces = self._sanitize_faces_for_render(v, m["faces"])
        if render_faces is None:
            md = self._placeholder_meshdata()
        else:
            md = gl.MeshData(vertexes=v, faces=render_faces)
        m["meshdata_full"] = md
        if bool(m.get("wireframe")):
            m["meshdata_wireframe"] = self._build_wireframe_meshdata(v, render_faces if render_faces is not None else m["faces"])
        else:
            m["meshdata_wireframe"] = None
        base_color = theme_value("mesh_color", (0.0, 0.9, 0.4, 0.9))
        warn_color = theme_value("mesh_warning", (1.0, 0.25, 0.2, 0.95))
        color = warn_color if m.get("out_of_bounds") else base_color

        use_wireframe_mesh = bool(m.get("wireframe")) and m.get("meshdata_wireframe") is not None
        meshdata = m["meshdata_wireframe"] if use_wireframe_mesh else md
        item = m.get("item")
        if item is None:
            item = gl.GLMeshItem(meshdata=meshdata, smooth=True, color=color, shader="shaded")
            gl_mode = "translucent" if getattr(self, "_model_preview_alpha", 1.0) < 0.999 else "opaque"
            item.setGLOptions(gl_mode)
            self.addItem(item)
            item.setVisible(self._models_visible)
            m["item"] = item
        else:
            item.setMeshData(meshdata=meshdata)
            self._apply_model_color(m)
            item.setVisible(self._models_visible)
        self._apply_wireframe_to_item(item, bool(m.get("wireframe")), draw_faces=True)
        if not self._models_visible:
            if bool(m.get("wireframe")):
                item.setVisible(True)
                self._apply_wireframe_to_item(item, True, draw_faces=False)
            else:
                item.setVisible(False)
        if self._overhang_visible:
            self._update_overhang_item(model_id, vertices=v, faces=m.get("faces"))

    def _build_wireframe_meshdata(self, vertices: np.ndarray, faces: np.ndarray):
        safe_faces = self._sanitize_faces_for_render(vertices, faces)
        if safe_faces is None:
            return self._placeholder_meshdata()
        faces = safe_faces
        face_count = int(faces.shape[0]) if faces is not None else 0
        target_faces = wireframe_target_faces(face_count)
        if target_faces and target_faces < face_count:
            simplified = simplify_mesh(vertices, faces, target_faces)
            if simplified is not None:
                wire_v, wire_f = simplified
                if wire_v is not None and wire_f is not None and wire_f.shape[0] > 0:
                    safe_wire_faces = self._sanitize_faces_for_render(wire_v, wire_f)
                    if safe_wire_faces is not None:
                        return gl.MeshData(vertexes=wire_v, faces=safe_wire_faces)
        return gl.MeshData(vertexes=vertices, faces=faces)

    def _ensure_model_wireframe_meshdata(self, model_id: int):
        model = self.models.get(model_id)
        if model is None:
            return
        if model.get("meshdata_wireframe") is not None:
            return
        result = self._compute_transformed_vertices(model)
        if result is None:
            return
        vertices, offset, mn, mx = result
        model["offset"] = offset
        model["bounds"] = (mn, mx)
        self._update_bed_state(model_id)
        faces = model.get("faces")
        if faces is None:
            return
        render_faces = self._sanitize_faces_for_render(vertices, faces)
        if render_faces is None:
            return
        model["meshdata_wireframe"] = self._build_wireframe_meshdata(vertices, render_faces)

    def _compute_transformed_vertices(self, model: dict):
        v0 = model.get("base_vertices")
        if v0 is None or len(v0) == 0:
            return None
        s = self._normalize_scale(model.get("scale", 1.0))
        off = np.array(model.get("offset", [0.0, 0.0, 0.0]), dtype=float)
        rot = np.array(model.get("rotation", [0.0, 0.0, 0.0]), dtype=float)
        pivot = model.get("pivot", np.zeros(3, dtype=float))
        plate_origin = np.array(self._plate_origin(int(model.get("plate_id", self.get_current_plate_id()))), dtype=float)
        assembly_offset = np.zeros(3, dtype=float)
        if self.scene_state.tool_state.assembly_mode:
            value = self.scene_state.tool_state.assembly_offsets.get(str(int(model.get("instance_id", model.get("id", 0)))))
            if isinstance(value, list) and len(value) == 3:
                assembly_offset = np.asarray(value, dtype=float)

        v = (v0 - pivot) * s
        R = self._rotation_matrix(float(rot[0]), float(rot[1]), float(rot[2]))
        v = v @ R.T
        v = v + pivot + off + plate_origin + assembly_offset

        mn = v.min(axis=0)
        if float(mn[2]) < 0.0:
            lift = -float(mn[2])
            off = np.array([float(off[0]), float(off[1]), float(off[2]) + lift], dtype=float)
            v = (v0 - pivot) * s
            v = v @ R.T
            v = v + pivot + off + plate_origin + assembly_offset
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

    def _view_cube_target_size(self) -> int:
        min_dim = max(1, int(min(self.width(), self.height())))
        target = int(round(min_dim * 0.12))
        return max(84, min(170, target))

    def _position_view_cube(self):
        if not hasattr(self, "_view_cube") or self._view_cube is None:
            return
        if hasattr(self._view_cube, "set_cube_size"):
            self._view_cube.set_cube_size(self._view_cube_target_size())
        if hasattr(self, "_sync_overlay_button_metrics"):
            self._sync_overlay_button_metrics()
        size = self._view_cube.sizeHint()
        margin = max(12, int(round(size.width() * 0.18)))
        x = margin
        y = max(0, self.height() - size.height() - margin)
        self._view_cube.setGeometry(x, y, size.width(), size.height())
        self._view_cube.raise_()
        if hasattr(self, "_position_fit_camera_button"):
            self._position_fit_camera_button()
        if hasattr(self, "_position_plate_action_strip"):
            self._position_plate_action_strip()

    def _sync_view_cube(self):
        if not hasattr(self, "_view_cube") or self._view_cube is None:
            return
        az = self._coerce_float(self.opts.get("azimuth"), float(self._default_view["azimuth"]))
        el = self._coerce_float(self.opts.get("elevation"), float(self._default_view["elevation"]))
        self._view_cube.set_camera(az, el)
        if hasattr(self, "_position_fit_camera_button"):
            self._position_fit_camera_button()
        if hasattr(self, "_position_plate_action_strip"):
            self._position_plate_action_strip()

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
        self._position_view_cube()
        self._position_bottom_left_panels()

    
