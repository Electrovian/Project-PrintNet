from __future__ import annotations

from .runtime import resolve_worker_count
from .travel_planning import build_travel_plan
from .types import SlicerContext


STAGE_NAME = "travel"


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
    perimeters_artifact = context.stage_artifacts.get("perimeters", {})
    infill_artifact = context.stage_artifacts.get("infill", {})
    support_artifact = context.stage_artifacts.get("supports", {})
    islands_artifact = context.stage_artifacts.get("islands", {})

    travel_speed = _to_float(context.resolved_settings.get("travel_speed", 150.0), 150.0)
    combing_enabled = bool(context.resolved_settings.get("travel_combing_enabled", True))
    combing_max_detour_ratio = _to_float(
        context.resolved_settings.get("travel_combing_max_detour_ratio", 1.5),
        1.5,
    )
    retract_enabled = bool(context.resolved_settings.get("travel_retract_enabled", True))
    retract_min_travel_mm = _to_float(context.resolved_settings.get("travel_retract_min_travel_mm", 2.0), 2.0)
    z_hop_enabled = bool(context.resolved_settings.get("travel_z_hop_enabled", False))
    z_hop_mm = _to_float(context.resolved_settings.get("travel_z_hop_mm", 0.2), 0.2)

    layer_graphs = islands_artifact.get("layer_graphs", [])
    layer_perimeter_counts = perimeters_artifact.get("layer_perimeter_counts", [])
    layer_infill_counts = infill_artifact.get("layer_infill_counts", [])
    layer_support_counts = support_artifact.get("layer_support_path_counts", [])
    worker_count = resolve_worker_count(
        context.runtime_settings,
        len(layer_graphs) if isinstance(layer_graphs, list) else 0,
        default=1,
    )

    if isinstance(layer_graphs, list) and layer_graphs:
        layer_plans, report = build_travel_plan(
            layer_graphs,
            layer_perimeter_counts=layer_perimeter_counts if isinstance(layer_perimeter_counts, list) else [],
            layer_infill_counts=layer_infill_counts if isinstance(layer_infill_counts, list) else [],
            layer_support_counts=layer_support_counts if isinstance(layer_support_counts, list) else [],
            travel_speed_mm_s=travel_speed,
            combing_enabled=combing_enabled,
            combing_max_detour_ratio=combing_max_detour_ratio,
            retract_enabled=retract_enabled,
            retract_min_travel_mm=retract_min_travel_mm,
            z_hop_enabled=z_hop_enabled,
            z_hop_mm=z_hop_mm,
            max_workers=worker_count,
        )
        artifact = {
            "travel_speed_mm_s": travel_speed,
            "travel_combing_enabled": combing_enabled,
            "travel_combing_max_detour_ratio": combing_max_detour_ratio,
            "travel_retract_enabled": retract_enabled,
            "travel_retract_min_travel_mm": retract_min_travel_mm,
            "travel_z_hop_enabled": z_hop_enabled,
            "travel_z_hop_mm": z_hop_mm,
            "travel_move_count": report.move_count_total,
            "travel_length_mm_total": report.travel_length_mm_total,
            "travel_combed_move_count": report.combed_move_count_total,
            "travel_fallback_move_count": report.fallback_move_count_total,
            "travel_retract_count": report.retract_count_total,
            "travel_z_hop_count": report.z_hop_count_total,
            "layer_travel_move_counts": [plan.move_count for plan in layer_plans],
            "layer_travel_lengths_mm": [plan.travel_length_mm for plan in layer_plans],
            "layer_travel_combed_counts": [plan.combed_move_count for plan in layer_plans],
            "layer_travel_fallback_counts": [plan.fallback_move_count for plan in layer_plans],
            "layer_travel_retract_counts": [plan.retract_count for plan in layer_plans],
            "layer_travel_z_hop_counts": [plan.z_hop_count for plan in layer_plans],
            "warning_count": report.warning_count,
            "warnings": report.warnings,
            "report": report.to_dict(),
            "layer_plans": layer_plans,
        }
        context.stage_artifacts[STAGE_NAME] = artifact
        return artifact

    perimeter_paths = _to_int(perimeters_artifact.get("perimeter_path_count", 0), 0)
    infill_paths = _to_int(infill_artifact.get("infill_path_count", 0), 0)
    support_paths = _to_int(support_artifact.get("support_path_count", 0), 0)
    travel_moves = max(1, perimeter_paths + infill_paths + support_paths)
    warnings: list[str] = []
    if combing_enabled:
        warnings.append("travel_planning:fallback_without_islands")

    artifact = {
        "travel_speed_mm_s": travel_speed,
        "travel_combing_enabled": combing_enabled,
        "travel_combing_max_detour_ratio": combing_max_detour_ratio,
        "travel_retract_enabled": retract_enabled,
        "travel_retract_min_travel_mm": retract_min_travel_mm,
        "travel_z_hop_enabled": z_hop_enabled,
        "travel_z_hop_mm": z_hop_mm,
        "travel_move_count": travel_moves,
        "travel_length_mm_total": 0.0,
        "travel_combed_move_count": 0,
        "travel_fallback_move_count": travel_moves,
        "travel_retract_count": 0,
        "travel_z_hop_count": 0,
        "layer_travel_move_counts": [],
        "layer_travel_lengths_mm": [],
        "layer_travel_combed_counts": [],
        "layer_travel_fallback_counts": [],
        "layer_travel_retract_counts": [],
        "layer_travel_z_hop_counts": [],
        "warning_count": len(warnings),
        "warnings": warnings,
    }
    context.stage_artifacts[STAGE_NAME] = artifact
    return artifact
