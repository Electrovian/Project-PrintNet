from __future__ import annotations

import math
import random
import re
from dataclasses import dataclass

from .errors import SlicerV2InfillPatternError


_JOINT_SIGNS = "/NnZz$LlUuQq~^|#"
_META_PATTERN = re.compile(r"[+\-%*@'\"$LlUuQq~^|#NnZz]")


@dataclass(frozen=True)
class _RotationToken:
    raw: str
    angle_deg: float
    absolute: bool
    joint: str
    negative: bool
    count_value: float | None
    count_unit: str
    repeat_count: int
    once: bool


def _normalize_angle(angle_deg: float) -> float:
    value = float(angle_deg)
    while value < 0.0:
        value += 360.0
    while value >= 360.0:
        value -= 360.0
    return value


def _split_tokens(template_string: str) -> list[str]:
    tokens = [token.strip() for token in re.split(r"[\s,]+", template_string.strip()) if token.strip()]
    return tokens


def _contains_meta(template_string: str) -> bool:
    return bool(_META_PATTERN.search(template_string))


def _parse_simple_angles(template_string: str) -> list[float]:
    values: list[float] = []
    for token in _split_tokens(template_string):
        try:
            values.append(float(token))
        except (TypeError, ValueError) as exc:
            raise SlicerV2InfillPatternError(f"INFILL_ROTATION_TEMPLATE_INVALID_TOKEN:{token}") from exc
    return values


def _parse_repeat(text: str) -> int:
    if not text:
        return 1
    assert text[0] == "*"
    suffix = text[1:].strip()
    if not suffix:
        # Bare '*' is treated as an explicit no-op marker.
        return 0
    try:
        value = int(float(suffix))
    except (TypeError, ValueError) as exc:
        raise SlicerV2InfillPatternError(f"INFILL_ROTATION_TEMPLATE_INVALID_REPEAT:{text}") from exc
    return max(0, value)


def _parse_count(count_text: str) -> float | None:
    text = count_text.strip()
    if not text:
        return None
    try:
        return abs(float(text))
    except (TypeError, ValueError) as exc:
        raise SlicerV2InfillPatternError(f"INFILL_ROTATION_TEMPLATE_INVALID_COUNT:{count_text}") from exc


def _parse_rotation_token(token_text: str) -> _RotationToken:
    text = token_text.strip()
    if not text:
        raise SlicerV2InfillPatternError("INFILL_ROTATION_TEMPLATE_EMPTY_TOKEN")

    once = text.endswith("!")
    if once:
        text = text[:-1].strip()

    repeat_raw = ""
    repeat_idx = text.find("*")
    if repeat_idx >= 0:
        repeat_raw = text[repeat_idx:]
        text = text[:repeat_idx].strip()
    repeat_count = _parse_repeat(repeat_raw)

    match = re.match(r"^([+\-]?)(\d+(?:\.\d+)?)(%?)", text)
    if match is None:
        raise SlicerV2InfillPatternError(f"INFILL_ROTATION_TEMPLATE_INVALID_TOKEN:{token_text}")

    sign = match.group(1)
    angle_str = match.group(2)
    angle_percent = match.group(3) == "%"
    try:
        angle_deg = float(angle_str)
    except (TypeError, ValueError) as exc:
        raise SlicerV2InfillPatternError(f"INFILL_ROTATION_TEMPLATE_INVALID_ANGLE:{token_text}") from exc
    if angle_percent:
        angle_deg *= 3.6
    if sign == "-":
        angle_deg *= -1.0

    absolute = sign == ""
    suffix = text[match.end() :].strip()
    joint = ""
    if suffix and suffix[0] in _JOINT_SIGNS:
        joint = suffix[0]
        suffix = suffix[1:].strip()

    negative = False
    if suffix.startswith("-"):
        negative = True
        suffix = suffix[1:].strip()

    unit = ""
    count_text = suffix
    for candidate in ("mm", "cm", "m", "'", "\"", "B", "T", "#", "%"):
        if suffix.endswith(candidate):
            unit = candidate
            count_text = suffix[: -len(candidate)].strip()
            break

    count_value = _parse_count(count_text)
    return _RotationToken(
        raw=token_text,
        angle_deg=float(angle_deg),
        absolute=absolute,
        joint=joint,
        negative=negative,
        count_value=count_value,
        count_unit=unit,
        repeat_count=repeat_count,
        once=once,
    )


def _resolve_count_layers(
    token: _RotationToken,
    *,
    layer_count: int,
    layer_height_mm: float,
    bottom_shell_layers: int,
    top_shell_layers: int,
) -> int:
    unit = token.count_unit
    value = token.count_value if token.count_value is not None else 1.0

    if unit == "B":
        return max(1, int(bottom_shell_layers))
    if unit == "T":
        return max(1, int(top_shell_layers))
    if unit == "%":
        return max(1, int(round((value / 100.0) * max(1, layer_count))))
    if unit == "#":
        return max(1, int(round(value)))

    mm_value = None
    if unit == "mm":
        mm_value = value
    elif unit == "cm":
        mm_value = value * 10.0
    elif unit == "m":
        mm_value = value * 1000.0
    elif unit == "\"":
        mm_value = value * 25.4
    elif unit == "'":
        mm_value = value * 25.4 * 12.0

    if mm_value is not None:
        lh = max(0.01, float(layer_height_mm))
        return max(1, int(round(mm_value / lh)))

    return max(1, int(round(value)))


def _shape_progress(joint: str, progress: float, negative: bool, rng: random.Random) -> float:
    p = max(0.0, min(1.0, float(progress)))
    if negative:
        p = 1.0 - p

    if joint in ("", "/"):
        return p
    if joint == "N":
        return p - math.sin(p * math.pi * 2.0) / (math.pi * 2.0)
    if joint == "n":
        return p - math.sin(p * math.pi * 2.0) / (math.pi * 4.0)
    if joint == "Z":
        return p + math.sin(p * math.pi * 2.0) / (math.pi * 2.0)
    if joint == "z":
        return p + math.sin(p * math.pi * 2.0) / (math.pi * 4.0)
    if joint == "$":
        return math.asin(max(-1.0, min(1.0, p * 2.0 - 1.0))) / math.pi + 0.5
    if joint == "L":
        return math.sin(p * math.pi / 2.0)
    if joint == "l":
        return 1.0 - math.cos(p * math.pi / 2.0)
    if joint == "U":
        return 1.0 - (1.0 - p) ** 2
    if joint == "u":
        return (1.0 - p) ** 2
    if joint == "Q":
        return 1.0 - (1.0 - p) ** 3
    if joint == "q":
        return (1.0 - p) ** 3
    if joint == "~":
        return rng.random()
    if joint == "^":
        return max(0.0, min(1.0, p + rng.random() - 0.5))
    if joint == "|":
        return 0.5
    if joint == "#":
        return 0.0 if negative else 1.0
    return p


def calculate_infill_rotation_angles(
    *,
    layer_count: int,
    fixed_infill_angle_deg: float,
    template_string: str,
    layer_height_mm: float,
    bottom_shell_layers: int = 0,
    top_shell_layers: int = 0,
    seed: int = 0,
) -> list[float]:
    if layer_count <= 0:
        return []

    template = str(template_string or "").strip()
    if not template:
        return [_normalize_angle(float(fixed_infill_angle_deg)) for _ in range(layer_count)]

    if not _contains_meta(template):
        values = _parse_simple_angles(template)
        if not values:
            return [_normalize_angle(float(fixed_infill_angle_deg)) for _ in range(layer_count)]
        return [_normalize_angle(values[index % len(values)]) for index in range(layer_count)]

    tokens_raw = _split_tokens(template)
    if not tokens_raw:
        return [_normalize_angle(float(fixed_infill_angle_deg)) for _ in range(layer_count)]
    tokens = [_parse_rotation_token(token) for token in tokens_raw]
    stopped = [False] * len(tokens)
    rng = random.Random(int(seed))

    result: list[float] = []
    current_angle = float(fixed_infill_angle_deg)
    token_index = 0
    guard = max(64, layer_count * 16)

    while len(result) < layer_count and guard > 0:
        guard -= 1
        token = tokens[token_index]
        if stopped[token_index]:
            token_index = (token_index + 1) % len(tokens)
            if all(stopped):
                break
            continue

        if token.repeat_count <= 0:
            token_index = (token_index + 1) % len(tokens)
            continue

        count_layers = _resolve_count_layers(
            token,
            layer_count=layer_count,
            layer_height_mm=layer_height_mm,
            bottom_shell_layers=bottom_shell_layers,
            top_shell_layers=top_shell_layers,
        )

        start_angle = float(token.angle_deg) if token.absolute else current_angle
        if token.absolute:
            delta = 0.0
        elif token.joint:
            delta = float(token.angle_deg)
        else:
            delta = float(token.angle_deg) * float(count_layers)

        for _repeat in range(token.repeat_count):
            for step in range(count_layers):
                if len(result) >= layer_count:
                    break
                progress = 1.0 if count_layers <= 1 else float(step) / float(count_layers - 1)
                shaped = _shape_progress(token.joint, progress, token.negative, rng)
                angle = start_angle + (delta * shaped)
                result.append(_normalize_angle(angle))

            if len(result) >= layer_count:
                break
            if count_layers > 0:
                current_angle = start_angle + delta
                start_angle = current_angle

        if token.once:
            stopped[token_index] = True
        token_index = (token_index + 1) % len(tokens)

    if not result:
        return [_normalize_angle(float(fixed_infill_angle_deg)) for _ in range(layer_count)]
    while len(result) < layer_count:
        result.append(result[-1])
    return result[:layer_count]


def calculate_infill_rotation_angle(
    *,
    layer_index: int,
    layer_count: int,
    fixed_infill_angle_deg: float,
    template_string: str,
    layer_height_mm: float,
    bottom_shell_layers: int = 0,
    top_shell_layers: int = 0,
    seed: int = 0,
) -> float:
    if layer_index < 0:
        raise SlicerV2InfillPatternError("INFILL_ROTATION_LAYER_INDEX_NEGATIVE")
    angles = calculate_infill_rotation_angles(
        layer_count=max(layer_count, layer_index + 1),
        fixed_infill_angle_deg=fixed_infill_angle_deg,
        template_string=template_string,
        layer_height_mm=layer_height_mm,
        bottom_shell_layers=bottom_shell_layers,
        top_shell_layers=top_shell_layers,
        seed=seed,
    )
    return float(angles[layer_index])
