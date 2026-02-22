from __future__ import annotations

from typing import Any, Iterable


def _normalized_text(value: Any) -> str:
    return str(value or "").strip().lower()


def connector_name(printer: dict[str, Any] | None) -> str:
    if not isinstance(printer, dict):
        return ""
    connector = _normalized_text(printer.get("connector_type"))
    if connector:
        return connector
    protocol = _normalized_text(printer.get("protocol"))
    if protocol:
        return protocol
    if printer.get("moonraker_url"):
        return "moonraker"
    if printer.get("prusalink_url"):
        return "prusalink"
    if printer.get("octoprint_url"):
        return "octoprint"
    return ""


def connector_endpoint(printer: dict[str, Any] | None) -> str:
    if not isinstance(printer, dict):
        return ""
    connector = connector_name(printer)
    if connector == "moonraker":
        return str(printer.get("moonraker_url", "") or "").strip()
    if connector == "prusalink":
        return str(printer.get("prusalink_url", "") or "").strip()
    if connector == "octoprint":
        return str(printer.get("octoprint_url", "") or "").strip()
    return ""


def printer_identity(printer: dict[str, Any] | None) -> tuple[str, str, str]:
    if not isinstance(printer, dict):
        return "", "", ""
    name = _normalized_text(printer.get("name"))
    connector = connector_name(printer)
    endpoint = _normalized_text(connector_endpoint(printer))
    return name, connector, endpoint


def find_printer_index(
    printers: Iterable[dict[str, Any]],
    target: dict[str, Any] | None,
) -> int | None:
    target_name, target_connector, target_endpoint = printer_identity(target)
    if not target_name:
        return None

    fallback_name_index: int | None = None
    for index, printer in enumerate(printers):
        name, connector, endpoint = printer_identity(printer)
        if name != target_name:
            continue
        if fallback_name_index is None:
            fallback_name_index = index
        if connector == target_connector and endpoint == target_endpoint:
            return index
    return fallback_name_index


def sync_printer_selection(
    printer: dict[str, Any] | None,
    source: str | None,
    settings_view: Any = None,
    device_view: Any = None,
    control_view: Any = None,
    preview_view: Any = None,
) -> None:
    if not isinstance(printer, dict):
        return
    name = _normalized_text(printer.get("name"))
    if not name:
        return

    def _select(view: Any):
        if view is None:
            return
        if hasattr(view, "select_printer"):
            view.select_printer(printer, emit=False)
            return
        if hasattr(view, "select_printer_by_name"):
            view.select_printer_by_name(name, emit=False)

    if source != "settings":
        _select(settings_view)
    if source != "device":
        _select(device_view)
    if source != "control":
        _select(control_view)
    if source != "preview":
        _select(preview_view)
