import os
import sys
import unittest
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from integrations.web_backend_activity import WebBackendActivityClient, WebBackendActivityError  # noqa: E402


class _FakeResponse:
    def __init__(self, *, ok: bool, status_code: int, payload: dict):
        self.ok = bool(ok)
        self.status_code = int(status_code)
        self._payload = dict(payload)
        self.text = ""

    def json(self):
        return dict(self._payload)


class WebBackendActivityClientTests(unittest.TestCase):
    def test_client_requires_service_token(self):
        with self.assertRaises(WebBackendActivityError):
            WebBackendActivityClient(base_url="http://127.0.0.1:8000/api/v1", service_token="")

    def test_client_sends_service_token_header(self):
        calls = []

        def _fake_request(method, url, params=None, json=None, headers=None, timeout=None):  # noqa: A002
            calls.append(
                {
                    "method": method,
                    "url": url,
                    "params": dict(params or {}),
                    "json": dict(json or {}),
                    "headers": dict(headers or {}),
                    "timeout": timeout,
                }
            )
            if str(url).endswith("/activity/feed"):
                return _FakeResponse(
                    ok=True,
                    status_code=200,
                    payload={
                        "ok": True,
                        "feed": {
                            "items": [],
                            "cursor_in": 0,
                            "cursor_out": 0,
                            "max_cursor": 0,
                            "has_more": False,
                            "reset_required": False,
                        },
                    },
                )
            if str(url).endswith("/compliance/region"):
                return _FakeResponse(
                    ok=True,
                    status_code=200,
                    payload={
                        "ok": True,
                        "compliance": {
                            "decision": "allow",
                            "reason_code": "REGION_ALLOWED",
                            "detail": "allowed",
                            "state_code": "NY",
                        },
                    },
                )
            return _FakeResponse(
                ok=True,
                status_code=200,
                payload={"ok": True, "snapshot": {"jobs": [], "job_count": 0}},
            )

        with mock.patch("requests.Session.request", side_effect=_fake_request):
            client = WebBackendActivityClient(
                base_url="http://127.0.0.1:8000/api/v1",
                service_token="activity-secret",
                timeout_seconds=2.0,
            )
            feed = client.fetch_activity_feed(cursor=0, limit=50)
            snapshot = client.fetch_queue_snapshot()
            compliance = client.fetch_compliance_region()

        self.assertIn("items", feed)
        self.assertIn("jobs", snapshot)
        self.assertEqual(compliance["decision"], "allow")
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0]["headers"].get("x-activity-service-token"), "activity-secret")
        self.assertEqual(calls[1]["headers"].get("x-activity-service-token"), "activity-secret")
        self.assertEqual(calls[2]["headers"].get("x-activity-service-token"), "activity-secret")


if __name__ == "__main__":
    unittest.main()
