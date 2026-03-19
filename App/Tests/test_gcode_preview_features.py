import pytest

from slicer_v2.legacy_gcode_preview import parse_gcode_preview


BASE_FEATURE_CASES = [
    ("WALL-OUTER", "outer_wall"),
    ("WALL-INNER", "inner_wall"),
    ("PERIMETER-OUTER", "outer_wall"),
    ("PERIMETER-INNER", "inner_wall"),
    ("PERIMETER", "outer_wall"),
    ("TOP", "top_surface"),
    ("TOP-SKIN", "top_surface"),
    ("SKIN", "top_surface"),
    ("BOTTOM", "bottom_surface"),
    ("BOTTOM-SURFACE", "bottom_surface"),
    ("BRIDGE", "bridge"),
    ("BRIDGE-INFILL", "bridge"),
    ("GAP", "gap_infill"),
    ("GAP-FILL", "gap_infill"),
    ("THIN", "thin_wall"),
    ("THIN-WALL", "thin_wall"),
    ("IRONING", "ironing"),
    ("SKIRT", "skirt"),
    ("BRIM", "brim"),
    ("RAFT", "raft"),
    ("SUPPORT", "support"),
    ("SUPPORT_INTERFACE", "support"),
    ("SUPPORT-BASE", "support"),
    ("SOLID-INFILL", "solid_infill"),
    ("SOLID", "solid_infill"),
    ("INFILL", "sparse_infill"),
    ("FILL", "sparse_infill"),
    ("INFILL-GRID", "sparse_infill"),
    ("RETRACT", "retract"),
    ("TRAVEL", "travel"),
]


@pytest.mark.parametrize(
    "prefix,token,expected",
    [(prefix, token, expected) for prefix in ("TYPE", "FEATURE") for token, expected in BASE_FEATURE_CASES],
)
def test_feature_mapping(prefix, token, expected):
    lines = [
        f";{prefix}:{token}",
        "G1 X0 Y0 Z0.2 F1200",
        "G1 X10 Y0 E0.5",
    ]
    preview = parse_gcode_preview(lines)
    assert preview.layers
    assert preview.layers[0].segments
    assert preview.layers[0].segments[-1].feature == expected

