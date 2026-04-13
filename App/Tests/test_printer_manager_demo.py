from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Mapping

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from connectors.base import ConnectorCapabilities, PrinterConnector  # noqa: E402
from connectors.errors import ConnectorOperationError  # noqa: E402
from connectors.registry import ConnectorRegistry  # noqa: E402
from integrations.printer_manager import PrinterManager  # noqa: E402
from security.keychain_store import KeychainStore  # noqa: E402


class _ScriptedConnector(PrinterConnector):
    def __init__(
        self,
        connector_type: str,
        *,
        connect_result: dict[str, Any] | None = None,
        upload_result: dict[str, Any] | None = None,
        start_result: dict[str, Any] | None = None,
    ):
        self._capabilities = ConnectorCapabilities(
            connector_type=connector_type,
            display_name=connector_type,
            protocol=connector_type,
        )
        self._connect_result = dict(connect_result or {"ok": True, "state": "ready"})
        self._upload_result = dict(upload_result or {"ok": True, "remote_path": "job.gcode"})
        self._start_result = dict(start_result or {"ok": True, "state": "submitted", "message": ""})
        self.last_printer: dict[str, Any] | None = None
        self.last_gcode_path: str | None = None

    @property
    def capabilities(self) -> ConnectorCapabilities:
        return self._capabilities

    def connect(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        self.last_printer = dict(printer)
        result = dict(self._connect_result)
        result.setdefault("printer", dict(printer))
        return result

    def upload(self, printer: Mapping[str, Any], gcode_path: str) -> dict[str, Any]:
        self.last_printer = dict(printer)
        self.last_gcode_path = str(gcode_path)
        result = dict(self._upload_result)
        if result.pop("__raise__", False):
            raise ConnectorOperationError(result.get("message", "upload failure"))
        result.setdefault("printer", dict(printer))
        return result

    def start_print(
        self,
        printer: Mapping[str, Any],
        *,
        remote_path: str | None = None,
        gcode_path: str | None = None,
    ) -> dict[str, Any]:
        self.last_printer = dict(printer)
        self.last_gcode_path = str(gcode_path or remote_path or "")
        result = dict(self._start_result)
        if result.pop("__raise__", False):
            raise ConnectorOperationError(result.get("message", "start failure"))
        result.setdefault("printer", dict(printer))
        return result

    def pause(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        return {"ok": True, "state": "paused"}

    def resume(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        return {"ok": True, "state": "printing"}

    def cancel(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        return {"ok": True, "state": "canceled"}

    def status(self, printer: Mapping[str, Any]) -> dict[str, Any]:
        return {"ok": True, "state": "idle"}


def _build_registry(connectors: dict[str, _ScriptedConnector]) -> ConnectorRegistry:
    registry = ConnectorRegistry()
    for connector in connectors.values():
        registry.register(connector)
    return registry


class PrinterManagerDemoTests(unittest.TestCase):
    def test_print_gcode_reports_stage_specific_failure_messages(self):
        connectors = {
            "octoprint": _ScriptedConnector(
                "octoprint",
                connect_result={"ok": False, "state": "missing_config", "message": "OCTOPRINT_API_KEY_REQUIRED: octoprint_api_key is required."},
            ),
            "moonraker": _ScriptedConnector(
                "moonraker",
                upload_result={"ok": False, "state": "rejected", "message": "moonraker upload denied."},
            ),
            "prusalink": _ScriptedConnector(
                "prusalink",
                start_result={"ok": False, "state": "busy", "message": "prusalink printer is busy."},
            ),
            "bambu_lan": _ScriptedConnector(
                "bambu_lan",
                connect_result={"ok": False, "state": "unreachable", "message": "BAMBU_CONNECT_FAILED: no status endpoint responded."},
            ),
            "creality": _ScriptedConnector(
                "creality",
                start_result={"ok": False, "state": "blocked", "message": "creality print start rejected."},
            ),
            "local_file": _ScriptedConnector(
                "local_file",
                start_result={
                    "ok": True,
                    "state": "queued_local",
                    "message": "Local queue placeholder: ready to send job.gcode to a physical connector.",
                },
            ),
        }
        registry = _build_registry(connectors)
        manager = PrinterManager(printers=[], airtable_cfg={}, connector_registry=registry)

        with tempfile.TemporaryDirectory() as tmp:
            gcode_path = Path(tmp).joinpath("job.gcode")
            gcode_path.write_text("G28\n", encoding="utf-8")

            cases = [
                (
                    "octoprint",
                    {"name": "Octo", "connector_type": "octoprint", "octoprint_url": "http://localhost", "octoprint_api_key": ""},
                    ("octoprint connect failed", "missing_config", "OCTOPRINT_API_KEY_REQUIRED"),
                ),
                (
                    "moonraker",
                    {"name": "Moon", "connector_type": "moonraker", "moonraker_url": "http://localhost:7125"},
                    ("moonraker upload failed", "rejected", "moonraker upload denied"),
                ),
                (
                    "prusalink",
                    {"name": "Prusa", "connector_type": "prusalink", "prusalink_url": "http://localhost:8080", "prusalink_api_key": "token"},
                    ("prusalink start failed", "busy", "prusalink printer is busy"),
                ),
                (
                    "bambu_lan",
                    {"name": "Bambu", "connector_type": "bambu_lan", "bambu_url": "http://10.0.0.5", "bambu_access_code": "token"},
                    ("bambu_lan connect failed", "unreachable", "BAMBU_CONNECT_FAILED"),
                ),
                (
                    "creality",
                    {"name": "Creality", "connector_type": "creality", "creality_url": "http://10.0.0.77", "creality_token": "abc"},
                    ("creality start failed", "blocked", "creality print start rejected"),
                ),
                (
                    "local_file",
                    {"name": "Local", "connector_type": "local_file"},
                    ("Local queue placeholder", "", ""),
                ),
            ]

            for connector_type, printer, expected in cases:
                with self.subTest(connector_type=connector_type):
                    message = manager.print_gcode(str(gcode_path), printer=printer)
                    for fragment in expected:
                        if fragment:
                            self.assertIn(fragment, message)

    def test_run_connection_diagnostics_returns_stage_and_details(self):
        connector = _ScriptedConnector(
            "moonraker",
            connect_result={
                "ok": False,
                "state": "unreachable",
                "message": "MOONRAKER_REQUEST_FAILED: timeout",
                "attempts": 2,
            },
        )
        registry = _build_registry({"moonraker": connector})
        manager = PrinterManager(printers=[], airtable_cfg={}, connector_registry=registry)

        payload = manager.run_connection_diagnostics(
            {
                "name": "Moon",
                "connector_type": "moonraker",
                "moonraker_url": "http://localhost:7125",
                "moonraker_token": "secret",
            }
        )

        self.assertFalse(payload["ok"])
        self.assertEqual(payload["stage"], "connect")
        self.assertEqual(payload["connector_type"], "moonraker")
        self.assertEqual(payload["state"], "unreachable")
        self.assertIn("MOONRAKER_REQUEST_FAILED", payload["message"])
        self.assertEqual(payload["details"]["attempts"], 2)

    def test_manual_endpoint_maps_connector_specific_fields(self):
        connectors = {
            name: _ScriptedConnector(name, connect_result={"ok": True, "state": "ready", "message": f"{name} ready"})
            for name in ("octoprint", "moonraker", "prusalink", "bambu_lan", "creality", "local_file")
        }
        registry = _build_registry(connectors)
        manager = PrinterManager(printers=[], airtable_cfg={}, connector_registry=registry)

        expectations = {
            "octoprint": ("octoprint_url", "octoprint_api_key"),
            "moonraker": ("moonraker_url", "moonraker_token"),
            "prusalink": ("prusalink_url", "prusalink_api_key"),
            "bambu_lan": ("bambu_url", "bambu_access_code"),
            "creality": ("creality_url", "creality_protocol", "creality_token"),
            "local_file": ("endpoint",),
        }

        for connector_type, keys in expectations.items():
            with self.subTest(connector_type=connector_type):
                payload = manager.test_manual_endpoint(
                    connector_type=connector_type,
                    endpoint=f"http://demo.local/{connector_type}",
                    credentials={
                        "api_key": "shared-token",
                        "creality_protocol": "moonraker",
                    },
                )
                self.assertTrue(payload["ok"])
                self.assertEqual(payload["stage"], "connect")
                self.assertEqual(payload["connector_type"], connector_type)
                details = payload["details"]["printer"]
                for key in keys:
                    self.assertIn(key, details)

    def test_onboarding_add_printer_refuses_failed_health_check(self):
        keychain = KeychainStore(service_name="test-eon-printer-manager")
        keychain._memory_fallback.clear()  # noqa: SLF001
        connector = _ScriptedConnector(
            "octoprint",
            connect_result={"ok": False, "state": "missing_config", "message": "OCTOPRINT_API_KEY_REQUIRED: octoprint_api_key is required."},
        )
        registry = _build_registry({"octoprint": connector})
        manager = PrinterManager(
            printers=[],
            airtable_cfg={},
            connector_registry=registry,
            keychain_store=keychain,
        )

        result = manager.onboarding_add_printer(
            {
                "name": "Demo Octo",
                "connector_type": "octoprint",
                "octoprint_url": "http://localhost",
                "octoprint_api_key": "secret-token",
                "printer_id": "printer-octo-01",
            }
        )

        self.assertFalse(result["ok"])
        self.assertEqual(result["state"], "health_check_failed")
        self.assertEqual(result["diagnostic"]["stage"], "connect")
        self.assertEqual(result["diagnostic"]["connector_type"], "octoprint")
        self.assertEqual(manager.printers, [])
        self.assertEqual(keychain.get_secret("printer:printer-octo-01"), "")


if __name__ == "__main__":
    unittest.main()
