import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
TESTS = os.path.abspath(os.path.dirname(__file__))
if TESTS not in sys.path:
    sys.path.insert(0, TESTS)

from config import performance
from harness import BaseTestCase


class PerformanceTests(BaseTestCase):
    def setUp(self):
        performance._CACHED_LIMITS = None
        performance._CACHED_TOTAL_MB = None

    def tearDown(self):
        performance._CACHED_LIMITS = None
        performance._CACHED_TOTAL_MB = None

    def test_recommend_cache_mb(self):
        self.assertEqual(performance._recommend_cache_mb(2000), 32)
        self.assertEqual(performance._recommend_cache_mb(6000), 64)
        self.assertEqual(performance._recommend_cache_mb(12000), 128)
        self.assertEqual(performance._recommend_cache_mb(32000), 256)

    def test_recommend_threads(self):
        self.assertEqual(performance._recommend_threads(2000, 8), 1)
        self.assertEqual(performance._recommend_threads(6000, 8), 2)
        self.assertEqual(performance._recommend_threads(12000, 8), 4)
        self.assertEqual(performance._recommend_threads(32000, 8), 7)

    def test_resolve_overrides(self):
        limits = performance.resolve_performance_limits(
            {"max_threads": 3, "max_slice_cache_mb": 96}
        )
        self.assertEqual(limits["max_threads"], 3)
        self.assertEqual(limits["max_slice_cache_mb"], 96)


if __name__ == "__main__":
    unittest.main()
