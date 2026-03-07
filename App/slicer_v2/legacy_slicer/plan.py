from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import math
from typing import Iterable, List, Optional, Sequence, Tuple

import numpy as np
import trimesh

from ..legacy_mesh import MeshModel
from ..legacy_geometry import (Island2D, LineSegment2D, Polygon2D, compensate_holes,
                        ensure_winding, gap_fill_lines, offset_islands,
                        thin_wall_lines)
from ..legacy_gcode_writer import SliceSettings
from .. import legacy_infill as infill_generator
from .. import legacy_support as support_generator
from .raft import BrimPlan, RaftLayer, SkirtPlan, build_brim_plan, build_raft_layers, build_skirt_plan
from .supports import BridgeInfill, IroningPass, build_bridge_infill, build_ironing_pass

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
    support: Optional[support_generator.SupportPlan] = None

def _wrap_islands(islands: List[Island2D]) -> List[IslandPerimeters]:
    return [IslandPerimeters(outer=outer, holes=holes) for outer, holes in islands]

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
    first_height = max(settings.min_layer_height,
                       min(settings.first_layer_height, settings.max_layer_height))
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
        is_first_layer = len(heights) == 0
        if is_first_layer:
            height = first_height
        else:
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

def _compute_layer_perimeters(mesh: MeshModel,
                              layer_index: int,
                              z_value: float,
                              settings: SliceSettings,
                              perimeter_count: int,
                              perimeter_spacing: float) -> LayerPerimeters:
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
    return LayerPerimeters(z=z_value, shells=shells)

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
        layers.append(_compute_layer_perimeters(mesh,
                                                 layer_index,
                                                 z_value,
                                                 settings,
                                                 perimeter_count,
                                                 perimeter_spacing))
    return layers

def generate_layer_perimeters_parallel(mesh: MeshModel,
                                       z_heights: Iterable[float],
                                       settings: Optional[SliceSettings] = None,
                                       perimeter_count: Optional[int] = None,
                                       perimeter_spacing: Optional[float] = None,
                                       max_workers: Optional[int] = None
                                       ) -> List[LayerPerimeters]:
    if settings is None:
        settings = SliceSettings()
    if perimeter_count is None:
        perimeter_count = settings.perimeter_count
    if perimeter_spacing is None:
        perimeter_spacing = settings.inner_wall_line_width
    perimeter_count = max(1, int(perimeter_count))

    z_list = [float(z) for z in z_heights]
    if not z_list:
        return []

    worker_count = int(max_workers or 0)
    if worker_count <= 1 or len(z_list) <= 1:
        return generate_layer_perimeters(mesh,
                                         z_list,
                                         settings=settings,
                                         perimeter_count=perimeter_count,
                                         perimeter_spacing=perimeter_spacing)

    worker_count = max(1, min(worker_count, len(z_list)))
    results: List[Optional[LayerPerimeters]] = [None for _ in z_list]
    with ThreadPoolExecutor(max_workers=worker_count) as pool:
        futures = {}
        for layer_index, z_value in enumerate(z_list):
            fut = pool.submit(_compute_layer_perimeters,
                              mesh,
                              layer_index,
                              z_value,
                              settings,
                              perimeter_count,
                              perimeter_spacing)
            futures[fut] = layer_index
        for fut, layer_index in futures.items():
            results[layer_index] = fut.result()
    return [layer for layer in results if layer is not None]

def _shells_to_islands(shell: PerimeterShell) -> List[Island2D]:
    return [(island.outer, island.holes) for island in shell.islands]

def _merge_layer_perimeters(layers_by_model: Sequence[List[LayerPerimeters]]
                            ) -> List[LayerPerimeters]:
    if not layers_by_model:
        return []
    layer_count = min(len(layers) for layers in layers_by_model)
    merged: List[LayerPerimeters] = []
    for idx in range(layer_count):
        z_value = layers_by_model[0][idx].z
        shells_map = {}
        for layers in layers_by_model:
            for shell in layers[idx].shells:
                existing = shells_map.get(shell.index)
                if existing is None:
                    shells_map[shell.index] = PerimeterShell(index=shell.index,
                                                            islands=list(shell.islands))
                else:
                    existing.islands.extend(shell.islands)
        shells = [shells_map[i] for i in sorted(shells_map.keys())]
        merged.append(LayerPerimeters(z=z_value, shells=shells))
    return merged

def _build_plan_from_layers(layers: List[LayerPerimeters],
                            settings: SliceSettings,
                            mesh: Optional[MeshModel] = None,
                            z_heights: Optional[Sequence[float]] = None
                            ) -> PrintPlan:
    if not layers:
        return PrintPlan(raft_layers=[],
                         brim=None,
                         skirt=None,
                         layers=[],
                         support=None)

    total_layers = len(layers)
    plans: List[LayerPlan] = []
    brim_plan: Optional[BrimPlan] = None
    skirt_plan: Optional[SkirtPlan] = None

    base_islands = _shells_to_islands(layers[0].shells[0]) if layers and layers[0].shells else []
    z_offset = settings.raft_layers * settings.layer_height
    raft_layers = build_raft_layers(base_islands, settings)
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
            bridge, has_overhang = build_bridge_infill(
                current_islands,
                below_islands,
                settings,
                is_top,
                index,
            )

        ironing = build_ironing_pass(
            islands,
            settings,
            index,
            total_layers,
            is_top,
            is_solid,
        )
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
        brim_plan = build_brim_plan(base_islands, first_layer.z + z_offset, settings)
        skirt_plan = build_skirt_plan(base_islands, first_layer.z + z_offset, settings)

    support_plan = None
    if settings.support_enabled and layers:
        if z_heights is None:
            z_heights = [layer.z for layer in layers]
        support_islands = [
            _shells_to_islands(layer.shells[0]) if layer.shells else []
            for layer in layers
        ]
        support_plan = support_generator.generate_support_plan(
            mesh,
            [z + z_offset for z in z_heights],
            settings,
            layer_islands=support_islands,
        )

    return PrintPlan(raft_layers=raft_layers,
                     brim=brim_plan,
                     skirt=skirt_plan,
                     layers=plans,
                     support=support_plan)

def generate_layer_plans(mesh: MeshModel,
                         z_heights: Optional[Iterable[float]] = None,
                         settings: Optional[SliceSettings] = None,
                         perimeter_count: Optional[int] = None,
                         perimeter_spacing: Optional[float] = None,
                         max_workers: Optional[int] = None
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
                         layers=[],
                         support=None)

    if max_workers and max_workers > 1:
        layers = generate_layer_perimeters_parallel(mesh,
                                                    z_heights,
                                                    settings=settings,
                                                    perimeter_count=perimeter_count,
                                                    perimeter_spacing=perimeter_spacing,
                                                    max_workers=max_workers)
    else:
        layers = generate_layer_perimeters(mesh,
                                           z_heights,
                                           settings=settings,
                                           perimeter_count=perimeter_count,
                                           perimeter_spacing=perimeter_spacing)

    return _build_plan_from_layers(layers, settings, mesh=mesh, z_heights=z_heights)


def generate_layer_plans_multi(models: Sequence[MeshModel],
                               z_heights: Optional[Iterable[float]] = None,
                               settings: Optional[SliceSettings] = None,
                               perimeter_count: Optional[int] = None,
                               perimeter_spacing: Optional[float] = None,
                               max_workers: Optional[int] = None
                               ) -> PrintPlan:
    if settings is None:
        settings = SliceSettings()
    if not models:
        return PrintPlan(raft_layers=[],
                         brim=None,
                         skirt=None,
                         layers=[],
                         support=None)
    if z_heights is None:
        combined = trimesh.util.concatenate([m.mesh for m in models])
        reference = MeshModel(path="<combined>", mesh=combined)
        z_heights = build_z_heights(reference, settings)
    z_heights = list(z_heights)
    if not z_heights:
        return PrintPlan(raft_layers=[],
                         brim=None,
                         skirt=None,
                         layers=[],
                         support=None)

    if perimeter_count is None:
        perimeter_count = settings.perimeter_count
    if perimeter_spacing is None:
        perimeter_spacing = settings.inner_wall_line_width
    perimeter_count = max(1, int(perimeter_count))

    worker_count = int(max_workers or 0)
    if worker_count > 1 and len(models) > 1:
        worker_count = max(1, min(worker_count, len(models)))
        layers_by_model: List[Optional[List[LayerPerimeters]]] = [None for _ in models]
        with ThreadPoolExecutor(max_workers=worker_count) as pool:
            futures = {}
            for idx, model in enumerate(models):
                fut = pool.submit(generate_layer_perimeters,
                                  model,
                                  z_heights,
                                  settings=settings,
                                  perimeter_count=perimeter_count,
                                  perimeter_spacing=perimeter_spacing)
                futures[fut] = idx
            for fut, idx in futures.items():
                layers_by_model[idx] = fut.result()
    else:
        layers_by_model = [
            generate_layer_perimeters(model,
                                      z_heights,
                                      settings=settings,
                                      perimeter_count=perimeter_count,
                                      perimeter_spacing=perimeter_spacing)
            for model in models
        ]

    merged_layers = _merge_layer_perimeters([layers for layers in layers_by_model if layers is not None])
    combined_mesh = None
    if models:
        combined_mesh = MeshModel.from_trimesh(
            trimesh.util.concatenate([m.mesh for m in models]),
            path="<combined>",
        )
    return _build_plan_from_layers(merged_layers,
                                   settings,
                                   mesh=combined_mesh,
                                   z_heights=z_heights)


