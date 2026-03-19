from __future__ import annotations

from .adaptive_layers import MAX_LAYER_COUNT, build_layer_plan
from .types import SlicerContext


STAGE_NAME = "slice_grid"


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


def run(context: SlicerContext) -> dict:
    mesh_artifact = context.stage_artifacts.get("mesh", {})
    layer_height = _to_float(context.resolved_settings.get("layer_height", 0.2), 0.2)
    model_height = _to_float(context.resolved_settings.get("model_height_mm", 20.0), 20.0)
    z_min = _to_float(mesh_artifact.get("z_min_mm", 0.0), 0.0)
    z_max = _to_float(mesh_artifact.get("z_max_mm", 0.0), 0.0)

    if layer_height <= 0:
        layer_height = 0.2
    if z_max > z_min:
        model_height = z_max - z_min
    if model_height <= 0:
        model_height = layer_height

    plan = build_layer_plan(
        context.resolved_settings,
        z_min_mm=z_min,
        z_max_mm=z_max,
        model_height_mm=model_height,
        max_layer_count=MAX_LAYER_COUNT,
    )
    artifact = plan.to_artifact()
    context.stage_artifacts[STAGE_NAME] = artifact
    return artifact
