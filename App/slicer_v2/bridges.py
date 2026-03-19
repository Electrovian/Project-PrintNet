from __future__ import annotations

from .runtime import resolve_worker_count
from .solid_bridges import build_solid_layers_and_bridges
from .types import SlicerContext


STAGE_NAME = "bridges"


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
    enable_bridge = bool(context.resolved_settings.get("bridge_enabled", True))
    top_layers = _to_int(context.resolved_settings.get("top_layers", 3), 3)
    bottom_layers = _to_int(context.resolved_settings.get("bottom_layers", 3), 3)
    extrusion_width = _to_float(context.resolved_settings.get("extrusion_width", 0.4), 0.4)
    bridge_flow_ratio = _to_float(context.resolved_settings.get("bridge_flow_ratio", 1.0), 1.0)
    bridge_speed_ratio = _to_float(context.resolved_settings.get("bridge_speed_ratio", 0.8), 0.8)
    bridge_density_percent = _to_float(context.resolved_settings.get("bridge_density_percent", 100.0), 100.0)
    internal_bridge_flow_ratio = _to_float(context.resolved_settings.get("internal_bridge_flow_ratio", 1.0), 1.0)
    internal_bridge_density_percent = _to_float(
        context.resolved_settings.get("internal_bridge_density_percent", 100.0),
        100.0,
    )
    internal_bridge_angle_deg = _to_float(context.resolved_settings.get("internal_bridge_angle_deg", 0.0), 0.0)
    thick_bridges = bool(context.resolved_settings.get("thick_bridges", False))
    thick_internal_bridges = bool(context.resolved_settings.get("thick_internal_bridges", False))
    extra_bridge_layer_enabled = bool(context.resolved_settings.get("extra_bridge_layer_enabled", False))
    bridge_over_infill_enabled = bool(context.resolved_settings.get("bridge_over_infill_enabled", True))
    bridge_over_infill_min_candidate_ratio = _to_float(
        context.resolved_settings.get("bridge_over_infill_min_candidate_ratio", 0.05),
        0.05,
    )
    bridge_over_infill_sample_count = _to_int(
        context.resolved_settings.get("bridge_over_infill_sample_count", 7),
        7,
    )
    bridge_span_strip_geometry_enabled = bool(
        context.resolved_settings.get("bridge_span_strip_geometry_enabled", True)
    )

    regions_artifact = context.stage_artifacts.get("regions", {})
    if not isinstance(regions_artifact, dict):
        regions_artifact = {}
    region_count = _to_int(regions_artifact.get("region_count", 1), 1)
    islands_artifact = context.stage_artifacts.get("islands", {})
    if not isinstance(islands_artifact, dict):
        islands_artifact = {}
    infill_artifact = context.stage_artifacts.get("infill", {})
    if not isinstance(infill_artifact, dict):
        infill_artifact = {}
    layer_graphs = islands_artifact.get("layer_graphs", [])
    vertical_edges = islands_artifact.get("vertical_edges", [])
    layer_anchor_angles = infill_artifact.get("layer_infill_anchor_angles_deg", [])
    layer_infill_void_flags = infill_artifact.get("layer_infill_void_flags", [])
    layer_infill_void_depth_layers = infill_artifact.get("layer_infill_void_depth_layers", [])
    layer_infill_combine_void_depth_layers = infill_artifact.get("layer_infill_combine_void_depth_layers", [])
    layer_infill_combined_into_layers = infill_artifact.get("layer_infill_combined_into_layers", [])
    layer_infill_combine_target_layers = infill_artifact.get("layer_infill_combine_target_layers", [])
    layer_infill_thickness_layers = infill_artifact.get("layer_infill_thickness_layers", [])
    layer_infill_combine_thickness_layers = infill_artifact.get("layer_infill_combine_thickness_layers", [])
    layer_infill_support_surface_ratios = infill_artifact.get("layer_infill_support_surface_ratios", [])
    worker_count = resolve_worker_count(
        context.runtime_settings,
        len(layer_graphs) if isinstance(layer_graphs, list) else 0,
        default=1,
    )

    if isinstance(layer_graphs, list) and layer_graphs:
        combined_into_layers = (
            layer_infill_combine_target_layers
            if isinstance(layer_infill_combine_target_layers, list) and layer_infill_combine_target_layers
            else layer_infill_combined_into_layers
        )
        combined_thickness_layers = (
            layer_infill_combine_thickness_layers
            if isinstance(layer_infill_combine_thickness_layers, list) and layer_infill_combine_thickness_layers
            else layer_infill_thickness_layers
        )
        combined_void_depth_layers = (
            layer_infill_combine_void_depth_layers
            if isinstance(layer_infill_combine_void_depth_layers, list) and layer_infill_combine_void_depth_layers
            else layer_infill_void_depth_layers
        )
        layer_plans, report = build_solid_layers_and_bridges(
            layer_graphs,
            vertical_edges=vertical_edges if isinstance(vertical_edges, tuple) or isinstance(vertical_edges, list) else (),
            top_layers=top_layers,
            bottom_layers=bottom_layers,
            extrusion_width_mm=extrusion_width,
            bridge_enabled=enable_bridge,
            bridge_flow_ratio=bridge_flow_ratio,
            bridge_speed_ratio=bridge_speed_ratio,
            bridge_density_percent=bridge_density_percent,
            internal_bridge_flow_ratio=internal_bridge_flow_ratio,
            internal_bridge_density_percent=internal_bridge_density_percent,
            internal_bridge_angle_deg=internal_bridge_angle_deg,
            thick_bridges=thick_bridges,
            thick_internal_bridges=thick_internal_bridges,
            extra_bridge_layer_enabled=extra_bridge_layer_enabled,
            bridge_over_infill_enabled=bridge_over_infill_enabled,
            bridge_over_infill_min_candidate_ratio=bridge_over_infill_min_candidate_ratio,
            bridge_over_infill_sample_count=bridge_over_infill_sample_count,
            layer_infill_void_flags=layer_infill_void_flags if isinstance(layer_infill_void_flags, list) else [],
            layer_infill_void_depth_layers=(
                combined_void_depth_layers if isinstance(combined_void_depth_layers, list) else []
            ),
            layer_infill_combined_into_layers=(
                combined_into_layers if isinstance(combined_into_layers, list) else []
            ),
            layer_infill_thickness_layers=(
                combined_thickness_layers if isinstance(combined_thickness_layers, list) else []
            ),
            layer_infill_support_surface_ratios=(
                layer_infill_support_surface_ratios if isinstance(layer_infill_support_surface_ratios, list) else []
            ),
            layer_anchor_angles_deg=layer_anchor_angles if isinstance(layer_anchor_angles, list) else [],
            max_workers=worker_count,
        )
        artifact = {
            "bridge_enabled": enable_bridge,
            "bridge_flow_ratio": bridge_flow_ratio,
            "bridge_speed_ratio": bridge_speed_ratio,
            "bridge_density_percent": bridge_density_percent,
            "internal_bridge_flow_ratio": internal_bridge_flow_ratio,
            "internal_bridge_density_percent": internal_bridge_density_percent,
            "internal_bridge_angle_deg": internal_bridge_angle_deg,
            "thick_bridges": thick_bridges,
            "thick_internal_bridges": thick_internal_bridges,
            "extra_bridge_layer_enabled": extra_bridge_layer_enabled,
            "bridge_over_infill_enabled": bridge_over_infill_enabled,
            "bridge_over_infill_min_candidate_ratio": bridge_over_infill_min_candidate_ratio,
            "bridge_over_infill_sample_count": bridge_over_infill_sample_count,
            "bridge_span_strip_geometry_enabled": bridge_span_strip_geometry_enabled,
            "infill_combine_metadata_consumed": bool(
                (isinstance(combined_into_layers, list) and bool(combined_into_layers))
                or (isinstance(combined_thickness_layers, list) and bool(combined_thickness_layers))
                or (isinstance(combined_void_depth_layers, list) and bool(combined_void_depth_layers))
            ),
            "top_layers": top_layers,
            "bottom_layers": bottom_layers,
            "solid_layer_count": report.solid_layer_count,
            "top_solid_layer_count": report.top_solid_layer_count,
            "bottom_solid_layer_count": report.bottom_solid_layer_count,
            "solid_path_count_total": report.solid_path_count_total,
            "solid_path_length_mm_total": report.solid_path_length_mm_total,
            "bridge_region_count": report.bridge_region_count_total,
            "bridge_path_count": report.bridge_path_count_total,
            "bridge_path_length_mm_total": report.bridge_path_length_mm_total,
            "bridge_span_component_count_total": report.bridge_span_component_count_total,
            "bridge_span_inter_island_edge_count_total": report.bridge_span_inter_island_edge_count_total,
            "bridge_span_node_count_total": report.bridge_span_node_count_total,
            "bridge_span_edge_count_total": report.bridge_span_edge_count_total,
            "bridge_candidate_ratio_avg": report.bridge_candidate_ratio_avg,
            "bridge_support_surface_ratio_avg": report.bridge_support_surface_ratio_avg,
            "layer_solid_path_counts": [plan.solid_path_count for plan in layer_plans],
            "layer_bridge_region_counts": [plan.bridge_region_count for plan in layer_plans],
            "layer_bridge_path_counts": [plan.bridge_path_count for plan in layer_plans],
            "layer_bridge_span_component_counts": [plan.bridge_span_component_count for plan in layer_plans],
            "layer_bridge_span_inter_island_edge_counts": [
                plan.bridge_span_inter_island_edge_count for plan in layer_plans
            ],
            "layer_bridge_span_node_counts_total": [plan.bridge_span_node_count for plan in layer_plans],
            "layer_bridge_span_edge_counts_total": [plan.bridge_span_edge_count for plan in layer_plans],
            "layer_bridge_angles_deg": [
                (plan.bridge_regions[0].angle_deg if plan.bridge_regions else 0.0) for plan in layer_plans
            ],
            "layer_bridge_angle_sources": [
                (plan.bridge_regions[0].direction_angle_source if plan.bridge_regions else "local")
                for plan in layer_plans
            ],
            "layer_bridge_direction_vote_angles_deg": [
                (plan.bridge_regions[0].direction_vote_angle_deg if plan.bridge_regions else 0.0)
                for plan in layer_plans
            ],
            "layer_bridge_direction_vote_confidences": [
                (plan.bridge_regions[0].direction_vote_confidence if plan.bridge_regions else 0.0)
                for plan in layer_plans
            ],
            "layer_bridge_candidate_ratios": [
                (plan.bridge_regions[0].candidate_ratio if plan.bridge_regions else 0.0) for plan in layer_plans
            ],
            "layer_bridge_candidate_areas_mm2": [
                (plan.bridge_regions[0].candidate_area_mm2 if plan.bridge_regions else 0.0) for plan in layer_plans
            ],
            "layer_bridge_candidate_depth_layers": [
                (plan.bridge_regions[0].candidate_depth_layers if plan.bridge_regions else 1) for plan in layer_plans
            ],
            "layer_bridge_support_surface_ratios": [
                (plan.bridge_regions[0].support_surface_ratio if plan.bridge_regions else 0.0) for plan in layer_plans
            ],
            "layer_infill_combine_target_layers": [
                _to_int(value, 0) for value in (combined_into_layers if isinstance(combined_into_layers, list) else [])
            ],
            "layer_infill_combine_thickness_layers": [
                _to_int(value, 1) for value in (combined_thickness_layers if isinstance(combined_thickness_layers, list) else [])
            ],
            "layer_infill_combine_void_depth_layers": [
                _to_int(value, 1) for value in (combined_void_depth_layers if isinstance(combined_void_depth_layers, list) else [])
            ],
            "layer_bridge_unsupported_surface_areas_mm2": [
                (plan.bridge_regions[0].unsupported_surface_area_mm2 if plan.bridge_regions else 0.0)
                for plan in layer_plans
            ],
            "layer_bridge_span_node_counts": [
                (len(plan.bridge_regions[0].span_nodes) if plan.bridge_regions else 0) for plan in layer_plans
            ],
            "layer_bridge_span_edge_counts": [
                (len(plan.bridge_regions[0].span_edges) if plan.bridge_regions else 0) for plan in layer_plans
            ],
            "bridge_span_components": [
                component.to_dict() for plan in layer_plans for component in plan.bridge_span_components
            ],
            "layer_classifications": [plan.classification for plan in layer_plans],
            "warning_count": report.warning_count,
            "warnings": report.warnings,
            "report": report.to_dict(),
            "layer_plans": layer_plans,
        }
        _update_parity_artifact(
            context,
            {
                "bridge_region_count": int(report.bridge_region_count_total),
                "bridge_path_count": int(report.bridge_path_count_total),
                "bridge_path_length_mm_total": float(report.bridge_path_length_mm_total),
                "bridge_candidate_ratio_avg": float(report.bridge_candidate_ratio_avg),
                "bridge_support_surface_ratio_avg": float(report.bridge_support_surface_ratio_avg),
            },
        )
        context.stage_artifacts[STAGE_NAME] = artifact
        return artifact

    bridge_regions = 0
    if enable_bridge:
        bridge_regions = max(0, int(region_count * 0.1))

    artifact = {
        "bridge_enabled": enable_bridge,
        "bridge_flow_ratio": bridge_flow_ratio,
        "bridge_speed_ratio": bridge_speed_ratio,
        "bridge_density_percent": bridge_density_percent,
        "internal_bridge_flow_ratio": internal_bridge_flow_ratio,
        "internal_bridge_density_percent": internal_bridge_density_percent,
        "internal_bridge_angle_deg": internal_bridge_angle_deg,
        "thick_bridges": thick_bridges,
        "thick_internal_bridges": thick_internal_bridges,
        "extra_bridge_layer_enabled": extra_bridge_layer_enabled,
        "bridge_over_infill_enabled": bridge_over_infill_enabled,
        "bridge_over_infill_min_candidate_ratio": bridge_over_infill_min_candidate_ratio,
        "bridge_over_infill_sample_count": bridge_over_infill_sample_count,
        "bridge_span_strip_geometry_enabled": bridge_span_strip_geometry_enabled,
        "infill_combine_metadata_consumed": False,
        "top_layers": top_layers,
        "bottom_layers": bottom_layers,
        "solid_layer_count": 0,
        "top_solid_layer_count": 0,
        "bottom_solid_layer_count": 0,
        "solid_path_count_total": 0,
        "solid_path_length_mm_total": 0.0,
        "bridge_region_count": bridge_regions,
        "bridge_path_count": bridge_regions,
        "bridge_path_length_mm_total": 0.0,
        "bridge_span_component_count_total": 0,
        "bridge_span_inter_island_edge_count_total": 0,
        "bridge_span_node_count_total": 0,
        "bridge_span_edge_count_total": 0,
        "bridge_candidate_ratio_avg": 0.0,
        "bridge_support_surface_ratio_avg": 0.0,
        "layer_solid_path_counts": [],
        "layer_bridge_region_counts": [],
        "layer_bridge_path_counts": [],
        "layer_bridge_span_component_counts": [],
        "layer_bridge_span_inter_island_edge_counts": [],
        "layer_bridge_span_node_counts_total": [],
        "layer_bridge_span_edge_counts_total": [],
        "layer_bridge_angles_deg": [],
        "layer_bridge_angle_sources": [],
        "layer_bridge_direction_vote_angles_deg": [],
        "layer_bridge_direction_vote_confidences": [],
        "layer_bridge_candidate_ratios": [],
        "layer_bridge_candidate_areas_mm2": [],
        "layer_bridge_candidate_depth_layers": [],
        "layer_bridge_support_surface_ratios": [],
        "layer_infill_combine_target_layers": [],
        "layer_infill_combine_thickness_layers": [],
        "layer_infill_combine_void_depth_layers": [],
        "layer_bridge_unsupported_surface_areas_mm2": [],
        "layer_bridge_span_node_counts": [],
        "layer_bridge_span_edge_counts": [],
        "bridge_span_components": [],
        "layer_classifications": [],
        "warning_count": 1,
        "warnings": ["solid_bridges:fallback_without_islands"],
    }
    _update_parity_artifact(
        context,
        {
            "bridge_region_count": int(bridge_regions),
            "bridge_path_count": int(bridge_regions),
            "bridge_path_length_mm_total": 0.0,
            "bridge_candidate_ratio_avg": 0.0,
            "bridge_support_surface_ratio_avg": 0.0,
        },
    )
    context.stage_artifacts[STAGE_NAME] = artifact
    return artifact
