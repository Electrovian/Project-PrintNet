import os
import sys
import unittest

from PyQt5 import QtCore, QtGui, QtTest, QtWidgets

from qt_harness import QtTestCase

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


class ViewCubeOverlayTests(QtTestCase):
    def _build_widget(self):
        from gui.widgets.view_cube_overlay import ViewCubeOverlay

        widget = ViewCubeOverlay()
        widget.resize(widget.sizeHint())
        widget.show()
        QtWidgets.QApplication.processEvents()
        self.addCleanup(widget.close)
        return widget

    @staticmethod
    def _polygon_center(poly):
        count = poly.count()
        if count <= 0:
            return QtCore.QPoint()
        x = 0.0
        y = 0.0
        for idx in range(count):
            point = poly.at(idx)
            x += float(point.x())
            y += float(point.y())
        return QtCore.QPoint(int(round(x / count)), int(round(y / count)))

    def test_default_visible_faces_match_front_right_top_iso(self):
        widget = self._build_widget()
        faces, corners, edges = widget._project_faces()
        visible_faces = {face["name"] for face in faces}
        labels = {face["label"] for face in faces}
        positions = {face["name"]: float(face["label_pos"][0]) for face in faces}

        self.assertEqual(visible_faces, {"front", "right", "top"})
        self.assertEqual(labels, {"Front", "Right", "Top"})
        self.assertLess(positions["front"], positions["right"])
        self.assertGreaterEqual(len(corners), 4)
        self.assertGreaterEqual(len(edges), 3)

    def test_cube_size_clamps_to_presentation_bounds(self):
        widget = self._build_widget()
        widget.set_cube_size(10)
        self.assertEqual(widget.sizeHint(), QtCore.QSize(96, 96))

        widget.set_cube_size(400)
        self.assertEqual(widget.sizeHint(), QtCore.QSize(260, 260))

    def test_face_click_emits_snap_target_on_release(self):
        widget = self._build_widget()
        captured = []
        widget.viewRequested.connect(captured.append)
        faces, _corners, _edges = widget._project_faces()
        front = next(face for face in faces if face["name"] == "front")
        pos = QtCore.QPoint(int(round(front["label_pos"][0])), int(round(front["label_pos"][1])))

        QtTest.QTest.mousePress(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, pos)
        QtTest.QTest.mouseRelease(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, pos)
        QtWidgets.QApplication.processEvents()

        self.assertEqual(captured, ["front"])

    def test_edge_click_emits_perspective_snap_target(self):
        widget = self._build_widget()
        widget.repaint()
        QtWidgets.QApplication.processEvents()
        self.assertTrue(widget._edge_regions)
        captured = []
        widget.viewRequested.connect(captured.append)
        poly, name, _depth = widget._edge_regions[0]
        pos = self._polygon_center(poly)

        QtTest.QTest.mousePress(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, pos)
        QtTest.QTest.mouseRelease(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, pos)
        QtWidgets.QApplication.processEvents()

        self.assertTrue(str(name).startswith("edge:"))
        self.assertEqual(captured, [name])

    def test_corner_click_emits_isometric_snap_target(self):
        widget = self._build_widget()
        widget.repaint()
        QtWidgets.QApplication.processEvents()
        self.assertTrue(widget._corner_regions)
        captured = []
        widget.viewRequested.connect(captured.append)
        poly, name, _depth = widget._corner_regions[0]
        pos = self._polygon_center(poly)

        QtTest.QTest.mousePress(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, pos)
        QtTest.QTest.mouseRelease(widget, QtCore.Qt.LeftButton, QtCore.Qt.NoModifier, pos)
        QtWidgets.QApplication.processEvents()

        self.assertTrue(str(name).startswith("iso:"))
        self.assertEqual(captured, [name])

    def test_drag_emits_orbit_without_triggering_view_snap(self):
        widget = self._build_widget()
        orbit_events = []
        view_events = []
        widget.orbitRequested.connect(lambda az, el: orbit_events.append((float(az), float(el))))
        widget.viewRequested.connect(view_events.append)
        start = QtCore.QPoint(int(round(widget._cube_rect.center().x())), int(round(widget._cube_rect.center().y())))
        end = QtCore.QPoint(start.x() + 18, start.y() - 12)

        press = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonPress,
            QtCore.QPointF(start),
            QtCore.Qt.LeftButton,
            QtCore.Qt.LeftButton,
            QtCore.Qt.NoModifier,
        )
        move = QtGui.QMouseEvent(
            QtCore.QEvent.MouseMove,
            QtCore.QPointF(end),
            QtCore.Qt.NoButton,
            QtCore.Qt.LeftButton,
            QtCore.Qt.NoModifier,
        )
        release = QtGui.QMouseEvent(
            QtCore.QEvent.MouseButtonRelease,
            QtCore.QPointF(end),
            QtCore.Qt.LeftButton,
            QtCore.Qt.NoButton,
            QtCore.Qt.NoModifier,
        )

        QtWidgets.QApplication.sendEvent(widget, press)
        QtWidgets.QApplication.sendEvent(widget, move)
        QtWidgets.QApplication.sendEvent(widget, release)
        QtWidgets.QApplication.processEvents()

        self.assertGreaterEqual(len(orbit_events), 1)
        self.assertEqual(view_events, [])

    def test_axis_tripod_tracks_camera_orientation(self):
        widget = self._build_widget()
        base = QtCore.QPointF(widget._axis_origin)
        initial = {str(axis["label"]): axis["end"] for axis in widget._tripod_axes()}

        self.assertGreater(initial["X"].x(), base.x())
        self.assertGreater(initial["X"].y(), base.y())
        self.assertGreater(initial["Y"].x(), base.x())
        self.assertLess(initial["Y"].y(), base.y())
        self.assertLess(initial["Z"].y(), base.y())

        widget.set_camera(-45.0, 30.0)
        updated = {str(axis["label"]): axis["end"] for axis in widget._tripod_axes()}

        changed = [
            abs(updated[label].x() - initial[label].x()) + abs(updated[label].y() - initial[label].y())
            for label in ("X", "Y", "Z")
        ]
        self.assertTrue(any(delta > 10.0 for delta in changed), msg=f"expected tripod axes to move, got {changed}")

    def test_companion_buttons_emit_menu_and_fit_signals(self):
        widget = self._build_widget()
        menu_hits = []
        fit_hits = []
        widget.menuRequested.connect(lambda point: menu_hits.append(point))
        widget.fitRequested.connect(lambda: fit_hits.append(True))

        widget._menu_button.click()
        widget._fit_button.click()
        QtWidgets.QApplication.processEvents()

        self.assertEqual(len(menu_hits), 1)
        self.assertEqual(len(fit_hits), 1)

    def test_visible_face_labels_render_bright_pixels_inside_label_bounds(self):
        widget = self._build_widget()
        widget.repaint()
        QtWidgets.QApplication.processEvents()

        image = widget.grab().toImage().convertToFormat(QtGui.QImage.Format_ARGB32)
        layouts = dict(widget._visible_label_layouts)

        for name in ("front", "right", "top"):
            self.assertIn(name, layouts)
            bounds = layouts[name]["bounds"].intersected(image.rect())
            self.assertGreater(bounds.width(), 0)
            self.assertGreater(bounds.height(), 0)
            channel_values = []
            highlight_pixels = 0
            peak_value = 0
            for y in range(bounds.top(), bounds.bottom() + 1):
                for x in range(bounds.left(), bounds.right() + 1):
                    color = image.pixelColor(x, y)
                    if color.alpha() <= 0:
                        continue
                    channel_max = max(color.red(), color.green(), color.blue())
                    channel_values.append(channel_max)
                    peak_value = max(peak_value, channel_max)
            self.assertTrue(channel_values, msg=f"expected non-transparent label area for {name}")
            baseline = sum(channel_values) / float(len(channel_values))
            for value in channel_values:
                if value >= baseline + 24.0:
                    highlight_pixels += 1
            self.assertGreaterEqual(
                peak_value,
                int(round(baseline + 30.0)),
                msg=f"expected label highlight above face background for {name}, found peak {peak_value} baseline {baseline:.1f}",
            )
            self.assertGreaterEqual(
                highlight_pixels,
                8,
                msg=f"expected readable label pixels for {name}, found {highlight_pixels} with baseline {baseline:.1f}",
            )


if __name__ == "__main__":
    unittest.main()
