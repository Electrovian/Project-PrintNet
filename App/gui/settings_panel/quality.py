from __future__ import annotations

from typing import Any, TYPE_CHECKING

from PyQt5 import QtCore, QtGui, QtWidgets


class QualitySectionMixin:
    if TYPE_CHECKING:
        def __getattr__(self, name: str) -> Any: ...

    def _build_quality_page(self):
        layout = self._build_page("quality")

        section, section_layout = self._section("Layer height")
        self.layer_height_spin = self._make_double_spin(
            self._defaults.layer_height, 0.05, 1.0, 0.01, "mm"
        )
        self._label_layer_height = self._add_row(
            "quality",
            section,
            section_layout,
            "Layer height",
            self.layer_height_spin,
            "Height of each layer.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_layer_height, "layer_height")
        self._register_hover_tooltip(self.layer_height_spin, "layer_height")
        self.first_layer_height_spin = self._make_double_spin(
            self._defaults.first_layer_height, 0.05, 1.0, 0.01, "mm"
        )
        self._label_first_layer_height = self._add_row(
            "quality",
            section,
            section_layout,
            "First layer height",
            self.first_layer_height_spin,
            "Height of the first layer.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_first_layer_height, "first_layer_height")
        self._register_hover_tooltip(self.first_layer_height_spin, "first_layer_height")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Line width")
        self.line_width_default_spin = self._make_double_spin(
            self._defaults.extrusion_width, 0.1, 2.0, 0.01, "mm"
        )
        self._label_line_width_default = self._add_row(
            "quality", section, section_layout, "Default",
            self.line_width_default_spin, "Default extrusion width.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_default, "line_width_default")
        self._register_hover_tooltip(self.line_width_default_spin, "line_width_default")
        self.line_width_first_layer_spin = self._make_double_spin(
            self._defaults.first_layer_line_width, 0.1, 3.0, 0.01, "mm"
        )
        self._label_line_width_first_layer = self._add_row(
            "quality", section, section_layout, "First layer",
            self.line_width_first_layer_spin, "Extrusion width on the first layer.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_first_layer, "line_width_first_layer")
        self._register_hover_tooltip(self.line_width_first_layer_spin, "line_width_first_layer")
        self.line_width_outer_wall_spin = self._make_double_spin(
            self._defaults.outer_wall_line_width, 0.1, 2.0, 0.01, "mm"
        )
        self._label_line_width_outer_wall = self._add_row(
            "quality", section, section_layout, "Outer wall",
            self.line_width_outer_wall_spin, "Extrusion width for outer walls.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_outer_wall, "line_width_outer_wall")
        self._register_hover_tooltip(self.line_width_outer_wall_spin, "line_width_outer_wall")
        self.line_width_inner_wall_spin = self._make_double_spin(
            self._defaults.inner_wall_line_width, 0.1, 2.0, 0.01, "mm"
        )
        self._label_line_width_inner_wall = self._add_row(
            "quality", section, section_layout, "Inner wall",
            self.line_width_inner_wall_spin, "Extrusion width for inner walls.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_inner_wall, "line_width_inner_wall")
        self._register_hover_tooltip(self.line_width_inner_wall_spin, "line_width_inner_wall")
        self.line_width_top_surface_spin = self._make_double_spin(
            self._defaults.top_surface_line_width, 0.1, 2.0, 0.01, "mm"
        )
        self._label_line_width_top_surface = self._add_row(
            "quality", section, section_layout, "Top surface",
            self.line_width_top_surface_spin, "Extrusion width for top surfaces.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_top_surface, "line_width_top_surface")
        self._register_hover_tooltip(self.line_width_top_surface_spin, "line_width_top_surface")
        self.line_width_sparse_infill_spin = self._make_double_spin(
            self._defaults.sparse_infill_line_width, 0.1, 2.0, 0.01, "mm"
        )
        self._label_line_width_sparse_infill = self._add_row(
            "quality", section, section_layout, "Sparse infill",
            self.line_width_sparse_infill_spin, "Extrusion width for sparse infill.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_sparse_infill, "line_width_sparse_infill")
        self._register_hover_tooltip(self.line_width_sparse_infill_spin, "line_width_sparse_infill")
        self.line_width_internal_solid_spin = self._make_double_spin(
            self._defaults.internal_solid_infill_line_width, 0.1, 2.0, 0.01, "mm"
        )
        self._label_line_width_internal_solid = self._add_row(
            "quality", section, section_layout, "Internal solid infill",
            self.line_width_internal_solid_spin, "Extrusion width for internal solid infill.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_internal_solid,
                                     "line_width_internal_solid")
        self._register_hover_tooltip(self.line_width_internal_solid_spin,
                                     "line_width_internal_solid")
        self.line_width_support_spin = self._make_double_spin(
            self._defaults.support_line_width, 0.1, 2.0, 0.01, "mm"
        )
        self._label_line_width_support = self._add_row(
            "quality", section, section_layout, "Support",
            self.line_width_support_spin, "Extrusion width for supports.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_line_width_support, "line_width_support")
        self._register_hover_tooltip(self.line_width_support_spin, "line_width_support")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Seam", advanced=True)
        self.seam_position_combo = self._make_combo(
            [
                ("Nearest", "nearest"),
                ("Aligned", "aligned"),
                ("Back", "back"),
                ("Random", "random"),
                ("Assemble", "assemble"),
            ]
        )
        self._set_combo_value(self.seam_position_combo, self._defaults.seam_position)
        self._label_seam_position = self._add_row(
            "quality",
            section,
            section_layout,
            "Seam position",
            self.seam_position_combo,
            "Starting position for each outer wall loop.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_seam_position, "seam_position")
        self._register_hover_tooltip(self.seam_position_combo, "seam_position")
        self.staggered_inner_seams_check = QtWidgets.QCheckBox(section)
        self.staggered_inner_seams_check.setObjectName("SettingsCheck")
        self.staggered_inner_seams_check.setChecked(bool(self._defaults.staggered_inner_seams))
        self._label_staggered_inner_seams = self._add_row(
            "quality", section, section_layout, "Staggered inner seams",
            self.staggered_inner_seams_check, "Offset inner seams to reduce alignment.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_staggered_inner_seams, "staggered_inner_seams")
        self._register_hover_tooltip(self.staggered_inner_seams_check, "staggered_inner_seams")
        self.seam_gap_spin = self._make_double_spin(self._defaults.seam_gap, 0.0, 100.0, 1.0, "%")
        self._label_seam_gap = self._add_row(
            "quality", section, section_layout, "Seam gap",
            self.seam_gap_spin, "Skip a small percentage of the seam to reduce blobs.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_seam_gap, "seam_gap")
        self._register_hover_tooltip(self.seam_gap_spin, "seam_gap")
        self.scarf_joint_seam_combo = self._make_combo(
            [
                ("None", "none"),
                ("Contour", "contour"),
                ("Contour and hole", "contour_hole"),
            ]
        )
        self._set_combo_value(self.scarf_joint_seam_combo, self._defaults.scarf_joint_seam)
        self._label_scarf_joint_seam = self._add_row(
            "quality", section, section_layout, "Scarf joint seam (beta)",
            self.scarf_joint_seam_combo, "Apply seam shaping on contours/holes.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_scarf_joint_seam, "scarf_joint_seam")
        self._register_hover_tooltip(self.scarf_joint_seam_combo, "scarf_joint_seam")
        self.wipe_use_base_speed_check = QtWidgets.QCheckBox(section)
        self.wipe_use_base_speed_check.setObjectName("SettingsCheck")
        self.wipe_use_base_speed_check.setChecked(bool(self._defaults.wipe_use_base_speed))
        self._label_wipe_use_base_speed = self._add_row(
            "quality", section, section_layout, "Use base wipe speed",
            self.wipe_use_base_speed_check, "Use the base print speed for wipe moves.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wipe_use_base_speed, "wipe_use_base_speed")
        self._register_hover_tooltip(self.wipe_use_base_speed_check, "wipe_use_base_speed")
        self.wipe_speed_spin = self._make_double_spin(
            self._defaults.wipe_speed_percent, 0.0, 200.0, 5.0, "%"
        )
        self._label_wipe_speed = self._add_row(
            "quality", section, section_layout, "Wipe speed",
            self.wipe_speed_spin, "Wipe speed as a percent of the base speed.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wipe_speed, "wipe_speed")
        self._register_hover_tooltip(self.wipe_speed_spin, "wipe_speed")
        self.wipe_on_loops_check = QtWidgets.QCheckBox(section)
        self.wipe_on_loops_check.setObjectName("SettingsCheck")
        self.wipe_on_loops_check.setChecked(bool(self._defaults.wipe_on_loops))
        self._label_wipe_on_loops = self._add_row(
            "quality", section, section_layout, "Wipe on loops",
            self.wipe_on_loops_check, "Add a short wipe at loop ends.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wipe_on_loops, "wipe_on_loops")
        self._register_hover_tooltip(self.wipe_on_loops_check, "wipe_on_loops")
        self.wipe_before_external_loop_check = QtWidgets.QCheckBox(section)
        self.wipe_before_external_loop_check.setObjectName("SettingsCheck")
        self.wipe_before_external_loop_check.setChecked(bool(self._defaults.wipe_before_external_loop))
        self._label_wipe_before_external = self._add_row(
            "quality", section, section_layout, "Wipe before external loop",
            self.wipe_before_external_loop_check,
            "Wipe before starting the outer wall.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wipe_before_external, "wipe_before_external_loop")
        self._register_hover_tooltip(self.wipe_before_external_loop_check,
                                     "wipe_before_external_loop")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Precision", advanced=True)
        self.precise_wall_check = QtWidgets.QCheckBox(section)
        self.precise_wall_check.setObjectName("SettingsCheck")
        self.precise_wall_check.setChecked(bool(self._defaults.precise_wall))
        self._label_precise_wall = self._add_row(
            "quality",
            section,
            section_layout,
            "Precise wall",
            self.precise_wall_check,
            "Adjust outer wall spacing for better accuracy.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_precise_wall, "precise_wall")
        self._register_hover_tooltip(self.precise_wall_check, "precise_wall")
        self.slice_gap_closing_radius_spin = self._make_double_spin(
            self._defaults.slice_gap_closing_radius, 0.0, 1.0, 0.001, "mm"
        )
        self._label_slice_gap_closing = self._add_row(
            "quality", section, section_layout, "Slice gap closing radius",
            self.slice_gap_closing_radius_spin,
            "Close tiny gaps during slicing.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_slice_gap_closing, "slice_gap_closing_radius")
        self._register_hover_tooltip(self.slice_gap_closing_radius_spin,
                                     "slice_gap_closing_radius")
        self.resolution_spin = self._make_double_spin(
            self._defaults.resolution, 0.0, 1.0, 0.001, "mm"
        )
        self._label_resolution = self._add_row(
            "quality", section, section_layout, "Resolution",
            self.resolution_spin,
            "Simplification tolerance for sliced polygons.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_resolution, "resolution")
        self._register_hover_tooltip(self.resolution_spin, "resolution")
        self.arc_fitting_check = QtWidgets.QCheckBox(section)
        self.arc_fitting_check.setObjectName("SettingsCheck")
        self.arc_fitting_check.setChecked(bool(self._defaults.arc_fitting))
        self._label_arc_fitting = self._add_row(
            "quality", section, section_layout, "Arc fitting",
            self.arc_fitting_check, "Use arcs for compatible loops.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_arc_fitting, "arc_fitting")
        self._register_hover_tooltip(self.arc_fitting_check, "arc_fitting")
        self.xy_hole_compensation_spin = self._make_double_spin(
            self._defaults.xy_hole_compensation, -1.0, 1.0, 0.01, "mm"
        )
        self._label_xy_hole_comp = self._add_row(
            "quality", section, section_layout, "X-Y hole compensation",
            self.xy_hole_compensation_spin,
            "Offset circular holes to improve fit.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_xy_hole_comp, "xy_hole_compensation")
        self._register_hover_tooltip(self.xy_hole_compensation_spin, "xy_hole_compensation")
        self.xy_contour_compensation_spin = self._make_double_spin(
            self._defaults.xy_contour_compensation, -1.0, 1.0, 0.01, "mm"
        )
        self._label_xy_contour_comp = self._add_row(
            "quality", section, section_layout, "X-Y contour compensation",
            self.xy_contour_compensation_spin,
            "Offset model contours to tweak dimensions.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_xy_contour_comp, "xy_contour_compensation")
        self._register_hover_tooltip(self.xy_contour_compensation_spin,
                                     "xy_contour_compensation")
        self.elephant_foot_compensation_spin = self._make_double_spin(
            self._defaults.elephant_foot_compensation, 0.0, 2.0, 0.01, "mm"
        )
        self._label_elephant_foot = self._add_row(
            "quality", section, section_layout, "Elephant foot compensation",
            self.elephant_foot_compensation_spin,
            "Shrink lower layers to reduce bulging.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_elephant_foot, "elephant_foot_compensation")
        self._register_hover_tooltip(self.elephant_foot_compensation_spin,
                                     "elephant_foot_compensation")
        self.elephant_foot_layers_spin = self._make_int_spin(
            self._defaults.elephant_foot_compensation_layers, 0, 10, suffix="layers"
        )
        self._label_elephant_foot_layers = self._add_row(
            "quality", section, section_layout, "Elephant foot compensation layers",
            self.elephant_foot_layers_spin,
            "Number of layers to apply elephant foot compensation.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_elephant_foot_layers, "elephant_foot_layers")
        self._register_hover_tooltip(self.elephant_foot_layers_spin, "elephant_foot_layers")
        self.convert_holes_to_polyholes_check = QtWidgets.QCheckBox(section)
        self.convert_holes_to_polyholes_check.setObjectName("SettingsCheck")
        self.convert_holes_to_polyholes_check.setChecked(bool(self._defaults.convert_holes_to_polyholes))
        self._label_convert_holes = self._add_row(
            "quality", section, section_layout, "Convert holes to polyholes",
            self.convert_holes_to_polyholes_check,
            "Approximate circular holes with polygons.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_convert_holes, "convert_holes_to_polyholes")
        self._register_hover_tooltip(self.convert_holes_to_polyholes_check,
                                     "convert_holes_to_polyholes")
        self.precise_z_height_check = QtWidgets.QCheckBox(section)
        self.precise_z_height_check.setObjectName("SettingsCheck")
        self.precise_z_height_check.setChecked(bool(self._defaults.precise_z_height))
        self._label_precise_z_height = self._add_row(
            "quality", section, section_layout, "Precise Z height",
            self.precise_z_height_check,
            "Adjust final layers to match the exact model height.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_precise_z_height, "precise_z_height")
        self._register_hover_tooltip(self.precise_z_height_check, "precise_z_height")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Ironing", advanced=True)
        self.ironing_type_combo = self._make_combo(
            [
                ("No ironing", "no_ironing"),
                ("All top surfaces", "all_top_surfaces"),
                ("Topmost surface only", "topmost_surface_only"),
                ("All solid layers", "all_solid_layers"),
            ]
        )
        self._set_combo_value(self.ironing_type_combo, self._defaults.ironing_type)
        self._label_ironing_type = self._add_row(
            "quality", section, section_layout, "Ironing type",
            self.ironing_type_combo, "Control which layers are ironed.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_ironing_type, "ironing_type")
        self._register_hover_tooltip(self.ironing_type_combo, "ironing_type")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Wall generator", advanced=True)
        self.wall_generator_combo = self._make_combo(
            [
                ("Classic", "classic"),
                ("Arachne", "arachne"),
            ]
        )
        self._set_combo_value(self.wall_generator_combo, self._defaults.wall_generator)
        self._label_wall_generator = self._add_row(
            "quality", section, section_layout, "Wall generator",
            self.wall_generator_combo, "Select the wall generation method.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wall_generator, "wall_generator")
        self._register_hover_tooltip(self.wall_generator_combo, "wall_generator")
        self.wall_transition_angle_spin = self._make_double_spin(
            self._defaults.wall_transition_angle, 0.0, 90.0, 1.0, "deg"
        )
        self._label_wall_transition_angle = self._add_row(
            "quality", section, section_layout, "Wall transitioning threshold angle",
            self.wall_transition_angle_spin, "Angle threshold for wall transitions.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wall_transition_angle, "wall_transition_angle")
        self._register_hover_tooltip(self.wall_transition_angle_spin, "wall_transition_angle")
        self.wall_transition_filter_margin_spin = self._make_double_spin(
            self._defaults.wall_transition_filter_margin, 0.0, 200.0, 1.0, "%"
        )
        self._label_wall_transition_filter = self._add_row(
            "quality", section, section_layout, "Wall transitioning filter margin",
            self.wall_transition_filter_margin_spin, "Filter margin for wall transitions.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wall_transition_filter,
                                     "wall_transition_filter_margin")
        self._register_hover_tooltip(self.wall_transition_filter_margin_spin,
                                     "wall_transition_filter_margin")
        self.wall_transition_length_spin = self._make_double_spin(
            self._defaults.wall_transition_length, 0.0, 500.0, 1.0, "%"
        )
        self._label_wall_transition_length = self._add_row(
            "quality", section, section_layout, "Wall transition length",
            self.wall_transition_length_spin, "Transition length percentage.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wall_transition_length, "wall_transition_length")
        self._register_hover_tooltip(self.wall_transition_length_spin, "wall_transition_length")
        self.wall_distribution_count_spin = self._make_int_spin(
            self._defaults.wall_distribution_count, 1, 10
        )
        self._label_wall_distribution_count = self._add_row(
            "quality", section, section_layout, "Wall distribution count",
            self.wall_distribution_count_spin, "Number of walls for distribution.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wall_distribution_count, "wall_distribution_count")
        self._register_hover_tooltip(self.wall_distribution_count_spin, "wall_distribution_count")
        self.first_layer_min_wall_width_spin = self._make_double_spin(
            self._defaults.first_layer_min_wall_width, 10.0, 400.0, 1.0, "%"
        )
        self._label_first_layer_min_wall = self._add_row(
            "quality", section, section_layout, "First layer minimum wall width",
            self.first_layer_min_wall_width_spin, "Minimum wall width on the first layer.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_first_layer_min_wall,
                                     "first_layer_min_wall_width")
        self._register_hover_tooltip(self.first_layer_min_wall_width_spin,
                                     "first_layer_min_wall_width")
        self.min_wall_width_spin = self._make_double_spin(
            self._defaults.min_wall_width, 10.0, 400.0, 1.0, "%"
        )
        self._label_min_wall_width = self._add_row(
            "quality", section, section_layout, "Minimum wall width",
            self.min_wall_width_spin, "Minimum wall width for thin features.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_min_wall_width, "min_wall_width")
        self._register_hover_tooltip(self.min_wall_width_spin, "min_wall_width")
        self.min_feature_size_spin = self._make_double_spin(
            self._defaults.min_feature_size, 10.0, 400.0, 1.0, "%"
        )
        self._label_min_feature_size = self._add_row(
            "quality", section, section_layout, "Minimum feature size",
            self.min_feature_size_spin, "Minimum feature size percentage.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_min_feature_size, "min_feature_size")
        self._register_hover_tooltip(self.min_feature_size_spin, "min_feature_size")
        self.min_wall_length_spin = self._make_double_spin(
            self._defaults.min_wall_length, 0.0, 5.0, 0.1, "mm"
        )
        self._label_min_wall_length = self._add_row(
            "quality", section, section_layout, "Minimum wall length",
            self.min_wall_length_spin, "Discard walls shorter than this.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_min_wall_length, "min_wall_length")
        self._register_hover_tooltip(self.min_wall_length_spin, "min_wall_length")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Walls and surfaces", advanced=True)
        self.wall_printing_order_combo = self._make_combo(
            [
                ("Inner/Outer", "inner_outer"),
                ("Outer/Inner", "outer_inner"),
                ("Inner/Outer/Inner", "inner_outer_inner"),
                ("Adaptive Outer/Inner (experimental)", "adaptive_outer_inner"),
            ]
        )
        self._set_combo_value(self.wall_printing_order_combo, self._defaults.wall_printing_order)
        self._label_wall_printing_order = self._add_row(
            "quality", section, section_layout, "Walls printing order",
            self.wall_printing_order_combo, "Order for printing wall perimeters.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wall_printing_order, "wall_printing_order")
        self._register_hover_tooltip(self.wall_printing_order_combo, "wall_printing_order")
        self.print_infill_first_check = QtWidgets.QCheckBox(section)
        self.print_infill_first_check.setObjectName("SettingsCheck")
        self.print_infill_first_check.setChecked(bool(self._defaults.print_infill_first))
        self._label_print_infill_first = self._add_row(
            "quality", section, section_layout, "Print infill first",
            self.print_infill_first_check, "Print infill before walls.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_print_infill_first, "print_infill_first")
        self._register_hover_tooltip(self.print_infill_first_check, "print_infill_first")
        self.wall_loop_direction_combo = self._make_combo(
            [
                ("Auto", "auto"),
                ("Counter clockwise", "counter_clockwise"),
                ("Clockwise", "clockwise"),
            ]
        )
        self._set_combo_value(self.wall_loop_direction_combo, self._defaults.wall_loop_direction)
        self._label_wall_loop_direction = self._add_row(
            "quality", section, section_layout, "Wall loop direction",
            self.wall_loop_direction_combo, "Direction for perimeter loops.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_wall_loop_direction, "wall_loop_direction")
        self._register_hover_tooltip(self.wall_loop_direction_combo, "wall_loop_direction")
        self.top_surface_flow_ratio_spin = self._make_double_spin(
            self._defaults.top_surface_flow_ratio, 0.5, 2.0, 0.05
        )
        self._label_top_surface_flow_ratio = self._add_row(
            "quality", section, section_layout, "Top surface flow ratio",
            self.top_surface_flow_ratio_spin, "Extrusion multiplier for top surfaces.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_top_surface_flow_ratio, "top_surface_flow_ratio")
        self._register_hover_tooltip(self.top_surface_flow_ratio_spin, "top_surface_flow_ratio")
        self.bottom_surface_flow_ratio_spin = self._make_double_spin(
            self._defaults.bottom_surface_flow_ratio, 0.5, 2.0, 0.05
        )
        self._label_bottom_surface_flow_ratio = self._add_row(
            "quality", section, section_layout, "Bottom surface flow ratio",
            self.bottom_surface_flow_ratio_spin, "Extrusion multiplier for bottom surfaces.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_bottom_surface_flow_ratio, "bottom_surface_flow_ratio")
        self._register_hover_tooltip(self.bottom_surface_flow_ratio_spin, "bottom_surface_flow_ratio")
        self.only_one_wall_top_check = QtWidgets.QCheckBox(section)
        self.only_one_wall_top_check.setObjectName("SettingsCheck")
        self.only_one_wall_top_check.setChecked(bool(self._defaults.only_one_wall_top))
        self._label_one_wall_top = self._add_row(
            "quality",
            section,
            section_layout,
            "Only one wall on top surfaces",
            self.only_one_wall_top_check,
            "Use a single wall for top surfaces.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_one_wall_top, "only_one_wall_top")
        self._register_hover_tooltip(self.only_one_wall_top_check, "only_one_wall_top")
        self.one_wall_threshold_spin = self._make_double_spin(
            self._defaults.one_wall_threshold, 0.0, 500.0, 5.0, "%"
        )
        self._label_one_wall_threshold = self._add_row(
            "quality", section, section_layout, "One wall threshold",
            self.one_wall_threshold_spin,
            "Threshold for using a single wall on small surfaces.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_one_wall_threshold, "one_wall_threshold")
        self._register_hover_tooltip(self.one_wall_threshold_spin, "one_wall_threshold")
        self.only_one_wall_first_layer_check = QtWidgets.QCheckBox(section)
        self.only_one_wall_first_layer_check.setObjectName("SettingsCheck")
        self.only_one_wall_first_layer_check.setChecked(bool(self._defaults.only_one_wall_first_layer))
        self._label_one_wall_first = self._add_row(
            "quality",
            section,
            section_layout,
            "Only one wall on first layer",
            self.only_one_wall_first_layer_check,
            "Use a single wall for the first layer.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_one_wall_first, "only_one_wall_first")
        self._register_hover_tooltip(self.only_one_wall_first_layer_check, "only_one_wall_first")
        self.avoid_crossing_walls_check = QtWidgets.QCheckBox(section)
        self.avoid_crossing_walls_check.setObjectName("SettingsCheck")
        self.avoid_crossing_walls_check.setChecked(bool(self._defaults.avoid_crossing_walls))
        self._label_avoid_crossing_walls = self._add_row(
            "quality", section, section_layout, "Avoid crossing walls",
            self.avoid_crossing_walls_check,
            "Keep travel moves inside perimeters when possible.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_avoid_crossing_walls, "avoid_crossing_walls")
        self._register_hover_tooltip(self.avoid_crossing_walls_check, "avoid_crossing_walls")
        self.small_area_flow_compensation_check = QtWidgets.QCheckBox(section)
        self.small_area_flow_compensation_check.setObjectName("SettingsCheck")
        self.small_area_flow_compensation_check.setChecked(bool(self._defaults.small_area_flow_compensation))
        self._label_small_area_flow_comp = self._add_row(
            "quality", section, section_layout, "Small area flow compensation (beta)",
            self.small_area_flow_compensation_check,
            "Reduce flow on tiny segments.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_small_area_flow_comp,
                                     "small_area_flow_compensation")
        self._register_hover_tooltip(self.small_area_flow_compensation_check,
                                     "small_area_flow_compensation")
        self.smooth_wall_speed_z_check = QtWidgets.QCheckBox(section)
        self.smooth_wall_speed_z_check.setObjectName("SettingsCheck")
        self.smooth_wall_speed_z_check.setChecked(bool(self._defaults.smooth_wall_speed_z))
        self._label_smooth_wall_speed_z = self._add_row(
            "quality", section, section_layout, "Smoothing wall speed along Z (experimental)",
            self.smooth_wall_speed_z_check,
            "Smooth wall speeds across variable layer heights.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_smooth_wall_speed_z, "smooth_wall_speed_z")
        self._register_hover_tooltip(self.smooth_wall_speed_z_check, "smooth_wall_speed_z")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Bridging", advanced=True)
        self.bridge_flow_ratio_spin = self._make_double_spin(
            self._defaults.bridge_flow_ratio, 0.1, 2.0, 0.05
        )
        self._label_bridge_flow_ratio = self._add_row(
            "quality", section, section_layout, "Bridge flow ratio",
            self.bridge_flow_ratio_spin, "Extrusion multiplier for bridge lines.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_bridge_flow_ratio, "bridge_flow_ratio")
        self._register_hover_tooltip(self.bridge_flow_ratio_spin, "bridge_flow_ratio")
        self.internal_bridge_flow_ratio_spin = self._make_double_spin(
            self._defaults.internal_bridge_flow_ratio, 0.1, 2.0, 0.05
        )
        self._label_internal_bridge_flow_ratio = self._add_row(
            "quality", section, section_layout, "Internal bridge flow ratio",
            self.internal_bridge_flow_ratio_spin,
            "Extrusion multiplier for internal bridges.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_internal_bridge_flow_ratio,
                                     "internal_bridge_flow_ratio")
        self._register_hover_tooltip(self.internal_bridge_flow_ratio_spin,
                                     "internal_bridge_flow_ratio")
        self.bridge_density_spin = self._make_double_spin(
            self._defaults.bridge_density, 0.0, 100.0, 1.0, "%"
        )
        self._label_bridge_density = self._add_row(
            "quality", section, section_layout, "Bridge density",
            self.bridge_density_spin, "Density of bridge infill.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_bridge_density, "bridge_density")
        self._register_hover_tooltip(self.bridge_density_spin, "bridge_density")
        self.thick_bridges_check = QtWidgets.QCheckBox(section)
        self.thick_bridges_check.setObjectName("SettingsCheck")
        self.thick_bridges_check.setChecked(bool(self._defaults.thick_bridges))
        self._label_thick_bridges = self._add_row(
            "quality", section, section_layout, "Thick bridges",
            self.thick_bridges_check, "Use thicker extrusion for bridges.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_thick_bridges, "thick_bridges")
        self._register_hover_tooltip(self.thick_bridges_check, "thick_bridges")
        self.thick_internal_bridges_check = QtWidgets.QCheckBox(section)
        self.thick_internal_bridges_check.setObjectName("SettingsCheck")
        self.thick_internal_bridges_check.setChecked(bool(self._defaults.thick_internal_bridges))
        self._label_thick_internal_bridges = self._add_row(
            "quality", section, section_layout, "Thick internal bridges",
            self.thick_internal_bridges_check,
            "Use thicker extrusion for internal bridges.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_thick_internal_bridges, "thick_internal_bridges")
        self._register_hover_tooltip(self.thick_internal_bridges_check,
                                     "thick_internal_bridges")
        self.bridge_filter_mode_combo = self._make_combo(
            [
                ("Disabled", "disabled"),
                ("Limited filtering", "limited"),
                ("No filtering", "none"),
            ]
        )
        self._set_combo_value(self.bridge_filter_mode_combo, self._defaults.bridge_filter_mode)
        self._label_bridge_filter_mode = self._add_row(
            "quality", section, section_layout, "Don't filter out small internal bridges (beta)",
            self.bridge_filter_mode_combo,
            "Control filtering for small internal bridges.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_bridge_filter_mode, "bridge_filter_mode")
        self._register_hover_tooltip(self.bridge_filter_mode_combo, "bridge_filter_mode")
        self.bridge_counterbore_combo = self._make_combo(
            [
                ("None", "none"),
                ("Partially bridged", "partial"),
                ("Sacrificial layer", "sacrificial"),
            ]
        )
        self._set_combo_value(self.bridge_counterbore_combo, self._defaults.bridge_counterbore_holes)
        self._label_bridge_counterbore = self._add_row(
            "quality", section, section_layout, "Bridge counterbore holes",
            self.bridge_counterbore_combo,
            "Create bridges for counterbore holes.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_bridge_counterbore, "bridge_counterbore_holes")
        self._register_hover_tooltip(self.bridge_counterbore_combo, "bridge_counterbore_holes")
        layout.insertWidget(layout.count() - 1, section)

        section, section_layout = self._section("Overhangs", advanced=True)
        self.detect_overhang_walls_check = QtWidgets.QCheckBox(section)
        self.detect_overhang_walls_check.setObjectName("SettingsCheck")
        self.detect_overhang_walls_check.setChecked(bool(self._defaults.detect_overhang_walls))
        self._label_detect_overhang_walls = self._add_row(
            "quality", section, section_layout, "Detect overhang walls",
            self.detect_overhang_walls_check,
            "Detect walls that exceed the overhang angle.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_detect_overhang_walls, "detect_overhang_walls")
        self._register_hover_tooltip(self.detect_overhang_walls_check, "detect_overhang_walls")
        self.make_overhangs_printable_check = QtWidgets.QCheckBox(section)
        self.make_overhangs_printable_check.setObjectName("SettingsCheck")
        self.make_overhangs_printable_check.setChecked(bool(self._defaults.make_overhangs_printable))
        self._label_make_overhangs_printable = self._add_row(
            "quality", section, section_layout, "Make overhangs printable",
            self.make_overhangs_printable_check,
            "Adjust slicing to improve overhang printability.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_make_overhangs_printable,
                                     "make_overhangs_printable")
        self._register_hover_tooltip(self.make_overhangs_printable_check,
                                     "make_overhangs_printable")
        self.extra_perimeters_on_overhangs_check = QtWidgets.QCheckBox(section)
        self.extra_perimeters_on_overhangs_check.setObjectName("SettingsCheck")
        self.extra_perimeters_on_overhangs_check.setChecked(bool(self._defaults.extra_perimeters_on_overhangs))
        self._label_extra_perimeters = self._add_row(
            "quality", section, section_layout, "Extra perimeters on overhangs",
            self.extra_perimeters_on_overhangs_check,
            "Add extra perimeters on overhang layers.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_extra_perimeters,
                                     "extra_perimeters_on_overhangs")
        self._register_hover_tooltip(self.extra_perimeters_on_overhangs_check,
                                     "extra_perimeters_on_overhangs")
        self.reverse_overhang_on_odd_check = QtWidgets.QCheckBox(section)
        self.reverse_overhang_on_odd_check.setObjectName("SettingsCheck")
        self.reverse_overhang_on_odd_check.setChecked(bool(self._defaults.reverse_overhang_on_odd))
        self._label_reverse_overhang = self._add_row(
            "quality", section, section_layout, "Reverse on odd",
            self.reverse_overhang_on_odd_check,
            "Reverse wall direction on odd overhang layers.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_reverse_overhang, "reverse_overhang_on_odd")
        self._register_hover_tooltip(self.reverse_overhang_on_odd_check,
                                     "reverse_overhang_on_odd")
        self.overhang_optimization_check = QtWidgets.QCheckBox(section)
        self.overhang_optimization_check.setObjectName("SettingsCheck")
        self.overhang_optimization_check.setChecked(bool(self._defaults.overhang_optimization))
        self._label_overhang_optimization = self._add_row(
            "quality", section, section_layout, "Overhang optimization (beta)",
            self.overhang_optimization_check,
            "Use adaptive settings for overhangs.",
            use_native_tooltip=False,
        )
        self._register_hover_tooltip(self._label_overhang_optimization, "overhang_optimization")
        self._register_hover_tooltip(self.overhang_optimization_check, "overhang_optimization")
        layout.insertWidget(layout.count() - 1, section)

