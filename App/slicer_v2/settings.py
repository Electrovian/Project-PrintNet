from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

from .errors import SlicerV2SettingsNormalizationError


DEFAULT_SETTINGS: dict[str, object] = {
    "layer_height": 0.2,
    "model_height_mm": 20.0,
    "parity_fff_strict_mode": False,
    "perimeter_mode": "classic",
    "perimeter_count": 2,
    "wall_sequence": "outer_to_inner",
    "first_layer_single_wall": False,
    "variable_line_width_min": 0.3,
    "variable_line_width_max": 0.5,
    "arachne_transition_smoothing": 0.35,
    "arachne_junction_compensation_enabled": True,
    "arachne_junction_sharp_angle_deg": 120.0,
    "arachne_carryover_cross_island_enabled": False,
    "arachne_carryover_strength": -1.0,
    "infill_percent": 15.0,
    "infill_wall_overlap_percent": 15.0,
    "top_bottom_infill_wall_overlap_percent": 15.0,
    "infill_pattern": "rectilinear",
    "infill_angle_start": 45.0,
    "infill_angle_step": 90.0,
    "infill_angle_template": "",
    "infill_anchor": 0.0,
    "infill_anchor_max": 1000.0,
    "infill_combination_enabled": False,
    "infill_combination_max_layer_height_mm": 0.0,
    "infill_antivibration_enabled": True,
    "infill_antivibration_short_line_threshold_mm": 4.0,
    "infill_antivibration_max_skips_allowed": 2,
    "infill_antivibration_min_depth_for_line_removing": 5,
    "support_enabled": False,
    "support_type": "normal",
    "support_style": "pillars",
    "support_density_percent": 15.0,
    "support_spacing_mm": 2.5,
    "support_base_spacing_mm": 2.5,
    "support_interface_spacing_mm": 2.5,
    "support_bottom_interface_spacing_mm": 2.5,
    "support_xy_gap_mm": 0.25,
    "support_z_gap_mm": 0.2,
    "support_bottom_z_gap_mm": 0.2,
    "support_build_plate_only": False,
    "support_threshold_angle_deg": 45.0,
    "support_threshold_overlap_percent": 0.0,
    "support_critical_regions_only": False,
    "support_remove_small_overhang": False,
    "support_interface_layers": 2,
    "support_interface_top_layers": 2,
    "support_interface_bottom_layers": 0,
    "tree_support_branch_angle_deg": 45.0,
    "tree_support_wall_count": 1,
    "tree_support_branch_diameter_mm": 0.6,
    "tree_support_tip_diameter_mm": 0.3,
    "tree_support_branch_distance_mm": 2.0,
    "tree_support_branch_distance_organic_mm": 2.5,
    "tree_support_top_rate_percent": 30.0,
    "tree_support_branch_diameter_angle_deg": 5.0,
    "tree_support_branch_angle_organic_deg": 35.0,
    "tree_support_branch_diameter_organic_mm": 0.7,
    "tree_support_auto_brim": False,
    "tree_support_brim_width_mm": 0.0,
    "tree_support_branch_merge_distance_ratio": 1.2,
    "tree_support_branch_growth_ratio": 1.08,
    "tree_support_min_branch_radius_mm": 0.3,
    "tree_support_parent_weight_route": 0.56,
    "tree_support_parent_weight_load": 0.40,
    "tree_support_parent_root_bonus": 0.06,
    "tree_support_trunk_root_bonus": 0.08,
    "tree_support_trunk_depth_bonus": 0.07,
    "tree_support_strict_parity_mode": False,
    "travel_speed": 150.0,
    "travel_combing_enabled": True,
    "travel_combing_max_detour_ratio": 1.5,
    "travel_retract_enabled": True,
    "travel_retract_min_travel_mm": 2.0,
    "travel_z_hop_enabled": False,
    "travel_z_hop_mm": 0.2,
    "print_speed": 60.0,
    "flow_multiplier": 1.0,
    "perimeter_flow_ratio": 1.0,
    "infill_flow_ratio": 1.0,
    "support_flow_ratio": 1.0,
    "solid_flow_ratio": 1.0,
    "bridge_enabled": True,
    "bridge_flow_ratio": 1.0,
    "bridge_speed_ratio": 0.8,
    "bridge_density_percent": 100.0,
    "internal_bridge_flow_ratio": 1.0,
    "internal_bridge_density_percent": 100.0,
    "internal_bridge_angle_deg": 0.0,
    "thick_bridges": False,
    "thick_internal_bridges": False,
    "extra_bridge_layer_enabled": False,
    "bridge_over_infill_enabled": True,
    "bridge_over_infill_min_candidate_ratio": 0.05,
    "bridge_over_infill_sample_count": 7,
    "bridge_span_strip_geometry_enabled": True,
    "filament_density_g_cm3": 1.24,
    "filament_cost_usd_per_kg": 0.0,
    "small_feature_threshold_mm": 4.0,
    "small_feature_flow_boost_ratio": 1.05,
    "gcode_absolute_extrusion": True,
    "gcode_firmware_flavor": "marlin",
    "gcode_startup_macro": (),
    "gcode_end_macro": (),
    "gcode_retract_length_mm": 0.8,
    "gcode_emit_layer_comments": True,
    "gcode_validation_enabled": True,
    "gcode_validation_strict": False,
    "gcode_validation_bed_x_mm": 220.0,
    "gcode_validation_bed_y_mm": 220.0,
    "gcode_validation_bed_z_mm": 250.0,
    "gcode_validation_require_monotonic_z": True,
    "gcode_validation_require_monotonic_e": True,
    "gcode_validation_allow_absolute_retract": True,
    "gcode_validation_allow_negative_xy": False,
    "gcode_validation_line_length_limit": 512,
    "gcode_validation_max_line_count": 250000,
    "gcode_validation_tolerance_mm": 0.0001,
    "seam_position": "aligned",
    "seam_random_seed": 0,
    "nozzle_diameter": 0.4,
    "filament_diameter": 1.75,
    "extrusion_width": 0.4,
    "top_layers": 3,
    "bottom_layers": 3,
    "brim_width": 0.0,
    "adaptive_layering_enabled": False,
    "adaptive_layer_min": 0.08,
    "adaptive_layer_max": 0.32,
    "adaptive_top_bottom_refine_mm": 0.0,
    "adaptive_layer_ranges": (),
}

KEY_ALIASES: dict[str, str] = {
    "layer_height_mm": "layer_height",
    "model_height": "model_height_mm",
    "part_height_mm": "model_height_mm",
    "fff_strict_mode": "parity_fff_strict_mode",
    "perimeters": "perimeter_count",
    "wall_loops": "perimeter_count",
    "wall_line_count": "perimeter_count",
    "perimeter_strategy": "perimeter_mode",
    "perimeter_generator": "perimeter_mode",
    "wall_sequence_mode": "wall_sequence",
    "single_wall_first_layer": "first_layer_single_wall",
    "line_width_min": "variable_line_width_min",
    "line_width_max": "variable_line_width_max",
    "wall_transition_smoothing": "arachne_transition_smoothing",
    "arachne_smoothing": "arachne_transition_smoothing",
    "junction_compensation": "arachne_junction_compensation_enabled",
    "wall_junction_compensation": "arachne_junction_compensation_enabled",
    "junction_sharp_angle": "arachne_junction_sharp_angle_deg",
    "arachne_carryover_cross_island": "arachne_carryover_cross_island_enabled",
    "arachne_cross_island_carryover": "arachne_carryover_cross_island_enabled",
    "arachne_carry_strength": "arachne_carryover_strength",
    "infill_density": "infill_percent",
    "fill_density": "infill_percent",
    "sparse_infill_density": "infill_percent",
    "infill_overlap": "infill_wall_overlap_percent",
    "infill_wall_overlap": "infill_wall_overlap_percent",
    "top_bottom_infill_wall_overlap": "top_bottom_infill_wall_overlap_percent",
    "sparse_infill_pattern": "infill_pattern",
    "infill_angle": "infill_angle_start",
    "infill_rotation": "infill_angle_start",
    "infill_angle_increment": "infill_angle_step",
    "infill_angle_step_deg": "infill_angle_step",
    "infill_rotate_template": "infill_angle_template",
    "sparse_infill_rotate_template": "infill_angle_template",
    "solid_infill_rotate_template": "infill_angle_template",
    "infill_anchor_length": "infill_anchor",
    "infill_anchor_max_length": "infill_anchor_max",
    "infill_anchor_max_mm": "infill_anchor_max",
    "infill_combination": "infill_combination_enabled",
    "infill_combination_max_layer_height": "infill_combination_max_layer_height_mm",
    "infill_line_filter": "infill_antivibration_enabled",
    "infill_antivibration": "infill_antivibration_enabled",
    "infill_line_filter_max_length": "infill_antivibration_short_line_threshold_mm",
    "infill_antivibration_short_line": "infill_antivibration_short_line_threshold_mm",
    "infill_antivibration_max_skips": "infill_antivibration_max_skips_allowed",
    "infill_antivibration_min_depth": "infill_antivibration_min_depth_for_line_removing",
    "enable_support": "support_enabled",
    "support_enable": "support_enabled",
    "support": "support_enabled",
    "support_style": "support_style",
    "support_structure": "support_style",
    "support_density": "support_density_percent",
    "support_density_pct": "support_density_percent",
    "support_line_spacing": "support_spacing_mm",
    "support_spacing": "support_spacing_mm",
    "support_material_spacing": "support_spacing_mm",
    "support_base_pattern_spacing": "support_base_spacing_mm",
    "support_interface_spacing": "support_interface_spacing_mm",
    "support_bottom_interface_spacing": "support_bottom_interface_spacing_mm",
    "support_material_xy_spacing": "support_xy_gap_mm",
    "support_material_contact_distance": "support_z_gap_mm",
    "support_material_bottom_contact_distance": "support_bottom_z_gap_mm",
    "support_threshold_overlap": "support_threshold_overlap_percent",
    "support_threshold_angle": "support_threshold_angle_deg",
    "support_critical_regions_only": "support_critical_regions_only",
    "support_remove_small_overhang": "support_remove_small_overhang",
    "support_xy_distance": "support_xy_gap_mm",
    "support_xy_gap": "support_xy_gap_mm",
    "support_object_xy_distance": "support_xy_gap_mm",
    "support_z_distance": "support_z_gap_mm",
    "support_z_gap": "support_z_gap_mm",
    "support_contact_z_distance": "support_z_gap_mm",
    "support_top_z_distance": "support_z_gap_mm",
    "support_bottom_z_distance": "support_bottom_z_gap_mm",
    "support_on_build_plate_only": "support_build_plate_only",
    "support_interface_layer_count": "support_interface_layers",
    "support_material_interface_layers": "support_interface_top_layers",
    "support_material_bottom_interface_layers": "support_interface_bottom_layers",
    "interface_layers": "support_interface_layers",
    "tree_branch_merge_distance": "tree_support_branch_merge_distance_ratio",
    "tree_branch_growth": "tree_support_branch_growth_ratio",
    "tree_min_branch_radius": "tree_support_min_branch_radius_mm",
    "tree_branch_angle": "tree_support_branch_angle_deg",
    "support_tree_angle": "tree_support_branch_angle_deg",
    "tree_support_branch_angle": "tree_support_branch_angle_deg",
    "tree_support_branch_angle_organic": "tree_support_branch_angle_organic_deg",
    "support_tree_angle_organic": "tree_support_branch_angle_organic_deg",
    "tree_support_wall_count": "tree_support_wall_count",
    "support_tree_branch_distance": "tree_support_branch_distance_mm",
    "tree_support_branch_distance": "tree_support_branch_distance_mm",
    "tree_support_branch_distance_organic": "tree_support_branch_distance_organic_mm",
    "support_tree_branch_distance_organic": "tree_support_branch_distance_organic_mm",
    "support_tree_top_rate": "tree_support_top_rate_percent",
    "tree_support_top_rate": "tree_support_top_rate_percent",
    "support_tree_branch_diameter_angle": "tree_support_branch_diameter_angle_deg",
    "tree_support_branch_diameter_angle": "tree_support_branch_diameter_angle_deg",
    "tree_support_branch_diameter": "tree_support_branch_diameter_mm",
    "tree_support_branch_diameter_organic": "tree_support_branch_diameter_organic_mm",
    "support_tree_branch_diameter_organic": "tree_support_branch_diameter_organic_mm",
    "tree_support_tip_diameter": "tree_support_tip_diameter_mm",
    "tree_support_auto_brim": "tree_support_auto_brim",
    "tree_support_brim_width": "tree_support_brim_width_mm",
    "tree_parent_weight_route": "tree_support_parent_weight_route",
    "tree_parent_weight_load": "tree_support_parent_weight_load",
    "tree_parent_root_bonus": "tree_support_parent_root_bonus",
    "tree_trunk_root_bonus": "tree_support_trunk_root_bonus",
    "tree_trunk_depth_bonus": "tree_support_trunk_depth_bonus",
    "tree_support_strict_parity": "tree_support_strict_parity_mode",
    "travel_speed_mm_s": "travel_speed",
    "combing": "travel_combing_enabled",
    "avoid_crossing_walls": "travel_combing_enabled",
    "travel_combing": "travel_combing_enabled",
    "combing_max_detour_ratio": "travel_combing_max_detour_ratio",
    "travel_combing_detour_ratio": "travel_combing_max_detour_ratio",
    "retraction_enable": "travel_retract_enabled",
    "travel_retract": "travel_retract_enabled",
    "retract_min_travel": "travel_retract_min_travel_mm",
    "travel_retract_min": "travel_retract_min_travel_mm",
    "z_hop_enable": "travel_z_hop_enabled",
    "travel_zhop_enable": "travel_z_hop_enabled",
    "z_hop_height": "travel_z_hop_mm",
    "travel_zhop_mm": "travel_z_hop_mm",
    "default_speed": "print_speed",
    "outer_wall_speed": "print_speed",
    "flow": "flow_multiplier",
    "flow_ratio": "flow_multiplier",
    "extrusion_flow_multiplier": "flow_multiplier",
    "wall_flow": "perimeter_flow_ratio",
    "perimeter_flow": "perimeter_flow_ratio",
    "infill_flow": "infill_flow_ratio",
    "support_flow": "support_flow_ratio",
    "solid_flow": "solid_flow_ratio",
    "enable_bridge": "bridge_enabled",
    "bridge_flow": "bridge_flow_ratio",
    "bridge_flow_multiplier": "bridge_flow_ratio",
    "bridge_speed": "bridge_speed_ratio",
    "bridge_speed_multiplier": "bridge_speed_ratio",
    "bridge_density": "bridge_density_percent",
    "internal_bridge_flow": "internal_bridge_flow_ratio",
    "internal_bridge_density": "internal_bridge_density_percent",
    "internal_bridge_angle": "internal_bridge_angle_deg",
    "thick_bridge": "thick_bridges",
    "thick_internal_bridge": "thick_internal_bridges",
    "enable_extra_bridge_layer": "extra_bridge_layer_enabled",
    "bridge_over_infill": "bridge_over_infill_enabled",
    "bridge_over_sparse_infill": "bridge_over_infill_enabled",
    "bridge_over_infill_min_ratio": "bridge_over_infill_min_candidate_ratio",
    "bridge_over_infill_min_candidate": "bridge_over_infill_min_candidate_ratio",
    "bridge_over_infill_samples": "bridge_over_infill_sample_count",
    "bridge_strip_geometry": "bridge_span_strip_geometry_enabled",
    "filament_density": "filament_density_g_cm3",
    "material_density": "filament_density_g_cm3",
    "filament_cost": "filament_cost_usd_per_kg",
    "filament_cost_per_kg": "filament_cost_usd_per_kg",
    "material_cost_per_kg": "filament_cost_usd_per_kg",
    "small_feature_threshold": "small_feature_threshold_mm",
    "small_feature_flow_boost": "small_feature_flow_boost_ratio",
    "small_feature_flow_boost_ratio": "small_feature_flow_boost_ratio",
    "seam_seed": "seam_random_seed",
    "absolute_extrusion": "gcode_absolute_extrusion",
    "gcode_absolute_e": "gcode_absolute_extrusion",
    "gcode_firmware": "gcode_firmware_flavor",
    "firmware_flavor": "gcode_firmware_flavor",
    "start_gcode": "gcode_startup_macro",
    "startup_gcode": "gcode_startup_macro",
    "end_gcode": "gcode_end_macro",
    "shutdown_gcode": "gcode_end_macro",
    "retract_length": "gcode_retract_length_mm",
    "gcode_retract_length": "gcode_retract_length_mm",
    "emit_layer_comments": "gcode_emit_layer_comments",
    "gcode_layer_comments": "gcode_emit_layer_comments",
    "gcode_validate_enabled": "gcode_validation_enabled",
    "gcode_validate_strict": "gcode_validation_strict",
    "gcode_validation_strict_mode": "gcode_validation_strict",
    "bed_x": "gcode_validation_bed_x_mm",
    "bed_y": "gcode_validation_bed_y_mm",
    "bed_z": "gcode_validation_bed_z_mm",
    "build_volume_x": "gcode_validation_bed_x_mm",
    "build_volume_y": "gcode_validation_bed_y_mm",
    "build_volume_z": "gcode_validation_bed_z_mm",
    "validation_require_monotonic_z": "gcode_validation_require_monotonic_z",
    "validation_require_monotonic_e": "gcode_validation_require_monotonic_e",
    "validation_allow_absolute_retract": "gcode_validation_allow_absolute_retract",
    "validation_allow_negative_xy": "gcode_validation_allow_negative_xy",
    "gcode_validation_line_limit": "gcode_validation_max_line_count",
    "gcode_validation_max_lines": "gcode_validation_max_line_count",
    "gcode_validation_line_length": "gcode_validation_line_length_limit",
    "gcode_validation_tolerance": "gcode_validation_tolerance_mm",
    "default_nozzle_diameter": "nozzle_diameter",
    "nozzle_size": "nozzle_diameter",
    "filament_size": "filament_diameter",
    "line_width": "extrusion_width",
    "default_line_width": "extrusion_width",
    "top_shell_layers": "top_layers",
    "bottom_shell_layers": "bottom_layers",
    "adaptive_layering": "adaptive_layering_enabled",
    "adaptive_layers": "adaptive_layering_enabled",
    "adaptive_enable": "adaptive_layering_enabled",
    "adaptive_layering_enable": "adaptive_layering_enabled",
    "adaptive_layer_min_mm": "adaptive_layer_min",
    "adaptive_layer_max_mm": "adaptive_layer_max",
    "adaptive_refine_mm": "adaptive_top_bottom_refine_mm",
    "adaptive_layer_ranges_mm": "adaptive_layer_ranges",
}

BOOL_TRUE_VALUES = {"1", "true", "yes", "on", "enabled"}
BOOL_FALSE_VALUES = {"0", "false", "no", "off", "disabled"}

INFILL_PATTERN_ALIASES = {
    "rectilinear": "rectilinear",
    "lines": "rectilinear",
    "grid": "grid",
    "gyroid": "gyroid",
    "triangle": "triangle",
    "triangles": "triangle",
    "adaptive_cubic": "adaptive_cubic",
    "adaptive": "adaptive_cubic",
    "support_cubic": "support_cubic",
    "lightning": "lightning",
    "concentric": "concentric",
    "honeycomb": "honeycomb",
    "3dhoneycomb": "3d_honeycomb",
    "3d_honeycomb": "3d_honeycomb",
    "cross_hatch": "cross_hatch",
    "crosshatch": "cross_hatch",
    "tpms_d": "tpms_d",
    "tpmsd": "tpms_d",
    "tpms_f_k": "tpms_f_k",
    "tpms_fk": "tpms_f_k",
}

SUPPORT_TYPE_ALIASES = {
    "normal": "normal",
    "default": "normal",
    "tree": "tree",
    "organic": "tree",
}

SUPPORT_STYLE_ALIASES = {
    "default": "pillars",
    "normal": "pillars",
    "pillars": "pillars",
    "tree": "tree",
    "organic": "organic",
}

SEAM_POSITION_ALIASES = {
    "nearest": "nearest",
    "aligned": "aligned",
    "rear": "rear",
    "back": "rear",
    "random": "random",
}

PERIMETER_MODE_ALIASES = {
    "classic": "classic",
    "default": "classic",
    "variable_width": "variable_width",
    "variable-width": "variable_width",
    "variable": "variable_width",
    "arachne": "variable_width",
    "arachne_like": "variable_width",
}

WALL_SEQUENCE_ALIASES = {
    "outer_to_inner": "outer_to_inner",
    "outer-inner": "outer_to_inner",
    "inner_to_outer": "inner_to_outer",
    "inner-outer": "inner_to_outer",
}

GCODE_FIRMWARE_ALIASES = {
    "marlin": "marlin",
    "klipper": "klipper",
    "prusalink": "prusalink",
    "generic": "generic",
}


@dataclass
class SettingsNormalizationReport:
    normalized_at_utc: str
    input_key_count: int
    output_key_count: int
    alias_applied_count: int
    coerced_value_count: int
    clamped_value_count: int
    unknown_key_count: int
    warning_count: int
    warnings: list[str] = field(default_factory=list)
    unknown_keys: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


class _NormalizationState:
    def __init__(self) -> None:
        self.alias_applied_count = 0
        self.coerced_value_count = 0
        self.clamped_value_count = 0
        self.warnings: list[str] = []
        self.unknown_keys: list[str] = []

    def add_warning(self, key: str, code: str, value: object) -> None:
        self.warnings.append(f"{key}:{code}:{value}")


_PERCENT_REFERENCE_DISTANCE_KEYS = frozenset(
    {
        "support_spacing_mm",
        "support_base_spacing_mm",
        "support_interface_spacing_mm",
        "support_bottom_interface_spacing_mm",
        "support_xy_gap_mm",
        "support_z_gap_mm",
        "support_bottom_z_gap_mm",
        "tree_support_branch_diameter_mm",
        "tree_support_branch_diameter_organic_mm",
        "tree_support_tip_diameter_mm",
        "tree_support_branch_distance_mm",
        "tree_support_branch_distance_organic_mm",
        "tree_support_brim_width_mm",
    }
)


def _is_percent_literal(value: object) -> bool:
    if not isinstance(value, (str, bytes, bytearray)):
        return False
    return str(value).strip().endswith("%")


def _coerce_float(value: object, fallback: float) -> float:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text:
        return fallback
    if text.endswith("%"):
        text = text[:-1].strip()
    try:
        return float(text)
    except (TypeError, ValueError):
        return fallback


def _parse_float(value: object, *, key: str, state: _NormalizationState) -> float | None:
    if isinstance(value, bool):
        state.add_warning(key, "invalid_float", value)
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text:
        state.add_warning(key, "invalid_float", value)
        return None
    if text.endswith("%"):
        text = text[:-1].strip()
        state.coerced_value_count += 1
    try:
        parsed = float(text)
    except (TypeError, ValueError):
        state.add_warning(key, "invalid_float", value)
        return None
    state.coerced_value_count += 1
    return parsed


def _normalize_length_or_percent(
    value: object,
    *,
    key: str,
    state: _NormalizationState,
    default: object,
    minimum: float,
    maximum: float,
) -> object:
    if isinstance(value, (str, bytes, bytearray)):
        text = str(value).strip()
        if text.endswith("%"):
            number_text = text[:-1].strip()
            parsed = _parse_float(number_text, key=key, state=state)
            if parsed is None:
                return default
            clamped = _clamp_float(parsed, minimum=minimum, maximum=maximum, state=state)
            return f"{clamped:g}%"
    parsed = _parse_float(value, key=key, state=state)
    if parsed is None:
        return default
    return _clamp_float(parsed, minimum=minimum, maximum=maximum, state=state)


def _normalize_float_or_percent_distance(
    value: object,
    *,
    key: str,
    state: _NormalizationState,
    default: object,
    minimum: float,
    maximum: float,
    reference_mm: float,
) -> float:
    if isinstance(value, (str, bytes, bytearray)):
        text = str(value).strip()
        if text.endswith("%"):
            number_text = text[:-1].strip()
            parsed_pct = _parse_float(number_text, key=key, state=state)
            if parsed_pct is None:
                return float(default)
            parsed = max(0.0, float(reference_mm)) * (parsed_pct * 0.01)
            state.coerced_value_count += 1
            return _clamp_float(parsed, minimum=minimum, maximum=maximum, state=state)

    parsed = _parse_float(value, key=key, state=state)
    if parsed is None:
        return float(default)
    return _clamp_float(parsed, minimum=minimum, maximum=maximum, state=state)


def _parse_int(value: object, *, key: str, state: _NormalizationState) -> int | None:
    if isinstance(value, bool):
        state.add_warning(key, "invalid_int", value)
        return None
    if isinstance(value, int):
        return value
    parsed_float = _parse_float(value, key=key, state=state)
    if parsed_float is None:
        return None
    rounded = int(round(parsed_float))
    return rounded


def _parse_bool(value: object, *, key: str, state: _NormalizationState) -> bool | None:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in BOOL_TRUE_VALUES:
        state.coerced_value_count += 1
        return True
    if text in BOOL_FALSE_VALUES:
        state.coerced_value_count += 1
        return False
    state.add_warning(key, "invalid_bool", value)
    return None


def _clamp_float(value: float, *, minimum: float, maximum: float, state: _NormalizationState) -> float:
    clamped = max(minimum, min(maximum, value))
    if clamped != value:
        state.clamped_value_count += 1
    return clamped


def _clamp_int(value: int, *, minimum: int, maximum: int, state: _NormalizationState) -> int:
    clamped = max(minimum, min(maximum, value))
    if clamped != value:
        state.clamped_value_count += 1
    return clamped


def _normalize_percent(value: object, *, key: str, state: _NormalizationState, default: float) -> float:
    parsed = _parse_float(value, key=key, state=state)
    if parsed is None:
        return default
    if 0.0 <= parsed <= 1.0:
        parsed = parsed * 100.0
        state.coerced_value_count += 1
    return _clamp_float(parsed, minimum=0.0, maximum=100.0, state=state)


def _normalize_choice(
    value: object,
    *,
    key: str,
    allowed_aliases: dict[str, str],
    default: str,
    state: _NormalizationState,
) -> str:
    text = str(value).strip().lower()
    if not text:
        state.add_warning(key, "empty_choice", value)
        return default
    if text in allowed_aliases:
        normalized = allowed_aliases[text]
        if normalized != text:
            state.coerced_value_count += 1
        return normalized
    state.add_warning(key, "invalid_choice", value)
    return default


def _normalize_layer_ranges(value: object, *, key: str, state: _NormalizationState) -> tuple[dict[str, float], ...]:
    parsed_value = value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return ()
        try:
            parsed_value = json.loads(text)
            state.coerced_value_count += 1
        except (TypeError, ValueError):
            state.add_warning(key, "invalid_json", value)
            return ()

    if isinstance(parsed_value, tuple):
        parsed_value = list(parsed_value)
    if not isinstance(parsed_value, list):
        state.add_warning(key, "invalid_range_list", value)
        return ()

    normalized_ranges: list[dict[str, float]] = []
    for index, entry in enumerate(parsed_value):
        scoped_key = f"{key}[{index}]"
        if not isinstance(entry, dict):
            state.add_warning(scoped_key, "invalid_range_entry", entry)
            continue

        z_min_raw = entry.get("z_min_mm", entry.get("z_min", entry.get("start")))
        z_max_raw = entry.get("z_max_mm", entry.get("z_max", entry.get("end")))
        height_raw = entry.get("layer_height_mm", entry.get("layer_height", entry.get("height")))

        if z_min_raw is None or z_max_raw is None or height_raw is None:
            state.add_warning(scoped_key, "missing_range_fields", entry)
            continue

        z_min = _parse_float(z_min_raw, key=f"{scoped_key}.z_min", state=state)
        z_max = _parse_float(z_max_raw, key=f"{scoped_key}.z_max", state=state)
        layer_height = _parse_float(height_raw, key=f"{scoped_key}.layer_height", state=state)
        if z_min is None or z_max is None or layer_height is None:
            state.add_warning(scoped_key, "invalid_range_values", entry)
            continue
        if z_max <= z_min:
            state.add_warning(scoped_key, "invalid_range_window", entry)
            continue

        normalized_ranges.append(
            {
                "z_min_mm": z_min,
                "z_max_mm": z_max,
                "layer_height_mm": _clamp_float(layer_height, minimum=0.02, maximum=1.0, state=state),
            }
        )

    return tuple(normalized_ranges)


def _normalize_string_lines(value: object, *, key: str, state: _NormalizationState) -> tuple[str, ...]:
    if value is None:
        return ()

    raw_lines: list[str] | list[object]
    if isinstance(value, str):
        raw_lines = value.splitlines()
        if "\n" in value or "\r" in value:
            state.coerced_value_count += 1
    elif isinstance(value, tuple):
        raw_lines = list(value)
    elif isinstance(value, list):
        raw_lines = value
    else:
        state.add_warning(key, "invalid_string_lines", value)
        return ()

    lines: list[str] = []
    for index, item in enumerate(raw_lines):
        text = str(item).strip()
        if not text:
            continue
        if "\n" in text or "\r" in text:
            state.add_warning(f"{key}[{index}]", "embedded_newline", text)
            continue
        lines.append(text)

    if len(lines) > 200:
        state.add_warning(key, "string_lines_truncated", len(lines))
        lines = lines[:200]
    return tuple(lines)


def _normalize_known_value(
    key: str,
    value: object,
    state: _NormalizationState,
    *,
    reference_mm: float,
) -> object:
    defaults = DEFAULT_SETTINGS
    if key == "perimeter_mode":
        return _normalize_choice(
            value,
            key=key,
            allowed_aliases=PERIMETER_MODE_ALIASES,
            default=str(defaults[key]),
            state=state,
        )
    if key == "layer_height":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.01, maximum=1.0, state=state)
    if key == "model_height_mm":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.1, maximum=10000.0, state=state)
    if key == "parity_fff_strict_mode":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "perimeter_count":
        parsed = _parse_int(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_int(parsed, minimum=1, maximum=20, state=state)
    if key == "wall_sequence":
        return _normalize_choice(
            value,
            key=key,
            allowed_aliases=WALL_SEQUENCE_ALIASES,
            default=str(defaults[key]),
            state=state,
        )
    if key == "first_layer_single_wall":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "variable_line_width_min":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.1, maximum=2.0, state=state)
    if key == "variable_line_width_max":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.1, maximum=2.0, state=state)
    if key == "arachne_transition_smoothing":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=1.0, state=state)
    if key == "arachne_junction_compensation_enabled":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "arachne_junction_sharp_angle_deg":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=30.0, maximum=175.0, state=state)
    if key == "arachne_carryover_cross_island_enabled":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "arachne_carryover_strength":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        if parsed < 0.0:
            return -1.0
        return _clamp_float(parsed, minimum=0.0, maximum=1.5, state=state)
    if key == "infill_percent":
        return _normalize_percent(value, key=key, state=state, default=_coerce_float(defaults[key], 15.0))
    if key == "infill_wall_overlap_percent":
        return _normalize_percent(value, key=key, state=state, default=_coerce_float(defaults[key], 15.0))
    if key == "top_bottom_infill_wall_overlap_percent":
        return _normalize_percent(value, key=key, state=state, default=_coerce_float(defaults[key], 15.0))
    if key == "infill_pattern":
        return _normalize_choice(
            value,
            key=key,
            allowed_aliases=INFILL_PATTERN_ALIASES,
            default=str(defaults[key]),
            state=state,
        )
    if key == "infill_angle_start":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=-360.0, maximum=360.0, state=state)
    if key == "infill_angle_step":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=-360.0, maximum=360.0, state=state)
    if key == "infill_angle_template":
        text = str(value or "").strip()
        if len(text) > 4096:
            state.add_warning(key, "template_truncated", len(text))
            text = text[:4096]
        return text
    if key == "infill_anchor":
        return _normalize_length_or_percent(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.0,
            maximum=2000.0,
        )
    if key == "infill_anchor_max":
        return _normalize_length_or_percent(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.0,
            maximum=5000.0,
        )
    if key == "infill_combination_enabled":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "infill_combination_max_layer_height_mm":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=10.0, state=state)
    if key == "infill_antivibration_enabled":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "infill_antivibration_short_line_threshold_mm":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.1, maximum=100.0, state=state)
    if key == "infill_antivibration_max_skips_allowed":
        parsed = _parse_int(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_int(parsed, minimum=0, maximum=16, state=state)
    if key == "infill_antivibration_min_depth_for_line_removing":
        parsed = _parse_int(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_int(parsed, minimum=1, maximum=64, state=state)
    if key == "support_enabled":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "support_type":
        return _normalize_choice(
            value,
            key=key,
            allowed_aliases=SUPPORT_TYPE_ALIASES,
            default=str(defaults[key]),
            state=state,
        )
    if key == "support_style":
        return _normalize_choice(
            value,
            key=key,
            allowed_aliases=SUPPORT_STYLE_ALIASES,
            default=str(defaults[key]),
            state=state,
        )
    if key == "support_density_percent":
        return _normalize_percent(value, key=key, state=state, default=_coerce_float(defaults[key], 15.0))
    if key == "support_spacing_mm":
        return _normalize_float_or_percent_distance(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.1,
            maximum=20.0,
            reference_mm=reference_mm,
        )
    if key == "support_base_spacing_mm":
        return _normalize_float_or_percent_distance(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.1,
            maximum=20.0,
            reference_mm=reference_mm,
        )
    if key == "support_interface_spacing_mm":
        return _normalize_float_or_percent_distance(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.1,
            maximum=20.0,
            reference_mm=reference_mm,
        )
    if key == "support_bottom_interface_spacing_mm":
        return _normalize_float_or_percent_distance(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.1,
            maximum=20.0,
            reference_mm=reference_mm,
        )
    if key == "support_xy_gap_mm":
        return _normalize_float_or_percent_distance(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.0,
            maximum=5.0,
            reference_mm=reference_mm,
        )
    if key == "support_z_gap_mm":
        return _normalize_float_or_percent_distance(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.0,
            maximum=3.0,
            reference_mm=reference_mm,
        )
    if key == "support_bottom_z_gap_mm":
        return _normalize_float_or_percent_distance(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.0,
            maximum=3.0,
            reference_mm=reference_mm,
        )
    if key == "support_build_plate_only":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "support_threshold_angle_deg":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=1.0, maximum=89.0, state=state)
    if key == "support_threshold_overlap_percent":
        return _normalize_percent(value, key=key, state=state, default=_coerce_float(defaults[key], 0.0))
    if key == "support_critical_regions_only":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "support_remove_small_overhang":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "support_interface_layers":
        parsed = _parse_int(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_int(parsed, minimum=0, maximum=20, state=state)
    if key == "support_interface_top_layers":
        parsed = _parse_int(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_int(parsed, minimum=0, maximum=20, state=state)
    if key == "support_interface_bottom_layers":
        parsed = _parse_int(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_int(parsed, minimum=-1, maximum=20, state=state)
    if key == "tree_support_branch_angle_deg":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=85.0, state=state)
    if key == "tree_support_wall_count":
        parsed = _parse_int(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_int(parsed, minimum=0, maximum=8, state=state)
    if key == "tree_support_branch_diameter_mm":
        return _normalize_float_or_percent_distance(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.05,
            maximum=20.0,
            reference_mm=reference_mm,
        )
    if key == "tree_support_tip_diameter_mm":
        return _normalize_float_or_percent_distance(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.05,
            maximum=20.0,
            reference_mm=reference_mm,
        )
    if key == "tree_support_branch_distance_mm":
        return _normalize_float_or_percent_distance(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.05,
            maximum=60.0,
            reference_mm=reference_mm,
        )
    if key == "tree_support_branch_distance_organic_mm":
        return _normalize_float_or_percent_distance(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.05,
            maximum=60.0,
            reference_mm=reference_mm,
        )
    if key == "tree_support_top_rate_percent":
        return _normalize_percent(value, key=key, state=state, default=_coerce_float(defaults[key], 30.0))
    if key == "tree_support_branch_diameter_angle_deg":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=89.0, state=state)
    if key == "tree_support_branch_angle_organic_deg":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=85.0, state=state)
    if key == "tree_support_branch_diameter_organic_mm":
        return _normalize_float_or_percent_distance(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.05,
            maximum=20.0,
            reference_mm=reference_mm,
        )
    if key == "tree_support_auto_brim":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "tree_support_brim_width_mm":
        return _normalize_float_or_percent_distance(
            value,
            key=key,
            state=state,
            default=defaults[key],
            minimum=0.0,
            maximum=30.0,
            reference_mm=reference_mm,
        )
    if key == "tree_support_branch_merge_distance_ratio":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.5, maximum=4.0, state=state)
    if key == "tree_support_branch_growth_ratio":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=1.0, maximum=2.0, state=state)
    if key == "tree_support_min_branch_radius_mm":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.05, maximum=10.0, state=state)
    if key == "tree_support_parent_weight_route":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=2.0, state=state)
    if key == "tree_support_parent_weight_load":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=2.0, state=state)
    if key == "tree_support_parent_root_bonus":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=1.0, state=state)
    if key == "tree_support_trunk_root_bonus":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=1.0, state=state)
    if key == "tree_support_trunk_depth_bonus":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=1.0, state=state)
    if key == "tree_support_strict_parity_mode":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "travel_speed":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=1.0, maximum=1000.0, state=state)
    if key == "travel_combing_enabled":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "travel_combing_max_detour_ratio":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=1.0, maximum=5.0, state=state)
    if key == "travel_retract_enabled":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "travel_retract_min_travel_mm":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=50.0, state=state)
    if key == "travel_z_hop_enabled":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "travel_z_hop_mm":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=10.0, state=state)
    if key == "print_speed":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=1.0, maximum=600.0, state=state)
    if key == "flow_multiplier":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.1, maximum=3.0, state=state)
    if key == "perimeter_flow_ratio":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.1, maximum=3.0, state=state)
    if key == "infill_flow_ratio":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.1, maximum=3.0, state=state)
    if key == "support_flow_ratio":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.1, maximum=3.0, state=state)
    if key == "solid_flow_ratio":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.1, maximum=3.0, state=state)
    if key == "bridge_enabled":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "bridge_flow_ratio":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.2, maximum=3.0, state=state)
    if key == "bridge_speed_ratio":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.1, maximum=3.0, state=state)
    if key == "bridge_density_percent":
        return _normalize_percent(value, key=key, state=state, default=_coerce_float(defaults[key], 100.0))
    if key == "internal_bridge_flow_ratio":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.2, maximum=3.0, state=state)
    if key == "internal_bridge_density_percent":
        return _normalize_percent(value, key=key, state=state, default=_coerce_float(defaults[key], 100.0))
    if key == "internal_bridge_angle_deg":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=360.0, state=state)
    if key == "thick_bridges":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "thick_internal_bridges":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "extra_bridge_layer_enabled":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "bridge_over_infill_enabled":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "bridge_over_infill_min_candidate_ratio":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=1.0, state=state)
    if key == "bridge_over_infill_sample_count":
        parsed = _parse_int(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_int(parsed, minimum=1, maximum=128, state=state)
    if key == "bridge_span_strip_geometry_enabled":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "filament_density_g_cm3":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=10.0, state=state)
    if key == "filament_cost_usd_per_kg":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=1000.0, state=state)
    if key == "small_feature_threshold_mm":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=100.0, state=state)
    if key == "small_feature_flow_boost_ratio":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=1.0, maximum=2.0, state=state)
    if key == "gcode_absolute_extrusion":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "gcode_firmware_flavor":
        return _normalize_choice(
            value,
            key=key,
            allowed_aliases=GCODE_FIRMWARE_ALIASES,
            default=str(defaults[key]),
            state=state,
        )
    if key == "gcode_startup_macro":
        return _normalize_string_lines(value, key=key, state=state)
    if key == "gcode_end_macro":
        return _normalize_string_lines(value, key=key, state=state)
    if key == "gcode_retract_length_mm":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=20.0, state=state)
    if key == "gcode_emit_layer_comments":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "gcode_validation_enabled":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "gcode_validation_strict":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "gcode_validation_bed_x_mm":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=1.0, maximum=10000.0, state=state)
    if key == "gcode_validation_bed_y_mm":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=1.0, maximum=10000.0, state=state)
    if key == "gcode_validation_bed_z_mm":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=1.0, maximum=10000.0, state=state)
    if key == "gcode_validation_require_monotonic_z":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "gcode_validation_require_monotonic_e":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "gcode_validation_allow_absolute_retract":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "gcode_validation_allow_negative_xy":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "gcode_validation_line_length_limit":
        parsed = _parse_int(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_int(parsed, minimum=32, maximum=4096, state=state)
    if key == "gcode_validation_max_line_count":
        parsed = _parse_int(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_int(parsed, minimum=1, maximum=2000000, state=state)
    if key == "gcode_validation_tolerance_mm":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=1.0, state=state)
    if key == "seam_position":
        return _normalize_choice(
            value,
            key=key,
            allowed_aliases=SEAM_POSITION_ALIASES,
            default=str(defaults[key]),
            state=state,
        )
    if key == "seam_random_seed":
        parsed = _parse_int(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_int(parsed, minimum=0, maximum=2_147_483_647, state=state)
    if key == "nozzle_diameter":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.1, maximum=2.0, state=state)
    if key == "filament_diameter":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=1.0, maximum=5.0, state=state)
    if key == "extrusion_width":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.1, maximum=2.0, state=state)
    if key == "top_layers":
        parsed = _parse_int(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_int(parsed, minimum=0, maximum=50, state=state)
    if key == "bottom_layers":
        parsed = _parse_int(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_int(parsed, minimum=0, maximum=50, state=state)
    if key == "brim_width":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=20.0, state=state)
    if key == "adaptive_layering_enabled":
        parsed_bool = _parse_bool(value, key=key, state=state)
        if parsed_bool is None:
            return defaults[key]
        return parsed_bool
    if key == "adaptive_layer_min":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.02, maximum=1.0, state=state)
    if key == "adaptive_layer_max":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.02, maximum=1.0, state=state)
    if key == "adaptive_top_bottom_refine_mm":
        parsed = _parse_float(value, key=key, state=state)
        if parsed is None:
            return defaults[key]
        return _clamp_float(parsed, minimum=0.0, maximum=25.0, state=state)
    if key == "adaptive_layer_ranges":
        return _normalize_layer_ranges(value, key=key, state=state)
    return value


def normalize_settings_with_report(
    raw_settings: dict[str, object] | None,
    *,
    strict: bool = False,
    keep_unknown_keys: bool = True,
) -> tuple[dict[str, object], SettingsNormalizationReport]:
    if raw_settings is None:
        raw_settings = {}
    if not isinstance(raw_settings, dict):
        raise SlicerV2SettingsNormalizationError("SETTINGS_PAYLOAD_NOT_DICT")

    normalized = dict(DEFAULT_SETTINGS)
    state = _NormalizationState()
    known_keys = set(DEFAULT_SETTINGS.keys())
    provided_known_keys: set[str] = set()
    deferred_percent_distance_values: dict[str, object] = {}

    for raw_key, raw_value in raw_settings.items():
        text_key = str(raw_key).strip()
        canonical_key = KEY_ALIASES.get(text_key, text_key)
        if canonical_key != text_key:
            state.alias_applied_count += 1
        if canonical_key in known_keys:
            provided_known_keys.add(canonical_key)
            if canonical_key in _PERCENT_REFERENCE_DISTANCE_KEYS and _is_percent_literal(raw_value):
                deferred_percent_distance_values[canonical_key] = raw_value
                continue
            deferred_percent_distance_values.pop(canonical_key, None)
            reference_mm = _coerce_float(
                normalized.get("extrusion_width", DEFAULT_SETTINGS["extrusion_width"]),
                _coerce_float(DEFAULT_SETTINGS["extrusion_width"], 0.4),
            )
            normalized[canonical_key] = _normalize_known_value(
                canonical_key,
                raw_value,
                state,
                reference_mm=reference_mm,
            )
        else:
            state.unknown_keys.append(text_key)
            if keep_unknown_keys:
                normalized[text_key] = raw_value

    if deferred_percent_distance_values:
        final_reference_mm = _coerce_float(
            normalized.get("extrusion_width", DEFAULT_SETTINGS["extrusion_width"]),
            _coerce_float(DEFAULT_SETTINGS["extrusion_width"], 0.4),
        )
        for canonical_key, raw_value in deferred_percent_distance_values.items():
            normalized[canonical_key] = _normalize_known_value(
                canonical_key,
                raw_value,
                state,
                reference_mm=final_reference_mm,
            )

    if "support_style" not in provided_known_keys:
        support_type_value = str(normalized.get("support_type", DEFAULT_SETTINGS["support_type"])).strip().lower()
        normalized["support_style"] = "tree" if support_type_value == "tree" else "pillars"
    if "support_type" not in provided_known_keys and "support_style" in provided_known_keys:
        support_style_value = str(normalized.get("support_style", DEFAULT_SETTINGS["support_style"])).strip().lower()
        if support_style_value in {"tree", "organic"}:
            normalized["support_type"] = "tree"
        else:
            normalized["support_type"] = "normal"

    if "support_interface_layers" in provided_known_keys:
        if "support_interface_top_layers" not in provided_known_keys:
            normalized["support_interface_top_layers"] = int(normalized.get("support_interface_layers", 0))
        if "support_interface_bottom_layers" not in provided_known_keys:
            normalized["support_interface_bottom_layers"] = int(DEFAULT_SETTINGS["support_interface_bottom_layers"])
    if "support_interface_top_layers" in provided_known_keys and "support_interface_layers" not in provided_known_keys:
        normalized["support_interface_layers"] = int(normalized.get("support_interface_top_layers", 0))

    if "support_spacing_mm" in provided_known_keys:
        if "support_base_spacing_mm" not in provided_known_keys:
            normalized["support_base_spacing_mm"] = float(normalized.get("support_spacing_mm", 0.1))
        if "support_interface_spacing_mm" not in provided_known_keys:
            normalized["support_interface_spacing_mm"] = float(normalized.get("support_spacing_mm", 0.1))
        if "support_bottom_interface_spacing_mm" not in provided_known_keys:
            normalized["support_bottom_interface_spacing_mm"] = float(normalized.get("support_interface_spacing_mm", 0.1))
    if "support_base_spacing_mm" in provided_known_keys and "support_spacing_mm" not in provided_known_keys:
        normalized["support_spacing_mm"] = float(normalized.get("support_base_spacing_mm", 0.1))
    if "support_interface_spacing_mm" in provided_known_keys and "support_bottom_interface_spacing_mm" not in provided_known_keys:
        normalized["support_bottom_interface_spacing_mm"] = float(normalized.get("support_interface_spacing_mm", 0.1))
    if "support_bottom_interface_spacing_mm" in provided_known_keys and "support_interface_spacing_mm" not in provided_known_keys:
        normalized["support_interface_spacing_mm"] = float(normalized.get("support_bottom_interface_spacing_mm", 0.1))

    if "support_z_gap_mm" in provided_known_keys and "support_bottom_z_gap_mm" not in provided_known_keys:
        normalized["support_bottom_z_gap_mm"] = float(normalized.get("support_z_gap_mm", 0.0))

    min_width = _coerce_float(normalized.get("variable_line_width_min", 0.1), 0.1)
    max_width = _coerce_float(normalized.get("variable_line_width_max", 0.1), 0.1)
    if min_width > max_width:
        normalized["variable_line_width_min"] = max_width
        normalized["variable_line_width_max"] = min_width
        state.clamped_value_count += 1
        state.add_warning("variable_line_width_bounds", "swapped_min_max", f"{min_width}>{max_width}")

    branch_diameter_mm = _coerce_float(
        normalized.get("tree_support_branch_diameter_mm", DEFAULT_SETTINGS["tree_support_branch_diameter_mm"]),
        _coerce_float(DEFAULT_SETTINGS["tree_support_branch_diameter_mm"], 0.6),
    )
    tip_diameter_mm = _coerce_float(
        normalized.get("tree_support_tip_diameter_mm", DEFAULT_SETTINGS["tree_support_tip_diameter_mm"]),
        _coerce_float(DEFAULT_SETTINGS["tree_support_tip_diameter_mm"], 0.3),
    )
    if tip_diameter_mm > branch_diameter_mm:
        normalized["tree_support_tip_diameter_mm"] = branch_diameter_mm
        state.clamped_value_count += 1
        state.add_warning(
            "tree_support_tip_diameter_mm",
            "clamped_to_branch_diameter",
            f"{tip_diameter_mm}>{branch_diameter_mm}",
        )

    report = SettingsNormalizationReport(
        normalized_at_utc=datetime.now(timezone.utc).isoformat(),
        input_key_count=len(raw_settings),
        output_key_count=len(normalized),
        alias_applied_count=state.alias_applied_count,
        coerced_value_count=state.coerced_value_count,
        clamped_value_count=state.clamped_value_count,
        unknown_key_count=len(state.unknown_keys),
        warning_count=len(state.warnings),
        warnings=state.warnings,
        unknown_keys=state.unknown_keys,
    )

    if strict and report.warning_count > 0:
        raise SlicerV2SettingsNormalizationError(
            f"STRICT_SETTINGS_NORMALIZATION_WARNING_FAILURE: {report.warning_count} warning(s)"
        )

    return normalized, report


def normalize_settings(
    raw_settings: dict[str, object] | None,
    *,
    strict: bool = False,
    keep_unknown_keys: bool = True,
) -> dict[str, object]:
    normalized, _report = normalize_settings_with_report(
        raw_settings,
        strict=strict,
        keep_unknown_keys=keep_unknown_keys,
    )
    return normalized
