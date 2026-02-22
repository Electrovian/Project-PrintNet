from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .errors import SlicerV2PolygonPipelineError
from .geometry import EPSILON, Island, Point2, Polygon
from .polygon_pipeline import offset_polygon


@dataclass(frozen=True)
class RegionExpansionParameters:
    tiny_expansion: float
    initial_step: float
    other_step: float
    num_other_steps: int
    max_inflation: float
    arc_tolerance: float
    shortest_edge_length: float

    @staticmethod
    def build(full_expansion: float, expansion_step: float, max_nr_expansion_steps: int) -> "RegionExpansionParameters":
        full = float(full_expansion)
        step = float(expansion_step)
        max_steps = int(max_nr_expansion_steps)
        if full <= EPSILON:
            raise SlicerV2PolygonPipelineError("REGION_EXPANSION_FULL_INVALID")
        if step <= EPSILON:
            raise SlicerV2PolygonPipelineError("REGION_EXPANSION_STEP_INVALID")
        if max_steps < 1:
            raise SlicerV2PolygonPipelineError("REGION_EXPANSION_MAX_STEPS_INVALID")

        tiny = min(0.25 * full, 0.05)
        nsteps = max(1, min(max_steps, int(round((full - tiny) / step)) if full > tiny else 1))
        initial = (full - tiny) / float(nsteps) if nsteps > 0 else full
        if initial <= EPSILON:
            initial = full
            nsteps = 1
            tiny = 0.0
        other = initial
        num_other = max(0, nsteps - 1)
        max_inflation = (tiny + (initial * nsteps)) * 1.1
        return RegionExpansionParameters(
            tiny_expansion=float(tiny),
            initial_step=float(initial),
            other_step=float(other),
            num_other_steps=int(num_other),
            max_inflation=float(max_inflation),
            arc_tolerance=0.1,
            shortest_edge_length=max(0.01, float(initial) * 0.1),
        )


@dataclass(frozen=True)
class WaveSeed:
    src: int
    boundary: int
    path: tuple[Point2, ...]


@dataclass(frozen=True)
class RegionExpansion:
    polygon: Polygon
    src_id: int
    boundary_id: int


def _as_polygon(item: Polygon | Island) -> Polygon:
    if isinstance(item, Polygon):
        return item
    if isinstance(item, Island):
        return item.outer
    raise SlicerV2PolygonPipelineError("REGION_EXPANSION_POLYGON_TYPE_INVALID")


def wave_seeds(
    src: Sequence[Polygon | Island],
    boundary: Sequence[Polygon | Island],
    tiny_expansion: float,
    sorted: bool = True,
) -> list[WaveSeed]:
    tiny = max(0.0, float(tiny_expansion))
    src_polys = [_as_polygon(item) for item in src]
    boundary_polys = [_as_polygon(item) for item in boundary]
    out: list[WaveSeed] = []
    for src_index, src_poly in enumerate(src_polys):
        expanded_bounds = src_poly.bounds.padded(tiny)
        for boundary_index, boundary_poly in enumerate(boundary_polys):
            if not expanded_bounds.intersects(boundary_poly.bounds):
                continue
            if not boundary_poly.contains_point(src_poly.centroid, include_boundary=True) and not src_poly.bounds.intersects(
                boundary_poly.bounds
            ):
                continue
            out.append(
                WaveSeed(
                    src=int(src_index),
                    boundary=int(boundary_index),
                    path=tuple(src_poly.points),
                )
            )
    if sorted:
        out.sort(key=lambda item: (item.boundary, item.src))
    return out


def propagate_waves(
    seeds: Sequence[WaveSeed],
    boundary: Sequence[Polygon | Island],
    params: RegionExpansionParameters,
) -> list[RegionExpansion]:
    boundary_polys = [_as_polygon(item) for item in boundary]
    if not seeds or not boundary_polys:
        return []

    total_offset = (
        float(params.tiny_expansion)
        + float(params.initial_step)
        + float(params.other_step) * float(max(0, int(params.num_other_steps)))
    )
    out: list[RegionExpansion] = []
    for seed in seeds:
        if seed.boundary < 0 or seed.boundary >= len(boundary_polys):
            continue
        if len(seed.path) < 3:
            continue
        try:
            src_poly = Polygon(tuple(seed.path))
        except Exception:
            continue
        expanded = offset_polygon(src_poly, total_offset, min_area=1e-8)
        if expanded is None:
            continue
        boundary_poly = boundary_polys[seed.boundary]
        if not expanded.bounds.intersects(boundary_poly.bounds):
            continue
        if not boundary_poly.contains_point(expanded.centroid, include_boundary=True):
            # Cheap clipping guard: keep the expansion only when the source is in-bound.
            if not boundary_poly.contains_point(src_poly.centroid, include_boundary=True):
                continue
        out.append(
            RegionExpansion(
                polygon=expanded,
                src_id=int(seed.src),
                boundary_id=int(seed.boundary),
            )
        )
    return out


def propagate_waves_from_polygons(
    src: Sequence[Polygon | Island],
    boundary: Sequence[Polygon | Island],
    params: RegionExpansionParameters,
) -> list[RegionExpansion]:
    seeds = wave_seeds(src, boundary, params.tiny_expansion, sorted=True)
    return propagate_waves(seeds, boundary, params)


def merge_expansions_into_polygons(src: Iterable[Polygon], expanded: Iterable[RegionExpansion]) -> list[Polygon]:
    src_list = list(src)
    expansions = list(expanded)
    if not expansions:
        return src_list

    by_src: dict[int, Polygon] = {}
    for region in expansions:
        current = by_src.get(region.src_id)
        if current is None:
            by_src[region.src_id] = region.polygon
            continue
        merged_bounds = current.bounds.union(region.polygon.bounds)
        merged = Polygon.from_tuples(
            [
                (merged_bounds.min_x, merged_bounds.min_y),
                (merged_bounds.max_x, merged_bounds.min_y),
                (merged_bounds.max_x, merged_bounds.max_y),
                (merged_bounds.min_x, merged_bounds.max_y),
            ]
        )
        by_src[region.src_id] = merged

    out: list[Polygon] = []
    for index, poly in enumerate(src_list):
        out.append(by_src.get(index, poly))
    return out
