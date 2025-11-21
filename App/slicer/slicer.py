from pathlib import Path
from typing import Optional

from .mesh import MeshModel
from .geometry import compute_bounding_square
from .gcode import GCodeWriter, SliceSettings

def slice_file(stl_path: str, output_gcode_path: Optional[str] = None,
               settings: Optional[SliceSettings] = None) -> str:
    """Very small demo slicer.

    Loads an STL, finds its XY bounding box, and emits a single square
    perimeter at Z = layer_height.

    Args:
        stl_path: Path to STL file.
        output_gcode_path: Where to write G-code. If None, uses same
            name with .gcode extension next to the STL.
        settings: SliceSettings instance.

    Returns:
        Path to generated G-code file.
    """
    stl_path = str(stl_path)
    mesh = MeshModel.from_file(stl_path)
    if settings is None:
        settings = SliceSettings()

    bounds = mesh.bounds
    square = compute_bounding_square(bounds)

    writer = GCodeWriter(settings=settings)
    writer.write_header()
    z = settings.layer_height
    writer.perimeter_loop(square, z=z, speed=settings.print_speed)
    writer.write_footer()

    if output_gcode_path is None:
        output_gcode_path = str(Path(stl_path).with_suffix(".gcode"))

    with open(output_gcode_path, "w", encoding="utf-8") as f:
        f.write(writer.get_gcode())

    return output_gcode_path
