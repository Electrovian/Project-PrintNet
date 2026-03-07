from __future__ import annotations

from dataclasses import asdict
from typing import Any, Mapping

from .base import ConnectorCapabilities, PrinterConnector
from .bambu_lan import BambuLanConnector
from .creality import CrealityConnector
from .errors import InvalidPrinterConfigError, UnsupportedConnectorError
from .legacy_octoprint import LegacyOctoPrintConnector
from .local_file import LocalFileConnector
from .moonraker import MoonrakerConnector
from .octoprint import OctoPrintConnector
from .prusalink import PrusaLinkConnector


def _normalize_connector_type(value: object) -> str:
    return str(value or "").strip().lower().replace("-", "_")


class ConnectorRegistry:
    """Runtime registry for connector implementations."""

    def __init__(self):
        self._connectors: dict[str, PrinterConnector] = {}

    def register(self, connector: PrinterConnector) -> None:
        key = _normalize_connector_type(getattr(connector, "connector_type", ""))
        if not key:
            raise InvalidPrinterConfigError("CONNECTOR_TYPE_INVALID: empty connector type.")
        self._connectors[key] = connector

    def connector_types(self) -> list[str]:
        return sorted(self._connectors.keys())

    def descriptors(self) -> list[dict[str, Any]]:
        payload: list[dict[str, Any]] = []
        for key in self.connector_types():
            capabilities: ConnectorCapabilities = self._connectors[key].capabilities
            item = asdict(capabilities)
            item["connector_type"] = key
            payload.append(item)
        return payload

    def get(self, connector_type: str) -> PrinterConnector:
        key = _normalize_connector_type(connector_type)
        connector = self._connectors.get(key)
        if connector is None:
            supported = ", ".join(self.connector_types()) or "none"
            raise UnsupportedConnectorError(
                f"CONNECTOR_UNSUPPORTED: {connector_type!r}. Supported connectors: {supported}."
            )
        return connector

    def _infer_connector_type(self, printer: Mapping[str, Any]) -> str:
        explicit = _normalize_connector_type(
            printer.get("connector_type") or printer.get("connector") or printer.get("protocol")
        )
        if explicit:
            return explicit
        prusalink_url = str(printer.get("prusalink_url", "") or printer.get("prusa_url", "")).strip()
        if prusalink_url:
            return "prusalink"
        moonraker_url = str(printer.get("moonraker_url", "") or printer.get("klipper_url", "")).strip()
        if moonraker_url:
            return "moonraker"
        bambu_url = str(printer.get("bambu_url", "") or printer.get("bambu_host", "")).strip()
        if bambu_url:
            return "bambu_lan"
        creality_url = str(printer.get("creality_url", "") or printer.get("creality_host", "")).strip()
        creality_protocol = str(printer.get("creality_protocol", "")).strip()
        if creality_url or creality_protocol:
            return "creality"
        octo_url = str(printer.get("octoprint_url", "")).strip()
        if octo_url or "octoprint_api_key" in printer:
            return "octoprint"
        return "local_file"

    def resolve(self, printer: Mapping[str, Any] | None) -> PrinterConnector:
        if printer is None or not isinstance(printer, Mapping):
            raise InvalidPrinterConfigError("PRINTER_CONFIG_INVALID: expected mapping for connector resolution.")
        connector_type = self._infer_connector_type(printer)
        return self.get(connector_type)


def build_default_connector_registry() -> ConnectorRegistry:
    registry = ConnectorRegistry()
    registry.register(LocalFileConnector())
    registry.register(PrusaLinkConnector())
    registry.register(MoonrakerConnector())
    registry.register(OctoPrintConnector())
    registry.register(LegacyOctoPrintConnector())
    registry.register(BambuLanConnector())
    registry.register(CrealityConnector())
    return registry
