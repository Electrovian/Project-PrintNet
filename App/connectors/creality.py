from __future__ import annotations

from typing import Any, Mapping, cast

from .base import ConnectorCapabilities, PrinterConnector
from .errors import InvalidPrinterConfigError
from .moonraker import MoonrakerConnector
from .octoprint import OctoPrintConnector
from .prusalink import PrusaLinkConnector


class CrealityConnector(PrinterConnector):
    """Creality adapter that routes to supported LAN protocols."""

    def __init__(self):
        self._capabilities = ConnectorCapabilities(
            connector_type="creality",
            display_name="Creality",
            protocol="adapter",
            supports_connect=True,
            supports_upload=True,
            supports_start=True,
            supports_pause=True,
            supports_resume=True,
            supports_cancel=True,
            supports_status=True,
        )
        self._moonraker = MoonrakerConnector()
        self._octoprint = OctoPrintConnector()
        self._prusalink = PrusaLinkConnector()

    @property
    def capabilities(self) -> ConnectorCapabilities:
        return self._capabilities

    def validate_printer(self, printer: Mapping[str, Any] | None) -> None:
        super().validate_printer(printer)
        if printer is None:
            raise InvalidPrinterConfigError("PRINTER_CONFIG_INVALID: expected mapping.")
        printer_map = cast(Mapping[str, Any], printer)
        if "name" not in printer_map:
            raise InvalidPrinterConfigError("PRINTER_NAME_REQUIRED: printer.name missing.")

    def _base_url(self, printer: Mapping[str, Any]) -> str:
        value = str(printer.get("creality_url", "") or printer.get("endpoint", "")).strip()
        if value:
            return value.rstrip("/")
        for key in ("moonraker_url", "octoprint_url", "prusalink_url"):
            alt = str(printer.get(key, "")).strip()
            if alt:
                return alt.rstrip("/")
        host = str(printer.get("host", "")).strip()
        port = int(printer.get("port", 0) or 0)
        if host and port > 0:
            return f"http://{host}:{port}"
        raise InvalidPrinterConfigError("CREALITY_URL_REQUIRED: creality_url/endpoint is required.")

    def _resolve_protocol(self, printer: Mapping[str, Any]) -> str:
        explicit = str(printer.get("creality_protocol", "") or printer.get("protocol", "")).strip().lower()
        if explicit:
            if explicit in ("moonraker", "klipper", "fluidd", "mainsail", "k1", "k1c", "k1max"):
                return "moonraker"
            if explicit in ("octoprint", "octopi", "creality_cloud"):
                return "octoprint"
            if explicit in ("prusalink",):
                return "prusalink"
        if str(printer.get("moonraker_url", "")).strip():
            return "moonraker"
        if str(printer.get("octoprint_url", "")).strip():
            return "octoprint"
        if str(printer.get("prusalink_url", "")).strip():
            return "prusalink"
        return "moonraker"

    def _map_printer(self, printer: Mapping[str, Any], protocol: str) -> Mapping[str, Any]:
        base_url = self._base_url(printer)
        token = str(
            printer.get("creality_token", "")
            or printer.get("creality_api_key", "")
            or printer.get("api_key", "")
            or ""
        ).strip()
        mapped = dict(printer)
        if protocol == "moonraker":
            mapped.setdefault("moonraker_url", base_url)
            mapped.setdefault("moonraker_token", token)
            return mapped
        if protocol == "octoprint":
            mapped.setdefault("octoprint_url", base_url)
            mapped.setdefault("octoprint_api_key", token)
            return mapped
        if protocol == "prusalink":
            mapped.setdefault("prusalink_url", base_url)
            mapped.setdefault("prusalink_api_key", token)
            return mapped
        raise InvalidPrinterConfigError(f"CREALITY_PROTOCOL_UNSUPPORTED: {protocol}")

    def _delegate(self, protocol: str) -> PrinterConnector:
        if protocol == "moonraker":
            return self._moonraker
        if protocol == "octoprint":
            return self._octoprint
        if protocol == "prusalink":
            return self._prusalink
        raise InvalidPrinterConfigError(f"CREALITY_PROTOCOL_UNSUPPORTED: {protocol}")

    def _route(self, printer: Mapping[str, Any]) -> tuple[PrinterConnector, Mapping[str, Any]]:
        self.validate_printer(printer)
        protocol = self._resolve_protocol(printer)
        mapped = self._map_printer(printer, protocol)
        return self._delegate(protocol), mapped

    def connect(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        delegate, mapped = self._route(printer)
        payload = dict(delegate.connect(mapped))
        payload.setdefault("adapter", "creality")
        payload.setdefault("protocol", delegate.connector_type)
        return payload

    def upload(self, printer: Mapping[str, Any], gcode_path: str) -> dict[str, Any]:
        delegate, mapped = self._route(printer)
        payload = dict(delegate.upload(mapped, gcode_path))
        payload.setdefault("adapter", "creality")
        payload.setdefault("protocol", delegate.connector_type)
        return payload

    def start_print(
        self,
        printer: Mapping[str, Any],
        *,
        remote_path: str | None = None,
        gcode_path: str | None = None,
    ) -> dict[str, Any]:
        delegate, mapped = self._route(printer)
        payload = dict(delegate.start_print(mapped, remote_path=remote_path, gcode_path=gcode_path))
        payload.setdefault("adapter", "creality")
        payload.setdefault("protocol", delegate.connector_type)
        return payload

    def pause(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        delegate, mapped = self._route(printer)
        return dict(delegate.pause(mapped))

    def resume(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        delegate, mapped = self._route(printer)
        return dict(delegate.resume(mapped))

    def cancel(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        delegate, mapped = self._route(printer)
        return dict(delegate.cancel(mapped))

    def status(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        delegate, mapped = self._route(printer)
        payload = dict(delegate.status(mapped))
        payload.setdefault("adapter", "creality")
        payload.setdefault("protocol", delegate.connector_type)
        return payload
