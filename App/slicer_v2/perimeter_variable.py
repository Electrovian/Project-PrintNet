from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from math import acos, degrees, hypot
from typing import Sequence

from .errors import SlicerV2PerimeterVariableError
from .geometry import EPSILON, Point2, Polygon
from .island_graph import LayerIslandGraph
from .perimeter_classic import (
    WALL_SEQUENCE_INNER_TO_OUTER,
    WALL_SEQUENCE_OUTER_TO_INNER,
    _shell_indices,
)


PERIMETER_MODE_VARIABLE_WIDTH = "variable_width"


@dataclass
class VariableWidthLoopPlan:
    layer_index: int
    island_index: int
    role: str
    shell_index: int
    width_mm: float
    width_start_mm: float
    width_end_mm: float
    point_count: int
    path_length_mm: float
    transition_length_mm: float
    half_edge_count: int
    half_edge_width_min_mm: float
    half_edge_width_max_mm: float
    half_edge_redistribution_mm: float
    junction_carryover_ratio: float
    junction_count: int
    junction_compensation_ratio: float
    points: tuple[Point2, ...] = field(default_factory=tuple)
    carryover_source_layer_index: int | None = None
    carryover_source_island_index: int | None = None
    carryover_strength: float = 0.0
    half_edge_redistribution_ratio: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class VariableWidthTransitionPlan:
    layer_index: int
    island_index: int
    from_shell_index: int
    to_shell_index: int
    width_start_mm: float
    width_end_mm: float
    transition_length_mm: float
    junction_count: int
    carryover_continuity_ratio: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class HalfEdgeBeadPlan:
    layer_index: int
    island_index: int
    role: str
    shell_index: int
    edge_index: int
    edge_length_mm: float
    base_width_mm: float
    width_mm: float
    sharpness_ratio: float

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass
class LayerVariableWidthPlan:
    layer_index: int
    z_height_mm: float
    loop_count: int
    path_length_mm: float
    min_width_mm: float
    max_width_mm: float
    transition_count: int
    transition_length_mm: float
    junction_count: int
    half_edge_bead_count: int
    half_edge_redistribution_mm: float
    junction_carryover_event_count: int
    junction_carryover_ratio_avg: float
    junction_carryover_cross_island_event_count: int = 0
    junction_carryover_source_island_count: int = 0
    loops: list[VariableWidthLoopPlan] = field(default_factory=list)
    transitions: list[VariableWidthTransitionPlan] = field(default_factory=list)
    half_edge_beads: list[HalfEdgeBeadPlan] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["path_count"] = self.loop_count
        return payload


@dataclass
class PerimeterVariableWidthReport:
    generated_at_utc: str
    layer_count: int
    island_count_total: int
    perimeter_count_requested: int
    wall_sequence: str
    min_width_mm: float
    max_width_mm: float
    loop_count_total: int
    path_length_mm_total: float
    transition_count_total: int
    transition_length_mm_total: float
    junction_count_total: int
    half_edge_bead_count_total: int
    half_edge_redistribution_mm_total: float
    junction_carryover_event_count_total: int
    junction_carryover_ratio_avg: float
    junction_carryover_cross_island_event_count_total: int
    junction_carryover_source_island_count_total: int
    warning_count: int
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _validate_perimeter_count(perimeter_count: int) -> int:
    if perimeter_count < 1:
        raise SlicerV2PerimeterVariableError("PERIMETER_VARIABLE_COUNT_INVALID")
    if perimeter_count > 20:
        raise SlicerV2PerimeterVariableError("PERIMETER_VARIABLE_COUNT_EXCESSIVE")
    return perimeter_count


def _validate_width_bounds(min_width_mm: float, max_width_mm: float, base_width_mm: float) -> tuple[float, float, float]:
    if min_width_mm <= EPSILON:
        raise SlicerV2PerimeterVariableError("PERIMETER_VARIABLE_MIN_WIDTH_INVALID")
    if max_width_mm <= EPSILON:
        raise SlicerV2PerimeterVariableError("PERIMETER_VARIABLE_MAX_WIDTH_INVALID")
    if max_width_mm < min_width_mm:
        raise SlicerV2PerimeterVariableError("PERIMETER_VARIABLE_WIDTH_RANGE_INVALID")
    if base_width_mm <= EPSILON:
        raise SlicerV2PerimeterVariableError("PERIMETER_VARIABLE_BASE_WIDTH_INVALID")
    base = max(min_width_mm, min(max_width_mm, base_width_mm))
    return min_width_mm, max_width_mm, base


def _validate_wall_sequence(wall_sequence: str) -> str:
    if wall_sequence not in {WALL_SEQUENCE_OUTER_TO_INNER, WALL_SEQUENCE_INNER_TO_OUTER}:
        raise SlicerV2PerimeterVariableError(f"PERIMETER_VARIABLE_WALL_SEQUENCE_INVALID:{wall_sequence}")
    return wall_sequence


def _validate_layer_graphs(layer_graphs: Sequence[LayerIslandGraph]) -> list[LayerIslandGraph]:
    graphs = list(layer_graphs)
    for index, graph in enumerate(graphs):
        if not isinstance(graph, LayerIslandGraph):
            raise SlicerV2PerimeterVariableError(f"PERIMETER_VARIABLE_LAYER_GRAPH_INVALID:{index}")
    return graphs


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, float(value)))


def _radial_offset_polygon(polygon: Polygon, delta_mm: float) -> Polygon | None:
    if abs(delta_mm) <= EPSILON:
        return polygon

    center = polygon.centroid
    shifted_points: list[Point2] = []
    for point in polygon.points:
        dx = point.x - center.x
        dy = point.y - center.y
        distance = hypot(dx, dy)
        if distance <= EPSILON:
            return None
        target_distance = distance + delta_mm
        if target_distance <= EPSILON:
            return None
        scale = target_distance / distance
        shifted_points.append(Point2(center.x + dx * scale, center.y + dy * scale))

    try:
        return Polygon(tuple(shifted_points)).with_winding(clockwise=polygon.is_clockwise)
    except Exception:
        return None


def _width_schedule(
    *,
    shell_count: int,
    feature_span_mm: float,
    min_width_mm: float,
    max_width_mm: float,
    base_width_mm: float,
) -> list[float]:
    if shell_count <= 0:
        return []
    if shell_count == 1:
        return [base_width_mm]

    denom = (base_width_mm * 12.0) + EPSILON
    span_factor = max(0.0, min(1.0, feature_span_mm / denom))
    outer_target = max(base_width_mm, min(max_width_mm, base_width_mm * (1.0 + 0.25 * span_factor)))
    inner_target = max(min_width_mm, min(base_width_mm, base_width_mm * (1.0 - (0.25 * (1.0 - span_factor)))))

    widths: list[float] = []
    for shell_index in range(shell_count):
        ratio = float(shell_index) / float(shell_count - 1)
        candidate = outer_target + (inner_target - outer_target) * ratio
        widths.append(max(min_width_mm, min(max_width_mm, candidate)))
    return widths


def _smooth_width_schedule(
    widths_mm: Sequence[float],
    *,
    min_width_mm: float,
    max_width_mm: float,
    smoothing: float,
) -> list[float]:
    widths = [float(value) for value in widths_mm]
    if len(widths) <= 1:
        return widths
    ratio = _clamp(smoothing, 0.0, 1.0)
    smoothed: list[float] = []
    for index, width in enumerate(widths):
        prev_width = widths[index - 1] if index > 0 else width
        next_width = widths[index + 1] if index + 1 < len(widths) else width
        local_avg = (prev_width + width + next_width) / 3.0
        blended = (width * (1.0 - ratio)) + (local_avg * ratio)
        smoothed.append(_clamp(blended, min_width_mm, max_width_mm))
    return smoothed


def _junction_count(polygon: Polygon, sharp_angle_deg: float) -> int:
    points = list(polygon.points)
    if len(points) < 3:
        return 0
    threshold = _clamp(sharp_angle_deg, 30.0, 175.0)
    count = 0
    for index, curr in enumerate(points):
        prev = points[index - 1]
        nxt = points[(index + 1) % len(points)]
        v1_x = prev.x - curr.x
        v1_y = prev.y - curr.y
        v2_x = nxt.x - curr.x
        v2_y = nxt.y - curr.y
        len1 = hypot(v1_x, v1_y)
        len2 = hypot(v2_x, v2_y)
        if len1 <= EPSILON or len2 <= EPSILON:
            continue
        cosine = ((v1_x * v2_x) + (v1_y * v2_y)) / (len1 * len2)
        cosine = _clamp(cosine, -1.0, 1.0)
        angle = degrees(acos(cosine))
        if angle <= threshold:
            count += 1
    return count


def _edge_lengths(polygon: Polygon) -> list[float]:
    points = list(polygon.points)
    if len(points) < 2:
        return []
    lengths: list[float] = []
    for index, start in enumerate(points):
        end = points[(index + 1) % len(points)]
        lengths.append(float(start.distance_to(end)))
    return lengths


def _edge_sharpness(polygon: Polygon, sharp_angle_deg: float) -> list[float]:
    points = list(polygon.points)
    count = len(points)
    if count < 3:
        return [0.0] * max(0, count)
    threshold = _clamp(sharp_angle_deg, 30.0, 175.0)
    vertex_sharpness: list[float] = [0.0] * count
    for index, curr in enumerate(points):
        prev = points[index - 1]
        nxt = points[(index + 1) % count]
        v1_x = prev.x - curr.x
        v1_y = prev.y - curr.y
        v2_x = nxt.x - curr.x
        v2_y = nxt.y - curr.y
        len1 = hypot(v1_x, v1_y)
        len2 = hypot(v2_x, v2_y)
        if len1 <= EPSILON or len2 <= EPSILON:
            continue
        cosine = ((v1_x * v2_x) + (v1_y * v2_y)) / (len1 * len2)
        cosine = _clamp(cosine, -1.0, 1.0)
        angle = degrees(acos(cosine))
        if angle >= threshold:
            vertex_sharpness[index] = 0.0
        else:
            vertex_sharpness[index] = _clamp((threshold - angle) / threshold, 0.0, 1.0)

    edge_sharpness: list[float] = []
    for index in range(count):
        left = vertex_sharpness[index]
        right = vertex_sharpness[(index + 1) % count]
        edge_sharpness.append(float((left + right) * 0.5))
    return edge_sharpness


@dataclass(frozen=True)
class _JunctionCarryState:
    fractions: tuple[float, ...]
    deltas: tuple[float, ...]
    source_layer_index: int | None = None
    source_island_index: int | None = None


def _edge_midpoint_fractions(edge_lengths_mm: Sequence[float]) -> list[float]:
    if not edge_lengths_mm:
        return []
    total_length = sum(max(EPSILON, float(length)) for length in edge_lengths_mm)
    if total_length <= EPSILON:
        return [0.0 for _ in edge_lengths_mm]
    fractions: list[float] = []
    offset = 0.0
    for edge_length in edge_lengths_mm:
        length = max(EPSILON, float(edge_length))
        midpoint = offset + (0.5 * length)
        fractions.append(float(midpoint / total_length))
        offset += length
    return fractions


def _normalize_fraction01(value: float) -> float:
    normalized = float(value) % 1.0
    if normalized < 0.0:
        normalized += 1.0
    return float(normalized)


def _prepare_carry_profile(state: _JunctionCarryState) -> tuple[list[float], list[float]]:
    pairs = list(zip(state.fractions, state.deltas))
    if not pairs:
        return [], []

    normalized = sorted((_normalize_fraction01(float(fraction)), float(delta)) for fraction, delta in pairs)
    merged_fractions: list[float] = []
    merged_deltas: list[float] = []
    current_fraction = normalized[0][0]
    acc = 0.0
    count = 0
    for fraction, delta in normalized:
        if abs(float(fraction) - float(current_fraction)) <= 1e-6:
            acc += float(delta)
            count += 1
            continue
        merged_fractions.append(float(current_fraction))
        merged_deltas.append(float(acc / max(1, count)))
        current_fraction = float(fraction)
        acc = float(delta)
        count = 1
    merged_fractions.append(float(current_fraction))
    merged_deltas.append(float(acc / max(1, count)))
    return merged_fractions, merged_deltas


def _sample_carry_profile(
    source_fractions: Sequence[float],
    source_deltas: Sequence[float],
    target_fraction: float,
    *,
    phase_shift: float,
) -> float:
    if not source_fractions or not source_deltas:
        return 0.0
    if len(source_fractions) == 1:
        return float(source_deltas[0])

    target = _normalize_fraction01(float(target_fraction) + float(phase_shift))
    count = len(source_fractions)
    for index in range(count):
        left_fraction = float(source_fractions[index])
        right_index = (index + 1) % count
        right_fraction = float(source_fractions[right_index])
        if right_index == 0:
            right_fraction += 1.0
        local_target = float(target)
        if right_index == 0 and local_target < left_fraction:
            local_target += 1.0
        if local_target < left_fraction - EPSILON or local_target > right_fraction + EPSILON:
            continue
        span = max(EPSILON, right_fraction - left_fraction)
        ratio = _clamp((local_target - left_fraction) / span, 0.0, 1.0)
        left_delta = float(source_deltas[index])
        right_delta = float(source_deltas[right_index])
        return float(left_delta + ((right_delta - left_delta) * ratio))

    nearest_index = 0
    nearest_distance = float("inf")
    for index, source_fraction in enumerate(source_fractions):
        distance = abs(float(source_fraction) - target)
        distance = min(distance, 1.0 - distance)
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_index = index
    return float(source_deltas[nearest_index])


def _sample_carry_profile_nearest(
    source_fractions: Sequence[float],
    source_deltas: Sequence[float],
    target_fraction: float,
    *,
    phase_shift: float,
) -> float:
    if not source_fractions or not source_deltas:
        return 0.0
    target = _normalize_fraction01(float(target_fraction) + float(phase_shift))
    nearest_index = 0
    nearest_distance = float("inf")
    for index, source_fraction in enumerate(source_fractions):
        distance = abs(float(source_fraction) - target)
        distance = min(distance, 1.0 - distance)
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_index = index
    return float(source_deltas[nearest_index])


def _carry_alignment_phase(
    source_fractions: Sequence[float],
    source_deltas: Sequence[float],
    target_fractions: Sequence[float],
    target_sharpness: Sequence[float],
) -> float:
    if not source_fractions or not target_fractions:
        return 0.0
    if not target_sharpness:
        return 0.0

    sharpness = [max(0.0, min(1.0, float(value))) for value in target_sharpness]
    if max(sharpness) <= EPSILON:
        return 0.0

    candidate_count = max(6, min(36, len(source_fractions) * 6))
    best_phase = 0.0
    best_score = float("-inf")
    for candidate_index in range(candidate_count):
        phase = float(candidate_index) / float(candidate_count)
        score = 0.0
        for target_index, target_fraction in enumerate(target_fractions):
            sampled = _sample_carry_profile(
                source_fractions,
                source_deltas,
                float(target_fraction),
                phase_shift=phase,
            )
            sharp = sharpness[target_index] if target_index < len(sharpness) else 0.0
            score += abs(float(sampled)) * (0.2 + (sharp * 0.8))
        if score > best_score:
            best_score = score
            best_phase = phase
    return float(best_phase)


def _resample_carryover_deltas(
    state: _JunctionCarryState | None,
    target_fractions: Sequence[float],
    target_sharpness: Sequence[float] = (),
) -> list[float]:
    if state is None or not state.fractions or not state.deltas or not target_fractions:
        return [0.0 for _ in target_fractions]
    source_fractions, source_deltas = _prepare_carry_profile(state)
    if not source_fractions:
        return [0.0 for _ in target_fractions]

    phase = _carry_alignment_phase(
        source_fractions,
        source_deltas,
        target_fractions,
        target_sharpness,
    )
    out: list[float] = []
    for target in target_fractions:
        interpolated = _sample_carry_profile(
            source_fractions,
            source_deltas,
            float(target),
            phase_shift=phase,
        )
        nearest = _sample_carry_profile_nearest(
            source_fractions,
            source_deltas,
            float(target),
            phase_shift=phase,
        )
        blended = (0.72 * float(interpolated)) + (0.28 * float(nearest))
        out.append(float(_clamp(blended, -0.9, 0.9)))
    return out


def _weighted_width_average(widths_mm: Sequence[float], edge_lengths_mm: Sequence[float]) -> float:
    if not widths_mm or not edge_lengths_mm or len(widths_mm) != len(edge_lengths_mm):
        return 0.0
    total_length = sum(max(EPSILON, float(length)) for length in edge_lengths_mm)
    if total_length <= EPSILON:
        return 0.0
    total_width = 0.0
    for width, edge_length in zip(widths_mm, edge_lengths_mm):
        total_width += float(width) * max(EPSILON, float(edge_length))
    return float(total_width / total_length)


def _rebalance_widths_to_base(
    widths_mm: Sequence[float],
    *,
    edge_lengths_mm: Sequence[float],
    base_width_mm: float,
    min_width_mm: float,
    max_width_mm: float,
    max_iterations: int = 4,
) -> list[float]:
    corrected = [_clamp(float(value), min_width_mm, max_width_mm) for value in widths_mm]
    if not corrected or not edge_lengths_mm or len(corrected) != len(edge_lengths_mm):
        return corrected

    for _ in range(max(1, int(max_iterations))):
        corrected_avg = _weighted_width_average(corrected, edge_lengths_mm)
        correction_delta = float(base_width_mm) - float(corrected_avg)
        if abs(correction_delta) <= 1e-6:
            break
        adjustable_indices = [
            index
            for index, value in enumerate(corrected)
            if value > (min_width_mm + EPSILON) and value < (max_width_mm - EPSILON)
        ]
        if not adjustable_indices:
            break
        adjustable_weight = sum(max(EPSILON, float(edge_lengths_mm[index])) for index in adjustable_indices)
        if adjustable_weight <= EPSILON:
            break
        for index in adjustable_indices:
            weight = max(EPSILON, float(edge_lengths_mm[index])) / adjustable_weight
            corrected[index] = _clamp(
                float(corrected[index]) + (correction_delta * weight),
                min_width_mm,
                max_width_mm,
            )
    return corrected


def _redistribute_half_edge_widths(
    *,
    base_width_mm: float,
    shell_index: int,
    widths_mm: Sequence[float],
    edge_lengths_mm: Sequence[float],
    edge_sharpness: Sequence[float],
    min_width_mm: float,
    max_width_mm: float,
    smoothing: float,
    carryover_deltas: Sequence[float] = (),
    carryover_strength: float = 0.0,
) -> tuple[list[float], float, float]:
    if not edge_lengths_mm:
        return [], 0.0, 0.0

    total_length = sum(max(EPSILON, float(length)) for length in edge_lengths_mm)
    avg_length = total_length / float(len(edge_lengths_mm))
    if avg_length <= EPSILON:
        return [float(base_width_mm)] * len(edge_lengths_mm), 0.0, 0.0

    shell_count = max(1, len(widths_mm))
    shell_progress = float(shell_index) / float(max(1, shell_count - 1))
    outer_bias = 1.0 - shell_progress
    prev_width = float(widths_mm[shell_index - 1]) if shell_index > 0 else float(base_width_mm)
    next_width = (
        float(widths_mm[shell_index + 1]) if shell_index + 1 < len(widths_mm) else float(base_width_mm)
    )
    neighbor_gradient = (prev_width - next_width) * 0.5
    smooth = _clamp(smoothing, 0.0, 1.0)
    carry_strength = _clamp(carryover_strength, 0.0, 1.0)
    carry_profile = [float(value) for value in carryover_deltas]

    provisional: list[float] = []
    carry_influence_acc = 0.0
    for index, edge_length in enumerate(edge_lengths_mm):
        length_ratio = _clamp(float(edge_length) / avg_length, 0.25, 2.25)
        length_term = (length_ratio - 1.0) * 0.22 * smooth
        sharpness = float(edge_sharpness[index]) if index < len(edge_sharpness) else 0.0
        junction_focus = _clamp(sharpness * sharpness, 0.0, 1.0)
        corner_term = ((outer_bias * 0.27) - ((1.0 - outer_bias) * 0.14)) * (0.35 + (0.65 * junction_focus)) * smooth
        gradient_term = (neighbor_gradient / max(base_width_mm, EPSILON)) * 0.08 * smooth
        carry_delta = float(carry_profile[index]) if index < len(carry_profile) else 0.0
        carry_term = carry_delta * carry_strength * (0.32 + (sharpness * 0.48))
        if sharpness > 0.35 and (carry_term * corner_term) < 0.0:
            carry_term *= max(0.2, 1.0 - (sharpness * 0.75))
        candidate = float(base_width_mm) * (1.0 + length_term + corner_term + gradient_term + carry_term)
        provisional.append(_clamp(candidate, min_width_mm, max_width_mm))
        carry_influence_acc += abs(carry_term) * max(EPSILON, float(edge_length))

    weighted_avg = _weighted_width_average(provisional, edge_lengths_mm)
    scale = float(base_width_mm / weighted_avg) if weighted_avg > EPSILON else 1.0
    corrected = [_clamp(float(value) * scale, min_width_mm, max_width_mm) for value in provisional]
    corrected = _rebalance_widths_to_base(
        corrected,
        edge_lengths_mm=edge_lengths_mm,
        base_width_mm=float(base_width_mm),
        min_width_mm=float(min_width_mm),
        max_width_mm=float(max_width_mm),
        max_iterations=5,
    )

    if len(corrected) > 2 and smooth > EPSILON:
        smoothed: list[float] = list(corrected)
        for index, width in enumerate(corrected):
            left = corrected[index - 1]
            right = corrected[(index + 1) % len(corrected)]
            laplacian = ((float(left) + float(right)) * 0.5) - float(width)
            sharpness = float(edge_sharpness[index]) if index < len(edge_sharpness) else 0.0
            lock = _clamp(sharpness * (0.45 + (outer_bias * 0.35)), 0.0, 0.9)
            gain = smooth * (0.28 + (0.12 * (1.0 - outer_bias))) * (1.0 - lock)
            carry_gradient = 0.0
            if carry_profile:
                prev_delta = float(carry_profile[index - 1]) if index > 0 else float(carry_profile[-1])
                next_delta = (
                    float(carry_profile[index + 1]) if index + 1 < len(carry_profile) else float(carry_profile[0])
                )
                carry_gradient = (next_delta - prev_delta) * 0.5 * carry_strength * 0.08 * (1.0 - lock)
            candidate = float(width) + (laplacian * gain) + (carry_gradient * float(base_width_mm))
            smoothed[index] = _clamp(candidate, min_width_mm, max_width_mm)
        corrected = _rebalance_widths_to_base(
            smoothed,
            edge_lengths_mm=edge_lengths_mm,
            base_width_mm=float(base_width_mm),
            min_width_mm=float(min_width_mm),
            max_width_mm=float(max_width_mm),
            max_iterations=4,
        )

    redistribution = 0.0
    for value, edge_length in zip(corrected, edge_lengths_mm):
        redistribution += abs(float(value) - float(base_width_mm)) * max(EPSILON, float(edge_length))
    redistribution = redistribution / total_length if total_length > EPSILON else 0.0
    carry_influence = carry_influence_acc / total_length if total_length > EPSILON else 0.0
    return corrected, float(redistribution), float(carry_influence)


def _half_edge_transition_length(
    edge_lengths_mm: Sequence[float],
    widths_mm: Sequence[float],
    nominal_width_mm: float,
) -> float:
    if len(widths_mm) < 2 or len(edge_lengths_mm) != len(widths_mm):
        return 0.0
    total = 0.0
    nominal = max(float(nominal_width_mm), EPSILON)
    for index, width in enumerate(widths_mm):
        next_width = widths_mm[(index + 1) % len(widths_mm)]
        edge_length = max(EPSILON, float(edge_lengths_mm[index]))
        total += edge_length * abs(float(next_width) - float(width)) / nominal
    return float(total)


def _cumulative_offset(widths: Sequence[float], shell_index: int) -> float:
    total = 0.0
    for index in range(shell_index):
        total += float(widths[index])
    return total


def _build_loops_for_polygon(
    *,
    layer_index: int,
    island_index: int,
    role: str,
    polygon: Polygon,
    widths_mm: Sequence[float],
    min_width_mm: float,
    max_width_mm: float,
    wall_sequence: str,
    transition_smoothing: float,
    junction_compensation_enabled: bool,
    junction_sharp_angle_deg: float,
    carryover_strength: float,
    carry_state: _JunctionCarryState | None,
    warnings: list[str],
) -> tuple[
    list[VariableWidthLoopPlan],
    list[VariableWidthTransitionPlan],
    list[HalfEdgeBeadPlan],
    _JunctionCarryState | None,
    int,
    float,
]:
    loops: list[VariableWidthLoopPlan] = []
    transitions: list[VariableWidthTransitionPlan] = []
    half_edge_beads: list[HalfEdgeBeadPlan] = []
    smoothing = _clamp(transition_smoothing, 0.0, 1.0)
    state = carry_state
    carry_event_count = 0
    carry_ratio_sum = 0.0
    indices = _shell_indices(len(widths_mm), wall_sequence)
    for shell_index in indices:
        source_layer_index = int(state.source_layer_index) if state and state.source_layer_index is not None else None
        source_island_index = int(state.source_island_index) if state and state.source_island_index is not None else None
        width_mm = float(widths_mm[shell_index])
        distance_from_boundary = _cumulative_offset(widths_mm, shell_index)
        if role == "outer":
            delta_mm = -distance_from_boundary
        elif role == "hole":
            delta_mm = distance_from_boundary
        else:
            raise SlicerV2PerimeterVariableError(f"PERIMETER_VARIABLE_ROLE_INVALID:{role}")

        offset_polygon = _radial_offset_polygon(polygon, delta_mm)
        if offset_polygon is None:
            warnings.append(
                f"layer_{layer_index}:island_{island_index}:{role}:shell_{shell_index}:offset_failed"
            )
            continue

        prev_width = float(widths_mm[shell_index - 1]) if shell_index > 0 else width_mm
        next_width = float(widths_mm[shell_index + 1]) if shell_index + 1 < len(widths_mm) else width_mm
        width_start = width_mm + ((prev_width - width_mm) * smoothing)
        width_end = width_mm + ((next_width - width_mm) * smoothing)
        transition_length = float(offset_polygon.perimeter * abs(width_end - width_start) / max(width_mm, EPSILON))
        edge_lengths = _edge_lengths(offset_polygon)
        edge_sharpness = _edge_sharpness(offset_polygon, junction_sharp_angle_deg)
        fractions = _edge_midpoint_fractions(edge_lengths)
        carryover_deltas = _resample_carryover_deltas(state, fractions, edge_sharpness)
        half_edge_widths, redistribution, carry_influence = _redistribute_half_edge_widths(
            base_width_mm=width_mm,
            shell_index=shell_index,
            widths_mm=widths_mm,
            edge_lengths_mm=edge_lengths,
            edge_sharpness=edge_sharpness,
            min_width_mm=float(min_width_mm),
            max_width_mm=float(max_width_mm),
            smoothing=smoothing,
            carryover_deltas=carryover_deltas,
            carryover_strength=float(carryover_strength),
        )
        if not half_edge_widths and edge_lengths:
            half_edge_widths = [width_mm] * len(edge_lengths)
        if edge_lengths and half_edge_widths:
            deltas = [
                _clamp((float(value) - width_mm) / max(width_mm, EPSILON), -0.6, 0.6)
                for value in half_edge_widths
            ]
            state = _JunctionCarryState(
                fractions=tuple(fractions),
                deltas=tuple(deltas),
                source_layer_index=int(layer_index),
                source_island_index=int(island_index),
            )
        half_edge_width_min = min(half_edge_widths) if half_edge_widths else float(width_mm)
        half_edge_width_max = max(half_edge_widths) if half_edge_widths else float(width_mm)
        transition_length += _half_edge_transition_length(edge_lengths, half_edge_widths, width_mm)
        if carry_influence > EPSILON:
            carry_event_count += 1
            carry_ratio_sum += float(carry_influence)
        junction_count = _junction_count(offset_polygon, junction_sharp_angle_deg)
        point_count = len(offset_polygon.points)
        junction_compensation_ratio = 1.0
        if junction_compensation_enabled and point_count > 0 and junction_count > 0:
            penalty = min(0.2, float(junction_count) / float(point_count * 8))
            junction_compensation_ratio = 1.0 - penalty
        path_length = float(offset_polygon.perimeter * junction_compensation_ratio)
        redistribution_ratio = _clamp(
            float(abs(redistribution) / max(EPSILON, path_length * max(width_mm, EPSILON))),
            0.0,
            1.0,
        )

        loops.append(
            VariableWidthLoopPlan(
                layer_index=layer_index,
                island_index=island_index,
                role=role,
                shell_index=shell_index,
                width_mm=width_mm,
                width_start_mm=float(width_start),
                width_end_mm=float(width_end),
                point_count=point_count,
                path_length_mm=path_length,
                transition_length_mm=transition_length,
                half_edge_count=len(half_edge_widths),
                half_edge_width_min_mm=float(half_edge_width_min),
                half_edge_width_max_mm=float(half_edge_width_max),
                half_edge_redistribution_mm=float(redistribution),
                junction_carryover_ratio=float(carry_influence),
                junction_count=junction_count,
                junction_compensation_ratio=float(junction_compensation_ratio),
                carryover_source_layer_index=source_layer_index,
                carryover_source_island_index=source_island_index,
                carryover_strength=float(max(0.0, carryover_strength)),
                half_edge_redistribution_ratio=float(redistribution_ratio),
                points=tuple(offset_polygon.points),
            )
        )

        for edge_index, redistributed_width in enumerate(half_edge_widths):
            edge_length = float(edge_lengths[edge_index]) if edge_index < len(edge_lengths) else 0.0
            sharpness_ratio = float(edge_sharpness[edge_index]) if edge_index < len(edge_sharpness) else 0.0
            half_edge_beads.append(
                HalfEdgeBeadPlan(
                    layer_index=layer_index,
                    island_index=island_index,
                    role=role,
                    shell_index=shell_index,
                    edge_index=edge_index,
                    edge_length_mm=edge_length,
                    base_width_mm=float(width_mm),
                    width_mm=float(redistributed_width),
                    sharpness_ratio=sharpness_ratio,
                )
            )

        if shell_index + 1 < len(widths_mm):
            width_next = float(widths_mm[shell_index + 1])
            inter_shell_transition = float(
                offset_polygon.perimeter * abs(width_next - width_mm) * max(0.0, smoothing)
            )
            transitions.append(
                VariableWidthTransitionPlan(
                    layer_index=layer_index,
                    island_index=island_index,
                    from_shell_index=shell_index,
                    to_shell_index=shell_index + 1,
                    width_start_mm=width_mm,
                    width_end_mm=width_next,
                    transition_length_mm=inter_shell_transition,
                    junction_count=junction_count,
                    carryover_continuity_ratio=float(_clamp(carry_influence, 0.0, 1.0)),
                )
            )
    return loops, transitions, half_edge_beads, state, int(carry_event_count), float(carry_ratio_sum)


def build_variable_width_perimeters(
    layer_graphs: Sequence[LayerIslandGraph],
    *,
    perimeter_count: int,
    base_line_width_mm: float,
    min_line_width_mm: float,
    max_line_width_mm: float,
    wall_sequence: str = WALL_SEQUENCE_OUTER_TO_INNER,
    first_layer_single_wall: bool = False,
    transition_smoothing: float = 0.35,
    junction_compensation_enabled: bool = True,
    junction_sharp_angle_deg: float = 120.0,
    carryover_cross_island_enabled: bool = False,
    carryover_strength: float = -1.0,
    max_workers: int = 1,
) -> tuple[list[LayerVariableWidthPlan], PerimeterVariableWidthReport]:
    shell_count_requested = _validate_perimeter_count(int(perimeter_count))
    min_width, max_width, base_width = _validate_width_bounds(
        float(min_line_width_mm),
        float(max_line_width_mm),
        float(base_line_width_mm),
    )
    sequence = _validate_wall_sequence(str(wall_sequence))
    smoothing = _clamp(float(transition_smoothing), 0.0, 1.0)
    cross_island_carry = bool(carryover_cross_island_enabled)
    carry_strength = smoothing
    if float(carryover_strength) >= 0.0:
        carry_strength = _clamp(float(carryover_strength), 0.0, 1.5)
    sharp_angle_deg = _clamp(float(junction_sharp_angle_deg), 30.0, 175.0)

    graphs = _validate_layer_graphs(layer_graphs)

    def _build_layer(layer_graph: LayerIslandGraph) -> tuple[LayerVariableWidthPlan, list[str], int]:
        layer_warnings: list[str] = []
        shell_count_for_layer = shell_count_requested
        if first_layer_single_wall and layer_graph.layer_index == 0:
            shell_count_for_layer = 1

        loops_for_layer: list[VariableWidthLoopPlan] = []
        transitions_for_layer: list[VariableWidthTransitionPlan] = []
        beads_for_layer: list[HalfEdgeBeadPlan] = []
        junction_carry_event_count = 0
        junction_carry_ratio_sum = 0.0
        junction_carry_cross_island_event_count = 0
        junction_carry_source_islands: set[int] = set()
        layer_carry_state: _JunctionCarryState | None = None
        for island_index, island in enumerate(layer_graph.islands):
            feature_span = min(float(island.bounds.width), float(island.bounds.height))
            widths = _width_schedule(
                shell_count=shell_count_for_layer,
                feature_span_mm=feature_span,
                min_width_mm=min_width,
                max_width_mm=max_width,
                base_width_mm=base_width,
            )
            smoothed_widths = _smooth_width_schedule(
                widths,
                min_width_mm=min_width,
                max_width_mm=max_width,
                smoothing=smoothing,
            )
            island_carry_state: _JunctionCarryState | None = layer_carry_state if cross_island_carry else None
            if (
                cross_island_carry
                and island_carry_state is not None
                and island_carry_state.source_island_index is not None
                and int(island_carry_state.source_island_index) != int(island_index)
            ):
                junction_carry_cross_island_event_count += 1
                junction_carry_source_islands.add(int(island_carry_state.source_island_index))
            loops, transitions, beads, island_carry_state, carry_events, carry_ratio_sum = _build_loops_for_polygon(
                layer_index=layer_graph.layer_index,
                island_index=island_index,
                role="outer",
                polygon=island.outer,
                widths_mm=smoothed_widths,
                min_width_mm=min_width,
                max_width_mm=max_width,
                wall_sequence=sequence,
                transition_smoothing=smoothing,
                junction_compensation_enabled=bool(junction_compensation_enabled),
                junction_sharp_angle_deg=sharp_angle_deg,
                carryover_strength=carry_strength,
                carry_state=island_carry_state,
                warnings=layer_warnings,
            )
            loops_for_layer.extend(loops)
            transitions_for_layer.extend(transitions)
            beads_for_layer.extend(beads)
            junction_carry_event_count += int(carry_events)
            junction_carry_ratio_sum += float(carry_ratio_sum)
            for hole in island.holes:
                loops, transitions, beads, island_carry_state, carry_events, carry_ratio_sum = _build_loops_for_polygon(
                    layer_index=layer_graph.layer_index,
                    island_index=island_index,
                    role="hole",
                    polygon=hole,
                    widths_mm=smoothed_widths,
                    min_width_mm=min_width,
                    max_width_mm=max_width,
                    wall_sequence=sequence,
                    transition_smoothing=smoothing,
                    junction_compensation_enabled=bool(junction_compensation_enabled),
                    junction_sharp_angle_deg=sharp_angle_deg,
                    carryover_strength=carry_strength,
                    carry_state=island_carry_state,
                    warnings=layer_warnings,
                )
                loops_for_layer.extend(loops)
                transitions_for_layer.extend(transitions)
                beads_for_layer.extend(beads)
                junction_carry_event_count += int(carry_events)
                junction_carry_ratio_sum += float(carry_ratio_sum)
            if cross_island_carry:
                layer_carry_state = island_carry_state

        layer_length = 0.0
        transition_length = 0.0
        junction_count = 0
        half_edge_redistribution = 0.0
        layer_min_width = max_width
        layer_max_width = min_width
        for loop in loops_for_layer:
            layer_length += loop.path_length_mm
            transition_length += loop.transition_length_mm
            junction_count += int(loop.junction_count)
            half_edge_redistribution += float(loop.half_edge_redistribution_mm)
            layer_min_width = min(layer_min_width, loop.width_mm)
            layer_max_width = max(layer_max_width, loop.width_mm)

        for transition in transitions_for_layer:
            transition_length += max(0.0, float(transition.transition_length_mm))

        if not loops_for_layer:
            layer_min_width = 0.0
            layer_max_width = 0.0

        return (
            LayerVariableWidthPlan(
                layer_index=layer_graph.layer_index,
                z_height_mm=float(layer_graph.z_height_mm),
                loop_count=len(loops_for_layer),
                path_length_mm=float(layer_length),
                min_width_mm=float(layer_min_width),
                max_width_mm=float(layer_max_width),
                transition_count=len(transitions_for_layer),
                transition_length_mm=float(transition_length),
                junction_count=int(junction_count),
                half_edge_bead_count=len(beads_for_layer),
                half_edge_redistribution_mm=float(half_edge_redistribution),
                junction_carryover_event_count=int(junction_carry_event_count),
                junction_carryover_ratio_avg=float(
                    junction_carry_ratio_sum / max(1, junction_carry_event_count)
                )
                if junction_carry_event_count > 0
                else 0.0,
                junction_carryover_cross_island_event_count=int(junction_carry_cross_island_event_count),
                junction_carryover_source_island_count=int(len(junction_carry_source_islands)),
                loops=loops_for_layer,
                transitions=transitions_for_layer,
                half_edge_beads=beads_for_layer,
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

    layer_plans: list[LayerVariableWidthPlan] = []
    warnings: list[str] = []
    island_count_total = 0
    loop_count_total = 0
    path_length_mm_total = 0.0
    transition_count_total = 0
    transition_length_mm_total = 0.0
    junction_count_total = 0
    half_edge_bead_count_total = 0
    half_edge_redistribution_mm_total = 0.0
    junction_carryover_event_count_total = 0
    junction_carryover_ratio_sum = 0.0
    junction_carryover_cross_island_event_count_total = 0
    junction_carryover_source_island_count_total = 0
    used_min_width = max_width
    used_max_width = min_width

    for layer_plan, layer_warnings, island_count in results:
        layer_plans.append(layer_plan)
        warnings.extend(layer_warnings)
        island_count_total += island_count
        loop_count_total += layer_plan.loop_count
        path_length_mm_total += layer_plan.path_length_mm
        transition_count_total += int(layer_plan.transition_count)
        transition_length_mm_total += float(layer_plan.transition_length_mm)
        junction_count_total += int(layer_plan.junction_count)
        half_edge_bead_count_total += int(layer_plan.half_edge_bead_count)
        half_edge_redistribution_mm_total += float(layer_plan.half_edge_redistribution_mm)
        junction_carryover_event_count_total += int(layer_plan.junction_carryover_event_count)
        junction_carryover_cross_island_event_count_total += int(layer_plan.junction_carryover_cross_island_event_count)
        junction_carryover_source_island_count_total += int(layer_plan.junction_carryover_source_island_count)
        junction_carryover_ratio_sum += float(layer_plan.junction_carryover_ratio_avg) * float(
            max(0, layer_plan.junction_carryover_event_count)
        )
        for loop in layer_plan.loops:
            used_min_width = min(used_min_width, loop.width_mm)
            used_max_width = max(used_max_width, loop.width_mm)

    layer_plans.sort(key=lambda plan: int(plan.layer_index))

    if loop_count_total == 0:
        used_min_width = 0.0
        used_max_width = 0.0

    report = PerimeterVariableWidthReport(
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        layer_count=len(layer_plans),
        island_count_total=island_count_total,
        perimeter_count_requested=shell_count_requested,
        wall_sequence=sequence,
        min_width_mm=float(used_min_width),
        max_width_mm=float(used_max_width),
        loop_count_total=loop_count_total,
        path_length_mm_total=float(path_length_mm_total),
        transition_count_total=int(transition_count_total),
        transition_length_mm_total=float(transition_length_mm_total),
        junction_count_total=int(junction_count_total),
        half_edge_bead_count_total=int(half_edge_bead_count_total),
        half_edge_redistribution_mm_total=float(half_edge_redistribution_mm_total),
        junction_carryover_event_count_total=int(junction_carryover_event_count_total),
        junction_carryover_ratio_avg=float(
            junction_carryover_ratio_sum / max(1, junction_carryover_event_count_total)
        )
        if junction_carryover_event_count_total > 0
        else 0.0,
        junction_carryover_cross_island_event_count_total=int(junction_carryover_cross_island_event_count_total),
        junction_carryover_source_island_count_total=int(junction_carryover_source_island_count_total),
        warning_count=len(warnings),
        warnings=warnings,
    )
    return layer_plans, report
