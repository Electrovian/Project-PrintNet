import math
from PyQt5 import QtWidgets, QtCore, QtGui

from .base_popup import BasePopup
from ..theme import theme_css, theme_qcolor
from config.defaults import DEFAULTS


class RotatePopup(BasePopup):
    rotation_changed = QtCore.pyqtSignal(float, float, float)
    reset_requested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("Rotate", parent=parent)
        self.setMinimumWidth(DEFAULTS["popups"]["min_width"])
        self._syncing = False
        self._build_ui()

    def _build_ui(self):
        layout = self.content_layout()

        self._axis_labels = {}
        header = QtWidgets.QHBoxLayout()
        header.setSpacing(12)
        world_label = QtWidgets.QLabel("World coordinates")
        world_label.setObjectName("Muted")
        header.addWidget(world_label)
        header.addStretch(1)
        header.addWidget(self._axis_label("X", "axis_x"))
        header.addWidget(self._axis_label("Y", "axis_y"))
        header.addWidget(self._axis_label("Z", "axis_z"))
        layout.addLayout(header)

        row = QtWidgets.QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(QtWidgets.QLabel("Rotation"))
        self._rot_spins = []
        popup_cfg = DEFAULTS["popups"]
        rot_cfg = popup_cfg["rotate"]
        for _ in range(3):
            spin = QtWidgets.QDoubleSpinBox()
            spin.setDecimals(rot_cfg["decimals"])
            spin.setRange(rot_cfg["min"], rot_cfg["max"])
            spin.setSingleStep(rot_cfg["step"])
            spin.setFixedWidth(popup_cfg["spin_width"])
            spin.valueChanged.connect(self._emit_rotation)
            row.addWidget(spin)
            self._rot_spins.append(spin)
        row.addWidget(QtWidgets.QLabel("deg"))
        self.reset_btn = QtWidgets.QToolButton()
        self.reset_btn.setAutoRaise(True)
        self.reset_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.reset_btn.setFixedSize(26, 26)
        self.reset_btn.setToolTip("Reset rotation")
        self.reset_btn.clicked.connect(self._emit_reset)
        row.addWidget(self.reset_btn)
        row.addStretch(1)
        layout.addLayout(row)

        note = QtWidgets.QLabel("Rotation is in world coordinates.")
        note.setObjectName("Muted")
        layout.addWidget(note)
        self._update_reset_icon()

    def _reset_icon_pixmap(self, color: QtGui.QColor):
        size = 18
        pm = QtGui.QPixmap(size, size)
        pm.fill(QtCore.Qt.transparent)
        p = QtGui.QPainter(pm)
        p.setRenderHint(QtGui.QPainter.Antialiasing, True)
        pen = QtGui.QPen(color, 2)
        p.setPen(pen)
        rect = QtCore.QRectF(3, 3, size - 6, size - 6)
        start_angle = 35
        span_angle = 280
        p.drawArc(rect, start_angle * 16, span_angle * 16)

        angle = math.radians(-50.0)
        cx = rect.center().x()
        cy = rect.center().y()
        r = rect.width() * 0.5
        tip = QtCore.QPointF(cx + r * math.cos(angle), cy + r * math.sin(angle))
        dir_vec = QtCore.QPointF(math.sin(angle), -math.cos(angle))
        length = math.hypot(dir_vec.x(), dir_vec.y())
        if length < 1e-6:
            length = 1.0
        dir_vec = QtCore.QPointF(dir_vec.x() / length, dir_vec.y() / length)
        normal = QtCore.QPointF(-dir_vec.y(), dir_vec.x())
        base = QtCore.QPointF(tip.x() - dir_vec.x() * 4.0, tip.y() - dir_vec.y() * 4.0)
        left = QtCore.QPointF(base.x() + normal.x() * 2.5, base.y() + normal.y() * 2.5)
        right = QtCore.QPointF(base.x() - normal.x() * 2.5, base.y() - normal.y() * 2.5)
        p.setBrush(QtGui.QBrush(color))
        p.drawPolygon(QtGui.QPolygonF([tip, left, right]))
        p.end()
        return pm

    def _update_reset_icon(self):
        color = theme_qcolor("rotate_reset")
        icon = QtGui.QIcon(self._reset_icon_pixmap(color))
        self.reset_btn.setIcon(icon)
        self.reset_btn.setIconSize(QtCore.QSize(18, 18))
        self.reset_btn.setStyleSheet(
            "QToolButton { border: none; background: transparent; }"
            f"QToolButton:hover {{ background: {theme_css('popup_button_hover_bg')}; border-radius: 4px; }}"
        )

    def _axis_label(self, text: str, color: str):
        lbl = QtWidgets.QLabel(text)
        self._axis_labels[text.lower()] = lbl
        lbl.setStyleSheet(f"color: {theme_css(color)}; font-weight: 600;")
        return lbl

    def set_rotation(self, x: float, y: float, z: float):
        self._syncing = True
        try:
            values = (x, y, z)
            for spin, val in zip(self._rot_spins, values):
                spin.setValue(float(val))
        finally:
            self._syncing = False

    def _emit_rotation(self):
        if self._syncing:
            return
        x, y, z = [float(s.value()) for s in self._rot_spins]
        self.rotation_changed.emit(x, y, z)

    def _emit_reset(self):
        self.set_rotation(0.0, 0.0, 0.0)
        self.reset_requested.emit()

    def apply_theme(self):
        super().apply_theme()
        for axis, key in (("x", "axis_x"), ("y", "axis_y"), ("z", "axis_z")):
            lbl = self._axis_labels.get(axis)
            if lbl is not None:
                lbl.setStyleSheet(f"color: {theme_css(key)}; font-weight: 600;")
        self._update_reset_icon()
