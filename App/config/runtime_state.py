from __future__ import annotations

from typing import Any, Mapping

from .defaults import DEFAULTS
from .runtime_printer_state import (
    RuntimePrinterState,
    runtime_printer_state_from_defaults,
    runtime_printer_state_from_profile,
)


def default_runtime_printer_state() -> RuntimePrinterState:
    return runtime_printer_state_from_defaults(DEFAULTS.get("printer", {}))


def resolve_state_from_profile(
    profile: Mapping[str, Any] | None,
    *,
    current_state: RuntimePrinterState | None = None,
    defaults: Mapping[str, Any] | None = None,
) -> RuntimePrinterState:
    if current_state is None:
        defaults_payload = defaults if defaults is not None else DEFAULTS.get("printer", {})
        current_state = runtime_printer_state_from_defaults(defaults_payload)
    return runtime_printer_state_from_profile(
        profile,
        fallback_state=current_state,
        source="runtime",
    )


def bed_limits_for_state(state: RuntimePrinterState) -> tuple[tuple[float, float], float]:
    return (state.bed_size, float(state.bed_z))


__all__ = [
    "RuntimePrinterState",
    "bed_limits_for_state",
    "default_runtime_printer_state",
    "resolve_state_from_profile",
]
