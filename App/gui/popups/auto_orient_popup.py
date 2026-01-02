from PyQt5 import QtWidgets, QtCore

from .base_popup import BasePopup


class AutoOrientPopup(BasePopup):
    orient_requested = QtCore.pyqtSignal(str)
    reset_requested = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("Auto orientation options", parent=parent)
        self._build_ui()

    def _build_ui(self):
        layout = self.content_layout()

        self.group = QtWidgets.QButtonGroup(self)
        self.default_radio = QtWidgets.QRadioButton("Default")
        self.support_radio = QtWidgets.QRadioButton("Minimize support volume")
        self.time_radio = QtWidgets.QRadioButton("Minimize print time")
        self.default_radio.setChecked(True)

        self.group.addButton(self.default_radio)
        self.group.addButton(self.support_radio)
        self.group.addButton(self.time_radio)

        layout.addWidget(self.default_radio)
        layout.addWidget(self.support_radio)
        layout.addWidget(self.time_radio)

        btn_row = QtWidgets.QHBoxLayout()
        self.orient_btn = QtWidgets.QPushButton("Orient")
        self.reset_btn = QtWidgets.QPushButton("Reset")
        self.orient_btn.clicked.connect(self._emit_orient)
        self.reset_btn.clicked.connect(self._emit_reset)
        btn_row.addWidget(self.orient_btn)
        btn_row.addWidget(self.reset_btn)
        btn_row.addStretch(1)
        layout.addLayout(btn_row)

    def _emit_orient(self):
        if self.default_radio.isChecked():
            mode = "default"
        elif self.support_radio.isChecked():
            mode = "min_support"
        else:
            mode = "min_time"
        self.orient_requested.emit(mode)

    def _emit_reset(self):
        self.default_radio.setChecked(True)
        self.reset_requested.emit()
