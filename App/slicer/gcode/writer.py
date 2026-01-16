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
    first_layer_height: float = 0.2
    min_layer_height: float = 0.1
    max_layer_height: float = 0.3
    seam_position: str = "aligned"
    staggered_inner_seams: bool = False
    seam_gap: float = 0.0
    scarf_joint_seam: str = "none"
    wipe_use_base_speed: bool = True
    wipe_speed_percent: float = 80.0
    wipe_on_loops: bool = False
    wipe_before_external_loop: bool = False
    precise_wall: bool = False
    slice_gap_closing_radius: float = 0.0
    resolution: float = 0.0
    arc_fitting: bool = False
    xy_hole_compensation: float = 0.0
    xy_contour_compensation: float = 0.0
    elephant_foot_compensation: float = 0.0
    elephant_foot_compensation_layers: int = 0
    convert_holes_to_polyholes: bool = False
    precise_z_height: bool = False
    only_one_wall_top: bool = False
    only_one_wall_first_layer: bool = False
    firmware_flavor: str = "marlin"
    retract_style: Optional[str] = None
    supports_arcs: Optional[bool] = None
    start_gcode: Optional[List[str] | str] = None
    end_gcode: Optional[List[str] | str] = None
    filament_name: str = "Hyper PLA"
    filament_color: str = "#42d94a"
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
    first_layer_line_width: float = 0.0
    outer_wall_line_width: float = 0.0
    inner_wall_line_width: float = 0.0
    top_surface_line_width: float = 0.0
    sparse_infill_line_width: float = 0.0
    internal_solid_infill_line_width: float = 0.0
    support_line_width: float = 0.0
    bridge_extrusion_width: float = 0.5
    bridge_flow_ratio: float = 0.9
    internal_bridge_flow_ratio: float = 1.0
    bridge_density: float = 100.0
    thick_bridges: bool = False
    thick_internal_bridges: bool = True
    bridge_filter_mode: str = "disabled"
    bridge_counterbore_holes: str = "none"
    filament_diameter: float = 1.75
    extrusion_multiplier: float = 1.0
    perimeter_count: int = 1
    top_layers: int = 3
    bottom_layers: int = 3
    wall_generator: str = "classic"
    wall_transition_angle: float = 10.0
    wall_transition_filter_margin: float = 25.0
    wall_transition_length: float = 100.0
    wall_distribution_count: int = 1
    first_layer_min_wall_width: float = 85.0
    min_wall_width: float = 85.0
    min_feature_size: float = 25.0
    min_wall_length: float = 0.5
    wall_printing_order: str = "inner_outer"
    print_infill_first: bool = False
    wall_loop_direction: str = "auto"
    top_surface_flow_ratio: float = 1.0
    bottom_surface_flow_ratio: float = 1.0
    one_wall_threshold: float = 0.0
    avoid_crossing_walls: bool = False
    small_area_flow_compensation: bool = False
    smooth_wall_speed_z: bool = False
    support_enabled: bool = False
    support_type: str = "normal"
    overhang_angle: float = 45.0
    support_build_plate_only: bool = False
    support_z_gap: float = 0.2
    support_xy_gap: float = 0.3
    interface_layers: int = 2
    interface_density: float = 0.9
    support_spacing: float = 2.0
    support_style: str = "pillars"
    support_filament_base: str = "default"
    support_filament_interface: str = "default"
    tree_branch_angle: float = 45.0
    tree_merge_distance: float = 2.0
    retract_distance: float = 1.0
    retract_speed: float = 25.0
    z_hop_height: float = 0.2
    ironing_type: str = "no_ironing"
    ironing_speed: float = 20.0
    ironing_flow: float = 0.1
    ironing_enabled: bool = True
    adaptive_overhang_enabled: bool = False
    adaptive_overhang_threshold: float = 0.3
    adaptive_overhang_height: float = 0.1
    detect_overhang_walls: bool = True
    make_overhangs_printable: bool = False
    extra_perimeters_on_overhangs: bool = False
    reverse_overhang_on_odd: bool = False
    overhang_optimization: bool = False
    layer_height_ranges: Optional[List[Tuple[float, float, float]]] = None
    brim_width: float = 0.0
    brim_type: str = "auto"
    skirt_loops: int = 0
    skirt_height: int = 1
    skirt_distance: float = 5.0
    print_sequence: str = "by_layer"
    spiral_vase: bool = False
    ignore_inner_color: bool = False
    timelapse_mode: str = "traditional"
    fuzzy_skin: str = "none"
    prime_tower_enabled: bool = False
    prime_tower_width: float = 35.0
    prime_tower_square: bool = True
    prime_tower_volume: float = 45.0
    flush_into_infill: bool = False
    flush_into_support: bool = False
    raft_layers: int = 0
    raft_margin: float = 3.0
    hole_compensation_mm: float = 0.0

    def __post_init__(self):
        self.min_layer_height = max(0.01, float(self.min_layer_height))
        self.max_layer_height = max(self.min_layer_height, float(self.max_layer_height))
        self.layer_height = max(self.min_layer_height,
                                min(float(self.layer_height), self.max_layer_height))
        self.first_layer_height = max(self.min_layer_height,
                                      min(float(self.first_layer_height), self.max_layer_height))
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

        def _width_or_default(value: float, fallback: float) -> float:
            fallback_value = float(fallback)
            try:
                numeric = float(value)
            except (TypeError, ValueError):
                return fallback_value
            return fallback_value if numeric <= 0.0 else numeric

        self.seam_position = str(self.seam_position).strip().lower() or "aligned"
        self.staggered_inner_seams = bool(self.staggered_inner_seams)
        self.seam_gap = max(0.0, min(100.0, float(self.seam_gap)))
        self.scarf_joint_seam = str(self.scarf_joint_seam).strip().lower() or "none"
        if self.scarf_joint_seam not in ("none", "contour", "contour_hole"):
            self.scarf_joint_seam = "none"
        self.wipe_use_base_speed = bool(self.wipe_use_base_speed)
        self.wipe_speed_percent = max(0.0, min(200.0, float(self.wipe_speed_percent)))
        self.wipe_on_loops = bool(self.wipe_on_loops)
        self.wipe_before_external_loop = bool(self.wipe_before_external_loop)
        self.precise_wall = bool(self.precise_wall)
        self.slice_gap_closing_radius = max(0.0, float(self.slice_gap_closing_radius))
        self.resolution = max(0.0, float(self.resolution))
        self.arc_fitting = bool(self.arc_fitting)
        self.xy_hole_compensation = float(self.xy_hole_compensation)
        self.xy_contour_compensation = float(self.xy_contour_compensation)
        self.elephant_foot_compensation = max(0.0, float(self.elephant_foot_compensation))
        self.elephant_foot_compensation_layers = max(0, int(self.elephant_foot_compensation_layers))
        self.convert_holes_to_polyholes = bool(self.convert_holes_to_polyholes)
        self.precise_z_height = bool(self.precise_z_height)
        self.only_one_wall_top = bool(self.only_one_wall_top)
        self.only_one_wall_first_layer = bool(self.only_one_wall_first_layer)
        self.filament_name = str(self.filament_name or "").strip() or "Hyper PLA"
        self.filament_color = str(self.filament_color or "").strip() or "#42d94a"
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
        self.extrusion_width = max(0.01, float(self.extrusion_width))
        self.first_layer_line_width = _width_or_default(self.first_layer_line_width,
                                                        self.extrusion_width)
        self.outer_wall_line_width = _width_or_default(self.outer_wall_line_width,
                                                       self.extrusion_width)
        self.inner_wall_line_width = _width_or_default(self.inner_wall_line_width,
                                                       self.extrusion_width)
        self.top_surface_line_width = _width_or_default(self.top_surface_line_width,
                                                        self.extrusion_width)
        self.sparse_infill_line_width = _width_or_default(self.sparse_infill_line_width,
                                                          self.extrusion_width)
        self.internal_solid_infill_line_width = _width_or_default(
            self.internal_solid_infill_line_width,
            self.extrusion_width,
        )
        self.support_line_width = _width_or_default(self.support_line_width,
                                                    self.extrusion_width)
        self.bridge_extrusion_width = _width_or_default(self.bridge_extrusion_width,
                                                        self.extrusion_width)
        self.bridge_flow_ratio = max(0.0, float(self.bridge_flow_ratio))
        self.internal_bridge_flow_ratio = max(0.0, float(self.internal_bridge_flow_ratio))
        self.bridge_density = max(0.0, min(100.0, float(self.bridge_density)))
        self.thick_bridges = bool(self.thick_bridges)
        self.thick_internal_bridges = bool(self.thick_internal_bridges)
        self.bridge_filter_mode = str(self.bridge_filter_mode).strip().lower() or "disabled"
        if self.bridge_filter_mode not in ("disabled", "limited", "none"):
            self.bridge_filter_mode = "disabled"
        self.bridge_counterbore_holes = str(self.bridge_counterbore_holes).strip().lower() or "none"
        if self.bridge_counterbore_holes not in ("none", "partial", "sacrificial"):
            self.bridge_counterbore_holes = "none"
        self.perimeter_count = max(1, int(self.perimeter_count))
        self.top_layers = max(0, int(self.top_layers))
        self.bottom_layers = max(0, int(self.bottom_layers))
        self.wall_generator = str(self.wall_generator).strip().lower() or "classic"
        if self.wall_generator not in ("classic", "arachne"):
            self.wall_generator = "classic"
        self.wall_transition_angle = max(0.0, min(90.0, float(self.wall_transition_angle)))
        self.wall_transition_filter_margin = max(0.0, min(200.0,
                                                          float(self.wall_transition_filter_margin)))
        self.wall_transition_length = max(0.0, min(500.0, float(self.wall_transition_length)))
        self.wall_distribution_count = max(1, int(self.wall_distribution_count))
        self.first_layer_min_wall_width = max(1.0, min(400.0, float(self.first_layer_min_wall_width)))
        self.min_wall_width = max(1.0, min(400.0, float(self.min_wall_width)))
        self.min_feature_size = max(1.0, min(400.0, float(self.min_feature_size)))
        self.min_wall_length = max(0.0, float(self.min_wall_length))
        self.wall_printing_order = str(self.wall_printing_order).strip().lower() or "inner_outer"
        if self.wall_printing_order not in ("inner_outer", "outer_inner", "inner_outer_inner",
                                            "adaptive_outer_inner"):
            self.wall_printing_order = "inner_outer"
        self.print_infill_first = bool(self.print_infill_first)
        self.wall_loop_direction = str(self.wall_loop_direction).strip().lower() or "auto"
        if self.wall_loop_direction not in ("auto", "clockwise", "counter_clockwise"):
            self.wall_loop_direction = "auto"
        self.top_surface_flow_ratio = max(0.0, min(2.0, float(self.top_surface_flow_ratio)))
        self.bottom_surface_flow_ratio = max(0.0, min(2.0, float(self.bottom_surface_flow_ratio)))
        self.one_wall_threshold = max(0.0, float(self.one_wall_threshold))
        self.avoid_crossing_walls = bool(self.avoid_crossing_walls)
        self.small_area_flow_compensation = bool(self.small_area_flow_compensation)
        self.smooth_wall_speed_z = bool(self.smooth_wall_speed_z)
        self.support_enabled = bool(self.support_enabled)
        self.support_type = str(self.support_type).strip().lower() or "normal"
        self.support_build_plate_only = bool(self.support_build_plate_only)
        self.interface_layers = max(0, int(self.interface_layers))
        self.interface_density = max(0.0, min(1.0, float(self.interface_density)))
        self.support_spacing = max(0.1, float(self.support_spacing))
        self.support_style = str(self.support_style).strip().lower() or "pillars"
        self.support_filament_base = str(self.support_filament_base).strip().lower() or "default"
        self.support_filament_interface = str(self.support_filament_interface).strip().lower() or "default"
        self.tree_branch_angle = max(0.0, min(85.0, float(self.tree_branch_angle)))
        self.tree_merge_distance = max(0.1, float(self.tree_merge_distance))
        self.retract_distance = max(0.0, float(self.retract_distance))
        self.retract_speed = max(1.0, float(self.retract_speed))
        ironing_flag = bool(self.ironing_enabled)
        self.ironing_type = str(self.ironing_type).strip().lower() or "no_ironing"
        if self.ironing_type not in ("no_ironing", "all_top_surfaces",
                                      "topmost_surface_only", "all_solid_layers"):
            self.ironing_type = "no_ironing"
        if ironing_flag and self.ironing_type == "no_ironing":
            self.ironing_type = "all_top_surfaces"
        self.ironing_enabled = self.ironing_type != "no_ironing"
        self.brim_type = str(self.brim_type).strip().lower() or "auto"
        self.skirt_height = max(0, int(self.skirt_height))
        self.print_sequence = str(self.print_sequence).strip().lower() or "by_layer"
        self.spiral_vase = bool(self.spiral_vase)
        self.ignore_inner_color = bool(self.ignore_inner_color)
        self.timelapse_mode = str(self.timelapse_mode).strip().lower() or "traditional"
        self.fuzzy_skin = str(self.fuzzy_skin).strip().lower() or "none"
        self.prime_tower_enabled = bool(self.prime_tower_enabled)
        self.prime_tower_width = max(0.0, float(self.prime_tower_width))
        self.prime_tower_square = bool(self.prime_tower_square)
        self.prime_tower_volume = max(0.0, float(self.prime_tower_volume))
        self.flush_into_infill = bool(self.flush_into_infill)
        self.flush_into_support = bool(self.flush_into_support)
        self.z_hop_height = max(0.0, float(self.z_hop_height))
        self.ironing_speed = max(1.0, float(self.ironing_speed))
        self.ironing_flow = max(0.0, min(1.0, float(self.ironing_flow)))
        self.detect_overhang_walls = bool(self.detect_overhang_walls)
        self.make_overhangs_printable = bool(self.make_overhangs_printable)
        self.extra_perimeters_on_overhangs = bool(self.extra_perimeters_on_overhangs)
        self.reverse_overhang_on_odd = bool(self.reverse_overhang_on_odd)
        self.overhang_optimization = bool(self.overhang_optimization)
        self.adaptive_overhang_enabled = bool(self.adaptive_overhang_enabled or self.overhang_optimization
                                              or self.make_overhangs_printable)
        self.adaptive_overhang_threshold = max(0.0,
                                               min(1.0, float(self.adaptive_overhang_threshold)))
        self.adaptive_overhang_height = max(self.min_layer_height,
                                            min(float(self.adaptive_overhang_height),
                                                self.max_layer_height))
        if self.make_overhangs_printable:
            self.adaptive_overhang_height = min(self.adaptive_overhang_height,
                                                self.min_layer_height)
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

    def move_wipe(self, x: float, y: float, z: float, speed: float):
        self.add(f"G1 X{x:.3f} Y{y:.3f} Z{z:.3f} F{speed * 60:.0f}")
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

    def perimeter_loop(self,
                       points: Iterable[Tuple[float, float]],
                       z: float,
                       speed: float,
                       width: Optional[float] = None,
                       multiplier: Optional[float] = None,
                       seam_gap: float = 0.0,
                       wipe_distance: float = 0.0,
                       wipe_speed: Optional[float] = None):
        pts = list(points)
        if not pts:
            return
        if len(pts) > 2 and pts[0] != pts[-1]:
            pts.append(pts[0])
        x0, y0 = pts[0]
        self.move_travel(x0, y0, z, self.settings.travel_speed)
        line_width = self.settings.extrusion_width if width is None else float(width)
        flow = self.settings.extrusion_multiplier if multiplier is None else float(multiplier)
        if self.settings.supports_arcs and self.settings.arc_fitting and len(pts) >= 5:
            try:
                from .. import path_planner
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
                        extrusion = self.extrusion_for_length(half_length,
                                                              width=line_width,
                                                              multiplier=flow)
                        self.move_arc_extrude(mid[0], mid[1], z, speed, extrusion,
                                              center_xy=(cx, cy),
                                              clockwise=fit.clockwise)
                        self.move_arc_extrude(x0, y0, z, speed, extrusion,
                                              center_xy=(cx, cy),
                                              clockwise=fit.clockwise)
                        return
        segments = []
        total_length = 0.0
        px, py = x0, y0
        for x, y in pts[1:]:
            length = math.hypot(x - px, y - py)
            segments.append((px, py, x, y, length))
            total_length += length
            px, py = x, y

        gap_length = 0.0
        if seam_gap > 0.0 and total_length > 0.0:
            gap_length = max(0.0, min(total_length, total_length * (seam_gap / 100.0)))
        remaining_gap = gap_length
        last_seg = None
        for px, py, x, y, length in segments:
            last_seg = (px, py, x, y, length)
            if length <= 0.0:
                continue
            if remaining_gap > 0.0:
                if remaining_gap >= length:
                    self.move_wipe(x, y, z, speed if wipe_speed is None else wipe_speed)
                    remaining_gap -= length
                    continue
                ratio = (length - remaining_gap) / length
                mid_x = px + (x - px) * ratio
                mid_y = py + (y - py) * ratio
                extrusion = self.extrusion_for_length(length - remaining_gap,
                                                      width=line_width,
                                                      multiplier=flow)
                self.move_extrude(mid_x, mid_y, z, speed, extrusion=extrusion)
                self.move_wipe(x, y, z, speed if wipe_speed is None else wipe_speed)
                remaining_gap = 0.0
                continue
            extrusion = self.extrusion_for_length(length, width=line_width, multiplier=flow)
            self.move_extrude(x, y, z, speed, extrusion=extrusion)

        if wipe_distance > 0.0 and last_seg is not None:
            px, py, x, y, length = last_seg
            if length > 1e-6:
                dist = min(wipe_distance, length)
                ratio = 1.0 - (dist / length)
                wx = px + (x - px) * ratio
                wy = py + (y - py) * ratio
                self.move_wipe(wx, wy, z, speed if wipe_speed is None else wipe_speed)

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
