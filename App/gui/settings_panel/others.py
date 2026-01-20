from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, TYPE_CHECKING, cast

from PyQt5 import QtCore, QtGui, QtWidgets

from config.defaults import DEFAULTS
from slicer.gcode.writer import SliceSettings
from ..theme import theme_css

if TYPE_CHECKING:
    from ..main_window import MainWindow
else:
    MainWindow = QtWidgets.QWidget


class OtherSectionMixin:
    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any: ...

    def _build_other_page(self):
        layout = self._build_page("others")

        section, section_layout = self._section("Skirt")
        self.skirt_loops_spin = self._make_int_spin(self._defaults.skirt_loops, 0, 10, suffix="loops")
        self._add_row("others", section, section_layout, "Skirt loops", self.skirt_loops_spin)

        self.skirt_height_spin = self._make_int_spin(self._defaults.skirt_height, 0, 20, suffix="layers")
        self._add_row("others", section, section_layout, "Skirt height", self.skirt_height_spin)
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Brim")
        self.brim_type_combo = self._make_combo(
            [
                ("Auto", "auto"),
                ("Outer", "outer"),
                ("Inner", "inner"),
                ("Both", "both"),
            ]
        )
        self._set_combo_value(self.brim_type_combo, self._defaults.brim_type)
        self._add_row("others", section, section_layout, "Brim type", self.brim_type_combo)
        self.brim_width_spin = self._make_double_spin(self._defaults.brim_width, 0.0, 50.0, 0.5, "mm")
        self._add_row("others", section, section_layout, "Brim width", self.brim_width_spin)
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Special mode")
        self.print_sequence_combo = self._make_combo(
            [
                ("By layer", "by_layer"),
                ("By object", "by_object"),
            ]
        )
        self._set_combo_value(self.print_sequence_combo, self._defaults.print_sequence)
        self._add_row("others", section, section_layout, "Print sequence", self.print_sequence_combo)

        self.spiral_vase_check = QtWidgets.QCheckBox(section)
        self.spiral_vase_check.setObjectName("SettingsCheck")
        self.spiral_vase_check.setChecked(bool(self._defaults.spiral_vase))
        self._add_row("others", section, section_layout, "Spiral vase", self.spiral_vase_check)

        self.ignore_inner_color_check = QtWidgets.QCheckBox(section)
        self.ignore_inner_color_check.setObjectName("SettingsCheck")
        self.ignore_inner_color_check.setChecked(bool(self._defaults.ignore_inner_color))
        self._add_row("others", section, section_layout, "Ignore inner color", self.ignore_inner_color_check)

        self.timelapse_combo = self._make_combo(
            [
                ("Traditional", "traditional"),
                ("Smooth", "smooth"),
            ]
        )
        self._set_combo_value(self.timelapse_combo, self._defaults.timelapse_mode)
        self._add_row("others", section, section_layout, "Timelapse", self.timelapse_combo)

        self.fuzzy_skin_combo = self._make_combo(
            [
                ("None", "none"),
                ("Light", "light"),
                ("Normal", "normal"),
                ("Heavy", "heavy"),
            ]
        )
        self._set_combo_value(self.fuzzy_skin_combo, self._defaults.fuzzy_skin)
        self._add_row("others", section, section_layout, "Fuzzy skin", self.fuzzy_skin_combo)
        layout.insertWidget(layout.count() - 1, section)

    def _choose_filament_color(self):
        color = QtWidgets.QColorDialog.getColor(
            self._filament_color, cast(QtWidgets.QWidget, self)
        )
        if color.isValid():
            self._filament_color = color
            self._update_filament_button_style()

    def set_printers(self, printers):
        self._printers = list(printers or [])
        if not hasattr(self, "_printer_combo"):
            return
        self._printer_combo.clear()
        if not self._printers:
            self._printer_combo.addItem("No printers configured")
            self._printer_combo.setEnabled(False)
            return
        self._printer_combo.setEnabled(True)
        default_name = str(DEFAULTS.get("printer", {}).get("name", "")).strip().lower()
        default_index = None
        for idx, printer in enumerate(self._printers):
            name = printer.get("name") if isinstance(printer, dict) else None
            self._printer_combo.addItem(name or "Printer")
            if default_name and str(name or "").strip().lower() == default_name:
                default_index = idx
        if default_index is not None:
            self._printer_combo.setCurrentIndex(default_index)
        self._on_printer_changed(self._printer_combo.currentIndex())

    def current_printer(self):
        if not getattr(self, "_printers", None):
            return None
        idx = self._printer_combo.currentIndex()
        if idx < 0 or idx >= len(self._printers):
            return None
        return self._printers[idx]

    def select_printer_by_name(self, name: str, emit: bool = True):
        if not hasattr(self, "_printer_combo"):
            return
        target = str(name or "").strip().lower()
        if not target:
            return
        idx = None
        for row in range(self._printer_combo.count()):
            if self._printer_combo.itemText(row).strip().lower() == target:
                idx = row
                break
        if idx is None:
            return
        block = self._printer_combo.blockSignals(True)
        self._printer_combo.setCurrentIndex(idx)
        self._printer_combo.blockSignals(block)
        if emit:
            self._on_printer_changed(idx)

    def _on_printer_changed(self, _index: int):
        printer = self.current_printer()
        if printer is None:
            return
        main = cast(MainWindow, self.parent())
        apply_printer = getattr(main, "_apply_printer_profile", None)
        if callable(apply_printer):
            apply_printer(printer, source="settings")

    def _on_filament_type_selected(self, name: str):
        name = (name or "").strip()
        if name:
            self._filament_button.setText(name)

    def _update_filament_button_style(self):
        accent = self._filament_color.name()
        self._filament_button.setStyleSheet(
            "QToolButton#FilamentButton {"
            f"  background: {accent};"
            "  color: #000000;"
            "  border-radius: 6px;"
            "  padding: 6px 8px;"
            "}"
        )
        if getattr(self, "_filament_color_button", None) is not None:
            self._filament_color_button.setStyleSheet(
                "QToolButton#FilamentColorButton {"
                f"  background: {accent};"
                "  border-radius: 6px;"
                "  border: 1px solid #1d1f23;"
                "}"
            )

    def _update_support_controls(self, enabled: bool):
        enabled = bool(enabled)
        support_type = ""
        support_style = ""
        if hasattr(self, "support_type_combo"):
            support_type = str(self.support_type_combo.currentData() or "").strip().lower()
        if hasattr(self, "support_style_combo"):
            support_style = str(self.support_style_combo.currentData() or "").strip().lower()
        tree_mode = enabled and (support_type == "tree" or support_style == "tree")

        for control in (
            self.support_type_combo,
            self.support_style_combo,
            self.support_angle_spin,
            self.support_build_plate_check,
            self.support_z_gap_spin,
            self.support_xy_gap_spin,
            self.support_spacing_spin,
            self.support_interface_layers_spin,
            self.support_interface_density_spin,
            self.support_pattern_combo,
            self.support_interface_pattern_combo,
            self.support_speed_spin,
            self.support_interface_speed_spin,
            self.support_base_combo,
            self.support_interface_combo,
        ):
            control.setEnabled(enabled)

        self.support_style_combo.setEnabled(enabled and support_type != "tree")
        for control in (
            self.tree_branch_angle_spin,
            self.tree_merge_distance_spin,
        ):
            control.setEnabled(tree_mode)

    def _update_prime_controls(self, enabled: bool):
        for control in (
            self.prime_tower_width_spin,
            self.prime_tower_square_check,
            self.prime_tower_volume_spin,
            self.flush_into_infill_check,
            self.flush_into_support_check,
        ):
            control.setEnabled(bool(enabled))

    def _on_nav_changed(self, button):
        idx = self._nav_group.id(button)
        if idx < 0:
            return
        self._pages_stack.setCurrentIndex(idx)
        self._apply_search_filter(self._search_input.text())

    def _on_advanced_toggled(self, _checked: bool):
        self._apply_search_filter(self._search_input.text())

    def _apply_search_filter(self, text: str):
        query = (text or "").strip().lower()
        page_index = int(self._pages_stack.currentIndex())
        if page_index < 0 or page_index >= len(self._page_keys):
            return
        key = self._page_keys[page_index]
        rows = self._search_rows.get(key, [])
        show_advanced = True
        if hasattr(self, "_advanced_toggle"):
            show_advanced = bool(self._advanced_toggle.isChecked())
        section_visible: Dict[QtWidgets.QFrame, bool] = {}
        for section, row, label in rows:
            is_advanced = row in self._advanced_rows
            if not show_advanced and is_advanced:
                match = False
            elif not query:
                match = True
            else:
                match = query in label
            row.setVisible(match)
            section_visible[section] = section_visible.get(section, False) or match
        for section, visible in section_visible.items():
            section.setVisible(visible)

    def _set_combo_value(self, combo: QtWidgets.QComboBox, value: str | None):
        if value is None:
            return
        value = str(value).strip().lower()
        for idx in range(combo.count()):
            data = combo.itemData(idx)
            if data is None:
                continue
            if str(data).strip().lower() == value:
                combo.setCurrentIndex(idx)
                return

    def _combo_value(self, combo: QtWidgets.QComboBox, default: str) -> str:
        data = combo.currentData()
        if data is None:
            text = combo.currentText().strip().lower().replace(" ", "_")
            return text or default
        return str(data).strip().lower() or default

    def apply_theme(self):
        panel_bg = theme_css("popup_bg")
        panel_border = theme_css("popup_border")
        panel_text = theme_css("popup_text")
        muted_text = theme_css("popup_muted_text")
        accent = theme_css("topbar_accent")
        input_bg = theme_css("popup_input_bg")
        button_hover = theme_css("action_button_hover_bg")

        self.setStyleSheet(
            "QWidget#SettingsPanel {"
            f"  background: {panel_bg};"
            "}"
            "QStackedWidget#SettingsPages {"
            f"  background: {panel_bg};"
            "}"
            "QScrollArea#SettingsScroll {"
            f"  background: {panel_bg};"
            "  border: none;"
            "}"
            "QScrollArea#SettingsScroll QWidget#qt_scrollarea_viewport {"
            f"  background: {panel_bg};"
            "}"
            "QWidget#SettingsPage {"
            f"  background: {panel_bg};"
            "}"
            "QFrame#SettingsHeader {"
            f"  background: {panel_bg};"
            "}"
            "QLabel#SettingsHeaderTitle {"
            f"  color: {panel_text};"
            "  font-weight: 600;"
            "  font-size: 13px;"
            "}"
            "QToolButton#SettingsHeaderButton {"
            f"  color: {muted_text};"
            f"  background: {panel_bg};"
            "  border: none;"
            "  padding: 2px 6px;"
            "}"
            "QLabel#FilamentSlot {"
            f"  color: {panel_text};"
            "  padding: 4px 6px;"
            "}"
            "QToolButton#FilamentButton {"
            "  border: none;"
            "}"
            "QToolButton#FilamentColorButton {"
            "  border: none;"
            "}"
            "QFrame#ProcessRow, QFrame#ProfileRow, QFrame#PrinterRow {"
            f"  background: {panel_bg};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 8px;"
            "}"
            "QLabel#PrinterLabel {"
            f"  color: {panel_text};"
            "  font-weight: 600;"
            "}"
            "QLabel#ProcessLabel {"
            f"  color: {panel_text};"
            "  font-weight: 600;"
            "}"
            "QLabel#AdvancedLabel {"
            f"  color: {panel_text};"
            "  font-weight: 600;"
            "}"
            "QToolButton#SettingsChip {"
            f"  background: {input_bg};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 10px;"
            "  padding: 3px 10px;"
            "}"
            "QToolButton#SettingsChip:checked {"
            f"  background: {accent};"
            "  color: #ffffff;"
            "  font-weight: 600;"
            "}"
            "QCheckBox#SettingsToggle::indicator {"
            "  width: 36px;"
            "  height: 18px;"
            "}"
            "QCheckBox#SettingsToggle::indicator:unchecked {"
            f"  background: {input_bg};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 9px;"
            "}"
            "QCheckBox#SettingsToggle::indicator:checked {"
            f"  background: {accent};"
            "  border-radius: 9px;"
            "}"
            "QComboBox#ProfileCombo, QComboBox#PrinterCombo, QLineEdit#SettingsSearch {"
            f"  background: {input_bg};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 6px;"
            "  padding: 3px 6px;"
            "}"
            "QToolButton#ProfileButton {"
            f"  background: {input_bg};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 6px;"
            "  padding: 2px 8px;"
            "}"
            "QFrame#SettingsNav {"
            f"  background: {panel_bg};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 8px;"
            "}"
            "QToolButton#SettingsNavButton {"
            f"  color: {panel_text};"
            "  padding: 6px 6px;"
            "  border-radius: 6px;"
            "}"
            "QToolButton#SettingsNavButton:checked {"
            f"  background: {accent};"
            "  color: #ffffff;"
            "  font-weight: 600;"
            "}"
            "QFrame#SettingsSection {"
            f"  background: {panel_bg};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 8px;"
            "}"
            "QLabel#SettingsSectionTitle {"
            f"  color: {panel_text};"
            "  font-weight: 600;"
            "}"
            "QFrame#SettingsSectionLine {"
            f"  color: {panel_border};"
            "}"
            "QLabel#SettingsLabel {"
            f"  color: {panel_text};"
            "}"
            "QComboBox#SettingsCombo, QSpinBox#SettingsSpin, QDoubleSpinBox#SettingsSpin {"
            f"  background: {input_bg};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 6px;"
            "  padding: 2px 6px;"
            "}"
            "QCheckBox#SettingsCheck::indicator {"
            "  width: 18px;"
            "  height: 18px;"
            "}"
            "QCheckBox#SettingsCheck::indicator:unchecked {"
            f"  border: 1px solid {panel_border};"
            f"  background: {input_bg};"
            "  border-radius: 3px;"
            "}"
            "QCheckBox#SettingsCheck::indicator:checked {"
            f"  background: {accent};"
            "  border-radius: 3px;"
            "}"
            "QWidget#ObjectsPanel {"
            f"  background: {panel_bg};"
            "}"
            "QListWidget#ObjectsList {"
            f"  background: {input_bg};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 6px;"
            "}"
            "QListWidget#ObjectsList::item:selected {"
            f"  background: {accent};"
            "  color: #ffffff;"
            "}"
            "QPushButton#ObjectsButton {"
            f"  background: {input_bg};"
            f"  color: {panel_text};"
            f"  border: 1px solid {panel_border};"
            "  border-radius: 6px;"
            "  padding: 4px 10px;"
            "}"
            "QPushButton#ObjectsButton:hover {"
            f"  background: {button_hover};"
            "}"
        )
        self._update_filament_button_style()
        self._tooltip.apply_theme(panel_bg, panel_border, panel_text, muted_text)

    def to_settings(self) -> SliceSettings:
        return SliceSettings(
            layer_height=float(self.layer_height_spin.value()),
            first_layer_height=float(self.first_layer_height_spin.value()),
            seam_position=self._combo_value(self.seam_position_combo, "aligned"),
            staggered_inner_seams=bool(self.staggered_inner_seams_check.isChecked()),
            seam_gap=float(self.seam_gap_spin.value()),
            scarf_joint_seam=self._combo_value(self.scarf_joint_seam_combo, "none"),
            wipe_use_base_speed=bool(self.wipe_use_base_speed_check.isChecked()),
            wipe_speed_percent=float(self.wipe_speed_spin.value()),
            wipe_on_loops=bool(self.wipe_on_loops_check.isChecked()),
            wipe_before_external_loop=bool(self.wipe_before_external_loop_check.isChecked()),
            precise_wall=bool(self.precise_wall_check.isChecked()),
            slice_gap_closing_radius=float(self.slice_gap_closing_radius_spin.value()),
            resolution=float(self.resolution_spin.value()),
            arc_fitting=bool(self.arc_fitting_check.isChecked()),
            xy_hole_compensation=float(self.xy_hole_compensation_spin.value()),
            xy_contour_compensation=float(self.xy_contour_compensation_spin.value()),
            elephant_foot_compensation=float(self.elephant_foot_compensation_spin.value()),
            elephant_foot_compensation_layers=int(self.elephant_foot_layers_spin.value()),
            convert_holes_to_polyholes=bool(self.convert_holes_to_polyholes_check.isChecked()),
            precise_z_height=bool(self.precise_z_height_check.isChecked()),
            only_one_wall_top=bool(self.only_one_wall_top_check.isChecked()),
            only_one_wall_first_layer=bool(self.only_one_wall_first_layer_check.isChecked()),
            extrusion_width=float(self.line_width_default_spin.value()),
            first_layer_line_width=float(self.line_width_first_layer_spin.value()),
            outer_wall_line_width=float(self.line_width_outer_wall_spin.value()),
            inner_wall_line_width=float(self.line_width_inner_wall_spin.value()),
            top_surface_line_width=float(self.line_width_top_surface_spin.value()),
            sparse_infill_line_width=float(self.line_width_sparse_infill_spin.value()),
            internal_solid_infill_line_width=float(self.line_width_internal_solid_spin.value()),
            support_line_width=float(self.line_width_support_spin.value()),
            ironing_type=self._combo_value(self.ironing_type_combo, "no_ironing"),
            wall_generator=self._combo_value(self.wall_generator_combo, "classic"),
            wall_transition_angle=float(self.wall_transition_angle_spin.value()),
            wall_transition_filter_margin=float(self.wall_transition_filter_margin_spin.value()),
            wall_transition_length=float(self.wall_transition_length_spin.value()),
            wall_distribution_count=int(self.wall_distribution_count_spin.value()),
            first_layer_min_wall_width=float(self.first_layer_min_wall_width_spin.value()),
            min_wall_width=float(self.min_wall_width_spin.value()),
            min_feature_size=float(self.min_feature_size_spin.value()),
            min_wall_length=float(self.min_wall_length_spin.value()),
            wall_printing_order=self._combo_value(self.wall_printing_order_combo, "inner_outer"),
            print_infill_first=bool(self.print_infill_first_check.isChecked()),
            wall_loop_direction=self._combo_value(self.wall_loop_direction_combo, "auto"),
            top_surface_flow_ratio=float(self.top_surface_flow_ratio_spin.value()),
            bottom_surface_flow_ratio=float(self.bottom_surface_flow_ratio_spin.value()),
            one_wall_threshold=float(self.one_wall_threshold_spin.value()),
            avoid_crossing_walls=bool(self.avoid_crossing_walls_check.isChecked()),
            small_area_flow_compensation=bool(self.small_area_flow_compensation_check.isChecked()),
            smooth_wall_speed_z=bool(self.smooth_wall_speed_z_check.isChecked()),
            bridge_flow_ratio=float(self.bridge_flow_ratio_spin.value()),
            internal_bridge_flow_ratio=float(self.internal_bridge_flow_ratio_spin.value()),
            bridge_density=float(self.bridge_density_spin.value()),
            thick_bridges=bool(self.thick_bridges_check.isChecked()),
            thick_internal_bridges=bool(self.thick_internal_bridges_check.isChecked()),
            bridge_filter_mode=self._combo_value(self.bridge_filter_mode_combo, "disabled"),
            bridge_counterbore_holes=self._combo_value(self.bridge_counterbore_combo, "none"),
            detect_overhang_walls=bool(self.detect_overhang_walls_check.isChecked()),
            make_overhangs_printable=bool(self.make_overhangs_printable_check.isChecked()),
            extra_perimeters_on_overhangs=bool(self.extra_perimeters_on_overhangs_check.isChecked()),
            reverse_overhang_on_odd=bool(self.reverse_overhang_on_odd_check.isChecked()),
            overhang_optimization=bool(self.overhang_optimization_check.isChecked()),
            perimeter_count=int(self.wall_loops_spin.value()),
            top_layers=int(self.top_shell_layers_spin.value()),
            bottom_layers=int(self.bottom_shell_layers_spin.value()),
            infill_percent=float(self.infill_density_spin.value()),
            infill_pattern=self._combo_value(self.infill_pattern_combo, "rectilinear"),
            support_enabled=bool(self.support_enable_check.isChecked()),
            support_type=self._combo_value(self.support_type_combo, "normal"),
            support_style=self._combo_value(self.support_style_combo, "pillars"),
            overhang_angle=float(self.support_angle_spin.value()),
            support_build_plate_only=bool(self.support_build_plate_check.isChecked()),
            support_z_gap=float(self.support_z_gap_spin.value()),
            support_xy_gap=float(self.support_xy_gap_spin.value()),
            interface_layers=int(self.support_interface_layers_spin.value()),
            interface_density=float(self.support_interface_density_spin.value()) / 100.0,
            support_spacing=float(self.support_spacing_spin.value()),
            support_speed=float(self.support_speed_spin.value()),
            support_interface_speed=float(self.support_interface_speed_spin.value()),
            support_pattern=self._combo_value(self.support_pattern_combo, "rectilinear"),
            support_interface_pattern=self._combo_value(self.support_interface_pattern_combo,
                                                       "rectilinear"),
            support_filament_base=self._combo_value(self.support_base_combo, "default"),
            support_filament_interface=self._combo_value(self.support_interface_combo, "default"),
            tree_branch_angle=float(self.tree_branch_angle_spin.value()),
            tree_merge_distance=float(self.tree_merge_distance_spin.value()),
            prime_tower_enabled=bool(self.prime_tower_enable_check.isChecked()),
            prime_tower_width=float(self.prime_tower_width_spin.value()),
            prime_tower_square=bool(self.prime_tower_square_check.isChecked()),
            prime_tower_volume=float(self.prime_tower_volume_spin.value()),
            flush_into_infill=bool(self.flush_into_infill_check.isChecked()),
            flush_into_support=bool(self.flush_into_support_check.isChecked()),
            skirt_loops=int(self.skirt_loops_spin.value()),
            skirt_height=int(self.skirt_height_spin.value()),
            brim_type=self._combo_value(self.brim_type_combo, "auto"),
            brim_width=float(self.brim_width_spin.value()),
            print_sequence=self._combo_value(self.print_sequence_combo, "by_layer"),
            spiral_vase=bool(self.spiral_vase_check.isChecked()),
            ignore_inner_color=bool(self.ignore_inner_color_check.isChecked()),
            timelapse_mode=self._combo_value(self.timelapse_combo, "traditional"),
            fuzzy_skin=self._combo_value(self.fuzzy_skin_combo, "none"),
            filament_name=self._filament_button.text().strip() or self._defaults.filament_name,
            filament_color=self._filament_color.name(),
        )

    def apply_settings(self, settings):
        data = {}
        if isinstance(settings, SliceSettings):
            data = asdict(settings)
        elif isinstance(settings, dict):
            data = settings

        if "layer_height" in data:
            self.layer_height_spin.setValue(float(data["layer_height"]))
        if "first_layer_height" in data:
            self.first_layer_height_spin.setValue(float(data["first_layer_height"]))
        if "seam_position" in data:
            self._set_combo_value(self.seam_position_combo, data["seam_position"])
        if "staggered_inner_seams" in data:
            self.staggered_inner_seams_check.setChecked(bool(data["staggered_inner_seams"]))
        if "seam_gap" in data:
            self.seam_gap_spin.setValue(float(data["seam_gap"]))
        if "scarf_joint_seam" in data:
            self._set_combo_value(self.scarf_joint_seam_combo, data["scarf_joint_seam"])
        if "wipe_use_base_speed" in data:
            self.wipe_use_base_speed_check.setChecked(bool(data["wipe_use_base_speed"]))
        if "wipe_speed_percent" in data:
            self.wipe_speed_spin.setValue(float(data["wipe_speed_percent"]))
        if "wipe_on_loops" in data:
            self.wipe_on_loops_check.setChecked(bool(data["wipe_on_loops"]))
        if "wipe_before_external_loop" in data:
            self.wipe_before_external_loop_check.setChecked(bool(data["wipe_before_external_loop"]))
        if "precise_wall" in data:
            self.precise_wall_check.setChecked(bool(data["precise_wall"]))
        if "slice_gap_closing_radius" in data:
            self.slice_gap_closing_radius_spin.setValue(float(data["slice_gap_closing_radius"]))
        if "resolution" in data:
            self.resolution_spin.setValue(float(data["resolution"]))
        if "arc_fitting" in data:
            self.arc_fitting_check.setChecked(bool(data["arc_fitting"]))
        if "xy_hole_compensation" in data:
            self.xy_hole_compensation_spin.setValue(float(data["xy_hole_compensation"]))
        if "xy_contour_compensation" in data:
            self.xy_contour_compensation_spin.setValue(float(data["xy_contour_compensation"]))
        if "elephant_foot_compensation" in data:
            self.elephant_foot_compensation_spin.setValue(float(data["elephant_foot_compensation"]))
        if "elephant_foot_compensation_layers" in data:
            self.elephant_foot_layers_spin.setValue(int(data["elephant_foot_compensation_layers"]))
        if "convert_holes_to_polyholes" in data:
            self.convert_holes_to_polyholes_check.setChecked(bool(data["convert_holes_to_polyholes"]))
        if "precise_z_height" in data:
            self.precise_z_height_check.setChecked(bool(data["precise_z_height"]))
        if "only_one_wall_top" in data:
            self.only_one_wall_top_check.setChecked(bool(data["only_one_wall_top"]))
        if "only_one_wall_first_layer" in data:
            self.only_one_wall_first_layer_check.setChecked(bool(data["only_one_wall_first_layer"]))
        if "extrusion_width" in data:
            self.line_width_default_spin.setValue(float(data["extrusion_width"]))
        if "first_layer_line_width" in data:
            self.line_width_first_layer_spin.setValue(float(data["first_layer_line_width"]))
        if "outer_wall_line_width" in data:
            self.line_width_outer_wall_spin.setValue(float(data["outer_wall_line_width"]))
        if "inner_wall_line_width" in data:
            self.line_width_inner_wall_spin.setValue(float(data["inner_wall_line_width"]))
        if "top_surface_line_width" in data:
            self.line_width_top_surface_spin.setValue(float(data["top_surface_line_width"]))
        if "sparse_infill_line_width" in data:
            self.line_width_sparse_infill_spin.setValue(float(data["sparse_infill_line_width"]))
        if "internal_solid_infill_line_width" in data:
            self.line_width_internal_solid_spin.setValue(float(data["internal_solid_infill_line_width"]))
        if "support_line_width" in data:
            self.line_width_support_spin.setValue(float(data["support_line_width"]))
        if "ironing_type" in data:
            self._set_combo_value(self.ironing_type_combo, data["ironing_type"])
        if "wall_generator" in data:
            self._set_combo_value(self.wall_generator_combo, data["wall_generator"])
        if "wall_transition_angle" in data:
            self.wall_transition_angle_spin.setValue(float(data["wall_transition_angle"]))
        if "wall_transition_filter_margin" in data:
            self.wall_transition_filter_margin_spin.setValue(float(data["wall_transition_filter_margin"]))
        if "wall_transition_length" in data:
            self.wall_transition_length_spin.setValue(float(data["wall_transition_length"]))
        if "wall_distribution_count" in data:
            self.wall_distribution_count_spin.setValue(int(data["wall_distribution_count"]))
        if "first_layer_min_wall_width" in data:
            self.first_layer_min_wall_width_spin.setValue(float(data["first_layer_min_wall_width"]))
        if "min_wall_width" in data:
            self.min_wall_width_spin.setValue(float(data["min_wall_width"]))
        if "min_feature_size" in data:
            self.min_feature_size_spin.setValue(float(data["min_feature_size"]))
        if "min_wall_length" in data:
            self.min_wall_length_spin.setValue(float(data["min_wall_length"]))
        if "wall_printing_order" in data:
            self._set_combo_value(self.wall_printing_order_combo, data["wall_printing_order"])
        if "print_infill_first" in data:
            self.print_infill_first_check.setChecked(bool(data["print_infill_first"]))
        if "wall_loop_direction" in data:
            self._set_combo_value(self.wall_loop_direction_combo, data["wall_loop_direction"])
        if "top_surface_flow_ratio" in data:
            self.top_surface_flow_ratio_spin.setValue(float(data["top_surface_flow_ratio"]))
        if "bottom_surface_flow_ratio" in data:
            self.bottom_surface_flow_ratio_spin.setValue(float(data["bottom_surface_flow_ratio"]))
        if "one_wall_threshold" in data:
            self.one_wall_threshold_spin.setValue(float(data["one_wall_threshold"]))
        if "avoid_crossing_walls" in data:
            self.avoid_crossing_walls_check.setChecked(bool(data["avoid_crossing_walls"]))
        if "small_area_flow_compensation" in data:
            self.small_area_flow_compensation_check.setChecked(bool(data["small_area_flow_compensation"]))
        if "smooth_wall_speed_z" in data:
            self.smooth_wall_speed_z_check.setChecked(bool(data["smooth_wall_speed_z"]))
        if "bridge_flow_ratio" in data:
            self.bridge_flow_ratio_spin.setValue(float(data["bridge_flow_ratio"]))
        if "internal_bridge_flow_ratio" in data:
            self.internal_bridge_flow_ratio_spin.setValue(float(data["internal_bridge_flow_ratio"]))
        if "bridge_density" in data:
            self.bridge_density_spin.setValue(float(data["bridge_density"]))
        if "thick_bridges" in data:
            self.thick_bridges_check.setChecked(bool(data["thick_bridges"]))
        if "thick_internal_bridges" in data:
            self.thick_internal_bridges_check.setChecked(bool(data["thick_internal_bridges"]))
        if "bridge_filter_mode" in data:
            self._set_combo_value(self.bridge_filter_mode_combo, data["bridge_filter_mode"])
        if "bridge_counterbore_holes" in data:
            self._set_combo_value(self.bridge_counterbore_combo, data["bridge_counterbore_holes"])
        if "detect_overhang_walls" in data:
            self.detect_overhang_walls_check.setChecked(bool(data["detect_overhang_walls"]))
        if "make_overhangs_printable" in data:
            self.make_overhangs_printable_check.setChecked(bool(data["make_overhangs_printable"]))
        if "extra_perimeters_on_overhangs" in data:
            self.extra_perimeters_on_overhangs_check.setChecked(
                bool(data["extra_perimeters_on_overhangs"])
            )
        if "reverse_overhang_on_odd" in data:
            self.reverse_overhang_on_odd_check.setChecked(bool(data["reverse_overhang_on_odd"]))
        if "overhang_optimization" in data:
            self.overhang_optimization_check.setChecked(bool(data["overhang_optimization"]))
        if "perimeter_count" in data:
            self.wall_loops_spin.setValue(int(data["perimeter_count"]))
        if "top_layers" in data:
            self.top_shell_layers_spin.setValue(int(data["top_layers"]))
        if "bottom_layers" in data:
            self.bottom_shell_layers_spin.setValue(int(data["bottom_layers"]))
        if "infill_percent" in data:
            self.infill_density_spin.setValue(int(float(data["infill_percent"])))
        if "infill_pattern" in data:
            self._set_combo_value(self.infill_pattern_combo, data["infill_pattern"])
        if "support_enabled" in data:
            self.support_enable_check.setChecked(bool(data["support_enabled"]))
        if "support_type" in data:
            self._set_combo_value(self.support_type_combo, data["support_type"])
        if "support_style" in data:
            self._set_combo_value(self.support_style_combo, data["support_style"])
        if "overhang_angle" in data:
            self.support_angle_spin.setValue(float(data["overhang_angle"]))
        if "support_build_plate_only" in data:
            self.support_build_plate_check.setChecked(bool(data["support_build_plate_only"]))
        if "support_z_gap" in data:
            self.support_z_gap_spin.setValue(float(data["support_z_gap"]))
        if "support_xy_gap" in data:
            self.support_xy_gap_spin.setValue(float(data["support_xy_gap"]))
        if "interface_layers" in data:
            self.support_interface_layers_spin.setValue(int(data["interface_layers"]))
        if "interface_density" in data:
            density = max(0.0, min(1.0, float(data["interface_density"]))) * 100.0
            self.support_interface_density_spin.setValue(density)
        if "support_spacing" in data:
            self.support_spacing_spin.setValue(float(data["support_spacing"]))
        if "support_speed" in data:
            self.support_speed_spin.setValue(float(data["support_speed"]))
        if "support_interface_speed" in data:
            self.support_interface_speed_spin.setValue(float(data["support_interface_speed"]))
        if "support_pattern" in data:
            self._set_combo_value(self.support_pattern_combo, data["support_pattern"])
        if "support_interface_pattern" in data:
            self._set_combo_value(self.support_interface_pattern_combo,
                                  data["support_interface_pattern"])
        if "support_filament_base" in data:
            self._set_combo_value(self.support_base_combo, data["support_filament_base"])
        if "support_filament_interface" in data:
            self._set_combo_value(self.support_interface_combo, data["support_filament_interface"])
        if "tree_branch_angle" in data:
            self.tree_branch_angle_spin.setValue(float(data["tree_branch_angle"]))
        if "tree_merge_distance" in data:
            self.tree_merge_distance_spin.setValue(float(data["tree_merge_distance"]))
        if "prime_tower_enabled" in data:
            self.prime_tower_enable_check.setChecked(bool(data["prime_tower_enabled"]))
        if "prime_tower_width" in data:
            self.prime_tower_width_spin.setValue(float(data["prime_tower_width"]))
        if "prime_tower_square" in data:
            self.prime_tower_square_check.setChecked(bool(data["prime_tower_square"]))
        if "prime_tower_volume" in data:
            self.prime_tower_volume_spin.setValue(float(data["prime_tower_volume"]))
        if "flush_into_infill" in data:
            self.flush_into_infill_check.setChecked(bool(data["flush_into_infill"]))
        if "flush_into_support" in data:
            self.flush_into_support_check.setChecked(bool(data["flush_into_support"]))
        if "skirt_loops" in data:
            self.skirt_loops_spin.setValue(int(data["skirt_loops"]))
        if "skirt_height" in data:
            self.skirt_height_spin.setValue(int(data["skirt_height"]))
        if "brim_type" in data:
            self._set_combo_value(self.brim_type_combo, data["brim_type"])
        if "brim_width" in data:
            self.brim_width_spin.setValue(float(data["brim_width"]))
        if "print_sequence" in data:
            self._set_combo_value(self.print_sequence_combo, data["print_sequence"])
        if "spiral_vase" in data:
            self.spiral_vase_check.setChecked(bool(data["spiral_vase"]))
        if "ignore_inner_color" in data:
            self.ignore_inner_color_check.setChecked(bool(data["ignore_inner_color"]))
        if "timelapse_mode" in data:
            self._set_combo_value(self.timelapse_combo, data["timelapse_mode"])
        if "fuzzy_skin" in data:
            self._set_combo_value(self.fuzzy_skin_combo, data["fuzzy_skin"])
        if "filament_name" in data:
            name = str(data["filament_name"]).strip()
            if name:
                self._filament_button.setText(name)
        if "filament_color" in data:
            color = QtGui.QColor(str(data["filament_color"]))
            if color.isValid():
                self._filament_color = color
                self._update_filament_button_style()
