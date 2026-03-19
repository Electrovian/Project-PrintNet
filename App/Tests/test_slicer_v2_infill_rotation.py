import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.infill_rotation import calculate_infill_rotation_angles  # noqa: E402


class TestSlicerV2InfillRotation(unittest.TestCase):
    def test_simple_template_sequence(self) -> None:
        angles = calculate_infill_rotation_angles(
            layer_count=5,
            fixed_infill_angle_deg=12.0,
            template_string='0,90',
            layer_height_mm=0.2,
        )
        self.assertEqual(angles, [0.0, 90.0, 0.0, 90.0, 0.0])

    def test_relative_linear_joint(self) -> None:
        angles = calculate_infill_rotation_angles(
            layer_count=3,
            fixed_infill_angle_deg=0.0,
            template_string='+90/3',
            layer_height_mm=0.2,
        )
        self.assertAlmostEqual(angles[0], 0.0, places=4)
        self.assertAlmostEqual(angles[1], 45.0, places=4)
        self.assertAlmostEqual(angles[2], 90.0, places=4)

    def test_default_when_empty_template(self) -> None:
        angles = calculate_infill_rotation_angles(
            layer_count=4,
            fixed_infill_angle_deg=37.0,
            template_string='',
            layer_height_mm=0.2,
        )
        self.assertEqual(angles, [37.0, 37.0, 37.0, 37.0])


if __name__ == '__main__':
    unittest.main()
