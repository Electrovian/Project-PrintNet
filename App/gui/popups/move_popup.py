from PyQt5 import QtWidgets, QtCore

from .base_popup import BasePopup
from ..theme import theme_css


class MovePopup(BasePopup):
    position_changed = QtCore.pyqtSignal(float, float, float)
    center_requested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("Move", parent=parent)
        self._syncing = False
        self._build_ui()

    def _build_ui(self):
        layout = self.content_layout()

        header = QtWidgets.QHBoxLayout()
        header.setSpacing(12)
        world_label = QtWidgets.QLabel("World coordinates")
        world_label.setObjectName("Muted")
        header.addWidget(world_label)
        header.addStretch(1)
        header.addWidget(self._axis_label("X", theme_css("axis_x")))
        header.addWidget(self._axis_label("Y", theme_css("axis_y")))
        header.addWidget(self._axis_label("Z", theme_css("axis_z")))
        layout.addLayout(header)

        row = QtWidgets.QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(QtWidgets.QLabel("Position"))
        self._pos_spins = []
        for _ in range(3):
            spin = QtWidgets.QDoubleSpinBox()
            spin.setDecimals(2)
            spin.setRange(-9999.0, 9999.0)
            spin.setSingleStep(0.5)
            spin.setFixedWidth(86)
            spin.valueChanged.connect(self._emit_position)
            row.addWidget(spin)
            self._pos_spins.append(spin)
        row.addWidget(QtWidgets.QLabel("mm"))
        row.addStretch(1)
        layout.addLayout(row)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch(1)
        self.center_btn = QtWidgets.QPushButton("Center")
        self.center_btn.clicked.connect(self.center_requested.emit)
        btn_row.addWidget(self.center_btn)
        btn_row.addStretch(1)
        layout.addLayout(btn_row)

    def _axis_label(self, text: str, color: str):
        lbl = QtWidgets.QLabel(text)
        lbl.setStyleSheet(f"color: {color}; font-weight: 600;")
        return lbl

    def set_position(self, x: float, y: float, z: float):
        self._syncing = True
        try:
            values = (x, y, z)
            for spin, val in zip(self._pos_spins, values):
                spin.setValue(float(val))
        finally:
            self._syncing = False

    def _emit_position(self):
        if self._syncing:
            return
        x, y, z = [float(s.value()) for s in self._pos_spins]
        self.position_changed.emit(x, y, z)
