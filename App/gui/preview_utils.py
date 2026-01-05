from __future__ import annotations

def play_interval_ms(base_ms: int, speed: float, min_ms: int = 8, max_ms: int = 250) -> int:
    base = max(1, int(base_ms))
    try:
        speed_val = float(speed)
    except (TypeError, ValueError):
        speed_val = 1.0
    if speed_val <= 0:
        speed_val = 1.0
    interval = int(round(base / speed_val))
    return max(min_ms, min(max_ms, interval))
