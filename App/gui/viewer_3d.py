import os
import math
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5 import QtCore, QtGui, QtWidgets

from .widgets.view_cube_overlay import ViewCubeOverlay
from .theme import theme_value


class Viewer3D(gl.GLViewWidget):
    modelPicked = QtCore.pyqtSignal(int)
    modelMoved = QtCore.pyqtSignal(int, float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackgroundColor(theme_value("view_bg", (20, 22, 26)))

        # pyqtgraph expects a scalar here; guard it
        self._default_view = {"distance": 300.0, "elevation": 30.0, "azimuth": -45.0}
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

        self._snap_enabled = False
        self._snap_step = 1.0

        self._gizmo_mode = "move"
        self._gizmo_items = {}
        self._gizmo_origin = None
        self._gizmo_size = 20.0
        self._gizmo_drag_axis = None
        self._gizmo_drag_start_param = None
        self._gizmo_drag_start_offset = None

        g = gl.GLGridItem()
        g.setSize(200, 200, 0)
        g.setSpacing(10, 10, 1)
        g.translate(0, 0, 0)
        g.setColor(theme_value("grid_color", (80, 80, 80, 255)))
        self.addItem(g)

        self._build_gizmo()
        self._build_view_cube()

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

    def paintGL(self, *args, **kwargs):
        self._coerce_distance()
        self._sync_view_cube()
        return super().paintGL(*args, **kwargs)

    # -------------------- public helpers --------------------

    def set_selected_model(self, model_id: int | None):
        self._selected_model_id = model_id
        self._update_gizmo()

    def set_gizmo_mode(self, mode: str):
        self._gizmo_mode = mode
        self._update_gizmo()

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
            safe_name = os.path.basename(path)
        if not safe_name:
            safe_name = f"Model {model_id}"

        v = np.array(vertices, dtype=float)
        f = np.array(faces, dtype=int)

        self.models[model_id] = {
            "id": model_id,
            "path": path,
            "name": safe_name,
            "base_vertices": v,
            "faces": f,
            "item": None,
            "scale": 1.0,
            "offset": np.array([0.0, 0.0, 0.0], dtype=float),
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
        return float(m.get("scale", 1.0)), np.array(m.get("offset", [0.0, 0.0, 0.0]), dtype=float)

    def get_model_bounds(self, model_id: int):
        m = self.models.get(model_id)
        if not m:
            return None
        return m.get("bounds")

    # -------------------- transforms --------------------

    def set_model_transform(self, model_id: int, scale: float | None = None, offset_xy=None, offset_xyz=None):
        m = self.models.get(model_id)
        if not m:
            return

        if scale is not None:
            m["scale"] = float(scale)

        if offset_xyz is not None:
            x, y, z = offset_xyz
            m["offset"] = np.array([float(x), float(y), float(z)], dtype=float)
        elif offset_xy is not None:
            x, y = offset_xy
            z = float(m["offset"][2]) if m.get("offset") is not None else 0.0
            m["offset"] = np.array([float(x), float(y), z], dtype=float)

        self._create_or_update_mesh_item(model_id)
        if self._selected_model_id == model_id:
            self._update_gizmo()
        self.update()

    # -------------------- mouse interaction --------------------

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        if ev.button() == QtCore.Qt.LeftButton:
            axis = self._pick_gizmo_axis(ev.pos())
            if axis is not None:
                if self._begin_gizmo_drag(axis, ev.pos()):
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
        s = m["scale"]
        off = m["offset"]

        v = v0 * s + off

        mn = v.min(axis=0)
        mx = v.max(axis=0)
        m["bounds"] = (mn, mx)

        md = gl.MeshData(vertexes=v, faces=f)
        color = theme_value("mesh_color", (0.0, 0.9, 0.4, 0.9))

        if m["item"] is not None:
            self.removeItem(m["item"])

        item = gl.GLMeshItem(meshdata=md, smooth=False, color=color, shader="shaded")
        self.addItem(item)
        m["item"] = item

    # -------------------- view cube --------------------

    def _build_view_cube(self):
        self._view_cube = ViewCubeOverlay(self)
        self._view_cube.viewRequested.connect(self._set_view_from_cube)
        self._view_cube.homeRequested.connect(self.reset_view)
        self._position_view_cube()
        self._sync_view_cube()

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
        az = float(self.opts.get("azimuth", self._default_view["azimuth"]))
        el = float(self.opts.get("elevation", self._default_view["elevation"]))
        self._view_cube.set_camera(az, el)

    def _set_view_from_cube(self, face: str):
        invert_x = getattr(self._view_cube, "invert_x", False)
        invert_y = getattr(self._view_cube, "invert_y", False)
        invert_z = getattr(self._view_cube, "invert_z", False)

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
        self.set_view(view[0], view[1])

    def resizeEvent(self, e: QtGui.QResizeEvent):
        super().resizeEvent(e)
        self._position_view_cube()

    # -------------------- gizmo --------------------

    def _build_gizmo(self):
        self._gizmo_items = {
            "x": gl.GLLinePlotItem(color=theme_value("gizmo_x", (1.0, 0.1, 0.1, 1.0)), width=2.5, antialias=True),
            "y": gl.GLLinePlotItem(color=theme_value("gizmo_y", (0.1, 1.0, 0.1, 1.0)), width=2.5, antialias=True),
            "z": gl.GLLinePlotItem(color=theme_value("gizmo_z", (0.1, 0.4, 1.0, 1.0)), width=2.5, antialias=True),
        }
        for item in self._gizmo_items.values():
            item.setVisible(False)
            self.addItem(item)

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
        size = float(np.max(mx - mn))
        size = max(10.0, min(80.0, size * 0.25))

        self._gizmo_origin = np.array(center, dtype=float)
        self._gizmo_size = size

        for axis, direction in self._gizmo_axes().items():
            p0 = self._gizmo_origin
            p1 = self._gizmo_origin + direction * self._gizmo_size
            self._gizmo_items[axis].setData(pos=np.array([p0, p1], dtype=float))

        self._set_gizmo_visible(True)

    def _set_gizmo_visible(self, visible: bool):
        for item in self._gizmo_items.values():
            item.setVisible(bool(visible))

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

        click_x = float(pos.x())
        click_y = float(pos.y())
        threshold = 8.0

        best_axis = None
        best_dist = None

        for axis, direction in self._gizmo_axes().items():
            p0 = self._gizmo_origin
            p1 = self._gizmo_origin + direction * self._gizmo_size
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

    # -------------------- matrices / unproject --------------------

    def _view_projection_matrix(self):
        """
        Your pyqtgraph version indexes `region` and `viewport` like sequences:
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


