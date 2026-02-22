from __future__ import annotations

from .infill_patterns import build_infill_patterns
from .runtime import resolve_worker_count
from .types import SlicerContext


STAGE_NAME = "infill"


def _update_parity_artifact(context: SlicerContext, payload: dict[str, object]) -> None:
    parity_artifact = context.stage_artifacts.get("parity")
    if not isinstance(parity_artifact, dict):
        parity_artifact = {}
    parity_artifact[STAGE_NAME] = dict(payload)
    context.stage_artifacts["parity"] = parity_artifact


def _to_float(value: object, default: float) -> float:
    if isinstance(value, bool):
        return default
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (str, bytes, bytearray)):
        text = str(value).strip()
        if not text:
            return default
        try:
            return float(text)
        except (TypeError, ValueError, OverflowError):
            return default
    text = str(value).strip()
    if not text:
        return default
    try:
        return float(text)
    except (TypeError, ValueError, OverflowError):
        return default


def _to_int(value: object, default: int) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return int(value)
    if isinstance(value, float):
        return int(value)
    if isinstance(value, (str, bytes, bytearray)):
        text = str(value).strip()
        if not text:
            return default
        try:
            return int(float(text))
        except (TypeError, ValueError, OverflowError):
            return default
    text = str(value).strip()
    if not text:
        return default
    try:
        return int(float(text))
    except (TypeError, ValueError, OverflowError):
        return default


def run(context: SlicerContext) -> dict:
    regions_artifact = context.stage_artifacts.get("regions", {})
    islands_artifact = context.stage_artifacts.get("islands", {})
    region_count = _to_int(regions_artifact.get("region_count", 1), 1)

    infill_percent = _to_float(context.resolved_settings.get("infill_percent", 15.0), 15.0)
    infill_percent = max(0.0, min(infill_percent, 100.0))
    infill_pattern = str(context.resolved_settings.get("infill_pattern", "rectilinear")).strip().lower()
    infill_angle_start = _to_float(context.resolved_settings.get("infill_angle_start", 45.0), 45.0)
    infill_angle_step = _to_float(context.resolved_settings.get("infill_angle_step", 90.0), 90.0)
    infill_angle_template = str(context.resolved_settings.get("infill_angle_template", "")).strip()
    infill_anchor = context.resolved_settings.get("infill_anchor", 0.0)
    infill_anchor_max = context.resolved_settings.get("infill_anchor_max", 1000.0)
    infill_combination_enabled = bool(context.resolved_settings.get("infill_combination_enabled", False))
    infill_combination_max_height = _to_float(
        context.resolved_settings.get("infill_combination_max_layer_height_mm", 0.0),
        0.0,
    )
    infill_antivibration_enabled = bool(context.resolved_settings.get("infill_antivibration_enabled", True))
    infill_antivibration_short_line_threshold = _to_float(
        context.resolved_settings.get("infill_antivibration_short_line_threshold_mm", 4.0),
        4.0,
    )
    infill_antivibration_max_skips = _to_int(
        context.resolved_settings.get("infill_antivibration_max_skips_allowed", 2),
        2,
    )
    infill_antivibration_min_depth = _to_int(
        context.resolved_settings.get("infill_antivibration_min_depth_for_line_removing", 5),
        5,
    )
    extrusion_width = _to_float(context.resolved_settings.get("extrusion_width", 0.4), 0.4)
    layer_height = _to_float(context.resolved_settings.get("layer_height", 0.2), 0.2)
    bottom_shell_layers = _to_int(context.resolved_settings.get("bottom_layers", 0), 0)
    top_shell_layers = _to_int(context.resolved_settings.get("top_layers", 0), 0)
    density_ratio = infill_percent / 100.0

    layer_graphs = islands_artifact.get("layer_graphs", [])
    worker_count = resolve_worker_count(
        context.runtime_settings,
        len(layer_graphs) if isinstance(layer_graphs, list) else 0,
        default=1,
    )
    if isinstance(layer_graphs, list) and layer_graphs:
        layer_plans, report = build_infill_patterns(
            layer_graphs,
            infill_pattern=infill_pattern,
            infill_percent=infill_percent,
            extrusion_width_mm=extrusion_width,
            angle_start_deg=infill_angle_start,
            angle_step_deg=infill_angle_step,
            angle_template=infill_angle_template,
            infill_anchor=infill_anchor,
            infill_anchor_max=infill_anchor_max,
            combine_infill_enabled=infill_combination_enabled,
            combine_max_layer_height_mm=infill_combination_max_height,
            layer_height_mm=layer_height,
            bottom_shell_layers=bottom_shell_layers,
            top_shell_layers=top_shell_layers,
            anti_vibration_enabled=infill_antivibration_enabled,
            anti_vibration_short_line_threshold_mm=infill_antivibration_short_line_threshold,
            anti_vibration_max_skips_allowed=infill_antivibration_max_skips,
            anti_vibration_min_depth_for_line_removing=infill_antivibration_min_depth,
            max_workers=worker_count,
        )
        artifact = {
            "infill_percent": infill_percent,
            "infill_pattern": infill_pattern,
            "infill_density_ratio": density_ratio,
            "infill_angle_start_deg": infill_angle_start,
            "infill_angle_step_deg": infill_angle_step,
            "infill_anchor": infill_anchor,
            "infill_anchor_max": infill_anchor_max,
            "infill_combination_enabled": infill_combination_enabled,
            "infill_combination_max_layer_height_mm": infill_combination_max_height,
            "infill_antivibration_enabled": infill_antivibration_enabled,
            "infill_antivibration_short_line_threshold_mm": infill_antivibration_short_line_threshold,
            "infill_antivibration_max_skips_allowed": infill_antivibration_max_skips,
            "infill_antivibration_min_depth_for_line_removing": infill_antivibration_min_depth,
            "infill_path_count": int(report.path_count_total),
            "infill_path_length_mm_total": report.path_length_mm_total,
            "layer_infill_counts": [plan.path_count for plan in layer_plans],
            "layer_infill_angles_deg": [plan.angle_deg for plan in layer_plans],
            "layer_infill_anchor_angles_deg": [plan.anchor_angle_deg for plan in layer_plans],
            "layer_infill_combined_counts": [plan.combined_layer_count for plan in layer_plans],
            "layer_infill_thickness_layers": [plan.combined_thickness_layers for plan in layer_plans],
            "layer_infill_void_flags": [bool(plan.is_void_layer) for plan in layer_plans],
            "layer_infill_void_depth_layers": [int(plan.void_depth_layers) for plan in layer_plans],
            "layer_infill_combine_void_depth_layers": [int(plan.combine_void_depth_layers) for plan in layer_plans],
            "layer_infill_support_surface_ratios": [float(plan.support_surface_ratio) for plan in layer_plans],
            "layer_infill_island_areas_mm2": [float(plan.island_area_mm2) for plan in layer_plans],
            "layer_infill_effective_areas_mm2": [float(plan.effective_infill_area_mm2) for plan in layer_plans],
            "layer_infill_combine_effective_areas_mm2": [float(plan.combine_effective_area_mm2) for plan in layer_plans],
            "layer_infill_combined_into_layers": [
                int(plan.combined_into_layer_index)
                if plan.combined_into_layer_index is not None
                else int(plan.layer_index)
                for plan in layer_plans
            ],
            "layer_infill_combine_target_layers": [
                int(plan.combine_target_layer_index)
                if plan.combine_target_layer_index is not None
                else int(plan.layer_index)
                for plan in layer_plans
            ],
            "layer_infill_combine_thickness_layers": [int(plan.combine_thickness_layers) for plan in layer_plans],
            "warning_count": report.warning_count,
            "warnings": report.warnings,
            "report": report.to_dict(),
            "layer_plans": layer_plans,
        }
        _update_parity_artifact(
            context,
            {
                "infill_path_count": int(report.path_count_total),
                "infill_path_length_mm_total": float(report.path_length_mm_total),
                "void_layer_count": int(report.void_layer_count),
                "support_surface_ratio_avg": float(report.support_surface_ratio_avg),
            },
        )
        context.stage_artifacts[STAGE_NAME] = artifact
        return artifact

    fallback_path_count = 0
    if infill_percent > 0.0:
        fallback_path_count = max(1, int(region_count * (1.0 + density_ratio)))
    artifact = {
        "infill_percent": infill_percent,
        "infill_pattern": infill_pattern,
        "infill_density_ratio": density_ratio,
        "infill_angle_start_deg": infill_angle_start,
        "infill_angle_step_deg": infill_angle_step,
        "infill_anchor": infill_anchor,
        "infill_anchor_max": infill_anchor_max,
        "infill_combination_enabled": infill_combination_enabled,
        "infill_combination_max_layer_height_mm": infill_combination_max_height,
        "infill_antivibration_enabled": infill_antivibration_enabled,
        "infill_antivibration_short_line_threshold_mm": infill_antivibration_short_line_threshold,
        "infill_antivibration_max_skips_allowed": infill_antivibration_max_skips,
        "infill_antivibration_min_depth_for_line_removing": infill_antivibration_min_depth,
        "infill_path_count": fallback_path_count,
        "infill_path_length_mm_total": 0.0,
        "layer_infill_counts": [],
        "layer_infill_angles_deg": [],
        "layer_infill_anchor_angles_deg": [],
        "layer_infill_combined_counts": [],
        "layer_infill_thickness_layers": [],
        "layer_infill_void_flags": [],
        "layer_infill_void_depth_layers": [],
        "layer_infill_combine_void_depth_layers": [],
        "layer_infill_support_surface_ratios": [],
        "layer_infill_island_areas_mm2": [],
        "layer_infill_effective_areas_mm2": [],
        "layer_infill_combine_effective_areas_mm2": [],
        "layer_infill_combined_into_layers": [],
        "layer_infill_combine_target_layers": [],
        "layer_infill_combine_thickness_layers": [],
        "warning_count": 1,
        "warnings": ["infill_patterns:fallback_without_islands"],
    }
    _update_parity_artifact(
        context,
        {
            "infill_path_count": int(fallback_path_count),
            "infill_path_length_mm_total": 0.0,
            "void_layer_count": 0,
            "support_surface_ratio_avg": 0.0,
        },
    )
    context.stage_artifacts[STAGE_NAME] = artifact
    return artifact
