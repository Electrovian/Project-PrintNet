from __future__ import annotations

import math
from typing import Any, Dict, TYPE_CHECKING

import numpy as np
import pyqtgraph.opengl as gl
from PyQt5 import QtCore

from ..theme import theme_value
from ..widgets.nozzle_item import make_cone_mesh


class GizmoMixin:
    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any: ...

    # -------------------- gizmo --------------------

    def _color_with_alpha(self, color, alpha: float):
        if not isinstance(color, (tuple, list)) or len(color) < 3:
            return color
        values = list(color)
        if len(values) == 3:
            values.append(1.0 if max(values) <= 1.0 else 255.0)
        max_rgb = max(values[:3]) if values[:3] else 1.0
        if max_rgb > 1.0:
            values[3] = max(0.0, min(255.0, float(values[3]) * alpha))
        else:
            values[3] = max(0.0, min(1.0, float(values[3]) * alpha))
        return tuple(values)

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
                width=2.4,
                antialias=True,
            )
            ring.setVisible(False)
            self._gizmo_rotate_rings[axis] = ring
            self.addItem(ring)

            ring_outer = gl.GLLinePlotItem(
                color=theme_value(key, (1.0, 0.1, 0.1, 1.0)),
                width=4.2,
                antialias=True,
            )
            ring_outer.setVisible(False)
            self._gizmo_rotate_rings_outer[axis] = ring_outer
            self.addItem(ring_outer)

            ticks_major = gl.GLLinePlotItem(
                color=theme_value("gizmo_tick", (1.0, 1.0, 1.0, 1.0)),
                width=1.6,
                antialias=True,
            )
            ticks_major.setVisible(False)
            self._gizmo_rotate_ticks_major[axis] = ticks_major
            self.addItem(ticks_major)

            ticks_minor = gl.GLLinePlotItem(
                color=theme_value("gizmo_tick", (1.0, 1.0, 1.0, 1.0)),
                width=1.0,
                antialias=True,
            )
            ticks_minor.setVisible(False)
            self._gizmo_rotate_ticks_minor[axis] = ticks_minor
            self.addItem(ticks_minor)

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
        for axis, item in self._gizmo_rotate_rings_outer.items():
            item.setVisible(show_rotate and (rotate_axis is None or axis == rotate_axis))
        for axis, item in self._gizmo_rotate_ticks_major.items():
            item.setVisible(show_rotate and (rotate_axis is None or axis == rotate_axis))
        for axis, item in self._gizmo_rotate_ticks_minor.items():
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

    def _tick_points_for_axis(self,
                              axis: str,
                              radius: float,
                              tick_count: int,
                              tick_len: float):
        origin = self._gizmo_origin
        if origin is None:
            return np.zeros((0, 3), dtype=float)
        basis1, basis2 = self._ring_basis(axis)
        points = []
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
        radius = max(22.0, model_extent * 0.7)
        tick_color = theme_value("gizmo_tick", (1.0, 1.0, 1.0, 1.0))
        tick_minor = self._color_with_alpha(tick_color, 0.45)
        arrow_len = max(7.0, radius * 0.1)
        arrow_radius = arrow_len * 0.32
        for axis in ("x", "y", "z"):
            color = theme_value(f"gizmo_{axis}", (1.0, 0.1, 0.1, 1.0))
            ring_points = self._ring_points_for_axis(axis, radius, 128)
            self._gizmo_rotate_rings[axis].setData(pos=ring_points,
                                                   mode="line_strip",
                                                   color=self._color_array(color, len(ring_points)))
            self._gizmo_ring_points[axis] = ring_points

            ring_outer = self._gizmo_rotate_rings_outer.get(axis)
            if ring_outer is not None:
                ring_outer.setData(
                    pos=ring_points,
                    mode="line_strip",
                    color=self._color_array(self._color_with_alpha(color, 0.25), len(ring_points)),
                )

            tick_points_major = self._tick_points_for_axis(axis, radius, 24, radius * 0.12)
            tick_points_minor = self._tick_points_for_axis(axis, radius, 72, radius * 0.06)
            self._gizmo_rotate_ticks_major[axis].setData(
                pos=tick_points_major,
                mode="lines",
                color=self._color_array(tick_color, len(tick_points_major)),
            )
            self._gizmo_rotate_ticks_minor[axis].setData(
                pos=tick_points_minor,
                mode="lines",
                color=self._color_array(tick_minor, len(tick_points_minor)),
            )
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

    
