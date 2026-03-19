from __future__ import annotations

from dataclasses import dataclass
import math
from typing import List, Optional, Sequence, Tuple

from ..legacy_geometry import Island2D, LineSegment2D, ensure_winding
from .. import legacy_infill as infill_generator
from .. import legacy_path_planner as path_planner
from ..legacy_gcode_writer import SliceSettings


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


def _polygon_area(points: Sequence[Tuple[float, float]]) -> float:
    if not points or len(points) < 3:
        return 0.0
    area = 0.0
    for idx in range(len(points)):
        x1, y1 = points[idx]
        x2, y2 = points[(idx + 1) % len(points)]
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


def build_bridge_infill(current_islands: Sequence[Island2D],
                        below_islands: Sequence[Island2D],
                        settings: SliceSettings,
                        is_top: bool,
                        layer_index: int) -> Tuple[Optional[BridgeInfill], bool]:
    bridge = None
    has_overhang = False
    if not current_islands or not below_islands:
        return bridge, has_overhang

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
        filtered = [island for island in bridge_islands if _island_area(island) >= min_area]

    regions: List[path_planner.BridgeRegion] = []
    if filtered and settings.bridge_density > 0.0:
        density = max(0.0, min(1.0, settings.bridge_density / 100.0))
        bridge_width = settings.bridge_extrusion_width
        if is_top and settings.thick_bridges:
            bridge_width *= 1.2
        elif (not is_top) and settings.thick_internal_bridges:
            bridge_width *= 1.2
        regions = path_planner.generate_bridge_infill(
            filtered,
            layer_index=layer_index,
            extrusion_width=bridge_width,
            density=density,
        )
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
                    layer_index=layer_index,
                    extrusion_width=bridge_width,
                    density=hole_density,
                ))
        if regions:
            flow_ratio = (settings.bridge_flow_ratio if is_top
                          else settings.internal_bridge_flow_ratio)
            bridge = BridgeInfill(
                regions=regions,
                speed=settings.bridge_speed,
                extrusion_width=bridge_width,
                flow_ratio=flow_ratio,
            )

    return bridge, has_overhang


def build_ironing_pass(islands: Sequence[Island2D],
                        settings: SliceSettings,
                        layer_index: int,
                        total_layers: int,
                        is_top: bool,
                        is_solid: bool) -> Optional[IroningPass]:
    ironing_mode = settings.ironing_type
    ironing_enabled = False
    if ironing_mode == "all_solid_layers":
        ironing_enabled = is_solid
    elif ironing_mode == "topmost_surface_only":
        ironing_enabled = is_top and layer_index == total_layers - 1
    elif ironing_mode == "all_top_surfaces":
        ironing_enabled = is_top and is_solid

    if not ironing_enabled or not islands:
        return None

    ironing_lines = infill_generator.rectilinear_infill(
        islands,
        density=1.0,
        angle_deg=settings.infill_angle,
        layer_index=layer_index,
        extrusion_width=settings.extrusion_width,
        alternate=False,
    )
    if not ironing_lines:
        return None

    return IroningPass(
        lines=ironing_lines,
        speed=settings.ironing_speed,
        flow=settings.ironing_flow,
    )

