from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from math import hypot
from typing import Sequence

from .errors import SlicerV2GCodeEmissionError
from .gcode_contract import build_output_contract, build_setup_lines, build_teardown_lines
from .geometry import EPSILON


FIRMWARE_MARLIN = "marlin"
FIRMWARE_KLIPPER = "klipper"
FIRMWARE_PRUSALINK = "prusalink"
FIRMWARE_GENERIC = "generic"
ALLOWED_FIRMWARE_FLAVORS = {
    FIRMWARE_MARLIN,
    FIRMWARE_KLIPPER,
    FIRMWARE_PRUSALINK,
    FIRMWARE_GENERIC,
}

MAX_LAYER_COUNT = 5000
MAX_MACRO_LINES = 200


@dataclass
class GCodeCommandPlan:
    line_number: int
    command: str
    semantic_tag: str
    layer_index: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class LayerGCodePlan:
    layer_index: int
    z_height_mm: float
    command_count: int
    travel_command_count: int
    extrusion_command_count: int
    retract_command_count: int
    z_hop_command_count: int
    filament_length_mm: float
    commands: list[GCodeCommandPlan] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class GCodeEmissionReport:
    generated_at_utc: str
    layer_count: int
    command_count_total: int
    setup_command_count: int
    teardown_command_count: int
    travel_command_count_total: int
    extrusion_command_count_total: int
    retract_command_count_total: int
    z_hop_command_count_total: int
    filament_length_mm_total: float
    absolute_extrusion: bool
    firmware_flavor: str
    startup_macro_line_count: int
    end_macro_line_count: int
    warning_count: int
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _validate_float_sequence(values: Sequence[float], label: str, *, allow_zero: bool = True) -> list[float]:
    parsed: list[float] = []
    for index, value in enumerate(values):
        try:
            parsed_value = float(value)
        except (TypeError, ValueError) as exc:
            raise SlicerV2GCodeEmissionError(f"GCODE_EMISSION_SEQUENCE_NON_NUMERIC:{label}:{index}") from exc
        if allow_zero:
            if parsed_value < 0.0:
                raise SlicerV2GCodeEmissionError(f"GCODE_EMISSION_SEQUENCE_NEGATIVE:{label}:{index}")
        elif parsed_value <= EPSILON:
            raise SlicerV2GCodeEmissionError(f"GCODE_EMISSION_SEQUENCE_NON_POSITIVE:{label}:{index}")
        parsed.append(parsed_value)
    return parsed


def _validate_int_sequence(values: Sequence[int], label: str) -> list[int]:
    parsed: list[int] = []
    for index, value in enumerate(values):
        parsed_value = int(value)
        if parsed_value < 0:
            raise SlicerV2GCodeEmissionError(f"GCODE_EMISSION_SEQUENCE_NEGATIVE:{label}:{index}")
        parsed.append(parsed_value)
    return parsed


def _validate_speed(value: float, code: str) -> float:
    speed = float(value)
    if speed <= EPSILON:
        raise SlicerV2GCodeEmissionError(code)
    if speed > 3000.0:
        raise SlicerV2GCodeEmissionError(code)
    return speed


def _validate_ratio(value: float, code: str, minimum: float, maximum: float) -> float:
    parsed = float(value)
    if parsed < minimum or parsed > maximum:
        raise SlicerV2GCodeEmissionError(code)
    return parsed


def _validate_firmware(value: str) -> str:
    normalized = str(value).strip().lower()
    if normalized not in ALLOWED_FIRMWARE_FLAVORS:
        raise SlicerV2GCodeEmissionError(f"GCODE_EMISSION_FIRMWARE_UNSUPPORTED:{value}")
    return normalized


def _normalize_macro_lines(value: Sequence[str] | str, label: str) -> list[str]:
    lines: list[str] = []
    if isinstance(value, str):
        split = value.splitlines()
    elif isinstance(value, tuple):
        split = list(value)
    elif isinstance(value, list):
        split = value
    else:
        raise SlicerV2GCodeEmissionError(f"GCODE_EMISSION_MACRO_INVALID_TYPE:{label}")

    for index, item in enumerate(split):
        text = str(item).strip()
        if not text:
            continue
        if "\n" in text or "\r" in text:
            raise SlicerV2GCodeEmissionError(f"GCODE_EMISSION_MACRO_INVALID_NEWLINE:{label}:{index}")
        lines.append(text)

    if len(lines) > MAX_MACRO_LINES:
        raise SlicerV2GCodeEmissionError(f"GCODE_EMISSION_MACRO_TOO_LONG:{label}")
    return lines


def _value_or_default(values: Sequence[float], index: int, default: float) -> float:
    if index < 0 or index >= len(values):
        return default
    return float(values[index])


def _int_or_default(values: Sequence[int], index: int, default: int) -> int:
    if index < 0 or index >= len(values):
        return default
    return int(values[index])


def _normalize_xy_targets(layer_xy_targets: Sequence[tuple[float, float, float, float]]) -> list[tuple[float, float, float, float]]:
    normalized: list[tuple[float, float, float, float]] = []
    for target in layer_xy_targets:
        if not isinstance(target, tuple):
            continue
        if len(target) < 4:
            continue
        travel_x = float(target[0])
        travel_y = float(target[1])
        extrude_x = float(target[2])
        extrude_y = float(target[3])
        normalized.append((travel_x, travel_y, extrude_x, extrude_y))
    return normalized


def _point_xy(item: object) -> tuple[float, float] | None:
    if isinstance(item, (list, tuple)) and len(item) >= 2:
        return (float(item[0]), float(item[1]))
    if isinstance(item, dict) and "x" in item and "y" in item:
        return (float(item["x"]), float(item["y"]))
    if hasattr(item, "x") and hasattr(item, "y"):
        return (float(getattr(item, "x")), float(getattr(item, "y")))
    return None


def _normalize_point_sequence(points: object) -> tuple[tuple[float, float], ...]:
    if not isinstance(points, (list, tuple)):
        return ()
    normalized: list[tuple[float, float]] = []
    for item in points:
        point = _point_xy(item)
        if point is None:
            continue
        if normalized:
            prev_x, prev_y = normalized[-1]
            if abs(prev_x - point[0]) <= EPSILON and abs(prev_y - point[1]) <= EPSILON:
                continue
        normalized.append(point)
    if len(normalized) > 1:
        first_x, first_y = normalized[0]
        last_x, last_y = normalized[-1]
        if abs(first_x - last_x) <= EPSILON and abs(first_y - last_y) <= EPSILON:
            normalized.pop()
    if len(normalized) < 2:
        return ()
    return tuple(normalized)


def _normalize_perimeter_paths(
    layer_perimeter_paths: Sequence[Sequence[object]],
) -> list[list[tuple[float, tuple[tuple[float, float], ...]]]]:
    normalized: list[list[tuple[float, tuple[tuple[float, float], ...]]]] = []
    for layer_entry in layer_perimeter_paths:
        layer_paths: list[tuple[float, tuple[tuple[float, float], ...]]] = []
        if not isinstance(layer_entry, (list, tuple)):
            normalized.append(layer_paths)
            continue
        for raw_path in layer_entry:
            if isinstance(raw_path, dict):
                planned_length = float(raw_path.get("path_length_mm", 0.0))
                points = _normalize_point_sequence(raw_path.get("points", ()))
            else:
                planned_length = float(getattr(raw_path, "path_length_mm", 0.0))
                points = _normalize_point_sequence(getattr(raw_path, "points", ()))
            if len(points) < 2:
                continue
            layer_paths.append((max(0.0, planned_length), points))
        normalized.append(layer_paths)
    return normalized


def _closed_loop_points(points: tuple[tuple[float, float], ...]) -> tuple[tuple[float, float], ...]:
    if len(points) < 2:
        return points
    first_x, first_y = points[0]
    last_x, last_y = points[-1]
    if abs(first_x - last_x) <= EPSILON and abs(first_y - last_y) <= EPSILON:
        return points
    return points + (points[0],)


def _segment_lengths(points: tuple[tuple[float, float], ...]) -> list[float]:
    lengths: list[float] = []
    for index in range(len(points) - 1):
        start_x, start_y = points[index]
        end_x, end_y = points[index + 1]
        lengths.append(float(hypot(end_x - start_x, end_y - start_y)))
    return lengths


def _layer_count(
    layer_heights_mm: Sequence[float],
    layer_z_values_mm: Sequence[float],
    layer_path_lengths_mm: Sequence[float],
    layer_filament_lengths_mm: Sequence[float],
    layer_perimeter_filament_lengths_mm: Sequence[float],
    layer_travel_move_counts: Sequence[int],
    layer_travel_lengths_mm: Sequence[float],
    layer_perimeter_paths: Sequence[Sequence[object]],
) -> int:
    return max(
        len(layer_heights_mm),
        len(layer_z_values_mm),
        len(layer_path_lengths_mm),
        len(layer_filament_lengths_mm),
        len(layer_perimeter_filament_lengths_mm),
        len(layer_travel_move_counts),
        len(layer_travel_lengths_mm),
        len(layer_perimeter_paths),
    )


def emit_gcode_semantics(
    *,
    layer_heights_mm: Sequence[float],
    layer_z_values_mm: Sequence[float],
    layer_path_lengths_mm: Sequence[float],
    layer_filament_lengths_mm: Sequence[float],
    layer_perimeter_filament_lengths_mm: Sequence[float] = (),
    layer_travel_move_counts: Sequence[int],
    layer_travel_lengths_mm: Sequence[float],
    layer_retract_counts: Sequence[int] = (),
    layer_z_hop_counts: Sequence[int] = (),
    print_speed_mm_s: float,
    travel_speed_mm_s: float,
    absolute_extrusion: bool | None = None,
    firmware_flavor: str = FIRMWARE_MARLIN,
    startup_macro: Sequence[str] | str = (),
    end_macro: Sequence[str] | str = (),
    nozzle_temperature_c: float | None = None,
    bed_temperature_c: float | None = None,
    retract_length_mm: float = 0.8,
    emit_layer_comments: bool = True,
    bed_x_mm: float = 220.0,
    bed_y_mm: float = 220.0,
    layer_xy_targets: Sequence[tuple[float, float, float, float]] = (),
    layer_perimeter_paths: Sequence[Sequence[object]] = (),
) -> tuple[list[LayerGCodePlan], list[str], GCodeEmissionReport]:
    heights = _validate_float_sequence(layer_heights_mm, "layer_height")
    z_values = _validate_float_sequence(layer_z_values_mm, "layer_z")
    path_lengths = _validate_float_sequence(layer_path_lengths_mm, "path_length")
    filament_lengths = _validate_float_sequence(layer_filament_lengths_mm, "filament_length")
    perimeter_filament_lengths = _validate_float_sequence(
        layer_perimeter_filament_lengths_mm,
        "perimeter_filament_length",
    )
    travel_move_counts = _validate_int_sequence(layer_travel_move_counts, "travel_move_count")
    travel_lengths = _validate_float_sequence(layer_travel_lengths_mm, "travel_length")
    retract_counts = _validate_int_sequence(layer_retract_counts, "retract_count")
    z_hop_counts = _validate_int_sequence(layer_z_hop_counts, "z_hop_count")

    print_speed = _validate_speed(print_speed_mm_s, "GCODE_EMISSION_PRINT_SPEED_INVALID")
    travel_speed = _validate_speed(travel_speed_mm_s, "GCODE_EMISSION_TRAVEL_SPEED_INVALID")
    retract_length = _validate_ratio(
        retract_length_mm,
        "GCODE_EMISSION_RETRACT_LENGTH_INVALID",
        0.0,
        20.0,
    )
    firmware = _validate_firmware(firmware_flavor)
    startup_lines = _normalize_macro_lines(startup_macro, "startup")
    end_lines = _normalize_macro_lines(end_macro, "end")
    bed_x = _validate_ratio(bed_x_mm, "GCODE_EMISSION_BED_X_INVALID", 1.0, 10000.0)
    bed_y = _validate_ratio(bed_y_mm, "GCODE_EMISSION_BED_Y_INVALID", 1.0, 10000.0)
    output_contract = build_output_contract(
        bed_x_mm=bed_x,
        bed_y_mm=bed_y,
        firmware_flavor=firmware,
        absolute_extrusion=absolute_extrusion,
        startup_macro=startup_lines,
        end_macro=end_lines,
        nozzle_temperature_c=nozzle_temperature_c,
        bed_temperature_c=bed_temperature_c,
    )
    absolute_extrusion = output_contract.absolute_extrusion
    firmware = output_contract.firmware_flavor
    xy_targets = _normalize_xy_targets(layer_xy_targets)
    perimeter_paths_by_layer = _normalize_perimeter_paths(layer_perimeter_paths)

    layer_count = _layer_count(
        heights,
        z_values,
        path_lengths,
        filament_lengths,
        perimeter_filament_lengths,
        travel_move_counts,
        travel_lengths,
        perimeter_paths_by_layer,
    )
    if layer_count <= 0:
        layer_count = 1
        heights = [0.2]
    if layer_count > MAX_LAYER_COUNT:
        raise SlicerV2GCodeEmissionError("GCODE_EMISSION_LAYER_COUNT_EXCESSIVE")

    warnings: list[str] = []
    if len(heights) < layer_count:
        warnings.append("gcode_emission:layer_heights_short")
    if len(z_values) < layer_count:
        warnings.append("gcode_emission:layer_z_values_short")
    if len(filament_lengths) < layer_count:
        warnings.append("gcode_emission:layer_filament_lengths_short")

    lines: list[str] = []
    layer_plans: list[LayerGCodePlan] = []
    line_number = 0
    e_position = 0.0
    margin = max(0.5, min(5.0, min(bed_x, bed_y) * 0.02))
    span_x = max(1.0, bed_x - (margin * 2.0))
    span_y = max(1.0, bed_y - (margin * 2.0))
    virtual_x = margin
    virtual_y = margin

    setup_lines = build_setup_lines(
        output_contract,
        header_comment="EON-OpenSlicer slicer_v2 semantic emitter",
    )
    lines.extend(setup_lines)
    line_number += len(setup_lines)

    travel_feed = float(travel_speed * 60.0)
    print_feed = float(print_speed * 60.0)

    travel_command_count_total = 0
    extrusion_command_count_total = 0
    retract_command_count_total = 0
    z_hop_command_count_total = 0
    filament_length_total = 0.0

    current_z = 0.0
    for layer_index in range(layer_count):
        layer_commands: list[GCodeCommandPlan] = []
        command_count = 0
        travel_count = 0
        extrusion_count = 0
        retract_count_layer = 0
        z_hop_count_layer = 0

        layer_height = _value_or_default(heights, layer_index, heights[-1])
        if layer_height <= EPSILON:
            layer_height = 0.2
        z_value = _value_or_default(z_values, layer_index, current_z + (layer_height * 0.5))
        if z_value <= EPSILON:
            z_value = current_z + (layer_height * 0.5)
        current_z = z_value

        path_length = _value_or_default(path_lengths, layer_index, 0.0)
        filament_length = _value_or_default(filament_lengths, layer_index, 0.0)
        perimeter_filament_length = min(
            max(0.0, filament_length),
            _value_or_default(perimeter_filament_lengths, layer_index, 0.0),
        )
        travel_moves = _int_or_default(travel_move_counts, layer_index, 0)
        travel_length = _value_or_default(travel_lengths, layer_index, 0.0)
        retract_events = _int_or_default(retract_counts, layer_index, 0)
        z_hop_events = _int_or_default(z_hop_counts, layer_index, 0)
        perimeter_paths = perimeter_paths_by_layer[layer_index] if layer_index < len(perimeter_paths_by_layer) else []
        if layer_index < len(xy_targets):
            target = xy_targets[layer_index]
            travel_x = float(target[0])
            travel_y = float(target[1])
            extrude_x = float(target[2])
            extrude_y = float(target[3])
        else:
            travel_x = margin + ((float(layer_index) * 7.3) % span_x)
            travel_y = margin + ((float(layer_index) * 5.1) % span_y)
            extrude_x = margin + ((float(layer_index) * 9.7) % span_x)
            extrude_y = margin + ((float(layer_index) * 6.9) % span_y)

        if emit_layer_comments:
            lines.append(f";LAYER:{layer_index}")
            layer_commands.append(
                GCodeCommandPlan(
                    line_number=line_number,
                    command=lines[-1],
                    semantic_tag="layer_comment",
                    layer_index=layer_index,
                )
            )
            line_number += 1
            command_count += 1

        z_line = f"G0 Z{z_value:.3f} F{travel_feed:.0f}"
        lines.append(z_line)
        layer_commands.append(
            GCodeCommandPlan(
                line_number=line_number,
                command=z_line,
                semantic_tag="layer_z_move",
                layer_index=layer_index,
            )
        )
        line_number += 1
        command_count += 1
        travel_count += 1

        prepared_perimeter_paths: list[tuple[float, tuple[tuple[float, float], ...], list[float], float]] = []
        perimeter_weight_total = 0.0
        for planned_length, path_points in perimeter_paths:
            closed_points = _closed_loop_points(path_points)
            if len(closed_points) < 2:
                continue
            segment_lengths = _segment_lengths(closed_points)
            geometry_length = float(sum(segment_lengths))
            if geometry_length <= EPSILON:
                continue
            weight_length = float(planned_length) if planned_length > EPSILON else geometry_length
            prepared_perimeter_paths.append((weight_length, closed_points, segment_lengths, geometry_length))
            perimeter_weight_total += weight_length

        if prepared_perimeter_paths:
            start_x, start_y = prepared_perimeter_paths[0][1][0]
            virtual_x = start_x
            virtual_y = start_y
            travel_line = f"G0 X{virtual_x:.3f} Y{virtual_y:.3f} F{travel_feed:.0f}"
            lines.append(travel_line)
            layer_commands.append(
                GCodeCommandPlan(
                    line_number=line_number,
                    command=travel_line,
                    semantic_tag="travel_move",
                    layer_index=layer_index,
                )
            )
            line_number += 1
            command_count += 1
            travel_count += 1
        elif travel_moves > 0:
            if travel_length <= EPSILON:
                warnings.append(f"layer_{layer_index}:travel_moves_without_length")
            virtual_x = travel_x
            virtual_y = travel_y
            travel_line = f"G0 X{virtual_x:.3f} Y{virtual_y:.3f} F{travel_feed:.0f}"
            lines.append(travel_line)
            layer_commands.append(
                GCodeCommandPlan(
                    line_number=line_number,
                    command=travel_line,
                    semantic_tag="travel_move",
                    layer_index=layer_index,
                )
            )
            line_number += 1
            command_count += 1
            travel_count += 1

        if retract_events > 0 and retract_length > EPSILON:
            retract_value = -retract_length if not absolute_extrusion else (e_position - retract_length)
            if absolute_extrusion:
                e_position = retract_value
            retract_line = f"G1 E{retract_value:.5f} F{print_feed:.0f} ; retract"
            lines.append(retract_line)
            layer_commands.append(
                GCodeCommandPlan(
                    line_number=line_number,
                    command=retract_line,
                    semantic_tag="retract",
                    layer_index=layer_index,
                )
            )
            line_number += 1
            command_count += 1
            retract_count_layer += 1

        if z_hop_events > 0:
            hop_line = f"G0 Z{(z_value + 0.2):.3f} F{travel_feed:.0f} ; zhop"
            lines.append(hop_line)
            layer_commands.append(
                GCodeCommandPlan(
                    line_number=line_number,
                    command=hop_line,
                    semantic_tag="z_hop",
                    layer_index=layer_index,
                )
            )
            line_number += 1
            command_count += 1
            z_hop_count_layer += 1

        emitted_layer_filament = 0.0
        if prepared_perimeter_paths and perimeter_filament_length > EPSILON:
            if path_length <= EPSILON:
                warnings.append(f"layer_{layer_index}:filament_without_path_length")
            for path_index, (weight_length, closed_points, segment_lengths, geometry_length) in enumerate(
                prepared_perimeter_paths
            ):
                path_filament = perimeter_filament_length
                if perimeter_weight_total > EPSILON:
                    path_filament = perimeter_filament_length * (weight_length / perimeter_weight_total)
                if path_index > 0:
                    start_x, start_y = closed_points[0]
                    virtual_x = start_x
                    virtual_y = start_y
                    travel_line = f"G0 X{virtual_x:.3f} Y{virtual_y:.3f} F{travel_feed:.0f}"
                    lines.append(travel_line)
                    layer_commands.append(
                        GCodeCommandPlan(
                            line_number=line_number,
                            command=travel_line,
                            semantic_tag="travel_move",
                            layer_index=layer_index,
                        )
                    )
                    line_number += 1
                    command_count += 1
                    travel_count += 1
                for segment_index, segment_length in enumerate(segment_lengths):
                    if segment_length <= EPSILON:
                        continue
                    end_x, end_y = closed_points[segment_index + 1]
                    segment_filament = path_filament * (segment_length / geometry_length)
                    virtual_x = end_x
                    virtual_y = end_y
                    if absolute_extrusion:
                        e_position += segment_filament
                        e_value = e_position
                    else:
                        e_value = segment_filament
                    extrude_line = f"G1 X{virtual_x:.3f} Y{virtual_y:.3f} E{e_value:.5f} F{print_feed:.0f}"
                    lines.append(extrude_line)
                    layer_commands.append(
                        GCodeCommandPlan(
                            line_number=line_number,
                            command=extrude_line,
                            semantic_tag="extrusion_move",
                            layer_index=layer_index,
                        )
                    )
                    line_number += 1
                    command_count += 1
                    extrusion_count += 1
                    filament_length_total += segment_filament
                    emitted_layer_filament += segment_filament

        residual_filament = max(0.0, filament_length - emitted_layer_filament)
        if residual_filament > EPSILON:
            if path_length <= EPSILON:
                warnings.append(f"layer_{layer_index}:filament_without_path_length")
            if prepared_perimeter_paths:
                virtual_x = travel_x
                virtual_y = travel_y
                travel_line = f"G0 X{virtual_x:.3f} Y{virtual_y:.3f} F{travel_feed:.0f}"
                lines.append(travel_line)
                layer_commands.append(
                    GCodeCommandPlan(
                        line_number=line_number,
                        command=travel_line,
                        semantic_tag="travel_move",
                        layer_index=layer_index,
                    )
                )
                line_number += 1
                command_count += 1
                travel_count += 1
            virtual_x = extrude_x
            virtual_y = extrude_y
            if absolute_extrusion:
                e_position += residual_filament
                e_value = e_position
            else:
                e_value = residual_filament
            extrude_line = f"G1 X{virtual_x:.3f} Y{virtual_y:.3f} E{e_value:.5f} F{print_feed:.0f}"
            lines.append(extrude_line)
            layer_commands.append(
                GCodeCommandPlan(
                    line_number=line_number,
                    command=extrude_line,
                    semantic_tag="extrusion_move",
                    layer_index=layer_index,
                )
            )
            line_number += 1
            command_count += 1
            extrusion_count += 1
            filament_length_total += residual_filament
            emitted_layer_filament += residual_filament

        layer_plans.append(
            LayerGCodePlan(
                layer_index=layer_index,
                z_height_mm=float(z_value),
                command_count=command_count,
                travel_command_count=travel_count,
                extrusion_command_count=extrusion_count,
                retract_command_count=retract_count_layer,
                z_hop_command_count=z_hop_count_layer,
                filament_length_mm=float(emitted_layer_filament),
                commands=layer_commands,
            )
        )

        travel_command_count_total += travel_count
        extrusion_command_count_total += extrusion_count
        retract_command_count_total += retract_count_layer
        z_hop_command_count_total += z_hop_count_layer

    teardown_lines = build_teardown_lines(output_contract)
    lines.extend(teardown_lines)
    line_number += len(teardown_lines)

    report = GCodeEmissionReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        layer_count=layer_count,
        command_count_total=len(lines),
        setup_command_count=len(setup_lines),
        teardown_command_count=len(teardown_lines),
        travel_command_count_total=travel_command_count_total,
        extrusion_command_count_total=extrusion_command_count_total,
        retract_command_count_total=retract_command_count_total,
        z_hop_command_count_total=z_hop_command_count_total,
        filament_length_mm_total=float(filament_length_total),
        absolute_extrusion=bool(absolute_extrusion),
        firmware_flavor=firmware,
        startup_macro_line_count=len(output_contract.startup_macro_lines),
        end_macro_line_count=len(output_contract.end_macro_lines),
        warning_count=len(warnings),
        warnings=warnings,
    )
    return layer_plans, lines, report
