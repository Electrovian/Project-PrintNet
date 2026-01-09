import unittest

try:
    from PyQt5 import QtWidgets
except Exception:  # pragma: no cover - optional dependency in tests
    QtWidgets = None


@unittest.skipIf(QtWidgets is None, "PyQt5 not available")
class ModelPanelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if QtWidgets is None:
            raise unittest.SkipTest("PyQt5 not available")
        assert QtWidgets is not None
        cls._app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    def test_add_remove_and_select(self):
        from gui.model_panel import ModelPanel

        panel = ModelPanel()
        selections = []
        current = []
        panel.selection_changed.connect(lambda ids: selections.append(list(ids)))
        panel.model_selected.connect(lambda mid: current.append(mid))

        panel.add_model("First", 1)
        panel.add_model("Second", 2)
        self.assertEqual(panel.list_widget.count(), 2)

        item0 = panel.list_widget.item(0)
        item1 = panel.list_widget.item(1)
        assert item0 is not None
        assert item1 is not None
        item0.setSelected(True)
        item1.setSelected(True)
        panel.list_widget.setCurrentRow(1)

        self.assertTrue(current)
        self.assertEqual(current[-1], 2)
        self.assertTrue(selections)
        self.assertEqual(sorted(selections[-1]), [1, 2])

        panel.remove_model(1)
        self.assertEqual(panel.list_widget.count(), 1)

    def test_truncate_name(self):
        from gui.model_panel import ModelPanel

        panel = ModelPanel()
        long_name = "a" * (panel.MAX_DISPLAY_NAME + 5)
        truncated = panel._truncate_name(long_name)
        self.assertTrue(truncated.endswith("..."))
        self.assertLessEqual(len(truncated), panel.MAX_DISPLAY_NAME)


if __name__ == "__main__":
    unittest.main()
