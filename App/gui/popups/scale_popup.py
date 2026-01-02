from PyQt5 import QtWidgets, QtCore

from .base_popup import BasePopup
from ..theme import theme_css


class ScalePopup(BasePopup):
    scale_changed = QtCore.pyqtSignal(float, float, float)

    def __init__(self, parent=None):
        super().__init__("Scale", parent=parent)
        self.setMinimumWidth(420)
        self._syncing = False
        self._build_ui()

    def _build_ui(self):
        layout = self.content_layout()

        self._axis_labels = {}
        header = QtWidgets.QHBoxLayout()
        header.setSpacing(12)
        header.addWidget(QtWidgets.QLabel("Scale"))
        header.addStretch(1)
        header.addWidget(self._axis_label("X", "axis_x"))
        header.addWidget(self._axis_label("Y", "axis_y"))
        header.addWidget(self._axis_label("Z", "axis_z"))
        layout.addLayout(header)

        scale_row = QtWidgets.QHBoxLayout()
        scale_row.setSpacing(8)
        scale_row.addWidget(QtWidgets.QLabel("Scale"))
        self._scale_spins = []
        for _ in range(3):
            spin = QtWidgets.QDoubleSpinBox()
            spin.setDecimals(2)
            spin.setRange(1.0, 500.0)
            spin.setSingleStep(1.0)
            spin.setValue(100.0)
            spin.setFixedWidth(86)
            spin.valueChanged.connect(self._emit_scale)
            scale_row.addWidget(spin)
            self._scale_spins.append(spin)
        scale_row.addWidget(QtWidgets.QLabel("%"))
        scale_row.addStretch(1)
        layout.addLayout(scale_row)

        size_row = QtWidgets.QHBoxLayout()
        size_row.setSpacing(8)
        size_row.addWidget(QtWidgets.QLabel("Size"))
        self._size_spins = []
        for _ in range(3):
            spin = QtWidgets.QDoubleSpinBox()
            spin.setDecimals(2)
            spin.setRange(0.0, 99999.0)
            spin.setSingleStep(1.0)
            spin.setFixedWidth(86)
            spin.setReadOnly(True)
            spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            size_row.addWidget(spin)
            self._size_spins.append(spin)
        size_row.addWidget(QtWidgets.QLabel("mm"))
        size_row.addStretch(1)
        layout.addLayout(size_row)

        self.uniform_check = QtWidgets.QCheckBox("Uniform scale")
        self.uniform_check.setChecked(True)
        self.uniform_check.toggled.connect(self._emit_scale)
        layout.addWidget(self.uniform_check)

    def _axis_label(self, text: str, color: str):
        lbl = QtWidgets.QLabel(text)
        self._axis_labels[text.lower()] = lbl
        lbl.setStyleSheet(f"color: {theme_css(color)}; font-weight: 600;")
        return lbl

    def set_scale(self, x: float, y: float, z: float):
        self._syncing = True
        try:
            values = (x, y, z)
            for spin, val in zip(self._scale_spins, values):
                spin.setValue(float(val))
        finally:
            self._syncing = False

    def set_size(self, x: float, y: float, z: float):
        self._syncing = True
        try:
            values = (x, y, z)
            for spin, val in zip(self._size_spins, values):
                spin.setValue(float(val))
        finally:
            self._syncing = False

    def _emit_scale(self):
        if self._syncing:
            return
        values = [float(s.value()) for s in self._scale_spins]
        if self.uniform_check.isChecked():
            sender = self.sender()
            v = None
            for spin in self._scale_spins:
                if spin is sender:
                    v = float(spin.value())
                    break
            if v is None:
                v = values[0]
            self._syncing = True
            try:
                for spin in self._scale_spins:
                    spin.setValue(v)
            finally:
                self._syncing = False
            values = [v, v, v]
        self.scale_changed.emit(values[0], values[1], values[2])

    def apply_theme(self):
        super().apply_theme()
        for axis, key in (("x", "axis_x"), ("y", "axis_y"), ("z", "axis_z")):
            lbl = self._axis_labels.get(axis)
            if lbl is not None:
                lbl.setStyleSheet(f"color: {theme_css(key)}; font-weight: 600;")
