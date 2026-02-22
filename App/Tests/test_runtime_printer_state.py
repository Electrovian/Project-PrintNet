import copy
import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config.defaults import DEFAULTS  # noqa: E402
from config.runtime_printer_state import (  # noqa: E402
    RuntimePrinterState,
    runtime_printer_state_from_defaults,
    runtime_printer_state_from_profile,
)
from gui.Windows.controller.ui import UiMixin  # noqa: E402


class _DummyViewer:
    def __init__(self):
        self.last_bed_limits = None

    def set_bed_limits(self, bed_size, max_height):
        self.last_bed_limits = (tuple(bed_size), float(max_height))


class _DummyPrinterManager:
    def __init__(self):
        self.active_printer = None

    def set_active_printer(self, printer):
        self.active_printer = printer


class _DummyStatusBar:
    def __init__(self):
        self.messages = []

    def showMessage(self, message):
        self.messages.append(str(message))


class _DummyUi(UiMixin):
    def __init__(self):
        self.main = self
        self.viewer = _DummyViewer()
        self.printer_manager = _DummyPrinterManager()
        self.runtime_printer_state = runtime_printer_state_from_defaults(DEFAULTS.get("printer", {}))
        self.synced_name = None
        self.warning_refresh_count = 0
        self._status = _DummyStatusBar()

    def statusBar(self):
        return self._status

    def _update_bed_warnings(self):
        self.warning_refresh_count += 1

    def _sync_printer_selection(self, printer, source=None):
        _ = source
        self.synced_name = str(printer.get("name", "")).strip()


class RuntimePrinterStateTests(unittest.TestCase):
    def test_runtime_state_from_defaults(self):
        state = runtime_printer_state_from_defaults(DEFAULTS.get("printer", {}))
        self.assertIsInstance(state, RuntimePrinterState)
        self.assertGreater(state.bed_x, 0.0)
        self.assertGreater(state.bed_y, 0.0)
        self.assertGreater(state.bed_z, 0.0)
        self.assertTrue(state.name)

    def test_runtime_state_from_profile_invalid_values_use_fallback(self):
        fallback = RuntimePrinterState(name="Fallback", bed_x=220.0, bed_y=220.0, bed_z=250.0, source="defaults")
        state = runtime_printer_state_from_profile(
            {"name": "Test", "bed_x": "bad", "bed_y": None, "bed_z": -50},
            fallback_state=fallback,
            source="device",
        )
        self.assertEqual(state.name, "Test")
        self.assertEqual(state.bed_x, 220.0)
        self.assertEqual(state.bed_y, 220.0)
        self.assertEqual(state.bed_z, 250.0)
        self.assertEqual(state.source, "device")

    def test_apply_printer_profile_updates_runtime_state_without_mutating_defaults(self):
        ui = _DummyUi()
        defaults_snapshot = copy.deepcopy(DEFAULTS.get("printer", {}))

        ui._apply_printer_profile({"name": "RuntimePrinter", "bed_x": 300.0, "bed_y": 280.0, "bed_z": 320.0}, source="device")

        self.assertEqual(DEFAULTS.get("printer", {}), defaults_snapshot)
        self.assertEqual(ui.runtime_printer_state.name, "RuntimePrinter")
        self.assertEqual(ui.runtime_printer_state.bed_size, (300.0, 280.0))
        self.assertEqual(ui.runtime_printer_state.bed_z, 320.0)
        self.assertEqual(ui.viewer.last_bed_limits, ((300.0, 280.0), 320.0))
        self.assertEqual(ui.printer_manager.active_printer.get("name"), "RuntimePrinter")
        self.assertEqual(ui.warning_refresh_count, 1)

    def test_effective_bed_limits_prefers_runtime_state(self):
        ui = _DummyUi()
        ui.runtime_printer_state = RuntimePrinterState(
            name="StatePrinter",
            bed_x=400.0,
            bed_y=300.0,
            bed_z=500.0,
            source="runtime",
        )
        bed, z_max, name = ui._effective_bed_limits()
        self.assertEqual(bed, (400.0, 300.0))
        self.assertEqual(z_max, 500.0)
        self.assertEqual(name, "StatePrinter")


if __name__ == "__main__":
    unittest.main()
