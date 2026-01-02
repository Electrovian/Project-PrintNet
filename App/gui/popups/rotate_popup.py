from PyQt5 import QtWidgets, QtCore

from .base_popup import BasePopup
from ..theme import theme_css


class RotatePopup(BasePopup):
    rotation_changed = QtCore.pyqtSignal(float, float, float)

    def __init__(self, parent=None):
        super().__init__("Rotate", parent=parent)
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
        row.addWidget(QtWidgets.QLabel("Rotation"))
        self._rot_spins = []
        for _ in range(3):
            spin = QtWidgets.QDoubleSpinBox()
            spin.setDecimals(2)
            spin.setRange(-360.0, 360.0)
            spin.setSingleStep(1.0)
            spin.setFixedWidth(86)
            spin.setEnabled(False)
            row.addWidget(spin)
            self._rot_spins.append(spin)
        row.addWidget(QtWidgets.QLabel("deg"))
        row.addStretch(1)
        layout.addLayout(row)

        note = QtWidgets.QLabel("Rotation controls are not implemented yet.")
        note.setObjectName("Muted")
        layout.addWidget(note)

    def _axis_label(self, text: str, color: str):
        lbl = QtWidgets.QLabel(text)
        lbl.setStyleSheet(f"color: {color}; font-weight: 600;")
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
