import os
import sys
import tempfile
import unittest
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui.Windows.controller.print import PrintMixin, _sanitize_gcode_basename  # noqa: E402


class _DummySettingsPanel:
    def __init__(self, settings):
        self._settings = settings

    def to_settings(self):
        return self._settings


class _DummyViewer:
    def __init__(self, model_ids=None, paths=None, names=None):
        self._model_ids = list(model_ids or [])
        self._paths = dict(paths or {})
        self._names = dict(names or {})

    def get_model_ids(self):
        return list(self._model_ids)

    def get_model_path(self, model_id):
        return self._paths.get(model_id)

    def get_model_name(self, model_id):
        return self._names.get(model_id)


class _DummyController(PrintMixin):
    def __init__(self):
        self.settings_panel = _DummySettingsPanel({"profile": "default"})
        self.viewer = _DummyViewer([1], {1: "C:/models/part.stl"}, {1: "Part"})
        self.main = type("MainWindowStub", (), {"activity_logger": None})()
        self._last_gcode_path = None
        self._last_slice_signature = None
        self.sent_payloads = []
        self.print_requests = []
        self.slice_requests = 0

    def _build_slice_signature(self, settings):
        if settings == {"profile": "default"}:
            return "sig-default"
        return "sig-other"

    def _send_existing_gcode(self, printer, gcode_path: str):
        self.sent_payloads.append((printer, gcode_path))

    def print_current_plate(self, printer=None):
        self.print_requests.append(printer)

    def slice_current_plate(self):
        self.slice_requests += 1


class _EngineOnlyController(PrintMixin):
    def __init__(self, *, fail: bool):
        self.main = type("MainWindowStub", (), {"activity_logger": None})()
        self._last_slicer_backend = None
        self._fail = bool(fail)
        self.logged_actions = []

    def _runtime_performance(self):
        return {"max_threads": 1, "gpu_mode": "off"}

    def _log_slicer_activity(self, action: str, **payload):
        self.logged_actions.append((action, dict(payload)))

    def _slice_with_v2_pipeline(self, **_kwargs):
        if self._fail:
            raise RuntimeError("v2 failure")
        return "C:/tmp/out.gcode"


class DesktopPlateFlowTests(unittest.TestCase):
    def test_sanitize_gcode_basename(self):
        self.assertEqual(_sanitize_gcode_basename("My Part (v2)"), "My_Part_v2")
        self.assertEqual(_sanitize_gcode_basename(""), "plate")

    def test_default_plate_gcode_basename_for_multi_model_plate(self):
        controller = _DummyController()
        controller.viewer = _DummyViewer([1, 2], {1: "C:/models/a.stl", 2: "C:/models/b.stl"}, {1: "A", 2: "B"})
        self.assertEqual(controller._default_plate_gcode_basename(), "a_plate")

    def test_resolve_reusable_gcode_path_requires_existing_file_and_signature(self):
        controller = _DummyController()
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False) as handle:
            gcode_path = handle.name
        try:
            controller._last_gcode_path = gcode_path
            controller._last_slice_signature = "sig-default"
            reusable = controller._resolve_reusable_gcode_path(controller.settings_panel.to_settings())
            self.assertEqual(reusable, gcode_path)
        finally:
            if os.path.exists(gcode_path):
                os.remove(gcode_path)

    def test_resolve_reusable_gcode_path_rejects_signature_mismatch(self):
        controller = _DummyController()
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False) as handle:
            gcode_path = handle.name
        try:
            controller._last_gcode_path = gcode_path
            controller._last_slice_signature = "sig-old"
            reusable = controller._resolve_reusable_gcode_path(controller.settings_panel.to_settings())
            self.assertIsNone(reusable)
        finally:
            if os.path.exists(gcode_path):
                os.remove(gcode_path)

    def test_device_send_reuses_cached_plate_gcode_when_valid(self):
        controller = _DummyController()
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False) as handle:
            gcode_path = handle.name
        try:
            controller._last_gcode_path = gcode_path
            controller._last_slice_signature = "sig-default"
            controller._on_device_send_requested({"name": "Printer"})
            self.assertEqual(len(controller.sent_payloads), 1)
            self.assertEqual(controller.sent_payloads[0][1], gcode_path)
            self.assertEqual(controller.print_requests, [])
        finally:
            if os.path.exists(gcode_path):
                os.remove(gcode_path)

    def test_device_send_falls_back_to_plate_print_when_cache_invalid(self):
        controller = _DummyController()
        controller._last_gcode_path = "C:/missing/file.gcode"
        controller._last_slice_signature = "sig-default"
        controller._on_device_send_requested({"name": "Printer"})
        self.assertEqual(controller.sent_payloads, [])
        self.assertEqual(len(controller.print_requests), 1)

    def test_alias_methods_route_to_plate_methods(self):
        controller = _DummyController()
        controller.slice_current_model()
        controller.print_current_model(printer={"name": "P1"})
        self.assertEqual(controller.slice_requests, 1)
        self.assertEqual(controller.print_requests, [{"name": "P1"}])

    def test_slicer_engine_preference_is_python_v2_only(self):
        controller = _EngineOnlyController(fail=False)
        with mock.patch.dict(os.environ, {"EON_USE_SLICER_V2": "0"}):
            self.assertEqual(controller._slicer_engine_preference(), "v2")

    def test_slice_with_selected_engine_does_not_fallback(self):
        controller = _EngineOnlyController(fail=True)
        with self.assertRaises(RuntimeError):
            controller._slice_with_selected_engine(
                meshes=[],
                combined_mesh=None,  # type: ignore[arg-type]
                settings=None,  # type: ignore[arg-type]
                source_path="C:/models/part.stl",
                output_gcode_path=None,
            )
        self.assertEqual(controller._last_slicer_backend, "v2")
        self.assertTrue(any(item[0] == "slice_engine_error" for item in controller.logged_actions))


if __name__ == "__main__":
    unittest.main()
