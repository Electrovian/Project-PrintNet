from __future__ import annotations

from typing import Any, List, Tuple, TYPE_CHECKING, cast

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from ..selection_utils import rect_from_points, rect_intersects, rect_size
from ..theme import theme_qcolor


class SelectionMixin:
    # -------------------- marquee selection --------------------

    def _ensure_marquee_band(self):
        if self._marquee_band is None:
            band = QtWidgets.QRubberBand(
                QtWidgets.QRubberBand.Rectangle,
                cast(QtWidgets.QWidget, self),
            )
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

    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any:
            ...
