from __future__ import annotations

import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from integrations.printer_manager import PrinterManager  # noqa: E402
from security.keychain_store import KeychainStore  # noqa: E402


class PrinterOnboardingTests(unittest.TestCase):
    def test_onboarding_add_printer_runs_health_check_and_stores(self):
        keychain = KeychainStore(service_name="test-eon")
        manager = PrinterManager(printers=[], airtable_cfg={}, keychain_store=keychain)
        result = manager.onboarding_add_printer(
            {
                "name": "Local Test",
                "connector_type": "local_file",
                "endpoint": "local://queue",
                "printer_id": "printer-local-01",
                "api_key": "secret-token",
            }
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["state"], "saved")
        self.assertEqual(len(manager.printers), 1)
        self.assertNotIn("api_key", manager.printers[0])
        hydrated = manager.hydrate_printer_credentials({"printer_id": "printer-local-01"})
        self.assertEqual(hydrated.get("api_key"), "secret-token")

    def test_manual_endpoint_requires_values(self):
        manager = PrinterManager(printers=[], airtable_cfg={})
        missing_type = manager.test_manual_endpoint(connector_type="", endpoint="http://localhost")
        self.assertFalse(missing_type["ok"])
        missing_endpoint = manager.test_manual_endpoint(connector_type="octoprint", endpoint="")
        self.assertFalse(missing_endpoint["ok"])


if __name__ == "__main__":
    unittest.main()
