import unittest

from gui.arrange_utils import positions_fit, spacing_candidates, spacing_with_base


class TestArrangeUtils(unittest.TestCase):
    def test_spacing_with_base(self):
        self.assertEqual(spacing_with_base(3.0, 0.0), 3.0)
        self.assertEqual(spacing_with_base(3.0, 2.0), 5.0)
        self.assertEqual(spacing_with_base(3.0, -1.0), 3.0)

    def test_spacing_candidates(self):
        values = spacing_candidates(2.0, step=0.5)
        self.assertEqual(values[0], 2.0)
        self.assertIn(0.0, values)

    def test_positions_fit(self):
        sizes = [(1, 20.0, 20.0)]
        bed_bounds = (-50.0, 50.0, -50.0, 50.0)
        self.assertTrue(positions_fit({1: (0.0, 0.0)}, sizes, bed_bounds))
        self.assertFalse(positions_fit({1: (60.0, 0.0)}, sizes, bed_bounds))


if __name__ == "__main__":
    unittest.main()
