import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from gui.Windows.activity import ActivityView  # noqa: E402
    from Tests.qt_harness import QtTestCase  # noqa: E402
except Exception:
    ActivityView = None
    QtTestCase = unittest.TestCase


@unittest.skipIf(ActivityView is None, "activity view unavailable")
class ActivityViewTests(QtTestCase):
    def test_refresh_button_emits_refresh_requested(self):
        view = ActivityView()
        calls = []
        view.refresh_requested.connect(lambda: calls.append("refresh"))

        view._refresh_btn.click()

        self.assertEqual(calls, ["refresh"])

    def test_cache_banner_visibility_is_independent_from_compliance_banner(self):
        view = ActivityView()

        view.set_compliance_banner("region blocked")
        self.assertFalse(view._compliance_banner.isHidden())
        self.assertTrue(view._cache_banner.isHidden())

        view.set_cache_banner("cached data")
        self.assertFalse(view._compliance_banner.isHidden())
        self.assertFalse(view._cache_banner.isHidden())
        self.assertIn("cached data", view._cache_banner.text())

        view.set_cache_banner("")
        self.assertFalse(view._compliance_banner.isHidden())
        self.assertTrue(view._cache_banner.isHidden())

        view.set_compliance_banner("")
        self.assertTrue(view._compliance_banner.isHidden())


if __name__ == "__main__":
    unittest.main()
