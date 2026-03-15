import unittest

from config.defaults import DEFAULTS
from config.runtime_state import (
    RuntimePrinterState,
    bed_limits_for_state,
    default_runtime_printer_state,
    resolve_state_from_profile,
)


class RuntimeStateTests(unittest.TestCase):

    def test_default_runtime_printer_state_uses_defaults(self):
        state = default_runtime_printer_state()
        printer_defaults = DEFAULTS["printer"]
        self.assertEqual(state.name, printer_defaults["name"])
        self.assertEqual(state.bed_x, float(printer_defaults["bed_size"][0]))
        self.assertEqual(state.bed_y, float(printer_defaults["bed_size"][1]))
        self.assertEqual(state.bed_z, float(printer_defaults["max_height"]))

    def test_runtime_state_bed_size_property(self):
        state = RuntimePrinterState(name="Test", bed_x=123.0, bed_y=234.0, bed_z=345.0)
        self.assertEqual(state.bed_size, (123.0, 234.0))

    def test_resolve_state_from_profile_uses_profile_values(self):
        current = RuntimePrinterState(name="Current", bed_x=200.0, bed_y=200.0, bed_z=200.0)
        profile = {"name": "K1 Max", "bed_x": 300, "bed_y": 300, "bed_z": 400}

        state = resolve_state_from_profile(profile, current_state=current)

        self.assertEqual(state.name, "K1 Max")
        self.assertEqual(state.bed_x, 300.0)
        self.assertEqual(state.bed_y, 300.0)
        self.assertEqual(state.bed_z, 400.0)

    def test_resolve_state_from_profile_keeps_current_name_when_missing(self):
        current = RuntimePrinterState(name="CarryName", bed_x=200.0, bed_y=200.0, bed_z=200.0)
        profile = {"bed_x": 210, "bed_y": 220, "bed_z": 230}

        state = resolve_state_from_profile(profile, current_state=current)

        self.assertEqual(state.name, "CarryName")
        self.assertEqual(state.bed_x, 210.0)
        self.assertEqual(state.bed_y, 220.0)
        self.assertEqual(state.bed_z, 230.0)

    def test_resolve_state_from_profile_falls_back_defaults_for_bad_values(self):
        printer_defaults = DEFAULTS["printer"]
        profile = {"name": "Demo", "bed_x": "bad", "bed_y": None, "bed_z": "oops"}

        state = resolve_state_from_profile(profile, current_state=None, defaults=printer_defaults)

        self.assertEqual(state.name, "Demo")
        self.assertEqual(state.bed_x, float(printer_defaults["bed_size"][0]))
        self.assertEqual(state.bed_y, float(printer_defaults["bed_size"][1]))
        self.assertEqual(state.bed_z, float(printer_defaults["max_height"]))

    def test_bed_limits_for_state_returns_viewer_shape(self):
        state = RuntimePrinterState(name="Test", bed_x=256.0, bed_y=256.0, bed_z=300.0)

        bed_size, max_height = bed_limits_for_state(state)

        self.assertEqual(bed_size, (256.0, 256.0))
        self.assertEqual(max_height, 300.0)


if __name__ == "__main__":
    unittest.main()
