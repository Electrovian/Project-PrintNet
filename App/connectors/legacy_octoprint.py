from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from integrations.octoprint_api import upload_and_print

from .base import ConnectorCapabilities, PrinterConnector
from .errors import ConnectorOperationError, InvalidPrinterConfigError


class LegacyOctoPrintConnector(PrinterConnector):
    """Bridge connector that keeps current OctoPrint upload/start behavior."""

    def __init__(self):
        self._capabilities = ConnectorCapabilities(
            connector_type="octoprint_legacy",
            display_name="OctoPrint (Legacy Bridge)",
            protocol="octoprint",
            supports_pause=False,
            supports_resume=False,
            supports_cancel=False,
            supports_status=False,
        )
        self._last_upload_path: str = ""

    @property
    def capabilities(self) -> ConnectorCapabilities:
        return self._capabilities

    def _url(self, printer: Mapping[str, Any]) -> str:
        return str(printer.get("octoprint_url", "")).strip()

    def _api_key(self, printer: Mapping[str, Any]) -> str:
        return str(printer.get("octoprint_api_key", "")).strip()

    def connect(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        url = self._url(printer)
        if not url:
            return {"ok": False, "state": "missing_url", "message": "OctoPrint URL not configured."}
        api_key = self._api_key(printer)
        if not api_key:
            return {"ok": False, "state": "missing_api_key", "message": "OctoPrint API key not configured."}
        return {"ok": True, "state": "ready", "message": "OctoPrint legacy connector configured."}

    def upload(self, printer: Mapping[str, Any], gcode_path: str) -> dict[str, Any]:
        self.validate_printer(printer)
        path = Path(gcode_path)
        if not path.exists():
            raise ConnectorOperationError(f"GCODE_NOT_FOUND: {path}")
        self._last_upload_path = str(path)
        return {"ok": True, "remote_path": path.name, "bytes": int(path.stat().st_size)}

    def start_print(
        self,
        printer: Mapping[str, Any],
        *,
        remote_path: str | None = None,
        gcode_path: str | None = None,
    ) -> dict[str, Any]:
        self.validate_printer(printer)
        path = str(gcode_path or self._last_upload_path or "").strip()
        if not path:
            raise ConnectorOperationError("GCODE_PATH_REQUIRED: upload must run before start_print.")
        message = upload_and_print(self._url(printer), self._api_key(printer), path)
        return {"ok": True, "state": "submitted", "remote_path": remote_path or "", "message": str(message)}

    def pause(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        return {"ok": False, "state": "unsupported", "message": "Legacy OctoPrint bridge pause not implemented."}

    def resume(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        return {"ok": False, "state": "unsupported", "message": "Legacy OctoPrint bridge resume not implemented."}

    def cancel(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        return {"ok": False, "state": "unsupported", "message": "Legacy OctoPrint bridge cancel not implemented."}

    def status(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        return {"ok": True, "state": "unknown", "message": "Legacy OctoPrint bridge status not implemented."}

    def validate_printer(self, printer: Mapping[str, Any] | None) -> None:
        super().validate_printer(printer)
        if printer is None:
            raise InvalidPrinterConfigError("PRINTER_CONFIG_INVALID: expected mapping.")
        if "name" not in printer:
            raise InvalidPrinterConfigError("PRINTER_NAME_REQUIRED: printer.name missing.")
