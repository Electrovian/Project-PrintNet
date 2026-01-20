import pytest

from slicer.gcode.writer import SliceSettings


@pytest.mark.parametrize(
    "min_h,max_h,layer,expected",
    [
        (0.1, 0.3, 0.05, 0.1),
        (0.1, 0.3, 0.1, 0.1),
        (0.1, 0.3, 0.2, 0.2),
        (0.1, 0.3, 0.35, 0.3),
        (0.2, 0.5, 0.6, 0.5),
        (0.2, 0.5, 0.1, 0.2),
    ],
)
def test_layer_height_clamped(min_h, max_h, layer, expected):
    settings = SliceSettings(min_layer_height=min_h, max_layer_height=max_h, layer_height=layer)
    assert settings.layer_height == pytest.approx(expected)


@pytest.mark.parametrize(
    "min_h,max_h,first_layer,expected",
    [
        (0.1, 0.3, 0.05, 0.1),
        (0.1, 0.3, 0.12, 0.12),
        (0.1, 0.3, 0.4, 0.3),
        (0.2, 0.5, 0.1, 0.2),
        (0.2, 0.5, 0.6, 0.5),
        (0.2, 0.5, 0.25, 0.25),
    ],
)
def test_first_layer_height_clamped(min_h, max_h, first_layer, expected):
    settings = SliceSettings(min_layer_height=min_h, max_layer_height=max_h,
                             first_layer_height=first_layer)
    assert settings.first_layer_height == pytest.approx(expected)


@pytest.mark.parametrize(
    "input_val,expected",
    [
        ("none", "none"),
        ("CONTOUR", "contour"),
        ("contour_hole", "contour_hole"),
        ("invalid", "none"),
        ("", "none"),
    ],
)
def test_scarf_joint_seam_normalized(input_val, expected):
    settings = SliceSettings(scarf_joint_seam=input_val)
    assert settings.scarf_joint_seam == expected


@pytest.mark.parametrize(
    "input_val,expected",
    [
        ("disabled", "disabled"),
        ("limited", "limited"),
        ("none", "none"),
        ("invalid", "disabled"),
        ("", "disabled"),
    ],
)
def test_bridge_filter_mode_normalized(input_val, expected):
    settings = SliceSettings(bridge_filter_mode=input_val)
    assert settings.bridge_filter_mode == expected


@pytest.mark.parametrize(
    "input_val,expected",
    [
        ("none", "none"),
        ("partial", "partial"),
        ("sacrificial", "sacrificial"),
        ("invalid", "none"),
        ("", "none"),
    ],
)
def test_bridge_counterbore_normalized(input_val, expected):
    settings = SliceSettings(bridge_counterbore_holes=input_val)
    assert settings.bridge_counterbore_holes == expected


@pytest.mark.parametrize(
    "input_val,expected",
    [
        ("classic", "classic"),
        ("ARACHNE", "arachne"),
        ("invalid", "classic"),
        ("", "classic"),
    ],
)
def test_wall_generator_normalized(input_val, expected):
    settings = SliceSettings(wall_generator=input_val)
    assert settings.wall_generator == expected


@pytest.mark.parametrize(
    "input_val,expected",
    [
        ("inner_outer", "inner_outer"),
        ("outer_inner", "outer_inner"),
        ("inner_outer_inner", "inner_outer_inner"),
        ("adaptive_outer_inner", "adaptive_outer_inner"),
        ("invalid", "inner_outer"),
    ],
)
def test_wall_printing_order_normalized(input_val, expected):
    settings = SliceSettings(wall_printing_order=input_val)
    assert settings.wall_printing_order == expected


@pytest.mark.parametrize(
    "input_val,expected",
    [
        ("auto", "auto"),
        ("clockwise", "clockwise"),
        ("counter_clockwise", "counter_clockwise"),
        ("invalid", "auto"),
    ],
)
def test_wall_loop_direction_normalized(input_val, expected):
    settings = SliceSettings(wall_loop_direction=input_val)
    assert settings.wall_loop_direction == expected


@pytest.mark.parametrize(
    "base_pattern,interface_pattern,expected_base,expected_interface",
    [
        ("rectilinear", "rectilinear", "rectilinear", "rectilinear"),
        ("grid", "triangle", "grid", "triangle"),
        ("triangle", "grid", "triangle", "grid"),
        ("invalid", "rectilinear", "rectilinear", "rectilinear"),
        ("grid", "invalid", "grid", "grid"),
        ("invalid", "invalid", "rectilinear", "rectilinear"),
    ],
)
def test_support_patterns_normalized(base_pattern, interface_pattern,
                                     expected_base, expected_interface):
    settings = SliceSettings(
        support_pattern=base_pattern,
        support_interface_pattern=interface_pattern,
    )
    assert settings.support_pattern == expected_base
    assert settings.support_interface_pattern == expected_interface


@pytest.mark.parametrize(
    "infill_percent,infill_density,expected",
    [
        (15.0, None, 0.15),
        (40.0, None, 0.4),
        (0.0, None, 0.0),
        (50.0, 0.2, 0.2),
    ],
)
def test_infill_density_defaults(infill_percent, infill_density, expected):
    settings = SliceSettings(infill_percent=infill_percent, infill_density=infill_density)
    assert settings.infill_density == pytest.approx(expected)


@pytest.mark.parametrize(
    "spacing,speed,interface_speed,expected_spacing,expected_speed,expected_interface",
    [
        (2.0, 60.0, 50.0, 2.0, 60.0, 50.0),
        (0.05, 0.5, 0.5, 0.1, 1.0, 1.0),
        (-1.0, -10.0, -3.0, 0.1, 1.0, 1.0),
        (5.5, 120.0, 80.0, 5.5, 120.0, 80.0),
        (0.2, 1.0, 1.0, 0.2, 1.0, 1.0),
        (0.15, 10.0, 5.0, 0.15, 10.0, 5.0),
    ],
)
def test_support_spacing_speed_clamps(spacing, speed, interface_speed,
                                      expected_spacing, expected_speed, expected_interface):
    settings = SliceSettings(
        support_spacing=spacing,
        support_speed=speed,
        support_interface_speed=interface_speed,
    )
    assert settings.support_spacing == pytest.approx(expected_spacing)
    assert settings.support_speed == pytest.approx(expected_speed)
    assert settings.support_interface_speed == pytest.approx(expected_interface)


@pytest.mark.parametrize(
    "angle,merge,expected_angle,expected_merge",
    [
        (45.0, 2.0, 45.0, 2.0),
        (-10.0, 0.05, 0.0, 0.1),
        (100.0, -3.0, 85.0, 0.1),
        (0.0, 5.0, 0.0, 5.0),
        (85.0, 0.1, 85.0, 0.1),
        (84.9, 9.0, 84.9, 9.0),
    ],
)
def test_tree_support_clamps(angle, merge, expected_angle, expected_merge):
    settings = SliceSettings(tree_branch_angle=angle, tree_merge_distance=merge)
    assert settings.tree_branch_angle == pytest.approx(expected_angle)
    assert settings.tree_merge_distance == pytest.approx(expected_merge)


@pytest.mark.parametrize(
    "ironing_type,ironing_enabled,expected_type,expected_enabled",
    [
        ("no_ironing", True, "all_top_surfaces", True),
        ("no_ironing", False, "no_ironing", False),
        ("all_top_surfaces", True, "all_top_surfaces", True),
        ("invalid", True, "all_top_surfaces", True),
    ],
)
def test_ironing_type_enforced(ironing_type, ironing_enabled, expected_type, expected_enabled):
    settings = SliceSettings(ironing_type=ironing_type, ironing_enabled=ironing_enabled)
    assert settings.ironing_type == expected_type
    assert settings.ironing_enabled == expected_enabled
