from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PyQt5 import QtCore, QtGui, QtWidgets


class MultifilamentSectionMixin:
    if TYPE_CHECKING:
        _defaults: Any
        prime_tower_enable_check: QtWidgets.QCheckBox

        def _build_page(self, key: str) -> QtWidgets.QVBoxLayout: ...
        def _section(self, title: str) -> tuple[QtWidgets.QFrame, QtWidgets.QVBoxLayout]: ...
        def _add_row(
            self,
            page_key: str,
            section: QtWidgets.QFrame,
            layout: QtWidgets.QVBoxLayout,
            label_text: str,
            control: QtWidgets.QWidget,
            tooltip: str | None = None,
            use_native_tooltip: bool = True,
            advanced: bool | None = None,
        ) -> QtWidgets.QLabel: ...
        def _make_double_spin(self, value: float, minimum: float, maximum: float,
                              step: float, suffix: str = "") -> QtWidgets.QDoubleSpinBox: ...
        def _update_prime_controls(self, enabled: bool) -> None: ...
    def _build_multifilament_page(self):
        layout = self._build_page("multifilament")

        section, section_layout = self._section("Prime tower")
        self.prime_tower_enable_check = QtWidgets.QCheckBox(section)
        self.prime_tower_enable_check.setObjectName("SettingsCheck")
        self.prime_tower_enable_check.setChecked(bool(self._defaults.prime_tower_enabled))
        self._add_row("multifilament", section, section_layout, "Enable", self.prime_tower_enable_check)

        self.prime_tower_width_spin = self._make_double_spin(
            self._defaults.prime_tower_width, 5.0, 100.0, 1.0, "mm"
        )
        self._add_row("multifilament", section, section_layout, "Width", self.prime_tower_width_spin)

        self.prime_tower_square_check = QtWidgets.QCheckBox(section)
        self.prime_tower_square_check.setObjectName("SettingsCheck")
        self.prime_tower_square_check.setChecked(bool(self._defaults.prime_tower_square))
        self._add_row("multifilament", section, section_layout, "Square prime tower",
                      self.prime_tower_square_check)

        self.prime_tower_volume_spin = self._make_double_spin(
            self._defaults.prime_tower_volume, 1.0, 200.0, 1.0, "mm3"
        )
        self._add_row("multifilament", section, section_layout, "Prime volume",
                      self.prime_tower_volume_spin)
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Flush options")
        self.flush_into_infill_check = QtWidgets.QCheckBox(section)
        self.flush_into_infill_check.setObjectName("SettingsCheck")
        self.flush_into_infill_check.setChecked(bool(self._defaults.flush_into_infill))
        self._add_row("multifilament", section, section_layout, "Flush into objects' infill",
                      self.flush_into_infill_check)

        self.flush_into_support_check = QtWidgets.QCheckBox(section)
        self.flush_into_support_check.setObjectName("SettingsCheck")
        self.flush_into_support_check.setChecked(bool(self._defaults.flush_into_support))
        self._add_row("multifilament", section, section_layout, "Flush into objects' support",
                      self.flush_into_support_check)
        layout.insertWidget(layout.count() - 1, section)

        self.prime_tower_enable_check.toggled.connect(self._update_prime_controls)
        self._update_prime_controls(self.prime_tower_enable_check.isChecked())

