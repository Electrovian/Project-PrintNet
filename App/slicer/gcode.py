from dataclasses import dataclass, field
from typing import List, Iterable, Tuple

@dataclass
class SliceSettings:
    layer_height: float = 0.2
    infill_percent: float = 15.0
    print_speed: float = 60.0  # mm/s
    travel_speed: float = 150.0  # mm/s
    nozzle_diameter: float = 0.4
    filament_diameter: float = 1.75

@dataclass
class GCodeWriter:
    settings: SliceSettings
    lines: List[str] = field(default_factory=list)
    e_position: float = 0.0

    def add(self, line: str):
        self.lines.append(line)

    def write_header(self):
        self.add("; OpenSlicer demo G-code")
        self.add("G90 ; absolute positioning")
        self.add("M82 ; absolute extrusion")
        self.add("G28 ; home all axes")
        self.add("")

    def write_footer(self):
        self.add("M104 S0 ; hotend off")
        self.add("M140 S0 ; bed off")
        self.add("G28 X0 Y0 ; home XY")
        self.add("M84 ; disable motors")
        self.add("; End of OpenSlicer demo")

    def move_travel(self, x: float, y: float, z: float, f: float):
        self.add(f"G0 X{x:.3f} Y{y:.3f} Z{z:.3f} F{f * 60:.0f}")

    def move_extrude(self, x: float, y: float, z: float, speed: float, extrusion: float):
        self.e_position += extrusion
        self.add(f"G1 X{x:.3f} Y{y:.3f} Z{z:.3f} E{self.e_position:.5f} F{speed * 60:.0f}")

    def perimeter_loop(self, points: Iterable[Tuple[float, float]], z: float, speed: float):
        pts = list(points)
        if not pts:
            return
        x0, y0 = pts[0]
        self.move_travel(x0, y0, z, self.settings.travel_speed)
        for x, y in pts[1:]:
            # Super naive extrusion: fixed amount per segment.
            self.move_extrude(x, y, z, speed, extrusion=0.02)

    def get_gcode(self) -> str:
        return "\n".join(self.lines)
