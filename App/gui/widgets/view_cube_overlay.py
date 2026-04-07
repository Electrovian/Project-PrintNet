import math
from typing import Optional

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

from ..theme import theme_qcolor


class ViewCubeOverlay(QtWidgets.QWidget):
    viewRequested = QtCore.pyqtSignal(str)
    orbitRequested = QtCore.pyqtSignal(float, float)
    fitRequested = QtCore.pyqtSignal()
    homeRequested = QtCore.pyqtSignal()
    menuRequested = QtCore.pyqtSignal(QtCore.QPoint)

    _FACE_NORMALS = {
        "front": np.array([-1.0, 0.0, 0.0], dtype=float),
        "back": np.array([1.0, 0.0, 0.0], dtype=float),
        "right": np.array([0.0, -1.0, 0.0], dtype=float),
        "left": np.array([0.0, 1.0, 0.0], dtype=float),
        "top": np.array([0.0, 0.0, -1.0], dtype=float),
        "bottom": np.array([0.0, 0.0, 1.0], dtype=float),
    }
    _SNAP_VECTORS = {
        "front": np.array([1.0, 0.0, 0.0], dtype=float),
        "back": np.array([-1.0, 0.0, 0.0], dtype=float),
        "right": np.array([0.0, 1.0, 0.0], dtype=float),
        "left": np.array([0.0, -1.0, 0.0], dtype=float),
        "top": np.array([0.0, 0.0, 1.0], dtype=float),
        "bottom": np.array([0.0, 0.0, -1.0], dtype=float),
    }
    _TRIPOD_VECTORS = {
        "X": np.array([0.0, -1.0, 0.0], dtype=float),
        "Y": np.array([1.0, 0.0, 0.0], dtype=float),
        "Z": np.array([0.0, 0.0, -1.0], dtype=float),
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._azimuth = 45.0
        self._elevation = 30.0
        self._cube_size = 132
        self._min_cube_size = 96
        self._max_cube_size = 260
        self._padding = 8
        self._button_gap = 10
        self._button_size = 34
        self._cube_rect = QtCore.QRectF()
        self._axis_origin = QtCore.QPointF()
        self._projected_cube_center = (0.0, 0.0)
        self._face_regions = []
        self._edge_regions = []
        self._corner_regions = []
        self._hover_name: Optional[str] = None
        self._active_name: Optional[str] = None
        self._pressed_target: Optional[str] = None
        self._press_pos: Optional[QtCore.QPointF] = None
        self._drag_last_pos: Optional[QtCore.QPointF] = None
        self._dragging_cube = False
        self._drag_threshold = 6.0
        self._label_cache: dict[tuple[object, ...], QtGui.QImage] = {}
        self._visible_label_layouts: dict[str, dict[str, object]] = {}
        self._apply_theme()

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)

        self._menu_button = self._build_button(
            "NavigatorMenuButton",
            "View options",
            self._build_button_icon("menu"),
        )
        self._menu_button.clicked.connect(self._emit_menu_requested)
        self._fit_button = self._build_button(
            "NavigatorFitButton",
            "Fit camera to scene or selected object.",
            self._build_button_icon("fit"),
        )
        self._fit_button.clicked.connect(self.fitRequested.emit)
        self._apply_button_theme()

    def _build_button(self, object_name: str, tooltip: str, icon: QtGui.QIcon) -> QtWidgets.QToolButton:
        button = QtWidgets.QToolButton(self)
        button.setObjectName(object_name)
        button.setAutoRaise(True)
        button.setCursor(QtCore.Qt.PointingHandCursor)
        button.setToolTip(str(tooltip or ""))
        button.setIcon(icon)
        return button

    def _emit_menu_requested(self) -> None:
        anchor = self._menu_button.mapToGlobal(self._menu_button.rect().bottomLeft())
        self.menuRequested.emit(anchor)

    def _apply_theme(self):
        self._panel_color = theme_qcolor("cube_panel")
        self._face_color = theme_qcolor("cube_face")
        self._border_color = theme_qcolor("cube_border")
        self._text_color = theme_qcolor("cube_text")
        self._accent_color = theme_qcolor("cube_accent")
        self._hover_color = theme_qcolor("cube_hover")
        self._active_color = theme_qcolor("cube_active")
        self._axis_x_color = theme_qcolor("axis_x")
        self._axis_y_color = theme_qcolor("axis_y")
        self._axis_z_color = theme_qcolor("axis_z")
        self._muted_text = theme_qcolor("popup_muted_text")
        self._button_bg = theme_qcolor("popup_bg")
        self._button_border = theme_qcolor("popup_border")
        self._button_hover = theme_qcolor("menu_hover_bg")

    def apply_theme(self):
        self._apply_theme()
        self._label_cache.clear()
        self._apply_button_theme()
        self.update()

    def _rgba_css(self, color: QtGui.QColor, alpha: int | None = None) -> str:
        c = QtGui.QColor(color)
        if alpha is not None:
            c.setAlpha(int(alpha))
        return f"rgba({c.red()}, {c.green()}, {c.blue()}, {c.alpha()})"

    def _apply_button_theme(self) -> None:
        radius = max(14, int(round(self._button_size * 0.5)))
        style = (
            "QToolButton {"
            f"background-color: {self._rgba_css(self._button_bg, 186)};"
            f"border: 1px solid {self._rgba_css(self._button_border, 210)};"
            f"border-radius: {radius}px;"
            "padding: 0;"
            "}"
            "QToolButton:hover {"
            f"background-color: {self._rgba_css(self._button_hover, 224)};"
            f"border-color: {self._rgba_css(self._accent_color, 235)};"
            "}"
            "QToolButton:pressed {"
            f"background-color: {self._rgba_css(self._accent_color, 172)};"
            f"border-color: {self._rgba_css(self._accent_color, 255)};"
            "}"
        )
        for button in (self._menu_button, self._fit_button):
            button.setStyleSheet(style)
            button.setIconSize(QtCore.QSize(max(14, int(round(self._button_size * 0.44))), max(14, int(round(self._button_size * 0.44)))))
        self._menu_button.setIcon(self._build_button_icon("menu"))
        self._fit_button.setIcon(self._build_button_icon("fit"))

    def _build_button_icon(self, kind: str) -> QtGui.QIcon:
        size = max(18, int(round(self._button_size * 0.5)))
        pm = QtGui.QPixmap(size, size)
        pm.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pm)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        color = QtGui.QColor(self._muted_text)
        pen = QtGui.QPen(color, max(1.4, size * 0.09))
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setJoinStyle(QtCore.Qt.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.NoBrush)

        if kind == "menu":
            left = size * 0.18
            right = size * 0.82
            for y in (size * 0.3, size * 0.5, size * 0.7):
                painter.drawLine(QtCore.QPointF(left, y), QtCore.QPointF(right, y))
        else:
            lens = QtCore.QRectF(size * 0.18, size * 0.18, size * 0.42, size * 0.42)
            painter.drawEllipse(lens)
            painter.drawLine(
                QtCore.QLineF(
                    QtCore.QPointF(lens.right() - size * 0.01, lens.bottom() - size * 0.01),
                    QtCore.QPointF(size * 0.82, size * 0.82),
                )
            )
        painter.end()
        return QtGui.QIcon(pm)

    def sizeHint(self):
        return QtCore.QSize(self._cube_size, self._cube_size)

    def set_cube_size(self, size: int):
        target = max(int(self._min_cube_size), min(int(self._max_cube_size), int(size)))
        if target == self._cube_size:
            return
        self._cube_size = target
        self._padding = max(8, int(round(target * 0.07)))
        self._button_gap = max(8, int(round(target * 0.06)))
        self._button_size = max(28, min(46, int(round(target * 0.24))))
        self._drag_threshold = max(4.0, target * 0.04)
        self._label_cache.clear()
        self.updateGeometry()
        self._apply_button_theme()
        self._relayout()
        self.update()

    def set_camera(self, azimuth: float, elevation: float):
        if abs(self._azimuth - azimuth) < 1e-3 and abs(self._elevation - elevation) < 1e-3:
            return
        self._azimuth = float(azimuth)
        self._elevation = float(elevation)
        self.update()

    def resizeEvent(self, event: QtGui.QResizeEvent):
        super().resizeEvent(event)
        self._relayout()

    def _relayout(self) -> None:
        footprint = max(1, min(self.width() or self._cube_size, self.height() or self._cube_size))
        cube_edge = max(48.0, footprint * 0.48)
        margin = max(8.0, footprint * 0.07)
        tripod_left = max(16.0, footprint * 0.18)
        tripod_bottom = max(18.0, footprint * 0.18)
        control_gap = float(self._button_gap)

        cube_left = margin + tripod_left
        cube_top = margin + max(2.0, footprint * 0.02)
        button_x = min(
            self.width() - margin - self._button_size,
            cube_left + cube_edge + control_gap,
        )
        if button_x < cube_left + cube_edge * 0.84:
            button_x = cube_left + cube_edge * 0.84
        stack_height = self._button_size * 2 + control_gap
        stack_top = cube_top + (cube_edge - stack_height) * 0.5

        self._cube_rect = QtCore.QRectF(cube_left, cube_top, cube_edge, cube_edge)
        self._axis_origin = QtCore.QPointF(margin + tripod_left * 0.33, self.height() - margin - tripod_bottom * 0.18)

        self._menu_button.setGeometry(
            int(round(button_x)),
            int(round(stack_top)),
            int(self._button_size),
            int(self._button_size),
        )
        self._fit_button.setGeometry(
            int(round(button_x)),
            int(round(stack_top + self._button_size + control_gap)),
            int(self._button_size),
            int(self._button_size),
        )

    def paintEvent(self, event: QtGui.QPaintEvent):
        del event
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)

        faces, corners, edges = self._project_faces()
        self._face_regions = []
        self._edge_regions = []
        self._corner_regions = []
        self._visible_label_layouts = {}

        border = QtGui.QColor(self._border_color)
        border.setAlpha(182)
        border_pen = QtGui.QPen(border, max(1.0, self._cube_rect.width() * 0.018))
        border_pen.setJoinStyle(QtCore.Qt.RoundJoin)

        self._draw_axis_tripod(painter)

        faces.sort(key=lambda face: face["depth"])
        for face in faces:
            poly = QtGui.QPolygonF([QtCore.QPointF(pt[0], pt[1]) for pt in face["points"]])
            painter.setBrush(QtGui.QBrush(self._face_fill(face["normal_z"], face["name"])))
            painter.setPen(border_pen)
            painter.drawPolygon(poly)
            self._face_regions.append((poly, face["name"], face["depth"]))

        self._draw_hover_marker(painter, corners, self._corner_regions, radius=max(3.0, self._cube_rect.width() * 0.05))
        self._draw_hover_marker(painter, edges, self._edge_regions, radius=max(2.5, self._cube_rect.width() * 0.04))
        self._draw_face_labels(painter, faces)

    def _face_fill(self, normal_z: float, name: str) -> QtGui.QColor:
        if name == self._active_name:
            color = QtGui.QColor(self._active_color)
            color.setAlpha(232)
            return color
        if name == self._hover_name:
            color = QtGui.QColor(self._hover_color)
            color.setAlpha(224)
            return color
        shade = max(0.0, min(1.0, float(normal_z)))
        color = QtGui.QColor(self._face_color)
        color = color.lighter(92 + int(shade * 18))
        color.setAlpha(235)
        return color

    def _draw_face_labels(self, painter: QtGui.QPainter, faces) -> None:
        for face in faces:
            poly = QtGui.QPolygonF([QtCore.QPointF(pt[0], pt[1]) for pt in face["points"]])
            image = self._face_label_image(face)
            target = self._label_target_rect(poly, image, face["label_pos"])
            clip_path = QtGui.QPainterPath()
            clip_path.addPolygon(poly)
            painter.save()
            painter.setClipPath(clip_path, QtCore.Qt.IntersectClip)
            painter.drawImage(target.topLeft(), image)
            painter.restore()
            self._visible_label_layouts[str(face["name"])] = {
                "label": str(face["label"]),
                "bounds": QtCore.QRect(
                    int(math.floor(target.left())),
                    int(math.floor(target.top())),
                    int(math.ceil(target.width())),
                    int(math.ceil(target.height())),
                ),
                "polygon": QtGui.QPolygonF(poly),
                "angle": float(face["label_angle"]),
            }

    def _face_label_font(self, pixel_size: int) -> QtGui.QFont:
        font = QtGui.QFont(self.font())
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        font.setWeight(QtGui.QFont.Black)
        font.setPixelSize(max(13, int(pixel_size)))
        font.setLetterSpacing(
            QtGui.QFont.AbsoluteSpacing,
            max(0.0, self._cube_rect.width() * 0.005),
        )
        return font

    def _face_label_image(self, face: dict[str, object]) -> QtGui.QImage:
        label = str(face["label"])
        angle_deg = round(float(face["label_angle"]), 1)
        font_px = self._face_label_pixel_size(face)
        text_color = QtGui.QColor(self._text_color).lighter(114)
        color_key = (
            int(text_color.rgba()),
            int(QtGui.QColor(0, 0, 0, 56).rgba()),
        )
        cache_key = (
            label,
            angle_deg,
            font_px,
            round(float(self.devicePixelRatioF()), 3),
            color_key,
        )
        cached = self._label_cache.get(cache_key)
        if cached is not None:
            return QtGui.QImage(cached)

        font = self._face_label_font(font_px)
        metrics = QtGui.QFontMetrics(font)
        bounds = metrics.tightBoundingRect(label)
        padding = max(4, int(round(self._cube_rect.width() * 0.04)))
        base = QtGui.QImage(
            max(1, bounds.width() + padding * 2),
            max(1, bounds.height() + padding * 2),
            QtGui.QImage.Format_ARGB32_Premultiplied,
        )
        base.fill(QtCore.Qt.transparent)

        painter = QtGui.QPainter(base)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        painter.setFont(font)
        rect = QtCore.QRectF(0.0, 0.0, float(base.width()), float(base.height()))
        shadow = QtGui.QColor(0, 0, 0, 56)
        offset = max(0.8, self._cube_rect.width() * 0.01)
        shadow_rect = QtCore.QRectF(rect)
        shadow_rect.translate(offset, offset)
        painter.setPen(shadow)
        painter.drawText(shadow_rect, QtCore.Qt.AlignCenter, label)
        painter.setPen(QtGui.QPen(text_color))
        painter.drawText(rect, QtCore.Qt.AlignCenter, label)
        painter.end()

        rotated = base
        if abs(angle_deg) > 0.25:
            transform = QtGui.QTransform()
            transform.rotate(float(angle_deg))
            rotated = base.transformed(transform, QtCore.Qt.SmoothTransformation)
        rotated = rotated.convertToFormat(QtGui.QImage.Format_ARGB32_Premultiplied)
        self._label_cache[cache_key] = QtGui.QImage(rotated)
        return QtGui.QImage(rotated)

    def _face_label_pixel_size(self, face: dict[str, object]) -> int:
        points = [QtCore.QPointF(pt[0], pt[1]) for pt in face["points"]]
        if len(points) < 2:
            return max(12, int(round(self._cube_rect.width() * 0.16)))
        edge_lengths = [
            QtCore.QLineF(points[idx], points[(idx + 1) % len(points)]).length()
            for idx in range(len(points))
        ]
        face_span = min(edge_lengths) if edge_lengths else self._cube_rect.width() * 0.4
        return max(13, min(28, int(round(face_span * 0.30))))

    def _label_target_rect(
        self,
        polygon: QtGui.QPolygonF,
        image: QtGui.QImage,
        preferred_pos,
    ) -> QtCore.QRectF:
        center = self._clamp_label_center(
            polygon,
            QtCore.QPointF(float(preferred_pos[0]), float(preferred_pos[1])),
            QtCore.QSizeF(float(image.width()), float(image.height())),
        )
        return QtCore.QRectF(
            center.x() - image.width() * 0.5,
            center.y() - image.height() * 0.5,
            float(image.width()),
            float(image.height()),
        )

    def _clamp_label_center(
        self,
        polygon: QtGui.QPolygonF,
        center: QtCore.QPointF,
        image_size: QtCore.QSizeF,
    ) -> QtCore.QPointF:
        bounds = polygon.boundingRect()
        margin = max(2.0, self._cube_rect.width() * 0.025)
        inner = bounds.adjusted(margin, margin, -margin, -margin)
        half_w = image_size.width() * 0.5
        half_h = image_size.height() * 0.5
        if inner.width() > image_size.width():
            center.setX(max(inner.left() + half_w, min(inner.right() - half_w, center.x())))
        if inner.height() > image_size.height():
            center.setY(max(inner.top() + half_h, min(inner.bottom() - half_h, center.y())))
        return center

    def _draw_axis_tripod(self, painter: QtGui.QPainter) -> None:
        axes = self._tripod_axes()

        painter.save()
        font = painter.font()
        font.setBold(True)
        font.setPointSize(max(7, int(round(self._cube_rect.width() * 0.11))))
        painter.setFont(font)
        for axis in sorted(axes, key=lambda item: float(item["depth"])):
            pen = QtGui.QPen(axis["color"], max(1.6, self._cube_rect.width() * 0.022))
            pen.setCapStyle(QtCore.Qt.RoundCap)
            painter.setPen(pen)
            painter.drawLine(axis["base"], axis["end"])
            painter.drawText(axis["label_pos"], str(axis["label"]))
        painter.restore()

    def _tripod_axes(self) -> list[dict[str, object]]:
        base = QtCore.QPointF(self._axis_origin)
        axis_len = max(16.0, self._cube_rect.width() * 0.52)
        right, up, forward = self._camera_basis()
        axes = []

        for label, color, vector in (
            ("X", self._axis_x_color, self._TRIPOD_VECTORS["X"]),
            ("Y", self._axis_y_color, self._TRIPOD_VECTORS["Y"]),
            ("Z", self._axis_z_color, self._TRIPOD_VECTORS["Z"]),
        ):
            projected = np.array(
                [
                    np.dot(vector, right),
                    np.dot(vector, up),
                ],
                dtype=float,
            )
            screen_len = float(np.linalg.norm(projected))
            depth = float(np.dot(vector, forward))
            if screen_len > 1e-6:
                direction = projected / screen_len
            else:
                direction = np.array([0.0, -1.0 if depth >= 0.0 else 1.0], dtype=float)
            visible_len = axis_len * max(0.18, min(1.0, screen_len))
            end = QtCore.QPointF(
                base.x() + float(direction[0]) * visible_len,
                base.y() + float(direction[1]) * visible_len,
            )
            label_pos = QtCore.QPointF(
                end.x() + (4.0 if float(direction[0]) >= -0.1 else -10.0),
                end.y() + (12.0 if float(direction[1]) >= 0.15 else -2.0),
            )
            axes.append(
                {
                    "label": label,
                    "color": QtGui.QColor(color),
                    "vector": np.array(vector, dtype=float),
                    "base": QtCore.QPointF(base),
                    "end": end,
                    "label_pos": label_pos,
                    "depth": depth,
                }
            )
        return axes

    def _draw_hover_marker(self, painter: QtGui.QPainter, items, regions, radius: float) -> None:
        if not items:
            return
        hover_name = self._hover_name if self._hover_name and self._hover_name not in self._FACE_NORMALS else None
        active_name = self._active_name if self._active_name and self._active_name not in self._FACE_NORMALS else None
        target_name = active_name or hover_name

        for item in items:
            point = QtCore.QPointF(float(item["pos"][0]), float(item["pos"][1]))
            marker_poly = QtGui.QPolygonF(
                [
                    QtCore.QPointF(point.x() - radius, point.y()),
                    QtCore.QPointF(point.x(), point.y() - radius),
                    QtCore.QPointF(point.x() + radius, point.y()),
                    QtCore.QPointF(point.x(), point.y() + radius),
                ]
            )
            regions.append((marker_poly, item["name"], item["depth"]))
            if item["name"] != target_name:
                continue
            if not target_name:
                continue
            fill = QtGui.QColor(self._hover_color if item["name"] == hover_name else self._active_color)
            fill.setAlpha(160)
            border = QtGui.QColor(self._border_color)
            border.setAlpha(190)
            painter.setBrush(QtGui.QBrush(fill))
            painter.setPen(QtGui.QPen(border, max(1.0, radius * 0.34)))
            painter.drawEllipse(point, radius, radius)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() != QtCore.Qt.LeftButton:
            super().mousePressEvent(event)
            return
        pos = QtCore.QPointF(event.pos())
        self._press_pos = pos
        self._drag_last_pos = pos
        self._dragging_cube = False
        self._pressed_target = self._hit_test_any(pos)
        if self._pressed_target is not None or self._cube_rect.adjusted(-4.0, -4.0, 4.0, 4.0).contains(pos):
            self._active_name = self._pressed_target
            self._update_cursor(True)
            event.accept()
            self.update()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        pos = QtCore.QPointF(event.pos())
        if self._press_pos is not None and bool(event.buttons() & QtCore.Qt.LeftButton):
            diff = pos - (self._drag_last_pos or pos)
            total = pos - self._press_pos
            if self._dragging_cube or abs(total.x()) >= self._drag_threshold or abs(total.y()) >= self._drag_threshold:
                self._dragging_cube = True
                self._pressed_target = None
                self._hover_name = None
                self._active_name = None
                self._drag_last_pos = pos
                self._update_cursor(True)
                self.orbitRequested.emit(float(-diff.x()), float(diff.y()))
                event.accept()
                self.update()
                return

        hover = self._hit_test_any(pos)
        if hover != self._hover_name:
            self._hover_name = hover
            self._update_cursor(False)
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.LeftButton and self._press_pos is not None:
            pressed_target = self._pressed_target
            dragging = self._dragging_cube
            self._press_pos = None
            self._drag_last_pos = None
            self._pressed_target = None
            self._dragging_cube = False
            self._active_name = None
            self._update_cursor(False)
            if not dragging and pressed_target is not None:
                self.viewRequested.emit(str(pressed_target))
                event.accept()
                self.update()
                return
        super().mouseReleaseEvent(event)

    def leaveEvent(self, event: QtCore.QEvent):
        if self._hover_name is not None and not self._dragging_cube:
            self._hover_name = None
            self._update_cursor(False)
            self.update()
        super().leaveEvent(event)

    def _update_cursor(self, dragging: bool) -> None:
        if dragging and self._press_pos is not None:
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            return
        if self._hover_name is not None or self._cube_rect.adjusted(-4.0, -4.0, 4.0, 4.0).contains(self.mapFromGlobal(QtGui.QCursor.pos())):
            self.setCursor(QtCore.Qt.OpenHandCursor)
            return
        self.unsetCursor()

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

        cube_area = QtCore.QRectF(self._cube_rect)
        minx, maxx = float(np.min(x)), float(np.max(x))
        miny, maxy = float(np.min(y)), float(np.max(y))
        width = max(1e-6, maxx - minx)
        height = max(1e-6, maxy - miny)
        scale = min(cube_area.width() / width, cube_area.height() / height) * 0.78
        cx = cube_area.center().x()
        cy = cube_area.center().y()

        def project(idx: int) -> tuple[float, float]:
            px = (x[idx] - (minx + width * 0.5)) * scale + cx
            py = (y[idx] - (miny + height * 0.5)) * scale + cy
            return (float(px), float(py))

        faces = [
            ("back", [1, 3, 7, 5], self._FACE_NORMALS["back"]),
            ("front", [0, 4, 6, 2], self._FACE_NORMALS["front"]),
            ("left", [2, 6, 7, 3], self._FACE_NORMALS["left"]),
            ("right", [0, 1, 5, 4], self._FACE_NORMALS["right"]),
            ("bottom", [4, 5, 7, 6], self._FACE_NORMALS["bottom"]),
            ("top", [0, 2, 3, 1], self._FACE_NORMALS["top"]),
        ]

        result = []
        for name, idxs, normal in faces:
            n_cam = np.array([np.dot(normal, right), np.dot(normal, up), np.dot(normal, forward)], dtype=float)
            if n_cam[2] <= 0:
                continue
            points = [project(idx) for idx in idxs]
            depth = float(np.mean([z[idx] for idx in idxs]))
            result.append(
                {
                    "name": name,
                    "label": name.title(),
                    "points": points,
                    "depth": depth,
                    "normal_z": float(n_cam[2]),
                    "label_pos": self._polygon_centroid(points),
                    "label_angle": self._label_angle_from_points(points),
                }
            )

        proj_pts = [project(idx) for idx in range(len(verts))]
        if proj_pts:
            avg_x = sum(point[0] for point in proj_pts) / len(proj_pts)
            avg_y = sum(point[1] for point in proj_pts) / len(proj_pts)
            self._projected_cube_center = (float(avg_x), float(avg_y))
        else:
            self._projected_cube_center = (float(cx), float(cy))

        corners = []
        for idx, pos in enumerate(proj_pts):
            depth = float(z[idx])
            if depth <= 0:
                continue
            vx, vy, vz = verts[idx]
            corners.append(
                {
                    "pos": pos,
                    "depth": depth,
                    "name": self._corner_view_name(vx, vy, vz),
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

    @staticmethod
    def _polygon_centroid(points):
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        return (sum(xs) / len(xs), sum(ys) / len(ys))

    @staticmethod
    def _label_angle_from_points(points):
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

    def _hit_test_any(self, pos: QtCore.QPointF) -> Optional[str]:
        for regions in (self._corner_regions, self._edge_regions, self._face_regions):
            hit = self._hit_test_regions(regions, pos)
            if hit is not None:
                return str(hit)
        return None

    @staticmethod
    def _hit_test_regions(regions, pos: QtCore.QPointF) -> Optional[str]:
        hits = sorted(regions, key=lambda item: item[2], reverse=True)
        for poly, name, _depth in hits:
            if poly.containsPoint(pos, QtCore.Qt.WindingFill):
                return str(name)
        return None

    @classmethod
    def _name_for_components(cls, *, vx: float | None = None, vy: float | None = None, vz: float | None = None):
        names = []
        if vx is not None:
            names.append("back" if vx > 0 else "front")
        if vy is not None:
            names.append("left" if vy > 0 else "right")
        if vz is not None:
            names.append("bottom" if vz > 0 else "top")
        return names

    @classmethod
    def _corner_view_name(cls, vx: float, vy: float, vz: float):
        x_name, y_name, z_name = cls._name_for_components(vx=vx, vy=vy, vz=vz)
        return f"iso:{x_name}:{y_name}:{z_name}"

    @classmethod
    def _edge_regions_from_vertices(cls, verts, proj_pts, z_vals):
        edges = [
            (6, 7),
            (4, 5),
            (2, 3),
            (0, 1),
            (2, 6),
            (3, 7),
            (0, 4),
            (1, 5),
            (5, 7),
            (4, 6),
            (1, 3),
            (0, 2),
        ]

        result = []
        for a, b in edges:
            pa = proj_pts[a]
            pb = proj_pts[b]
            depth = float((z_vals[a] + z_vals[b]) * 0.5)
            if depth <= 0:
                continue
            vx, vy, vz = (verts[a] + verts[b]) * 0.5
            if abs(vx) < 0.1:
                first, second = cls._name_for_components(vy=vy, vz=vz)
            elif abs(vy) < 0.1:
                first, second = cls._name_for_components(vx=vx, vz=vz)
            else:
                first, second = cls._name_for_components(vx=vx, vy=vy)
            result.append(
                {
                    "pos": ((pa[0] + pb[0]) * 0.5, (pa[1] + pb[1]) * 0.5),
                    "depth": depth,
                    "name": f"edge:{first}:{second}",
                }
            )
        return result
