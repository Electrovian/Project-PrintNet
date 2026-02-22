import unittest

from gui.printer_selection import find_printer_index, printer_identity, sync_printer_selection


class _DummyView:
    def __init__(self):
        self.calls = []

    def select_printer(self, printer, emit=True):
        self.calls.append(("select_printer", printer, emit))


class _DummyByNameView:
    def __init__(self):
        self.calls = []

    def select_printer_by_name(self, name, emit=True):
        self.calls.append(("select_printer_by_name", name, emit))


class PrinterSelectionSyncTests(unittest.TestCase):
    def test_printer_identity_includes_name_connector_endpoint(self):
        printer = {
            "name": "K1",
            "connector_type": "moonraker",
            "moonraker_url": "http://k1.local",
        }
        self.assertEqual(
            printer_identity(printer),
            ("k1", "moonraker", "http://k1.local"),
        )

    def test_find_printer_index_prefers_exact_match_over_name_only(self):
        printers = [
            {
                "name": "SharedName",
                "connector_type": "octoprint",
                "octoprint_url": "http://octo.local",
            },
            {
                "name": "SharedName",
                "connector_type": "moonraker",
                "moonraker_url": "http://moon.local",
            },
        ]
        target = {
            "name": "SharedName",
            "connector_type": "moonraker",
            "moonraker_url": "http://moon.local",
        }
        self.assertEqual(find_printer_index(printers, target), 1)

    def test_find_printer_index_falls_back_to_name(self):
        printers = [
            {"name": "Alpha"},
            {"name": "Beta"},
        ]
        target = {"name": "Beta", "connector_type": "prusalink"}
        self.assertEqual(find_printer_index(printers, target), 1)

    def test_sync_printer_selection_skips_source_and_uses_structured_selector(self):
        settings = _DummyView()
        device = _DummyView()
        control = _DummyView()
        preview = _DummyView()
        printer = {"name": "P1", "connector_type": "octoprint", "octoprint_url": "http://p1.local"}

        sync_printer_selection(
            printer=printer,
            source="device",
            settings_view=settings,
            device_view=device,
            control_view=control,
            preview_view=preview,
        )

        self.assertEqual(len(settings.calls), 1)
        self.assertEqual(len(device.calls), 0)
        self.assertEqual(len(control.calls), 1)
        self.assertEqual(len(preview.calls), 1)
        self.assertEqual(settings.calls[0][0], "select_printer")
        self.assertEqual(settings.calls[0][2], False)

    def test_sync_printer_selection_uses_name_fallback_selector(self):
        settings = _DummyByNameView()
        printer = {"name": "FallbackPrinter"}

        sync_printer_selection(printer=printer, source=None, settings_view=settings)

        self.assertEqual(settings.calls, [("select_printer_by_name", "fallbackprinter", False)])


if __name__ == "__main__":
    unittest.main()

