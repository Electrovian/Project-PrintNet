from __future__ import annotations

from typing import Any, Mapping

from PyQt5 import QtCore, QtWidgets

from .i18n import tr


_LANGUAGE_ITEMS: tuple[tuple[str, str], ...] = (
    ("en", "English"),
    ("es", "Espanol"),
)

_REGION_ITEMS: tuple[str, ...] = (
    "",
    "US",
    "US-CA",
    "US-NY",
    "US-TX",
    "US-FL",
)


class BootstrapSetupDialog(QtWidgets.QDialog):
    def __init__(self, *, initial: Mapping[str, Any] | None = None, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle(tr("setup.title", "Initial Setup"))
        self.setMinimumWidth(420)
        self._result_config: dict[str, Any] = {}
        self._initial = dict(initial or {})
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        intro = QtWidgets.QLabel(tr("setup.intro", "Configure language and region before using cloud features."), self)
        intro.setWordWrap(True)
        layout.addWidget(intro)

        form = QtWidgets.QFormLayout()
        form.setLabelAlignment(QtCore.Qt.AlignLeft)
        form.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(10)

        self._language_combo = QtWidgets.QComboBox(self)
        for code, label in _LANGUAGE_ITEMS:
            self._language_combo.addItem(label, code)
        requested_lang = str(self._initial.get("ui_language", "en")).strip().lower() or "en"
        for index in range(self._language_combo.count()):
            if str(self._language_combo.itemData(index) or "").strip().lower() == requested_lang:
                self._language_combo.setCurrentIndex(index)
                break
        form.addRow(tr("setup.language", "Language"), self._language_combo)

        self._region_combo = QtWidgets.QComboBox(self)
        self._region_combo.setEditable(True)
        for item in _REGION_ITEMS:
            label = item if item else tr("setup.region_unknown", "Unknown")
            self._region_combo.addItem(label, item)
        requested_region = str(self._initial.get("region_code", "")).strip().upper()
        if requested_region:
            self._region_combo.setEditText(requested_region)
        form.addRow(tr("setup.region", "Region"), self._region_combo)

        prefs = self._initial.get("connectivity_preferences", {})
        if not isinstance(prefs, Mapping):
            prefs = {}
        self._wifi_checkbox = QtWidgets.QCheckBox(tr("setup.connectivity.wifi", "Enable Wi-Fi onboarding"), self)
        self._wifi_checkbox.setChecked(bool(prefs.get("wifi_enabled", True)))
        self._bluetooth_checkbox = QtWidgets.QCheckBox(
            tr("setup.connectivity.bluetooth", "Enable Bluetooth pairing"),
            self,
        )
        self._bluetooth_checkbox.setChecked(bool(prefs.get("bluetooth_enabled", True)))
        form.addRow("", self._wifi_checkbox)
        form.addRow("", self._bluetooth_checkbox)

        layout.addLayout(form)

        buttons = QtWidgets.QDialogButtonBox(self)
        self._cancel_btn = buttons.addButton(tr("setup.cancel", "Exit"), QtWidgets.QDialogButtonBox.RejectRole)
        self._ok_btn = buttons.addButton(tr("setup.continue", "Continue"), QtWidgets.QDialogButtonBox.AcceptRole)
        self._ok_btn.setDefault(True)
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _on_accept(self) -> None:
        language = str(self._language_combo.currentData() or "en").strip().lower() or "en"
        region = str(self._region_combo.currentText() or "").strip().upper()
        if region == tr("setup.region_unknown", "Unknown").upper():
            region = ""
        self._result_config = {
            "ui_language": language,
            "region_code": region,
            "connectivity_preferences": {
                "wifi_enabled": bool(self._wifi_checkbox.isChecked()),
                "bluetooth_enabled": bool(self._bluetooth_checkbox.isChecked()),
            },
        }
        self.accept()

    def result_config(self) -> dict[str, Any]:
        return dict(self._result_config)

