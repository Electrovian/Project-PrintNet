from __future__ import annotations

import random

from .extrusion_flow import FEATURE_PERIMETER, build_extrusion_flow_model
from .gcode_emission import emit_gcode_semantics
from .gcode_validation import validate_gcode_semantics
from .geometry import EPSILON
from .runtime import resolve_cpu_threads, resolve_gpu_mode
from .types import SlicerContext


STAGE_NAME = "gcode"


def _parse_float(value: object) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (str, bytes, bytearray)):
        text = str(value).strip()
        if not text:
            return None
        try:
            return float(text)
        except (TypeError, ValueError, OverflowError):
            return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except (TypeError, ValueError, OverflowError):
        return None


def _parse_int(value: object) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return int(value)
    if isinstance(value, float):
        return int(value)
    if isinstance(value, (str, bytes, bytearray)):
        text = str(value).strip()
        if not text:
            return None
        try:
            return int(float(text))
        except (TypeError, ValueError, OverflowError):
            return None
    text = str(value).strip()
    if not text:
        return None
    try:
        return int(float(text))
    except (TypeError, ValueError, OverflowError):
        return None


def _to_float(value: object, default: float) -> float:
    parsed = _parse_float(value)
    if parsed is None:
        return default
    return parsed


def _to_int(value: object, default: int) -> int:
    parsed = _parse_int(value)
    if parsed is None:
        return default
    return parsed


def _collect_layer_heights(
    *,
    slice_grid_artifact: dict,
    default_layer_height: float,
    fallback_layer_count: int,
) -> tuple[list[float], list[float]]:
    raw_heights = slice_grid_artifact.get("layer_heights_mm", [])
    raw_z = slice_grid_artifact.get("layer_z_values_mm", [])

    heights: list[float] = []
    if isinstance(raw_heights, list):
        for value in raw_heights:
            parsed = _parse_float(value)
            if parsed is not None:
                heights.append(parsed)

    z_values: list[float] = []
    if isinstance(raw_z, list):
        for value in raw_z:
            parsed = _parse_float(value)
            if parsed is not None:
                z_values.append(parsed)

    if not heights:
        layer_count = max(1, _to_int(fallback_layer_count, 1))
        heights = [default_layer_height for _ in range(layer_count)]
    return heights, z_values


def _layer_lengths_from_plan_objects(layer_plans: object, attr_name: str) -> list[float]:
    if not isinstance(layer_plans, list):
        return []
    values: list[float] = []
    for plan in layer_plans:
        value = getattr(plan, attr_name, 0.0)
        parsed = _parse_float(value)
        values.append(parsed if parsed is not None else 0.0)
    return values


def _collect_float_list(value: object) -> list[float]:
    if not isinstance(value, list):
        return []
    values: list[float] = []
    for item in value:
        parsed = _parse_float(item)
        values.append(parsed if parsed is not None else 0.0)
    return values


def _collect_int_list(value: object) -> list[int]:
    if not isinstance(value, list):
        return []
    values: list[int] = []
    for item in value:
        parsed = _parse_int(item)
        values.append(parsed if parsed is not None else 0)
    return values


def _macro_value(value: object) -> list[str] | str:
    if isinstance(value, str):
        return value
    if isinstance(value, tuple):
        return [str(item) for item in value]
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def _value_from_mapping_or_attr(value: object, key: str, default: object = None) -> object:
    if isinstance(value, dict):
        return value.get(key, default)
    return getattr(value, key, default)


def _point_xy(item: object) -> tuple[float, float]:
    if isinstance(item, (list, tuple)) and len(item) >= 2:
        return (_to_float(item[0], 0.0), _to_float(item[1], 0.0))
    return (
        _to_float(getattr(item, "x", 0.0), 0.0),
        _to_float(getattr(item, "y", 0.0), 0.0),
    )


def _normalize_loop_points(points: object) -> tuple[tuple[float, float], ...]:
    if not isinstance(points, (list, tuple)):
        return ()
    normalized: list[tuple[float, float]] = []
    for item in points:
        x, y = _point_xy(item)
        if normalized:
            prev_x, prev_y = normalized[-1]
            if abs(prev_x - x) <= EPSILON and abs(prev_y - y) <= EPSILON:
                continue
        normalized.append((x, y))
    if len(normalized) > 1:
        first_x, first_y = normalized[0]
        last_x, last_y = normalized[-1]
        if abs(first_x - last_x) <= EPSILON and abs(first_y - last_y) <= EPSILON:
            normalized.pop()
    if len(normalized) < 3:
        return ()
    return tuple(normalized)


def _layer_polygons(layer_contours: object, layer_index: int) -> list[object]:
    if not isinstance(layer_contours, list):
        return []
    if layer_index < 0 or layer_index >= len(layer_contours):
        return []
    entry = layer_contours[layer_index]
    if not isinstance(entry, list):
        return []
    polygons: list[object] = []
    for candidate in entry:
        centroid = getattr(candidate, "centroid", None)
        points = getattr(candidate, "points", None)
        if centroid is None:
            continue
        if not isinstance(points, tuple):
            continue
        if len(points) < 1:
            continue
        polygons.append(candidate)
    return polygons


def _best_point_index(points: tuple[object, ...], target: tuple[float, float]) -> int:
    best_index = 0
    best_dist = float("inf")
    tx, ty = target
    for idx in range(len(points)):
        px, py = _point_xy(points[idx])
        dist = ((px - tx) ** 2) + ((py - ty) ** 2)
        if dist < best_dist:
            best_dist = dist
            best_index = idx
    return best_index


def _seam_index_for_points(
    *,
    points: tuple[object, ...],
    seam_position: str,
    layer_index: int,
    rng: random.Random,
    aligned_reference: tuple[float, float] | None,
    previous_target: tuple[float, float] | None,
) -> tuple[int, tuple[float, float] | None]:
    if not points:
        return 0, aligned_reference

    strategy = str(seam_position or "aligned").strip().lower()
    if strategy == "random":
        idx = rng.randrange(len(points))
    elif strategy == "rear":
        idx = min(
            range(len(points)),
            key=lambda candidate: (_point_xy(points[candidate])[1], _point_xy(points[candidate])[0]),
        )
    elif strategy == "nearest" and previous_target is not None:
        idx = _best_point_index(points, previous_target)
    elif strategy == "aligned":
        if aligned_reference is None:
            idx = min(
                range(len(points)),
                key=lambda candidate: (_point_xy(points[candidate])[1], _point_xy(points[candidate])[0]),
            )
            aligned_reference = _point_xy(points[idx])
        else:
            idx = _best_point_index(points, aligned_reference)
    else:
        idx = layer_index % len(points)
    return idx, aligned_reference


def _seam_point_for_polygon(
    *,
    points: tuple[object, ...],
    seam_position: str,
    layer_index: int,
    rng: random.Random,
    aligned_reference: tuple[float, float] | None,
    previous_target: tuple[float, float] | None,
) -> tuple[float, float, tuple[float, float] | None]:
    if not points:
        return 0.0, 0.0, aligned_reference

    idx, aligned_reference = _seam_index_for_points(
        points=points,
        seam_position=seam_position,
        layer_index=layer_index,
        rng=rng,
        aligned_reference=aligned_reference,
        previous_target=previous_target,
    )
    x, y = _point_xy(points[idx])
    return x, y, aligned_reference


def _build_layer_xy_targets(
    *,
    regions_artifact: dict,
    mesh_artifact: dict,
    bed_x_mm: float,
    bed_y_mm: float,
    layer_count: int,
    seam_position: str,
    seam_seed: int,
) -> list[tuple[float, float, float, float]]:
    bed_x = max(10.0, float(bed_x_mm))
    bed_y = max(10.0, float(bed_y_mm))
    bed_center_x = bed_x * 0.5
    bed_center_y = bed_y * 0.5
    bed_margin = 0.5

    mesh_x_min = _to_float(mesh_artifact.get("x_min_mm", 0.0), 0.0)
    mesh_x_max = _to_float(mesh_artifact.get("x_max_mm", mesh_x_min), mesh_x_min)
    mesh_y_min = _to_float(mesh_artifact.get("y_min_mm", 0.0), 0.0)
    mesh_y_max = _to_float(mesh_artifact.get("y_max_mm", mesh_y_min), mesh_y_min)
    mesh_center_x = (mesh_x_min + mesh_x_max) * 0.5
    mesh_center_y = (mesh_y_min + mesh_y_max) * 0.5
    mesh_span_x = max(6.0, abs(mesh_x_max - mesh_x_min))
    mesh_span_y = max(6.0, abs(mesh_y_max - mesh_y_min))

    fallback_span_x = max(6.0, min(mesh_span_x, bed_x * 0.6))
    fallback_span_y = max(6.0, min(mesh_span_y, bed_y * 0.6))
    ring_offsets = (
        (1.0, 0.0),
        (1.0, 1.0),
        (0.0, 1.0),
        (-1.0, 1.0),
        (-1.0, 0.0),
        (-1.0, -1.0),
        (0.0, -1.0),
        (1.0, -1.0),
    )

    layer_contours = regions_artifact.get("layer_contours", [])
    seam_mode = str(seam_position or "aligned").strip().lower()
    seam_rng = random.Random(int(seam_seed))
    aligned_reference_xy: tuple[float, float] | None = None
    previous_extrude_xy: tuple[float, float] | None = None
    targets: list[tuple[float, float, float, float]] = []
    for layer_index in range(max(1, int(layer_count))):
        polygons = _layer_polygons(layer_contours, layer_index)

        if polygons:
            chosen = polygons[0]
            chosen_area = _to_float(getattr(chosen, "area", 0.0), 0.0)
            for candidate in polygons[1:]:
                candidate_area = _to_float(getattr(candidate, "area", 0.0), 0.0)
                if candidate_area > chosen_area:
                    chosen = candidate
                    chosen_area = candidate_area

            centroid = getattr(chosen, "centroid", None)
            points = getattr(chosen, "points", ())
            raw_travel_x = _to_float(getattr(centroid, "x", mesh_center_x), mesh_center_x)
            raw_travel_y = _to_float(getattr(centroid, "y", mesh_center_y), mesh_center_y)
            raw_extrude_x, raw_extrude_y, aligned_reference_xy = _seam_point_for_polygon(
                points=points if isinstance(points, tuple) else tuple(),
                seam_position=seam_mode,
                layer_index=layer_index,
                rng=seam_rng,
                aligned_reference=aligned_reference_xy,
                previous_target=previous_extrude_xy,
            )
        else:
            offset = ring_offsets[layer_index % len(ring_offsets)]
            offset_2 = ring_offsets[(layer_index + 2) % len(ring_offsets)]
            raw_travel_x = mesh_center_x + (offset[0] * fallback_span_x * 0.25)
            raw_travel_y = mesh_center_y + (offset[1] * fallback_span_y * 0.25)
            raw_extrude_x = mesh_center_x + (offset_2[0] * fallback_span_x * 0.35)
            raw_extrude_y = mesh_center_y + (offset_2[1] * fallback_span_y * 0.35)

        travel_x = raw_travel_x - mesh_center_x + bed_center_x
        travel_y = raw_travel_y - mesh_center_y + bed_center_y
        extrude_x = raw_extrude_x - mesh_center_x + bed_center_x
        extrude_y = raw_extrude_y - mesh_center_y + bed_center_y

        targets.append((travel_x, travel_y, extrude_x, extrude_y))
        previous_extrude_xy = (extrude_x, extrude_y)

    return targets


def _build_layer_perimeter_paths(
    *,
    perimeters_artifact: dict,
    mesh_artifact: dict,
    bed_x_mm: float,
    bed_y_mm: float,
    layer_count: int,
    seam_position: str,
    seam_seed: int,
) -> list[list[dict[str, object]]]:
    bed_x = max(10.0, float(bed_x_mm))
    bed_y = max(10.0, float(bed_y_mm))
    bed_center_x = bed_x * 0.5
    bed_center_y = bed_y * 0.5

    mesh_x_min = _to_float(mesh_artifact.get("x_min_mm", 0.0), 0.0)
    mesh_x_max = _to_float(mesh_artifact.get("x_max_mm", mesh_x_min), mesh_x_min)
    mesh_y_min = _to_float(mesh_artifact.get("y_min_mm", 0.0), 0.0)
    mesh_y_max = _to_float(mesh_artifact.get("y_max_mm", mesh_y_min), mesh_y_min)
    mesh_center_x = (mesh_x_min + mesh_x_max) * 0.5
    mesh_center_y = (mesh_y_min + mesh_y_max) * 0.5

    raw_layer_plans = perimeters_artifact.get("layer_plans", [])
    if not isinstance(raw_layer_plans, list):
        return [[] for _ in range(max(1, int(layer_count)))]

    loops_by_layer: dict[int, list[object]] = {}
    for fallback_index, plan in enumerate(raw_layer_plans):
        layer_index = _to_int(_value_from_mapping_or_attr(plan, "layer_index", fallback_index), fallback_index)
        loops = _value_from_mapping_or_attr(plan, "loops", [])
        if isinstance(loops, tuple):
            loops_by_layer[layer_index] = list(loops)
        elif isinstance(loops, list):
            loops_by_layer[layer_index] = loops

    seam_mode = str(seam_position or "aligned").strip().lower()
    seam_rng = random.Random(int(seam_seed))
    aligned_reference_xy: tuple[float, float] | None = None
    previous_extrude_xy: tuple[float, float] | None = None

    layer_paths: list[list[dict[str, object]]] = []
    for layer_index in range(max(1, int(layer_count))):
        loops_for_layer = loops_by_layer.get(layer_index, [])
        paths_for_layer: list[dict[str, object]] = []
        for loop in loops_for_layer:
            points = _normalize_loop_points(_value_from_mapping_or_attr(loop, "points", ()))
            if len(points) < 3:
                continue
            seam_index, aligned_reference_xy = _seam_index_for_points(
                points=tuple(points),
                seam_position=seam_mode,
                layer_index=layer_index,
                rng=seam_rng,
                aligned_reference=aligned_reference_xy,
                previous_target=previous_extrude_xy,
            )
            ordered_points = list(points[seam_index:]) + list(points[:seam_index])
            translated_points = tuple(
                (
                    float(point[0] - mesh_center_x + bed_center_x),
                    float(point[1] - mesh_center_y + bed_center_y),
                )
                for point in ordered_points
            )
            paths_for_layer.append(
                {
                    "layer_index": layer_index,
                    "island_index": _to_int(_value_from_mapping_or_attr(loop, "island_index", 0), 0),
                    "role": str(_value_from_mapping_or_attr(loop, "role", "outer")),
                    "shell_index": _to_int(_value_from_mapping_or_attr(loop, "shell_index", 0), 0),
                    "path_length_mm": _to_float(_value_from_mapping_or_attr(loop, "path_length_mm", 0.0), 0.0),
                    "points": translated_points,
                }
            )
            previous_extrude_xy = ordered_points[0]
        layer_paths.append(paths_for_layer)
    return layer_paths


def _feature_metric_values(
    layer_flow_plans: object,
    *,
    feature_name: str,
    attr_name: str,
) -> list[float]:
    if not isinstance(layer_flow_plans, list):
        return []
    normalized_feature = str(feature_name).strip().lower()
    values: list[float] = []
    for layer_plan in layer_flow_plans:
        features = _value_from_mapping_or_attr(layer_plan, "features", [])
        value = 0.0
        if isinstance(features, list):
            for feature in features:
                feature_key = str(_value_from_mapping_or_attr(feature, "feature", "")).strip().lower()
                if feature_key != normalized_feature:
                    continue
                value = _to_float(_value_from_mapping_or_attr(feature, attr_name, 0.0), 0.0)
                break
        values.append(value)
    return values


def run(context: SlicerContext) -> dict:
    mesh_artifact = context.stage_artifacts.get("mesh", {})
    slice_grid_artifact = context.stage_artifacts.get("slice_grid", {})
    regions_artifact = context.stage_artifacts.get("regions", {})
    perimeters_artifact = context.stage_artifacts.get("perimeters", {})
    infill_artifact = context.stage_artifacts.get("infill", {})
    supports_artifact = context.stage_artifacts.get("supports", {})
    bridges_artifact = context.stage_artifacts.get("bridges", {})
    travel_artifact = context.stage_artifacts.get("travel", {})

    print_speed = _to_float(context.resolved_settings.get("print_speed", 60.0), 60.0)
    travel_speed = _to_float(context.resolved_settings.get("travel_speed", 150.0), 150.0)
    layer_height = _to_float(context.resolved_settings.get("layer_height", 0.2), 0.2)
    line_width = _to_float(context.resolved_settings.get("extrusion_width", 0.4), 0.4)
    nozzle_diameter = _to_float(context.resolved_settings.get("nozzle_diameter", 0.4), 0.4)
    filament_diameter = _to_float(context.resolved_settings.get("filament_diameter", 1.75), 1.75)
    flow_multiplier = _to_float(context.resolved_settings.get("flow_multiplier", 1.0), 1.0)
    perimeter_flow_ratio = _to_float(context.resolved_settings.get("perimeter_flow_ratio", 1.0), 1.0)
    infill_flow_ratio = _to_float(context.resolved_settings.get("infill_flow_ratio", 1.0), 1.0)
    support_flow_ratio = _to_float(context.resolved_settings.get("support_flow_ratio", 1.0), 1.0)
    solid_flow_ratio = _to_float(context.resolved_settings.get("solid_flow_ratio", 1.0), 1.0)
    bridge_flow_ratio = _to_float(context.resolved_settings.get("bridge_flow_ratio", 1.0), 1.0)
    filament_density = _to_float(context.resolved_settings.get("filament_density_g_cm3", 1.24), 1.24)
    filament_cost = _to_float(context.resolved_settings.get("filament_cost_usd_per_kg", 0.0), 0.0)
    small_feature_threshold = _to_float(context.resolved_settings.get("small_feature_threshold_mm", 4.0), 4.0)
    small_feature_boost_ratio = _to_float(
        context.resolved_settings.get("small_feature_flow_boost_ratio", 1.05),
        1.05,
    )
    seam_position = str(context.resolved_settings.get("seam_position", "aligned")).strip().lower()
    seam_random_seed = _to_int(context.resolved_settings.get("seam_random_seed", 0), 0)

    perimeter_lengths = _layer_lengths_from_plan_objects(perimeters_artifact.get("layer_plans", []), "path_length_mm")
    infill_lengths = _layer_lengths_from_plan_objects(infill_artifact.get("layer_plans", []), "path_length_mm")
    support_lengths = _layer_lengths_from_plan_objects(supports_artifact.get("layer_plans", []), "support_path_length_mm")
    solid_lengths = _layer_lengths_from_plan_objects(bridges_artifact.get("layer_plans", []), "solid_path_length_mm")
    bridge_lengths = _layer_lengths_from_plan_objects(bridges_artifact.get("layer_plans", []), "bridge_path_length_mm")

    layer_count_fallback = max(
        len(perimeter_lengths),
        len(infill_lengths),
        len(support_lengths),
        len(solid_lengths),
        len(bridge_lengths),
    )
    layer_heights, layer_z_values = _collect_layer_heights(
        slice_grid_artifact=slice_grid_artifact,
        default_layer_height=layer_height,
        fallback_layer_count=layer_count_fallback,
    )
    if layer_z_values:
        min_z = min(layer_z_values)
        if min_z < 0.0:
            z_shift = -min_z
            layer_z_values = [float(z + z_shift) for z in layer_z_values]

    layer_flow_plans, flow_report = build_extrusion_flow_model(
        layer_heights_mm=layer_heights,
        layer_z_values_mm=layer_z_values,
        perimeter_lengths_mm=perimeter_lengths,
        infill_lengths_mm=infill_lengths,
        support_lengths_mm=support_lengths,
        solid_lengths_mm=solid_lengths,
        bridge_lengths_mm=bridge_lengths,
        line_width_mm=line_width,
        nozzle_diameter_mm=nozzle_diameter,
        filament_diameter_mm=filament_diameter,
        flow_multiplier=flow_multiplier,
        perimeter_flow_ratio=perimeter_flow_ratio,
        infill_flow_ratio=infill_flow_ratio,
        support_flow_ratio=support_flow_ratio,
        solid_flow_ratio=solid_flow_ratio,
        bridge_flow_ratio=bridge_flow_ratio,
        filament_density_g_cm3=filament_density,
        filament_cost_usd_per_kg=filament_cost,
        small_feature_threshold_mm=small_feature_threshold,
        small_feature_flow_boost_ratio=small_feature_boost_ratio,
    )

    layer_path_lengths = [plan.path_length_mm_total for plan in layer_flow_plans]
    layer_filament_lengths = [plan.filament_length_mm_total for plan in layer_flow_plans]
    layer_perimeter_filament_lengths = _feature_metric_values(
        layer_flow_plans,
        feature_name=FEATURE_PERIMETER,
        attr_name="filament_length_mm",
    )

    layer_travel_move_counts = _collect_int_list(travel_artifact.get("layer_travel_move_counts", []))
    layer_travel_lengths = _collect_float_list(travel_artifact.get("layer_travel_lengths_mm", []))
    layer_retract_counts = _collect_int_list(travel_artifact.get("layer_travel_retract_counts", []))
    layer_z_hop_counts = _collect_int_list(travel_artifact.get("layer_travel_z_hop_counts", []))

    if not layer_travel_move_counts:
        fallback_move_count = _to_int(travel_artifact.get("travel_move_count", 0), 0)
        if fallback_move_count > 0:
            layer_travel_move_counts = [fallback_move_count]
    if not layer_travel_lengths:
        fallback_travel_length = _to_float(travel_artifact.get("travel_length_mm_total", 0.0), 0.0)
        if fallback_travel_length > 0.0:
            layer_travel_lengths = [fallback_travel_length]

    absolute_extrusion_setting = context.resolved_settings.get("gcode_absolute_extrusion")
    absolute_extrusion = absolute_extrusion_setting if isinstance(absolute_extrusion_setting, bool) else None
    firmware_flavor = str(context.resolved_settings.get("gcode_firmware_flavor", "marlin"))
    startup_macro = _macro_value(context.resolved_settings.get("gcode_startup_macro", ()))
    end_macro = _macro_value(context.resolved_settings.get("gcode_end_macro", ()))
    nozzle_temperature_c = _parse_float(context.resolved_settings.get("nozzle_temperature_c"))
    bed_temperature_c = _parse_float(context.resolved_settings.get("bed_temperature_c"))
    retract_length = _to_float(context.resolved_settings.get("gcode_retract_length_mm", 0.8), 0.8)
    emit_layer_comments = bool(context.resolved_settings.get("gcode_emit_layer_comments", True))
    gcode_validation_enabled = bool(context.resolved_settings.get("gcode_validation_enabled", True))
    gcode_validation_strict = bool(context.resolved_settings.get("gcode_validation_strict", False))
    gcode_validation_bed_x = _to_float(context.resolved_settings.get("gcode_validation_bed_x_mm", 220.0), 220.0)
    gcode_validation_bed_y = _to_float(context.resolved_settings.get("gcode_validation_bed_y_mm", 220.0), 220.0)
    gcode_validation_bed_z = _to_float(context.resolved_settings.get("gcode_validation_bed_z_mm", 250.0), 250.0)
    gcode_validation_require_monotonic_z = bool(
        context.resolved_settings.get("gcode_validation_require_monotonic_z", True)
    )
    gcode_validation_require_monotonic_e = bool(
        context.resolved_settings.get("gcode_validation_require_monotonic_e", True)
    )
    gcode_validation_allow_absolute_retract = bool(
        context.resolved_settings.get("gcode_validation_allow_absolute_retract", True)
    )
    gcode_validation_allow_negative_xy = False
    gcode_validation_line_length_limit = _to_int(
        context.resolved_settings.get("gcode_validation_line_length_limit", 512),
        512,
    )
    gcode_validation_max_line_count = _to_int(
        context.resolved_settings.get("gcode_validation_max_line_count", 250000),
        250000,
    )
    gcode_validation_tolerance_mm = _to_float(
        context.resolved_settings.get("gcode_validation_tolerance_mm", 0.0001),
        0.0001,
    )
    cpu_threads = resolve_cpu_threads(context.runtime_settings, default=1)
    gpu_mode = resolve_gpu_mode(context.runtime_settings, default="auto")
    seam_seed = (
        seam_random_seed
        if seam_random_seed > 0
        else sum((index + 1) * ord(ch) for index, ch in enumerate(str(context.job_id))) % 2_147_483_647
    )
    layer_xy_targets = _build_layer_xy_targets(
        regions_artifact=regions_artifact,
        mesh_artifact=mesh_artifact,
        bed_x_mm=gcode_validation_bed_x,
        bed_y_mm=gcode_validation_bed_y,
        layer_count=len(layer_heights),
        seam_position=seam_position,
        seam_seed=seam_seed,
    )
    layer_perimeter_paths = _build_layer_perimeter_paths(
        perimeters_artifact=perimeters_artifact,
        mesh_artifact=mesh_artifact,
        bed_x_mm=gcode_validation_bed_x,
        bed_y_mm=gcode_validation_bed_y,
        layer_count=len(layer_heights),
        seam_position=seam_position,
        seam_seed=seam_seed,
    )

    layer_gcode_plans, lines, gcode_report = emit_gcode_semantics(
        layer_heights_mm=layer_heights,
        layer_z_values_mm=layer_z_values,
        layer_path_lengths_mm=layer_path_lengths,
        layer_filament_lengths_mm=layer_filament_lengths,
        layer_perimeter_filament_lengths_mm=layer_perimeter_filament_lengths,
        layer_travel_move_counts=layer_travel_move_counts,
        layer_travel_lengths_mm=layer_travel_lengths,
        layer_retract_counts=layer_retract_counts,
        layer_z_hop_counts=layer_z_hop_counts,
        print_speed_mm_s=print_speed,
        travel_speed_mm_s=travel_speed,
        absolute_extrusion=absolute_extrusion,
        firmware_flavor=firmware_flavor,
        startup_macro=startup_macro,
        end_macro=end_macro,
        nozzle_temperature_c=nozzle_temperature_c,
        bed_temperature_c=bed_temperature_c,
        retract_length_mm=retract_length,
        emit_layer_comments=emit_layer_comments,
        bed_x_mm=gcode_validation_bed_x,
        bed_y_mm=gcode_validation_bed_y,
        layer_xy_targets=layer_xy_targets,
        layer_perimeter_paths=layer_perimeter_paths,
    )

    if gcode_validation_enabled:
        validation_report = validate_gcode_semantics(
            lines,
            absolute_extrusion=bool(gcode_report.absolute_extrusion),
            strict=gcode_validation_strict,
            bed_x_mm=gcode_validation_bed_x,
            bed_y_mm=gcode_validation_bed_y,
            bed_z_mm=gcode_validation_bed_z,
            require_monotonic_z=gcode_validation_require_monotonic_z,
            require_monotonic_e=gcode_validation_require_monotonic_e,
            allow_absolute_retract=gcode_validation_allow_absolute_retract,
            allow_negative_xy=gcode_validation_allow_negative_xy,
            line_length_limit=gcode_validation_line_length_limit,
            max_line_count=gcode_validation_max_line_count,
            tolerance_mm=gcode_validation_tolerance_mm,
        )
        validation_payload = validation_report.to_dict()
        validation_ok = bool(validation_report.ok)
        validation_error_count = int(validation_report.error_count)
        validation_warning_count = int(validation_report.warning_count)
    else:
        validation_payload = {
            "ok": True,
            "error_count": 0,
            "warning_count": 0,
            "line_count": len(lines),
            "strict_mode": False,
            "issues": [],
        }
        validation_ok = True
        validation_error_count = 0
        validation_warning_count = 0

    total_travel_length = (
        sum(layer_travel_lengths)
        if layer_travel_lengths
        else _to_float(travel_artifact.get("travel_length_mm_total", 0.0), 0.0)
    )
    estimated_time_seconds = 0.0
    if print_speed > EPSILON:
        estimated_time_seconds += flow_report.path_length_mm_total / print_speed
    if travel_speed > EPSILON:
        estimated_time_seconds += total_travel_length / travel_speed
    estimated_time_seconds = float(max(1.0, estimated_time_seconds))

    artifact = {
        "line_count": len(lines),
        "lines": lines,
        "estimated_time_seconds": estimated_time_seconds,
        "estimated_filament_mm": flow_report.filament_length_mm_total,
        "estimated_mass_g": flow_report.filament_mass_g_total,
        "estimated_cost_usd": flow_report.filament_cost_usd_total,
        "extrusion_path_length_mm_total": flow_report.path_length_mm_total,
        "extrusion_volume_mm3_total": flow_report.volume_mm3_total,
        "layer_path_lengths_mm": layer_path_lengths,
        "layer_extrusion_volumes_mm3": [plan.volume_mm3_total for plan in layer_flow_plans],
        "layer_filament_lengths_mm": [plan.filament_length_mm_total for plan in layer_flow_plans],
        "extrusion_flow_warning_count": flow_report.warning_count,
        "extrusion_flow_warnings": flow_report.warnings,
        "extrusion_flow": flow_report.to_dict(),
        "layer_extrusion_plans": layer_flow_plans,
        "gcode_absolute_extrusion": bool(gcode_report.absolute_extrusion),
        "gcode_firmware_flavor": gcode_report.firmware_flavor,
        "seam_position": seam_position,
        "seam_random_seed": seam_random_seed,
        "layer_xy_targets": layer_xy_targets,
        "layer_perimeter_path_counts": [len(paths) for paths in layer_perimeter_paths],
        "layer_perimeter_paths": layer_perimeter_paths,
        "gcode_command_count_total": gcode_report.command_count_total,
        "gcode_setup_command_count": gcode_report.setup_command_count,
        "gcode_teardown_command_count": gcode_report.teardown_command_count,
        "gcode_travel_command_count_total": gcode_report.travel_command_count_total,
        "gcode_extrusion_command_count_total": gcode_report.extrusion_command_count_total,
        "gcode_retract_command_count_total": gcode_report.retract_command_count_total,
        "gcode_z_hop_command_count_total": gcode_report.z_hop_command_count_total,
        "gcode_warning_count": gcode_report.warning_count,
        "gcode_warnings": gcode_report.warnings,
        "gcode_emission": gcode_report.to_dict(),
        "layer_gcode_plans": layer_gcode_plans,
        "gcode_validation_enabled": gcode_validation_enabled,
        "gcode_validation_ok": validation_ok,
        "gcode_validation_error_count": validation_error_count,
        "gcode_validation_warning_count": validation_warning_count,
        "gcode_validation": validation_payload,
        "cpu_threads": cpu_threads,
        "gpu_mode": gpu_mode,
        "gpu_compute_accelerated": False,
    }
    context.stage_artifacts[STAGE_NAME] = artifact
    parity_artifact = context.stage_artifacts.get("parity")
    if not isinstance(parity_artifact, dict):
        parity_artifact = {}
    parity_artifact["gcode"] = {
        "line_count": int(len(lines)),
        "estimated_time_seconds": float(estimated_time_seconds),
        "estimated_filament_mm": float(flow_report.filament_length_mm_total),
        "path_length_mm_total": float(flow_report.path_length_mm_total),
        "gcode_validation_ok": bool(validation_ok),
        "gcode_validation_error_count": int(validation_error_count),
        "gcode_validation_warning_count": int(validation_warning_count),
    }
    context.stage_artifacts["parity"] = parity_artifact
    return artifact
