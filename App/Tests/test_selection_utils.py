import unittest

from gui.selection_utils import rect_contains, rect_from_points, rect_intersects, rect_size


class SelectionUtilsTests(unittest.TestCase):
    def test_rect_from_points_normalizes(self):
        rect = rect_from_points((10, 5), (2, 7))
        self.assertEqual(rect, (2.0, 5.0, 10.0, 7.0))

    def test_rect_size(self):
        rect = (2.0, 5.0, 10.0, 7.0)
        self.assertEqual(rect_size(rect), (8.0, 2.0))
        self.assertEqual(rect_size((5.0, 5.0, 2.0, 2.0)), (0.0, 0.0))

    def test_rect_intersects(self):
        a = (0.0, 0.0, 5.0, 5.0)
        b = (4.0, 4.0, 8.0, 8.0)
        self.assertTrue(rect_intersects(a, b))

    def test_rect_intersects_edges(self):
        a = (0.0, 0.0, 5.0, 5.0)
        b = (5.0, 5.0, 9.0, 9.0)
        self.assertTrue(rect_intersects(a, b))

    def test_rect_contains(self):
        outer = (0.0, 0.0, 10.0, 10.0)
        inner = (2.0, 3.0, 6.0, 7.0)
        self.assertTrue(rect_contains(outer, inner))
        self.assertFalse(rect_contains(inner, outer))

    def test_rect_intersects_false(self):
        a = (0.0, 0.0, 5.0, 5.0)
        b = (6.0, 6.0, 8.0, 9.0)
        self.assertFalse(rect_intersects(a, b))


if __name__ == "__main__":
    unittest.main()
