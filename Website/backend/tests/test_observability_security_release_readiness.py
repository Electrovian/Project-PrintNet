import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from printnet_backend.app import create_app  # noqa: E402
from printnet_backend.compat import create_test_client  # noqa: E402
from printnet_backend.observability import redact_sensitive_fields  # noqa: E402
from printnet_backend.settings import BackendSettings  # noqa: E402


class ObservabilitySecurityReleaseReadinessTests(unittest.TestCase):
    def setUp(self):
        settings = BackendSettings(
            enable_docs=False,
            release_required_checks=(
                "backend_health",
                "authz_enforced",
                "queue_worker_operational",
                "kubernetes_packaging_validated",
            ),
        )
        app = create_app(settings=settings)
        self.client = create_test_client(app)
        self.student_token = self._create_session("student-1", "student")
        self.operator_token = self._create_session("operator-1", "operator")
        self.admin_token = self._create_session("admin-1", "admin")

    def _create_session(self, user_id: str, role: str) -> str:
        response = self.client.post("/api/v1/auth/session", json={"user_id": user_id, "role": role})
        self.assertEqual(response.status_code, 200)
        return str(response.json()["session"]["token"])

    def test_redaction_masks_sensitive_fields(self):
        payload = {
            "auth_token": "token-123",
            "profile": {"api_key": "abc", "name": "safe"},
            "items": [{"password": "hidden"}, {"ok": True}],
        }
        sanitized = redact_sensitive_fields(payload)
        self.assertEqual(sanitized["auth_token"], "***REDACTED***")
        self.assertEqual(sanitized["profile"]["api_key"], "***REDACTED***")
        self.assertEqual(sanitized["profile"]["name"], "safe")
        self.assertEqual(sanitized["items"][0]["password"], "***REDACTED***")
        self.assertTrue(sanitized["items"][1]["ok"])

    def test_ops_routes_require_operator_or_admin(self):
        student = self.client.get(f"/api/v1/ops/metrics?auth_token={self.student_token}")
        self.assertEqual(student.status_code, 403)

        operator = self.client.get(f"/api/v1/ops/metrics?auth_token={self.operator_token}")
        self.assertEqual(operator.status_code, 200)
        self.assertTrue(operator.json()["ok"])

    def test_audit_log_redacts_auth_token_in_details(self):
        update = self.client.post(
            "/api/v1/ops/release-readiness/check",
            json={
                "auth_token": self.admin_token,
                "check_name": "authz_enforced",
                "passed": True,
                "detail": "ok",
            },
        )
        self.assertEqual(update.status_code, 200)

        audit = self.client.get(f"/api/v1/ops/audit?auth_token={self.operator_token}&limit=20")
        self.assertEqual(audit.status_code, 200)
        self.assertGreaterEqual(audit.json()["count"], 1)
        first = audit.json()["records"][0]
        details = first["details"]
        self.assertEqual(details["auth_token"], "***REDACTED***")

    def test_release_readiness_transitions_to_ready_when_checks_pass(self):
        initial = self.client.get(f"/api/v1/ops/release-readiness?auth_token={self.operator_token}")
        self.assertEqual(initial.status_code, 200)
        self.assertFalse(initial.json()["release"]["ready"])

        checks = [
            "authz_enforced",
            "queue_worker_operational",
            "kubernetes_packaging_validated",
        ]
        for check_name in checks:
            response = self.client.post(
                "/api/v1/ops/release-readiness/check",
                json={
                    "auth_token": self.admin_token,
                    "check_name": check_name,
                    "passed": True,
                    "detail": "validated",
                },
            )
            self.assertEqual(response.status_code, 200)

        final = self.client.get(f"/api/v1/ops/release-readiness?auth_token={self.operator_token}")
        self.assertEqual(final.status_code, 200)
        release = final.json()["release"]
        self.assertTrue(release["ready"])
        self.assertEqual(release["missing_required"], [])
        self.assertEqual(release["failing_required"], [])

    def test_ops_metrics_include_success_and_error_events(self):
        self.client.get("/api/v1/ops/metrics?auth_token=bad-token")
        self.client.get(f"/api/v1/ops/metrics?auth_token={self.operator_token}")

        metrics = self.client.get(f"/api/v1/ops/metrics?auth_token={self.operator_token}")
        self.assertEqual(metrics.status_code, 200)
        rows = metrics.json()["metrics"]["metrics"]
        event_names = {f"{item['event']}|{item['status']}" for item in rows}
        self.assertIn("ops.metrics.read|ok", event_names)
        self.assertIn("ops.metrics.read|error", event_names)


if __name__ == "__main__":
    unittest.main()
