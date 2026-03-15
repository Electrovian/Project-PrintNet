from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .base import ConnectorCapabilities, PrinterConnector
from .errors import ConnectorOperationError


class LocalFileConnector(PrinterConnector):
    """Offline-safe connector that only validates and stages local G-code."""

    def __init__(self):
        self._capabilities = ConnectorCapabilities(
            connector_type="local_file",
            display_name="Local File Connector",
            protocol="local",
            supports_connect=False,
            supports_pause=False,
            supports_resume=False,
            supports_cancel=False,
            supports_status=False,
        )

    @property
    def capabilities(self) -> ConnectorCapabilities:
        return self._capabilities

    def connect(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        return {"ok": True, "mode": "offline", "message": "Local connector does not require network connect."}

    def upload(self, printer: Mapping[str, Any], gcode_path: str) -> dict[str, Any]:
        self.validate_printer(printer)
        path = Path(gcode_path)
        if not path.exists():
            raise ConnectorOperationError(f"GCODE_NOT_FOUND: {path}")
        return {"ok": True, "remote_path": str(path), "bytes": int(path.stat().st_size)}

    def start_print(
        self,
        printer: Mapping[str, Any],
        *,
        remote_path: str | None = None,
        gcode_path: str | None = None,
    ) -> dict[str, Any]:
        self.validate_printer(printer)
        path = remote_path or gcode_path or ""
        if not path:
            raise ConnectorOperationError("GCODE_PATH_REQUIRED: remote_path or gcode_path must be provided.")
        return {
            "ok": True,
            "state": "queued_local",
            "message": f"Local queue placeholder: ready to send {Path(path).name} to a physical connector.",
        }

    def pause(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        return {"ok": False, "state": "unsupported", "message": "Pause is unsupported for local connector."}

    def resume(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        return {"ok": False, "state": "unsupported", "message": "Resume is unsupported for local connector."}

    def cancel(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        return {"ok": False, "state": "unsupported", "message": "Cancel is unsupported for local connector."}

    def status(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        return {"ok": True, "state": "idle", "message": "Local connector idle."}
