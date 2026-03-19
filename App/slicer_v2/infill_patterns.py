from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from math import ceil, cos, radians, sin
from typing import Sequence

from .errors import SlicerV2InfillPatternError
from .geometry import EPSILON, Island, Point2
from .island_graph import LayerIslandGraph
from .infill_rotation import calculate_infill_rotation_angles
from .line_split import split_line


INFILL_PATTERN_RECTILINEAR = "rectilinear"
INFILL_PATTERN_GRID = "grid"
INFILL_PATTERN_GYROID = "gyroid"
INFILL_PATTERN_TRIANGLE = "triangle"
INFILL_PATTERN_ADAPTIVE_CUBIC = "adaptive_cubic"
INFILL_PATTERN_SUPPORT_CUBIC = "support_cubic"
INFILL_PATTERN_LIGHTNING = "lightning"
INFILL_PATTERN_CONCENTRIC = "concentric"
INFILL_PATTERN_HONEYCOMB = "honeycomb"
INFILL_PATTERN_3D_HONEYCOMB = "3d_honeycomb"
INFILL_PATTERN_CROSS_HATCH = "cross_hatch"
INFILL_PATTERN_TPMS_D = "tpms_d"
INFILL_PATTERN_TPMS_F_K = "tpms_f_k"
ALLOWED_INFILL_PATTERNS = {
    INFILL_PATTERN_RECTILINEAR,
    INFILL_PATTERN_GRID,
    INFILL_PATTERN_GYROID,
    INFILL_PATTERN_TRIANGLE,
    INFILL_PATTERN_ADAPTIVE_CUBIC,
    INFILL_PATTERN_SUPPORT_CUBIC,
    INFILL_PATTERN_LIGHTNING,
    INFILL_PATTERN_CONCENTRIC,
    INFILL_PATTERN_HONEYCOMB,
    INFILL_PATTERN_3D_HONEYCOMB,
    INFILL_PATTERN_CROSS_HATCH,
    INFILL_PATTERN_TPMS_D,
    INFILL_PATTERN_TPMS_F_K,
}


@dataclass
class InfillPathPlan:
    layer_index: int
    island_index: int
    pattern: str
    pass_index: int
    angle_deg: float
    line_count: int
    path_count: int
    path_length_mm: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class LayerInfillPlan:
    layer_index: int
    z_height_mm: float
    pattern: str
    density_ratio: float
    angle_deg: float
    anchor_angle_deg: float
    combined_layer_count: int
    combined_thickness_layers: int
    is_void_layer: bool
    combined_into_layer_index: int | None
    void_depth_layers: int
    support_surface_ratio: float
    island_area_mm2: float
    effective_infill_area_mm2: float
    path_count: int
    path_length_mm: float
    combine_target_layer_index: int | None = None
    combine_thickness_layers: int = 1
    combine_void_depth_layers: int = 1
    combine_effective_area_mm2: float = 0.0
    paths: list[InfillPathPlan] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class InfillPatternsReport:
    generated_at_utc: str
    layer_count: int
    island_count_total: int
    pattern: str
    infill_percent: float
    density_ratio: float
    path_count_total: int
    path_length_mm_total: float
    void_layer_count: int
    support_surface_ratio_avg: float
    warning_count: int
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _validate_pattern(pattern: str) -> str:
    normalized = str(pattern).strip().lower()
    if normalized not in ALLOWED_INFILL_PATTERNS:
        raise SlicerV2InfillPatternError(f"INFILL_PATTERN_UNSUPPORTED:{pattern}")
    return normalized


def _validate_infill_percent(infill_percent: float) -> float:
    percent = float(infill_percent)
    if percent < 0.0:
        raise SlicerV2InfillPatternError("INFILL_PERCENT_NEGATIVE")
    if percent > 100.0:
        raise SlicerV2InfillPatternError("INFILL_PERCENT_EXCESSIVE")
    return percent


def _validate_extrusion_width(extrusion_width_mm: float) -> float:
    width = float(extrusion_width_mm)
    if width <= EPSILON:
        raise SlicerV2InfillPatternError("INFILL_EXTRUSION_WIDTH_INVALID")
    return width


def _validate_layer_graphs(layer_graphs: Sequence[LayerIslandGraph]) -> list[LayerIslandGraph]:
    graphs = list(layer_graphs)
    for index, graph in enumerate(graphs):
        if not isinstance(graph, LayerIslandGraph):
            raise SlicerV2InfillPatternError(f"INFILL_LAYER_GRAPH_INVALID:{index}")
    return graphs


def _normalize_angle(value: float) -> float:
    angle = float(value)
    while angle < 0.0:
        angle += 360.0
    while angle >= 360.0:
        angle -= 360.0
    return angle


def _line_spacing(extrusion_width_mm: float, density_ratio: float) -> float:
    if density_ratio <= EPSILON:
        return 10_000.0
    # Higher density means tighter spacing.
    base_spacing = extrusion_width_mm / max(density_ratio, 0.01)
    return max(extrusion_width_mm * 0.75, base_spacing)


def _passes_and_length_factor(pattern: str) -> tuple[int, float]:
    if pattern == INFILL_PATTERN_RECTILINEAR:
        return 1, 1.0
    if pattern == INFILL_PATTERN_GRID:
        return 2, 1.0
    if pattern == INFILL_PATTERN_GYROID:
        return 2, 1.25
    if pattern == INFILL_PATTERN_TRIANGLE:
        return 3, 1.0
    if pattern == INFILL_PATTERN_ADAPTIVE_CUBIC:
        return 3, 1.35
    if pattern == INFILL_PATTERN_SUPPORT_CUBIC:
        return 2, 1.15
    if pattern == INFILL_PATTERN_LIGHTNING:
        return 1, 0.7
    if pattern == INFILL_PATTERN_CONCENTRIC:
        return 1, 0.95
    if pattern == INFILL_PATTERN_HONEYCOMB:
        return 3, 1.25
    if pattern == INFILL_PATTERN_3D_HONEYCOMB:
        return 3, 1.35
    if pattern == INFILL_PATTERN_CROSS_HATCH:
        return 2, 1.1
    if pattern == INFILL_PATTERN_TPMS_D:
        return 2, 1.45
    if pattern == INFILL_PATTERN_TPMS_F_K:
        return 2, 1.5
    raise SlicerV2InfillPatternError(f"INFILL_PATTERN_UNSUPPORTED:{pattern}")


def _pattern_pass_angle(pattern: str, *, layer_angle_deg: float, pass_index: int, layer_index: int) -> float:
    base = float(layer_angle_deg)
    if pattern in {INFILL_PATTERN_RECTILINEAR, INFILL_PATTERN_CONCENTRIC, INFILL_PATTERN_LIGHTNING}:
        return _normalize_angle(base)
    if pattern in {INFILL_PATTERN_GRID, INFILL_PATTERN_GYROID, INFILL_PATTERN_SUPPORT_CUBIC}:
        return _normalize_angle(base + (pass_index * 90.0))
    if pattern in {INFILL_PATTERN_TRIANGLE, INFILL_PATTERN_HONEYCOMB}:
        return _normalize_angle(base + (pass_index * 60.0))
    if pattern == INFILL_PATTERN_3D_HONEYCOMB:
        return _normalize_angle(base + (pass_index * 60.0) + (layer_index * 15.0))
    if pattern == INFILL_PATTERN_CROSS_HATCH:
        return _normalize_angle(base + (pass_index * 45.0))
    if pattern == INFILL_PATTERN_ADAPTIVE_CUBIC:
        return _normalize_angle(base + (pass_index * 60.0) + ((layer_index % 2) * 15.0))
    if pattern == INFILL_PATTERN_TPMS_D:
        return _normalize_angle(base + (pass_index * 90.0) + ((layer_index % 3) * 12.0))
    if pattern == INFILL_PATTERN_TPMS_F_K:
        return _normalize_angle(base + (pass_index * 90.0) + ((layer_index % 4) * 10.0))
    return _normalize_angle(base + (pass_index * 90.0))


def _pattern_spacing_scale(pattern: str, layer_index: int) -> float:
    if pattern == INFILL_PATTERN_LIGHTNING:
        return 1.5
    if pattern == INFILL_PATTERN_CONCENTRIC:
        return 0.9
    if pattern == INFILL_PATTERN_HONEYCOMB:
        return 1.15
    if pattern == INFILL_PATTERN_3D_HONEYCOMB:
        return 1.2 + ((layer_index % 2) * 0.05)
    if pattern == INFILL_PATTERN_CROSS_HATCH:
        return 1.1
    if pattern == INFILL_PATTERN_TPMS_D:
        return 1.25
    if pattern == INFILL_PATTERN_TPMS_F_K:
        return 1.3
    return 1.0


def _pattern_segment_scale(pattern: str) -> float:
    if pattern == INFILL_PATTERN_GYROID:
        return 1.2
    if pattern == INFILL_PATTERN_LIGHTNING:
        return 0.65
    if pattern == INFILL_PATTERN_CONCENTRIC:
        return 0.85
    if pattern == INFILL_PATTERN_HONEYCOMB:
        return 1.15
    if pattern == INFILL_PATTERN_3D_HONEYCOMB:
        return 1.2
    if pattern == INFILL_PATTERN_CROSS_HATCH:
        return 1.05
    if pattern == INFILL_PATTERN_TPMS_D:
        return 1.25
    if pattern == INFILL_PATTERN_TPMS_F_K:
        return 1.3
    return 1.0


def _resolve_anchor_length(value: object, spacing_mm: float, default_mm: float) -> float:
    if isinstance(value, bool):
        return float(default_mm)
    if isinstance(value, (int, float)):
        return max(0.0, float(value))
    text = str(value).strip()
    if not text:
        return float(default_mm)
    if text.endswith("%"):
        try:
            pct = float(text[:-1].strip())
        except (TypeError, ValueError, OverflowError):
            return float(default_mm)
        return max(0.0, float(spacing_mm * pct * 0.01))
    try:
        return max(0.0, float(text))
    except (TypeError, ValueError, OverflowError):
        return float(default_mm)


def _layer_thickness_mm(graphs: Sequence[LayerIslandGraph], index: int, fallback: float) -> float:
    if not graphs:
        return float(fallback)
    if index > 0:
        dz = float(graphs[index].z_height_mm) - float(graphs[index - 1].z_height_mm)
        if dz > EPSILON:
            return dz
    if index + 1 < len(graphs):
        dz = float(graphs[index + 1].z_height_mm) - float(graphs[index].z_height_mm)
        if dz > EPSILON:
            return dz
    return float(fallback)


def _layer_island_area_mm2(layer_graph: LayerIslandGraph) -> float:
    return float(sum(max(0.0, float(island.area)) for island in layer_graph.islands))


def _layer_support_surface_ratio(
    *,
    is_void_layer: bool,
    density_ratio: float,
    combine_infill_enabled: bool,
    combined_thickness_layers: int,
) -> float:
    if is_void_layer:
        return 0.0
    if density_ratio <= EPSILON:
        return 0.0

    ratio = 1.0
    thickness = max(1, int(combined_thickness_layers))
    if combine_infill_enabled and thickness > 1:
        ratio = 1.0 / float(thickness)
    return max(0.0, min(1.0, float(ratio)))


def _scanline_segment_lengths(island: Island, angle_deg: float, spacing_mm: float) -> tuple[int, list[float]]:
    step = max(float(spacing_mm), EPSILON)
    angle_rad = radians(_normalize_angle(angle_deg))
    dir_x = cos(angle_rad)
    dir_y = sin(angle_rad)
    norm_x = -dir_y
    norm_y = dir_x

    points = list(island.outer.points)
    if not points:
        return 0, []

    proj_t = [point.x * dir_x + point.y * dir_y for point in points]
    proj_s = [point.x * norm_x + point.y * norm_y for point in points]
    min_t = min(proj_t)
    max_t = max(proj_t)
    min_s = min(proj_s)
    max_s = max(proj_s)
    span_s = max_s - min_s
    if span_s <= EPSILON:
        return 0, []

    margin = max(0.5, step * 1.5)
    line_count = max(1, int(ceil(span_s / step)))
    line_lengths: list[float] = []
    for line_index in range(line_count):
        s = min_s + ((line_index + 0.5) * step)
        if s > max_s + step:
            break
        start = Point2((dir_x * (min_t - margin)) + (norm_x * s), (dir_y * (min_t - margin)) + (norm_y * s))
        end = Point2((dir_x * (max_t + margin)) + (norm_x * s), (dir_y * (max_t + margin)) + (norm_y * s))
        split = split_line((start, end), [island], closed=False)
        if len(split) < 2:
            continue
        line_length = 0.0
        for idx in range(len(split) - 1):
            a = split[idx]
            b = split[idx + 1]
            if not a.clipped:
                continue
            seg_len = a.p.distance_to(b.p)
            if seg_len > EPSILON:
                line_length += seg_len
        if line_length > EPSILON:
            line_lengths.append(float(line_length))
    return line_count, line_lengths


def _apply_antivibration_filter(
    line_lengths: Sequence[float],
    *,
    enabled: bool,
    short_line_threshold_mm: float,
    max_skips_allowed: int,
    min_depth_for_line_removing: int,
) -> list[float]:
    lengths = [max(0.0, float(length)) for length in line_lengths if float(length) > EPSILON]
    if not enabled:
        return lengths
    if len(lengths) < max(1, int(min_depth_for_line_removing)):
        return lengths

    threshold = max(0.1, float(short_line_threshold_mm))
    max_skips = max(0, int(max_skips_allowed))
    kept: list[float] = []
    for index, length in enumerate(lengths):
        if length >= threshold:
            kept.append(length)
            continue
        left_start = max(0, index - max_skips - 1)
        right_end = min(len(lengths), index + max_skips + 2)
        has_left_long = any(value >= threshold for value in lengths[left_start:index])
        has_right_long = any(value >= threshold for value in lengths[index + 1 : right_end])
        if has_left_long and has_right_long:
            kept.append(length)
    return kept


def _combined_top_layer_indices(
    graphs: Sequence[LayerIslandGraph],
    *,
    enabled: bool,
    max_layer_height_mm: float,
    fallback_layer_height_mm: float,
) -> tuple[set[int], dict[int, int], dict[int, int], dict[int, int]]:
    if not graphs:
        return set(), {}, {}, {}
    if not enabled:
        layer_indices = [int(graph.layer_index) for graph in graphs]
        single = {layer_index: 1 for layer_index in layer_indices}
        combined_into = {layer_index: layer_index for layer_index in layer_indices}
        return set(layer_indices), single, combined_into, dict(single)

    target_height = float(max_layer_height_mm)
    if target_height <= EPSILON:
        target_height = max(float(fallback_layer_height_mm), 0.2)

    layer_indices = [int(graph.layer_index) for graph in graphs]
    active: set[int] = set()
    groups: dict[int, int] = {}
    combined_into: dict[int, int] = {}
    thickness_layers: dict[int, int] = {}

    first_layer = int(layer_indices[0])
    active.add(first_layer)
    groups[first_layer] = 1
    combined_into[first_layer] = first_layer
    thickness_layers[first_layer] = 1
    if len(graphs) == 1:
        return active, groups, combined_into, thickness_layers

    def _finalize_group(group: Sequence[int]) -> None:
        if not group:
            return
        top = int(group[-1])
        group_size = max(1, len(group))
        active.add(top)
        groups[top] = group_size
        for layer_id in group:
            layer_key = int(layer_id)
            combined_into[layer_key] = top
            thickness_layers[layer_key] = group_size

    current_group: list[int] = []
    current_height = 0.0
    for idx in range(1, len(graphs)):
        lid = layer_indices[idx]
        thickness = _layer_thickness_mm(graphs, idx, fallback_layer_height_mm)
        if current_group and (current_height + thickness > target_height + EPSILON):
            _finalize_group(current_group)
            current_group = [lid]
            current_height = thickness
        else:
            current_group.append(lid)
            current_height += thickness

    _finalize_group(current_group)
    for layer_index in layer_indices:
        if layer_index not in combined_into:
            combined_into[layer_index] = layer_index
        if layer_index not in thickness_layers:
            thickness_layers[layer_index] = 1
    return active, groups, combined_into, thickness_layers


def build_infill_patterns(
    layer_graphs: Sequence[LayerIslandGraph],
    *,
    infill_pattern: str,
    infill_percent: float,
    extrusion_width_mm: float,
    angle_start_deg: float = 45.0,
    angle_step_deg: float = 90.0,
    angle_template: str = "",
    infill_anchor: object = 0.0,
    infill_anchor_max: object = 1000.0,
    combine_infill_enabled: bool = False,
    combine_max_layer_height_mm: float = 0.0,
    layer_height_mm: float = 0.2,
    bottom_shell_layers: int = 0,
    top_shell_layers: int = 0,
    random_seed: int = 0,
    anti_vibration_enabled: bool = True,
    anti_vibration_short_line_threshold_mm: float = 4.0,
    anti_vibration_max_skips_allowed: int = 2,
    anti_vibration_min_depth_for_line_removing: int = 5,
    max_workers: int = 1,
) -> tuple[list[LayerInfillPlan], InfillPatternsReport]:
    pattern = _validate_pattern(infill_pattern)
    percent = _validate_infill_percent(infill_percent)
    width = _validate_extrusion_width(extrusion_width_mm)
    graphs = _validate_layer_graphs(layer_graphs)

    density_ratio = percent / 100.0
    spacing = _line_spacing(width, density_ratio)

    warnings: list[str] = []

    pattern_for_generation = pattern
    if pattern == INFILL_PATTERN_TRIANGLE:
        pattern_for_generation = INFILL_PATTERN_GRID
        warnings.append("infill_pattern:triangle_delegated_to_grid")

    passes, length_factor = _passes_and_length_factor(pattern)
    active_layers, combined_layer_counts, combined_into_layers, combined_thickness_layers = _combined_top_layer_indices(
        graphs,
        enabled=bool(combine_infill_enabled),
        max_layer_height_mm=float(combine_max_layer_height_mm),
        fallback_layer_height_mm=max(float(layer_height_mm), EPSILON),
    )
    if combine_infill_enabled:
        warnings.append("infill_combination:enabled")

    normalized_template = str(angle_template or "").strip()
    template_angles: list[float] | None = None
    if normalized_template:
        max_layer_index = -1
        for graph in graphs:
            max_layer_index = max(max_layer_index, int(graph.layer_index))
        computed_layer_count = max(0, max_layer_index + 1)
        template_angles = calculate_infill_rotation_angles(
            layer_count=max(1, computed_layer_count),
            fixed_infill_angle_deg=angle_start_deg,
            template_string=normalized_template,
            layer_height_mm=layer_height_mm,
            bottom_shell_layers=bottom_shell_layers,
            top_shell_layers=top_shell_layers,
            seed=random_seed,
        )

    def _build_layer(layer_graph: LayerIslandGraph) -> tuple[LayerInfillPlan, list[str], int]:
        layer_warnings: list[str] = []
        layer_index = int(layer_graph.layer_index)
        island_area_mm2 = _layer_island_area_mm2(layer_graph)
        combined_into = int(combined_into_layers.get(layer_index, layer_index))
        thickness_layers = max(
            1,
            int(
                combined_thickness_layers.get(
                    layer_index,
                    combined_layer_counts.get(layer_index, 1),
                )
            ),
        )
        is_void_layer = bool(
            combine_infill_enabled and layer_index not in active_layers and combined_into != layer_index
        )
        if template_angles is not None and layer_index >= 0 and layer_index < len(template_angles):
            layer_angle = _normalize_angle(template_angles[layer_index])
        else:
            layer_angle = _normalize_angle(angle_start_deg + (layer_index * angle_step_deg))
        paths: list[InfillPathPlan] = []
        combined_count = max(1, int(combined_layer_counts.get(layer_index, thickness_layers)))

        if is_void_layer:
            layer_warnings.append(f"layer_{layer_index}:infill_combined_into_upper_layer")
            void_depth_layers = max(1, int(combined_into - layer_index))
            return (
                LayerInfillPlan(
                    layer_index=layer_graph.layer_index,
                    z_height_mm=float(layer_graph.z_height_mm),
                    pattern=pattern,
                    density_ratio=density_ratio,
                    angle_deg=layer_angle,
                    anchor_angle_deg=layer_angle,
                    combined_layer_count=0,
                    combined_thickness_layers=thickness_layers,
                    is_void_layer=True,
                    combined_into_layer_index=combined_into,
                    void_depth_layers=void_depth_layers,
                    support_surface_ratio=0.0,
                    island_area_mm2=island_area_mm2,
                    effective_infill_area_mm2=0.0,
                    path_count=0,
                    path_length_mm=0.0,
                    combine_target_layer_index=combined_into,
                    combine_thickness_layers=thickness_layers,
                    combine_void_depth_layers=void_depth_layers,
                    combine_effective_area_mm2=0.0,
                    paths=[],
                ),
                layer_warnings,
                int(layer_graph.island_count),
            )

        if density_ratio > EPSILON:
            pattern_segment_scale = _pattern_segment_scale(pattern_for_generation)
            anti_vibration_enabled_for_layer = bool(
                anti_vibration_enabled
                and pattern_for_generation
                in {
                    INFILL_PATTERN_RECTILINEAR,
                    INFILL_PATTERN_GRID,
                    INFILL_PATTERN_TRIANGLE,
                    INFILL_PATTERN_CROSS_HATCH,
                    INFILL_PATTERN_SUPPORT_CUBIC,
                    INFILL_PATTERN_ADAPTIVE_CUBIC,
                }
            )
            for island_index, island in enumerate(layer_graph.islands):
                span_major = max(float(island.bounds.width), float(island.bounds.height))
                span_minor = min(float(island.bounds.width), float(island.bounds.height))
                if span_major <= EPSILON or span_minor <= EPSILON:
                    layer_warnings.append(f"layer_{layer_graph.layer_index}:island_{island_index}:degenerate_bounds")
                    continue

                island_spacing = spacing * _pattern_spacing_scale(pattern_for_generation, layer_index)
                line_count = max(1, int(ceil(span_minor / max(island_spacing, EPSILON))))
                for pass_index in range(passes):
                    pass_angle = _pattern_pass_angle(
                        pattern_for_generation,
                        layer_angle_deg=layer_angle,
                        pass_index=pass_index,
                        layer_index=layer_index,
                    )
                    scan_lines, line_lengths = _scanline_segment_lengths(island, pass_angle, island_spacing)
                    filtered_lengths = _apply_antivibration_filter(
                        line_lengths,
                        enabled=anti_vibration_enabled_for_layer,
                        short_line_threshold_mm=anti_vibration_short_line_threshold_mm,
                        max_skips_allowed=anti_vibration_max_skips_allowed,
                        min_depth_for_line_removing=anti_vibration_min_depth_for_line_removing,
                    )
                    pass_path_count = len(filtered_lengths)
                    if pass_path_count <= 0:
                        continue

                    pass_length = float(sum(filtered_lengths)) * length_factor * max(0.2, pattern_segment_scale)
                    anchor_length = _resolve_anchor_length(infill_anchor, island_spacing, 0.0)
                    anchor_max = _resolve_anchor_length(infill_anchor_max, island_spacing, 1000.0)
                    if anchor_max > EPSILON and anchor_length > EPSILON:
                        anchor_effective = min(anchor_length, anchor_max, span_minor * 0.5)
                        pass_length += float(pass_path_count * anchor_effective * 0.35)
                    paths.append(
                        InfillPathPlan(
                            layer_index=layer_graph.layer_index,
                            island_index=island_index,
                            pattern=pattern,
                            pass_index=pass_index,
                            angle_deg=pass_angle,
                            line_count=max(line_count, scan_lines),
                            path_count=pass_path_count,
                            path_length_mm=pass_length,
                        )
                    )

        layer_path_count = sum(path.path_count for path in paths)
        layer_path_length = float(sum(path.path_length_mm for path in paths))
        void_depth_layers = 1
        if combine_infill_enabled and thickness_layers > 1:
            void_depth_layers = max(1, thickness_layers - 1)
        layer_support_surface_ratio = _layer_support_surface_ratio(
            is_void_layer=False,
            density_ratio=density_ratio,
            combine_infill_enabled=bool(combine_infill_enabled),
            combined_thickness_layers=thickness_layers,
        )
        if layer_path_count <= 0:
            layer_support_surface_ratio = 0.0
        effective_infill_area_mm2 = float(island_area_mm2 * layer_support_surface_ratio)
        layer_anchor_angle = layer_angle
        if paths:
            angle_weights: dict[float, float] = {}
            for path in paths:
                key = _normalize_angle(path.angle_deg)
                angle_weights[key] = angle_weights.get(key, 0.0) + max(path.path_length_mm, 0.0)
            if angle_weights:
                layer_anchor_angle = max(angle_weights.items(), key=lambda item: item[1])[0]

        return (
            LayerInfillPlan(
                layer_index=layer_graph.layer_index,
                z_height_mm=float(layer_graph.z_height_mm),
                pattern=pattern,
                density_ratio=density_ratio,
                angle_deg=layer_angle,
                anchor_angle_deg=layer_anchor_angle,
                combined_layer_count=combined_count,
                combined_thickness_layers=thickness_layers,
                is_void_layer=False,
                combined_into_layer_index=combined_into,
                void_depth_layers=void_depth_layers,
                support_surface_ratio=layer_support_surface_ratio,
                island_area_mm2=island_area_mm2,
                effective_infill_area_mm2=effective_infill_area_mm2,
                path_count=layer_path_count,
                path_length_mm=layer_path_length,
                combine_target_layer_index=combined_into,
                combine_thickness_layers=thickness_layers,
                combine_void_depth_layers=void_depth_layers,
                combine_effective_area_mm2=effective_infill_area_mm2,
                paths=paths,
            ),
            layer_warnings,
            int(layer_graph.island_count),
        )

    worker_count = max(1, min(int(max_workers), len(graphs) if graphs else 1))
    if worker_count > 1 and len(graphs) > 1:
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            results = list(executor.map(_build_layer, graphs))
    else:
        results = [_build_layer(layer_graph) for layer_graph in graphs]

    layer_plans: list[LayerInfillPlan] = []
    island_count_total = 0
    path_count_total = 0
    path_length_mm_total = 0.0
    void_layer_count = 0
    support_surface_ratio_area_sum = 0.0
    support_surface_area_weight_total = 0.0
    for layer_plan, layer_warnings, island_count in results:
        layer_plans.append(layer_plan)
        warnings.extend(layer_warnings)
        island_count_total += island_count
        path_count_total += layer_plan.path_count
        path_length_mm_total += layer_plan.path_length_mm
        if layer_plan.is_void_layer:
            void_layer_count += 1
        support_surface_ratio_area_sum += float(layer_plan.support_surface_ratio) * float(layer_plan.island_area_mm2)
        support_surface_area_weight_total += float(layer_plan.island_area_mm2)

    layer_plans.sort(key=lambda plan: int(plan.layer_index))

    report = InfillPatternsReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        layer_count=len(layer_plans),
        island_count_total=island_count_total,
        pattern=pattern,
        infill_percent=percent,
        density_ratio=density_ratio,
        path_count_total=path_count_total,
        path_length_mm_total=path_length_mm_total,
        void_layer_count=void_layer_count,
        support_surface_ratio_avg=(
            float(support_surface_ratio_area_sum / support_surface_area_weight_total)
            if support_surface_area_weight_total > EPSILON
            else 0.0
        ),
        warning_count=len(warnings),
        warnings=warnings,
    )
    return layer_plans, report
