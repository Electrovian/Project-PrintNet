from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import math
from typing import Any, Mapping


MIN_BED_MM = 1.0
MAX_BED_MM = 10000.0


@dataclass(frozen=True)
class RuntimePrinterState:
    name: str
    bed_x: float
    bed_y: float
    bed_z: float
    source: str = "defaults"
    updated_at_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def bed_size(self) -> tuple[float, float]:
        return (float(self.bed_x), float(self.bed_y))

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["bed_size"] = self.bed_size
        return payload


def _to_float(value: object, fallback: float) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return float(fallback)
    if not math.isfinite(parsed):
        return float(fallback)
    if parsed < MIN_BED_MM:
        return float(fallback)
    if parsed > MAX_BED_MM:
        return float(MAX_BED_MM)
    return float(parsed)


def _resolve_name(value: object, fallback: str) -> str:
    text = str(value or "").strip()
    if text:
        return text
    return str(fallback or "Printer").strip() or "Printer"


def runtime_printer_state_from_defaults(printer_defaults: Mapping[str, Any] | None) -> RuntimePrinterState:
    defaults = printer_defaults or {}
    bed_defaults = defaults.get("bed_size", (200.0, 200.0))
    if not isinstance(bed_defaults, (list, tuple)) or len(bed_defaults) < 2:
        bed_defaults = (200.0, 200.0)
    bed_x = _to_float(bed_defaults[0], 200.0)
    bed_y = _to_float(bed_defaults[1], 200.0)
    bed_z = _to_float(defaults.get("max_height", 200.0), 200.0)
    name = _resolve_name(defaults.get("name", "Printer"), "Printer")
    return RuntimePrinterState(
        name=name,
        bed_x=bed_x,
        bed_y=bed_y,
        bed_z=bed_z,
        source="defaults",
    )


def runtime_printer_state_from_profile(
    printer: Mapping[str, Any] | None,
    *,
    fallback_state: RuntimePrinterState,
    source: str = "runtime",
) -> RuntimePrinterState:
    if printer is None:
        return RuntimePrinterState(
            name=fallback_state.name,
            bed_x=fallback_state.bed_x,
            bed_y=fallback_state.bed_y,
            bed_z=fallback_state.bed_z,
            source=source,
        )
    name = _resolve_name(printer.get("name"), fallback_state.name)
    bed_x = _to_float(printer.get("bed_x"), fallback_state.bed_x)
    bed_y = _to_float(printer.get("bed_y"), fallback_state.bed_y)
    bed_z = _to_float(printer.get("bed_z"), fallback_state.bed_z)
    return RuntimePrinterState(
        name=name,
        bed_x=bed_x,
        bed_y=bed_y,
        bed_z=bed_z,
        source=source,
    )
