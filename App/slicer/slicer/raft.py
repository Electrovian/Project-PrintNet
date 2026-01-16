from __future__ import annotations

from dataclasses import dataclass
import math
from typing import List, Optional, Sequence

from ..geometry import Island2D, LineSegment2D, Polygon2D, offset_islands
from .. import infill as infill_generator
from ..gcode.writer import SliceSettings


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


def build_raft_layers(base_islands: Sequence[Island2D],
                      settings: SliceSettings) -> List[RaftLayer]:
    if settings.raft_layers <= 0 or not base_islands:
        return []
    raft_islands = offset_islands(list(base_islands), settings.raft_margin)
    if not raft_islands:
        return []

    layers: List[RaftLayer] = []
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
        layers.append(RaftLayer(z=z, lines=lines, angle=angle))
    return layers


def build_brim_plan(base_islands: Sequence[Island2D],
                    z: float,
                    settings: SliceSettings) -> Optional[BrimPlan]:
    if settings.brim_width <= 0.0 or not base_islands:
        return None
    count = int(math.ceil(settings.brim_width / settings.extrusion_width))
    loops: List[Polygon2D] = []
    current = list(base_islands)
    for _ in range(count):
        current = offset_islands(current, settings.extrusion_width)
        for outer, _holes in current:
            loops.append(outer)
    if not loops:
        return None
    return BrimPlan(loops=loops, z=z)


def build_skirt_plan(base_islands: Sequence[Island2D],
                     z: float,
                     settings: SliceSettings) -> Optional[SkirtPlan]:
    if settings.skirt_loops <= 0 or not base_islands:
        return None
    loops: List[Polygon2D] = []
    current = offset_islands(list(base_islands), settings.skirt_distance)
    for _ in range(settings.skirt_loops):
        if not current:
            break
        for outer, _holes in current:
            loops.append(outer)
        current = offset_islands(current, settings.extrusion_width)
    if not loops:
        return None
    return SkirtPlan(loops=loops, z=z)
