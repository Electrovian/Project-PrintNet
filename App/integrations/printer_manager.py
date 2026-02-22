from pathlib import Path
from typing import List, Dict, Optional

from slicer_v2.service import slice_file
from slicer_v2.legacy_gcode_writer import SliceSettings
from connectors.errors import ConnectorError, LocalWifiOnboardingError
from connectors.local_wifi import LocalWifiOnboarding
from connectors.registry import ConnectorRegistry, build_default_connector_registry


class PrinterManager:
    """High-level helper to slice and send to printer."""

    def __init__(
        self,
        printers: List[Dict],
        airtable_cfg: Dict,
        connector_registry: Optional[ConnectorRegistry] = None,
        wifi_onboarding: Optional[LocalWifiOnboarding] = None,
    ):
        self.printers = printers
        self.airtable_cfg = airtable_cfg
        self.connector_registry = connector_registry or build_default_connector_registry()
        self.wifi_onboarding = wifi_onboarding or LocalWifiOnboarding()
        # For now we just use the first printer.
        self.active_printer = printers[0] if printers else None

    def set_active_printer(self, printer: Dict | None):
        self.active_printer = printer

    def slice_and_print(self, stl_path: str, settings: SliceSettings) -> str:
        gcode_path = slice_file(stl_path, settings=settings)
        return self.print_gcode(gcode_path, printer=self.active_printer)

    def print_gcode(self, gcode_path: str, printer: Dict | None = None) -> str:
        active = printer or self.active_printer
        if not active:
            return (f"No printer configured. G-code generated at "
                    f"{gcode_path}")
        try:
            connector = self.connector_registry.resolve(active)
            connect_result = connector.connect(active)
            if isinstance(connect_result, dict) and not bool(connect_result.get("ok", True)):
                message = str(connect_result.get("message", "")).strip()
                if message:
                    return message
                return f"Connector {connector.connector_type} is not ready."

            upload_result = connector.upload(active, gcode_path)
            if isinstance(upload_result, dict) and not bool(upload_result.get("ok", True)):
                message = str(upload_result.get("message", "")).strip()
                if message:
                    return message
                return f"Connector {connector.connector_type} upload failed."
            remote_path = str(upload_result.get("remote_path", "")).strip() if isinstance(upload_result, dict) else ""
            start_result = connector.start_print(active, remote_path=remote_path, gcode_path=gcode_path)
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
        self.printers = merged
        if self.active_printer is None and self.printers:
            self.active_printer = self.printers[0]

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
        self.printers = merged
        if self.active_printer is None and self.printers:
            self.active_printer = self.printers[0]

        result = dict(report)
        result["merged_printer_count"] = len(self.printers)
        return result
