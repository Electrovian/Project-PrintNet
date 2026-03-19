import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from printnet_backend.app import create_app  # noqa: E402
from printnet_backend.compat import create_test_client  # noqa: E402
from printnet_backend.settings import BackendSettings  # noqa: E402


class AuthAccountSecurityTests(unittest.TestCase):
    def setUp(self):
        app = create_app(
            settings=BackendSettings(
                enable_docs=False,
                operator_user_ids=("operator-1",),
                admin_user_ids=("admin-1",),
                super_admin_email="owner@example.com",
                super_admin_password="password-123",
                auth_expose_debug_code=True,
            )
        )
        self.client = create_test_client(app)

    def test_register_and_login_require_real_account(self):
        register = self.client.post(
            "/api/v1/auth/register",
            json={"user_id": "Student.One", "password": "password-123"},
        )
        self.assertEqual(register.status_code, 200)
        self.assertEqual(register.json()["account"]["user_id"], "student.one")
        self.assertEqual(register.json()["account"]["role"], "student")

        login = self.client.post(
            "/api/v1/auth/login",
            json={"user_id": "student.one", "password": "password-123"},
        )
        self.assertEqual(login.status_code, 200)
        token = str(login.json()["session"]["token"])
        whoami = self.client.get(f"/api/v1/auth/whoami?auth_token={token}")
        self.assertEqual(whoami.status_code, 200)
        self.assertEqual(whoami.json()["identity"]["user_id"], "student.one")
        self.assertEqual(whoami.json()["identity"]["role"], "student")

    def test_login_rejects_unknown_or_bad_password(self):
        unknown = self.client.post(
            "/api/v1/auth/login",
            json={"user_id": "missing-user", "password": "password-123"},
        )
        self.assertEqual(unknown.status_code, 401)
        self.assertEqual(unknown.json()["error"]["code"], "BACKEND_AUTHENTICATION_ERROR")

        register = self.client.post(
            "/api/v1/auth/register",
            json={"user_id": "student-two", "password": "password-123"},
        )
        self.assertEqual(register.status_code, 200)

        bad_password = self.client.post(
            "/api/v1/auth/login",
            json={"user_id": "student-two", "password": "wrong-password"},
        )
        self.assertEqual(bad_password.status_code, 401)
        self.assertEqual(bad_password.json()["error"]["code"], "BACKEND_AUTHENTICATION_ERROR")

    def test_self_registration_cannot_escalate_role(self):
        response = self.client.post(
            "/api/v1/auth/register",
            json={"user_id": "attacker", "password": "password-123", "role": "admin"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "BACKEND_VALIDATION_ERROR")

    def test_registered_student_cannot_access_operator_route(self):
        register = self.client.post(
            "/api/v1/auth/register",
            json={"user_id": "student-three", "password": "password-123"},
        )
        self.assertEqual(register.status_code, 200)
        token = str(register.json()["session"]["token"])

        denied = self.client.post(
            "/api/v1/printers/register",
            json={
                "auth_token": token,
                "printer_id": "printer-01",
                "name": "Lab Printer",
                "connector_type": "octoprint",
                "endpoint": "http://127.0.0.1:5000",
            },
        )
        self.assertEqual(denied.status_code, 403)
        self.assertEqual(denied.json()["error"]["code"], "BACKEND_AUTHORIZATION_ERROR")

    def test_legacy_session_rejects_unconfigured_worker_alias(self):
        response = self.client.post(
            "/api/v1/auth/session",
            json={"user_id": "worker-rogue", "role": "operator"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"]["code"], "BACKEND_AUTHENTICATION_ERROR")

    def test_super_admin_password_login_requires_verification(self):
        response = self.client.post(
            "/api/v1/auth/login",
            json={"user_id": "owner@example.com", "password": "password-123"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"]["code"], "BACKEND_AUTHENTICATION_ERROR")

    def test_super_admin_two_step_login_flow(self):
        request_code = self.client.post(
            "/api/v1/auth/login/request-code",
            json={"user_id": "owner@example.com", "password": "password-123"},
        )
        self.assertEqual(request_code.status_code, 200)
        challenge = request_code.json()["challenge"]
        challenge_id = str(challenge["challenge_id"])
        debug_code = str(challenge.get("debug_code", ""))
        self.assertTrue(challenge_id.startswith("challenge-"))
        self.assertEqual(challenge["role"], "admin")
        self.assertTrue(debug_code)

        verify = self.client.post(
            "/api/v1/auth/login/verify-code",
            json={"challenge_id": challenge_id, "verification_code": debug_code},
        )
        self.assertEqual(verify.status_code, 200)
        token = str(verify.json()["session"]["token"])
        self.assertTrue(token.startswith("session-"))
        self.assertEqual(verify.json()["session"]["role"], "admin")

        whoami = self.client.get(f"/api/v1/auth/whoami?auth_token={token}")
        self.assertEqual(whoami.status_code, 200)
        self.assertEqual(whoami.json()["identity"]["user_id"], "owner@example.com")
        self.assertEqual(whoami.json()["identity"]["role"], "admin")

    def test_super_admin_verification_rejects_bad_code(self):
        request_code = self.client.post(
            "/api/v1/auth/login/request-code",
            json={"user_id": "owner@example.com", "password": "password-123"},
        )
        self.assertEqual(request_code.status_code, 200)
        challenge_id = str(request_code.json()["challenge"]["challenge_id"])

        verify = self.client.post(
            "/api/v1/auth/login/verify-code",
            json={"challenge_id": challenge_id, "verification_code": "000000"},
        )
        self.assertEqual(verify.status_code, 401)
        self.assertEqual(verify.json()["error"]["code"], "BACKEND_AUTHENTICATION_ERROR")


if __name__ == "__main__":
    unittest.main()
