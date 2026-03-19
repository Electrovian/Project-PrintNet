from __future__ import annotations

from .runtime import resolve_worker_count
from .support_planning import build_support_plan
from .types import SlicerContext


STAGE_NAME = "supports"


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
    support_enabled = bool(context.resolved_settings.get("support_enabled", False))
    support_type = str(context.resolved_settings.get("support_type", "normal"))
    support_style = str(context.resolved_settings.get("support_style", "pillars")).strip().lower() or "pillars"
    support_density_percent = _to_float(context.resolved_settings.get("support_density_percent", 15.0), 15.0)
    support_spacing_mm = _to_float(context.resolved_settings.get("support_spacing_mm", 2.5), 2.5)
    support_base_spacing_mm = _to_float(
        context.resolved_settings.get("support_base_spacing_mm", support_spacing_mm),
        support_spacing_mm,
    )
    support_interface_spacing_mm = _to_float(
        context.resolved_settings.get("support_interface_spacing_mm", support_spacing_mm),
        support_spacing_mm,
    )
    support_bottom_interface_spacing_mm = _to_float(
        context.resolved_settings.get("support_bottom_interface_spacing_mm", support_interface_spacing_mm),
        support_interface_spacing_mm,
    )
    support_xy_gap_mm = _to_float(context.resolved_settings.get("support_xy_gap_mm", 0.25), 0.25)
    support_z_gap_mm = _to_float(context.resolved_settings.get("support_z_gap_mm", 0.2), 0.2)
    support_bottom_z_gap_mm = _to_float(
        context.resolved_settings.get("support_bottom_z_gap_mm", support_z_gap_mm),
        support_z_gap_mm,
    )
    support_build_plate_only = bool(context.resolved_settings.get("support_build_plate_only", False))
    support_threshold_angle_deg = _to_float(
        context.resolved_settings.get("support_threshold_angle_deg", 45.0),
        45.0,
    )
    support_threshold_overlap_percent = _to_float(
        context.resolved_settings.get("support_threshold_overlap_percent", 0.0),
        0.0,
    )
    support_critical_regions_only = bool(context.resolved_settings.get("support_critical_regions_only", False))
    support_remove_small_overhang = bool(context.resolved_settings.get("support_remove_small_overhang", False))
    support_interface_layers = _to_int(context.resolved_settings.get("support_interface_layers", 2), 2)
    support_interface_top_layers = _to_int(
        context.resolved_settings.get("support_interface_top_layers", support_interface_layers),
        support_interface_layers,
    )
    support_interface_bottom_layers = _to_int(
        context.resolved_settings.get("support_interface_bottom_layers", 0),
        0,
    )
    tree_support_branch_angle_deg = _to_float(
        context.resolved_settings.get("tree_support_branch_angle_deg", 45.0),
        45.0,
    )
    tree_support_wall_count = _to_int(
        context.resolved_settings.get("tree_support_wall_count", 1),
        1,
    )
    tree_support_branch_diameter_mm = _to_float(
        context.resolved_settings.get("tree_support_branch_diameter_mm", 0.6),
        0.6,
    )
    tree_support_tip_diameter_mm = _to_float(
        context.resolved_settings.get("tree_support_tip_diameter_mm", 0.3),
        0.3,
    )
    tree_support_branch_distance_mm = _to_float(
        context.resolved_settings.get("tree_support_branch_distance_mm", 2.0),
        2.0,
    )
    tree_support_branch_distance_organic_mm = _to_float(
        context.resolved_settings.get("tree_support_branch_distance_organic_mm", tree_support_branch_distance_mm),
        tree_support_branch_distance_mm,
    )
    tree_support_top_rate_percent = _to_float(
        context.resolved_settings.get("tree_support_top_rate_percent", 30.0),
        30.0,
    )
    tree_support_branch_diameter_angle_deg = _to_float(
        context.resolved_settings.get("tree_support_branch_diameter_angle_deg", 5.0),
        5.0,
    )
    tree_support_branch_angle_organic_deg = _to_float(
        context.resolved_settings.get("tree_support_branch_angle_organic_deg", tree_support_branch_angle_deg),
        tree_support_branch_angle_deg,
    )
    tree_support_branch_diameter_organic_mm = _to_float(
        context.resolved_settings.get("tree_support_branch_diameter_organic_mm", tree_support_branch_diameter_mm),
        tree_support_branch_diameter_mm,
    )
    tree_support_auto_brim = bool(context.resolved_settings.get("tree_support_auto_brim", False))
    tree_support_brim_width_mm = _to_float(
        context.resolved_settings.get("tree_support_brim_width_mm", 0.0),
        0.0,
    )
    tree_branch_merge_distance_ratio = _to_float(
        context.resolved_settings.get("tree_support_branch_merge_distance_ratio", 1.2),
        1.2,
    )
    tree_branch_growth_ratio = _to_float(
        context.resolved_settings.get("tree_support_branch_growth_ratio", 1.08),
        1.08,
    )
    tree_min_branch_radius_mm = _to_float(
        context.resolved_settings.get("tree_support_min_branch_radius_mm", 0.3),
        0.3,
    )
    tree_parent_weight_route = _to_float(
        context.resolved_settings.get("tree_support_parent_weight_route", 0.56),
        0.56,
    )
    tree_parent_weight_load = _to_float(
        context.resolved_settings.get("tree_support_parent_weight_load", 0.40),
        0.40,
    )
    tree_parent_root_bonus = _to_float(
        context.resolved_settings.get("tree_support_parent_root_bonus", 0.06),
        0.06,
    )
    tree_trunk_root_bonus = _to_float(
        context.resolved_settings.get("tree_support_trunk_root_bonus", 0.08),
        0.08,
    )
    tree_trunk_depth_bonus = _to_float(
        context.resolved_settings.get("tree_support_trunk_depth_bonus", 0.07),
        0.07,
    )
    tree_support_strict_parity_mode = bool(
        context.resolved_settings.get("tree_support_strict_parity_mode", False)
    )
    extrusion_width = _to_float(context.resolved_settings.get("extrusion_width", 0.4), 0.4)

    islands_artifact = context.stage_artifacts.get("islands", {})
    layer_graphs = islands_artifact.get("layer_graphs", [])
    vertical_edges = islands_artifact.get("vertical_edges", [])
    worker_count = resolve_worker_count(
        context.runtime_settings,
        len(layer_graphs) if isinstance(layer_graphs, list) else 0,
        default=1,
    )

    if isinstance(layer_graphs, list) and layer_graphs:
        layer_plans, report = build_support_plan(
            layer_graphs,
            vertical_edges=vertical_edges if isinstance(vertical_edges, tuple) or isinstance(vertical_edges, list) else (),
            support_enabled=support_enabled,
            support_type=support_type,
            support_style=support_style,
            support_density_percent=support_density_percent,
            support_spacing_mm=support_spacing_mm,
            support_base_spacing_mm=support_base_spacing_mm,
            support_interface_spacing_mm=support_interface_spacing_mm,
            support_bottom_interface_spacing_mm=support_bottom_interface_spacing_mm,
            support_xy_gap_mm=support_xy_gap_mm,
            support_z_gap_mm=support_z_gap_mm,
            support_bottom_z_gap_mm=support_bottom_z_gap_mm,
            support_build_plate_only=support_build_plate_only,
            support_threshold_angle_deg=support_threshold_angle_deg,
            support_threshold_overlap_percent=support_threshold_overlap_percent,
            support_critical_regions_only=support_critical_regions_only,
            support_remove_small_overhang=support_remove_small_overhang,
            support_interface_layers=support_interface_layers,
            support_interface_top_layers=support_interface_top_layers,
            support_interface_bottom_layers=support_interface_bottom_layers,
            extrusion_width_mm=extrusion_width,
            tree_support_branch_angle_deg=tree_support_branch_angle_deg,
            tree_support_wall_count=tree_support_wall_count,
            tree_support_branch_diameter_mm=tree_support_branch_diameter_mm,
            tree_support_tip_diameter_mm=tree_support_tip_diameter_mm,
            tree_support_branch_distance_mm=tree_support_branch_distance_mm,
            tree_support_branch_distance_organic_mm=tree_support_branch_distance_organic_mm,
            tree_support_top_rate_percent=tree_support_top_rate_percent,
            tree_support_branch_diameter_angle_deg=tree_support_branch_diameter_angle_deg,
            tree_support_branch_angle_organic_deg=tree_support_branch_angle_organic_deg,
            tree_support_branch_diameter_organic_mm=tree_support_branch_diameter_organic_mm,
            tree_support_auto_brim=tree_support_auto_brim,
            tree_support_brim_width_mm=tree_support_brim_width_mm,
            tree_branch_merge_distance_ratio=tree_branch_merge_distance_ratio,
            tree_branch_growth_ratio=tree_branch_growth_ratio,
            tree_min_branch_radius_mm=tree_min_branch_radius_mm,
            tree_parent_weight_route=tree_parent_weight_route,
            tree_parent_weight_load=tree_parent_weight_load,
            tree_parent_root_bonus=tree_parent_root_bonus,
            tree_trunk_root_bonus=tree_trunk_root_bonus,
            tree_trunk_depth_bonus=tree_trunk_depth_bonus,
            tree_support_strict_parity_mode=tree_support_strict_parity_mode,
            max_workers=worker_count,
        )
        artifact = {
            "support_enabled": support_enabled,
            "support_type": report.support_type,
            "support_style": report.support_style,
            "support_density_percent": support_density_percent,
            "support_spacing_mm": support_spacing_mm,
            "support_base_spacing_mm": support_base_spacing_mm,
            "support_interface_spacing_mm": support_interface_spacing_mm,
            "support_bottom_interface_spacing_mm": support_bottom_interface_spacing_mm,
            "support_xy_gap_mm": support_xy_gap_mm,
            "support_z_gap_mm": support_z_gap_mm,
            "support_bottom_z_gap_mm": support_bottom_z_gap_mm,
            "support_build_plate_only": support_build_plate_only,
            "support_threshold_angle_deg": support_threshold_angle_deg,
            "support_threshold_overlap_percent": support_threshold_overlap_percent,
            "support_critical_regions_only": support_critical_regions_only,
            "support_remove_small_overhang": support_remove_small_overhang,
            "support_interface_layers": support_interface_layers,
            "support_interface_top_layers": support_interface_top_layers,
            "support_interface_bottom_layers": support_interface_bottom_layers,
            "support_interface_bottom_layers_effective": int(report.support_interface_bottom_layers_effective),
            "tree_support_branch_angle_deg": tree_support_branch_angle_deg,
            "tree_support_wall_count": tree_support_wall_count,
            "tree_support_branch_diameter_mm": tree_support_branch_diameter_mm,
            "tree_support_tip_diameter_mm": tree_support_tip_diameter_mm,
            "tree_support_branch_distance_mm": tree_support_branch_distance_mm,
            "tree_support_branch_distance_organic_mm": tree_support_branch_distance_organic_mm,
            "tree_support_top_rate_percent": tree_support_top_rate_percent,
            "tree_support_branch_diameter_angle_deg": tree_support_branch_diameter_angle_deg,
            "tree_support_branch_angle_organic_deg": tree_support_branch_angle_organic_deg,
            "tree_support_branch_diameter_organic_mm": tree_support_branch_diameter_organic_mm,
            "tree_support_auto_brim": tree_support_auto_brim,
            "tree_support_brim_width_mm": tree_support_brim_width_mm,
            "tree_support_branch_merge_distance_ratio": tree_branch_merge_distance_ratio,
            "tree_support_branch_growth_ratio": tree_branch_growth_ratio,
            "tree_support_min_branch_radius_mm": tree_min_branch_radius_mm,
            "tree_support_parent_weight_route": tree_parent_weight_route,
            "tree_support_parent_weight_load": tree_parent_weight_load,
            "tree_support_parent_root_bonus": tree_parent_root_bonus,
            "tree_support_trunk_root_bonus": tree_trunk_root_bonus,
            "tree_support_trunk_depth_bonus": tree_trunk_depth_bonus,
            "tree_support_strict_parity_mode": tree_support_strict_parity_mode,
            "support_region_count": report.support_region_count_total,
            "support_path_count": report.support_path_count_total,
            "support_path_length_mm_total": report.support_path_length_mm_total,
            "support_interface_path_count_total": report.interface_path_count_total,
            "unsupported_island_count_total": report.unsupported_island_count_total,
            "tree_branch_count_total": report.tree_branch_count_total,
            "tree_merge_count_total": report.tree_merge_count_total,
            "tree_collision_avoid_count_total": report.tree_collision_avoid_count_total,
            "tree_pruned_branch_count_total": report.tree_pruned_branch_count_total,
            "tree_parent_assignment_count_total": report.tree_parent_assignment_count_total,
            "tree_trunk_count_total": report.tree_trunk_count_total,
            "tree_branch_load_score_avg": report.tree_branch_load_score_avg,
            "tree_branch_selection_score_avg": report.tree_branch_selection_score_avg,
            "tree_branch_reroute_cost_mm_total": report.tree_branch_reroute_cost_mm_total,
            "tree_branch_trunk_assignment_counts": report.tree_branch_trunk_assignment_counts,
            "tree_branches": [branch.to_dict() for branch in report.tree_branches],
            "layer_support_counts": [plan.support_region_count for plan in layer_plans],
            "layer_support_path_counts": [plan.support_path_count for plan in layer_plans],
            "layer_support_interface_path_counts": [plan.interface_path_count for plan in layer_plans],
            "layer_tree_branch_counts": [plan.tree_branch_count for plan in layer_plans],
            "layer_tree_merge_counts": [plan.tree_merge_count for plan in layer_plans],
            "layer_tree_collision_avoid_counts": [plan.tree_collision_avoid_count for plan in layer_plans],
            "layer_tree_pruned_branch_counts": [plan.tree_pruned_branch_count for plan in layer_plans],
            "layer_tree_parent_assignment_counts": [plan.tree_parent_assignment_count for plan in layer_plans],
            "layer_tree_trunk_counts": [plan.tree_trunk_count for plan in layer_plans],
            "warning_count": report.warning_count,
            "warnings": report.warnings,
            "report": report.to_dict(),
            "layer_plans": layer_plans,
        }
        _update_parity_artifact(
            context,
            {
                "support_region_count": int(report.support_region_count_total),
                "support_path_count": int(report.support_path_count_total),
                "support_path_length_mm_total": float(report.support_path_length_mm_total),
                "support_threshold_angle_deg": float(support_threshold_angle_deg),
                "support_threshold_overlap_percent": float(support_threshold_overlap_percent),
                "support_critical_regions_only": bool(support_critical_regions_only),
                "support_remove_small_overhang": bool(support_remove_small_overhang),
                "support_build_plate_only": bool(support_build_plate_only),
                "support_interface_bottom_layers": int(support_interface_bottom_layers),
                "support_interface_bottom_layers_effective": int(report.support_interface_bottom_layers_effective),
                "tree_branch_count_total": int(report.tree_branch_count_total),
                "tree_trunk_count_total": int(report.tree_trunk_count_total),
            },
        )
        context.stage_artifacts[STAGE_NAME] = artifact
        return artifact

    region_count = _to_int(context.stage_artifacts.get("regions", {}).get("region_count", 1), 1)
    path_count = 0
    if support_enabled:
        path_count = max(1, int(region_count * 0.5))

    warnings: list[str] = []
    if support_enabled:
        warnings.append("support_planning:fallback_without_islands")

    artifact = {
        "support_enabled": support_enabled,
        "support_type": support_type,
        "support_style": support_style,
        "support_density_percent": support_density_percent,
        "support_spacing_mm": support_spacing_mm,
        "support_base_spacing_mm": support_base_spacing_mm,
        "support_interface_spacing_mm": support_interface_spacing_mm,
        "support_bottom_interface_spacing_mm": support_bottom_interface_spacing_mm,
        "support_xy_gap_mm": support_xy_gap_mm,
        "support_z_gap_mm": support_z_gap_mm,
        "support_bottom_z_gap_mm": support_bottom_z_gap_mm,
        "support_build_plate_only": support_build_plate_only,
        "support_threshold_angle_deg": support_threshold_angle_deg,
        "support_threshold_overlap_percent": support_threshold_overlap_percent,
        "support_critical_regions_only": support_critical_regions_only,
        "support_remove_small_overhang": support_remove_small_overhang,
        "support_interface_layers": support_interface_layers,
        "support_interface_top_layers": support_interface_top_layers,
        "support_interface_bottom_layers": support_interface_bottom_layers,
        "support_interface_bottom_layers_effective": (
            int(support_interface_top_layers)
            if int(support_interface_bottom_layers) == -1
            else int(support_interface_bottom_layers)
        ),
        "tree_support_branch_angle_deg": tree_support_branch_angle_deg,
        "tree_support_wall_count": tree_support_wall_count,
        "tree_support_branch_diameter_mm": tree_support_branch_diameter_mm,
        "tree_support_tip_diameter_mm": tree_support_tip_diameter_mm,
        "tree_support_branch_distance_mm": tree_support_branch_distance_mm,
        "tree_support_branch_distance_organic_mm": tree_support_branch_distance_organic_mm,
        "tree_support_top_rate_percent": tree_support_top_rate_percent,
        "tree_support_branch_diameter_angle_deg": tree_support_branch_diameter_angle_deg,
        "tree_support_branch_angle_organic_deg": tree_support_branch_angle_organic_deg,
        "tree_support_branch_diameter_organic_mm": tree_support_branch_diameter_organic_mm,
        "tree_support_auto_brim": tree_support_auto_brim,
        "tree_support_brim_width_mm": tree_support_brim_width_mm,
        "tree_support_branch_merge_distance_ratio": tree_branch_merge_distance_ratio,
        "tree_support_branch_growth_ratio": tree_branch_growth_ratio,
        "tree_support_min_branch_radius_mm": tree_min_branch_radius_mm,
        "tree_support_parent_weight_route": tree_parent_weight_route,
        "tree_support_parent_weight_load": tree_parent_weight_load,
        "tree_support_parent_root_bonus": tree_parent_root_bonus,
        "tree_support_trunk_root_bonus": tree_trunk_root_bonus,
        "tree_support_trunk_depth_bonus": tree_trunk_depth_bonus,
        "tree_support_strict_parity_mode": tree_support_strict_parity_mode,
        "support_region_count": path_count,
        "support_path_count": path_count,
        "support_path_length_mm_total": 0.0,
        "support_interface_path_count_total": 0,
        "unsupported_island_count_total": 0,
        "tree_branch_count_total": 0,
        "tree_merge_count_total": 0,
        "tree_collision_avoid_count_total": 0,
        "tree_pruned_branch_count_total": 0,
        "tree_parent_assignment_count_total": 0,
        "tree_trunk_count_total": 0,
        "tree_branch_load_score_avg": 0.0,
        "tree_branch_selection_score_avg": 0.0,
        "tree_branch_reroute_cost_mm_total": 0.0,
        "tree_branch_trunk_assignment_counts": {},
        "tree_branches": [],
        "layer_support_counts": [],
        "layer_support_path_counts": [],
        "layer_support_interface_path_counts": [],
        "layer_tree_branch_counts": [],
        "layer_tree_merge_counts": [],
        "layer_tree_collision_avoid_counts": [],
        "layer_tree_pruned_branch_counts": [],
        "layer_tree_parent_assignment_counts": [],
        "layer_tree_trunk_counts": [],
        "warning_count": len(warnings),
        "warnings": warnings,
    }
    _update_parity_artifact(
        context,
        {
            "support_region_count": int(path_count),
            "support_path_count": int(path_count),
            "support_path_length_mm_total": 0.0,
            "support_threshold_angle_deg": float(support_threshold_angle_deg),
            "support_threshold_overlap_percent": float(support_threshold_overlap_percent),
            "support_critical_regions_only": bool(support_critical_regions_only),
            "support_remove_small_overhang": bool(support_remove_small_overhang),
            "support_build_plate_only": bool(support_build_plate_only),
            "support_interface_bottom_layers": int(support_interface_bottom_layers),
            "support_interface_bottom_layers_effective": (
                int(support_interface_top_layers)
                if int(support_interface_bottom_layers) == -1
                else int(support_interface_bottom_layers)
            ),
            "tree_branch_count_total": 0,
            "tree_trunk_count_total": 0,
        },
    )
    context.stage_artifacts[STAGE_NAME] = artifact
    return artifact
