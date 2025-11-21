"""Geometric helper utilities.

For now this is intentionally tiny. As you extend the slicer, this is
where you can put plane/triangle intersections, polygon offset
operations, etc.
"""

from typing import Tuple

def compute_bounding_square(bounds: Tuple[Tuple[float, float, float], Tuple[float, float, float]]):
    """Return a simple XY square that covers the mesh bounds.

    Args:
        bounds: ((minx, miny, minz), (maxx, maxy, maxz))

    Returns:
        List of (x, y) points in order around the square.
    """
    (minx, miny, _), (maxx, maxy, _) = bounds
    return [
        (minx, miny),
        (maxx, miny),
        (maxx, maxy),
        (minx, maxy),
        (minx, miny),
    ]
