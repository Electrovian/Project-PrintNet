from PyQt5 import QtWidgets, QtCore

from slicer.gcode import SliceSettings
from config.defaults import DEFAULTS

class SettingsPanel(QtWidgets.QWidget):
    """Basic print settings panel (layer height, infill, etc.)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QtWidgets.QFormLayout(self)
        defaults = DEFAULTS["settings_panel"]
        layer = defaults["layer_height"]
        infill = defaults["infill"]
        speed = defaults["speed"]

        self.layer_height_spin = QtWidgets.QDoubleSpinBox()
        self.layer_height_spin.setRange(layer["min"], layer["max"])
        self.layer_height_spin.setSingleStep(layer["step"])
        self.layer_height_spin.setValue(layer["default"])

        self.infill_spin = QtWidgets.QSpinBox()
        self.infill_spin.setRange(infill["min"], infill["max"])
        self.infill_spin.setValue(infill["default"])

        self.speed_spin = QtWidgets.QDoubleSpinBox()
        self.speed_spin.setRange(speed["min"], speed["max"])
        self.speed_spin.setValue(speed["default"])

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
