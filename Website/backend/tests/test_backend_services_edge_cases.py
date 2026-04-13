import base64
import os
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from printnet_backend.errors import (  # noqa: E402
    BackendNotFoundError,
    BackendOrchestrationError,
    BackendValidationError,
)
from printnet_backend.services import (  # noqa: E402
    BackendState,
    _as_bounded_int,
    _normalize_model_store_dir,
    _normalize_required_checks,
    _sanitize_upload_file_name,
    _sanitize_upload_owner,
)


class BackendServicesEdgeCasesTests(unittest.TestCase):
    def test_as_bounded_int_validation(self):
        self.assertEqual(_as_bounded_int("4", field="f", minimum=1, maximum=10), 4)
        with self.assertRaises(BackendValidationError):
            _as_bounded_int(True, field="f", minimum=1, maximum=10)
        with self.assertRaises(BackendValidationError):
            _as_bounded_int("bad", field="f", minimum=1, maximum=10)
        with self.assertRaises(BackendValidationError):
            _as_bounded_int(99, field="f", minimum=1, maximum=10)

    def test_normalize_required_checks(self):
        self.assertEqual(
            _normalize_required_checks(("a", "a", "b", "")),
            ("a", "b"),
        )
        self.assertEqual(
            _normalize_required_checks(["x", "x", "y"]),
            ("x", "y"),
        )
        self.assertEqual(
            _normalize_required_checks("r1,r2, r2"),
            ("r1", "r2"),
        )
        self.assertEqual(
            _normalize_required_checks(None),
            (),
        )

    def test_upload_sanitizers(self):
        self.assertEqual(_sanitize_upload_owner("User Name!"), "user-name")
        self.assertEqual(_sanitize_upload_owner(""), "web-user")
        self.assertEqual(_sanitize_upload_file_name("model.step"), "model.step")
        self.assertEqual(_sanitize_upload_file_name("unsafe<>name"), "unsafe_name.stl")
        self.assertEqual(_sanitize_upload_file_name(""), "")

    def test_model_store_dir_normalization(self):
        resolved = _normalize_model_store_dir("")
        self.assertTrue(resolved.endswith(os.path.join("Website", "backend", "runtime", "uploads")))
        self.assertEqual(resolved, BackendState().model_store_dir)
        self.assertEqual(_normalize_model_store_dir("Website/backend/uploads"), resolved)
        self.assertEqual(_normalize_model_store_dir("Website/backend/Website/backend/uploads"), resolved)
        custom = _normalize_model_store_dir("Website/backend/custom_uploads")
        self.assertTrue(custom.endswith(os.path.join("Website", "backend", "custom_uploads")))

    def test_submit_job_validation_paths(self):
        state = BackendState(queue_name="lab-q")
        state.register_printer(
            printer_id="printer-1",
            name="P1",
            connector_type="octoprint",
            endpoint="http://127.0.0.1:5000",
        )

        with self.assertRaises(BackendValidationError):
            state.submit_job(model_name="", profile_id="p-default-pla", requested_by="student-1")
        with self.assertRaises(BackendValidationError):
            state.submit_job(model_name="part.stl", profile_id="", requested_by="student-1")
        with self.assertRaises(BackendNotFoundError):
            state.submit_job(model_name="part.stl", profile_id="missing-profile", requested_by="student-1")
        with self.assertRaises(BackendValidationError):
            state.submit_job(model_name="part.stl", profile_id="p-default-pla", requested_by="")
        with self.assertRaises(BackendNotFoundError):
            state.submit_job(
                model_name="part.stl",
                profile_id="p-default-pla",
                requested_by="student-1",
                printer_id="missing-printer",
            )

    def test_private_job_state_guards(self):
        state = BackendState(queue_name="lab-q")
        with self.assertRaises(BackendNotFoundError):
            state._append_job_event("missing-job", "event")  # noqa: SLF001

        pending = state.submit_job(
            model_name="part.stl",
            profile_id="p-default-pla",
            requested_by="student-1",
        )
        with self.assertRaises(BackendValidationError):
            state._append_job_event(pending.job_id, "")  # noqa: SLF001
        with self.assertRaises(BackendValidationError):
            state._set_job_status(pending.job_id, "bad-status", "event")  # noqa: SLF001
        with self.assertRaises(BackendValidationError):
            state._process_queued_job("")  # noqa: SLF001
        with self.assertRaises(BackendOrchestrationError):
            state._process_queued_job(pending.job_id)  # noqa: SLF001

    def test_store_uploaded_model_validation_and_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = BackendState(model_store_dir=tmp)
            with self.assertRaises(BackendValidationError):
                state.store_uploaded_model(file_name="", data_base64="abc", requested_by="user")
            with self.assertRaises(BackendValidationError):
                state.store_uploaded_model(file_name="part.stl", data_base64="", requested_by="user")
            with self.assertRaises(BackendValidationError):
                state.store_uploaded_model(file_name="part.stl", data_base64="not-base64", requested_by="user")

            payload = base64.b64encode(b"solid stl bytes").decode("ascii")
            result = state.store_uploaded_model(
                file_name="part.stl",
                data_base64=payload,
                requested_by="student-1",
            )
            self.assertIn("model_name", result)
            self.assertGreater(int(result["size_bytes"]), 0)
            self.assertTrue(os.path.exists(str(result["stored_path"])))

    def test_store_uploaded_model_repairs_owner_writable_directory(self):
        if os.name == "nt":
            self.skipTest("chmod-based directory mode repair is not portable on Windows hosts")
        with tempfile.TemporaryDirectory() as tmp:
            upload_dir = os.path.join(tmp, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            os.chmod(upload_dir, 0o555)
            state = BackendState(model_store_dir=upload_dir)
            payload = base64.b64encode(b"solid stl bytes").decode("ascii")
            result = state.store_uploaded_model(
                file_name="part.stl",
                data_base64=payload,
                requested_by="student-1",
            )
            self.assertTrue(os.path.exists(str(result["stored_path"])))

    def test_status_and_observability_snapshots(self):
        state = BackendState(queue_name="lab-q")
        state.create_session(user_id="operator-1", role="operator", trusted_role=True)
        state.append_security_audit(
            actor="operator-1",
            action="test",
            resource="job",
            outcome="ok",
            details={"auth_token": "secret"},
        )
        metrics = state.record_operation_metric(event="edge.case", status="ok", duration_ms=1.2)
        self.assertEqual(metrics["event"], "edge.case")
        release = state.set_release_readiness_check(
            check_name="authz_enforced",
            passed=True,
            detail="ok",
        )
        self.assertEqual(release["name"], "authz_enforced")
        audit_rows = state.observability_audit_snapshot(limit="5")
        self.assertGreaterEqual(len(audit_rows), 1)
        snapshot = state.status_snapshot()
        self.assertEqual(snapshot["queue"], "lab-q")
        self.assertGreaterEqual(int(snapshot["sessions"]), 1)


if __name__ == "__main__":
    unittest.main()
