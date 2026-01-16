import contextlib
import math
import tempfile
import unittest
from typing import Iterable, Sequence, Tuple

import numpy as np

Point2D = Tuple[float, float]


class BaseTestCase(unittest.TestCase):
    def assertPointsAlmostEqual(self, a: Sequence[float], b: Sequence[float], places: int = 6):
        self.assertEqual(len(a), len(b))
        for av, bv in zip(a, b):
            self.assertAlmostEqual(float(av), float(bv), places=places)

    def assertPointClose(self, a: Point2D, b: Point2D, tol: float = 1e-6):
        self.assertTrue(math.isclose(a[0], b[0], abs_tol=tol))
        self.assertTrue(math.isclose(a[1], b[1], abs_tol=tol))

    def assertAllFinite(self, values: Iterable[float]):
        for value in values:
            self.assertTrue(math.isfinite(float(value)))


@contextlib.contextmanager
def temp_directory():
    with tempfile.TemporaryDirectory() as tmp:
        yield tmp


def circle_points(radius: float, steps: int) -> list[Point2D]:
    if steps <= 0:
        return []
    pts: list[Point2D] = []
    for i in range(steps):
        angle = (2.0 * math.pi * i) / float(steps)
        pts.append((radius * math.cos(angle), radius * math.sin(angle)))
    return pts


def square_points(size: float) -> list[Point2D]:
    half = size / 2.0
    return [
        (-half, -half),
        (half, -half),
        (half, half),
        (-half, half),
        (-half, -half),
    ]


def to_np(points: Sequence[Point2D]) -> np.ndarray:
    return np.asarray(points, dtype=float)
