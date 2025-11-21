from PyQt5 import QtWidgets, QtCore

from slicer.gcode import SliceSettings

class SettingsPanel(QtWidgets.QWidget):
    """Basic print settings panel (layer height, infill, etc.)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QFormLayout(self)
        self.layer_height_spin = QtWidgets.QDoubleSpinBox()
        self.layer_height_spin.setRange(0.05, 1.0)
        self.layer_height_spin.setSingleStep(0.05)
        self.layer_height_spin.setValue(0.2)

        self.infill_spin = QtWidgets.QSpinBox()
        self.infill_spin.setRange(0, 100)
        self.infill_spin.setValue(15)

        self.speed_spin = QtWidgets.QDoubleSpinBox()
        self.speed_spin.setRange(10, 200)
        self.speed_spin.setValue(60.0)

        layout.addRow("Layer height (mm)", self.layer_height_spin)
        layout.addRow("Infill (%)", self.infill_spin)
        layout.addRow("Print speed (mm/s)", self.speed_spin)

        layout.addItem(QtWidgets.QSpacerItem(20, 20,
                                             QtWidgets.QSizePolicy.Minimum,
                                             QtWidgets.QSizePolicy.Expanding))

    def to_settings(self) -> SliceSettings:
        return SliceSettings(
            layer_height=float(self.layer_height_spin.value()),
            infill_percent=float(self.infill_spin.value()),
            print_speed=float(self.speed_spin.value()),
        )
