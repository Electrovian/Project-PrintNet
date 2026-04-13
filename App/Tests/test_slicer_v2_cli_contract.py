import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.cli import main as slicer_v2_cli_main  # noqa: E402
from slicer_v2.cli_contract import CliExitCode  # noqa: E402


def _write_minimal_stl(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "solid eon",
                "facet normal 0 0 1",
                "outer loop",
                "vertex 0 0 0",
                "vertex 1 0 0",
                "vertex 0 1 0",
                "endloop",
                "endfacet",
                "endsolid eon",
            ]
        ),
        encoding="utf-8",
    )


def _write_profile(path: Path, profile_type: str, extra: dict[str, object] | None = None) -> None:
    payload: dict[str, object] = {"type": profile_type, "name": f"{profile_type}_preset"}
    if extra:
        payload.update(extra)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


class TestSlicerV2CliContract(unittest.TestCase):
    def test_cli_happy_path_writes_result_and_gcode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mesh = root / "part.stl"
            _write_minimal_stl(mesh)

            machine = root / "machine.json"
            process = root / "process.json"
            filament = root / "filament.json"
            _write_profile(machine, "machine", {"gcode_validation_bed_x_mm": 180})
            _write_profile(process, "process", {"layer_height": 0.24, "infill_percent": 18})
            _write_profile(filament, "filament", {"filament_density": 1.25})

            outdir = root / "out"
            result_path = root / "result.json"
            exit_code = slicer_v2_cli_main(
                [
                    "--mesh-path",
                    str(mesh),
                    "--load-settings",
                    str(machine),
                    "--load-settings",
                    str(process),
                    "--load-filaments",
                    str(filament),
                    "--outputdir",
                    str(outdir),
                    "--result-path",
                    str(result_path),
                ]
            )

            self.assertEqual(exit_code, int(CliExitCode.CLI_SUCCESS))
            payload = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["return_code"], int(CliExitCode.CLI_SUCCESS))
            self.assertEqual(payload["plate_index"], 1)
            self.assertIn("prepare_time", payload)
            self.assertIn("export_time", payload)
            self.assertEqual(payload["cli_config_source"], "")
            self.assertEqual(len(payload["sliced_plates"]), 1)
            self.assertTrue((outdir / "part.gcode").exists())

    def test_invalid_params_for_downward_check_requires_printer_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mesh = root / "part.stl"
            _write_minimal_stl(mesh)
            result_path = root / "result.json"

            exit_code = slicer_v2_cli_main(
                [
                    "--mesh-path",
                    str(mesh),
                    "--downward-check",
                    "--result-path",
                    str(result_path),
                ]
            )

            self.assertEqual(exit_code, int(CliExitCode.CLI_INVALID_PARAMS))
            payload = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["return_code"], int(CliExitCode.CLI_INVALID_PARAMS))

    def test_missing_input_file_returns_not_found(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result_path = root / "result.json"
            missing_mesh = root / "missing.stl"
            exit_code = slicer_v2_cli_main(
                [
                    "--mesh-path",
                    str(missing_mesh),
                    "--result-path",
                    str(result_path),
                ]
            )
            self.assertEqual(exit_code, int(CliExitCode.CLI_FILE_NOTFOUND))
            payload = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["return_code"], int(CliExitCode.CLI_FILE_NOTFOUND))

    def test_invalid_profile_json_returns_config_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mesh = root / "part.stl"
            _write_minimal_stl(mesh)
            bad_profile = root / "bad.json"
            bad_profile.write_text("{ invalid json", encoding="utf-8")
            result_path = root / "result.json"

            exit_code = slicer_v2_cli_main(
                [
                    "--mesh-path",
                    str(mesh),
                    "--load-settings",
                    str(bad_profile),
                    "--result-path",
                    str(result_path),
                ]
            )
            self.assertEqual(exit_code, int(CliExitCode.CLI_CONFIG_FILE_ERROR))
            payload = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["return_code"], int(CliExitCode.CLI_CONFIG_FILE_ERROR))

    def test_downward_compatibility_lookup_known_and_unknown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mesh = root / "part.stl"
            _write_minimal_stl(mesh)

            cli_config = root / "cli_config.json"
            cli_payload = {
                "printer": {
                    "ModelA": {
                        "downward_check": {
                            "PresetA": ["PresetB 0.4 nozzle", "PresetC 0.4 nozzle"],
                        }
                    }
                }
            }
            cli_config.write_text(json.dumps(cli_payload, indent=2), encoding="utf-8")

            result_known = root / "result_known.json"
            exit_known = slicer_v2_cli_main(
                [
                    "--mesh-path",
                    str(mesh),
                    "--downward-check",
                    "--cli-config-path",
                    str(cli_config),
                    "--printer-model",
                    "ModelA",
                    "--printer-name",
                    "PresetA",
                    "--result-path",
                    str(result_known),
                ]
            )
            self.assertEqual(exit_known, int(CliExitCode.CLI_SUCCESS))
            payload_known = json.loads(result_known.read_text(encoding="utf-8"))
            self.assertEqual(
                payload_known["downward_compatible_machine"],
                ["PresetB 0.4 nozzle", "PresetC 0.4 nozzle"],
            )
            self.assertEqual(payload_known["cli_config_source"], str(cli_config.resolve()))

            result_unknown = root / "result_unknown.json"
            exit_unknown = slicer_v2_cli_main(
                [
                    "--mesh-path",
                    str(mesh),
                    "--downward-check",
                    "--cli-config-path",
                    str(cli_config),
                    "--printer-model",
                    "ModelA",
                    "--printer-name",
                    "PresetMissing",
                    "--result-path",
                    str(result_unknown),
                ]
            )
            self.assertEqual(exit_unknown, int(CliExitCode.CLI_SUCCESS))
            payload_unknown = json.loads(result_unknown.read_text(encoding="utf-8"))
            self.assertEqual(payload_unknown["downward_compatible_machine"], [])
            self.assertEqual(payload_unknown["cli_config_source"], str(cli_config.resolve()))

    def test_default_embedded_cli_config_is_used_when_path_is_omitted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mesh = root / "part.stl"
            _write_minimal_stl(mesh)
            result_path = root / "result.json"

            exit_code = slicer_v2_cli_main(
                [
                    "--mesh-path",
                    str(mesh),
                    "--downward-check",
                    "--printer-model",
                    "Bambu Lab A1",
                    "--printer-name",
                    "Bambu Lab A1 0.4 nozzle",
                    "--result-path",
                    str(result_path),
                ]
            )

            self.assertEqual(exit_code, int(CliExitCode.CLI_SUCCESS))
            payload = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["cli_config_source"], "embedded:profiles/BBL/cli_config.json")
            self.assertGreaterEqual(len(payload["downward_compatible_machine"]), 1)

    def test_explicit_missing_cli_config_path_returns_not_found(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            mesh = root / "part.stl"
            _write_minimal_stl(mesh)
            result_path = root / "result.json"
            missing_cli_config = root / "missing_cli_config.json"

            exit_code = slicer_v2_cli_main(
                [
                    "--mesh-path",
                    str(mesh),
                    "--downward-check",
                    "--cli-config-path",
                    str(missing_cli_config),
                    "--printer-model",
                    "Bambu Lab A1",
                    "--printer-name",
                    "Bambu Lab A1 0.4 nozzle",
                    "--result-path",
                    str(result_path),
                ]
            )

            self.assertEqual(exit_code, int(CliExitCode.CLI_FILE_NOTFOUND))
            payload = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["return_code"], int(CliExitCode.CLI_FILE_NOTFOUND))

    def test_unsupported_operations_are_guarded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result_3mf = root / "result_3mf.json"
            three_mf = root / "project.3mf"
            three_mf.write_text("placeholder", encoding="utf-8")

            exit_3mf = slicer_v2_cli_main(
                [
                    "--mesh-path",
                    str(three_mf),
                    "--result-path",
                    str(result_3mf),
                ]
            )
            self.assertEqual(exit_3mf, int(CliExitCode.CLI_UNSUPPORTED_OPERATION))

            mesh = root / "part.stl"
            _write_minimal_stl(mesh)
            result_slice = root / "result_slice.json"
            exit_slice = slicer_v2_cli_main(
                [
                    "--mesh-path",
                    str(mesh),
                    "--slice",
                    "2",
                    "--result-path",
                    str(result_slice),
                ]
            )
            self.assertEqual(exit_slice, int(CliExitCode.CLI_UNSUPPORTED_OPERATION))
            payload_slice = json.loads(result_slice.read_text(encoding="utf-8"))
            self.assertEqual(payload_slice["return_code"], int(CliExitCode.CLI_UNSUPPORTED_OPERATION))


if __name__ == "__main__":
    unittest.main()
