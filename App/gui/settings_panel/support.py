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

        section, section_layout = self._section("Spacing & gaps", advanced=True)
        self.support_z_gap_spin = self._make_double_spin(self._defaults.support_z_gap, 0.0, 5.0, 0.05,
                                                         "mm")
        self._add_row("support", section, section_layout, "Top Z gap", self.support_z_gap_spin,
                      "Vertical gap between support and model.")

        self.support_xy_gap_spin = self._make_double_spin(self._defaults.support_xy_gap, 0.0, 5.0, 0.05,
                                                          "mm")
        self._add_row("support", section, section_layout, "XY gap", self.support_xy_gap_spin,
                      "Horizontal gap between support and model.")

        self.support_spacing_spin = self._make_double_spin(self._defaults.support_spacing, 0.1, 10.0, 0.1,
                                                           "mm")
        self._add_row("support", section, section_layout, "Support spacing", self.support_spacing_spin,
                      "Spacing between support lines.")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Support interface", advanced=True)
        self.support_interface_layers_spin = self._make_int_spin(
            self._defaults.interface_layers, 0, 10, suffix="layers"
        )
        self._add_row("support", section, section_layout, "Interface layers",
                      self.support_interface_layers_spin)

        interface_density = max(0.0, min(1.0, float(self._defaults.interface_density))) * 100.0
        self.support_interface_density_spin = self._make_double_spin(
            interface_density, 0.0, 100.0, 1.0, "%"
        )
        self._add_row("support", section, section_layout, "Interface density",
                      self.support_interface_density_spin)

        self.support_pattern_combo = self._make_combo(
            [
                ("Rectilinear", "rectilinear"),
                ("Grid", "grid"),
                ("Triangle", "triangle"),
            ]
        )
        self._set_combo_value(self.support_pattern_combo, self._defaults.support_pattern)
        self._add_row("support", section, section_layout, "Base pattern", self.support_pattern_combo)

        self.support_interface_pattern_combo = self._make_combo(
            [
                ("Rectilinear", "rectilinear"),
                ("Grid", "grid"),
                ("Triangle", "triangle"),
            ]
        )
        self._set_combo_value(self.support_interface_pattern_combo,
                              self._defaults.support_interface_pattern)
        self._add_row("support", section, section_layout, "Interface pattern",
                      self.support_interface_pattern_combo)
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Support speeds", advanced=True)
        self.support_speed_spin = self._make_double_spin(self._defaults.support_speed, 5.0, 200.0, 1.0,
                                                         "mm/s")
        self._add_row("support", section, section_layout, "Support speed", self.support_speed_spin)

        self.support_interface_speed_spin = self._make_double_spin(
            self._defaults.support_interface_speed, 5.0, 200.0, 1.0, "mm/s"
        )
        self._add_row("support", section, section_layout, "Interface speed",
                      self.support_interface_speed_spin)
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Tree supports", advanced=True)
        self.tree_branch_angle_spin = self._make_double_spin(self._defaults.tree_branch_angle, 0.0, 85.0,
                                                             1.0, "deg")
        self._add_row("support", section, section_layout, "Branch angle",
                      self.tree_branch_angle_spin)

        self.tree_merge_distance_spin = self._make_double_spin(self._defaults.tree_merge_distance, 0.1,
                                                               10.0, 0.1, "mm")
        self._add_row("support", section, section_layout, "Merge distance",
                      self.tree_merge_distance_spin)
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
        self.support_type_combo.currentIndexChanged.connect(self._on_support_mode_changed)
        self.support_style_combo.currentIndexChanged.connect(self._on_support_mode_changed)
        self._on_support_mode_changed()
        self._update_support_controls(self.support_enable_check.isChecked())

    def _on_support_mode_changed(self):
        support_type = str(self.support_type_combo.currentData() or "").strip().lower()
        if not support_type:
            support_type = "normal"
        if support_type == "tree":
            block = self.support_style_combo.blockSignals(True)
            self._set_combo_value(self.support_style_combo, "tree")
            self.support_style_combo.blockSignals(block)
        elif str(self.support_style_combo.currentData() or "").strip().lower() == "tree":
            block = self.support_style_combo.blockSignals(True)
            self._set_combo_value(self.support_style_combo, "pillars")
            self.support_style_combo.blockSignals(block)
        self._update_support_controls(self.support_enable_check.isChecked())

