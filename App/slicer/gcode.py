from dataclasses import dataclass, field
import math
from typing import Dict, Iterable, List, Optional, Tuple

@dataclass
class FirmwareProfile:
    name: str
    start_gcode: List[str]
    end_gcode: List[str]
    retract_style: str
    supports_arcs: bool

def _normalize_gcode_lines(value) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        lines = [line.rstrip() for line in value.splitlines()]
        return [line for line in lines if line.strip()]
    if isinstance(value, (list, tuple)):
        lines = []
        for item in value:
            if item is None:
                continue
            line = str(item).rstrip()
            if line.strip():
                lines.append(line)
        return lines
    return []

_FIRMWARE_PROFILES: Dict[str, FirmwareProfile] = {
    "marlin": FirmwareProfile(
        name="marlin",
        start_gcode=[],
        end_gcode=[],
        retract_style="explicit",
        supports_arcs=False,
    ),
    "klipper": FirmwareProfile(
        name="klipper",
        start_gcode=[],
        end_gcode=[],
        retract_style="explicit",
        supports_arcs=False,
    ),
}

def get_firmware_profile(name: str) -> FirmwareProfile:
    key = (name or "").strip().lower()
    return _FIRMWARE_PROFILES.get(key, _FIRMWARE_PROFILES["marlin"])

@dataclass
class SliceSettings:
    layer_height: float = 0.2
    min_layer_height: float = 0.1
    max_layer_height: float = 0.3
    firmware_flavor: str = "marlin"
    retract_style: Optional[str] = None
    supports_arcs: Optional[bool] = None
    start_gcode: Optional[List[str] | str] = None
    end_gcode: Optional[List[str] | str] = None
    filament_density: float = 1.24
    infill_percent: float = 15.0
    infill_density: Optional[float] = None
    infill_angle: float = 45.0
    infill_pattern: str = "rectilinear"
    print_speed: float = 60.0  # mm/s
    travel_speed: float = 150.0  # mm/s
    bridge_speed: float = 30.0
    nozzle_diameter: float = 0.4
    extrusion_width: float = 0.4
    bridge_extrusion_width: float = 0.5
    filament_diameter: float = 1.75
    extrusion_multiplier: float = 1.0
    perimeter_count: int = 1
    top_layers: int = 3
    bottom_layers: int = 3
    overhang_angle: float = 45.0
    support_z_gap: float = 0.2
    support_xy_gap: float = 0.3
    interface_layers: int = 2
    interface_density: float = 0.9
    support_spacing: float = 2.0
    support_style: str = "pillars"
    tree_branch_angle: float = 45.0
    tree_merge_distance: float = 2.0
    retract_distance: float = 1.0
    retract_speed: float = 25.0
    z_hop_height: float = 0.2
    ironing_speed: float = 20.0
    ironing_flow: float = 0.1
    ironing_enabled: bool = True
    adaptive_overhang_enabled: bool = False
    adaptive_overhang_threshold: float = 0.3
    adaptive_overhang_height: float = 0.1
    layer_height_ranges: Optional[List[Tuple[float, float, float]]] = None
    brim_width: float = 0.0
    skirt_loops: int = 0
    skirt_distance: float = 5.0
    raft_layers: int = 0
    raft_margin: float = 3.0
    hole_compensation_mm: float = 0.0

    def __post_init__(self):
        self.min_layer_height = max(0.01, float(self.min_layer_height))
        self.max_layer_height = max(self.min_layer_height, float(self.max_layer_height))
        self.layer_height = max(self.min_layer_height,
                                min(float(self.layer_height), self.max_layer_height))
        profile = get_firmware_profile(self.firmware_flavor)
        self.firmware_flavor = profile.name
        if self.retract_style is None:
            self.retract_style = profile.retract_style
        self.retract_style = str(self.retract_style).strip().lower() or "explicit"
        if self.retract_style not in ("explicit", "firmware"):
            self.retract_style = "explicit"
        if self.supports_arcs is None:
            self.supports_arcs = profile.supports_arcs
        self.supports_arcs = bool(self.supports_arcs)
        if self.start_gcode is None:
            self.start_gcode = list(profile.start_gcode)
        self.start_gcode = _normalize_gcode_lines(self.start_gcode)
        if self.end_gcode is None:
            self.end_gcode = list(profile.end_gcode)
        self.end_gcode = _normalize_gcode_lines(self.end_gcode)
        self.filament_density = max(0.1, float(self.filament_density))
        if self.infill_density is None:
            self.infill_density = self.infill_percent / 100.0
        self.infill_density = max(0.0, min(1.0, float(self.infill_density)))
        if self.bridge_extrusion_width <= 0.0:
            self.bridge_extrusion_width = self.extrusion_width
        self.perimeter_count = max(1, int(self.perimeter_count))
        self.top_layers = max(0, int(self.top_layers))
        self.bottom_layers = max(0, int(self.bottom_layers))
        self.interface_layers = max(0, int(self.interface_layers))
        self.interface_density = max(0.0, min(1.0, float(self.interface_density)))
        self.support_spacing = max(0.1, float(self.support_spacing))
        self.support_style = str(self.support_style).strip().lower() or "pillars"
        self.tree_branch_angle = max(0.0, min(85.0, float(self.tree_branch_angle)))
        self.tree_merge_distance = max(0.1, float(self.tree_merge_distance))
        self.retract_distance = max(0.0, float(self.retract_distance))
        self.retract_speed = max(1.0, float(self.retract_speed))
        self.z_hop_height = max(0.0, float(self.z_hop_height))
        self.ironing_speed = max(1.0, float(self.ironing_speed))
        self.ironing_flow = max(0.0, min(1.0, float(self.ironing_flow)))
        self.adaptive_overhang_enabled = bool(self.adaptive_overhang_enabled)
        self.adaptive_overhang_threshold = max(0.0,
                                               min(1.0, float(self.adaptive_overhang_threshold)))
        self.adaptive_overhang_height = max(self.min_layer_height,
                                            min(float(self.adaptive_overhang_height),
                                                self.max_layer_height))
        if self.layer_height_ranges is None:
            self.layer_height_ranges = []
        else:
            self.layer_height_ranges = list(self.layer_height_ranges)
        self.brim_width = max(0.0, float(self.brim_width))
        self.skirt_loops = max(0, int(self.skirt_loops))
        self.skirt_distance = max(0.0, float(self.skirt_distance))
        self.raft_layers = max(0, int(self.raft_layers))
        self.raft_margin = max(0.0, float(self.raft_margin))
        self.hole_compensation_mm = max(0.0, float(self.hole_compensation_mm))

@dataclass
class GCodeWriter:
    settings: SliceSettings
    lines: List[str] = field(default_factory=list)
    e_position: float = 0.0
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    is_retracted: bool = False
    has_extruded: bool = False

    def add(self, line: str):
        self.lines.append(line)

    def _emit_macro(self, lines: Iterable[str]):
        for line in lines:
            line = str(line).rstrip()
            if line:
                self.add(line)

    def write_header(self):
        self.add("; OpenSlicer demo G-code")
        self.add("G90 ; absolute positioning")
        self.add("M82 ; absolute extrusion")
        self.add("G28 ; home all axes")
        if self.settings.start_gcode:
            self._emit_macro(self.settings.start_gcode)
        self.add("")

    def write_footer(self):
        if self.settings.end_gcode:
            self._emit_macro(self.settings.end_gcode)
        self.add("M104 S0 ; hotend off")
        self.add("M140 S0 ; bed off")
        self.add("G28 X0 Y0 ; home XY")
        self.add("M84 ; disable motors")
        self.add("; End of OpenSlicer demo")

    def move_travel(self, x: float, y: float, z: float, f: float):
        distance = math.hypot(x - self.position[0], y - self.position[1])
        if distance > 0.0 and self.has_extruded:
            self.retract()
        self.add(f"G0 X{x:.3f} Y{y:.3f} Z{z:.3f} F{f * 60:.0f}")
        self.position = (x, y, z)

    def move_extrude(self, x: float, y: float, z: float, speed: float, extrusion: float):
        self.unretract()
        self.e_position += extrusion
        self.add(f"G1 X{x:.3f} Y{y:.3f} Z{z:.3f} E{self.e_position:.5f} F{speed * 60:.0f}")
        self.position = (x, y, z)
        if extrusion > 0.0:
            self.has_extruded = True

    def move_arc_extrude(self,
                         x: float,
                         y: float,
                         z: float,
                         speed: float,
                         extrusion: float,
                         center_xy: Tuple[float, float],
                         clockwise: bool):
        self.unretract()
        self.e_position += extrusion
        i = center_xy[0] - self.position[0]
        j = center_xy[1] - self.position[1]
        cmd = "G2" if clockwise else "G3"
        self.add(
            f"{cmd} X{x:.3f} Y{y:.3f} Z{z:.3f} I{i:.3f} J{j:.3f} "
            f"E{self.e_position:.5f} F{speed * 60:.0f}"
        )
        self.position = (x, y, z)
        if extrusion > 0.0:
            self.has_extruded = True

    def retract(self):
        if self.is_retracted or self.settings.retract_distance <= 0.0:
            return
        if self.settings.retract_style == "firmware":
            self.add("G10")
        else:
            self.e_position -= self.settings.retract_distance
            self.add(f"G1 E{self.e_position:.5f} F{self.settings.retract_speed * 60:.0f}")
        self.is_retracted = True

    def unretract(self):
        if not self.is_retracted or self.settings.retract_distance <= 0.0:
            return
        if self.settings.retract_style == "firmware":
            self.add("G11")
        else:
            self.e_position += self.settings.retract_distance
            self.add(f"G1 E{self.e_position:.5f} F{self.settings.retract_speed * 60:.0f}")
        self.is_retracted = False

    def extrusion_for_length(self,
                             length: float,
                             width: Optional[float] = None,
                             multiplier: Optional[float] = None) -> float:
        filament_area = math.pi * (self.settings.filament_diameter / 2.0) ** 2
        line_width = self.settings.extrusion_width if width is None else width
        flow = self.settings.extrusion_multiplier if multiplier is None else multiplier
        volume = length * self.settings.layer_height * line_width
        if filament_area <= 0.0:
            return 0.0
        return (volume / filament_area) * flow

    def perimeter_loop(self, points: Iterable[Tuple[float, float]], z: float, speed: float):
        pts = list(points)
        if not pts:
            return
        x0, y0 = pts[0]
        self.move_travel(x0, y0, z, self.settings.travel_speed)
        if self.settings.supports_arcs and len(pts) >= 5:
            try:
                from . import path_planner
            except Exception:
                path_planner = None
            if path_planner is not None:
                fit = path_planner.fit_arc(pts)
                if fit is not None and fit.is_full_circle:
                    cx, cy = fit.center
                    radius = fit.radius
                    if radius > 0.0:
                        start_angle = math.atan2(y0 - cy, x0 - cx)
                        direction = -1.0 if fit.clockwise else 1.0
                        mid_angle = start_angle + direction * math.pi
                        mid = (cx + radius * math.cos(mid_angle),
                               cy + radius * math.sin(mid_angle))
                        half_length = math.pi * radius
                        extrusion = self.extrusion_for_length(half_length)
                        self.move_arc_extrude(mid[0], mid[1], z, speed, extrusion,
                                              center_xy=(cx, cy),
                                              clockwise=fit.clockwise)
                        self.move_arc_extrude(x0, y0, z, speed, extrusion,
                                              center_xy=(cx, cy),
                                              clockwise=fit.clockwise)
                        return
        px, py = x0, y0
        for x, y in pts[1:]:
            length = math.hypot(x - px, y - py)
            extrusion = self.extrusion_for_length(length)
            self.move_extrude(x, y, z, speed, extrusion=extrusion)
            px, py = x, y

    def extrude_lines(self,
                      lines: Iterable[Tuple[Tuple[float, float], Tuple[float, float]]],
                      z: float,
                      speed: float,
                      width: Optional[float] = None,
                      multiplier: Optional[float] = None):
        for start, end in lines:
            self.move_travel(start[0], start[1], z, self.settings.travel_speed)
            length = math.hypot(end[0] - start[0], end[1] - start[1])
            extrusion = self.extrusion_for_length(length, width=width, multiplier=multiplier)
            self.move_extrude(end[0], end[1], z, speed, extrusion=extrusion)

    def get_gcode(self) -> str:
        return "\n".join(self.lines)

@dataclass
class PreviewSegment:
    start: Tuple[float, float, float]
    end: Tuple[float, float, float]
    speed: float
    extrusion: float
    flow: float
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
    ex, ey = end
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

def parse_gcode_preview(lines: Iterable[str]) -> GCodePreview:
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

    def ensure_layer(z_val: float) -> PreviewLayer:
        nonlocal current_layer, current_z
        if current_layer is None or current_z is None or abs(z_val - current_z) > 1e-6:
            current_layer = PreviewLayer(z=z_val)
            layers.append(current_layer)
            current_z = z_val
        return current_layer

    def add_segment(seg: PreviewSegment):
        nonlocal min_speed, max_speed, min_flow, max_flow
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
        if cmd == "G92":
            for part in parts[1:]:
                if part.startswith("E"):
                    try:
                        e_position = float(part[1:])
                    except ValueError:
                        pass
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
                radius = math.hypot(start_xy[0] - center[0], start_xy[1] - center[1])
                delta = _arc_delta(start_xy, end_xy, center, clockwise)
                segments = max(4, int(abs(delta) / (math.pi / 8.0)))
                points = _arc_points(start_xy, end_xy, center, clockwise, segments)
                per_seg_e = delta_e / max(1, len(points) - 1)
                for idx in range(len(points) - 1):
                    seg_start = points[idx]
                    seg_end = points[idx + 1]
                    dist = math.hypot(seg_end[0] - seg_start[0], seg_end[1] - seg_start[1])
                    flow = per_seg_e / dist if dist > 0 and delta_e > 0.0 else 0.0
                    segment = PreviewSegment(
                        start=(seg_start[0], seg_start[1], position[2]),
                        end=(seg_end[0], seg_end[1], new_pos[2]),
                        speed=speed,
                        extrusion=per_seg_e,
                        flow=flow,
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
        segment = PreviewSegment(
            start=(position[0], position[1], position[2]),
            end=(new_pos[0], new_pos[1], new_pos[2]),
            speed=speed,
            extrusion=delta_e,
            flow=flow,
            feature=feature,
            is_extrude=is_extrude,
        )
        add_segment(segment)
        position = new_pos

    if not layers:
        layers.append(PreviewLayer(z=0.0))
    min_speed = 0.0 if min_speed == float("inf") else min_speed
    min_flow = 0.0 if min_flow == float("inf") else min_flow
    return GCodePreview(
        layers=layers,
        min_speed=min_speed,
        max_speed=max_speed,
        min_flow=min_flow,
        max_flow=max_flow,
    )

def parse_gcode_preview_file(path: str) -> GCodePreview:
    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        return parse_gcode_preview(handle)

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
        if cmd == "G92":
            for part in parts[1:]:
                if part.startswith("E"):
                    try:
                        e_position = float(part[1:])
                    except ValueError:
                        pass
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

def _tower_square(size: float, center: Tuple[float, float] = (0.0, 0.0)) -> List[Tuple[float, float]]:
    half = size / 2.0
    cx, cy = center
    return [
        (cx - half, cy - half),
        (cx + half, cy - half),
        (cx + half, cy + half),
        (cx - half, cy + half),
        (cx - half, cy - half),
    ]

def generate_temperature_tower(settings: SliceSettings,
                               start_temp: float,
                               end_temp: float,
                               step: float,
                               block_height: float = 5.0,
                               tower_size: float = 20.0) -> str:
    writer = GCodeWriter(settings=settings)
    writer.write_header()
    writer.add("; Temperature tower")

    z = settings.layer_height
    square = _tower_square(tower_size)
    if step == 0:
        step = 1.0
    if (end_temp - start_temp) * step < 0:
        step = -step

    temp = start_temp
    while (temp <= end_temp and step > 0) or (temp >= end_temp and step < 0):
        writer.add(f"; TEMP: {temp:.0f}C")
        writer.add(f"M104 S{temp:.0f}")
        writer.add(f"M109 S{temp:.0f}")
        layers = max(1, int(round(block_height / settings.layer_height)))
        for _ in range(layers):
            writer.perimeter_loop(square, z=z, speed=settings.print_speed)
            z += settings.layer_height
        temp += step

    writer.write_footer()
    return writer.get_gcode()

def generate_retraction_tower(settings: SliceSettings,
                              start_distance: float,
                              end_distance: float,
                              step: float,
                              block_height: float = 5.0,
                              tower_size: float = 20.0) -> str:
    writer = GCodeWriter(settings=settings)
    writer.write_header()
    writer.add("; Retraction tower")

    z = settings.layer_height
    square = _tower_square(tower_size)
    if step == 0:
        step = 0.1
    if (end_distance - start_distance) * step < 0:
        step = -step

    distance = start_distance
    while (distance <= end_distance and step > 0) or (distance >= end_distance and step < 0):
        writer.add(f"; RETRACT_DISTANCE: {distance:.2f}mm")
        if settings.retract_style == "firmware":
            writer.add(f"M207 S{distance:.2f} F{settings.retract_speed * 60:.0f}")
        else:
            writer.settings.retract_distance = float(distance)
        layers = max(1, int(round(block_height / settings.layer_height)))
        for _ in range(layers):
            writer.perimeter_loop(square, z=z, speed=settings.print_speed)
            writer.retract()
            writer.move_travel(square[0][0], square[0][1], z, settings.travel_speed)
            writer.unretract()
            z += settings.layer_height
        distance += step

    writer.write_footer()
    return writer.get_gcode()

def generate_pressure_advance_pattern(settings: SliceSettings,
                                      start_value: float,
                                      end_value: float,
                                      step: float,
                                      line_length: float = 80.0,
                                      line_count: int = 5,
                                      spacing: float = 5.0) -> str:
    writer = GCodeWriter(settings=settings)
    writer.write_header()
    writer.add("; Pressure advance pattern")

    if step == 0:
        step = 0.02
    if (end_value - start_value) * step < 0:
        step = -step

    z = settings.layer_height
    y = 0.0
    value = start_value
    while (value <= end_value and step > 0) or (value >= end_value and step < 0):
        writer.add(f"; PRESSURE_ADVANCE: {value:.3f}")
        writer.add(f"SET_PRESSURE_ADVANCE ADVANCE={value:.3f}")
        start = (0.0, y)
        end = (line_length, y)
        for _ in range(max(1, int(line_count))):
            writer.move_travel(start[0], start[1], z, settings.travel_speed)
            length = math.hypot(end[0] - start[0], end[1] - start[1])
            extrusion = writer.extrusion_for_length(length)
            writer.move_extrude(end[0], end[1], z, settings.print_speed, extrusion)
            y += spacing
            start = (0.0, y)
            end = (line_length, y)
        y += spacing
        value += step

    writer.write_footer()
    return writer.get_gcode()
