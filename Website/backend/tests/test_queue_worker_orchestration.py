import os
import sys
import unittest
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from printnet_backend.app import create_app  # noqa: E402
from printnet_backend.compat import create_test_client  # noqa: E402
from printnet_backend.settings import BackendSettings  # noqa: E402


class QueueWorkerOrchestrationTests(unittest.TestCase):
    def setUp(self):
        settings = BackendSettings(
            enable_docs=False,
            operator_user_ids=("operator-1",),
            queue_name="q-lab",
            queue_worker_max_jobs_per_tick=2,
            queue_worker_heartbeat_ttl_seconds=30,
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

    def test_queue_snapshot_filters_student_visibility(self):
        self._submit_job(token=self.student_1_token, requested_by="student-1", model_name="a.stl")
        self._submit_job(token=self.student_2_token, requested_by="student-2", model_name="b.stl")

        student_snapshot = self.client.get(f"/api/v1/queue/snapshot?auth_token={self.student_1_token}")
        self.assertEqual(student_snapshot.status_code, 200)
        self.assertEqual(student_snapshot.json()["snapshot"]["job_count"], 1)

        operator_snapshot = self.client.get(f"/api/v1/queue/snapshot?auth_token={self.operator_token}")
        self.assertEqual(operator_snapshot.status_code, 200)
        self.assertEqual(operator_snapshot.json()["snapshot"]["job_count"], 2)
        self.assertEqual(operator_snapshot.json()["snapshot"]["queue_depth"], 2)

    def test_worker_tick_advances_job_status_and_events(self):
        job_id = self._submit_job(token=self.student_1_token, requested_by="student-1", model_name="part.stl")

        tick = self.client.post(
            "/api/v1/queue/worker/tick",
            json={
                "auth_token": self.operator_token,
                "worker_id": "worker-a",
                "max_jobs": 1,
            },
        )
        self.assertEqual(tick.status_code, 200)
        self.assertEqual(tick.json()["cycle"]["completed"], 1)
        self.assertEqual(list(tick.json()["cycle"]["processed_job_ids"]), [job_id])

        status = self.client.get(f"/api/v1/jobs/status?job_id={job_id}&auth_token={self.student_1_token}")
        self.assertEqual(status.status_code, 200)
        self.assertEqual(status.json()["job"]["status"], "completed")

        events = self.client.get(f"/api/v1/jobs/events?job_id={job_id}&auth_token={self.student_1_token}")
        self.assertEqual(events.status_code, 200)
        self.assertGreaterEqual(events.json()["count"], 3)

        snapshot = self.client.get(f"/api/v1/queue/snapshot?auth_token={self.operator_token}")
        self.assertEqual(snapshot.status_code, 200)
        jobs = list(snapshot.json()["snapshot"].get("jobs", []))
        row = next((item for item in jobs if str(item.get("job_id", "")).strip() == job_id), None)
        self.assertIsNotNone(row)
        assert row is not None

        created_raw = str(row.get("created_at_utc", "")).strip()
        started_raw = str(row.get("print_started_at_utc", "")).strip()
        updated_raw = str(row.get("updated_at_utc", "")).strip()
        self.assertTrue(created_raw)
        self.assertTrue(started_raw)
        self.assertTrue(updated_raw)

        created_at = datetime.fromisoformat(created_raw)
        started_at = datetime.fromisoformat(started_raw)
        updated_at = datetime.fromisoformat(updated_raw)
        self.assertGreaterEqual(started_at, created_at)
        self.assertGreaterEqual(updated_at, started_at)

        feed = self.client.get(f"/api/v1/activity/feed?auth_token={self.operator_token}&cursor=0&limit=50")
        self.assertEqual(feed.status_code, 200)
        items = list(feed.json()["feed"].get("items", []))
        completed = next(
            (
                item
                for item in items
                if str(item.get("job_id", "")).strip() == job_id
                and str(item.get("status", "")).strip().lower() == "completed"
            ),
            None,
        )
        self.assertIsNotNone(completed)
        assert completed is not None
        self.assertTrue(str(completed.get("print_started_at_utc", "")).strip())

    def test_student_cannot_tick_or_heartbeat_worker(self):
        heartbeat = self.client.post(
            "/api/v1/queue/worker/heartbeat",
            json={"auth_token": self.student_1_token, "worker_id": "student-worker"},
        )
        self.assertEqual(heartbeat.status_code, 403)

        tick = self.client.post(
            "/api/v1/queue/worker/tick",
            json={"auth_token": self.student_1_token, "worker_id": "student-worker", "max_jobs": 1},
        )
        self.assertEqual(tick.status_code, 403)

    def test_worker_tick_rejects_invalid_max_jobs(self):
        self._submit_job(token=self.student_1_token, requested_by="student-1", model_name="part.stl")
        tick = self.client.post(
            "/api/v1/queue/worker/tick",
            json={
                "auth_token": self.operator_token,
                "worker_id": "worker-a",
                "max_jobs": 0,
            },
        )
        self.assertEqual(tick.status_code, 400)
        self.assertEqual(tick.json()["error"]["code"], "BACKEND_VALIDATION_ERROR")


if __name__ == "__main__":
    unittest.main()
