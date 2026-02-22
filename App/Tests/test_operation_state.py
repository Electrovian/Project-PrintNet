import unittest

from gui.operation_state import (
    can_transition,
    default_operation_message,
    normalize_operation_state,
    operation_state_label,
)


class OperationStateTests(unittest.TestCase):
    def test_normalize_unknown_state_defaults_to_idle(self):
        self.assertEqual(normalize_operation_state("weird"), "idle")
        self.assertEqual(normalize_operation_state(""), "idle")

    def test_known_transition_paths(self):
        self.assertTrue(can_transition("idle", "slicing"))
        self.assertTrue(can_transition("slicing", "uploading"))
        self.assertTrue(can_transition("uploading", "printing"))
        self.assertTrue(can_transition("printing", "idle"))

    def test_disallowed_transition_path(self):
        self.assertFalse(can_transition("uploading", "slicing"))

    def test_labels_and_default_messages(self):
        self.assertEqual(operation_state_label("slicing"), "Slicing")
        self.assertEqual(default_operation_message("failure"), "Operation failed.")


if __name__ == "__main__":
    unittest.main()

