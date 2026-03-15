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
                ("Organic tree", "organic"),
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
        threshold_angle_default = getattr(self._defaults, "support_threshold_angle_deg", self._defaults.overhang_angle)
        self.support_threshold_angle_deg_spin = self._make_double_spin(threshold_angle_default, 1.0, 89.0, 1.0, "deg")
        self._add_row(
            "support",
            section,
            section_layout,
            "Unsupported threshold angle",
            self.support_threshold_angle_deg_spin,
            "Angle used to allow horizontal overhang drift before support is required.",
        )

        self.support_z_gap_spin = self._make_double_spin(self._defaults.support_z_gap, 0.0, 5.0, 0.05,
                                                         "mm")
        self._add_row("support", section, section_layout, "Top Z gap", self.support_z_gap_spin,
                      "Vertical gap between support and model.")

        bottom_z_gap_default = getattr(self._defaults, "support_bottom_z_gap_mm", self._defaults.support_z_gap)
        self.support_bottom_z_gap_spin = self._make_double_spin(bottom_z_gap_default, 0.0, 5.0, 0.05,
                                                                "mm")
        self._add_row("support", section, section_layout, "Bottom Z gap",
                      self.support_bottom_z_gap_spin,
                      "Gap between support base and lower contact surface.")

        self.support_xy_gap_spin = self._make_double_spin(self._defaults.support_xy_gap, 0.0, 5.0, 0.05,
                                                          "mm")
        self._add_row("support", section, section_layout, "XY gap", self.support_xy_gap_spin,
                      "Horizontal gap between support and model.")

        base_spacing_default = getattr(self._defaults, "support_base_spacing_mm", self._defaults.support_spacing)
        self.support_spacing_spin = self._make_double_spin(base_spacing_default, 0.1, 10.0, 0.1,
                                                           "mm")
        self._add_row("support", section, section_layout, "Base spacing", self.support_spacing_spin,
                      "Spacing between support lines.")

        interface_spacing_default = getattr(self._defaults, "support_interface_spacing_mm",
                                            self._defaults.support_spacing)
        self.support_interface_spacing_spin = self._make_double_spin(interface_spacing_default, 0.1,
                                                                     10.0, 0.1, "mm")
        self._add_row("support", section, section_layout, "Interface spacing",
                      self.support_interface_spacing_spin)

        bottom_interface_spacing_default = getattr(
            self._defaults,
            "support_bottom_interface_spacing_mm",
            interface_spacing_default,
        )
        self.support_bottom_interface_spacing_spin = self._make_double_spin(
            bottom_interface_spacing_default,
            0.1,
            10.0,
            0.1,
            "mm",
        )
        self._add_row(
            "support",
            section,
            section_layout,
            "Bottom interface spacing",
            self.support_bottom_interface_spacing_spin,
        )

        threshold_overlap_default = getattr(self._defaults, "support_threshold_overlap_percent", 0.0)
        self.support_threshold_overlap_spin = self._make_double_spin(threshold_overlap_default, 0.0,
                                                                     100.0, 1.0, "%")
        self._add_row("support", section, section_layout, "Unsupported threshold overlap",
                      self.support_threshold_overlap_spin,
                      "Coverage ratio below this threshold is considered unsupported.")

        self.support_critical_regions_only_check = QtWidgets.QCheckBox(section)
        self.support_critical_regions_only_check.setObjectName("SettingsCheck")
        self.support_critical_regions_only_check.setChecked(
            bool(getattr(self._defaults, "support_critical_regions_only", False))
        )
        self._add_row(
            "support",
            section,
            section_layout,
            "Critical regions only",
            self.support_critical_regions_only_check,
            "Restrict support to severe/edge-critical unsupported areas.",
        )

        self.support_remove_small_overhang_check = QtWidgets.QCheckBox(section)
        self.support_remove_small_overhang_check.setObjectName("SettingsCheck")
        self.support_remove_small_overhang_check.setChecked(
            bool(getattr(self._defaults, "support_remove_small_overhang", False))
        )
        self._add_row(
            "support",
            section,
            section_layout,
            "Remove small overhangs",
            self.support_remove_small_overhang_check,
            "Drop tiny unsupported islands to reduce unnecessary support clutter.",
        )
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Support interface", advanced=True)
        interface_top_default = getattr(self._defaults, "support_interface_top_layers",
                                        self._defaults.interface_layers)
        self.support_interface_layers_spin = self._make_int_spin(
            interface_top_default, 0, 10, suffix="layers"
        )
        self._add_row("support", section, section_layout, "Top interface layers",
                      self.support_interface_layers_spin)
        self.support_interface_top_layers_spin = self.support_interface_layers_spin

        interface_bottom_default = getattr(self._defaults, "support_interface_bottom_layers", 0)
        self.support_interface_bottom_layers_spin = self._make_int_spin(
            interface_bottom_default,
            -1,
            10,
            suffix="layers",
        )
        self.support_interface_bottom_layers_spin.setSpecialValueText("Same as top")
        self._add_row("support", section, section_layout, "Bottom interface layers",
                      self.support_interface_bottom_layers_spin)

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
        branch_angle_default = getattr(self._defaults, "tree_support_branch_angle_deg",
                                       self._defaults.tree_branch_angle)
        self.tree_branch_angle_spin = self._make_double_spin(branch_angle_default, 0.0, 85.0,
                                                             1.0, "deg")
        self._add_row("support", section, section_layout, "Branch angle",
                      self.tree_branch_angle_spin)

        tree_wall_count_default = getattr(self._defaults, "tree_support_wall_count", 1)
        self.tree_support_wall_count_spin = self._make_int_spin(tree_wall_count_default, 0, 8)
        self._add_row("support", section, section_layout, "Wall count",
                      self.tree_support_wall_count_spin)

        branch_diameter_default = getattr(self._defaults, "tree_support_branch_diameter_mm", 0.6)
        self.tree_support_branch_diameter_spin = self._make_double_spin(branch_diameter_default,
                                                                        0.05, 10.0, 0.05, "mm")
        self._add_row("support", section, section_layout, "Branch diameter",
                      self.tree_support_branch_diameter_spin)

        tip_diameter_default = getattr(self._defaults, "tree_support_tip_diameter_mm", 0.3)
        self.tree_support_tip_diameter_spin = self._make_double_spin(tip_diameter_default,
                                                                     0.05, 10.0, 0.05, "mm")
        self._add_row("support", section, section_layout, "Tip diameter",
                      self.tree_support_tip_diameter_spin)

        tree_branch_distance_default = getattr(self._defaults, "tree_support_branch_distance_mm", 2.0)
        self.tree_support_branch_distance_spin = self._make_double_spin(
            tree_branch_distance_default,
            0.05,
            20.0,
            0.05,
            "mm",
        )
        self._add_row(
            "support",
            section,
            section_layout,
            "Branch distance",
            self.tree_support_branch_distance_spin,
        )

        tree_top_rate_default = getattr(self._defaults, "tree_support_top_rate_percent", 30.0)
        self.tree_support_top_rate_spin = self._make_double_spin(tree_top_rate_default, 0.0, 100.0, 1.0, "%")
        self._add_row("support", section, section_layout, "Top rate", self.tree_support_top_rate_spin)

        tree_branch_diameter_angle_default = getattr(self._defaults, "tree_support_branch_diameter_angle_deg", 5.0)
        self.tree_support_branch_diameter_angle_spin = self._make_double_spin(
            tree_branch_diameter_angle_default,
            0.0,
            89.0,
            1.0,
            "deg",
        )
        self._add_row(
            "support",
            section,
            section_layout,
            "Branch diameter angle",
            self.tree_support_branch_diameter_angle_spin,
        )

        tree_branch_angle_organic_default = getattr(self._defaults, "tree_support_branch_angle_organic_deg", 35.0)
        self.tree_support_branch_angle_organic_spin = self._make_double_spin(
            tree_branch_angle_organic_default,
            0.0,
            85.0,
            1.0,
            "deg",
        )
        self._add_row(
            "support",
            section,
            section_layout,
            "Organic angle",
            self.tree_support_branch_angle_organic_spin,
        )

        tree_branch_diameter_organic_default = getattr(self._defaults, "tree_support_branch_diameter_organic_mm", 0.7)
        self.tree_support_branch_diameter_organic_spin = self._make_double_spin(
            tree_branch_diameter_organic_default,
            0.05,
            10.0,
            0.05,
            "mm",
        )
        self._add_row(
            "support",
            section,
            section_layout,
            "Organic diameter",
            self.tree_support_branch_diameter_organic_spin,
        )

        tree_branch_distance_organic_default = getattr(self._defaults, "tree_support_branch_distance_organic_mm", 2.5)
        self.tree_support_branch_distance_organic_spin = self._make_double_spin(
            tree_branch_distance_organic_default,
            0.05,
            20.0,
            0.05,
            "mm",
        )
        self._add_row(
            "support",
            section,
            section_layout,
            "Organic distance",
            self.tree_support_branch_distance_organic_spin,
        )

        self.tree_support_auto_brim_check = QtWidgets.QCheckBox(section)
        self.tree_support_auto_brim_check.setObjectName("SettingsCheck")
        self.tree_support_auto_brim_check.setChecked(bool(getattr(self._defaults, "tree_support_auto_brim", False)))
        self._add_row("support", section, section_layout, "Auto brim",
                      self.tree_support_auto_brim_check)

        tree_brim_width_default = getattr(self._defaults, "tree_support_brim_width_mm", 0.0)
        self.tree_support_brim_width_spin = self._make_double_spin(tree_brim_width_default,
                                                                   0.0, 20.0, 0.1, "mm")
        self._add_row("support", section, section_layout, "Brim width",
                      self.tree_support_brim_width_spin)

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
        support_style = str(self.support_style_combo.currentData() or "").strip().lower()
        if support_type == "tree":
            if support_style not in {"tree", "organic"}:
                block = self.support_style_combo.blockSignals(True)
                self._set_combo_value(self.support_style_combo, "tree")
                self.support_style_combo.blockSignals(block)
        elif support_style in {"tree", "organic"}:
            block = self.support_style_combo.blockSignals(True)
            self._set_combo_value(self.support_style_combo, "pillars")
            self.support_style_combo.blockSignals(block)
        self._update_support_controls(self.support_enable_check.isChecked())

