# gui/transform_panel.py
from PyQt5 import QtWidgets, QtCore


class TransformPanel(QtWidgets.QWidget):
    """
    Transform UI:
      - Scale: apply button (optional)
      - Position X/Y: live (no apply)
      - Snap-to-grid toggle + grid size
    """

    scale_applied = QtCore.pyqtSignal(float)             # scale_factor
    position_changed = QtCore.pyqtSignal(float, float)   # x, y (live)
    snap_changed = QtCore.pyqtSignal(bool, float)        # enabled, step_mm

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QFormLayout(self)

        # ---- scale
        self.scale_spin = QtWidgets.QDoubleSpinBox()
        self.scale_spin.setRange(1.0, 500.0)
        self.scale_spin.setSingleStep(5.0)
        self.scale_spin.setValue(100.0)
        self.scale_spin.setSuffix(" %")

        self.apply_scale_btn = QtWidgets.QPushButton("Apply Scale")
        self.apply_scale_btn.clicked.connect(self._emit_scale)

        scale_row = QtWidgets.QHBoxLayout()
        scale_row.addWidget(self.scale_spin)
        scale_row.addWidget(self.apply_scale_btn)
        layout.addRow("Scale", scale_row)

        # ---- position (live)
        self.pos_x_spin = QtWidgets.QDoubleSpinBox()
        self.pos_x_spin.setRange(-500.0, 500.0)
        self.pos_x_spin.setSingleStep(1.0)
        self.pos_x_spin.setDecimals(3)
        self.pos_x_spin.setValue(0.0)
        self.pos_x_spin.setSuffix(" mm")

        self.pos_y_spin = QtWidgets.QDoubleSpinBox()
        self.pos_y_spin.setRange(-500.0, 500.0)
        self.pos_y_spin.setSingleStep(1.0)
        self.pos_y_spin.setDecimals(3)
        self.pos_y_spin.setValue(0.0)
        self.pos_y_spin.setSuffix(" mm")

        layout.addRow("Position X", self.pos_x_spin)
        layout.addRow("Position Y", self.pos_y_spin)

        self.pos_x_spin.valueChanged.connect(self._emit_position)
        self.pos_y_spin.valueChanged.connect(self._emit_position)

        # ---- snapping
        self.snap_enable = QtWidgets.QCheckBox("Snap to grid")
        self.snap_combo = QtWidgets.QComboBox()
        self.snap_combo.addItem("1 mm", 1.0)
        self.snap_combo.addItem("5 mm", 5.0)
        self.snap_combo.addItem("10 mm", 10.0)
        self.snap_combo.setCurrentIndex(0)

        snap_row = QtWidgets.QHBoxLayout()
        snap_row.addWidget(self.snap_enable)
        snap_row.addWidget(self.snap_combo)
        layout.addRow("Dragging", snap_row)

        self.snap_enable.toggled.connect(self._emit_snap)
        self.snap_combo.currentIndexChanged.connect(self._emit_snap)

        layout.addItem(
            QtWidgets.QSpacerItem(
                20, 20,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Expanding,
            )
        )

    # ---- API for MainWindow to update UI without feedback loops

    def set_position(self, x: float, y: float, block_signals: bool = True):
        if block_signals:
            bx = self.pos_x_spin.blockSignals(True)
            by = self.pos_y_spin.blockSignals(True)
            self.pos_x_spin.setValue(float(x))
            self.pos_y_spin.setValue(float(y))
            self.pos_x_spin.blockSignals(bx)
            self.pos_y_spin.blockSignals(by)
        else:
            self.pos_x_spin.setValue(float(x))
            self.pos_y_spin.setValue(float(y))

    def get_snap(self):
        return bool(self.snap_enable.isChecked()), float(self.snap_combo.currentData())

    # ---- signal emitters

    def _emit_scale(self):
        scale_pct = float(self.scale_spin.value())
        self.scale_applied.emit(scale_pct / 100.0)

    def _emit_position(self):
        x = float(self.pos_x_spin.value())
        y = float(self.pos_y_spin.value())
        self.position_changed.emit(x, y)

    def _emit_snap(self):
        enabled = bool(self.snap_enable.isChecked())
        step = float(self.snap_combo.currentData())
        self.snap_changed.emit(enabled, step)
