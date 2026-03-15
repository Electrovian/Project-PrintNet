from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, cast

import requests

from .base import ConnectorCapabilities, PrinterConnector
from .errors import ConnectorOperationError, InvalidPrinterConfigError


class BambuLanConnector(PrinterConnector):
    """Bambu LAN connector using configurable local HTTP bridge endpoints."""

    def __init__(self, *, timeout_s: float = 20.0, session: requests.Session | None = None):
        self._timeout_s = float(timeout_s)
        self._session = session if session is not None else requests.Session()
        self._capabilities = ConnectorCapabilities(
            connector_type="bambu_lan",
            display_name="Bambu LAN",
            protocol="bambu_lan",
            supports_connect=True,
            supports_upload=True,
            supports_start=True,
            supports_pause=True,
            supports_resume=True,
            supports_cancel=True,
            supports_status=True,
        )

    @property
    def capabilities(self) -> ConnectorCapabilities:
        return self._capabilities

    def _base_url(self, printer: Mapping[str, Any]) -> str:
        value = str(printer.get("bambu_url", "") or printer.get("endpoint", "")).strip()
        if not value:
            host = str(printer.get("host", "")).strip()
            port = int(printer.get("port", 0) or 0)
            if host and port > 0:
                value = f"http://{host}:{port}"
        if not value:
            raise InvalidPrinterConfigError("BAMBU_URL_REQUIRED: bambu_url is required.")
        return value.rstrip("/")

    def _token(self, printer: Mapping[str, Any]) -> str:
        return str(
            printer.get("bambu_access_code", "")
            or printer.get("bambu_token", "")
            or printer.get("api_key", "")
        ).strip()

    def _headers(self, printer: Mapping[str, Any]) -> dict[str, str]:
        token = self._token(printer)
        headers: dict[str, str] = {}
        if token:
            headers["X-Bambu-Token"] = token
            if token.lower().startswith("bearer "):
                headers["Authorization"] = token
            else:
                headers["Authorization"] = f"Bearer {token}"
        serial = str(printer.get("bambu_serial", "")).strip()
        if serial:
            headers["X-Bambu-Serial"] = serial
        return headers

    def _request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        if "timeout" not in kwargs:
            kwargs["timeout"] = self._timeout_s
        try:
            response = self._session.request(method, url, **kwargs)
        except requests.RequestException as exc:
            raise ConnectorOperationError(f"BAMBU_REQUEST_FAILED: {exc}") from exc
        if int(response.status_code) >= 400:
            snippet = str(getattr(response, "text", "") or "").strip()
            if len(snippet) > 180:
                snippet = snippet[:180]
            raise ConnectorOperationError(f"BAMBU_HTTP_{response.status_code}: {snippet}")
        return response

    def _json_or_empty(self, response: requests.Response) -> dict[str, Any]:
        try:
            payload = response.json()
        except ValueError:
            return {}
        if isinstance(payload, Mapping):
            return dict(payload)
        return {}

    def validate_printer(self, printer: Mapping[str, Any] | None) -> None:
        super().validate_printer(printer)
        if printer is None:
            raise InvalidPrinterConfigError("PRINTER_CONFIG_INVALID: expected mapping.")
        printer_map = cast(Mapping[str, Any], printer)
        if "name" not in printer_map:
            raise InvalidPrinterConfigError("PRINTER_NAME_REQUIRED: printer.name missing.")

    def connect(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        try:
            base_url = self._base_url(printer)
            headers = self._headers(printer)
        except InvalidPrinterConfigError as exc:
            return {"ok": False, "state": "missing_config", "message": str(exc)}
        paths = ("/api/v1/status", "/status")
        for suffix in paths:
            try:
                response = self._request("GET", f"{base_url}{suffix}", headers=headers)
            except ConnectorOperationError:
                continue
            payload = self._json_or_empty(response)
            return {
                "ok": True,
                "state": "ready",
                "path": suffix,
                "device": str(payload.get("device", "") or payload.get("name", "")).strip() or "Bambu",
            }
        return {
            "ok": False,
            "state": "unreachable",
            "message": "BAMBU_CONNECT_FAILED: no status endpoint responded.",
        }

    def upload(self, printer: Mapping[str, Any], gcode_path: str) -> dict[str, Any]:
        self.validate_printer(printer)
        path = Path(gcode_path)
        if not path.exists():
            raise ConnectorOperationError(f"GCODE_NOT_FOUND: {path}")
        base_url = self._base_url(printer)
        headers = self._headers(printer)
        with path.open("rb") as handle:
            response = self._request(
                "POST",
                f"{base_url}/api/v1/files/upload",
                headers=headers,
                files={"file": (path.name, handle, "application/octet-stream")},
            )
        payload = self._json_or_empty(response)
        remote_path = str(payload.get("remote_path", "") or payload.get("path", "")).strip() or path.name
        return {
            "ok": True,
            "remote_path": remote_path,
            "bytes": int(path.stat().st_size),
        }

    def start_print(
        self,
        printer: Mapping[str, Any],
        *,
        remote_path: str | None = None,
        gcode_path: str | None = None,
    ) -> dict[str, Any]:
        self.validate_printer(printer)
        base_url = self._base_url(printer)
        resolved = str(remote_path or "").strip()
        if not resolved and gcode_path:
            resolved = Path(str(gcode_path)).name
        if not resolved:
            raise ConnectorOperationError("GCODE_PATH_REQUIRED: remote_path or gcode_path must be provided.")
        self._request(
            "POST",
            f"{base_url}/api/v1/print/start",
            headers=self._headers(printer),
            json={"file": resolved},
        )
        return {"ok": True, "state": "submitted", "remote_path": resolved, "message": "Bambu print started."}

    def pause(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        base_url = self._base_url(printer)
        self._request("POST", f"{base_url}/api/v1/print/pause", headers=self._headers(printer))
        return {"ok": True, "state": "paused"}

    def resume(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        base_url = self._base_url(printer)
        self._request("POST", f"{base_url}/api/v1/print/resume", headers=self._headers(printer))
        return {"ok": True, "state": "printing"}

    def cancel(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        base_url = self._base_url(printer)
        self._request("POST", f"{base_url}/api/v1/print/cancel", headers=self._headers(printer))
        return {"ok": True, "state": "canceled"}

    def status(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        base_url = self._base_url(printer)
        response = self._request("GET", f"{base_url}/api/v1/status", headers=self._headers(printer))
        payload = self._json_or_empty(response)
        progress_pct = float(payload.get("progress_pct", payload.get("progress", 0.0)) or 0.0)
        if progress_pct <= 1.0:
            progress_pct *= 100.0
        return {
            "ok": True,
            "state": str(payload.get("state", "unknown")).strip().lower() or "unknown",
            "file": str(payload.get("file", "")).strip(),
            "progress_pct": float(progress_pct),
            "time_left_s": int(payload.get("time_left_s", 0) or 0),
        }
