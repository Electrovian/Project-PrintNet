from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Sequence

from .errors import SlicerV2GCodeValidationError


MOVEMENT_COMMANDS = {"G0", "G00", "G1", "G01"}
KNOWN_COMMANDS = {
    "G0",
    "G00",
    "G1",
    "G01",
    "G21",
    "G90",
    "G91",
    "G92",
    "M82",
    "M83",
    "M84",
    "M104",
    "M109",
    "M117",
    "M140",
    "M190",
    "M106",
    "M107",
    "M220",
    "M221",
}
MAX_VALIDATION_LINE_COUNT = 2_000_000
MAX_VALIDATION_LINE_LENGTH = 4096


@dataclass
class GCodeValidationIssue:
    severity: str
    code: str
    message: str
    line_number: int = 0
    command: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class GCodeValidationReport:
    validated_at_utc: str
    line_count: int
    strict_mode: bool
    error_count: int = 0
    warning_count: int = 0
    movement_command_count: int = 0
    extrusion_move_count: int = 0
    parse_error_count: int = 0
    bounds_violation_count: int = 0
    z_monotonicity_violation_count: int = 0
    extrusion_monotonicity_violation_count: int = 0
    unsupported_command_count: int = 0
    issues: list[GCodeValidationIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.error_count == 0

    def add_error(self, code: str, message: str, *, line_number: int = 0, command: str = "") -> None:
        self.error_count += 1
        self.issues.append(
            GCodeValidationIssue(
                severity="error",
                code=code,
                message=message,
                line_number=line_number,
                command=command,
            )
        )

    def add_warning(self, code: str, message: str, *, line_number: int = 0, command: str = "") -> None:
        self.warning_count += 1
        self.issues.append(
            GCodeValidationIssue(
                severity="warning",
                code=code,
                message=message,
                line_number=line_number,
                command=command,
            )
        )

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["ok"] = self.ok
        return payload


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _validate_positive_number(
    name: str,
    value: float,
    *,
    minimum: float,
    maximum: float,
) -> float:
    parsed = float(value)
    if parsed < minimum or parsed > maximum:
        raise SlicerV2GCodeValidationError(f"GCODE_VALIDATION_INVALID_PARAMETER:{name}:{value}")
    return parsed


def _validate_positive_int(
    name: str,
    value: int,
    *,
    minimum: int,
    maximum: int,
) -> int:
    parsed = int(value)
    if parsed < minimum or parsed > maximum:
        raise SlicerV2GCodeValidationError(f"GCODE_VALIDATION_INVALID_PARAMETER:{name}:{value}")
    return parsed


def _split_line(raw_line: object) -> tuple[str, str]:
    text = str(raw_line).strip()
    if not text:
        return "", ""
    parts = text.split(";", 1)
    code = parts[0].strip()
    if len(parts) == 1:
        return code, ""
    return code, parts[1].strip().lower()


def _parse_params(
    tokens: list[str],
    *,
    line_number: int,
    command: str,
    report: GCodeValidationReport,
) -> dict[str, float]:
    params: dict[str, float] = {}
    for token in tokens[1:]:
        value = str(token).strip()
        if not value:
            continue
        key = value[0].upper()
        if key not in {"X", "Y", "Z", "E", "F", "S"}:
            continue
        numeric = value[1:]
        if not numeric:
            report.parse_error_count += 1
            report.add_error(
                "GCODE_VALIDATION_NUMERIC_TOKEN_MISSING",
                f"Missing numeric token in line {line_number}: {value}",
                line_number=line_number,
                command=command,
            )
            continue
        try:
            params[key] = float(numeric)
        except (TypeError, ValueError):
            report.parse_error_count += 1
            report.add_error(
                "GCODE_VALIDATION_NUMERIC_TOKEN_INVALID",
                f"Invalid numeric token in line {line_number}: {value}",
                line_number=line_number,
                command=command,
            )
    return params


def _is_retract_marker(comment: str, e_value: float, previous_e: float) -> bool:
    _ = e_value
    _ = previous_e
    if "retract" in comment:
        return True
    return False


def _validate_bounds(
    *,
    x: float,
    y: float,
    z: float,
    bed_x_mm: float,
    bed_y_mm: float,
    bed_z_mm: float,
    allow_negative_xy: bool,
    tolerance_mm: float,
    line_number: int,
    report: GCodeValidationReport,
    command: str,
) -> None:
    if not allow_negative_xy:
        if x < -tolerance_mm:
            report.bounds_violation_count += 1
            report.add_error(
                "GCODE_VALIDATION_X_NEGATIVE",
                f"X below zero at line {line_number}: {x}",
                line_number=line_number,
                command=command,
            )
        if y < -tolerance_mm:
            report.bounds_violation_count += 1
            report.add_error(
                "GCODE_VALIDATION_Y_NEGATIVE",
                f"Y below zero at line {line_number}: {y}",
                line_number=line_number,
                command=command,
            )
    if x > bed_x_mm + tolerance_mm:
        report.bounds_violation_count += 1
        report.add_error(
            "GCODE_VALIDATION_X_BOUNDS_EXCEEDED",
            f"X exceeds bed bound at line {line_number}: {x}>{bed_x_mm}",
            line_number=line_number,
            command=command,
        )
    if y > bed_y_mm + tolerance_mm:
        report.bounds_violation_count += 1
        report.add_error(
            "GCODE_VALIDATION_Y_BOUNDS_EXCEEDED",
            f"Y exceeds bed bound at line {line_number}: {y}>{bed_y_mm}",
            line_number=line_number,
            command=command,
        )
    if z < -tolerance_mm:
        report.bounds_violation_count += 1
        report.add_error(
            "GCODE_VALIDATION_Z_NEGATIVE",
            f"Z below zero at line {line_number}: {z}",
            line_number=line_number,
            command=command,
        )
    if z > bed_z_mm + tolerance_mm:
        report.bounds_violation_count += 1
        report.add_error(
            "GCODE_VALIDATION_Z_BOUNDS_EXCEEDED",
            f"Z exceeds build height at line {line_number}: {z}>{bed_z_mm}",
            line_number=line_number,
            command=command,
        )


def validate_gcode_semantics(
    lines: Sequence[str],
    *,
    absolute_extrusion: bool = True,
    strict: bool = False,
    bed_x_mm: float = 220.0,
    bed_y_mm: float = 220.0,
    bed_z_mm: float = 250.0,
    require_monotonic_z: bool = True,
    require_monotonic_e: bool = True,
    allow_absolute_retract: bool = True,
    allow_negative_xy: bool = False,
    line_length_limit: int = 512,
    max_line_count: int = 250_000,
    tolerance_mm: float = 0.0001,
) -> GCodeValidationReport:
    if not isinstance(lines, Sequence):
        raise SlicerV2GCodeValidationError("GCODE_VALIDATION_LINES_NOT_SEQUENCE")

    bed_x = _validate_positive_number("bed_x_mm", bed_x_mm, minimum=1.0, maximum=10000.0)
    bed_y = _validate_positive_number("bed_y_mm", bed_y_mm, minimum=1.0, maximum=10000.0)
    bed_z = _validate_positive_number("bed_z_mm", bed_z_mm, minimum=1.0, maximum=10000.0)
    max_lines = _validate_positive_int("max_line_count", max_line_count, minimum=1, maximum=MAX_VALIDATION_LINE_COUNT)
    max_length = _validate_positive_int(
        "line_length_limit",
        line_length_limit,
        minimum=32,
        maximum=MAX_VALIDATION_LINE_LENGTH,
    )
    tolerance = _validate_positive_number("tolerance_mm", tolerance_mm, minimum=0.0, maximum=1.0)

    if len(lines) > max_lines:
        raise SlicerV2GCodeValidationError(f"GCODE_VALIDATION_LINE_COUNT_EXCEEDED:{len(lines)}>{max_lines}")

    report = GCodeValidationReport(
        validated_at_utc=_utc_now_iso(),
        line_count=len(lines),
        strict_mode=bool(strict),
    )

    xyz_absolute_mode = True
    extrusion_absolute_mode = bool(absolute_extrusion)
    current_x = 0.0
    current_y = 0.0
    current_z = 0.0
    current_e = 0.0
    last_z = 0.0
    last_e = 0.0

    for line_number, raw_line in enumerate(lines, start=1):
        text = str(raw_line).rstrip("\r\n")
        if len(text) > max_length:
            report.add_warning(
                "GCODE_VALIDATION_LINE_TOO_LONG",
                f"G-code line length exceeds limit at line {line_number}",
                line_number=line_number,
            )

        command_part, comment_part = _split_line(text)
        if not command_part:
            continue
        tokens = command_part.split()
        if not tokens:
            continue
        command = tokens[0].upper()

        if command in MOVEMENT_COMMANDS:
            report.movement_command_count += 1
            params = _parse_params(tokens, line_number=line_number, command=command, report=report)

            next_x = current_x
            next_y = current_y
            next_z = current_z
            next_e = current_e

            if "X" in params:
                next_x = params["X"] if xyz_absolute_mode else current_x + params["X"]
            if "Y" in params:
                next_y = params["Y"] if xyz_absolute_mode else current_y + params["Y"]
            if "Z" in params:
                next_z = params["Z"] if xyz_absolute_mode else current_z + params["Z"]

            _validate_bounds(
                x=next_x,
                y=next_y,
                z=next_z,
                bed_x_mm=bed_x,
                bed_y_mm=bed_y,
                bed_z_mm=bed_z,
                allow_negative_xy=allow_negative_xy,
                tolerance_mm=tolerance,
                line_number=line_number,
                report=report,
                command=command,
            )

            if require_monotonic_z and "Z" in params and next_z + tolerance < last_z:
                report.z_monotonicity_violation_count += 1
                report.add_error(
                    "GCODE_VALIDATION_Z_NON_MONOTONIC",
                    f"Z decreased at line {line_number}: {next_z} < {last_z}",
                    line_number=line_number,
                    command=command,
                )
            if "Z" in params:
                last_z = next_z if next_z > last_z else last_z

            if "E" in params:
                report.extrusion_move_count += 1
                if extrusion_absolute_mode:
                    next_e = params["E"]
                    if require_monotonic_e and next_e + tolerance < last_e:
                        if allow_absolute_retract and _is_retract_marker(comment_part, next_e, last_e):
                            report.add_warning(
                                "GCODE_VALIDATION_ABSOLUTE_RETRACT_ALLOWED",
                                f"Absolute extrusion decreased in retract context at line {line_number}",
                                line_number=line_number,
                                command=command,
                            )
                        else:
                            report.extrusion_monotonicity_violation_count += 1
                            report.add_error(
                                "GCODE_VALIDATION_E_NON_MONOTONIC",
                                f"Extrusion E decreased at line {line_number}: {next_e} < {last_e}",
                                line_number=line_number,
                                command=command,
                            )
                    last_e = next_e
                else:
                    next_e = current_e + params["E"]
                    if require_monotonic_e and params["E"] < -tolerance and "retract" not in comment_part:
                        report.add_warning(
                            "GCODE_VALIDATION_RELATIVE_NEGATIVE_E",
                            f"Relative extrusion move has negative E without retract marker at line {line_number}",
                            line_number=line_number,
                            command=command,
                        )
                    last_e = next_e

            current_x = next_x
            current_y = next_y
            current_z = next_z
            current_e = next_e
            continue

        if command == "G90":
            xyz_absolute_mode = True
            continue
        if command == "G91":
            xyz_absolute_mode = False
            continue
        if command == "M82":
            extrusion_absolute_mode = True
            continue
        if command == "M83":
            extrusion_absolute_mode = False
            continue
        if command == "G92":
            params = _parse_params(tokens, line_number=line_number, command=command, report=report)
            if "X" in params:
                current_x = params["X"]
            if "Y" in params:
                current_y = params["Y"]
            if "Z" in params:
                current_z = params["Z"]
                last_z = current_z if current_z > last_z else last_z
            if "E" in params:
                current_e = params["E"]
                last_e = current_e
            continue

        if command.startswith("T"):
            continue
        if command in KNOWN_COMMANDS:
            continue
        if command.startswith("G") or command.startswith("M"):
            report.unsupported_command_count += 1
            report.add_warning(
                "GCODE_VALIDATION_UNSUPPORTED_COMMAND",
                f"Unsupported G-code command in validator profile: {command}",
                line_number=line_number,
                command=command,
            )
            continue

        report.parse_error_count += 1
        report.add_error(
            "GCODE_VALIDATION_UNKNOWN_COMMAND",
            f"Unknown command token at line {line_number}: {command}",
            line_number=line_number,
            command=command,
        )

    if strict and not report.ok:
        raise SlicerV2GCodeValidationError(f"GCODE_VALIDATION_FAILED:{report.error_count}")

    return report
