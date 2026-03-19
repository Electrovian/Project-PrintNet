import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.geometry import polygon_from_tuples  # noqa: E402
from slicer_v2.line_split import split_line  # noqa: E402


class TestSlicerV2LineSplit(unittest.TestCase):
    def test_split_line_through_square(self) -> None:
        clip = [
            polygon_from_tuples(
                [
                    (0.0, 0.0),
                    (10.0, 0.0),
                    (10.0, 10.0),
                    (0.0, 10.0),
                ]
            )
        ]
        line = [(-5.0, 5.0), (15.0, 5.0)]
        result = split_line(line, clip, closed=False)
        self.assertGreaterEqual(len(result), 3)
        clipped_states = [item.clipped for item in result[:-1]]
        self.assertIn(True, clipped_states)
        self.assertIn(False, clipped_states)


if __name__ == '__main__':
    unittest.main()
