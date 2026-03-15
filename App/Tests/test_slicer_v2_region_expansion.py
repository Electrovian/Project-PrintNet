import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from slicer_v2.geometry import polygon_from_tuples  # noqa: E402
from slicer_v2.region_expansion import (  # noqa: E402
    RegionExpansionParameters,
    propagate_waves_from_polygons,
    wave_seeds,
)


class TestSlicerV2RegionExpansion(unittest.TestCase):
    def test_wave_seed_and_propagation(self) -> None:
        src = [
            polygon_from_tuples(
                [
                    (2.0, 2.0),
                    (4.0, 2.0),
                    (4.0, 4.0),
                    (2.0, 4.0),
                ]
            )
        ]
        boundary = [
            polygon_from_tuples(
                [
                    (0.0, 0.0),
                    (20.0, 0.0),
                    (20.0, 20.0),
                    (0.0, 20.0),
                ]
            )
        ]
        params = RegionExpansionParameters.build(2.0, 0.5, 8)
        seeds = wave_seeds(src, boundary, params.tiny_expansion, sorted=True)
        self.assertEqual(len(seeds), 1)
        expanded = propagate_waves_from_polygons(src, boundary, params)
        self.assertGreaterEqual(len(expanded), 1)
        self.assertGreater(expanded[0].polygon.area, src[0].area)


if __name__ == '__main__':
    unittest.main()
