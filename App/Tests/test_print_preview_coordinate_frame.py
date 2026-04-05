import os
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui.Windows.controller.print import PrintMixin  # noqa: E402
from slicer_v2.legacy_gcode_writer import SliceSettings  # noqa: E402


class _SettingsPanelStub:
    def __init__(self, settings):
        self._settings = settings

    def to_settings(self):
        return self._settings


class _PreviewViewStub:
    def __init__(self):
        self.preview_settings = None
        self.preview_data = None
        self.gcode_text = ""
        self.stats = {}

    def set_gcode_text(self, text):
        self.gcode_text = str(text or "")

    def update_stats(self, stats):
        self.stats = dict(stats or {})

    def set_preview_settings(self, settings):
        self.preview_settings = settings

    def set_preview_data(self, preview):
        self.preview_data = preview


class _ViewerStub:
    def __init__(self):
        self.preview_settings = None
        self.preview_data = None
        self.print_stats = {}

    def set_preview_settings(self, settings):
        self.preview_settings = settings

    def set_gcode_preview(self, preview):
        self.preview_data = preview

    def set_print_stats(self, stats):
        self.print_stats = dict(stats or {})


class _PrinterManagerStub:
    def __init__(self, printer):
        self.active_printer = dict(printer or {})


class _RuntimeStateStub:
    def __init__(self, *, bed_x: float, bed_y: float, bed_z: float):
        self.bed_x = float(bed_x)
        self.bed_y = float(bed_y)
        self.bed_z = float(bed_z)


class _PreviewController(PrintMixin):
    def __init__(self):
        self.settings_panel = _SettingsPanelStub(SliceSettings(bed_x=220.0, bed_y=220.0))
        self.preview_view = _PreviewViewStub()
        self.viewer = _ViewerStub()
        self.printer_manager = _PrinterManagerStub({"name": "RuntimePrinter", "bed_x": 300.0, "bed_y": 280.0})
        self.runtime_printer_state = _RuntimeStateStub(bed_x=300.0, bed_y=280.0, bed_z=250.0)
        self._last_slice_meshes = None
        self._last_gcode_stats = None
        self._last_preview_key = None
        self._last_preview_data = None
        self._last_preview_text = None


class PrintPreviewCoordinateFrameTests(unittest.TestCase):
    def test_update_preview_uses_resolved_bed_dimensions_for_preview_settings(self):
        controller = _PreviewController()
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False, mode="w", encoding="utf-8") as handle:
            handle.write(";LAYER:0\n")
            handle.write("G1 X150 Y140 Z0.20 F1200\n")
            handle.write("G1 X160 Y145 E0.60 F1200\n")
            gcode_path = handle.name
        try:
            controller._update_preview_from_gcode(gcode_path, {"time_seconds": 1.0})

            self.assertIsNotNone(controller.preview_view.preview_settings)
            self.assertEqual(controller.preview_view.preview_settings.bed_x, 300.0)
            self.assertEqual(controller.preview_view.preview_settings.bed_y, 280.0)
            self.assertEqual(controller.viewer.preview_settings.bed_x, 300.0)
            self.assertEqual(controller.viewer.preview_settings.bed_y, 280.0)
        finally:
            if os.path.exists(gcode_path):
                os.remove(gcode_path)


if __name__ == "__main__":
    unittest.main()
