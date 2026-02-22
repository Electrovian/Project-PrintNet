from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from math import pi
from typing import Sequence

from .errors import SlicerV2ExtrusionFlowError
from .geometry import EPSILON


FEATURE_PERIMETER = "perimeter"
FEATURE_INFILL = "infill"
FEATURE_SUPPORT = "support"
FEATURE_SOLID = "solid"
FEATURE_BRIDGE = "bridge"
ALLOWED_EXTRUSION_FEATURES = {
    FEATURE_PERIMETER,
    FEATURE_INFILL,
    FEATURE_SUPPORT,
    FEATURE_SOLID,
    FEATURE_BRIDGE,
}


@dataclass
class FeatureExtrusionPlan:
    layer_index: int
    feature: str
    path_length_mm: float
    flow_ratio: float
    volume_mm3: float
    filament_length_mm: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class LayerExtrusionFlowPlan:
    layer_index: int
    layer_height_mm: float
    z_height_mm: float
    path_length_mm_total: float
    volume_mm3_total: float
    filament_length_mm_total: float
    features: list[FeatureExtrusionPlan] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class ExtrusionFlowReport:
    generated_at_utc: str
    layer_count: int
    line_width_mm: float
    nozzle_diameter_mm: float
    filament_diameter_mm: float
    flow_multiplier: float
    perimeter_flow_ratio: float
    infill_flow_ratio: float
    support_flow_ratio: float
    solid_flow_ratio: float
    bridge_flow_ratio: float
    small_feature_threshold_mm: float
    small_feature_flow_boost_ratio: float
    path_length_mm_total: float
    volume_mm3_total: float
    filament_length_mm_total: float
    filament_mass_g_total: float
    filament_cost_usd_total: float
    warning_count: int
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _validate_non_negative_sequence(values: Sequence[float], label: str) -> list[float]:
    parsed = [float(value) for value in values]
    for index, value in enumerate(parsed):
        if value < 0.0:
            raise SlicerV2ExtrusionFlowError(f"EXTRUSION_FLOW_LENGTH_NEGATIVE:{label}:{index}")
    return parsed


def _validate_positive(value: float, code: str) -> float:
    parsed = float(value)
    if parsed <= EPSILON:
        raise SlicerV2ExtrusionFlowError(code)
    return parsed


def _validate_non_negative(value: float, code: str) -> float:
    parsed = float(value)
    if parsed < 0.0:
        raise SlicerV2ExtrusionFlowError(code)
    return parsed


def _validate_ratio(value: float, code: str, minimum: float, maximum: float) -> float:
    parsed = float(value)
    if parsed < minimum or parsed > maximum:
        raise SlicerV2ExtrusionFlowError(code)
    return parsed


def _layer_count(
    layer_heights_mm: Sequence[float],
    perimeter_lengths_mm: Sequence[float],
    infill_lengths_mm: Sequence[float],
    support_lengths_mm: Sequence[float],
    solid_lengths_mm: Sequence[float],
    bridge_lengths_mm: Sequence[float],
) -> int:
    return max(
        len(layer_heights_mm),
        len(perimeter_lengths_mm),
        len(infill_lengths_mm),
        len(support_lengths_mm),
        len(solid_lengths_mm),
        len(bridge_lengths_mm),
    )


def _value_or_zero(values: Sequence[float], index: int) -> float:
    if index < 0 or index >= len(values):
        return 0.0
    return float(values[index])


def _feature_effective_flow(
    *,
    global_flow_multiplier: float,
    feature_flow_ratio: float,
    path_length_mm: float,
    small_feature_threshold_mm: float,
    small_feature_flow_boost_ratio: float,
) -> float:
    effective = global_flow_multiplier * feature_flow_ratio
    if path_length_mm > EPSILON and path_length_mm < small_feature_threshold_mm:
        effective = effective * small_feature_flow_boost_ratio
    return effective


def _volume_from_length(
    *,
    path_length_mm: float,
    line_width_mm: float,
    layer_height_mm: float,
    effective_flow_ratio: float,
) -> float:
    return float(path_length_mm * line_width_mm * layer_height_mm * effective_flow_ratio)


def build_extrusion_flow_model(
    *,
    layer_heights_mm: Sequence[float],
    layer_z_values_mm: Sequence[float],
    perimeter_lengths_mm: Sequence[float],
    infill_lengths_mm: Sequence[float],
    support_lengths_mm: Sequence[float],
    solid_lengths_mm: Sequence[float],
    bridge_lengths_mm: Sequence[float],
    line_width_mm: float,
    nozzle_diameter_mm: float,
    filament_diameter_mm: float,
    flow_multiplier: float = 1.0,
    perimeter_flow_ratio: float = 1.0,
    infill_flow_ratio: float = 1.0,
    support_flow_ratio: float = 1.0,
    solid_flow_ratio: float = 1.0,
    bridge_flow_ratio: float = 1.0,
    filament_density_g_cm3: float = 1.24,
    filament_cost_usd_per_kg: float = 0.0,
    small_feature_threshold_mm: float = 4.0,
    small_feature_flow_boost_ratio: float = 1.05,
) -> tuple[list[LayerExtrusionFlowPlan], ExtrusionFlowReport]:
    heights = _validate_non_negative_sequence(layer_heights_mm, "layer_height")
    z_values = [float(value) for value in layer_z_values_mm]
    perimeter_lengths = _validate_non_negative_sequence(perimeter_lengths_mm, FEATURE_PERIMETER)
    infill_lengths = _validate_non_negative_sequence(infill_lengths_mm, FEATURE_INFILL)
    support_lengths = _validate_non_negative_sequence(support_lengths_mm, FEATURE_SUPPORT)
    solid_lengths = _validate_non_negative_sequence(solid_lengths_mm, FEATURE_SOLID)
    bridge_lengths = _validate_non_negative_sequence(bridge_lengths_mm, FEATURE_BRIDGE)

    width_mm = _validate_positive(line_width_mm, "EXTRUSION_FLOW_LINE_WIDTH_INVALID")
    nozzle_mm = _validate_positive(nozzle_diameter_mm, "EXTRUSION_FLOW_NOZZLE_DIAMETER_INVALID")
    filament_mm = _validate_positive(filament_diameter_mm, "EXTRUSION_FLOW_FILAMENT_DIAMETER_INVALID")
    global_flow = _validate_ratio(flow_multiplier, "EXTRUSION_FLOW_MULTIPLIER_INVALID", 0.1, 3.0)
    perimeter_flow = _validate_ratio(perimeter_flow_ratio, "EXTRUSION_FLOW_PERIMETER_RATIO_INVALID", 0.1, 3.0)
    infill_flow = _validate_ratio(infill_flow_ratio, "EXTRUSION_FLOW_INFILL_RATIO_INVALID", 0.1, 3.0)
    support_flow = _validate_ratio(support_flow_ratio, "EXTRUSION_FLOW_SUPPORT_RATIO_INVALID", 0.1, 3.0)
    solid_flow = _validate_ratio(solid_flow_ratio, "EXTRUSION_FLOW_SOLID_RATIO_INVALID", 0.1, 3.0)
    bridge_flow = _validate_ratio(bridge_flow_ratio, "EXTRUSION_FLOW_BRIDGE_RATIO_INVALID", 0.1, 3.0)
    density_g_cm3 = _validate_non_negative(filament_density_g_cm3, "EXTRUSION_FLOW_FILAMENT_DENSITY_INVALID")
    cost_usd_per_kg = _validate_non_negative(filament_cost_usd_per_kg, "EXTRUSION_FLOW_FILAMENT_COST_INVALID")
    small_threshold_mm = _validate_non_negative(small_feature_threshold_mm, "EXTRUSION_FLOW_SMALL_FEATURE_THRESHOLD_INVALID")
    small_boost = _validate_ratio(
        small_feature_flow_boost_ratio,
        "EXTRUSION_FLOW_SMALL_FEATURE_BOOST_INVALID",
        1.0,
        2.0,
    )

    warnings: list[str] = []
    if width_mm + EPSILON < nozzle_mm * 0.6:
        warnings.append("extrusion_flow:line_width_narrow_vs_nozzle")
    if width_mm > nozzle_mm * 2.0:
        warnings.append("extrusion_flow:line_width_wide_vs_nozzle")

    layer_count = _layer_count(
        heights,
        perimeter_lengths,
        infill_lengths,
        support_lengths,
        solid_lengths,
        bridge_lengths,
    )
    if layer_count == 0:
        warnings.append("extrusion_flow:no_layers")
        layer_count = 1
    if len(heights) == 0:
        heights = [0.2 for _ in range(layer_count)]
        warnings.append("extrusion_flow:default_layer_heights_applied")

    filament_area_mm2 = pi * ((filament_mm * 0.5) ** 2)
    if filament_area_mm2 <= EPSILON:
        raise SlicerV2ExtrusionFlowError("EXTRUSION_FLOW_FILAMENT_AREA_INVALID")

    layer_plans: list[LayerExtrusionFlowPlan] = []
    path_length_total = 0.0
    volume_total = 0.0
    filament_length_total = 0.0

    feature_specs = (
        (FEATURE_PERIMETER, perimeter_lengths, perimeter_flow),
        (FEATURE_INFILL, infill_lengths, infill_flow),
        (FEATURE_SUPPORT, support_lengths, support_flow),
        (FEATURE_SOLID, solid_lengths, solid_flow),
        (FEATURE_BRIDGE, bridge_lengths, bridge_flow),
    )

    for layer_index in range(layer_count):
        layer_height = _value_or_zero(heights, layer_index)
        if layer_height <= EPSILON:
            layer_height = heights[-1] if heights else 0.2

        z_height = _value_or_zero(z_values, layer_index)
        if z_height <= EPSILON:
            z_height = (layer_index + 0.5) * layer_height

        features: list[FeatureExtrusionPlan] = []
        layer_path_length = 0.0
        layer_volume = 0.0
        layer_filament_length = 0.0

        for feature_name, feature_lengths, feature_ratio in feature_specs:
            feature_length = _value_or_zero(feature_lengths, layer_index)
            effective_flow = _feature_effective_flow(
                global_flow_multiplier=global_flow,
                feature_flow_ratio=feature_ratio,
                path_length_mm=feature_length,
                small_feature_threshold_mm=small_threshold_mm,
                small_feature_flow_boost_ratio=small_boost,
            )
            feature_volume = _volume_from_length(
                path_length_mm=feature_length,
                line_width_mm=width_mm,
                layer_height_mm=layer_height,
                effective_flow_ratio=effective_flow,
            )
            feature_filament_length = 0.0
            if feature_volume > EPSILON:
                feature_filament_length = feature_volume / filament_area_mm2

            features.append(
                FeatureExtrusionPlan(
                    layer_index=layer_index,
                    feature=feature_name,
                    path_length_mm=float(feature_length),
                    flow_ratio=float(effective_flow),
                    volume_mm3=float(feature_volume),
                    filament_length_mm=float(feature_filament_length),
                )
            )

            layer_path_length += feature_length
            layer_volume += feature_volume
            layer_filament_length += feature_filament_length

        layer_plans.append(
            LayerExtrusionFlowPlan(
                layer_index=layer_index,
                layer_height_mm=float(layer_height),
                z_height_mm=float(z_height),
                path_length_mm_total=float(layer_path_length),
                volume_mm3_total=float(layer_volume),
                filament_length_mm_total=float(layer_filament_length),
                features=features,
            )
        )

        path_length_total += layer_path_length
        volume_total += layer_volume
        filament_length_total += layer_filament_length

    if path_length_total <= EPSILON:
        warnings.append("extrusion_flow:no_path_length")

    mass_g_total = float((volume_total / 1000.0) * density_g_cm3)
    cost_total = float((mass_g_total / 1000.0) * cost_usd_per_kg)

    report = ExtrusionFlowReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        layer_count=layer_count,
        line_width_mm=float(width_mm),
        nozzle_diameter_mm=float(nozzle_mm),
        filament_diameter_mm=float(filament_mm),
        flow_multiplier=float(global_flow),
        perimeter_flow_ratio=float(perimeter_flow),
        infill_flow_ratio=float(infill_flow),
        support_flow_ratio=float(support_flow),
        solid_flow_ratio=float(solid_flow),
        bridge_flow_ratio=float(bridge_flow),
        small_feature_threshold_mm=float(small_threshold_mm),
        small_feature_flow_boost_ratio=float(small_boost),
        path_length_mm_total=float(path_length_total),
        volume_mm3_total=float(volume_total),
        filament_length_mm_total=float(filament_length_total),
        filament_mass_g_total=mass_g_total,
        filament_cost_usd_total=cost_total,
        warning_count=len(warnings),
        warnings=warnings,
    )
    return layer_plans, report
