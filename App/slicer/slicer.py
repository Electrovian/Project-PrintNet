from dataclasses import dataclass
import math
import random
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple, cast

import numpy as np

from .mesh import MeshModel
from .geometry import (Island2D, LineSegment2D, Polygon2D, compensate_holes,
                       ensure_winding, gap_fill_lines, offset_islands, point_in_island,
                       thin_wall_lines)
from .gcode import GCodeWriter, SliceSettings
from . import infill as infill_generator
from . import path_planner

@dataclass
class IslandPerimeters:
    outer: Polygon2D
    holes: List[Polygon2D]

@dataclass
class PerimeterShell:
    index: int
    islands: List[IslandPerimeters]

@dataclass
class LayerPerimeters:
    z: float
    shells: List[PerimeterShell]

@dataclass
class LayerInfill:
    lines: List[LineSegment2D]
    pattern: str
    density: float
    angle: float
    is_solid: bool
    solid_kind: str

@dataclass
class IroningPass:
    lines: List[LineSegment2D]
    speed: float
    flow: float

@dataclass
class BridgeInfill:
    regions: List[path_planner.BridgeRegion]
    speed: float
    extrusion_width: float
    flow_ratio: float

@dataclass
class BrimPlan:
    loops: List[Polygon2D]
    z: float

@dataclass
class SkirtPlan:
    loops: List[Polygon2D]
    z: float

@dataclass
class RaftLayer:
    z: float
    lines: List[LineSegment2D]
    angle: float

@dataclass
class LayerPlan:
    z: float
    shells: List[PerimeterShell]
    infill: LayerInfill
    bridge: Optional[BridgeInfill]
    ironing: Optional[IroningPass]
    thin_walls: List[LineSegment2D]
    gap_fill: List[LineSegment2D]
    is_top: bool
    is_bottom: bool
    has_overhang: bool

@dataclass
class PrintPlan:
    raft_layers: List[RaftLayer]
    brim: Optional[BrimPlan]
    skirt: Optional[SkirtPlan]
    layers: List[LayerPlan]

def _wrap_islands(islands: List[Island2D]) -> List[IslandPerimeters]:
    return [IslandPerimeters(outer=outer, holes=holes) for outer, holes in islands]

def _polygon_area(points: Sequence[Tuple[float, float]]) -> float:
    if not points or len(points) < 3:
        return 0.0
    area = 0.0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        area += x1 * y2 - x2 * y1
    return area * 0.5

def _island_area(island: Island2D) -> float:
    outer, holes = island
    area = abs(_polygon_area(outer))
    for hole in holes:
        area -= abs(_polygon_area(hole))
    return max(0.0, area)

def _holes_as_islands(islands: Sequence[Island2D]) -> List[Island2D]:
    results: List[Island2D] = []
    for _outer, holes in islands:
        for hole in holes:
            oriented = ensure_winding(hole, clockwise=True)
            if oriented:
                results.append((oriented, []))
    return results

def _close_gap_islands(islands: List[Island2D], radius: float) -> List[Island2D]:
    if radius <= 0.0:
        return islands
    expanded = offset_islands(islands, radius)
    if not expanded:
        return islands
    closed = offset_islands(expanded, -radius)
    return closed or islands

def _wall_spacing(settings: SliceSettings, layer_index: int) -> float:
    spacing = max(0.01, float(settings.inner_wall_line_width))
    if settings.wall_generator == "arachne":
        min_pct = settings.first_layer_min_wall_width if layer_index == 0 else settings.min_wall_width
        min_width = max(0.01, float(settings.nozzle_diameter) * (min_pct / 100.0))
        spacing = max(min_width, spacing / max(1, settings.wall_distribution_count))
    return spacing

def _thin_wall_width(settings: SliceSettings, layer_index: int) -> float:
    base = max(0.01, float(settings.extrusion_width))
    if settings.wall_generator != "arachne":
        return base
    min_pct = settings.first_layer_min_wall_width if layer_index == 0 else settings.min_wall_width
    min_width = max(0.01, float(settings.nozzle_diameter) * (min_pct / 100.0))
    return max(min_width, base / max(1, settings.wall_distribution_count))

def _filter_thin_walls(lines: List[LineSegment2D], settings: SliceSettings) -> List[LineSegment2D]:
    if settings.wall_generator != "arachne":
        return lines
    if not lines:
        return lines
    nozzle = max(0.01, float(settings.nozzle_diameter))
    min_feature = nozzle * (settings.min_feature_size / 100.0)
    angle_scale = max(0.5, settings.wall_transition_angle / 45.0)
    margin_scale = 1.0 + (settings.wall_transition_filter_margin / 100.0)
    length_scale = max(0.1, settings.wall_transition_length / 100.0)
    min_length = max(settings.min_wall_length, min_feature)
    min_length *= angle_scale * margin_scale * length_scale
    if min_length <= 0.0:
        return lines
    filtered = []
    for start, end in lines:
        length = math.hypot(end[0] - start[0], end[1] - start[1])
        if length >= min_length:
            filtered.append((start, end))
    return filtered

def _offset_holes(islands: List[Island2D], delta: float) -> List[Island2D]:
    if abs(delta) <= 1e-6:
        return islands
    adjusted: List[Island2D] = []
    for outer, holes in islands:
        new_holes: List[Polygon2D] = []
        for hole in holes:
            offset = offset_islands([(hole, [])], delta)
            if offset:
                hole_loop = ensure_winding(offset[0][0], clockwise=False)
                if hole_loop:
                    new_holes.append(hole_loop)
                    continue
            oriented = ensure_winding(hole, clockwise=False)
            if oriented:
                new_holes.append(oriented)
        adjusted.append((outer, new_holes))
    return adjusted

def _polyhole_for_polygon(polygon: Polygon2D, nozzle: float) -> Polygon2D:
    base = polygon[:-1] if polygon and polygon[0] == polygon[-1] else list(polygon)
    if len(base) < 3:
        return polygon
    cx = sum(p[0] for p in base) / len(base)
    cy = sum(p[1] for p in base) / len(base)
    radii = [math.hypot(p[0] - cx, p[1] - cy) for p in base]
    mean_r = sum(radii) / len(radii)
    if mean_r <= 1e-6:
        return polygon
    variance = sum((r - mean_r) ** 2 for r in radii) / len(radii)
    if variance / (mean_r * mean_r) > 0.2:
        return polygon
    segment = max(0.1, nozzle * 0.75)
    sides = max(6, int(math.ceil((2.0 * math.pi * mean_r) / segment)))
    points = []
    for i in range(sides):
        angle = (2.0 * math.pi * i) / sides
        points.append((cx + mean_r * math.cos(angle), cy + mean_r * math.sin(angle)))
    points.append(points[0])
    return ensure_winding(points, clockwise=False)

def _convert_holes_to_polyholes(islands: List[Island2D], nozzle: float) -> List[Island2D]:
    if nozzle <= 0.0:
        return islands
    converted: List[Island2D] = []
    for outer, holes in islands:
        new_holes = []
        for hole in holes:
            new_holes.append(_polyhole_for_polygon(hole, nozzle))
        converted.append((outer, new_holes))
    return converted

def _normalize_height_ranges(ranges: Optional[Sequence[object]]
                             ) -> List[Tuple[float, float, float]]:
    cleaned: List[Tuple[float, float, float]] = []
    for entry in ranges or []:
        if isinstance(entry, dict):
            start = entry.get("start", entry.get("z_min", entry.get("min")))
            end = entry.get("end", entry.get("z_max", entry.get("max")))
            height = entry.get("height", entry.get("layer_height"))
        elif isinstance(entry, (list, tuple)) and len(entry) >= 3:
            start, end, height = entry[0], entry[1], entry[2]
        else:
            continue
        if start is None or end is None or height is None:
            continue
        try:
            start_f = float(start)
            end_f = float(end)
            height_f = float(height)
        except Exception:
            continue
        if end_f <= start_f or height_f <= 0.0:
            continue
        cleaned.append((start_f, end_f, height_f))
    return sorted(cleaned, key=lambda item: item[0])

def build_z_heights(mesh: MeshModel, settings: SliceSettings) -> List[float]:
    """Generate variable Z heights using manual ranges and overhang data."""
    (mn_x, mn_y, mn_z), (_mx_x, _mx_y, mx_z) = mesh.bounds
    z_min = float(mn_z)
    z_max = float(mx_z)
    if z_max <= z_min:
        return []

    base_height = max(settings.min_layer_height,
                      min(settings.layer_height, settings.max_layer_height))
    ranges = _normalize_height_ranges(settings.layer_height_ranges)

    ratios = None
    if settings.adaptive_overhang_enabled:
        centers = np.asarray(mesh.mesh.triangles_center, dtype=float)
        normals = np.asarray(mesh.mesh.face_normals, dtype=float)
        if centers.size and normals.size:
            bins = np.arange(z_min, z_max + base_height, base_height)
            if bins.size >= 2:
                total_counts, _ = np.histogram(centers[:, 2], bins=bins)
                cos_limit = math.cos(math.radians(float(settings.overhang_angle)))
                mask = (normals[:, 2] < cos_limit) & (normals[:, 2] < 0.0)
                over_counts, _ = np.histogram(centers[mask][:, 2], bins=bins)
                ratios = []
                for total, over in zip(total_counts, over_counts):
                    if total <= 0:
                        ratios.append(0.0)
                    else:
                        ratios.append(float(over) / float(total))

    z = z_min
    heights: List[float] = []
    while z < z_max - 1e-6:
        height = base_height
        for start, end, h in ranges:
            if start <= z < end:
                height = h
                break
        height = max(settings.min_layer_height,
                     min(float(height), settings.max_layer_height))

        if ratios is not None and settings.adaptive_overhang_enabled:
            idx = int((z - z_min) / base_height)
            if 0 <= idx < len(ratios):
                if ratios[idx] >= settings.adaptive_overhang_threshold:
                    height = min(height, settings.adaptive_overhang_height)
                    height = max(settings.min_layer_height,
                                 min(float(height), settings.max_layer_height))

        if z + height > z_max:
            if settings.precise_z_height:
                height = z_max - z
            elif (z_max - z) > settings.min_layer_height * 0.5:
                height = z_max - z

        z += height
        heights.append(float(z))
    return heights

def generate_layer_perimeters(mesh: MeshModel,
                              z_heights: Iterable[float],
                              settings: Optional[SliceSettings] = None,
                              perimeter_count: Optional[int] = None,
                              perimeter_spacing: Optional[float] = None
                              ) -> List[LayerPerimeters]:
    """Return per-layer perimeter shells with islands and holes grouped."""
    if settings is None:
        settings = SliceSettings()
    if perimeter_count is None:
        perimeter_count = settings.perimeter_count
    if perimeter_spacing is None:
        perimeter_spacing = settings.inner_wall_line_width
    perimeter_count = max(1, int(perimeter_count))

    layers: List[LayerPerimeters] = []
    for layer_index, z in enumerate(z_heights):
        z_value = float(z)
        tolerance = settings.resolution if settings.resolution > 0.0 else 0.0
        base_islands = mesh.slice_layer(z_value, tolerance=tolerance)
        if settings.slice_gap_closing_radius > 0.0 and base_islands:
            base_islands = _close_gap_islands(base_islands, settings.slice_gap_closing_radius)
        if settings.xy_contour_compensation != 0.0 and base_islands:
            offset = offset_islands(base_islands, settings.xy_contour_compensation)
            if offset:
                base_islands = offset
        if settings.xy_hole_compensation != 0.0 and base_islands:
            if settings.xy_hole_compensation > 0.0:
                base_islands = compensate_holes(base_islands, settings.xy_hole_compensation)
            else:
                base_islands = _offset_holes(base_islands, settings.xy_hole_compensation)
        if settings.convert_holes_to_polyholes and base_islands:
            base_islands = _convert_holes_to_polyholes(base_islands, settings.nozzle_diameter)
        if (settings.elephant_foot_compensation > 0.0
                and layer_index < settings.elephant_foot_compensation_layers
                and base_islands):
            offset = offset_islands(base_islands, -settings.elephant_foot_compensation)
            if offset:
                base_islands = offset
        if settings.hole_compensation_mm > 0.0 and base_islands:
            base_islands = compensate_holes(base_islands, settings.hole_compensation_mm)
        shells: List[PerimeterShell] = []
        if base_islands:
            shells.append(PerimeterShell(index=0, islands=_wrap_islands(base_islands)))

        current_islands = base_islands
        spacing = float(perimeter_spacing)
        if settings.wall_generator == "arachne":
            spacing = _wall_spacing(settings, layer_index)
        outer_spacing = spacing
        if settings.precise_wall and settings.wall_printing_order == "inner_outer":
            try:
                outer_spacing = max(0.01, float(settings.outer_wall_line_width))
            except (TypeError, ValueError):
                outer_spacing = spacing
            if settings.wall_generator == "arachne":
                outer_spacing = max(outer_spacing, spacing)
        for shell_index in range(1, perimeter_count):
            if not current_islands:
                break
            step = outer_spacing if shell_index == 1 else spacing
            current_islands = offset_islands(current_islands, -step)
            if not current_islands:
                break
            shells.append(PerimeterShell(index=shell_index,
                                         islands=_wrap_islands(current_islands)))
        layers.append(LayerPerimeters(z=z_value, shells=shells))
    return layers

def _shells_to_islands(shell: PerimeterShell) -> List[Island2D]:
    return [(island.outer, island.holes) for island in shell.islands]

def generate_layer_plans(mesh: MeshModel,
                         z_heights: Optional[Iterable[float]] = None,
                         settings: Optional[SliceSettings] = None,
                         perimeter_count: Optional[int] = None,
                         perimeter_spacing: Optional[float] = None
                         ) -> PrintPlan:
    if settings is None:
        settings = SliceSettings()

    if z_heights is None:
        z_heights = build_z_heights(mesh, settings)
    z_heights = list(z_heights)
    if not z_heights:
        return PrintPlan(raft_layers=[],
                         brim=None,
                         skirt=None,
                         layers=[])

    layers = generate_layer_perimeters(mesh,
                                       z_heights,
                                       settings=settings,
                                       perimeter_count=perimeter_count,
                                       perimeter_spacing=perimeter_spacing)
    total_layers = len(layers)
    plans: List[LayerPlan] = []
    raft_layers: List[RaftLayer] = []
    brim_plan: Optional[BrimPlan] = None
    skirt_plan: Optional[SkirtPlan] = None

    z_offset = settings.raft_layers * settings.layer_height

    if layers and settings.raft_layers > 0:
        base_islands = _shells_to_islands(layers[0].shells[0]) if layers[0].shells else []
        raft_islands = offset_islands(base_islands, settings.raft_margin) if base_islands else []
        for raft_index in range(settings.raft_layers):
            z = settings.layer_height * float(raft_index + 1)
            angle = settings.infill_angle + (raft_index % 2) * 90.0
            lines = infill_generator.rectilinear_infill(
                raft_islands,
                density=1.0,
                angle_deg=angle,
                layer_index=raft_index,
                extrusion_width=settings.extrusion_width,
                alternate=False,
            )
            raft_layers.append(RaftLayer(z=z, lines=lines, angle=angle))
    for index, layer in enumerate(layers):
        is_bottom = index < settings.bottom_layers
        is_top = index >= max(0, total_layers - settings.top_layers)
        infill_density = float(settings.infill_density or 0.0)
        is_solid = is_bottom or is_top
        solid_kind = "sparse"
        if is_solid:
            density = 1.0
            solid_kind = "top" if is_top else "bottom"
        elif infill_density >= 0.999:
            density = 1.0
            solid_kind = "internal"
            is_solid = True
        else:
            density = infill_density
            solid_kind = "sparse"
        pattern = "rectilinear" if is_solid else settings.infill_pattern
        angle = settings.infill_angle
        alternate = not is_top

        islands: List[Island2D] = []
        if layer.shells:
            islands = _shells_to_islands(layer.shells[-1])

        spacing = _wall_spacing(settings, index)
        thin_width = _thin_wall_width(settings, index)
        thin_lines = thin_wall_lines(islands, thin_width)
        thin_lines = _filter_thin_walls(thin_lines, settings)
        gap_lines = gap_fill_lines(islands,
                                   settings.extrusion_width,
                                   spacing)

        lines = infill_generator.generate_infill(islands,
                                                  density=float(density),
                                                  angle_deg=angle,
                                                  layer_index=index,
                                                  extrusion_width=settings.extrusion_width,
                                                  pattern=pattern,
                                                  alternate=alternate)
        infill = LayerInfill(lines=lines,
                             pattern=pattern,
                             density=float(density),
                             angle=angle,
                             is_solid=is_solid,
                             solid_kind=solid_kind)

        bridge: Optional[BridgeInfill] = None
        ironing: Optional[IroningPass] = None
        has_overhang = False
        if index > 0 and layer.shells and layers[index - 1].shells:
            current_islands = _shells_to_islands(layer.shells[0])
            below_islands = _shells_to_islands(layers[index - 1].shells[0])
            bridge_islands = path_planner.detect_bridge_islands(current_islands, below_islands)
            if bridge_islands and settings.detect_overhang_walls:
                has_overhang = True
            filtered = bridge_islands
            if bridge_islands and settings.bridge_filter_mode != "none":
                base = settings.extrusion_width
                if settings.bridge_filter_mode == "limited":
                    min_area = (base * 1.5) ** 2
                else:
                    min_area = (base * 3.0) ** 2
                filtered = [island for island in bridge_islands
                            if _island_area(island) >= min_area]
            regions: List[path_planner.BridgeRegion] = []
            if filtered and settings.bridge_density > 0.0:
                density = max(0.0, min(1.0, settings.bridge_density / 100.0))
                bridge_width = settings.bridge_extrusion_width
                if is_top and settings.thick_bridges:
                    bridge_width *= 1.2
                elif (not is_top) and settings.thick_internal_bridges:
                    bridge_width *= 1.2
                regions = path_planner.generate_bridge_infill(filtered,
                                                              layer_index=index,
                                                              extrusion_width=bridge_width,
                                                              density=density)
                if settings.bridge_counterbore_holes != "none":
                    hole_islands = _holes_as_islands(current_islands)
                    if hole_islands:
                        hole_density = density
                        if settings.bridge_counterbore_holes == "partial":
                            hole_density = min(1.0, density * 0.5)
                        elif settings.bridge_counterbore_holes == "sacrificial":
                            hole_density = 1.0
                        regions.extend(path_planner.generate_bridge_infill(
                            hole_islands,
                            layer_index=index,
                            extrusion_width=bridge_width,
                            density=hole_density,
                        ))
                if regions:
                    flow_ratio = (settings.bridge_flow_ratio if is_top
                                  else settings.internal_bridge_flow_ratio)
                    bridge = BridgeInfill(regions=regions,
                                          speed=settings.bridge_speed,
                                          extrusion_width=bridge_width,
                                          flow_ratio=flow_ratio)

        ironing_mode = settings.ironing_type
        ironing_enabled = False
        if ironing_mode == "all_solid_layers":
            ironing_enabled = is_solid
        elif ironing_mode == "topmost_surface_only":
            ironing_enabled = is_top and index == total_layers - 1
        elif ironing_mode == "all_top_surfaces":
            ironing_enabled = is_top and is_solid

        if ironing_enabled:
            ironing_islands: List[Island2D] = []
            if layer.shells:
                ironing_islands = _shells_to_islands(layer.shells[-1])
            if ironing_islands:
                ironing_lines = infill_generator.rectilinear_infill(
                    ironing_islands,
                    density=1.0,
                    angle_deg=settings.infill_angle,
                    layer_index=index,
                    extrusion_width=settings.extrusion_width,
                    alternate=False,
                )
                if ironing_lines:
                    ironing = IroningPass(lines=ironing_lines,
                                          speed=settings.ironing_speed,
                                          flow=settings.ironing_flow)
        plans.append(LayerPlan(z=layer.z + z_offset,
                               shells=layer.shells,
                               infill=infill,
                               bridge=bridge,
                               ironing=ironing,
                               thin_walls=thin_lines,
                               gap_fill=gap_lines,
                               is_top=is_top,
                               is_bottom=is_bottom,
                               has_overhang=has_overhang))
    if layers:
        first_layer = layers[0]
        base_islands = _shells_to_islands(first_layer.shells[0]) if first_layer.shells else []
        if settings.brim_width > 0.0 and base_islands:
            count = int(math.ceil(settings.brim_width / settings.extrusion_width))
            loops: List[Polygon2D] = []
            current = base_islands
            for _ in range(count):
                current = offset_islands(current, settings.extrusion_width)
                for outer, _holes in current:
                    loops.append(outer)
            if loops:
                brim_plan = BrimPlan(loops=loops, z=first_layer.z + z_offset)

        if settings.skirt_loops > 0 and base_islands:
            loops = []
            current = offset_islands(base_islands, settings.skirt_distance)
            for _ in range(settings.skirt_loops):
                if not current:
                    break
                for outer, _holes in current:
                    loops.append(outer)
                current = offset_islands(current, settings.extrusion_width)
            if loops:
                skirt_plan = SkirtPlan(loops=loops, z=first_layer.z + z_offset)

    return PrintPlan(raft_layers=raft_layers,
                     brim=brim_plan,
                     skirt=skirt_plan,
                     layers=plans)

def _emit_gcode(plan: PrintPlan,
                output_gcode_path: str,
                settings: SliceSettings) -> str:
    writer = GCodeWriter(settings=settings)  # type: ignore[arg-type]
    writer.write_header()

    rng = random.Random()

    def _seam_mode(mode: str) -> str:
        mode_norm = (mode or "").strip().lower()
        if mode_norm == "back":
            return "rear"
        if mode_norm in ("assemble", "nearest"):
            return "aligned"
        return mode_norm or "aligned"

    def _rotate_loop(loop: Polygon2D, offset: int) -> Polygon2D:
        points = loop[:-1] if loop and loop[0] == loop[-1] else list(loop)
        if not points:
            return loop
        offset = offset % len(points)
        ordered = points[offset:] + points[:offset]
        ordered.append(ordered[0])
        return ordered

    def _apply_direction(loop: Polygon2D, layer_index: int, has_overhang: bool) -> Polygon2D:
        if not loop:
            return loop
        direction = settings.wall_loop_direction
        reverse_on_odd = settings.reverse_overhang_on_odd and has_overhang and (layer_index % 2 == 1)
        if direction == "auto":
            return list(reversed(loop)) if reverse_on_odd else loop
        clockwise = direction == "clockwise"
        if reverse_on_odd:
            clockwise = not clockwise
        return ensure_winding(loop, clockwise=clockwise)

    def _apply_seam(loop: Polygon2D, shell_index: int, anchor: Tuple[float, float]) -> Polygon2D:
        mode = _seam_mode(settings.seam_position)
        anchor_point = None
        if settings.seam_position.strip().lower() == "nearest":
            anchor_point = anchor
        elif mode == "aligned":
            anchor_point = (0.0, 0.0)
        placed = path_planner.apply_seam_placement(loop, mode, anchor=anchor_point, rng=rng)
        if settings.staggered_inner_seams and shell_index > 0:
            offset = max(1, int(len(placed) * 0.25 * shell_index))
            placed = _rotate_loop(placed, offset)
        return placed

    def _wipe_speed() -> float:
        if settings.wipe_use_base_speed:
            return settings.print_speed * (settings.wipe_speed_percent / 100.0)
        return settings.wipe_speed_percent

    def _emit_loop(loop: Polygon2D,
                   z: float,
                   speed: float,
                   width: float,
                   multiplier: float,
                   shell_index: int,
                   layer_index: int,
                   has_overhang: bool,
                   is_hole: bool,
                   allow_gap: bool,
                   wipe: bool) -> None:
        if not loop:
            return
        anchor = (float(writer.position[0]), float(writer.position[1]))
        prepared = _apply_direction(loop, layer_index, has_overhang)
        prepared = _apply_seam(prepared, shell_index, anchor)
        seam_gap = settings.seam_gap if allow_gap else 0.0
        wipe_distance = width * 2.0 if wipe else 0.0
        wipe_speed = _wipe_speed() if wipe else None
        writer.perimeter_loop(prepared,
                              z=z,
                              speed=speed,
                              width=width,
                              multiplier=multiplier,
                              seam_gap=seam_gap,
                              wipe_distance=wipe_distance,
                              wipe_speed=wipe_speed)

    def emit_islands(islands: List[Island2D],
                     z: float,
                     speed: float,
                     label: str,
                     width: float,
                     multiplier: float,
                     shell_index: int,
                     layer_index: int,
                     has_overhang: bool,
                     allow_gap: bool,
                     wipe: bool) -> None:
        if not islands:
            return
        writer.add(f";TYPE:{label}")
        for outer, holes in islands:
            if outer:
                _emit_loop(outer, z, speed, width, multiplier, shell_index,
                           layer_index, has_overhang, False, allow_gap, wipe)
            for hole in holes:
                hole_gap = allow_gap and settings.scarf_joint_seam == "contour_hole"
                _emit_loop(hole, z, speed, width, multiplier, shell_index,
                           layer_index, has_overhang, True, hole_gap, wipe)

    def _pick_island(islands: Sequence[Island2D],
                     point: Tuple[float, float]) -> Optional[Island2D]:
        for island in islands:
            if point_in_island(point, island):
                return island
        return None

    def emit_lines(lines: List[LineSegment2D],
                   z: float,
                   speed: float,
                   label: str,
                   width: float,
                   multiplier: float,
                   comb_islands: Sequence[Island2D] | None = None) -> None:
        if not lines:
            return
        writer.add(f";TYPE:{label}")
        for start, end in lines:
            if settings.avoid_crossing_walls and comb_islands:
                island = _pick_island(comb_islands, start)
                if island is not None:
                    travel_path = path_planner.plan_travel(
                        (writer.position[0], writer.position[1], z),
                        (start[0], start[1], z),
                        retracted=writer.has_extruded,
                        z_hop_height=settings.z_hop_height,
                        comb_island=island,
                        z_hop_only_outside=True,
                    )
                    for tx, ty, tz in travel_path[1:]:
                        writer.move_travel(tx, ty, tz, settings.travel_speed)
                else:
                    writer.move_travel(start[0], start[1], z, settings.travel_speed)
            else:
                writer.move_travel(start[0], start[1], z, settings.travel_speed)

            length = math.hypot(end[0] - start[0], end[1] - start[1])
            flow_multiplier = multiplier
            if settings.small_area_flow_compensation and width > 0.0 and length > 0.0:
                scale = min(1.0, max(0.6, length / (width * 2.5)))
                flow_multiplier *= scale
            extrusion = writer.extrusion_for_length(length, width=width, multiplier=flow_multiplier)
            writer.move_extrude(end[0], end[1], z, speed, extrusion=extrusion)

    # Raft
    for raft in plan.raft_layers:
        writer.add(";LAYER:RAFT")
        writer.add(";TYPE:RAFT")
        writer.settings.layer_height = settings.layer_height
        emit_lines(raft.lines,
                   z=raft.z,
                   speed=settings.print_speed,
                   label="RAFT",
                   width=settings.extrusion_width,
                   multiplier=1.0)

    # Skirt/Brim
    if plan.skirt is not None:
        emit_lines([(loop[i], loop[i + 1]) for loop in plan.skirt.loops for i in range(len(loop) - 1)],
                   plan.skirt.z,
                   settings.print_speed,
                   "SKIRT",
                   settings.first_layer_line_width,
                   1.0)
    if plan.brim is not None:
        emit_lines([(loop[i], loop[i + 1]) for loop in plan.brim.loops for i in range(len(loop) - 1)],
                   plan.brim.z,
                   settings.print_speed,
                   "BRIM",
                   settings.first_layer_line_width,
                   1.0)

    prev_z = 0.0
    prev_wall_speed_factor = None
    for idx, layer in enumerate(plan.layers):
        writer.add(f";LAYER:{idx}")
        layer_height = layer.z - prev_z
        if layer_height > 0.0:
            writer.settings.layer_height = layer_height
        prev_z = layer.z
        wall_speed_factor = 1.0
        if settings.smooth_wall_speed_z and settings.layer_height > 0.0:
            wall_speed_factor = max(0.3, min(2.0, layer_height / settings.layer_height))
            if prev_wall_speed_factor is None:
                prev_wall_speed_factor = wall_speed_factor
            else:
                wall_speed_factor = (prev_wall_speed_factor * 0.5) + (wall_speed_factor * 0.5)
                prev_wall_speed_factor = wall_speed_factor
        wall_speed = settings.print_speed * wall_speed_factor

        def _should_single_wall() -> bool:
            if settings.one_wall_threshold <= 0.0:
                return True
            threshold = settings.extrusion_width * (settings.one_wall_threshold / 100.0)
            if not layer.shells:
                return False
            islands = _shells_to_islands(layer.shells[0])
            for outer, _holes in islands:
                if not outer:
                    continue
                xs = [p[0] for p in outer]
                ys = [p[1] for p in outer]
                if not xs or not ys:
                    continue
                span = min(max(xs) - min(xs), max(ys) - min(ys))
                if span <= threshold:
                    return True
            return False

        shells = list(layer.shells)
        if settings.only_one_wall_top and layer.is_top and _should_single_wall():
            shells = shells[:1]
        if settings.only_one_wall_first_layer and idx == 0 and _should_single_wall():
            shells = shells[:1]

        if settings.wall_printing_order == "inner_outer":
            ordered_shells = list(reversed(shells))
        elif settings.wall_printing_order == "inner_outer_inner" and len(shells) > 2:
            inner_shells = list(reversed(shells[1:]))
            ordered_shells = [inner_shells[0], shells[0]] + inner_shells[1:]
        elif settings.wall_printing_order == "adaptive_outer_inner" and layer.has_overhang:
            ordered_shells = list(reversed(shells))
        else:
            ordered_shells = shells

        def emit_perimeters():
            for shell in ordered_shells:
                islands = _shells_to_islands(shell)
                label = "WALL-OUTER" if shell.index == 0 else "WALL-INNER"
                width = settings.outer_wall_line_width if shell.index == 0 else settings.inner_wall_line_width
                if idx == 0:
                    width = settings.first_layer_line_width
                allow_gap = settings.seam_gap > 0.0 and shell.index == 0
                wipe = settings.wipe_on_loops
                if settings.wipe_before_external_loop and shell.index > 0 and any(
                        s.index == 0 for s in ordered_shells):
                    wipe = True
                emit_islands(islands,
                             layer.z,
                             wall_speed,
                             label,
                             width,
                             1.0,
                             shell.index,
                             idx,
                             layer.has_overhang,
                             allow_gap,
                             wipe)
                if shell.index == 0 and settings.extra_perimeters_on_overhangs and layer.has_overhang:
                    emit_islands(islands,
                                 layer.z,
                                 wall_speed,
                                 label,
                                 width,
                                 1.0,
                                 shell.index,
                                 idx,
                                 layer.has_overhang,
                                 allow_gap,
                                 wipe)

        def emit_infill():
            if layer.infill and layer.infill.lines:
                if layer.infill.solid_kind == "top":
                    label = "TOP"
                    width = settings.top_surface_line_width
                    multiplier = settings.top_surface_flow_ratio
                elif layer.infill.solid_kind == "bottom":
                    label = "BOTTOM"
                    width = settings.top_surface_line_width if idx == 0 else settings.extrusion_width
                    multiplier = settings.bottom_surface_flow_ratio
                elif layer.infill.solid_kind == "internal":
                    label = "SOLID-INFILL"
                    width = settings.internal_solid_infill_line_width
                    multiplier = 1.0
                else:
                    label = "INFILL"
                    width = settings.sparse_infill_line_width
                    multiplier = 1.0
                if idx == 0:
                    width = settings.first_layer_line_width
                emit_lines(layer.infill.lines,
                           z=layer.z,
                           speed=settings.print_speed,
                           label=label,
                           width=width,
                           multiplier=multiplier,
                           comb_islands=_shells_to_islands(layer.shells[-1]) if layer.shells else None)

        if settings.print_infill_first:
            emit_infill()
            emit_perimeters()
        else:
            emit_perimeters()
            emit_infill()

        if layer.thin_walls:
            emit_lines(layer.thin_walls,
                       z=layer.z,
                       speed=wall_speed,
                       label="THIN_WALL",
                       width=settings.inner_wall_line_width,
                       multiplier=1.0,
                       comb_islands=_shells_to_islands(layer.shells[-1]) if layer.shells else None)

        if layer.gap_fill:
            emit_lines(layer.gap_fill,
                       z=layer.z,
                       speed=wall_speed,
                       label="GAP_FILL",
                       width=settings.extrusion_width,
                       multiplier=1.0,
                       comb_islands=_shells_to_islands(layer.shells[-1]) if layer.shells else None)

        if layer.bridge is not None:
            for region in layer.bridge.regions:
                emit_lines(region.lines,
                           z=layer.z,
                           speed=layer.bridge.speed,
                           label="BRIDGE",
                           width=layer.bridge.extrusion_width,
                           multiplier=layer.bridge.flow_ratio,
                           comb_islands=_shells_to_islands(layer.shells[-1]) if layer.shells else None)

        if layer.ironing is not None:
            emit_lines(layer.ironing.lines,
                       z=layer.z,
                       speed=layer.ironing.speed,
                       label="IRONING",
                       width=settings.extrusion_width,
                       multiplier=layer.ironing.flow,
                       comb_islands=_shells_to_islands(layer.shells[-1]) if layer.shells else None)

    writer.write_footer()

    with open(output_gcode_path, "w", encoding="utf-8") as f:
        f.write(writer.get_gcode())

    return output_gcode_path


def slice_mesh_model(mesh: MeshModel,
                     output_gcode_path: Optional[str] = None,
                     settings: Optional[SliceSettings] = None,
                     source_path: Optional[str] = None) -> str:
    if settings is None:
        settings = SliceSettings()
    settings_obj = cast(SliceSettings, settings)
    plan = generate_layer_plans(mesh, None, settings=settings_obj)
    if output_gcode_path is None:
        source = source_path or mesh.path or "model"
        output_gcode_path = str(Path(source).with_suffix(".gcode"))
    return _emit_gcode(plan, output_gcode_path, settings_obj)


def slice_trimesh(mesh,
                  output_gcode_path: Optional[str] = None,
                  settings: Optional[SliceSettings] = None,
                  source_path: Optional[str] = None) -> str:
    model = MeshModel.from_trimesh(mesh, path=source_path or "<memory>")
    return slice_mesh_model(model,
                            output_gcode_path=output_gcode_path,
                            settings=settings,
                            source_path=source_path)


def slice_file(stl_path: str, output_gcode_path: Optional[str] = None,
               settings: Optional[SliceSettings] = None) -> str:
    """Slice an STL into multi-layer toolpaths and emit G-code."""
    stl_path = str(stl_path)
    mesh = MeshModel.from_file(stl_path)
    return slice_mesh_model(mesh,
                            output_gcode_path=output_gcode_path,
                            settings=settings,
                            source_path=stl_path)
