import os
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from connectors.errors import UnsupportedConnectorError  # noqa: E402
from connectors.registry import build_default_connector_registry  # noqa: E402
from integrations.printer_manager import PrinterManager  # noqa: E402


class ConnectorRegistryTests(unittest.TestCase):
    def test_default_registry_contains_expected_connector_types(self):
        registry = build_default_connector_registry()
        types = registry.connector_types()
        self.assertIn("local_file", types)
        self.assertIn("prusalink", types)
        self.assertIn("moonraker", types)
        self.assertIn("octoprint", types)
        self.assertIn("octoprint_legacy", types)

    def test_registry_resolve_uses_explicit_connector_type(self):
        registry = build_default_connector_registry()
        connector = registry.resolve({"name": "P1", "connector_type": "local_file"})
        self.assertEqual(connector.connector_type, "local_file")

    def test_registry_resolve_infers_octoprint(self):
        registry = build_default_connector_registry()
        connector = registry.resolve({"name": "P2", "octoprint_url": "http://localhost"})
        self.assertEqual(connector.connector_type, "octoprint")

    def test_registry_resolve_infers_moonraker(self):
        registry = build_default_connector_registry()
        connector = registry.resolve({"name": "P3", "moonraker_url": "http://localhost:7125"})
        self.assertEqual(connector.connector_type, "moonraker")

    def test_registry_resolve_infers_prusalink(self):
        registry = build_default_connector_registry()
        connector = registry.resolve({"name": "P4", "prusalink_url": "http://localhost:8080"})
        self.assertEqual(connector.connector_type, "prusalink")

    def test_registry_get_raises_for_unknown_connector(self):
        registry = build_default_connector_registry()
        with self.assertRaises(UnsupportedConnectorError):
            registry.get("not_real")

    def test_printer_manager_local_connector_message(self):
        registry = build_default_connector_registry()
        manager = PrinterManager(printers=[], airtable_cfg={}, connector_registry=registry)
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False) as handle:
            handle.write(b"G28\n")
            path = handle.name
        try:
            message = manager.print_gcode(path, printer={"name": "Local", "connector_type": "local_file"})
            self.assertIn("Local queue placeholder", message)
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_printer_manager_octoprint_legacy_message(self):
        registry = build_default_connector_registry()
        manager = PrinterManager(printers=[], airtable_cfg={}, connector_registry=registry)
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False) as handle:
            handle.write(b"G28\n")
            path = handle.name
        try:
            message = manager.print_gcode(
                path,
                printer={
                    "name": "Legacy Octo",
                    "connector_type": "octoprint_legacy",
                    "octoprint_url": "http://localhost",
                    "octoprint_api_key": "",
                },
            )
            self.assertIn("OctoPrint API key not configured", message)
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_printer_manager_octoprint_missing_key_message(self):
        registry = build_default_connector_registry()
        manager = PrinterManager(printers=[], airtable_cfg={}, connector_registry=registry)
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False) as handle:
            handle.write(b"G28\n")
            path = handle.name
        try:
            message = manager.print_gcode(
                path,
                printer={
                    "name": "Octo",
                    "connector_type": "octoprint",
                    "octoprint_url": "http://localhost",
                    "octoprint_api_key": "",
                },
            )
            self.assertIn("OCTOPRINT_API_KEY_REQUIRED", message)
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_printer_manager_moonraker_missing_url_message(self):
        registry = build_default_connector_registry()
        manager = PrinterManager(printers=[], airtable_cfg={}, connector_registry=registry)
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False) as handle:
            handle.write(b"G28\n")
            path = handle.name
        try:
            message = manager.print_gcode(
                path,
                printer={
                    "name": "Moon",
                    "connector_type": "moonraker",
                    "moonraker_url": "",
                },
            )
            self.assertIn("MOONRAKER_URL_REQUIRED", message)
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_printer_manager_prusalink_missing_url_message(self):
        registry = build_default_connector_registry()
        manager = PrinterManager(printers=[], airtable_cfg={}, connector_registry=registry)
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False) as handle:
            handle.write(b"G28\n")
            path = handle.name
        try:
            message = manager.print_gcode(
                path,
                printer={
                    "name": "Prusa",
                    "connector_type": "prusalink",
                    "prusalink_url": "",
                },
            )
            self.assertIn("PRUSALINK_URL_REQUIRED", message)
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_printer_manager_unknown_connector_error_message(self):
        registry = build_default_connector_registry()
        manager = PrinterManager(printers=[], airtable_cfg={}, connector_registry=registry)
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False) as handle:
            handle.write(b"G28\n")
            path = handle.name
        try:
            message = manager.print_gcode(path, printer={"name": "Bad", "connector_type": "unknown_connector"})
            self.assertIn("Printer connector error:", message)
        finally:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
