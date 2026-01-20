from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, List, Sequence

import trimesh

from .gcode.writer import SliceSettings


@dataclass
class AiCheckReport:
    warnings: List[str]
    suggestions: List[str]


def _merge_reports(reports: Iterable[AiCheckReport]) -> AiCheckReport:
    warnings: List[str] = []
    suggestions: List[str] = []
    for report in reports:
        for entry in report.warnings:
            if entry not in warnings:
                warnings.append(entry)
        for entry in report.suggestions:
            if entry not in suggestions:
                suggestions.append(entry)
    return AiCheckReport(warnings=warnings, suggestions=suggestions)


def _check_mesh(mesh: trimesh.Trimesh, settings: SliceSettings) -> AiCheckReport:
    warnings: List[str] = []
    suggestions: List[str] = []

    if mesh.faces.shape[0] >= 250000:
        suggestions.append("High triangle count detected. Simplify the model for faster slicing.")
    if not mesh.is_watertight:
        warnings.append("Model is not watertight; holes or non-manifold edges may cause defects.")
    if not mesh.is_winding_consistent:
        warnings.append("Model has inconsistent normals; repair or re-export for best results.")

    extents = mesh.extents
    if extents is not None and len(extents) >= 3:
        min_span = float(min(extents))
        nozzle = max(0.1, float(settings.nozzle_diameter))
        if min_span < nozzle * 0.6:
            warnings.append("Thin features detected; increase wall count or scale the model.")

    normals = mesh.face_normals
    cos_limit = math.cos(math.radians(float(settings.overhang_angle)))
    overhang_faces = (normals[:, 2] < cos_limit) & (normals[:, 2] < 0.0)
    if overhang_faces.any() and not settings.support_enabled:
        warnings.append("Overhangs detected with supports disabled; enable supports or adjust angle.")

    return AiCheckReport(warnings=warnings, suggestions=suggestions)


def _check_settings(settings: SliceSettings) -> AiCheckReport:
    warnings: List[str] = []
    suggestions: List[str] = []

    nozzle = max(0.1, float(settings.nozzle_diameter))
    if settings.layer_height > nozzle * 0.7:
        suggestions.append("Layer height is high for the nozzle size; reduce for better quality.")
    if settings.layer_height < nozzle * 0.1:
        suggestions.append("Layer height is very low; increase for faster prints.")
    if settings.print_speed > 120:
        suggestions.append("High print speed detected; reduce for better surface quality.")
    if settings.infill_density is not None and settings.infill_density < 0.08:
        suggestions.append("Low infill density may weaken parts; increase for stronger prints.")

    return AiCheckReport(warnings=warnings, suggestions=suggestions)


def run_ai_checks(meshes: Sequence[trimesh.Trimesh],
                  settings: SliceSettings) -> AiCheckReport:
    reports: List[AiCheckReport] = [_check_settings(settings)]
    for mesh in meshes:
        reports.append(_check_mesh(mesh, settings))
    return _merge_reports(reports)
