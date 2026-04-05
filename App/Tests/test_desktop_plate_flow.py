import json
import os
import sys
import tempfile
import unittest
from dataclasses import dataclass, replace
from types import SimpleNamespace
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui.Windows.controller.print import PrintMixin, _sanitize_gcode_basename, _settings_to_dict  # noqa: E402
from slicer_v2.legacy_gcode_writer import SliceSettings  # noqa: E402


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


class _SignatureViewer:
    def __init__(self, plate_name: str = "Plate A"):
        self._plate_name = plate_name
        self.models = {
            1: {
                "object_id": 11,
                "plate_id": 22,
            }
        }

    def get_model_ids(self):
        return [1]

    def get_model_path(self, model_id):
        return f"C:/models/{model_id}.stl"

    def get_model_name(self, model_id):
        return f"Model {model_id}"

    def get_model_transform(self, model_id):
        return ([1.0, 1.0, 1.0], [0.0, 0.0, 0.0])

    def get_model_rotation(self, model_id):
        return [0.0, 0.0, 0.0]

    def get_current_plate_id(self):
        return 7

    def get_current_plate_name(self):
        return self._plate_name


class _SignatureController(PrintMixin):
    def __init__(self, plate_name: str = "Plate A"):
        self.viewer = _SignatureViewer(plate_name=plate_name)
        self.main = type("MainWindowStub", (), {"activity_logger": None})()
        self.logged_actions = []

    def _log_slicer_activity(self, action: str, **payload):
        self.logged_actions.append((action, dict(payload)))


class _EngineOnlyController(PrintMixin):
    def __init__(self, *, fail: bool, payload=None):
        self.main = type("MainWindowStub", (), {"activity_logger": None})()
        self._last_slicer_backend = None
        self._fail = bool(fail)
        self._payload = payload
        self.logged_actions = []

    def _runtime_performance(self):
        return {"max_threads": 1, "gpu_mode": "off"}

    def _log_slicer_activity(self, action: str, **payload):
        self.logged_actions.append((action, dict(payload)))

    def _slice_with_v2_pipeline(self, **_kwargs):
        if self._fail:
            raise RuntimeError("v2 failure")
        if self._payload is not None:
            return self._payload
        return "C:/tmp/out.gcode"


class _PreviewViewStub:
    def __init__(self):
        self.gcode_text = ""
        self.stats = {}
        self.preview_settings = None
        self.preview_data = None

    def set_gcode_text(self, text):
        self.gcode_text = str(text or "")

    def update_stats(self, stats):
        self.stats = dict(stats or {})

    def set_preview_settings(self, settings):
        self.preview_settings = settings

    def set_preview_data(self, preview):
        self.preview_data = preview


class _ViewerPreviewStub:
    def __init__(self):
        self.print_stats = {}
        self.preview_settings = None
        self.preview_data = None

    def set_print_stats(self, stats):
        self.print_stats = dict(stats or {})

    def set_preview_settings(self, settings):
        self.preview_settings = settings

    def set_gcode_preview(self, preview):
        self.preview_data = preview


class _UpdatePreviewController(PrintMixin):
    def __init__(self):
        self.settings_panel = _DummySettingsPanel(SliceSettings())
        self.preview_view = _PreviewViewStub()
        self.viewer = _ViewerPreviewStub()
        self._last_slice_meshes = None
        self._last_gcode_stats = None
        self._last_preview_key = None
        self._last_preview_data = None
        self._last_preview_text = None
        self.logged_actions = []

    def _log_slicer_activity(self, action: str, **payload):
        self.logged_actions.append((action, dict(payload)))


class DesktopPlateFlowTests(unittest.TestCase):
    def test_sanitize_gcode_basename(self):
        self.assertEqual(_sanitize_gcode_basename("My Part (v2)"), "My_Part_v2")
        self.assertEqual(_sanitize_gcode_basename(""), "plate")

    def test_settings_to_dict_handles_dataclass_mapping_and_namespace(self):
        @dataclass
        class _ExampleSettings:
            profile: str
            nozzle_temperature_c: int

        self.assertEqual(
            _settings_to_dict(_ExampleSettings(profile="draft", nozzle_temperature_c=215)),
            {"profile": "draft", "nozzle_temperature_c": 215},
        )
        self.assertEqual(_settings_to_dict({"profile": "default"}), {"profile": "default"})
        self.assertEqual(
            _settings_to_dict(SimpleNamespace(profile="fast", _private="ignore")),
            {"profile": "fast"},
        )

    def test_default_plate_gcode_basename_for_multi_model_plate(self):
        controller = _DummyController()
        controller.viewer = _DummyViewer([1, 2], {1: "C:/models/a.stl", 2: "C:/models/b.stl"}, {1: "A", 2: "B"})
        self.assertEqual(controller._default_plate_gcode_basename(), "a_plate")

    def test_build_slice_signature_changes_with_plate_name(self):
        settings = SliceSettings()
        controller = _SignatureController(plate_name="Plate A")
        first = controller._build_slice_signature(settings)
        controller.viewer._plate_name = "Plate B"
        second = controller._build_slice_signature(settings)
        self.assertNotEqual(first, second)
        self.assertEqual(json.loads(first)["plate_name"], "Plate A")
        self.assertEqual(json.loads(second)["plate_name"], "Plate B")

    def test_build_slice_signature_changes_with_settings(self):
        settings = SliceSettings()
        controller = _SignatureController(plate_name="Plate A")
        first = controller._build_slice_signature(settings)
        changed = controller._build_slice_signature(replace(settings, nozzle_temperature_c=215))
        self.assertNotEqual(first, changed)

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

    def test_resolve_reusable_gcode_path_logs_cache_hit(self):
        controller = _SignatureController()
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False) as handle:
            gcode_path = handle.name
        try:
            settings = SliceSettings()
            controller._last_gcode_path = gcode_path
            controller._last_slice_signature = controller._build_slice_signature(settings)
            reusable = controller._resolve_reusable_gcode_path(settings)
            self.assertEqual(reusable, gcode_path)
            self.assertTrue(any(action == "slice_cache_hit" for action, _ in controller.logged_actions))
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

    def test_normalize_slice_result_marks_missing_support_diagnostics_unavailable(self):
        controller = _EngineOnlyController(fail=False)
        settings = replace(
            SliceSettings(),
            support_enabled=True,
            support_type="tree",
            support_style="organic",
        )
        payload = controller._normalize_slice_result_payload("C:/tmp/out.gcode", settings)
        self.assertEqual(payload["gcode_path"], "C:/tmp/out.gcode")
        self.assertEqual(payload["support_diagnostics"]["status"], "unavailable")
        self.assertEqual(payload["support_diagnostics"]["support_style"], "organic")
        self.assertIn(
            "support_planning:diagnostics_unavailable",
            payload["support_diagnostics"]["warnings"],
        )

    def test_slice_with_selected_engine_preserves_support_diagnostics_payload(self):
        controller = _EngineOnlyController(
            fail=False,
            payload={
                "gcode_path": "C:/tmp/out.gcode",
                "support_diagnostics": {
                    "support_enabled": True,
                    "support_type": "tree",
                    "support_style": "organic",
                    "support_region_count": 2,
                    "support_path_count": 5,
                    "warnings": ["support_planning:tree_style=organic"],
                },
            },
        )
        result = controller._slice_with_selected_engine(
            meshes=[],
            combined_mesh=None,  # type: ignore[arg-type]
            settings=replace(SliceSettings(), support_enabled=True, support_type="tree", support_style="organic"),
            source_path="C:/models/part.stl",
            output_gcode_path=None,
        )
        self.assertEqual(result["gcode_path"], "C:/tmp/out.gcode")
        self.assertEqual(result["support_diagnostics"]["support_style"], "organic")
        self.assertIn("support_planning:tree_style=organic", result["support_diagnostics"]["warnings"])
        self.assertTrue(
            any(
                action == "slice_success" and payload.get("support_status")
                for action, payload in controller.logged_actions
            )
        )

    def test_update_preview_recovers_when_primary_preview_parser_fails(self):
        controller = _UpdatePreviewController()
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False, mode="w", encoding="utf-8") as handle:
            handle.write(";LAYER:0\n")
            handle.write("G1 X0 Y0 Z0.20 F1200\n")
            handle.write("G1 X10 Y0 E0.60 F1200\n")
            gcode_path = handle.name
        try:
            with mock.patch(
                "gui.Windows.controller.print.parse_gcode_preview_file",
                side_effect=RuntimeError("preview parse boom"),
            ):
                controller._update_preview_from_gcode(gcode_path, {"time_seconds": 1.0})
            self.assertIn("G1 X10 Y0 E0.60", controller.preview_view.gcode_text)
            self.assertIsNotNone(controller.preview_view.preview_data)
            self.assertIsNotNone(controller.viewer.preview_data)
            self.assertIn("preview_parse_error", controller.preview_view.stats)
            self.assertTrue(any(action == "preview_parse_error" for action, _ in controller.logged_actions))
        finally:
            if os.path.exists(gcode_path):
                os.remove(gcode_path)

    def test_update_preview_preserves_support_diagnostics(self):
        controller = _UpdatePreviewController()
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False, mode="w", encoding="utf-8") as handle:
            handle.write(";LAYER:0\n")
            handle.write("G1 X0 Y0 Z0.20 F1200\n")
            handle.write("G1 X10 Y0 E0.60 F1200\n")
            gcode_path = handle.name
        try:
            support_diagnostics = {
                "status": "warnings",
                "support_type": "tree",
                "support_style": "organic",
                "support_region_count": 3,
                "support_path_count": 7,
                "warnings": ["support_planning:tree_style=organic"],
            }
            controller._update_preview_from_gcode(
                gcode_path,
                {
                    "time_seconds": 1.0,
                    "support_diagnostics": support_diagnostics,
                },
            )
            self.assertEqual(
                controller.preview_view.stats["support_diagnostics"]["support_style"],
                "organic",
            )
            self.assertEqual(
                controller.viewer.print_stats["support_diagnostics"]["support_region_count"],
                3,
            )
        finally:
            if os.path.exists(gcode_path):
                os.remove(gcode_path)


if __name__ == "__main__":
    unittest.main()
