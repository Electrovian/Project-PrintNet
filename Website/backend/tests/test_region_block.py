import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from printnet_backend.region_block import (  # noqa: E402
    evaluate_region_compliance,
    normalize_state_code,
    read_request_state_code,
)


class RegionBlockTests(unittest.TestCase):
    def test_normalize_state_code_handles_common_inputs(self):
        self.assertEqual(normalize_state_code("CA"), "CA")
        self.assertEqual(normalize_state_code("us-ca"), "CA")
        self.assertEqual(normalize_state_code("US_NY"), "NY")
        self.assertEqual(normalize_state_code(" US-TX "), "TX")
        self.assertEqual(normalize_state_code(""), "")
        self.assertEqual(normalize_state_code("USA"), "")

    def test_read_request_state_code_uses_known_headers(self):
        headers = {
            "x-something-else": "ignored",
            "x-vercel-ip-country-region": "ca",
        }
        self.assertEqual(read_request_state_code(headers), "CA")

    def test_read_request_state_code_returns_empty_when_missing(self):
        self.assertEqual(read_request_state_code({"x-us-country": "US"}), "")

    def test_read_request_state_code_respects_trusted_headers_override(self):
        headers = {
            "x-vercel-ip-country-region": "CA",
            "x-custom-geo": "NY",
        }
        self.assertEqual(
            read_request_state_code(headers, trusted_header_keys=("x-custom-geo",)),
            "NY",
        )

    def test_evaluate_region_compliance_denies_unknown_when_policy_is_deny(self):
        decision = evaluate_region_compliance(
            headers={},
            region_block_enabled=True,
            blocked_state_codes=("CA",),
            unknown_policy="deny",
            trusted_header_keys=(),
        )
        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason_code, "REGION_GEO_UNDETERMINED")

    def test_evaluate_region_compliance_allows_unknown_when_policy_is_allow(self):
        decision = evaluate_region_compliance(
            headers={},
            region_block_enabled=True,
            blocked_state_codes=("CA",),
            unknown_policy="allow",
            trusted_header_keys=(),
        )
        self.assertTrue(decision.allowed)
        self.assertEqual(decision.reason_code, "REGION_GEO_UNDETERMINED")


if __name__ == "__main__":
    unittest.main()
