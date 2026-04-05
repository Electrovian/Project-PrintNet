from __future__ import annotations

from pathlib import Path
import json
from typing import Any, Dict, List, Mapping, Optional

from connectors.bluetooth_pairing import BluetoothPairingManager
from connectors.errors import ConnectorError, LocalWifiOnboardingError
from connectors.local_wifi import LocalWifiOnboarding
from connectors.registry import ConnectorRegistry, build_default_connector_registry
from security.keychain_store import KeychainStore
from slicer_v2.legacy_gcode_writer import SliceSettings
from slicer_v2.service import slice_file


class PrinterManager:
    """High-level helper to slice and send to printer."""

    def __init__(
        self,
        printers: List[Dict],
        airtable_cfg: Dict,
        connector_registry: Optional[ConnectorRegistry] = None,
        wifi_onboarding: Optional[LocalWifiOnboarding] = None,
        bluetooth_pairing: Optional[BluetoothPairingManager] = None,
        keychain_store: Optional[KeychainStore] = None,
    ):
        self.printers = printers
        self.airtable_cfg = airtable_cfg
        self.connector_registry = connector_registry or build_default_connector_registry()
        self.wifi_onboarding = wifi_onboarding or LocalWifiOnboarding()
        self.bluetooth_pairing = bluetooth_pairing or BluetoothPairingManager()
        self.keychain_store = keychain_store or KeychainStore()
        # For now we just use the first printer.
        self.active_printer = printers[0] if printers else None

    _SECRET_KEYS = (
        "octoprint_api_key",
        "moonraker_token",
        "moonraker_api_key",
        "prusalink_api_key",
        "bambu_access_code",
        "bambu_token",
        "creality_token",
        "creality_api_key",
        "api_key",
    )

    def set_active_printer(self, printer: Mapping[str, Any] | None):
        self.active_printer = dict(printer) if isinstance(printer, Mapping) else None

    def _discovery_identity(self, printer: Mapping[str, Any]) -> str:
        # Use the same identity contract as local Wi-Fi merge logic when available.
        resolver = getattr(self.wifi_onboarding, "_discovery_identity", None)
        if callable(resolver):
            try:
                return str(resolver(printer))
            except Exception:
                pass
        connector_type = str(printer.get("connector_type", "")).strip().lower()
        host = str(printer.get("host", "")).strip().lower()
        port = int(printer.get("port", 0) or 0)
        if connector_type and host and port > 0:
            return f"{connector_type}|{host}:{port}"
        name = str(printer.get("name", "")).strip().lower()
        return f"{connector_type}|{name}"

    def _apply_merged_printers(self, merged: List[Dict[str, Any]]) -> None:
        selected = dict(self.active_printer) if isinstance(self.active_printer, Mapping) else None
        self.printers = [dict(item) for item in merged if isinstance(item, Mapping)]
        if not self.printers:
            self.active_printer = None
            return
        if selected is None:
            self.active_printer = self.printers[0]
            return

        selected_identity = self._discovery_identity(selected)
        for printer in self.printers:
            if self._discovery_identity(printer) == selected_identity:
                self.active_printer = dict(printer)
                return
        self.active_printer = self.printers[0]

    def slice_and_print(self, stl_path: str, settings: SliceSettings) -> str:
        gcode_path = slice_file(stl_path, settings=settings, printer=self.active_printer)
        return self.print_gcode(gcode_path, printer=self.active_printer)

    def print_gcode(self, gcode_path: str, printer: Mapping[str, Any] | None = None) -> str:
        active = dict(printer) if isinstance(printer, Mapping) else self.active_printer
        if not active:
            return f"No printer configured. G-code generated at {gcode_path}"

        try:
            connector = self.connector_registry.resolve(active)
            hydrated = self.hydrate_printer_credentials(active)
            connect_result = connector.connect(hydrated)
            if isinstance(connect_result, dict) and not bool(connect_result.get("ok", True)):
                message = str(connect_result.get("message", "")).strip()
                if message:
                    return message
                return f"Connector {connector.connector_type} is not ready."

            upload_result = connector.upload(hydrated, gcode_path)
            if isinstance(upload_result, dict) and not bool(upload_result.get("ok", True)):
                message = str(upload_result.get("message", "")).strip()
                if message:
                    return message
                return f"Connector {connector.connector_type} upload failed."

            remote_path = ""
            if isinstance(upload_result, dict):
                remote_path = str(upload_result.get("remote_path", "")).strip()
            start_result = connector.start_print(hydrated, remote_path=remote_path, gcode_path=gcode_path)
            if isinstance(start_result, dict):
                if not bool(start_result.get("ok", True)):
                    message = str(start_result.get("message", "")).strip()
                    if message:
                        return message
                    return f"Connector {connector.connector_type} start failed."
                message = str(start_result.get("message", "")).strip()
                if message:
                    return message

            filename = Path(gcode_path).name
            return f"Submitted {filename} to printer using {connector.connector_type}."
        except ConnectorError as exc:
            return f"Printer connector error: {exc}"
        except Exception as exc:
            return f"Unexpected printer connector error: {exc}"

    def discover_local_wifi_printers(
        self,
        *,
        hosts: List[str],
        ports: Optional[List[int]] = None,
        timeout_s: Optional[float] = None,
        max_targets: Optional[int] = None,
    ) -> Dict:
        try:
            report = self.wifi_onboarding.discover(
                hosts=hosts,
                ports=ports,
                timeout_s=timeout_s,
                max_targets=max_targets,
            )
        except LocalWifiOnboardingError as exc:
            return {"ok": False, "state": "invalid_config", "message": str(exc), "printers": []}

        discovered_printers = report.get("printers", [])
        merged = self.wifi_onboarding.merge_printers(self.printers, discovered_printers)
        self._apply_merged_printers(merged)

        result = dict(report)
        result["merged_printer_count"] = len(self.printers)
        return result

    def discover_local_wifi_printers_from_cidr(
        self,
        cidr: str,
        *,
        ports: Optional[List[int]] = None,
        host_limit: int = 64,
        timeout_s: Optional[float] = None,
        max_targets: Optional[int] = None,
    ) -> Dict:
        try:
            report = self.wifi_onboarding.discover_from_cidr(
                cidr,
                ports=ports,
                host_limit=host_limit,
                timeout_s=timeout_s,
                max_targets=max_targets,
            )
        except LocalWifiOnboardingError as exc:
            return {"ok": False, "state": "invalid_config", "message": str(exc), "printers": []}

        discovered_printers = report.get("printers", [])
        merged = self.wifi_onboarding.merge_printers(self.printers, discovered_printers)
        self._apply_merged_printers(merged)

        result = dict(report)
        result["merged_printer_count"] = len(self.printers)
        return result

    def discover_bluetooth_printers(self, *, timeout_s: float = 5.0) -> Dict:
        report = self.bluetooth_pairing.discover(timeout_s=timeout_s)
        payload = dict(report)
        devices = payload.get("devices", [])
        normalized_devices = [dict(item) for item in devices if isinstance(item, Mapping)]
        payload["device_count"] = len(normalized_devices)
        payload["devices"] = normalized_devices
        return payload

    def pair_bluetooth_printer(self, *, device_id: str) -> Dict:
        result = self.bluetooth_pairing.pair(device_id=device_id)
        return dict(result)

    def run_connection_diagnostics(self, printer: Mapping[str, Any]) -> Dict:
        try:
            candidate = self.hydrate_printer_credentials(printer)
            connector = self.connector_registry.resolve(candidate)
            connect_payload = connector.connect(candidate)
            ok = bool(connect_payload.get("ok", True)) if isinstance(connect_payload, Mapping) else True
            state = str(connect_payload.get("state", "ready")) if isinstance(connect_payload, Mapping) else "ready"
            message = str(connect_payload.get("message", "")) if isinstance(connect_payload, Mapping) else ""
            return {
                "ok": ok,
                "state": state,
                "connector_type": connector.connector_type,
                "message": message,
                "details": dict(connect_payload) if isinstance(connect_payload, Mapping) else {},
            }
        except Exception as exc:
            return {
                "ok": False,
                "state": "failed",
                "connector_type": str(printer.get("connector_type", "")).strip(),
                "message": str(exc),
                "details": {},
            }

    def test_manual_endpoint(
        self,
        *,
        connector_type: str,
        endpoint: str,
        name: str = "Manual Printer",
        credentials: Optional[Mapping[str, str]] = None,
    ) -> Dict:
        normalized_type = str(connector_type or "").strip().lower()
        normalized_endpoint = str(endpoint or "").strip()
        if not normalized_type:
            return {"ok": False, "state": "invalid_config", "message": "connector_type is required."}
        if not normalized_endpoint:
            return {"ok": False, "state": "invalid_config", "message": "endpoint is required."}
        printer: Dict[str, Any] = {
            "name": str(name or "Manual Printer"),
            "connector_type": normalized_type,
            "endpoint": normalized_endpoint,
        }
        creds = dict(credentials or {})
        if normalized_type == "octoprint":
            printer["octoprint_url"] = normalized_endpoint
            printer["octoprint_api_key"] = str(creds.get("octoprint_api_key", creds.get("api_key", "")))
        elif normalized_type == "moonraker":
            printer["moonraker_url"] = normalized_endpoint
            printer["moonraker_token"] = str(creds.get("moonraker_token", creds.get("api_key", "")))
        elif normalized_type == "prusalink":
            printer["prusalink_url"] = normalized_endpoint
            printer["prusalink_api_key"] = str(creds.get("prusalink_api_key", creds.get("api_key", "")))
        elif normalized_type == "bambu_lan":
            printer["bambu_url"] = normalized_endpoint
            printer["bambu_access_code"] = str(creds.get("bambu_access_code", creds.get("api_key", "")))
        elif normalized_type == "creality":
            printer["creality_url"] = normalized_endpoint
            printer["creality_protocol"] = str(creds.get("creality_protocol", "moonraker"))
            printer["creality_token"] = str(creds.get("creality_token", creds.get("api_key", "")))
        return self.run_connection_diagnostics(printer)

    def onboarding_add_printer(self, printer: Mapping[str, Any]) -> Dict:
        candidate = dict(printer or {})
        name = str(candidate.get("name", "")).strip()
        if not name:
            return {"ok": False, "state": "invalid_config", "message": "printer.name is required."}
        connector_type = str(candidate.get("connector_type", "")).strip().lower()
        if not connector_type:
            return {"ok": False, "state": "invalid_config", "message": "printer.connector_type is required."}
        diagnostic = self.run_connection_diagnostics(candidate)
        if not bool(diagnostic.get("ok", False)):
            return {"ok": False, "state": "health_check_failed", "diagnostic": diagnostic}

        identifier = str(candidate.get("printer_id", "")).strip() or self._build_printer_id(candidate)
        candidate["printer_id"] = identifier
        self.store_printer_credentials(identifier, candidate)
        sanitized = self._without_secret_keys(candidate)
        merged = self.wifi_onboarding.merge_printers(self.printers, [sanitized])
        self._apply_merged_printers(merged)
        return {
            "ok": True,
            "state": "saved",
            "printer": sanitized,
            "diagnostic": diagnostic,
            "printer_count": len(self.printers),
        }

    def store_printer_credentials(self, printer_id: str, printer: Mapping[str, Any]) -> None:
        key = str(printer_id or "").strip()
        if not key:
            return
        secrets_payload: dict[str, str] = {}
        for secret_key in self._SECRET_KEYS:
            value = str(printer.get(secret_key, "")).strip()
            if value:
                secrets_payload[secret_key] = value
        if not secrets_payload:
            return
        self.keychain_store.set_secret(f"printer:{key}", json.dumps(secrets_payload))

    def hydrate_printer_credentials(self, printer: Mapping[str, Any]) -> Dict[str, Any]:
        candidate = dict(printer or {})
        key = str(candidate.get("printer_id", "")).strip()
        if not key:
            return candidate
        blob = self.keychain_store.get_secret(f"printer:{key}")
        if not blob:
            return candidate
        try:
            payload = json.loads(blob)
        except Exception:
            return candidate
        if not isinstance(payload, Mapping):
            return candidate
        for secret_key in self._SECRET_KEYS:
            if secret_key not in payload:
                continue
            current = str(candidate.get(secret_key, "")).strip()
            if current:
                continue
            candidate[secret_key] = str(payload.get(secret_key, "")).strip()
        return candidate

    def delete_printer_credentials(self, printer_id: str) -> None:
        key = str(printer_id or "").strip()
        if not key:
            return
        self.keychain_store.delete_secret(f"printer:{key}")

    def _build_printer_id(self, printer: Mapping[str, Any]) -> str:
        connector = str(printer.get("connector_type", "printer")).strip().lower() or "printer"
        name = str(printer.get("name", "printer")).strip().lower().replace(" ", "-")
        endpoint = str(printer.get("endpoint", "") or printer.get("host", "")).strip().lower()
        token = f"{connector}-{name}".strip("-")
        if endpoint:
            endpoint_tail = endpoint.replace("http://", "").replace("https://", "").replace("/", "-")
            token = f"{token}-{endpoint_tail}"
        return token[:96]

    def _without_secret_keys(self, printer: Mapping[str, Any]) -> Dict[str, Any]:
        cleaned = dict(printer)
        for secret_key in self._SECRET_KEYS:
            cleaned.pop(secret_key, None)
        return cleaned
