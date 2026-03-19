import pytest
import trimesh

from slicer_v2.legacy_ai_checks import _check_mesh, _check_settings, _merge_reports, run_ai_checks, AiCheckReport
from slicer_v2.legacy_gcode_writer import SliceSettings


def test_merge_reports_deduplicates():
    reports = [
        AiCheckReport(warnings=["A", "B"], suggestions=["S1"]),
        AiCheckReport(warnings=["B", "C"], suggestions=["S1", "S2"]),
    ]
    merged = _merge_reports(reports)
    assert merged.warnings == ["A", "B", "C"]
    assert merged.suggestions == ["S1", "S2"]


@pytest.mark.parametrize(
    "layer_height,expected",
    [
        (0.6, "Layer height is high for the nozzle size; reduce for better quality."),
        (0.02, "Layer height is very low; increase for faster prints."),
    ],
)
def test_check_settings_layer_height_suggestions(layer_height, expected):
    settings = SliceSettings(
        layer_height=layer_height,
        nozzle_diameter=0.4,
        min_layer_height=0.01,
    )
    report = _check_settings(settings)
    assert expected in report.suggestions


@pytest.mark.parametrize(
    "print_speed,expected",
    [
        (150.0, "High print speed detected; reduce for better surface quality."),
    ],
)
def test_check_settings_speed_suggestion(print_speed, expected):
    settings = SliceSettings(print_speed=print_speed)
    report = _check_settings(settings)
    assert expected in report.suggestions


@pytest.mark.parametrize(
    "infill_density,expected",
    [
        (0.05, "Low infill density may weaken parts; increase for stronger prints."),
    ],
)
def test_check_settings_infill_suggestion(infill_density, expected):
    settings = SliceSettings(infill_density=infill_density)
    report = _check_settings(settings)
    assert expected in report.suggestions


def test_check_mesh_overhang_warning_when_supports_disabled():
    mesh = trimesh.creation.box(extents=(10, 10, 2))
    settings = SliceSettings(overhang_angle=45.0, support_enabled=False)
    report = _check_mesh(mesh, settings)
    assert "Overhangs detected with supports disabled; enable supports or adjust angle." in report.warnings


def test_check_mesh_overhang_no_warning_when_supports_enabled():
    mesh = trimesh.creation.box(extents=(10, 10, 2))
    settings = SliceSettings(overhang_angle=45.0, support_enabled=True)
    report = _check_mesh(mesh, settings)
    assert "Overhangs detected with supports disabled; enable supports or adjust angle." not in report.warnings


def test_run_ai_checks_merges_settings_and_mesh_reports():
    mesh = trimesh.creation.box(extents=(1, 1, 1))
    settings = SliceSettings(print_speed=150.0, support_enabled=False)
    report = run_ai_checks([mesh], settings)
    assert "High print speed detected; reduce for better surface quality." in report.suggestions
    assert "Overhangs detected with supports disabled; enable supports or adjust angle." in report.warnings

