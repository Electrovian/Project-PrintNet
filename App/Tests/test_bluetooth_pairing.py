from __future__ import annotations

import os
import sys
import unittest
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from connectors.bluetooth_pairing import BluetoothPairingManager  # noqa: E402


class BluetoothPairingTests(unittest.TestCase):
    def test_discover_uses_hook(self):
        manager = BluetoothPairingManager(
            discovery_hook=lambda _timeout: [{"id": "AA:BB:CC:DD", "name": "Printer BLE"}],
        )
        with mock.patch.object(manager, "is_supported", return_value=True):
            payload = manager.discover(timeout_s=2.0)
        self.assertTrue(payload["ok"])
        self.assertEqual(len(payload["devices"]), 1)

    def test_pair_uses_hook(self):
        manager = BluetoothPairingManager(pair_hook=lambda device_id: {"ok": True, "state": "paired", "device_id": device_id})
        with mock.patch.object(manager, "is_supported", return_value=True):
            payload = manager.pair(device_id="AA:BB")
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["state"], "paired")

    def test_linux_beta_flag_controls_support(self):
        manager = BluetoothPairingManager(linux_beta_env="EON_BLUETOOTH_LINUX_BETA")
        with mock.patch("sys.platform", "linux"), mock.patch.dict(os.environ, {"EON_BLUETOOTH_LINUX_BETA": "0"}, clear=False):
            self.assertFalse(manager.is_supported())
        with mock.patch("sys.platform", "linux"), mock.patch.dict(os.environ, {"EON_BLUETOOTH_LINUX_BETA": "1"}, clear=False):
            self.assertTrue(manager.is_supported())


if __name__ == "__main__":
    unittest.main()
