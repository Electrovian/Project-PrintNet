from dataclasses import dataclass
import math
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple, cast

import numpy as np

from .mesh import MeshModel
from .geometry import (Island2D, LineSegment2D, Polygon2D, compensate_holes,
                       gap_fill_lines, offset_islands, thin_wall_lines)
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

@dataclass
class PrintPlan:
    raft_layers: List[RaftLayer]
    brim: Optional[BrimPlan]
    skirt: Optional[SkirtPlan]
    layers: List[LayerPlan]

def _wrap_islands(islands: List[Island2D]) -> List[IslandPerimeters]:
    return [IslandPerimeters(outer=outer, holes=holes) for outer, holes in islands]

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

        if z + height > z_max and (z_max - z) > settings.min_layer_height * 0.5:
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
        perimeter_spacing = settings.extrusion_width
    perimeter_count = max(1, int(perimeter_count))

    layers: List[LayerPerimeters] = []
    for z in z_heights:
        z_value = float(z)
        base_islands = mesh.slice_layer(z_value)
        if settings.hole_compensation_mm > 0.0 and base_islands:
            base_islands = compensate_holes(base_islands, settings.hole_compensation_mm)
        shells: List[PerimeterShell] = []
        if base_islands:
            shells.append(PerimeterShell(index=0, islands=_wrap_islands(base_islands)))

        current_islands = base_islands
        for shell_index in range(1, perimeter_count):
            if not current_islands:
                break
            current_islands = offset_islands(current_islands, -perimeter_spacing)
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
        is_solid = is_bottom or is_top
        pattern = "rectilinear" if is_solid else settings.infill_pattern
        density = 1.0 if is_solid else float(settings.infill_density or 0.0)
        angle = settings.infill_angle
        alternate = not is_top

        islands: List[Island2D] = []
        if layer.shells:
            islands = _shells_to_islands(layer.shells[-1])

        thin_lines = thin_wall_lines(islands, settings.extrusion_width)
        gap_lines = gap_fill_lines(islands,
                                   settings.extrusion_width,
                                   settings.extrusion_width)

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
                             is_solid=is_solid)

        bridge: Optional[BridgeInfill] = None
        ironing: Optional[IroningPass] = None
        if index > 0 and layer.shells and layers[index - 1].shells:
            current_islands = _shells_to_islands(layer.shells[0])
            below_islands = _shells_to_islands(layers[index - 1].shells[0])
            bridge_islands = path_planner.detect_bridge_islands(current_islands, below_islands)
            if bridge_islands:
                regions = path_planner.generate_bridge_infill(bridge_islands,
                                                              layer_index=index,
                                                              extrusion_width=settings.bridge_extrusion_width)
                if regions:
                    bridge = BridgeInfill(regions=regions,
                                          speed=settings.bridge_speed,
                                          extrusion_width=settings.bridge_extrusion_width)

        if is_top and is_solid and settings.ironing_enabled:
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
                               is_bottom=is_bottom))
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

    def emit_loops(loops: List[Polygon2D], z: float, speed: float, label: str):
        if not loops:
            return
        writer.add(f";TYPE:{label}")
        for loop in loops:
            writer.perimeter_loop(loop, z=z, speed=speed)

    def emit_islands(islands: List[Island2D], z: float, speed: float, label: str):
        if not islands:
            return
        writer.add(f";TYPE:{label}")
        for outer, holes in islands:
            if outer:
                writer.perimeter_loop(outer, z=z, speed=speed)
            for hole in holes:
                writer.perimeter_loop(hole, z=z, speed=speed)

    # Raft
    for raft in plan.raft_layers:
        writer.add(";LAYER:RAFT")
        writer.add(";TYPE:RAFT")
        writer.settings.layer_height = settings.layer_height
        writer.extrude_lines(raft.lines,
                             z=raft.z,
                             speed=settings.print_speed,
                             width=settings.extrusion_width)

    # Skirt/Brim
    if plan.skirt is not None:
        emit_loops(plan.skirt.loops, plan.skirt.z, settings.print_speed, "SKIRT")
    if plan.brim is not None:
        emit_loops(plan.brim.loops, plan.brim.z, settings.print_speed, "BRIM")

    prev_z = 0.0
    for idx, layer in enumerate(plan.layers):
        writer.add(f";LAYER:{idx}")
        layer_height = layer.z - prev_z
        if layer_height > 0.0:
            writer.settings.layer_height = layer_height
        prev_z = layer.z

        for shell in layer.shells:
            islands = _shells_to_islands(shell)
            label = "WALL-OUTER" if shell.index == 0 else "WALL-INNER"
            emit_islands(islands, layer.z, settings.print_speed, label)

        if layer.thin_walls:
            writer.add(";TYPE:THIN_WALL")
            writer.extrude_lines(layer.thin_walls,
                                 z=layer.z,
                                 speed=settings.print_speed,
                                 width=settings.extrusion_width)

        if layer.gap_fill:
            writer.add(";TYPE:GAP_FILL")
            writer.extrude_lines(layer.gap_fill,
                                 z=layer.z,
                                 speed=settings.print_speed,
                                 width=settings.extrusion_width)

        if layer.infill and layer.infill.lines:
            if layer.infill.is_solid:
                if layer.is_top:
                    label = "TOP"
                elif layer.is_bottom:
                    label = "BOTTOM"
                else:
                    label = "SOLID-INFILL"
            else:
                label = "INFILL"
            writer.add(f";TYPE:{label}")
            writer.extrude_lines(layer.infill.lines,
                                 z=layer.z,
                                 speed=settings.print_speed,
                                 width=settings.extrusion_width)

        if layer.bridge is not None:
            for region in layer.bridge.regions:
                writer.add(";TYPE:BRIDGE")
                writer.extrude_lines(region.lines,
                                     z=layer.z,
                                     speed=layer.bridge.speed,
                                     width=layer.bridge.extrusion_width)

        if layer.ironing is not None:
            writer.add(";TYPE:IRONING")
            writer.extrude_lines(layer.ironing.lines,
                                 z=layer.z,
                                 speed=layer.ironing.speed,
                                 width=settings.extrusion_width,
                                 multiplier=layer.ironing.flow)

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
