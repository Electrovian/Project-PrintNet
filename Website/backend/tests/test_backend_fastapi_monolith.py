import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from printnet_backend.app import create_app  # noqa: E402
from printnet_backend.compat import HAS_FASTAPI, create_test_client  # noqa: E402
from printnet_backend.errors import (  # noqa: E402
    BackendConflictError,
    BackendNotFoundError,
    BackendValidationError,
    http_status_for_error,
)
from printnet_backend.services import BackendState  # noqa: E402
from printnet_backend.settings import BackendSettings  # noqa: E402


class BackendFastApiMonolithTests(unittest.TestCase):
    def test_settings_from_env(self):
        settings = BackendSettings.from_env(
            {
                "BACKEND_APP_NAME": "PrintNet API",
                "BACKEND_APP_VERSION": "1.2.3",
                "BACKEND_API_PREFIX": "api/custom",
                "BACKEND_ENV": "development",
                "BACKEND_DEFAULT_ROLE": "operator",
                "BACKEND_ALLOW_CLIENT_ROLE_OVERRIDE": "1",
                "BACKEND_OPERATOR_USER_IDS": "operator-1,worker-01",
                "BACKEND_ADMIN_USER_IDS": "admin-1",
                "BACKEND_ENABLE_DOCS": "0",
                "BACKEND_REGION_BLOCK_ENABLED": "1",
                "BACKEND_REGION_BLOCK_ON_UNKNOWN": "allow",
                "BACKEND_REGION_BLOCK_TRUST_HEADERS": "x-custom-geo,x-state",
                "BACKEND_BLOCKED_US_STATE_CODES": "CA,NY",
                "BACKEND_ACTIVITY_SERVICE_TOKEN": "activity-secret",
                "BACKEND_ACTIVITY_MAX_JOBS": "1500",
                "BACKEND_ACTIVITY_MAX_EVENTS": "8000",
                "BACKEND_QUEUE_NAME": "lab-a",
                "BACKEND_QUEUE_WORKER_MAX_JOBS_PER_TICK": "3",
                "BACKEND_QUEUE_WORKER_HEARTBEAT_TTL_SECONDS": "120",
                "BACKEND_OBSERVABILITY_MAX_AUDIT_RECORDS": "220",
                "BACKEND_OBSERVABILITY_MAX_METRIC_KEYS": "300",
                "BACKEND_SUPER_ADMIN_EMAIL": "admin@example.com",
                "BACKEND_SUPER_ADMIN_PASSWORD": "password-123",
                "BACKEND_AUTH_VERIFICATION_CODE_TTL_SECONDS": "900",
                "BACKEND_AUTH_VERIFICATION_MAX_ATTEMPTS": "4",
                "BACKEND_AUTH_EXPOSE_DEBUG_CODE": "1",
                "BACKEND_AUTH_EMAIL_FROM": "security@example.com",
                "BACKEND_SMTP_HOST": "smtp.example.com",
                "BACKEND_SMTP_PORT": "2525",
                "BACKEND_SMTP_USERNAME": "smtp-user",
                "BACKEND_SMTP_PASSWORD": "smtp-pass",
                "BACKEND_SMTP_STARTTLS": "0",
                "BACKEND_SMTP_USE_SSL": "1",
                "BACKEND_RELEASE_REQUIRED_CHECKS": "backend_health,authz_enforced,queue_worker_operational",
            }
        )
        self.assertEqual(settings.app_name, "PrintNet API")
        self.assertEqual(settings.app_version, "1.2.3")
        self.assertEqual(settings.api_prefix, "/api/custom")
        self.assertEqual(settings.backend_env, "development")
        self.assertEqual(settings.default_role, "operator")
        self.assertTrue(settings.allow_client_role_override)
        self.assertEqual(settings.operator_user_ids, ("operator-1", "worker-01"))
        self.assertEqual(settings.admin_user_ids, ("admin-1",))
        self.assertFalse(settings.enable_docs)
        self.assertTrue(settings.region_block_enabled)
        self.assertEqual(settings.region_block_on_unknown, "allow")
        self.assertEqual(settings.region_block_trust_headers, ("x-custom-geo", "x-state"))
        self.assertEqual(settings.blocked_us_state_codes, ("CA", "NY"))
        self.assertEqual(settings.activity_service_token, "activity-secret")
        self.assertEqual(settings.activity_max_jobs, 1500)
        self.assertEqual(settings.activity_max_events, 8000)
        self.assertEqual(settings.queue_name, "lab-a")
        self.assertEqual(settings.queue_worker_max_jobs_per_tick, 3)
        self.assertEqual(settings.queue_worker_heartbeat_ttl_seconds, 120)
        self.assertEqual(settings.observability_max_audit_records, 220)
        self.assertEqual(settings.observability_max_metric_keys, 300)
        self.assertEqual(settings.super_admin_email, "admin@example.com")
        self.assertEqual(settings.super_admin_password, "password-123")
        self.assertEqual(settings.auth_verification_code_ttl_seconds, 900)
        self.assertEqual(settings.auth_verification_max_attempts, 4)
        self.assertTrue(settings.auth_expose_debug_code)
        self.assertEqual(settings.auth_email_from, "security@example.com")
        self.assertEqual(settings.smtp_host, "smtp.example.com")
        self.assertEqual(settings.smtp_port, 2525)
        self.assertEqual(settings.smtp_username, "smtp-user")
        self.assertEqual(settings.smtp_password, "smtp-pass")
        self.assertFalse(settings.smtp_starttls)
        self.assertTrue(settings.smtp_use_ssl)
        self.assertEqual(
            settings.release_required_checks,
            ("backend_health", "authz_enforced", "queue_worker_operational"),
        )

    def test_service_register_and_submit_job(self):
        state = BackendState(queue_name="q1")
        printer = state.register_printer(
            printer_id="printer-01",
            name="Lab Printer",
            connector_type="octoprint",
            endpoint="http://127.0.0.1:5000",
        )
        self.assertEqual(printer.printer_id, "printer-01")
        self.assertEqual(len(state.list_printers()), 1)
        job = state.submit_job(
            model_name="part.stl",
            profile_id="p-default-pla",
            requested_by="student-1",
            printer_id="printer-01",
        )
        self.assertEqual(job.status, "queued")
        loaded = state.get_job(job.job_id)
        self.assertEqual(loaded.job_id, job.job_id)

    def test_error_status_mapping(self):
        self.assertEqual(http_status_for_error(BackendValidationError("x")), 400)
        self.assertEqual(http_status_for_error(BackendNotFoundError("x")), 404)
        self.assertEqual(http_status_for_error(BackendConflictError("x")), 409)
        self.assertEqual(http_status_for_error(RuntimeError("x")), 500)

    def test_app_routes_end_to_end(self):
        app = create_app(
            settings=BackendSettings(
                enable_docs=False,
                operator_user_ids=("operator-1",),
            )
        )
        client = create_test_client(app)

        live = client.get("/api/v1/health/live")
        self.assertEqual(live.status_code, 200)
        self.assertTrue(live.json()["ok"])

        register = client.post(
            "/api/v1/auth/register",
            json={"user_id": "student-1", "password": "password-123"},
        )
        self.assertEqual(register.status_code, 200)
        self.assertEqual(register.json()["account"]["role"], "student")

        login = client.post(
            "/api/v1/auth/login",
            json={"user_id": "student-1", "password": "password-123"},
        )
        self.assertEqual(login.status_code, 200)
        self.assertTrue(login.json()["ok"])
        student_token = login.json()["session"]["token"]
        self.assertTrue(str(student_token).startswith("session-"))
        self.assertEqual(login.json()["session"]["role"], "student")

        escalated = client.post(
            "/api/v1/auth/session",
            json={"user_id": "student-1", "role": "admin"},
        )
        self.assertEqual(escalated.status_code, 401)
        self.assertEqual(escalated.json()["error"]["code"], "BACKEND_AUTHENTICATION_ERROR")

        operator = client.post(
            "/api/v1/auth/session",
            json={"user_id": "operator-1", "role": "operator"},
        )
        self.assertEqual(operator.status_code, 200)
        operator_token = operator.json()["session"]["token"]

        whoami = client.get(f"/api/v1/auth/whoami?auth_token={student_token}")
        self.assertEqual(whoami.status_code, 200)
        self.assertEqual(whoami.json()["identity"]["user_id"], "student-1")

        profiles = client.get(f"/api/v1/profiles/catalog?auth_token={student_token}&vendor=EON&filament=PLA")
        self.assertEqual(profiles.status_code, 200)
        self.assertGreaterEqual(int(profiles.json()["count"]), 1)

        printer = client.post(
            "/api/v1/printers/register",
            json={
                "auth_token": operator_token,
                "printer_id": "printer-01",
                "name": "Lab Printer",
                "connector_type": "moonraker",
                "endpoint": "http://127.0.0.1:7125",
            },
        )
        self.assertEqual(printer.status_code, 200)
        self.assertTrue(printer.json()["ok"])

        job = client.post(
            "/api/v1/jobs/submit",
            json={
                "auth_token": student_token,
                "model_name": "part.stl",
                "profile_id": "p-default-pla",
                "requested_by": "student-1",
                "printer_id": "printer-01",
            },
        )
        self.assertEqual(job.status_code, 200)
        job_id = job.json()["job"]["job_id"]

        status = client.get(f"/api/v1/jobs/status?job_id={job_id}&auth_token={student_token}")
        self.assertEqual(status.status_code, 200)
        self.assertEqual(status.json()["job"]["job_id"], job_id)

        events = client.get(f"/api/v1/jobs/events?job_id={job_id}&auth_token={student_token}")
        self.assertEqual(events.status_code, 200)
        self.assertGreaterEqual(int(events.json()["count"]), 1)

        queue_snapshot = client.get(f"/api/v1/queue/snapshot?auth_token={student_token}")
        self.assertEqual(queue_snapshot.status_code, 200)
        self.assertGreaterEqual(int(queue_snapshot.json()["snapshot"]["job_count"]), 1)

    def test_app_validation_failure_returns_400(self):
        app = create_app(settings=BackendSettings(enable_docs=False))
        client = create_test_client(app)
        resp = client.post("/api/v1/auth/session", json={"user_id": ""})
        self.assertEqual(resp.status_code, 400)
        payload = resp.json()
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["code"], "BACKEND_VALIDATION_ERROR")

    @unittest.skipUnless(HAS_FASTAPI, "requires FastAPI middleware support")
    def test_region_block_rejects_california(self):
        app = create_app(
            settings=BackendSettings(
                enable_docs=False,
                region_block_enabled=True,
                region_block_on_unknown="allow",
                blocked_us_state_codes=("CA",),
            )
        )
        client = create_test_client(app)
        resp = client.get("/api/v1/health/live", headers={"x-us-state": "CA"})
        self.assertEqual(resp.status_code, 451)
        payload = resp.json()
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["code"], "REGION_BLOCKED")

    @unittest.skipUnless(HAS_FASTAPI, "requires FastAPI middleware support")
    def test_region_block_allows_non_blocked_state(self):
        app = create_app(
            settings=BackendSettings(
                enable_docs=False,
                region_block_enabled=True,
                region_block_on_unknown="allow",
                blocked_us_state_codes=("CA",),
            )
        )
        client = create_test_client(app)
        resp = client.get("/api/v1/health/live", headers={"x-us-state": "NY"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["ok"])

    @unittest.skipUnless(HAS_FASTAPI, "requires FastAPI middleware support")
    def test_region_block_can_be_disabled(self):
        app = create_app(
            settings=BackendSettings(
                enable_docs=False,
                region_block_enabled=False,
                region_block_on_unknown="deny",
                blocked_us_state_codes=("CA",),
            )
        )
        client = create_test_client(app)
        resp = client.get("/api/v1/health/live", headers={"x-us-state": "CA"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.json()["ok"])

    @unittest.skipUnless(HAS_FASTAPI, "requires FastAPI middleware support")
    def test_region_block_unknown_geo_denied_in_production_mode(self):
        app = create_app(
            settings=BackendSettings(
                enable_docs=False,
                backend_env="production",
                region_block_enabled=True,
                region_block_on_unknown="deny",
                blocked_us_state_codes=("CA",),
            )
        )
        client = create_test_client(app)
        resp = client.get("/api/v1/health/live")
        self.assertEqual(resp.status_code, 451)
        payload = resp.json()
        self.assertEqual(payload["error"]["code"], "REGION_GEO_UNDETERMINED")

    @unittest.skipUnless(HAS_FASTAPI, "requires FastAPI middleware support")
    def test_region_block_unknown_geo_allowed_in_development_mode(self):
        app = create_app(
            settings=BackendSettings(
                enable_docs=False,
                backend_env="development",
                region_block_enabled=True,
                region_block_on_unknown="allow",
                blocked_us_state_codes=("CA",),
            )
        )
        client = create_test_client(app)
        resp = client.get("/api/v1/health/live")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("x-compliance-warning"), "REGION_GEO_UNDETERMINED")

    @unittest.skipUnless(HAS_FASTAPI, "requires FastAPI middleware support")
    def test_compliance_region_endpoint_reports_decision_for_blocked_state(self):
        app = create_app(
            settings=BackendSettings(
                enable_docs=False,
                backend_env="production",
                region_block_enabled=True,
                region_block_on_unknown="deny",
                blocked_us_state_codes=("CA",),
            )
        )
        client = create_test_client(app)
        resp = client.get("/api/v1/compliance/region", headers={"x-us-state": "CA"})
        self.assertEqual(resp.status_code, 200)
        payload = resp.json()
        self.assertTrue(payload["ok"])
        compliance = payload["compliance"]
        self.assertEqual(compliance["decision"], "deny")
        self.assertEqual(compliance["reason_code"], "REGION_BLOCKED")
        self.assertEqual(compliance["http_status"], 451)


if __name__ == "__main__":
    unittest.main()
