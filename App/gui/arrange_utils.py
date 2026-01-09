from __future__ import annotations

import math
from typing import Dict, List, Sequence, Tuple


def spacing_with_base(base_spacing: float, extra_spacing: float) -> float:
    base_val = max(0.0, float(base_spacing))
    extra_val = max(0.0, float(extra_spacing))
    return base_val + extra_val


def spacing_candidates(extra_spacing: float, step: float = 0.5) -> List[float]:
    extra_val = max(0.0, float(extra_spacing))
    step_val = max(0.1, float(step))
    if extra_val <= 0.0:
        return [0.0]
    values = [extra_val]
    steps = int(math.floor(extra_val / step_val))
    for i in range(1, steps + 1):
        val = round(extra_val - i * step_val, 4)
        if val <= 0.0:
            val = 0.0
        if val not in values:
            values.append(val)
    if 0.0 not in values:
        values.append(0.0)
    return values


def positions_fit(
    positions: Dict[int, Tuple[float, float]],
    sizes: Sequence[Tuple[int, float, float]],
    bed_bounds: Tuple[float, float, float, float],
) -> bool:
    if not sizes:
        return True
    size_map = {mid: (float(w), float(d)) for mid, w, d in sizes}
    min_x, max_x, min_y, max_y = bed_bounds
    for mid, (x, y) in positions.items():
        if mid not in size_map:
            return False
        w, d = size_map[mid]
        if (x - w / 2.0) < min_x or (x + w / 2.0) > max_x:
            return False
        if (y - d / 2.0) < min_y or (y + d / 2.0) > max_y:
            return False
    return len(positions) == len(size_map)
