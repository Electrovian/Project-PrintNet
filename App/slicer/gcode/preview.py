from dataclasses import dataclass, field
import math
from typing import Dict, Iterable, List, Optional, Tuple

from .writer import SliceSettings

@dataclass
class PreviewSegment:
    start: Tuple[float, float, float]
    end: Tuple[float, float, float]
    speed: float
    extrusion: float
    flow: float
    width: float
    feature: str
    is_extrude: bool

@dataclass
class PreviewFeatureGroup:
    extrude: List[PreviewSegment] = field(default_factory=list)
    travel: List[PreviewSegment] = field(default_factory=list)

@dataclass
class PreviewLayer:
    z: float
    features: Dict[str, PreviewFeatureGroup] = field(default_factory=dict)
    segments: List[PreviewSegment] = field(default_factory=list)

@dataclass
class GCodePreview:
    layers: List[PreviewLayer]
    min_speed: float
    max_speed: float
    min_flow: float
    max_flow: float
    min_width: float
    max_width: float

def _arc_center_from_radius(start: Tuple[float, float],
                            end: Tuple[float, float],
                            radius: float,
                            clockwise: bool) -> Optional[Tuple[float, float]]:
    sx, sy = start
    ex, ey = end
    dx = ex - sx
    dy = ey - sy
    chord_len = math.hypot(dx, dy)
    if chord_len <= 1e-9:
        return None
    r = abs(radius)
    if r < chord_len / 2.0:
        return None
    mx = (sx + ex) / 2.0
    my = (sy + ey) / 2.0
    h = math.sqrt(max(r * r - (chord_len / 2.0) ** 2, 0.0))
    nx = -dy / chord_len
    ny = dx / chord_len
    if clockwise:
        cx = mx + nx * h
        cy = my + ny * h
    else:
        cx = mx - nx * h
        cy = my - ny * h
    return (cx, cy)

def _arc_delta(start: Tuple[float, float],
               end: Tuple[float, float],
               center: Tuple[float, float],
               clockwise: bool) -> float:
    sx, sy = start
    ex, ey = end
    cx, cy = center
    a0 = math.atan2(sy - cy, sx - cx)
    a1 = math.atan2(ey - cy, ex - cx)
    if clockwise:
        delta = a0 - a1
        if delta <= 0.0:
            delta += 2.0 * math.pi
    else:
        delta = a1 - a0
        if delta <= 0.0:
            delta += 2.0 * math.pi
    return delta

def _arc_points(start: Tuple[float, float],
                end: Tuple[float, float],
                center: Tuple[float, float],
                clockwise: bool,
                segments: int) -> List[Tuple[float, float]]:
    sx, sy = start
    cx, cy = center
    radius = math.hypot(sx - cx, sy - cy)
    if radius <= 0.0 or segments <= 1:
        return [start, end]
    delta = _arc_delta(start, end, center, clockwise)
    step = delta / segments
    direction = -1.0 if clockwise else 1.0
    a0 = math.atan2(sy - cy, sx - cx)
    points = []
    for i in range(segments + 1):
        angle = a0 + direction * step * i
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    points[-1] = end
    return points

def parse_gcode_preview(lines: Iterable[str],
                        settings: Optional[SliceSettings] = None) -> GCodePreview:
    position = [0.0, 0.0, 0.0]
    e_position = 0.0
    feed_rate = None
    absolute_mode = True
    extruder_absolute = True
    current_feature = "other"
    layers: List[PreviewLayer] = []
    current_layer: Optional[PreviewLayer] = None
    current_z = None
    min_speed = float("inf")
    max_speed = 0.0
    min_flow = float("inf")
    max_flow = 0.0
    min_width = float("inf")
    max_width = 0.0

    filament_area = None
    layer_height = None
    width_cap = None
    if settings is not None:
        try:
            filament_area = math.pi * (float(settings.filament_diameter) / 2.0) ** 2
        except (TypeError, ValueError):
            filament_area = None
        try:
            layer_height = max(0.0, float(settings.layer_height))
        except (TypeError, ValueError):
            layer_height = None
        try:
            base_width = max(0.0, float(settings.extrusion_width))
        except (TypeError, ValueError):
            base_width = 0.0
        width_cap = base_width * 5.0 if base_width > 0.0 else None

    def segment_width(dist: float, extrusion: float) -> float:
        if dist <= 1e-9 or extrusion <= 0.0:
            return 0.0
        if filament_area is None or layer_height is None:
            return 0.0
        if filament_area <= 0.0 or layer_height <= 0.0:
            return 0.0
        width = (extrusion * filament_area) / (dist * layer_height)
        if not math.isfinite(width) or width <= 0.0:
            return 0.0
        if width_cap is not None and width_cap > 0.0:
            width = min(width, width_cap)
        return width

    def ensure_layer(z_val: float) -> PreviewLayer:
        nonlocal current_layer, current_z
        if current_layer is None or current_z is None or abs(z_val - current_z) > 1e-6:
            current_layer = PreviewLayer(z=z_val)
            layers.append(current_layer)
            current_z = z_val
        return current_layer

    def add_segment(seg: PreviewSegment):
        nonlocal min_speed, max_speed, min_flow, max_flow, min_width, max_width
        layer = ensure_layer(seg.end[2])
        layer.segments.append(seg)
        group = layer.features.setdefault(seg.feature, PreviewFeatureGroup())
        if seg.is_extrude:
            group.extrude.append(seg)
        else:
            group.travel.append(seg)
        if seg.speed > 0:
            min_speed = min(min_speed, seg.speed)
            max_speed = max(max_speed, seg.speed)
        if seg.flow > 0:
            min_flow = min(min_flow, seg.flow)
            max_flow = max(max_flow, seg.flow)
        if seg.width > 0.0:
            min_width = min(min_width, seg.width)
            max_width = max(max_width, seg.width)

    def feature_from_comment(comment: str, current: str) -> str:
        if not comment:
            return current
        upper = comment.upper()
        token = None
        for key in ("TYPE:", "FEATURE:"):
            if key in upper:
                token = upper.split(key, 1)[1].strip().split()[0]
                break
        if not token:
            return current
        if "RETRACT" in token:
            return "retract"
        if "TRAVEL" in token:
            return "travel"
        if "WALL" in token or "PERIMETER" in token:
            if "OUTER" in token:
                return "outer_wall"
            if "INNER" in token:
                return "inner_wall"
            return "outer_wall"
        if "TOP" in token or "SKIN" in token:
            return "top_surface"
        if "BOTTOM" in token:
            return "bottom_surface"
        if "BRIDGE" in token:
            return "bridge"
        if "GAP" in token:
            return "gap_infill"
        if "THIN" in token:
            return "thin_wall"
        if "IRON" in token:
            return "ironing"
        if "SKIRT" in token:
            return "skirt"
        if "BRIM" in token:
            return "brim"
        if "RAFT" in token:
            return "raft"
        if "SUPPORT" in token:
            if "INTERFACE" in token:
                return "support_interface"
            return "support"
        if "SOLID" in token:
            return "solid_infill"
        if "INFILL" in token or "FILL" in token:
            return "sparse_infill"
        return "other"

    for raw in lines:
        if not raw:
            continue
        line = raw.strip()
        if not line:
            continue
        if ";" in line:
            code, comment = line.split(";", 1)
            current_feature = feature_from_comment(comment, current_feature)
        else:
            code = line
        code = code.strip()
        if not code:
            continue
        parts = code.split()
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

        speed = feed_rate / 60.0 if feed_rate is not None else 0.0
        is_extrude = delta_e > 0.0
        feature = current_feature if is_extrude else "travel"
        if delta_e < 0.0:
            feature = "retract"

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
                delta = _arc_delta(start_xy, end_xy, center, clockwise)
                segments = max(4, int(abs(delta) / (math.pi / 8.0)))
                points = _arc_points(start_xy, end_xy, center, clockwise, segments)
                per_seg_e = delta_e / max(1, len(points) - 1)
                for idx in range(len(points) - 1):
                    seg_start = points[idx]
                    seg_end = points[idx + 1]
                    dist = math.hypot(seg_end[0] - seg_start[0], seg_end[1] - seg_start[1])
                    flow = per_seg_e / dist if dist > 0 and delta_e > 0.0 else 0.0
                    width = segment_width(dist, per_seg_e)
                    segment = PreviewSegment(
                        start=(seg_start[0], seg_start[1], position[2]),
                        end=(seg_end[0], seg_end[1], new_pos[2]),
                        speed=speed,
                        extrusion=per_seg_e,
                        flow=flow,
                        width=width,
                        feature=feature,
                        is_extrude=is_extrude,
                    )
                    add_segment(segment)
                position = new_pos
                continue

        dist = math.dist(position, new_pos)
        if dist <= 0 and delta_e == 0.0:
            position = new_pos
            continue
        flow = delta_e / dist if dist > 0 and delta_e > 0.0 else 0.0
        width = segment_width(dist, delta_e)
        segment = PreviewSegment(
            start=(position[0], position[1], position[2]),
            end=(new_pos[0], new_pos[1], new_pos[2]),
            speed=speed,
            extrusion=delta_e,
            flow=flow,
            width=width,
            feature=feature,
            is_extrude=is_extrude,
        )
        add_segment(segment)
        position = new_pos

    if not layers:
        layers.append(PreviewLayer(z=0.0))
    min_speed = 0.0 if min_speed == float("inf") else min_speed
    min_flow = 0.0 if min_flow == float("inf") else min_flow
    min_width = 0.0 if min_width == float("inf") else min_width
    return GCodePreview(
        layers=layers,
        min_speed=min_speed,
        max_speed=max_speed,
        min_flow=min_flow,
        max_flow=max_flow,
        min_width=min_width,
        max_width=max_width,
    )

def parse_gcode_preview_file(path: str,
                             settings: Optional[SliceSettings] = None) -> GCodePreview:
    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        return parse_gcode_preview(handle, settings=settings)

def _format_duration(seconds: float) -> str:
    if seconds <= 0:
        return "0s"
    total = int(round(seconds))
    mins, secs = divmod(total, 60)
    hours, mins = divmod(mins, 60)
    if hours:
        return f"{hours}h{mins:02d}m"
    return f"{mins}m{secs:02d}s"

