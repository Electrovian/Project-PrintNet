import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from printnet_backend.app import create_app  # noqa: E402
from printnet_backend.compat import create_test_client  # noqa: E402
from printnet_backend.settings import BackendSettings  # noqa: E402


class ActivityFeedTests(unittest.TestCase):
    def setUp(self):
        settings = BackendSettings(
            enable_docs=False,
            operator_user_ids=("operator-1",),
            activity_service_token="activity-secret",
            activity_max_jobs=1000,
            activity_max_events=20,
        )
        app = create_app(settings=settings)
        self.client = create_test_client(app)
        self.student_1_token = self._register_and_login("student-1", "password-123")
        self.student_2_token = self._register_and_login("student-2", "password-123")
        self.operator_token = self._create_session("operator-1", "operator")
        self._register_printer("printer-01")

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

    def _register_printer(self, printer_id: str) -> None:
        response = self.client.post(
            "/api/v1/printers/register",
            json={
                "auth_token": self.operator_token,
                "printer_id": printer_id,
                "name": "Lab Printer",
                "connector_type": "octoprint",
                "endpoint": "http://127.0.0.1:5000",
            },
        )
        self.assertEqual(response.status_code, 200)

    def _submit_job(self, *, token: str, requested_by: str, model_name: str) -> str:
        response = self.client.post(
            "/api/v1/jobs/submit",
            json={
                "auth_token": token,
                "model_name": model_name,
                "profile_id": "p-default-pla",
                "requested_by": requested_by,
                "printer_id": "printer-01",
            },
        )
        self.assertEqual(response.status_code, 200)
        return str(response.json()["job"]["job_id"])

    def test_activity_feed_requires_session_or_service_token(self):
        missing = self.client.get("/api/v1/activity/feed")
        self.assertEqual(missing.status_code, 401)

        invalid = self.client.get(
            "/api/v1/activity/feed",
            headers={"x-activity-service-token": "bad-token"},
        )
        self.assertEqual(invalid.status_code, 401)

        valid = self.client.get(
            "/api/v1/activity/feed?cursor=0&limit=200",
            headers={"x-activity-service-token": "activity-secret"},
        )
        self.assertEqual(valid.status_code, 200)
        self.assertIn("feed", valid.json())

    def test_activity_feed_respects_visibility_and_cursor(self):
        self._submit_job(token=self.student_1_token, requested_by="student-1", model_name="a.stl")
        self._submit_job(token=self.student_2_token, requested_by="student-2", model_name="b.stl")

        first = self.client.get(
            f"/api/v1/activity/feed?auth_token={self.operator_token}&cursor=0&limit=1"
        )
        self.assertEqual(first.status_code, 200)
        first_feed = first.json()["feed"]
        self.assertEqual(len(first_feed["items"]), 1)
        self.assertTrue(first_feed["has_more"])

        cursor_out = int(first_feed["cursor_out"])
        second = self.client.get(
            f"/api/v1/activity/feed?auth_token={self.operator_token}&cursor={cursor_out}&limit=10"
        )
        self.assertEqual(second.status_code, 200)
        second_items = second.json()["feed"]["items"]
        self.assertGreaterEqual(len(second_items), 1)
        self.assertTrue(all(int(item["seq"]) > cursor_out for item in second_items))

        student = self.client.get(
            f"/api/v1/activity/feed?auth_token={self.student_1_token}&cursor=0&limit=50"
        )
        self.assertEqual(student.status_code, 200)
        student_items = student.json()["feed"]["items"]
        self.assertTrue(student_items)
        self.assertTrue(all(item["requested_by"] == "student-1" for item in student_items))

    def test_activity_feed_reset_required_when_cursor_stale(self):
        for idx in range(30):
            self._submit_job(
                token=self.student_1_token,
                requested_by="student-1",
                model_name=f"bulk-{idx:03d}.stl",
            )
        stale = self.client.get(
            f"/api/v1/activity/feed?auth_token={self.operator_token}&cursor=1&limit=20"
        )
        self.assertEqual(stale.status_code, 200)
        self.assertTrue(stale.json()["feed"]["reset_required"])

    def test_queue_snapshot_allows_service_token_auth(self):
        self._submit_job(token=self.student_1_token, requested_by="student-1", model_name="q.stl")
        snapshot = self.client.get(
            "/api/v1/queue/snapshot",
            headers={"x-activity-service-token": "activity-secret"},
        )
        self.assertEqual(snapshot.status_code, 200)
        self.assertEqual(int(snapshot.json()["snapshot"]["job_count"]), 1)

    def test_queue_snapshot_respects_activity_max_jobs_retention(self):
        app = create_app(
            settings=BackendSettings(
                enable_docs=False,
                operator_user_ids=("operator-1",),
                activity_service_token="activity-secret",
                activity_max_jobs=2,
                activity_max_events=20,
            )
        )
        client = create_test_client(app)
        register = client.post("/api/v1/auth/register", json={"user_id": "student-x", "password": "password-123"})
        self.assertEqual(register.status_code, 200)
        login = client.post("/api/v1/auth/login", json={"user_id": "student-x", "password": "password-123"})
        self.assertEqual(login.status_code, 200)
        student_token = str(login.json()["session"]["token"])
        op = client.post("/api/v1/auth/session", json={"user_id": "operator-1", "role": "operator"})
        self.assertEqual(op.status_code, 200)
        operator_token = str(op.json()["session"]["token"])
        reg = client.post(
            "/api/v1/printers/register",
            json={
                "auth_token": operator_token,
                "printer_id": "printer-01",
                "name": "Lab Printer",
                "connector_type": "octoprint",
                "endpoint": "http://127.0.0.1:5000",
            },
        )
        self.assertEqual(reg.status_code, 200)
        for idx in range(5):
            submit = client.post(
                "/api/v1/jobs/submit",
                json={
                    "auth_token": student_token,
                    "model_name": f"retained-{idx:03d}.stl",
                    "profile_id": "p-default-pla",
                    "requested_by": "student-x",
                    "printer_id": "printer-01",
                },
            )
            self.assertEqual(submit.status_code, 200)
        snapshot = client.get(f"/api/v1/queue/snapshot?auth_token={operator_token}")
        self.assertEqual(snapshot.status_code, 200)
        self.assertEqual(int(snapshot.json()["snapshot"]["job_count"]), 2)


if __name__ == "__main__":
    unittest.main()
