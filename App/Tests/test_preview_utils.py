import unittest

from gui.preview_utils import play_interval_ms


class TestPreviewUtils(unittest.TestCase):
    def test_play_interval_ms_scales_speed(self):
        self.assertEqual(play_interval_ms(30, 1.0), 30)
        self.assertEqual(play_interval_ms(30, 2.0), 15)
        self.assertEqual(play_interval_ms(30, 0.5), 60)

    def test_play_interval_ms_clamps(self):
        self.assertEqual(play_interval_ms(30, 10.0, min_ms=8, max_ms=250), 8)
        self.assertEqual(play_interval_ms(1000, 0.1, min_ms=8, max_ms=250), 250)

    def test_play_interval_ms_invalid_speed(self):
        self.assertEqual(play_interval_ms(50, None), 50)
        self.assertEqual(play_interval_ms(50, -2), 50)
        self.assertEqual(play_interval_ms(0, 1.0), 8)

if __name__ == "__main__":
    unittest.main()
