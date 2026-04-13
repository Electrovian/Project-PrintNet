import os
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

import trimesh

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config.runtime_printer_state import RuntimePrinterState  # noqa: E402
from gui.Windows.controller.print import PrintMixin  # noqa: E402
from integrations.printer_manager import PrinterManager  # noqa: E402
from slicer_v2 import service as slicer_service  # noqa: E402
from slicer_v2.legacy_gcode_writer import SliceSettings  # noqa: E402


def _tiny_mesh() -> trimesh.Trimesh:
    return trimesh.Trimesh(
        vertices=[
            (0.0, 0.0, 0.0),
            (10.0, 0.0, 0.0),
            (0.0, 10.0, 0.0),
        ],
        faces=[(0, 1, 2)],
        process=False,
    )


class _PrinterManagerStub:
    def __init__(self, printer):
        self.active_printer = printer


class _PipelineController(PrintMixin):
    def __init__(self, printer):
        self.main = type("MainWindowStub", (), {"activity_logger": None})()
        self.printer_manager = _PrinterManagerStub(printer)
        self.runtime_printer_state = RuntimePrinterState(
            name="RuntimePrinter",
            bed_x=300.0,
            bed_y=280.0,
            bed_z=320.0,
            source="runtime",
        )


class OutputContractPlumbingTests(unittest.TestCase):
    def test_desktop_legacy_slice_path_enriches_output_contract_settings(self) -> None:
        controller = _PipelineController({"connector_type": "moonraker"})
        mesh = _tiny_mesh()
        settings = SliceSettings()
        captured: dict[str, object] = {}

        with tempfile.TemporaryDirectory() as temp_dir:
            out_path = os.path.join(temp_dir, "legacy.gcode")

            def _fake_slice_trimesh_auto(**kwargs):
                captured["settings"] = kwargs["settings"]
                return out_path

            with mock.patch("gui.Windows.controller.print.slice_v2_trimesh_auto", side_effect=_fake_slice_trimesh_auto):
                result = controller._slice_with_v2_pipeline(
                    meshes=[mesh],
                    combined_mesh=mesh,
                    settings=settings,
                    source_path="C:/models/part.stl",
                    output_gcode_path=out_path,
                    perf={"max_threads": 1, "gpu_mode": "off"},
                )

        self.assertEqual(result["gcode_path"], out_path)
        self.assertIn("support_diagnostics", result)
        resolved_settings = captured["settings"]
        self.assertIsInstance(resolved_settings, SliceSettings)
        self.assertEqual(resolved_settings.bed_x, 300.0)
        self.assertEqual(resolved_settings.bed_y, 280.0)
        self.assertFalse(resolved_settings.gcode_absolute_extrusion)
        self.assertEqual(resolved_settings.firmware_flavor, "klipper")

    def test_desktop_legacy_slice_path_skips_semantic_pipeline_when_detailed_path_succeeds(self) -> None:
        controller = _PipelineController({"connector_type": "moonraker"})
        mesh = _tiny_mesh()

        with tempfile.TemporaryDirectory() as temp_dir:
            out_path = os.path.join(temp_dir, "legacy.gcode")
            with mock.patch("gui.Windows.controller.print.slice_v2_trimesh_auto", return_value=out_path):
                with mock.patch("gui.Windows.controller.print.create_v2_context") as patched_create_context:
                    with mock.patch("gui.Windows.controller.print.run_v2_pipeline") as patched_run_pipeline:
                        result = controller._slice_with_v2_pipeline(
                            meshes=[mesh],
                            combined_mesh=mesh,
                            settings=SliceSettings(),
                            source_path="C:/models/part.stl",
                            output_gcode_path=out_path,
                            perf={"max_threads": 1, "gpu_mode": "off"},
                        )

        self.assertEqual(result["gcode_path"], out_path)
        patched_create_context.assert_not_called()
        patched_run_pipeline.assert_not_called()

    def test_desktop_legacy_slice_path_marks_support_diagnostics_unavailable_without_semantic_pass(self) -> None:
        controller = _PipelineController({"connector_type": "moonraker"})
        mesh = _tiny_mesh()
        settings = SliceSettings(support_enabled=True, support_type="tree", support_style="organic")

        with tempfile.TemporaryDirectory() as temp_dir:
            out_path = os.path.join(temp_dir, "legacy_supports.gcode")
            with mock.patch("gui.Windows.controller.print.slice_v2_trimesh_auto", return_value=out_path):
                with mock.patch("gui.Windows.controller.print.create_v2_context") as patched_create_context:
                    result = controller._slice_with_v2_pipeline(
                        meshes=[mesh],
                        combined_mesh=mesh,
                        settings=settings,
                        source_path="C:/models/part.stl",
                        output_gcode_path=out_path,
                        perf={"max_threads": 1, "gpu_mode": "off"},
                    )

        self.assertEqual(result["support_diagnostics"]["status"], "unavailable")
        self.assertEqual(result["support_diagnostics"]["support_style"], "organic")
        self.assertIn(
            "support_planning:diagnostics_unavailable",
            result["support_diagnostics"]["warnings"],
        )
        patched_create_context.assert_not_called()

    def test_desktop_semantic_fallback_uses_strict_contract_settings(self) -> None:
        controller = _PipelineController({"connector_type": "moonraker"})
        mesh = _tiny_mesh()
        settings = SliceSettings()
        captured: dict[str, object] = {}

        def _fake_create_context(**kwargs):
            captured["resolved_settings"] = dict(kwargs["resolved_settings"])
            return SimpleNamespace(stage_artifacts={})

        fake_result = SimpleNamespace(
            context=SimpleNamespace(stage_artifacts={"gcode": {"lines": ["G21", "G90", "G0 X150 Y140"]}})
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            out_path = os.path.join(temp_dir, "semantic.gcode")
            with mock.patch("gui.Windows.controller.print.slice_v2_trimesh_auto", side_effect=RuntimeError("legacy failed")):
                with mock.patch("gui.Windows.controller.print.create_v2_context", side_effect=_fake_create_context):
                    with mock.patch("gui.Windows.controller.print.run_v2_pipeline", return_value=fake_result):
                        result = controller._slice_with_v2_pipeline(
                            meshes=[mesh],
                            combined_mesh=mesh,
                            settings=settings,
                            source_path="C:/models/part.stl",
                            output_gcode_path=out_path,
                            perf={"max_threads": 1, "gpu_mode": "off"},
                        )

        self.assertEqual(result["gcode_path"], out_path)
        self.assertIn("support_diagnostics", result)
        resolved_settings = captured["resolved_settings"]
        self.assertEqual(resolved_settings["bed_x"], 300.0)
        self.assertEqual(resolved_settings["bed_y"], 280.0)
        self.assertEqual(resolved_settings["gcode_validation_bed_x_mm"], 300.0)
        self.assertEqual(resolved_settings["gcode_validation_bed_y_mm"], 280.0)
        self.assertFalse(resolved_settings["gcode_validation_allow_negative_xy"])
        self.assertFalse(resolved_settings["gcode_absolute_extrusion"])
        self.assertEqual(resolved_settings["gcode_firmware_flavor"], "klipper")

    def test_service_slice_file_enriches_printer_output_contract(self) -> None:
        captured: dict[str, object] = {}

        def _fake_create_context(**kwargs):
            captured["resolved_settings"] = dict(kwargs["resolved_settings"])
            return SimpleNamespace(stage_artifacts={})

        fake_result = SimpleNamespace(
            context=SimpleNamespace(stage_artifacts={"gcode": {"lines": ["G21", "G90", "G0 X150 Y140"]}})
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            stl_path = os.path.join(temp_dir, "input.stl")
            out_path = os.path.join(temp_dir, "output.gcode")
            with open(stl_path, "w", encoding="utf-8") as handle:
                handle.write("solid test\nendsolid test\n")
            with mock.patch("slicer_v2.service.create_context", side_effect=_fake_create_context):
                with mock.patch("slicer_v2.service.run_pipeline", return_value=fake_result):
                    slicer_service.slice_file(
                        stl_path,
                        output_gcode_path=out_path,
                        settings=SliceSettings(),
                        printer={"connector_type": "moonraker", "bed_x": 300.0, "bed_y": 280.0},
                    )

        resolved_settings = captured["resolved_settings"]
        self.assertEqual(resolved_settings["bed_x"], 300.0)
        self.assertEqual(resolved_settings["bed_y"], 280.0)
        self.assertEqual(resolved_settings["gcode_validation_bed_x_mm"], 300.0)
        self.assertEqual(resolved_settings["gcode_validation_bed_y_mm"], 280.0)
        self.assertFalse(resolved_settings["gcode_absolute_extrusion"])
        self.assertFalse(resolved_settings["gcode_validation_allow_negative_xy"])
        self.assertEqual(resolved_settings["gcode_firmware_flavor"], "klipper")

    def test_printer_manager_slice_and_print_passes_active_printer_to_service(self) -> None:
        manager = PrinterManager(printers=[{"name": "Printer", "bed_x": 300.0, "bed_y": 280.0}], airtable_cfg={})
        settings = SliceSettings()
        with mock.patch("integrations.printer_manager.slice_file", return_value="C:/tmp/out.gcode") as patched_slice:
            with mock.patch.object(manager, "print_gcode", return_value="ok") as patched_print:
                result = manager.slice_and_print("C:/tmp/input.stl", settings)

        self.assertEqual(result, "ok")
        self.assertEqual(patched_slice.call_args.kwargs["printer"], manager.active_printer)
        patched_print.assert_called_once_with("C:/tmp/out.gcode", printer=manager.active_printer)


if __name__ == "__main__":
    unittest.main()
