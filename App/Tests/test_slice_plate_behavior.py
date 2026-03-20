import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui.Windows.controller.print import PrintMixin  # noqa: E402


class _SliceController(PrintMixin):
    def __init__(self):
        self.auto_orient_calls = 0
        self.slice_calls = []

    def _auto_orient_plate_default(self):
        self.auto_orient_calls += 1

    def _settings_with_slice_defaults(self):
        return {"profile": "default"}

    def _slice_model(self, settings, *, activate_preview=False, show_dialog=False, show_errors=False):
        self.slice_calls.append(
            {
                "settings": settings,
                "activate_preview": bool(activate_preview),
                "show_dialog": bool(show_dialog),
                "show_errors": bool(show_errors),
            }
        )


class SlicePlateBehaviorTests(unittest.TestCase):
    def test_slice_current_plate_uses_current_transforms_without_auto_orient(self):
        controller = _SliceController()
        controller.slice_current_plate()

        self.assertEqual(controller.auto_orient_calls, 0)
        self.assertEqual(len(controller.slice_calls), 1)
        self.assertEqual(controller.slice_calls[0]["settings"], {"profile": "default"})
        self.assertTrue(controller.slice_calls[0]["activate_preview"])
        self.assertTrue(controller.slice_calls[0]["show_dialog"])
        self.assertTrue(controller.slice_calls[0]["show_errors"])


if __name__ == "__main__":
    unittest.main()
