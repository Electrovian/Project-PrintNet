from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from App.slicer_v2.profile_compat import (
    DEFAULT_CLI_CONFIG_IDENTIFIER,
    ProfileCompatConfigError,
    ProfileCompatFileNotFoundError,
    resolve_downward_compatible_machines,
)


class TestSlicerV2ProfileCompat(unittest.TestCase):
    def test_blank_cli_config_path_uses_embedded_default(self) -> None:
        result = resolve_downward_compatible_machines(
            cli_config_path="",
            printer_model="Bambu Lab A1",
            printer_name="Bambu Lab A1 0.4 nozzle",
        )

        self.assertEqual(result.config_source, f"embedded:{DEFAULT_CLI_CONFIG_IDENTIFIER}")
        self.assertGreaterEqual(len(result.downward_compatible_machine), 1)
        self.assertEqual(result.warnings, [])

    def test_embedded_identifier_alias_resolves(self) -> None:
        result = resolve_downward_compatible_machines(
            cli_config_path="App/printer_presets/seed_resources/profiles/BBL/cli_config.json",
            printer_model="Bambu Lab A1",
            printer_name="Bambu Lab A1 0.4 nozzle",
        )

        self.assertEqual(result.config_source, f"embedded:{DEFAULT_CLI_CONFIG_IDENTIFIER}")
        self.assertGreaterEqual(len(result.downward_compatible_machine), 1)

    def test_missing_cli_config_path_fails_without_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing_cli_config.json"

            with self.assertRaises(ProfileCompatFileNotFoundError) as ctx:
                resolve_downward_compatible_machines(
                    cli_config_path=str(missing),
                    printer_model="Bambu Lab A1",
                    printer_name="Bambu Lab A1 0.4 nozzle",
                )

            self.assertIn("MISSING_CLI_CONFIG_FILE", str(ctx.exception))

    def test_invalid_cli_config_json_fails_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cli_config = Path(tmp) / "cli_config.json"
            cli_config.write_text("{not-json}", encoding="utf-8")

            with self.assertRaises(ProfileCompatConfigError) as ctx:
                resolve_downward_compatible_machines(
                    cli_config_path=str(cli_config),
                    printer_model="Bambu Lab A1",
                    printer_name="Bambu Lab A1 0.4 nozzle",
                )

            self.assertIn("CLI_CONFIG_JSON_PARSE_ERROR", str(ctx.exception))

    def test_warning_paths_still_report_config_source(self) -> None:
        result = resolve_downward_compatible_machines(
            cli_config_path="",
            printer_model="Not A Real Printer",
            printer_name="Not A Real Printer 0.4 nozzle",
        )

        self.assertEqual(result.config_source, f"embedded:{DEFAULT_CLI_CONFIG_IDENTIFIER}")
        self.assertEqual(result.downward_compatible_machine, [])
        self.assertTrue(result.warnings)

