import unittest

from qt_harness import QtTestCase


class PopupTests(QtTestCase):

    def test_move_popup_emits(self):
        from gui.popups.move_popup import MovePopup

        popup = MovePopup()
        emitted = []
        popup.position_changed.connect(lambda x, y, z: emitted.append((x, y, z)))

        popup.set_position(1.0, 2.0, 3.0)
        self.assertEqual(emitted, [])

        popup._pos_spins[0].setValue(4.0)
        self.assertTrue(emitted)
        self.assertEqual(emitted[-1][0], 4.0)

    def test_rotate_popup_reset(self):
        from gui.popups.rotate_popup import RotatePopup

        popup = RotatePopup()
        rotations = []
        resets = []
        popup.rotation_changed.connect(lambda x, y, z: rotations.append((x, y, z)))
        popup.reset_requested.connect(lambda: resets.append(True))

        popup.set_rotation(10.0, 20.0, 30.0)
        self.assertEqual(rotations, [])

        popup._emit_reset()
        self.assertEqual(len(resets), 1)
        self.assertEqual([spin.value() for spin in popup._rot_spins], [0.0, 0.0, 0.0])


if __name__ == "__main__":
    unittest.main()
