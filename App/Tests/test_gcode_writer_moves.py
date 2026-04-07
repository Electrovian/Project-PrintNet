from slicer_v2.legacy_gcode_writer import GCodeWriter, SliceSettings, _normalize_gcode_lines


def test_normalize_gcode_lines_from_string():
    text = "G28\n\n;comment\nG1 X0 Y0\n"
    assert _normalize_gcode_lines(text) == ["G28", ";comment", "G1 X0 Y0"]


def test_normalize_gcode_lines_from_list():
    lines = ["G28", None, "  ", "G1 X0"]
    assert _normalize_gcode_lines(lines) == ["G28", "G1 X0"]


def test_move_extrude_updates_position_and_e():
    settings = SliceSettings(retract_distance=1.0, retract_speed=25.0)
    writer = GCodeWriter(settings=settings)
    writer.move_extrude(10, 0, 0.2, 30.0, extrusion=0.5)
    assert writer.position == (10, 0, 0.2)
    assert writer.e_position == 0.5
    assert writer.has_extruded


def test_move_travel_retracts_after_extrude():
    settings = SliceSettings(retract_distance=1.0, retract_speed=25.0)
    writer = GCodeWriter(settings=settings)
    writer.move_extrude(0, 0, 0.2, 30.0, extrusion=0.5)
    writer.move_travel(10, 0, 0.2, 120.0)
    assert any(line.startswith("G1 E") for line in writer.lines)
    assert writer.lines[-1].startswith("G0")
    assert "X120" in writer.lines[-1]


def test_duplicate_extrusion_skips_e_increment():
    settings = SliceSettings(dedupe_extrusion_paths=True, retract_distance=0.0)
    writer = GCodeWriter(settings=settings)
    writer.move_extrude(10, 0, 0.2, 30.0, extrusion=0.5)
    e_after_first = writer.e_position
    writer.move_travel(0, 0, 0.2, 120.0)
    writer.move_extrude(10, 0, 0.2, 30.0, extrusion=0.5)
    assert writer.e_position == e_after_first


def test_move_travel_no_retract_when_not_extruded():
    settings = SliceSettings(retract_distance=1.0, retract_speed=25.0)
    writer = GCodeWriter(settings=settings)
    writer.move_travel(5, 0, 0.2, 120.0)
    assert not any(line.startswith("G1 E") for line in writer.lines)


def test_move_arc_extrude_clockwise_uses_g2():
    settings = SliceSettings(retract_distance=0.5)
    writer = GCodeWriter(settings=settings)
    writer.move_arc_extrude(10, 0, 0.2, 20.0, extrusion=0.2, center_xy=(5, 0), clockwise=True)
    assert any(line.startswith("G2 ") for line in writer.lines)


def test_move_arc_extrude_counter_clockwise_uses_g3():
    settings = SliceSettings(retract_distance=0.5)
    writer = GCodeWriter(settings=settings)
    writer.move_arc_extrude(10, 0, 0.2, 20.0, extrusion=0.2, center_xy=(5, 0), clockwise=False)
    assert any(line.startswith("G3 ") for line in writer.lines)


def test_firmware_retract_unretract():
    settings = SliceSettings(retract_style="firmware", retract_distance=1.0)
    writer = GCodeWriter(settings=settings)
    writer.retract()
    writer.unretract()
    assert "G10" in writer.lines
    assert "G11" in writer.lines


def test_retract_noop_when_distance_zero():
    settings = SliceSettings(retract_distance=0.0, retract_speed=25.0)
    writer = GCodeWriter(settings=settings)
    writer.retract()
    assert writer.lines == []


def test_move_extrude_translates_centered_coordinates_to_bed_space():
    settings = SliceSettings(retract_distance=0.0, bed_x=300.0, bed_y=280.0)
    writer = GCodeWriter(settings=settings)
    writer.move_extrude(10, 5, 0.2, 30.0, extrusion=0.5)
    assert any(line.startswith("G1 X160 Y145") for line in writer.lines)


def test_header_footer_use_shared_contract_and_remove_demo_footer():
    settings = SliceSettings(
        start_gcode=["M117 START"],
        end_gcode=["END_PRINT"],
        retract_distance=0.0,
    )
    writer = GCodeWriter(settings=settings)
    writer.write_header()
    writer.write_footer()
    gcode = writer.get_gcode()
    assert "demo" not in gcode.lower()
    assert "M117 START" in gcode
    assert "M82 ; absolute extrusion" in gcode
    assert gcode.rstrip().endswith("END_PRINT")
    assert "M104 S0" not in writer.lines
    assert "M140 S0" not in writer.lines
    assert "M84" not in writer.lines


def test_klipper_defaults_to_relative_extrusion_when_unset():
    settings = SliceSettings(
        firmware_flavor="klipper",
        gcode_absolute_extrusion=None,
        retract_distance=1.0,
        retract_speed=25.0,
    )
    writer = GCodeWriter(settings=settings)
    writer.write_header()
    writer.move_extrude(5, 5, 0.2, 30.0, extrusion=0.5)
    writer.move_travel(10, 5, 0.2, 120.0)
    assert "M83 ; relative extrusion" in writer.lines
    assert any("E-1" in line and line.endswith("; retract") for line in writer.lines)

