import math
from typing import Dict, Iterable

from .legacy_gcode_writer import SliceSettings
from .legacy_gcode_preview import _arc_center_from_radius, _arc_delta

def _format_duration(seconds: float) -> str:
    if seconds <= 0:
        return "0s"
    total = int(round(seconds))
    mins, secs = divmod(total, 60)
    hours, mins = divmod(mins, 60)
    if hours:
        return f"{hours}h{mins:02d}m"
    return f"{mins}m{secs:02d}s"

def estimate_gcode_stats(lines: Iterable[str], settings: SliceSettings) -> Dict[str, object]:
    position = [0.0, 0.0, 0.0]
    e_position = 0.0
    feed_rate = None
    absolute_mode = True
    extruder_absolute = True
    total_time = 0.0
    extrude_len = 0.0
    line_count = 0

    for raw in lines:
        if not raw:
            continue
        line = raw.split(";", 1)[0].strip()
        if not line:
            continue
        line_count += 1
        parts = line.split()
        if not parts:
            continue
        cmd = parts[0].upper()

        if cmd == "G90":
            absolute_mode = True
            continue
        if cmd == "G91":
            absolute_mode = False
            continue
        if cmd == "M82":
            extruder_absolute = True
            continue
        if cmd == "M83":
            extruder_absolute = False
            continue
        if cmd == "G28":
            axes = {part[0].upper() for part in parts[1:] if part}
            if not axes:
                position = [0.0, 0.0, 0.0]
            else:
                if "X" in axes:
                    position[0] = 0.0
                if "Y" in axes:
                    position[1] = 0.0
                if "Z" in axes:
                    position[2] = 0.0
            continue
        if cmd == "G92":
            for part in parts[1:]:
                if not part:
                    continue
                axis = part[0].upper()
                try:
                    value = float(part[1:])
                except ValueError:
                    continue
                if axis == "E":
                    e_position = value
                elif axis == "X":
                    position[0] = value
                elif axis == "Y":
                    position[1] = value
                elif axis == "Z":
                    position[2] = value
            continue
        if cmd not in ("G0", "G1", "G2", "G3"):
            continue

        x = y = z = None
        e_val = None
        i_val = j_val = r_val = None
        for part in parts[1:]:
            axis = part[0].upper()
            try:
                val = float(part[1:])
            except ValueError:
                continue
            if axis == "X":
                x = val
            elif axis == "Y":
                y = val
            elif axis == "Z":
                z = val
            elif axis == "E":
                e_val = val
            elif axis == "F":
                feed_rate = val
            elif axis == "I":
                i_val = val
            elif axis == "J":
                j_val = val
            elif axis == "R":
                r_val = val

        new_pos = position.copy()
        if x is not None:
            new_pos[0] = x + position[0] if not absolute_mode else x
        if y is not None:
            new_pos[1] = y + position[1] if not absolute_mode else y
        if z is not None:
            new_pos[2] = z + position[2] if not absolute_mode else z

        delta_e = 0.0
        if e_val is not None:
            if extruder_absolute:
                delta_e = e_val - e_position
                e_position = e_val
            else:
                delta_e = e_val
                e_position += e_val

        dist = math.dist(position, new_pos)
        if cmd in ("G2", "G3"):
            clockwise = cmd == "G2"
            start_xy = (position[0], position[1])
            end_xy = (new_pos[0], new_pos[1])
            center = None
            if i_val is not None or j_val is not None:
                center = (start_xy[0] + (i_val or 0.0), start_xy[1] + (j_val or 0.0))
            elif r_val is not None:
                center = _arc_center_from_radius(start_xy, end_xy, r_val, clockwise)
            if center is not None:
                radius = math.hypot(start_xy[0] - center[0], start_xy[1] - center[1])
                delta = _arc_delta(start_xy, end_xy, center, clockwise)
                dist = radius * delta

        if delta_e > 0.0:
            extrude_len += delta_e

        if dist > 0:
            if feed_rate is None:
                speed = settings.print_speed if delta_e > 0 else settings.travel_speed
                feed_rate = speed * 60.0
            if feed_rate:
                total_time += dist / (feed_rate / 60.0)

        position = new_pos

    filament_diameter = float(settings.filament_diameter or 1.75)
    area = math.pi * (filament_diameter / 2.0) ** 2
    volume_mm3 = area * extrude_len
    weight_g = (volume_mm3 / 1000.0) * float(settings.filament_density)
    length_m = extrude_len / 1000.0

    return {
        "time": _format_duration(total_time),
        "time_seconds": total_time,
        "weight": f"{weight_g:.2f} g",
        "length": f"{length_m:.2f} m",
        "length_mm": extrude_len,
        "cost": "n/a",
        "line_count": line_count,
    }

def estimate_gcode_file(path: str, settings: SliceSettings) -> Dict[str, object]:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as handle:
            return estimate_gcode_stats(handle, settings)
    except Exception:
        return {"time": "n/a", "weight": "n/a", "length": "n/a", "cost": "n/a", "line_count": 0}

