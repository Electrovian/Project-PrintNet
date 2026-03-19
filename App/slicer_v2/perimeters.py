from __future__ import annotations

from .perimeter_classic import (
    WALL_SEQUENCE_OUTER_TO_INNER,
    build_classic_perimeters,
)
from .perimeter_variable import PERIMETER_MODE_VARIABLE_WIDTH, build_variable_width_perimeters
from .runtime import resolve_worker_count
from .types import SlicerContext


STAGE_NAME = "perimeters"


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


def _to_bool(value: object, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "on", "enabled"}:
        return True
    if text in {"0", "false", "no", "off", "disabled"}:
        return False
    return default


def run(context: SlicerContext) -> dict:
    regions_artifact = context.stage_artifacts.get("regions", {})
    islands_artifact = context.stage_artifacts.get("islands", {})
    perimeter_count = _to_int(context.resolved_settings.get("perimeter_count", 2), 2)
    perimeter_count = max(1, perimeter_count)
    perimeter_mode = str(context.resolved_settings.get("perimeter_mode", "classic")).strip().lower()
    line_width_mm = _to_float(context.resolved_settings.get("extrusion_width", 0.4), 0.4)
    variable_line_width_min = _to_float(
        context.resolved_settings.get("variable_line_width_min", line_width_mm * 0.75),
        line_width_mm * 0.75,
    )
    variable_line_width_max = _to_float(
        context.resolved_settings.get("variable_line_width_max", line_width_mm * 1.25),
        line_width_mm * 1.25,
    )
    wall_sequence = str(context.resolved_settings.get("wall_sequence", WALL_SEQUENCE_OUTER_TO_INNER))
    first_layer_single_wall = bool(context.resolved_settings.get("first_layer_single_wall", False))
    arachne_transition_smoothing = _to_float(
        context.resolved_settings.get("arachne_transition_smoothing", 0.35),
        0.35,
    )
    arachne_junction_compensation_enabled = _to_bool(
        context.resolved_settings.get("arachne_junction_compensation_enabled", True),
        True,
    )
    arachne_junction_sharp_angle_deg = _to_float(
        context.resolved_settings.get("arachne_junction_sharp_angle_deg", 120.0),
        120.0,
    )
    arachne_carryover_cross_island_enabled = _to_bool(
        context.resolved_settings.get("arachne_carryover_cross_island_enabled", False),
        False,
    )
    arachne_carryover_strength = _to_float(
        context.resolved_settings.get("arachne_carryover_strength", -1.0),
        -1.0,
    )

    layer_graphs = islands_artifact.get("layer_graphs", [])
    worker_count = resolve_worker_count(
        context.runtime_settings,
        len(layer_graphs) if isinstance(layer_graphs, list) else 0,
        default=1,
    )
    if isinstance(layer_graphs, list) and layer_graphs:
        if perimeter_mode == PERIMETER_MODE_VARIABLE_WIDTH:
            layer_plans, report = build_variable_width_perimeters(
                layer_graphs,
                perimeter_count=perimeter_count,
                base_line_width_mm=line_width_mm,
                min_line_width_mm=variable_line_width_min,
                max_line_width_mm=variable_line_width_max,
                wall_sequence=wall_sequence,
                first_layer_single_wall=first_layer_single_wall,
                transition_smoothing=arachne_transition_smoothing,
                junction_compensation_enabled=arachne_junction_compensation_enabled,
                junction_sharp_angle_deg=arachne_junction_sharp_angle_deg,
                carryover_cross_island_enabled=arachne_carryover_cross_island_enabled,
                carryover_strength=arachne_carryover_strength,
                max_workers=worker_count,
            )
            artifact = {
                "perimeter_mode": PERIMETER_MODE_VARIABLE_WIDTH,
                "perimeter_count": perimeter_count,
                "line_width_mm": line_width_mm,
                "line_width_min_mm": variable_line_width_min,
                "line_width_max_mm": variable_line_width_max,
                "wall_sequence": report.wall_sequence,
                "arachne_transition_smoothing": arachne_transition_smoothing,
                "arachne_junction_compensation_enabled": arachne_junction_compensation_enabled,
                "arachne_junction_sharp_angle_deg": arachne_junction_sharp_angle_deg,
                "arachne_carryover_cross_island_enabled": arachne_carryover_cross_island_enabled,
                "arachne_carryover_strength": arachne_carryover_strength,
                "perimeter_path_count": int(report.loop_count_total),
                "perimeter_length_mm_total": report.path_length_mm_total,
                "perimeter_transition_count_total": report.transition_count_total,
                "perimeter_transition_length_mm_total": report.transition_length_mm_total,
                "perimeter_junction_count_total": report.junction_count_total,
                "perimeter_half_edge_bead_count_total": report.half_edge_bead_count_total,
                "perimeter_half_edge_redistribution_mm_total": report.half_edge_redistribution_mm_total,
                "perimeter_junction_carryover_event_count_total": report.junction_carryover_event_count_total,
                "perimeter_junction_carryover_ratio_avg": report.junction_carryover_ratio_avg,
                "perimeter_junction_carryover_cross_island_event_count_total": (
                    report.junction_carryover_cross_island_event_count_total
                ),
                "perimeter_junction_carryover_source_island_count_total": (
                    report.junction_carryover_source_island_count_total
                ),
                "layer_perimeter_counts": [plan.loop_count for plan in layer_plans],
                "layer_min_widths_mm": [plan.min_width_mm for plan in layer_plans],
                "layer_max_widths_mm": [plan.max_width_mm for plan in layer_plans],
                "layer_transition_counts": [plan.transition_count for plan in layer_plans],
                "layer_junction_counts": [plan.junction_count for plan in layer_plans],
                "layer_half_edge_bead_counts": [plan.half_edge_bead_count for plan in layer_plans],
                "layer_junction_carryover_event_counts": [plan.junction_carryover_event_count for plan in layer_plans],
                "layer_junction_carryover_cross_island_event_counts": [
                    plan.junction_carryover_cross_island_event_count for plan in layer_plans
                ],
                "layer_junction_carryover_source_island_counts": [
                    plan.junction_carryover_source_island_count for plan in layer_plans
                ],
                "warning_count": report.warning_count,
                "warnings": report.warnings,
                "report": report.to_dict(),
                "layer_plans": layer_plans,
            }
            _update_parity_artifact(
                context,
                {
                    "perimeter_mode": PERIMETER_MODE_VARIABLE_WIDTH,
                    "path_count": int(report.loop_count_total),
                    "path_length_mm_total": float(report.path_length_mm_total),
                    "transition_count_total": int(report.transition_count_total),
                    "junction_count_total": int(report.junction_count_total),
                },
            )
            context.stage_artifacts[STAGE_NAME] = artifact
            return artifact

        layer_plans, report = build_classic_perimeters(
            layer_graphs,
            perimeter_count=perimeter_count,
            line_width_mm=line_width_mm,
            wall_sequence=wall_sequence,
            first_layer_single_wall=first_layer_single_wall,
            max_workers=worker_count,
        )
        path_count = int(report.loop_count_total)
        artifact = {
            "perimeter_mode": "classic",
            "perimeter_count": perimeter_count,
            "line_width_mm": line_width_mm,
            "wall_sequence": report.wall_sequence,
            "perimeter_path_count": path_count,
            "perimeter_length_mm_total": report.path_length_mm_total,
            "layer_perimeter_counts": [plan.loop_count for plan in layer_plans],
            "warning_count": report.warning_count,
            "warnings": report.warnings,
            "report": report.to_dict(),
            "layer_plans": layer_plans,
        }
        _update_parity_artifact(
            context,
            {
                "perimeter_mode": "classic",
                "path_count": int(report.loop_count_total),
                "path_length_mm_total": float(report.path_length_mm_total),
                "transition_count_total": 0,
                "junction_count_total": 0,
            },
        )
        context.stage_artifacts[STAGE_NAME] = artifact
        return artifact

    region_count = _to_int(regions_artifact.get("region_count", 1), 1)
    artifact = {
        "perimeter_mode": perimeter_mode if perimeter_mode == PERIMETER_MODE_VARIABLE_WIDTH else "classic",
        "perimeter_count": perimeter_count,
        "line_width_mm": line_width_mm,
        "line_width_min_mm": variable_line_width_min,
        "line_width_max_mm": variable_line_width_max,
        "wall_sequence": wall_sequence,
        "arachne_transition_smoothing": arachne_transition_smoothing,
        "arachne_junction_compensation_enabled": arachne_junction_compensation_enabled,
        "arachne_junction_sharp_angle_deg": arachne_junction_sharp_angle_deg,
        "arachne_carryover_cross_island_enabled": arachne_carryover_cross_island_enabled,
        "arachne_carryover_strength": arachne_carryover_strength,
        "perimeter_path_count": region_count * perimeter_count,
        "perimeter_length_mm_total": 0.0,
        "perimeter_transition_count_total": 0,
        "perimeter_transition_length_mm_total": 0.0,
        "perimeter_junction_count_total": 0,
        "perimeter_half_edge_bead_count_total": 0,
        "perimeter_half_edge_redistribution_mm_total": 0.0,
        "perimeter_junction_carryover_event_count_total": 0,
        "perimeter_junction_carryover_ratio_avg": 0.0,
        "perimeter_junction_carryover_cross_island_event_count_total": 0,
        "perimeter_junction_carryover_source_island_count_total": 0,
        "layer_perimeter_counts": [],
        "layer_transition_counts": [],
        "layer_junction_counts": [],
        "layer_half_edge_bead_counts": [],
        "layer_junction_carryover_event_counts": [],
        "layer_junction_carryover_cross_island_event_counts": [],
        "layer_junction_carryover_source_island_counts": [],
        "warning_count": 1,
        "warnings": [
            "perimeter_variable:fallback_without_islands"
            if perimeter_mode == PERIMETER_MODE_VARIABLE_WIDTH
            else "perimeter_classic:fallback_without_islands"
        ],
    }
    _update_parity_artifact(
        context,
        {
            "perimeter_mode": artifact["perimeter_mode"],
            "path_count": int(artifact["perimeter_path_count"]),
            "path_length_mm_total": 0.0,
            "transition_count_total": int(artifact["perimeter_transition_count_total"]),
            "junction_count_total": int(artifact["perimeter_junction_count_total"]),
        },
    )
    context.stage_artifacts[STAGE_NAME] = artifact
    return artifact
