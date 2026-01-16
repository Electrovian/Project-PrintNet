from __future__ import annotations

from typing import Any, TYPE_CHECKING

from PyQt5 import QtCore, QtGui, QtWidgets


class SupportSectionMixin:
    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any: ...

    def _build_support_page(self):
        layout = self._build_page("support")

        section, section_layout = self._section("Support")
        self.support_enable_check = QtWidgets.QCheckBox(section)
        self.support_enable_check.setObjectName("SettingsCheck")
        self.support_enable_check.setChecked(bool(self._defaults.support_enabled))
        self._add_row("support", section, section_layout, "Enable support", self.support_enable_check,
                      "Generate support structures.")

        self.support_type_combo = self._make_combo(
            [
                ("Normal (auto)", "normal"),
                ("Tree", "tree"),
            ]
        )
        self._set_combo_value(self.support_type_combo, self._defaults.support_type)
        self._add_row("support", section, section_layout, "Type", self.support_type_combo)

        self.support_style_combo = self._make_combo(
            [
                ("Default", "pillars"),
                ("Pillars", "pillars"),
                ("Tree", "tree"),
            ]
        )
        self._set_combo_value(self.support_style_combo, self._defaults.support_style)
        self._add_row("support", section, section_layout, "Style", self.support_style_combo)

        self.support_angle_spin = self._make_double_spin(self._defaults.overhang_angle, 0, 90, 1, "deg")
        self._add_row("support", section, section_layout, "Threshold angle", self.support_angle_spin,
                      "Overhang angle that triggers support.")

        self.support_build_plate_check = QtWidgets.QCheckBox(section)
        self.support_build_plate_check.setObjectName("SettingsCheck")
        self.support_build_plate_check.setChecked(bool(self._defaults.support_build_plate_only))
        self._add_row("support", section, section_layout, "On build plate only",
                      self.support_build_plate_check)
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Filament for supports")
        self.support_base_combo = self._make_combo(
            [
                ("Default", "default"),
                ("Support", "support"),
            ]
        )
        self._set_combo_value(self.support_base_combo, self._defaults.support_filament_base)
        self._add_row("support", section, section_layout, "Support/raft base", self.support_base_combo)

        self.support_interface_combo = self._make_combo(
            [
                ("Default", "default"),
                ("Support", "support"),
            ]
        )
        self._set_combo_value(self.support_interface_combo, self._defaults.support_filament_interface)
        self._add_row("support", section, section_layout, "Support/raft interface",
                      self.support_interface_combo)
        layout.insertWidget(layout.count() - 1, section)

        self.support_enable_check.toggled.connect(self._update_support_controls)
        self._update_support_controls(self.support_enable_check.isChecked())

