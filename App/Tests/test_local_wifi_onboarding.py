import os
import sys
import unittest
from typing import Any, Mapping

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from connectors.local_wifi import LocalWifiOnboarding  # noqa: E402
from connectors.local_wifi import LocalWifiOnboardingError  # noqa: E402
from integrations.printer_manager import PrinterManager  # noqa: E402


def _probe_map_by_port(target, _timeout_s: float) -> Mapping[str, Any]:
    if target.path == "/api/version" and int(target.port) == 80:
        return {"ok": True, "connector_type": "octoprint"}
    if target.path == "/api/version" and int(target.port) == 8080:
        return {"ok": True, "connector_type": "prusalink"}
    if target.path == "/server/info" and int(target.port) == 7125:
        return {"ok": True, "connector_type": "moonraker"}
    return {"ok": False}


def _probe_with_bambu_and_creality(target, _timeout_s: float) -> Mapping[str, Any]:
    if target.path == "/api/v1/status" and int(target.port) == 9999:
        return {"ok": True, "connector_type": "bambu_lan"}
    if target.path == "/server/info" and int(target.port) == 7125:
        return {"ok": True, "connector_type": "creality"}
    return {"ok": False}


def _probe_creality_server_info_on_8080(target, _timeout_s: float) -> Mapping[str, Any]:
    if target.path == "/server/info" and int(target.port) == 8080:
        return {"ok": True, "connector_type": "creality"}
    return {"ok": False}


def _probe_creality_on_server_info_and_api_printer(target, _timeout_s: float) -> Mapping[str, Any]:
    if int(target.port) != 8080:
        return {"ok": False}
    if target.path == "/server/info":
        return {"ok": True, "connector_type": "creality"}
    if target.path == "/api/printer":
        return {"ok": True, "connector_type": "creality"}
    return {"ok": False}


class LocalWifiOnboardingTests(unittest.TestCase):
    def test_discover_requires_hosts(self):
        onboarding = LocalWifiOnboarding(probe_hook=_probe_map_by_port)
        with self.assertRaises(LocalWifiOnboardingError):
            onboarding.discover(hosts=[], ports=[80])

    def test_discover_detects_supported_protocols(self):
        onboarding = LocalWifiOnboarding(probe_hook=_probe_map_by_port)
        result = onboarding.discover(
            hosts=["10.0.0.42"],
            ports=[80, 8080, 7125],
            max_targets=64,
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["printer_count"], 3)
        connector_types = sorted(item.get("connector_type", "") for item in result["printers"])
        self.assertEqual(connector_types, ["moonraker", "octoprint", "prusalink"])

    def test_discover_from_cidr_applies_host_limit(self):
        onboarding = LocalWifiOnboarding(probe_hook=lambda *_args, **_kwargs: {"ok": False})
        result = onboarding.discover_from_cidr(
            "192.168.20.0/29",
            host_limit=3,
            ports=[80],
            max_targets=12,
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["cidr_host_count"], 3)
        self.assertEqual(result["scanned_target_count"], 12)

    def test_merge_printers_deduplicates_connector_url_entries(self):
        onboarding = LocalWifiOnboarding(probe_hook=_probe_map_by_port)
        existing = [
            {
                "name": "Existing Octo",
                "connector_type": "octoprint",
                "octoprint_url": "http://10.0.0.11:80",
                "octoprint_api_key": "abc",
            }
        ]
        discovered = [
            {
                "name": "Duplicate Octo",
                "connector_type": "octoprint",
                "octoprint_url": "http://10.0.0.11:80",
                "octoprint_api_key": "",
            },
            {
                "name": "Moon Device",
                "connector_type": "moonraker",
                "moonraker_url": "http://10.0.0.12:7125",
                "moonraker_token": "",
            },
        ]
        merged = onboarding.merge_printers(existing, discovered)
        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0]["name"], "Existing Octo")
        self.assertEqual(merged[1]["connector_type"], "moonraker")

    def test_printer_manager_discovery_merges_into_runtime_list(self):
        onboarding = LocalWifiOnboarding(probe_hook=_probe_map_by_port)
        manager = PrinterManager(
            printers=[],
            airtable_cfg={},
            wifi_onboarding=onboarding,
        )
        report = manager.discover_local_wifi_printers(
            hosts=["127.0.0.1"],
            ports=[80, 8080, 7125],
            max_targets=32,
        )
        self.assertTrue(report["ok"])
        self.assertEqual(report["printer_count"], 3)
        self.assertEqual(report["merged_printer_count"], 3)
        self.assertEqual(len(manager.printers), 3)
        self.assertIsNotNone(manager.active_printer)

    def test_printer_manager_discovery_returns_invalid_config(self):
        manager = PrinterManager(
            printers=[],
            airtable_cfg={},
            wifi_onboarding=LocalWifiOnboarding(probe_hook=_probe_map_by_port),
        )
        report = manager.discover_local_wifi_printers(hosts=[], ports=[80])
        self.assertFalse(report["ok"])
        self.assertEqual(report["state"], "invalid_config")
        self.assertIn("WIFI_HOSTS_REQUIRED", report["message"])

    def test_discover_detects_bambu_and_creality_signatures(self):
        onboarding = LocalWifiOnboarding(probe_hook=_probe_with_bambu_and_creality)
        result = onboarding.discover(hosts=["10.0.0.55"], ports=[7125, 9999], max_targets=32)
        self.assertTrue(result["ok"])
        connector_types = sorted(item.get("connector_type", "") for item in result["printers"])
        self.assertEqual(connector_types, ["bambu_lan", "creality"])

    def test_creality_server_info_on_non_default_port_keeps_moonraker_protocol(self):
        onboarding = LocalWifiOnboarding(probe_hook=_probe_creality_server_info_on_8080)
        result = onboarding.discover(hosts=["10.0.0.55"], ports=[8080], max_targets=32)
        self.assertTrue(result["ok"])
        self.assertEqual(result["printer_count"], 1)
        printer = result["printers"][0]
        self.assertEqual(printer.get("connector_type"), "creality")
        self.assertEqual(printer.get("creality_protocol"), "moonraker")

    def test_creality_probes_across_paths_are_deduplicated_with_moonraker_preference(self):
        onboarding = LocalWifiOnboarding(probe_hook=_probe_creality_on_server_info_and_api_printer)
        result = onboarding.discover(hosts=["10.0.0.55"], ports=[8080], max_targets=32)
        self.assertTrue(result["ok"])
        self.assertEqual(result["printer_count"], 1)
        printer = result["printers"][0]
        self.assertEqual(printer.get("connector_type"), "creality")
        self.assertEqual(printer.get("creality_protocol"), "moonraker")


if __name__ == "__main__":
    unittest.main()
