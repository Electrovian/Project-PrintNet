from slicer.gcode.writer import GCodeWriter, SliceSettings, _normalize_gcode_lines


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
    assert "X10" in writer.lines[-1]


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
