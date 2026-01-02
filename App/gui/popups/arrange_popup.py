from PyQt5 import QtWidgets, QtCore

from .base_popup import BasePopup


class ArrangePopup(BasePopup):
    arrange_requested = QtCore.pyqtSignal()
    arrange_selected_requested = QtCore.pyqtSignal()
    reset_requested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("Arrange options", parent=parent)
        self.setMinimumWidth(340)
        self._build_ui()

    def _build_ui(self):
        layout = self.content_layout()

        spacing_row = QtWidgets.QHBoxLayout()
        spacing_row.addWidget(QtWidgets.QLabel("Spacing"))
        self.spacing_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.spacing_slider.setRange(0, 20)
        self.spacing_slider.setSingleStep(1)
        self.spacing_slider.setValue(0)
        spacing_row.addWidget(self.spacing_slider, stretch=1)

        self.spacing_spin = QtWidgets.QDoubleSpinBox()
        self.spacing_spin.setRange(0.0, 20.0)
        self.spacing_spin.setDecimals(2)
        self.spacing_spin.setSingleStep(0.5)
        self.spacing_spin.setFixedWidth(86)
        spacing_row.addWidget(self.spacing_spin)
        layout.addLayout(spacing_row)

        hint = QtWidgets.QLabel("0 means auto spacing.")
        hint.setObjectName("Muted")
        layout.addWidget(hint)

        self.auto_rotate = QtWidgets.QCheckBox("Auto rotate for arrangement")
        self.multi_filament = QtWidgets.QCheckBox("Allow multiple filaments on same plate")
        self.multi_filament.setChecked(True)
        self.align_y = QtWidgets.QCheckBox("Align to Y axis")
        layout.addWidget(self.auto_rotate)
        layout.addWidget(self.multi_filament)
        layout.addWidget(self.align_y)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        layout.addWidget(line)

        btn_row = QtWidgets.QHBoxLayout()
        self.reset_btn = QtWidgets.QPushButton("Reset")
        self.arrange_btn = QtWidgets.QPushButton("Arrange")
        self.arrange_selected_btn = QtWidgets.QPushButton("Arrange Selected")
        self.reset_btn.clicked.connect(self._emit_reset)
        self.arrange_btn.clicked.connect(self.arrange_requested.emit)
        self.arrange_selected_btn.clicked.connect(self.arrange_selected_requested.emit)
        btn_row.addWidget(self.reset_btn)
        btn_row.addWidget(self.arrange_btn)
        btn_row.addWidget(self.arrange_selected_btn)
        btn_row.addStretch(1)
        layout.addLayout(btn_row)

        self.spacing_slider.valueChanged.connect(self._sync_spacing_from_slider)
        self.spacing_spin.valueChanged.connect(self._sync_spacing_from_spin)

    def _sync_spacing_from_slider(self, value: int):
        self.spacing_spin.blockSignals(True)
        try:
            self.spacing_spin.setValue(float(value))
        finally:
            self.spacing_spin.blockSignals(False)

    def _sync_spacing_from_spin(self, value: float):
        self.spacing_slider.blockSignals(True)
        try:
            self.spacing_slider.setValue(int(round(value)))
        finally:
            self.spacing_slider.blockSignals(False)

    def _emit_reset(self):
        self.spacing_slider.setValue(0)
        self.auto_rotate.setChecked(False)
        self.multi_filament.setChecked(False)
        self.align_y.setChecked(False)
        self.reset_requested.emit()
