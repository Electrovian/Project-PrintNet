from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from PyQt5 import QtCore, QtWidgets

from ..theme import theme_css


@dataclass(frozen=True)
class DetailLevel:
    label: str
    ratio: float


DETAIL_LEVELS: List[DetailLevel] = [
    DetailLevel("Extra low", 0.003),
    DetailLevel("Low", 0.005),
    DetailLevel("Medium", 0.015),
    DetailLevel("High", 0.035),
    DetailLevel("Extra high", 0.07),
]


class SimplifyDialog(QtWidgets.QDialog):
    applyRequested = QtCore.pyqtSignal(int)
    wireframeChanged = QtCore.pyqtSignal(bool)

    def __init__(self, mesh_name: str, triangles: int, parent=None):
        super().__init__(parent)
        self._mesh_name = mesh_name
        self._triangles = max(0, int(triangles))
        self._detail_ratio = DETAIL_LEVELS[2].ratio
        self._ratio_reduction = max(0.0, min(99.9, (1.0 - self._detail_ratio) * 100.0))
        self._build_ui()
        self._sync_detail_ui()
        self._sync_ratio_ui()

    def _build_ui(self):
        self.setWindowTitle("Simplify")
        self.setModal(True)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        header = QtWidgets.QGridLayout()
        header.setHorizontalSpacing(10)
        mesh_label = QtWidgets.QLabel("Mesh name:", self)
        mesh_label.setObjectName("SimplifyHeader")
        header.addWidget(mesh_label, 0, 0)
        self._mesh_value = QtWidgets.QLabel(self._mesh_name, self)
        self._mesh_value.setObjectName("SimplifyValue")
        header.addWidget(self._mesh_value, 0, 1)
        tri_label = QtWidgets.QLabel("Triangles:", self)
        tri_label.setObjectName("SimplifyHeader")
        header.addWidget(tri_label, 1, 0)
        self._tri_value = QtWidgets.QLabel(f"{self._triangles}", self)
        self._tri_value.setObjectName("SimplifyValue")
        header.addWidget(self._tri_value, 1, 1)
        header.setColumnStretch(1, 1)
        layout.addLayout(header)

        self._detail_radio = QtWidgets.QRadioButton("Detail level", self)
        self._detail_radio.setChecked(True)
        layout.addWidget(self._detail_radio)

        detail_row = QtWidgets.QHBoxLayout()
        self._detail_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self._detail_slider.setRange(0, len(DETAIL_LEVELS) - 1)
        self._detail_slider.setValue(2)
        detail_row.addWidget(self._detail_slider, 1)
        self._detail_label = QtWidgets.QLabel("Medium", self)
        self._detail_label.setObjectName("SimplifyAccent")
        detail_row.addWidget(self._detail_label)
        layout.addLayout(detail_row)

        self._detail_target = QtWidgets.QLabel("", self)
        self._detail_target.setObjectName("SimplifyMuted")
        layout.addWidget(self._detail_target)

        self._ratio_radio = QtWidgets.QRadioButton("Decimate ratio", self)
        layout.addWidget(self._ratio_radio)

        ratio_row = QtWidgets.QHBoxLayout()
        self._ratio_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self._ratio_slider.setRange(0, 999)
        self._ratio_slider.setValue(int(self._ratio_reduction * 10))
        ratio_row.addWidget(self._ratio_slider, 1)
        self._ratio_display = QtWidgets.QLineEdit(self)
        self._ratio_display.setReadOnly(True)
        self._ratio_display.setFixedWidth(80)
        ratio_row.addWidget(self._ratio_display)
        layout.addLayout(ratio_row)

        self._ratio_target = QtWidgets.QLabel("", self)
        self._ratio_target.setObjectName("SimplifyMuted")
        layout.addWidget(self._ratio_target)

        self._wireframe_check = QtWidgets.QCheckBox("Show wireframe", self)
        self._wireframe_check.setChecked(True)
        layout.addWidget(self._wireframe_check)

        btn_row = QtWidgets.QHBoxLayout()
        btn_row.addStretch(1)
        self._apply_btn = QtWidgets.QPushButton("Apply", self)
        self._apply_btn.setObjectName("SimplifyApply")
        self._cancel_btn = QtWidgets.QPushButton("Cancel", self)
        btn_row.addWidget(self._apply_btn)
        btn_row.addWidget(self._cancel_btn)
        layout.addLayout(btn_row)

        self._detail_slider.valueChanged.connect(self._on_detail_changed)
        self._ratio_slider.valueChanged.connect(self._on_ratio_changed)
        self._detail_radio.toggled.connect(self._sync_mode)
        self._ratio_radio.toggled.connect(self._sync_mode)
        self._wireframe_check.toggled.connect(self.wireframeChanged.emit)
        self._apply_btn.clicked.connect(self._emit_apply)
        self._cancel_btn.clicked.connect(self.reject)

        self.apply_theme()

    def _sync_mode(self):
        detail = self._detail_radio.isChecked()
        self._detail_slider.setEnabled(detail)
        self._ratio_slider.setEnabled(not detail)
        self._ratio_display.setEnabled(not detail)
        self._apply_btn.setEnabled(self._triangles > 0)

    def _on_detail_changed(self, value: int):
        idx = max(0, min(int(value), len(DETAIL_LEVELS) - 1))
        level = DETAIL_LEVELS[idx]
        self._detail_ratio = level.ratio
        self._detail_label.setText(level.label)
        self._sync_detail_ui()

    def _sync_detail_ui(self):
        target = max(4, int(round(self._triangles * self._detail_ratio)))
        self._detail_target.setText(f"{target:,} triangles")

    def _on_ratio_changed(self, value: int):
        self._ratio_reduction = max(0.0, min(99.9, float(value) / 10.0))
        self._sync_ratio_ui()

    def _sync_ratio_ui(self):
        remaining = max(0.0, 100.0 - self._ratio_reduction)
        target = max(4, int(round(self._triangles * (remaining / 100.0))))
        self._ratio_display.setText(f"{self._ratio_reduction:.2f}%")
        self._ratio_target.setText(f"{target:,} triangles")

    def _emit_apply(self):
        target = self.target_faces()
        if target <= 0:
            return
        self.applyRequested.emit(target)
        self.accept()

    def target_faces(self) -> int:
        if self._detail_radio.isChecked():
            target = max(4, int(round(self._triangles * self._detail_ratio)))
        else:
            remaining = max(0.0, 100.0 - self._ratio_reduction)
            target = max(4, int(round(self._triangles * (remaining / 100.0))))
        return min(target, self._triangles)

    def wireframe_enabled(self) -> bool:
        return bool(self._wireframe_check.isChecked())

    def apply_theme(self):
        self.setStyleSheet(
            "QDialog {"
            f"  background: {theme_css('popup_bg')};"
            f"  color: {theme_css('popup_text')};"
            "}"
            "QLabel#SimplifyHeader {"
            "  color: #ffffff;"
            "}"
            "QLabel#SimplifyValue {"
            "  color: #ffffff;"
            "  font-weight: 600;"
            "}"
            "QLabel#SimplifyAccent {"
            f"  color: {theme_css('topbar_accent')};"
            "  font-weight: 600;"
            "}"
            "QLabel#SimplifyMuted {"
            f"  color: {theme_css('popup_muted_text')};"
            "}"
            "QSlider::groove:horizontal {"
            f"  background: {theme_css('action_panel_border')};"
            "  height: 6px;"
            "  border-radius: 3px;"
            "}"
            "QSlider::handle:horizontal {"
            f"  background: {theme_css('topbar_accent')};"
            "  width: 12px;"
            "  margin: -4px 0;"
            "  border-radius: 6px;"
            "}"
            "QLineEdit {"
            f"  background: {theme_css('popup_input_bg')};"
            f"  color: {theme_css('popup_input_text')};"
            f"  border: 1px solid {theme_css('popup_input_border')};"
            "  padding: 3px 6px;"
            "  border-radius: 4px;"
            "}"
            "QPushButton#SimplifyApply {"
            f"  background: {theme_css('topbar_accent')};"
            f"  color: {theme_css('popup_text')};"
            "  border: none;"
            "  border-radius: 6px;"
            "  padding: 6px 16px;"
            "  font-weight: 600;"
            "}"
            "QPushButton {"
            f"  background: {theme_css('action_button_bg')};"
            f"  color: {theme_css('action_button_text')};"
            f"  border: 1px solid {theme_css('action_panel_border')};"
            "  border-radius: 6px;"
            "  padding: 6px 12px;"
            "}"
        )
