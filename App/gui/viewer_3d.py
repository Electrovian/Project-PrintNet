import os
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5 import QtCore, QtGui


class Viewer3D(gl.GLViewWidget):
    modelPicked = QtCore.pyqtSignal(int)
    modelMoved = QtCore.pyqtSignal(int, float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBackgroundColor((20, 22, 26))

        # pyqtgraph expects a scalar here; guard it
        self.opts["distance"] = 300.0 # pyright: ignore[reportArgumentType]
        self._coerce_distance()

        self.models = {}
        self._next_model_id = 1

        self._selected_model_id = None
        self._dragging = False
        self._drag_start_world = None
        self._drag_start_offset = None

        self._snap_enabled = False
        self._snap_step = 1.0

        g = gl.GLGridItem()
        g.setSize(200, 200, 0)
        g.setSpacing(10, 10, 1)
        g.translate(0, 0, 0)
        g.setColor((80, 80, 80, 255))
        self.addItem(g)

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
        return super().paintGL(*args, **kwargs)

    # -------------------- public helpers --------------------

    def set_selected_model(self, model_id: int | None):
        self._selected_model_id = model_id

    def set_snap(self, enabled: bool, step_mm: float):
        self._snap_enabled = bool(enabled)
        self._snap_step = max(0.001, float(step_mm))

    # -------------------- model management --------------------

    def add_model_from_data(self, name: str, path: str, vertices, faces):
        model_id = self._next_model_id
        self._next_model_id += 1

        v = np.array(vertices, dtype=float)
        f = np.array(faces, dtype=int)

        self.models[model_id] = {
            "id": model_id,
            "path": path,
            "name": name or os.path.basename(path),
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

    # -------------------- transforms --------------------

    def set_model_transform(self, model_id: int, scale: float | None = None, offset_xy=None):
        m = self.models.get(model_id)
        if not m:
            return

        if scale is not None:
            m["scale"] = float(scale)

        if offset_xy is not None:
            x, y = offset_xy
            m["offset"] = np.array([float(x), float(y), 0.0], dtype=float)

        self._create_or_update_mesh_item(model_id)
        self.update()

    # -------------------- mouse interaction --------------------

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        if ev.button() == QtCore.Qt.LeftButton:
            # 1) Try to pick a model under cursor
            picked = self._pick_model_at(ev.pos())
            if picked is not None:
                self._selected_model_id = picked
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
        color = (0.0, 0.9, 0.4, 0.9)

        if m["item"] is not None:
            self.removeItem(m["item"])

        item = gl.GLMeshItem(meshdata=md, smooth=False, color=color, shader="shaded")
        self.addItem(item)
        m["item"] = item

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
