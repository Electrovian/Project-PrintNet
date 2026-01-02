import os
import math
from numbers import Real
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5 import QtCore, QtGui, QtWidgets
import trimesh

from .widgets.view_cube_overlay import ViewCubeOverlay
from .theme import theme_value, theme_qcolor
from config.defaults import DEFAULTS


class Viewer3D(gl.GLViewWidget):
    modelPicked = QtCore.pyqtSignal(int)
    modelMoved = QtCore.pyqtSignal(int, float, float)
    modelRotated = QtCore.pyqtSignal(int, float, float, float)

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
        self._dragging = False
        self._drag_start_world = None
        self._drag_start_offset = None
        self._labels_enabled = False
        self._selection_info = None

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
        self._gizmo_drag_start_offset = None
        self._gizmo_rotate_axis = None
        self._gizmo_rotate_start_angle = None
        self._gizmo_rotate_start_rotation = None
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

        self._build_gizmo()
        self._build_view_cube()
        self._build_rotate_hud()
        self._build_selection_info()

    # -------------------- hardening --------------------

    def _coerce_distance(self):
        d = self.opts.get("distance", 300.0)
        try:
            self.opts["distance"] = float(d) # pyright: ignore[reportArgumentType]
            return
        except Exception:
            pass
        try:
            self.opts["distance"] = float(d[0])  # type: ignore[index]
            return
        except Exception:
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

    def paintGL(self, *args, **kwargs):
        self._coerce_distance()
        self._sync_view_cube()
        return super().paintGL(*args, **kwargs)

    # -------------------- public helpers --------------------

    def set_selected_model(self, model_id: int | None):
        self._selected_model_id = model_id
        self._update_gizmo()
        self._update_selection_info()

    def set_gizmo_mode(self, mode: str):
        self._gizmo_mode = mode
        self._gizmo_drag_axis = None
        self._gizmo_rotate_axis = None
        if mode != "rotate":
            self._hide_rotate_hud()
        self._update_gizmo()

    def apply_theme(self):
        self.setBackgroundColor(theme_value("view_bg", (20, 22, 26)))
        if getattr(self, "_grid_item", None) is not None:
            self._grid_item.setColor(theme_value("grid_color", (80, 80, 80, 255)))

        for axis, key in (("x", "gizmo_x"), ("y", "gizmo_y"), ("z", "gizmo_z")):
            line = self._gizmo_move_lines.get(axis)
            if line is not None:
                try:
                    line.setData(pos=line.pos, color=theme_value(key), width=line.width)
                except Exception:
                    pass
            cone = self._gizmo_move_cones.get(axis)
            if cone is not None:
                try:
                    cone.setColor(theme_value(key))
                except Exception:
                    pass

            ring = self._gizmo_rotate_rings.get(axis)
            if ring is not None:
                try:
                    ring.setData(pos=ring.pos, color=theme_value(key), width=ring.width)
                except Exception:
                    pass
            ticks = self._gizmo_rotate_ticks.get(axis)
            if ticks is not None:
                try:
                    ticks.setData(pos=ticks.pos, color=theme_value("gizmo_tick"), width=ticks.width)
                except Exception:
                    pass
            arrows = self._gizmo_rotate_arrows.get(axis)
            if arrows is not None:
                try:
                    arrows.setColor(theme_value(key))
                except Exception:
                    pass

        mesh_color = theme_value("mesh_color", (0.0, 0.9, 0.4, 0.9))
        for m in self.models.values():
            item = m.get("item")
            if item is not None:
                try:
                    item.setColor(mesh_color)
                except Exception:
                    pass

        if hasattr(self, "_view_cube") and self._view_cube is not None:
            self._view_cube.apply_theme()
        self._update_rotate_hud_style()
        self._update_selection_info_style()
        self._update_gizmo()

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

    def _position_selection_info(self):
        if not hasattr(self, "_selection_info") or self._selection_info is None:
            return
        if not self._selection_info.isVisible():
            return
        margin = 12
        self._selection_info.adjustSize()
        x = margin
        y = max(margin, self.height() - self._selection_info.height() - margin)
        self._selection_info.move(x, y)

    def set_labels_visible(self, visible: bool):
        self._labels_enabled = bool(visible)
        self._update_selection_info()

    def _update_selection_info(self):
        if not hasattr(self, "_selection_info") or self._selection_info is None:
            return
        if not self._labels_enabled or self._selected_model_id is None:
            self._selection_info.setVisible(False)
            return
        m = self.models.get(self._selected_model_id)
        if not m:
            self._selection_info.setVisible(False)
            return
        name = (m.get("name") or "").strip() or f"Model {self._selected_model_id}"
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
        self._position_selection_info()

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

    # -------------------- model management --------------------

    def add_model_from_data(self, name: str, path: str, vertices, faces):
        model_id = self._next_model_id
        self._next_model_id += 1

        safe_name = (name or "").strip()
        if not safe_name:
            safe_name = os.path.basename(path) or f"Model {model_id}"

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
        }

        self._create_or_update_mesh_item(model_id)

        mn = v.min(axis=0)
        mx = v.max(axis=0)
        center = (mn + mx) / 2.0
        size = float(np.max(mx - mn))

        self.opts["center"] = pg.Vector(*center) # pyright: ignore[reportArgumentType]
        self.opts["distance"] = float(max(size * 2.0, 200.0)) # pyright: ignore[reportArgumentType]
        self._coerce_distance()
        self.update()
        return model_id

    def remove_model(self, model_id: int):
        m = self.models.get(model_id)
        if not m:
            return
        if m.get("item") is not None:
            self.removeItem(m["item"])
        del self.models[model_id]
        if self._selected_model_id == model_id:
            self._selected_model_id = None
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
        if ev.button() == QtCore.Qt.LeftButton:
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
                self._selected_model_id = picked
                self._update_gizmo()
                self.modelPicked.emit(picked)

            # 2) Allow drag of selected model even if pick missed (Bambu-like)
            if self._selected_model_id is not None:
                hit = self._mouse_to_plane_z0(ev.pos())
                if hit is not None:
                    self._dragging = True
                    self._drag_start_world = hit

                    m = self.models.get(self._selected_model_id)
                    if m is not None:
                        self._drag_start_offset = (float(m["offset"][0]), float(m["offset"][1]))
                    else:
                        self._drag_start_offset = (0.0, 0.0)

                    ev.accept()
                    return

        super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev: QtGui.QMouseEvent):
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
            rot = np.array(self._gizmo_rotate_start_rotation, dtype=float)
            axis_idx = {"x": 0, "y": 1, "z": 2}[self._gizmo_rotate_axis]
            rot[axis_idx] = rot[axis_idx] + delta_deg
            self.set_model_transform(self._selected_model_id, rotation_xyz=rot)
            self.modelRotated.emit(self._selected_model_id, float(rot[0]), float(rot[1]), float(rot[2]))
            axis_label = self._gizmo_rotate_axis.upper()
            self._show_rotate_hud(ev.pos(), axis_label, float(rot[axis_idx]))
            ev.accept()
            return

        if self._gizmo_drag_axis is not None and bool(ev.buttons() & QtCore.Qt.LeftButton):
            if self._selected_model_id is None:
                ev.accept()
                return

            m = self.models.get(self._selected_model_id)
            if m is None or self._gizmo_origin is None:
                ev.accept()
                return

            axis_dir = self._gizmo_axis_direction(self._gizmo_drag_axis)
            if axis_dir is None:
                ev.accept()
                return

            param = self._axis_param_from_mouse(ev.pos(), self._gizmo_origin, axis_dir)
            if param is None or self._gizmo_drag_start_param is None or self._gizmo_drag_start_offset is None:
                ev.accept()
                return

            delta = float(param - self._gizmo_drag_start_param)
            new_offset = self._gizmo_drag_start_offset + axis_dir * delta

            if self._snap_enabled:
                step = self._snap_step
                axis_idx = {"x": 0, "y": 1, "z": 2}[self._gizmo_drag_axis]
                new_offset[axis_idx] = round(float(new_offset[axis_idx]) / step) * step

            self.set_model_transform(self._selected_model_id, offset_xyz=new_offset)
            self.modelMoved.emit(self._selected_model_id, float(new_offset[0]), float(new_offset[1]))
            ev.accept()
            return

        if self._dragging and bool(ev.buttons() & QtCore.Qt.LeftButton):
            if self._selected_model_id is None:
                ev.accept()
                return

            hit = self._mouse_to_plane_z0(ev.pos())
            if hit is None or self._drag_start_world is None or self._drag_start_offset is None:
                ev.accept()
                return

            dx = float(hit[0] - self._drag_start_world[0])
            dy = float(hit[1] - self._drag_start_world[1])

            new_x = self._drag_start_offset[0] + dx
            new_y = self._drag_start_offset[1] + dy

            if self._snap_enabled:
                step = self._snap_step
                new_x = round(new_x / step) * step
                new_y = round(new_y / step) * step

            self.set_model_transform(self._selected_model_id, offset_xy=(new_x, new_y))
            self.modelMoved.emit(self._selected_model_id, float(new_x), float(new_y))
            ev.accept()
            return

        super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        if ev.button() == QtCore.Qt.LeftButton and self._dragging:
            self._dragging = False
            self._drag_start_world = None
            self._drag_start_offset = None
            ev.accept()
            return
        if ev.button() == QtCore.Qt.LeftButton and self._gizmo_rotate_axis is not None:
            self._gizmo_rotate_axis = None
            self._gizmo_rotate_start_angle = None
            self._gizmo_rotate_start_rotation = None
            self._hide_rotate_hud()
            self._update_gizmo()
            ev.accept()
            return
        if ev.button() == QtCore.Qt.LeftButton and self._gizmo_drag_axis is not None:
            self._gizmo_drag_axis = None
            self._gizmo_drag_start_param = None
            self._gizmo_drag_start_offset = None
            ev.accept()
            return
        super().mouseReleaseEvent(ev)

    # -------------------- mesh rebuild + bounds --------------------

    def _create_or_update_mesh_item(self, model_id: int):
        m = self.models[model_id]
        v0 = m["base_vertices"]
        f = m["faces"]
        s = self._normalize_scale(m.get("scale", 1.0))
        off = np.array(m.get("offset", [0.0, 0.0, 0.0]), dtype=float)
        rot = np.array(m.get("rotation", [0.0, 0.0, 0.0]), dtype=float)
        pivot = m.get("pivot", np.zeros(3, dtype=float))

        v = (v0 - pivot) * s
        if rot is not None:
            R = self._rotation_matrix(float(rot[0]), float(rot[1]), float(rot[2]))
            v = v @ R.T
        v = v + pivot + off

        mn = v.min(axis=0)
        if float(mn[2]) < 0.0:
            # Safety: keep the model above the build plate.
            lift = -float(mn[2])
            off = np.array([float(off[0]), float(off[1]), float(off[2]) + lift], dtype=float)
            m["offset"] = off
            v = (v0 - pivot) * s
            if rot is not None:
                R = self._rotation_matrix(float(rot[0]), float(rot[1]), float(rot[2]))
                v = v @ R.T
            v = v + pivot + off
            mn = v.min(axis=0)
        mx = v.max(axis=0)
        m["bounds"] = (mn, mx)

        md = gl.MeshData(vertexes=v, faces=f)
        color = theme_value("mesh_color", (0.0, 0.9, 0.4, 0.9))

        item = m.get("item")
        if item is None:
            item = gl.GLMeshItem(meshdata=md, smooth=False, color=color, shader="shaded")
            self.addItem(item)
            m["item"] = item
        else:
            item.setMeshData(meshdata=md)
            try:
                item.setColor(color)
            except Exception:
                pass

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

        spacing_val = max(0.0, float(spacing))
        if spacing_val <= 0.0:
            spacing_val = float(DEFAULTS["popups"]["arrange"]["auto_spacing"])

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
        positions = {}
        if align_y:
            total_depth = sum(d for _mid, _w, d in sizes) + spacing_val * (len(sizes) - 1)
            y_cursor = -total_depth / 2.0
            for mid, _w, d in sizes:
                y = y_cursor + d / 2.0
                positions[mid] = (0.0, y)
                y_cursor += d + spacing_val
        else:
            total_area = sum(w * d for _mid, w, d in sizes)
            target_width = math.sqrt(total_area) if total_area > 0.0 else 0.0
            x_cursor = 0.0
            y_cursor = 0.0
            row_depth = 0.0

            for mid, w, d in sizes:
                if x_cursor > 0.0 and target_width > 0.0 and (x_cursor + w) > target_width:
                    x_cursor = 0.0
                    y_cursor += row_depth + spacing_val
                    row_depth = 0.0
                x = x_cursor + w / 2.0
                y = y_cursor + d / 2.0
                positions[mid] = (x, y)
                x_cursor += w + spacing_val
                row_depth = max(row_depth, d)

            min_x = float("inf")
            max_x = float("-inf")
            min_y = float("inf")
            max_y = float("-inf")
            for mid, w, d in sizes:
                x, y = positions[mid]
                min_x = min(min_x, x - w / 2.0)
                max_x = max(max_x, x + w / 2.0)
                min_y = min(min_y, y - d / 2.0)
                max_y = max(max_y, y + d / 2.0)
            cx = (min_x + max_x) / 2.0
            cy = (min_y + max_y) / 2.0
            for mid in positions:
                x, y = positions[mid]
                positions[mid] = (x - cx, y - cy)

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
        self._position_selection_info()
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
        if self._selected_model_id is None or self._gizmo_mode not in {"move", "rotate", "scale"}:
            self._set_gizmo_visible(False)
            return

        m = self.models.get(self._selected_model_id)
        if m is None or m.get("bounds") is None:
            self._set_gizmo_visible(False)
            return

        mn, mx = m["bounds"]
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
        m = self.models.get(self._selected_model_id)
        if m is None:
            return False
        axis_dir = self._gizmo_axis_direction(axis)
        if axis_dir is None:
            return False
        param = self._axis_param_from_mouse(pos, self._gizmo_origin, axis_dir)
        if param is None:
            return False

        self._gizmo_drag_axis = axis
        self._gizmo_drag_start_param = float(param)
        self._gizmo_drag_start_offset = np.array(m["offset"], dtype=float)
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
            self._gizmo_move_lines[axis].setData(pos=np.array([p0, p1], dtype=float), color=color)

            base = origin + direction * (line_length - cone_height)
            verts, faces = self._make_cone_mesh(cone_height, cone_radius, 18)
            R = self._axis_rotation_matrix(axis)
            verts = verts @ R.T
            verts = verts + base
            md = gl.MeshData(vertexes=verts, faces=faces)
            self._gizmo_move_cones[axis].setMeshData(meshdata=md)
            try:
                self._gizmo_move_cones[axis].setColor(color)
            except Exception:
                pass

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
            self._gizmo_rotate_rings[axis].setData(pos=ring_points, mode="line_strip", color=color)
            self._gizmo_ring_points[axis] = ring_points

            tick_points = self._tick_points_for_axis(axis, radius, 60)
            self._gizmo_rotate_ticks[axis].setData(pos=tick_points, mode="lines", color=tick_color)
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
        verts, faces = self._make_cone_mesh(height, cone_radius, 18)
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
        try:
            arrows.setColor(color)
        except Exception:
            pass

    def _make_cone_mesh(self, height: float, radius: float, segments: int):
        verts = []
        faces = []
        verts.append([0.0, 0.0, height])
        for i in range(segments):
            ang = (2.0 * math.pi * i) / segments
            verts.append([radius * math.cos(ang), radius * math.sin(ang), 0.0])
        tip_index = 0
        for i in range(segments):
            i0 = 1 + i
            i1 = 1 + ((i + 1) % segments)
            faces.append([tip_index, i0, i1])
        return np.array(verts, dtype=float), np.array(faces, dtype=int)

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

    def _mouse_to_plane_z0(self, pos: QtCore.QPoint):
        o, d = self._mouse_ray(pos)
        if o is None or d is None:
            return None
        if abs(d[2]) < 1e-8:
            return None

        t = -o[2] / d[2]
        if t < 0:
            return None

        p = o + t * d
        p[2] = 0.0
        return p

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
