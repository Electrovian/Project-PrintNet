from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field

from .errors import SlicerV2AdaptiveLayerError


MAX_LAYER_COUNT = 2000
EPSILON = 1e-6
MM_ROUND_DIGITS = 4


@dataclass(frozen=True)
class AdaptiveLayerRange:
    z_min_mm: float
    z_max_mm: float
    layer_height_mm: float

    def contains(self, z_value_mm: float) -> bool:
        return (self.z_min_mm - EPSILON) <= z_value_mm <= (self.z_max_mm + EPSILON)


@dataclass
class AdaptiveLayerPlanReport:
    strategy: str
    layer_count: int
    model_height_mm: float
    z_min_mm: float
    z_max_mm: float
    base_layer_height_mm: float
    min_layer_height_mm: float
    max_layer_height_mm: float
    top_bottom_refine_mm: float
    manual_range_count: int
    manual_adjustment_count: int
    boundary_adjustment_count: int
    warning_count: int
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class AdaptiveLayerPlan:
    layer_heights_mm: list[float]
    layer_z_values_mm: list[float]
    report: AdaptiveLayerPlanReport

    def to_artifact(self) -> dict[str, object]:
        return {
            "layer_height_mm": round(self.report.base_layer_height_mm, MM_ROUND_DIGITS),
            "layer_count": self.report.layer_count,
            "layer_heights_mm": [round(value, MM_ROUND_DIGITS) for value in self.layer_heights_mm],
            "z_min_mm": round(self.report.z_min_mm, MM_ROUND_DIGITS),
            "z_max_mm": round(self.report.z_max_mm, MM_ROUND_DIGITS),
            "model_height_mm": round(self.report.model_height_mm, MM_ROUND_DIGITS),
            "layer_z_values_mm": [round(value, MM_ROUND_DIGITS) for value in self.layer_z_values_mm],
            "adaptive_layering_enabled": self.report.strategy == "adaptive",
            "adaptive_layering_strategy": self.report.strategy,
            "adaptive_layer_report": self.report.to_dict(),
        }


def _to_float(value: object, fallback: float) -> float:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text:
        return fallback
    try:
        return float(text)
    except (TypeError, ValueError):
        return fallback


def _sanitize_bounds(
    *,
    z_min_mm: float,
    z_max_mm: float,
    model_height_mm: float,
    base_layer_height_mm: float,
) -> tuple[float, float, float]:
    z_start = _to_float(z_min_mm, 0.0)
    z_end = _to_float(z_max_mm, z_start)
    model_height = _to_float(model_height_mm, base_layer_height_mm)

    if z_end > z_start + EPSILON:
        model_height = z_end - z_start
    elif model_height > EPSILON:
        z_end = z_start + model_height
    else:
        z_end = z_start + base_layer_height_mm
        model_height = base_layer_height_mm

    if z_end <= z_start + EPSILON:
        raise SlicerV2AdaptiveLayerError("ADAPTIVE_LAYER_INVALID_Z_BOUNDS")

    return z_start, z_end, model_height


def _normalize_ranges(
    raw_ranges: object,
    *,
    min_layer_height_mm: float,
    max_layer_height_mm: float,
    warnings: list[str],
) -> list[AdaptiveLayerRange]:
    parsed_ranges = raw_ranges
    if isinstance(raw_ranges, str):
        text = raw_ranges.strip()
        if not text:
            return []
        try:
            parsed_ranges = json.loads(text)
        except (TypeError, ValueError):
            warnings.append("adaptive_layer_ranges:invalid_json")
            return []
    if isinstance(parsed_ranges, tuple):
        parsed_ranges = list(parsed_ranges)
    if not isinstance(parsed_ranges, list):
        if raw_ranges:
            warnings.append("adaptive_layer_ranges:not_list")
        return []

    normalized_ranges: list[AdaptiveLayerRange] = []
    for index, item in enumerate(parsed_ranges):
        if not isinstance(item, dict):
            warnings.append(f"adaptive_layer_ranges[{index}]:invalid_item")
            continue
        z_min = _to_float(item.get("z_min_mm", item.get("z_min", item.get("start", 0.0))), 0.0)
        z_max = _to_float(item.get("z_max_mm", item.get("z_max", item.get("end", 0.0))), 0.0)
        layer_height = _to_float(
            item.get("layer_height_mm", item.get("layer_height", item.get("height", 0.0))),
            0.0,
        )

        if z_max <= z_min + EPSILON:
            warnings.append(f"adaptive_layer_ranges[{index}]:invalid_z_window")
            continue
        if layer_height <= EPSILON:
            warnings.append(f"adaptive_layer_ranges[{index}]:invalid_layer_height")
            continue
        clamped_height = max(min_layer_height_mm, min(max_layer_height_mm, layer_height))
        normalized_ranges.append(AdaptiveLayerRange(z_min_mm=z_min, z_max_mm=z_max, layer_height_mm=clamped_height))

    normalized_ranges.sort(key=lambda item: (item.z_min_mm, item.z_max_mm, item.layer_height_mm))
    return normalized_ranges


def _resolve_range_target_height(
    *,
    z_value_mm: float,
    ranges: list[AdaptiveLayerRange],
) -> float | None:
    selected_height: float | None = None
    for item in ranges:
        if not item.contains(z_value_mm):
            continue
        if selected_height is None or item.layer_height_mm < selected_height:
            selected_height = item.layer_height_mm
    return selected_height


def _build_layer_heights(
    *,
    z_start_mm: float,
    z_end_mm: float,
    base_layer_height_mm: float,
    min_layer_height_mm: float,
    max_layer_height_mm: float,
    top_bottom_refine_mm: float,
    use_adaptive: bool,
    ranges: list[AdaptiveLayerRange],
    max_layer_count: int,
) -> tuple[list[float], int, int]:
    heights: list[float] = []
    current_z = z_start_mm
    manual_adjustment_count = 0
    boundary_adjustment_count = 0

    for _layer_index in range(max_layer_count):
        remaining = z_end_mm - current_z
        if remaining <= EPSILON:
            break

        target_height = base_layer_height_mm
        if use_adaptive:
            target_height = max_layer_height_mm
            midpoint = current_z + min(target_height, remaining) * 0.5
            range_target = _resolve_range_target_height(z_value_mm=midpoint, ranges=ranges)
            if range_target is not None and range_target + EPSILON < target_height:
                target_height = range_target
                manual_adjustment_count += 1

            if top_bottom_refine_mm > EPSILON:
                distance_from_bottom = current_z - z_start_mm
                distance_from_top = z_end_mm - current_z
                if distance_from_bottom < top_bottom_refine_mm or distance_from_top < top_bottom_refine_mm:
                    if target_height > min_layer_height_mm + EPSILON:
                        boundary_adjustment_count += 1
                    target_height = min(target_height, min_layer_height_mm)

        target_height = max(min_layer_height_mm, min(max_layer_height_mm, target_height))
        target_height = min(target_height, remaining)

        remaining_after = remaining - target_height
        if remaining_after > EPSILON and remaining_after < (min_layer_height_mm - EPSILON):
            adjusted = remaining - min_layer_height_mm
            if min_layer_height_mm <= adjusted <= max_layer_height_mm:
                target_height = adjusted
            else:
                target_height = remaining

        if target_height <= EPSILON:
            raise SlicerV2AdaptiveLayerError("ADAPTIVE_LAYER_TARGET_NON_POSITIVE")

        heights.append(target_height)
        current_z += target_height

    if z_end_mm - current_z > 1e-4:
        raise SlicerV2AdaptiveLayerError("ADAPTIVE_LAYER_MAX_COUNT_EXCEEDED")

    if heights:
        closure_delta = z_end_mm - current_z
        if abs(closure_delta) > EPSILON:
            corrected_last = heights[-1] + closure_delta
            if corrected_last <= EPSILON:
                raise SlicerV2AdaptiveLayerError("ADAPTIVE_LAYER_CLOSURE_INVALID")
            heights[-1] = corrected_last

    return heights, manual_adjustment_count, boundary_adjustment_count


def _build_layer_centers(z_min_mm: float, layer_heights_mm: list[float]) -> list[float]:
    centers: list[float] = []
    current_z = z_min_mm
    for layer_height in layer_heights_mm:
        centers.append(current_z + (layer_height * 0.5))
        current_z += layer_height
    return centers


def build_layer_plan(
    resolved_settings: dict[str, object] | None,
    *,
    z_min_mm: float,
    z_max_mm: float,
    model_height_mm: float,
    max_layer_count: int = MAX_LAYER_COUNT,
) -> AdaptiveLayerPlan:
    if not isinstance(resolved_settings, dict):
        raise SlicerV2AdaptiveLayerError("ADAPTIVE_LAYER_SETTINGS_NOT_DICT")
    if max_layer_count < 1:
        raise SlicerV2AdaptiveLayerError("ADAPTIVE_LAYER_MAX_COUNT_INVALID")

    base_layer_height = _to_float(resolved_settings.get("layer_height", 0.2), 0.2)
    if base_layer_height <= EPSILON:
        raise SlicerV2AdaptiveLayerError("ADAPTIVE_LAYER_BASE_HEIGHT_INVALID")

    z_start, z_end, resolved_height = _sanitize_bounds(
        z_min_mm=z_min_mm,
        z_max_mm=z_max_mm,
        model_height_mm=model_height_mm,
        base_layer_height_mm=base_layer_height,
    )

    adaptive_enabled = bool(resolved_settings.get("adaptive_layering_enabled", False))
    min_layer_height = _to_float(resolved_settings.get("adaptive_layer_min", base_layer_height), base_layer_height)
    max_layer_height = _to_float(resolved_settings.get("adaptive_layer_max", base_layer_height), base_layer_height)
    top_bottom_refine = _to_float(resolved_settings.get("adaptive_top_bottom_refine_mm", 0.0), 0.0)

    if min_layer_height <= EPSILON or max_layer_height <= EPSILON:
        raise SlicerV2AdaptiveLayerError("ADAPTIVE_LAYER_MIN_MAX_NON_POSITIVE")
    if min_layer_height > max_layer_height:
        raise SlicerV2AdaptiveLayerError("ADAPTIVE_LAYER_MIN_GREATER_THAN_MAX")

    warnings: list[str] = []
    manual_ranges = _normalize_ranges(
        resolved_settings.get("adaptive_layer_ranges", ()),
        min_layer_height_mm=min_layer_height,
        max_layer_height_mm=max_layer_height,
        warnings=warnings,
    )

    use_adaptive = adaptive_enabled or bool(manual_ranges) or top_bottom_refine > EPSILON
    strategy = "adaptive" if use_adaptive else "fixed"
    if not use_adaptive:
        min_layer_height = base_layer_height
        max_layer_height = base_layer_height
        top_bottom_refine = 0.0

    layer_heights, manual_adjustment_count, boundary_adjustment_count = _build_layer_heights(
        z_start_mm=z_start,
        z_end_mm=z_end,
        base_layer_height_mm=base_layer_height,
        min_layer_height_mm=min_layer_height,
        max_layer_height_mm=max_layer_height,
        top_bottom_refine_mm=max(0.0, top_bottom_refine),
        use_adaptive=use_adaptive,
        ranges=manual_ranges,
        max_layer_count=max_layer_count,
    )
    layer_z_values = _build_layer_centers(z_start, layer_heights)

    report = AdaptiveLayerPlanReport(
        strategy=strategy,
        layer_count=len(layer_heights),
        model_height_mm=resolved_height,
        z_min_mm=z_start,
        z_max_mm=z_end,
        base_layer_height_mm=base_layer_height,
        min_layer_height_mm=min_layer_height,
        max_layer_height_mm=max_layer_height,
        top_bottom_refine_mm=max(0.0, top_bottom_refine),
        manual_range_count=len(manual_ranges),
        manual_adjustment_count=manual_adjustment_count,
        boundary_adjustment_count=boundary_adjustment_count,
        warning_count=len(warnings),
        warnings=warnings,
    )

    return AdaptiveLayerPlan(layer_heights_mm=layer_heights, layer_z_values_mm=layer_z_values, report=report)

