from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, cast
from urllib.parse import quote

import requests

from .base import ConnectorCapabilities, PrinterConnector
from .errors import ConnectorOperationError, InvalidPrinterConfigError


class MoonrakerConnector(PrinterConnector):
    """Moonraker connector implementation using Klipper/Moonraker HTTP API."""

    def __init__(self, *, timeout_s: float = 20.0, session: requests.Session | None = None):
        self._timeout_s = float(timeout_s)
        self._session = session if session is not None else requests.Session()
        self._capabilities = ConnectorCapabilities(
            connector_type="moonraker",
            display_name="Moonraker",
            protocol="moonraker",
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
        value = str(printer.get("moonraker_url", "") or printer.get("klipper_url", "")).strip()
        if not value:
            raise InvalidPrinterConfigError("MOONRAKER_URL_REQUIRED: moonraker_url is required.")
        return value.rstrip("/")

    def _headers(self, printer: Mapping[str, Any]) -> dict[str, str]:
        token = str(printer.get("moonraker_token", "") or printer.get("moonraker_api_key", "")).strip()
        if not token:
            return {}
        if token.lower().startswith("bearer "):
            return {"Authorization": token}
        return {"Authorization": f"Bearer {token}"}

    def _request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        if "timeout" not in kwargs:
            kwargs["timeout"] = self._timeout_s
        try:
            response = self._session.request(method, url, **kwargs)
        except requests.RequestException as exc:
            raise ConnectorOperationError(f"MOONRAKER_REQUEST_FAILED: {exc}") from exc
        if int(response.status_code) >= 400:
            snippet = str(getattr(response, "text", "") or "").strip()
            if len(snippet) > 160:
                snippet = snippet[:160]
            raise ConnectorOperationError(f"MOONRAKER_HTTP_{response.status_code}: {snippet}")
        return response

    def _json_or_empty(self, response: requests.Response) -> dict[str, Any]:
        try:
            payload = response.json()
        except ValueError:
            return {}
        if isinstance(payload, dict):
            return payload
        return {}

    def _result_payload(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        result = payload.get("result", {})
        if isinstance(result, dict):
            return dict(result)
        return {}

    def _resolve_remote_path(self, payload: Mapping[str, Any], fallback_name: str) -> str:
        result = self._result_payload(payload)
        item = result.get("item", {})
        if isinstance(item, Mapping):
            path = str(item.get("path", "") or "").strip()
            if path:
                return path
            filename = str(item.get("filename", "") or "").strip()
            if filename:
                return filename
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
        except InvalidPrinterConfigError as exc:
            return {"ok": False, "state": "missing_config", "message": str(exc)}
        try:
            response = self._request("GET", f"{base_url}/server/info", headers=self._headers(printer))
            payload = self._json_or_empty(response)
            result = self._result_payload(payload)
            version = str(result.get("moonraker_version", "")).strip()
            return {"ok": True, "state": "ready", "version": version}
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
            data = {"root": "gcodes", "path": path.name}
            response = self._request(
                "POST",
                f"{base_url}/server/files/upload",
                headers=headers,
                files=files,
                data=data,
            )
        payload = self._json_or_empty(response)
        remote_path = self._resolve_remote_path(payload, path.name)
        return {"ok": True, "remote_path": remote_path, "bytes": int(path.stat().st_size)}

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
        encoded_path = quote(resolved, safe="/")
        self._request(
            "POST",
            f"{base_url}/printer/print/start?filename={encoded_path}",
            headers=self._headers(printer),
        )
        return {"ok": True, "state": "submitted", "remote_path": resolved, "message": "Moonraker print started."}

    def pause(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        base_url = self._base_url(printer)
        self._request("POST", f"{base_url}/printer/print/pause", headers=self._headers(printer))
        return {"ok": True, "state": "paused"}

    def resume(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        base_url = self._base_url(printer)
        self._request("POST", f"{base_url}/printer/print/resume", headers=self._headers(printer))
        return {"ok": True, "state": "printing"}

    def cancel(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        base_url = self._base_url(printer)
        self._request("POST", f"{base_url}/printer/print/cancel", headers=self._headers(printer))
        return {"ok": True, "state": "canceled"}

    def status(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.validate_printer(printer)
        base_url = self._base_url(printer)
        response = self._request(
            "GET",
            f"{base_url}/printer/objects/query?print_stats&virtual_sdcard",
            headers=self._headers(printer),
        )
        payload = self._json_or_empty(response)
        result = self._result_payload(payload)
        status = result.get("status", {})
        if not isinstance(status, Mapping):
            status = {}
        print_stats = status.get("print_stats", {})
        sdcard = status.get("virtual_sdcard", {})
        if not isinstance(print_stats, Mapping):
            print_stats = {}
        if not isinstance(sdcard, Mapping):
            sdcard = {}

        state = str(print_stats.get("state", "unknown")).strip().lower() or "unknown"
        filename = str(print_stats.get("filename", "")).strip()
        progress_raw = float(sdcard.get("progress", 0.0) or 0.0)
        progress_pct = progress_raw * 100.0 if progress_raw <= 1.0 else progress_raw
        print_duration = float(print_stats.get("print_duration", 0.0) or 0.0)
        time_left_s = 0
        if progress_pct > 0.0:
            total_seconds = print_duration / (progress_pct / 100.0)
            if total_seconds >= print_duration:
                time_left_s = int(max(total_seconds - print_duration, 0.0))

        return {
            "ok": True,
            "state": state,
            "file": filename,
            "progress_pct": float(progress_pct),
            "time_left_s": int(time_left_s),
        }
