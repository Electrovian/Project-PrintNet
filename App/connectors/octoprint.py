from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, cast
from urllib.parse import quote

import requests

from .base import ConnectorCapabilities, PrinterConnector
from .errors import ConnectorOperationError, InvalidPrinterConfigError


class OctoPrintConnector(PrinterConnector):
    """OctoPrint connector implementation using HTTP API endpoints."""

    def __init__(self, *, timeout_s: float = 20.0, session: requests.Session | None = None):
        self._timeout_s = float(timeout_s)
        self._session = session if session is not None else requests.Session()
        self._capabilities = ConnectorCapabilities(
            connector_type="octoprint",
            display_name="OctoPrint",
            protocol="octoprint",
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
        value = str(printer.get("octoprint_url", "")).strip()
        if not value:
            raise InvalidPrinterConfigError("OCTOPRINT_URL_REQUIRED: octoprint_url is required.")
        return value.rstrip("/")

    def _api_key(self, printer: Mapping[str, Any]) -> str:
        value = str(printer.get("octoprint_api_key", "")).strip()
        if not value:
            raise InvalidPrinterConfigError("OCTOPRINT_API_KEY_REQUIRED: octoprint_api_key is required.")
        return value

    def _headers(self, printer: Mapping[str, Any]) -> dict[str, str]:
        return {"X-Api-Key": self._api_key(printer)}

    def _request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        if "timeout" not in kwargs:
            kwargs["timeout"] = self._timeout_s
        try:
            response = self._session.request(method, url, **kwargs)
        except requests.RequestException as exc:
            raise ConnectorOperationError(f"OCTOPRINT_REQUEST_FAILED: {exc}") from exc
        if int(response.status_code) >= 400:
            snippet = str(getattr(response, "text", "") or "").strip()
            if len(snippet) > 160:
                snippet = snippet[:160]
            raise ConnectorOperationError(f"OCTOPRINT_HTTP_{response.status_code}: {snippet}")
        return response

    def _json_or_empty(self, response: requests.Response) -> dict[str, Any]:
        try:
            payload = response.json()
        except ValueError:
            return {}
        if isinstance(payload, dict):
            return payload
        return {}

    def _resolve_remote_path(self, payload: Mapping[str, Any], fallback_name: str) -> str:
        files = payload.get("files", {})
        if isinstance(files, Mapping):
            local = files.get("local", {})
            if isinstance(local, Mapping):
                path = str(local.get("path", "") or "").strip()
                if path:
                    return path
                name = str(local.get("name", "") or "").strip()
                if name:
                    return name
        return str(fallback_name or "").strip()

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
        try:
            response = self._request("GET", f"{base_url}/api/version", headers=headers)
            payload = self._json_or_empty(response)
            return {
                "ok": True,
                "state": "ready",
                "server": str(payload.get("server", "OctoPrint")),
                "api_version": str(payload.get("api", "")),
            }
        except ConnectorOperationError as exc:
            return {"ok": False, "state": "unreachable", "message": str(exc)}

    def upload(self, printer: Mapping[str, Any], gcode_path: str) -> dict[str, Any]:
        self.validate_printer(printer)
        path = Path(gcode_path)
        if not path.exists():
            raise ConnectorOperationError(f"GCODE_NOT_FOUND: {path}")
        base_url = self._base_url(printer)
        headers = self._headers(printer)
        with path.open("rb") as handle:
            files = {"file": (path.name, handle, "application/octet-stream")}
            data = {"select": "false", "print": "false"}
            response = self._request(
                "POST",
                f"{base_url}/api/files/local",
                headers=headers,
                files=files,
                data=data,
            )
        payload = self._json_or_empty(response)
        remote_path = self._resolve_remote_path(payload, path.name)
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
        headers = self._headers(printer)
        resolved = str(remote_path or "").strip()
        if not resolved and gcode_path:
            resolved = Path(str(gcode_path)).name
        if not resolved:
            raise ConnectorOperationError("GCODE_PATH_REQUIRED: remote_path or gcode_path must be provided.")
        encoded_path = quote(resolved, safe="/")
        self._request(
            "POST",
            f"{base_url}/api/files/local/{encoded_path}",
            headers=headers,
            json={"command": "select", "print": True},
        )
        return {"ok": True, "state": "submitted", "remote_path": resolved, "message": "OctoPrint print started."}

    def pause(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        base_url = self._base_url(printer)
        headers = self._headers(printer)
        self._request("POST", f"{base_url}/api/job", headers=headers, json={"command": "pause", "action": "pause"})
        return {"ok": True, "state": "paused"}

    def resume(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        base_url = self._base_url(printer)
        headers = self._headers(printer)
        self._request("POST", f"{base_url}/api/job", headers=headers, json={"command": "pause", "action": "resume"})
        return {"ok": True, "state": "printing"}

    def cancel(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        base_url = self._base_url(printer)
        headers = self._headers(printer)
        self._request("POST", f"{base_url}/api/job", headers=headers, json={"command": "cancel"})
        return {"ok": True, "state": "canceled"}

    def status(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        base_url = self._base_url(printer)
        headers = self._headers(printer)
        response = self._request("GET", f"{base_url}/api/job", headers=headers)
        payload = self._json_or_empty(response)
        progress = payload.get("progress", {})
        file_info = payload.get("job", {})
        if isinstance(file_info, Mapping):
            file_info = file_info.get("file", {})
        if not isinstance(progress, Mapping):
            progress = {}
        if not isinstance(file_info, Mapping):
            file_info = {}
        return {
            "ok": True,
            "state": str(payload.get("state", "unknown")).strip().lower() or "unknown",
            "file": str(file_info.get("name", "")).strip(),
            "progress_pct": float(progress.get("completion", 0.0) or 0.0),
            "time_left_s": int(progress.get("printTimeLeft", 0) or 0),
        }
