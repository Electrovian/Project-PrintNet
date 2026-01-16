import unittest

try:
    from PyQt5 import QtWidgets
except Exception:  # pragma: no cover - optional dependency in tests
    QtWidgets = None


@unittest.skipIf(QtWidgets is None, "PyQt5 not available")
class DeviceViewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert QtWidgets is not None
        cls._app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    def test_live_status_formatting(self):
        from gui.Windows.device import DeviceView

        view = DeviceView()
        view.update_live_status(
            head_pos=(1.2345, 2.3456, 3.4567),
            time_left_s=3661,
            pla_remaining_m=1.234,
            pla_low=True,
        )

        self.assertEqual(view._head_pos_value.text(), "X: 1.23  Y: 2.35  Z: 3.46")
        self.assertEqual(view._time_left_value.text(), "1h01m")
        self.assertEqual(view._pla_status_value.text(), "LOW (1.23 m left)")

    def test_live_status_empty(self):
        from gui.Windows.device import DeviceView

        view = DeviceView()
        view.update_live_status()

        self.assertEqual(view._head_pos_value.text(), "n/a")
        self.assertEqual(view._time_left_value.text(), "n/a")
        self.assertEqual(view._pla_status_value.text(), "n/a")


if __name__ == "__main__":
    unittest.main()
