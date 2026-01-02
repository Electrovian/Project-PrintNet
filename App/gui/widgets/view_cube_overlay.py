import math
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from ..theme import theme_qcolor


class ViewCubeOverlay(QtWidgets.QWidget):
    viewRequested = QtCore.pyqtSignal(str)
    homeRequested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._azimuth = -45.0
        self._elevation = 30.0
        self._cube_size = 90
        self._padding = 6
        self._home_size = 18
        self._face_regions = []
        self._edge_regions = []
        self._corner_regions = []
        self._home_rect = QtCore.QRect()
        self._corner_radius = 6
        self.invert_x = False
        self.invert_y = True
        self.invert_z = False
        self._hover_name = None
        self._active_name = None
        self._apply_theme()

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)

    def _apply_theme(self):
        self._panel_color = theme_qcolor("cube_panel")
        self._face_color = theme_qcolor("cube_face")
        self._border_color = theme_qcolor("cube_border")
        self._text_color = theme_qcolor("cube_text")
        self._accent_color = theme_qcolor("cube_accent")
        self._hover_color = theme_qcolor("cube_hover")
        self._active_color = theme_qcolor("cube_active")

    def apply_theme(self):
        self._apply_theme()
        self.update()

    def sizeHint(self):
        return QtCore.QSize(self._cube_size, self._cube_size + self._home_size + self._padding * 2)

    def set_camera(self, azimuth: float, elevation: float):
        if abs(self._azimuth - azimuth) < 1e-3 and abs(self._elevation - elevation) < 1e-3:
            return
        self._azimuth = float(azimuth)
        self._elevation = float(elevation)
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent):
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.Antialiasing, True)
        p.setRenderHint(QtGui.QPainter.TextAntialiasing, True)

        rect = self.rect()
        p.setPen(QtGui.QPen(self._border_color, 1))
        p.setBrush(QtGui.QBrush(self._panel_color))
        p.drawRoundedRect(rect.adjusted(0, 0, -1, -1), 8, 8)

        faces, corners, edges = self._project_faces()
        self._face_regions = []
        self._edge_regions = []
        self._corner_regions = []

        faces.sort(key=lambda f: f["depth"])
        for face in faces:
            poly = QtGui.QPolygonF([QtCore.QPointF(pt[0], pt[1]) for pt in face["points"]])
            face_color = self._face_fill(face["normal_z"], face["name"])
            p.setBrush(QtGui.QBrush(face_color))
            p.setPen(QtGui.QPen(self._border_color, 1))
            p.drawPolygon(poly)

            label_pos = face["label_pos"]
            self._draw_face_label(p, face["label"], label_pos, face["label_angle"], self._text_color)

            self._face_regions.append((poly, face["name"], face["depth"]))

        self._draw_edge_zones(p, edges, self._border_color)
        self._draw_corner_zones(p, corners, self._border_color)
        self._draw_home_button(p, rect, self._accent_color, self._border_color, self._text_color)

    def _face_fill(self, normal_z: float, name: str) -> QtGui.QColor:
        shade = max(0.0, min(1.0, float(normal_z)))
        color = QtGui.QColor(self._face_color)
        color = color.lighter(110 + int(shade * 60))
        if name == self._active_name:
            return QtGui.QColor(self._active_color)
        if name == self._hover_name:
            return QtGui.QColor(self._hover_color)
        return color

    def _draw_face_label(self, p: QtGui.QPainter, label: str, pos, angle_deg: float, text: QtGui.QColor):
        p.save()
        p.translate(float(pos[0]), float(pos[1]))
        p.rotate(float(angle_deg))
        p.setPen(QtGui.QPen(text))
        font = p.font()
        font.setBold(True)
        font.setPointSize(7)
        p.setFont(font)
        metrics = QtGui.QFontMetrics(font)
        rect = QtCore.QRectF(metrics.boundingRect(label))
        rect.moveCenter(QtCore.QPointF(0.0, 0.0))
        p.drawText(rect, QtCore.Qt.AlignCenter, label)
        p.restore()

    def _draw_home_button(self, p: QtGui.QPainter, rect: QtCore.QRect, accent: QtGui.QColor, border: QtGui.QColor, text: QtGui.QColor):
        size = self._home_size
        x = rect.center().x() - size // 2
        y = rect.bottom() - size - self._padding
        self._home_rect = QtCore.QRect(x, y, size, size)

        p.setPen(QtGui.QPen(border, 1))
        p.setBrush(QtGui.QBrush(accent))
        p.drawRoundedRect(self._home_rect, 4, 4)

        p.setPen(QtGui.QPen(text))
        path = QtGui.QPainterPath()
        cx = self._home_rect.center().x()
        cy = self._home_rect.center().y()
        w = size * 0.5
        h = size * 0.45
        path.moveTo(cx, cy - h * 0.6)
        path.lineTo(cx - w * 0.6, cy - h * 0.05)
        path.lineTo(cx - w * 0.6, cy + h * 0.6)
        path.lineTo(cx + w * 0.6, cy + h * 0.6)
        path.lineTo(cx + w * 0.6, cy - h * 0.05)
        path.closeSubpath()
        p.setBrush(QtGui.QBrush(text))
        p.drawPath(path)

    def _marker_color(self, name: str, default: QtGui.QColor):
        if name == self._active_name:
            return QtGui.QColor(self._active_color)
        if name == self._hover_name:
            return QtGui.QColor(self._hover_color)
        return default

    def _draw_corner_zones(self, p: QtGui.QPainter, corners, border: QtGui.QColor):
        if not corners:
            return
        fill = QtGui.QColor(self._accent_color)
        fill.setAlpha(190)
        p.setPen(QtGui.QPen(border, 1))
        r = float(self._corner_radius)
        for corner in corners:
            cx, cy = corner["pos"]
            name = corner["name"]
            p.setBrush(QtGui.QBrush(self._marker_color(name, fill)))
            poly = QtGui.QPolygonF(
                [
                    QtCore.QPointF(cx, cy - r),
                    QtCore.QPointF(cx + r, cy),
                    QtCore.QPointF(cx, cy + r),
                    QtCore.QPointF(cx - r, cy),
                ]
            )
            p.drawPolygon(poly)
            self._corner_regions.append((poly, name, corner["depth"]))

    def _draw_edge_zones(self, p: QtGui.QPainter, edges, border: QtGui.QColor):
        if not edges:
            return
        fill = QtGui.QColor(self._accent_color)
        fill.setAlpha(190)
        p.setPen(QtGui.QPen(border, 1))
        r = float(self._corner_radius)
        for edge in edges:
            cx, cy = edge["pos"]
            name = edge["name"]
            p.setBrush(QtGui.QBrush(self._marker_color(name, fill)))
            poly = QtGui.QPolygonF(
                [
                    QtCore.QPointF(cx, cy - r),
                    QtCore.QPointF(cx + r, cy),
                    QtCore.QPointF(cx, cy + r),
                    QtCore.QPointF(cx - r, cy),
                ]
            )
            p.drawPolygon(poly)
            self._edge_regions.append((poly, name, edge["depth"]))

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        if self._home_rect.contains(a0.pos()):
            self.homeRequested.emit()
            a0.accept()
            return

        pos = QtCore.QPointF(a0.pos())
        name = self._hit_test_regions(self._corner_regions, pos)
        if name is None:
            name = self._hit_test_regions(self._edge_regions, pos)
        if name is None:
            name = self._hit_test_regions(self._face_regions, pos)

        if name is not None:
            self._active_name = name
            self.viewRequested.emit(name)
            a0.accept()
            self.update()
            return

        super().mousePressEvent(a0)

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent):
        pos = QtCore.QPointF(a0.pos())
        hover = self._hit_test_regions(self._corner_regions, pos)
        if hover is None:
            hover = self._hit_test_regions(self._edge_regions, pos)
        if hover is None:
            hover = self._hit_test_regions(self._face_regions, pos)

        if hover != self._hover_name:
            self._hover_name = hover
            self.update()
        super().mouseMoveEvent(a0)

    def leaveEvent(self, a0: QtCore.QEvent):
        if self._hover_name is not None:
            self._hover_name = None
            self.update()
        super().leaveEvent(a0)

    def _project_faces(self):
        right, up, forward = self._camera_basis()

        verts = np.array(
            [
                [-1.0, -1.0, -1.0],
                [1.0, -1.0, -1.0],
                [-1.0, 1.0, -1.0],
                [1.0, 1.0, -1.0],
                [-1.0, -1.0, 1.0],
                [1.0, -1.0, 1.0],
                [-1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0],
            ],
            dtype=float,
        )

        verts_cam = np.stack(
            [
                np.dot(verts, right),
                np.dot(verts, up),
                np.dot(verts, forward),
            ],
            axis=1,
        )

        x = verts_cam[:, 0]
        y = verts_cam[:, 1]
        z = verts_cam[:, 2]

        minx, maxx = float(np.min(x)), float(np.max(x))
        miny, maxy = float(np.min(y)), float(np.max(y))
        w = max(1e-6, maxx - minx)
        h = max(1e-6, maxy - miny)

        cube_area = QtCore.QRectF(
            self._padding,
            self._padding,
            self._cube_size - self._padding * 2,
            self._cube_size - self._padding * 2,
        )
        scale = min(cube_area.width() / w, cube_area.height() / h) * 0.9
        cx = cube_area.center().x()
        cy = cube_area.center().y()

        def project(idx):
            px = (x[idx] - (minx + w / 2.0)) * scale + cx
            py = (y[idx] - (miny + h / 2.0)) * scale + cy
            return (px, py)

        faces = [
            ("x", 1.0, [1, 3, 7, 5], np.array([1.0, 0.0, 0.0])),
            ("x", -1.0, [0, 4, 6, 2], np.array([-1.0, 0.0, 0.0])),
            ("y", 1.0, [2, 6, 7, 3], np.array([0.0, 1.0, 0.0])),
            ("y", -1.0, [0, 1, 5, 4], np.array([0.0, -1.0, 0.0])),
            ("z", 1.0, [4, 5, 7, 6], np.array([0.0, 0.0, 1.0])),
            ("z", -1.0, [0, 2, 3, 1], np.array([0.0, 0.0, -1.0])),
        ]

        result = []
        for axis, sign, idxs, normal in faces:
            pos_name, neg_name = self._axis_names(axis)
            name = pos_name if sign > 0 else neg_name
            if axis == "z":
                label = "TOP" if sign > 0 else "BOTTOM"
            else:
                label = name.upper()
            n_cam = np.array([np.dot(normal, right), np.dot(normal, up), np.dot(normal, forward)], dtype=float)
            if n_cam[2] <= 0:
                continue
            points = [project(idx) for idx in idxs]
            depth = float(np.mean([z[idx] for idx in idxs]))
            label_pos = self._polygon_centroid(points)
            angle = self._label_angle_from_points(points)
            result.append(
                {
                    "name": name,
                    "points": points,
                    "depth": depth,
                    "normal_z": float(n_cam[2]),
                    "label": label,
                    "label_pos": label_pos,
                    "label_angle": angle,
                }
            )
        corners = []
        proj_pts = [project(idx) for idx in range(len(verts))]
        for idx, pos in enumerate(proj_pts):
            if pos is None:
                continue
            depth = float(z[idx])
            if depth <= 0:
                continue
            vx, vy, vz = verts[idx]
            corner_name = self._corner_view_name(vx, vy, vz)
            corners.append(
                {
                    "pos": pos,
                    "depth": depth,
                    "name": corner_name,
                }
            )
        edges = self._edge_regions_from_vertices(verts, proj_pts, z)
        return result, corners, edges

    def _camera_basis(self):
        az = np.deg2rad(self._azimuth)
        el = np.deg2rad(self._elevation)
        cam = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)], dtype=float)
        forward = -cam
        up = np.array([0.0, 0.0, 1.0], dtype=float)
        if abs(np.dot(up, forward)) > 0.95:
            up = np.array([0.0, 1.0, 0.0], dtype=float)
        right = np.cross(up, forward)
        right /= max(1e-6, np.linalg.norm(right))
        up = np.cross(forward, right)
        up /= max(1e-6, np.linalg.norm(up))
        forward /= max(1e-6, np.linalg.norm(forward))
        return right, up, forward

    def _polygon_centroid(self, points):
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        return (sum(xs) / len(xs), sum(ys) / len(ys))

    def _label_angle_from_points(self, points):
        if len(points) < 2:
            return 0.0
        dx = float(points[1][0] - points[0][0])
        dy = float(points[1][1] - points[0][1])
        if abs(dx) < 1e-6 and abs(dy) < 1e-6:
            return 0.0
        angle = math.degrees(math.atan2(dy, dx))
        if angle < -90.0 or angle > 90.0:
            angle += 180.0
        return angle

    def _axis_names(self, axis: str):
        if axis == "x":
            return ("left", "right") if self.invert_x else ("right", "left")
        if axis == "y":
            return ("back", "front") if self.invert_y else ("front", "back")
        return ("bottom", "top") if self.invert_z else ("top", "bottom")

    def _face_sign(self, axis: str, name: str):
        pos_name, neg_name = self._axis_names(axis)
        if name == pos_name:
            return 1.0
        if name == neg_name:
            return -1.0
        return None

    def _hit_test_regions(self, regions, pos: QtCore.QPointF):
        hits = sorted(regions, key=lambda f: f[2], reverse=True)
        for poly, name, _depth in hits:
            if poly.containsPoint(pos, QtCore.Qt.WindingFill):
                return name
        return None

    def _corner_view_name(self, vx: float, vy: float, vz: float):
        x_pos, x_neg = self._axis_names("x")
        y_pos, y_neg = self._axis_names("y")
        z_pos, z_neg = self._axis_names("z")
        x_name = x_pos if vx >= 0 else x_neg
        y_name = y_pos if vy >= 0 else y_neg
        z_name = z_pos if vz >= 0 else z_neg
        return f"iso:{x_name}:{y_name}:{z_name}"

    def _edge_regions_from_vertices(self, verts, proj_pts, z_vals):
        edges = [
            (6, 7),  # front/top
            (4, 5),  # back/top
            (2, 3),  # front/bottom
            (0, 1),  # back/bottom
            (2, 6),  # left/front
            (3, 7),  # right/front
            (0, 4),  # left/back
            (1, 5),  # right/back
            (5, 7),  # right/top
            (4, 6),  # left/top
            (1, 3),  # right/bottom
            (0, 2),  # left/bottom
        ]

        result = []
        for a, b in edges:
            pa = proj_pts[a]
            pb = proj_pts[b]
            if pa is None or pb is None:
                continue
            depth = float((z_vals[a] + z_vals[b]) * 0.5)
            if depth <= 0:
                continue
            vx, vy, vz = (verts[a] + verts[b]) * 0.5
            x_pos, x_neg = self._axis_names("x")
            y_pos, y_neg = self._axis_names("y")
            z_pos, z_neg = self._axis_names("z")
            x_name = x_pos if vx >= 0 else x_neg
            y_name = y_pos if vy >= 0 else y_neg
            z_name = z_pos if vz >= 0 else z_neg

            if abs(vx) < 0.1:
                name = f"edge:{y_name}:{z_name}"
            elif abs(vy) < 0.1:
                name = f"edge:{x_name}:{z_name}"
            else:
                name = f"edge:{x_name}:{y_name}"

            cx = (pa[0] + pb[0]) * 0.5
            cy = (pa[1] + pb[1]) * 0.5
            result.append(
                {
                    "pos": (cx, cy),
                    "depth": depth,
                    "name": name,
                }
            )
        return result
