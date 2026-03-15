import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from printnet_backend.app import create_app  # noqa: E402
from printnet_backend.compat import create_test_client  # noqa: E402
from printnet_backend.settings import BackendSettings  # noqa: E402


class AuthRoleEnforcementTests(unittest.TestCase):
    def setUp(self):
        app = create_app(
            settings=BackendSettings(
                enable_docs=False,
                operator_user_ids=("operator-1",),
                admin_user_ids=("admin-1",),
            )
        )
        self.client = create_test_client(app)

        self.student_token = self._register_and_login("student-1", "password-123")
        self.student_two_token = self._register_and_login("student-2", "password-123")
        self.operator_token = self._create_session("operator-1", "operator")
        self.admin_token = self._create_session("admin-1", "admin")

    def _register_and_login(self, user_id: str, password: str) -> str:
        register = self.client.post("/api/v1/auth/register", json={"user_id": user_id, "password": password})
        self.assertEqual(register.status_code, 200)
        login = self.client.post("/api/v1/auth/login", json={"user_id": user_id, "password": password})
        self.assertEqual(login.status_code, 200)
        return str(login.json()["session"]["token"])

    def _create_session(self, user_id: str, role: str) -> str:
        response = self.client.post("/api/v1/auth/session", json={"user_id": user_id, "role": role})
        self.assertEqual(response.status_code, 200)
        return str(response.json()["session"]["token"])

    def _register_printer_as_operator(self) -> None:
        response = self.client.post(
            "/api/v1/printers/register",
            json={
                "auth_token": self.operator_token,
                "printer_id": "printer-01",
                "name": "Lab Printer",
                "connector_type": "octoprint",
                "endpoint": "http://127.0.0.1:5000",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_profiles_requires_auth_token(self):
        response = self.client.get("/api/v1/profiles/catalog?vendor=EON")
        self.assertEqual(response.status_code, 401)
        payload = response.json()
        self.assertFalse(payload["ok"])
        self.assertEqual(payload["error"]["code"], "BACKEND_AUTHENTICATION_ERROR")

    def test_student_cannot_register_printer(self):
        response = self.client.post(
            "/api/v1/printers/register",
            json={
                "auth_token": self.student_token,
                "printer_id": "printer-01",
                "name": "Lab Printer",
                "connector_type": "octoprint",
                "endpoint": "http://127.0.0.1:5000",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["error"]["code"], "BACKEND_AUTHORIZATION_ERROR")

    def test_operator_can_register_and_list_printers(self):
        self._register_printer_as_operator()
        response = self.client.get(f"/api/v1/printers/list?auth_token={self.operator_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["printers"][0]["printer_id"], "printer-01")

    def test_student_submitter_mismatch_is_denied(self):
        self._register_printer_as_operator()
        response = self.client.post(
            "/api/v1/jobs/submit",
            json={
                "auth_token": self.student_token,
                "model_name": "part.stl",
                "profile_id": "p-default-pla",
                "requested_by": "different-user",
                "printer_id": "printer-01",
            },
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["error"]["code"], "BACKEND_AUTHORIZATION_ERROR")

    def test_student_can_view_only_own_jobs(self):
        self._register_printer_as_operator()
        created = self.client.post(
            "/api/v1/jobs/submit",
            json={
                "auth_token": self.student_token,
                "model_name": "part.stl",
                "profile_id": "p-default-pla",
                "requested_by": "student-1",
                "printer_id": "printer-01",
            },
        )
        self.assertEqual(created.status_code, 200)
        job_id = created.json()["job"]["job_id"]

        forbidden = self.client.get(f"/api/v1/jobs/status?job_id={job_id}&auth_token={self.student_two_token}")
        self.assertEqual(forbidden.status_code, 403)
        self.assertEqual(forbidden.json()["error"]["code"], "BACKEND_AUTHORIZATION_ERROR")

        allowed = self.client.get(f"/api/v1/jobs/status?job_id={job_id}&auth_token={self.student_token}")
        self.assertEqual(allowed.status_code, 200)
        self.assertEqual(allowed.json()["job"]["requested_by"], "student-1")

    def test_operator_and_admin_can_view_any_job(self):
        self._register_printer_as_operator()
        created = self.client.post(
            "/api/v1/jobs/submit",
            json={
                "auth_token": self.student_token,
                "model_name": "part.stl",
                "profile_id": "p-default-pla",
                "requested_by": "student-1",
                "printer_id": "printer-01",
            },
        )
        self.assertEqual(created.status_code, 200)
        job_id = created.json()["job"]["job_id"]

        operator_view = self.client.get(f"/api/v1/jobs/events?job_id={job_id}&auth_token={self.operator_token}")
        self.assertEqual(operator_view.status_code, 200)
        self.assertGreaterEqual(operator_view.json()["count"], 1)

        admin_view = self.client.get(f"/api/v1/jobs/status?job_id={job_id}&auth_token={self.admin_token}")
        self.assertEqual(admin_view.status_code, 200)
        self.assertEqual(admin_view.json()["job"]["job_id"], job_id)


if __name__ == "__main__":
    unittest.main()
