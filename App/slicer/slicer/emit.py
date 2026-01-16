from __future__ import annotations

import math
import random
from pathlib import Path
from typing import List, Optional, Sequence, Tuple, cast

from ..geometry import Island2D, LineSegment2D, Polygon2D, ensure_winding, point_in_island
from ..gcode.writer import GCodeWriter, SliceSettings
from .. import path_planner
from ..mesh import MeshModel
from .plan import PrintPlan, _shells_to_islands, generate_layer_plans


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
