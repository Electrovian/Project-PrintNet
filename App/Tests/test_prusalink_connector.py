import os
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from connectors.errors import ConnectorOperationError  # noqa: E402
from connectors.prusalink import PrusaLinkConnector  # noqa: E402


class _FakeResponse:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = int(status_code)
        self._payload = payload
        self.text = str(text)

    def json(self):
        if isinstance(self._payload, Exception):
            raise self._payload
        if self._payload is None:
            raise ValueError("No JSON payload")
        return self._payload


class _FakeSession:
    def __init__(self, responses):
        self._responses = list(responses or [])
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append((str(method), str(url), kwargs))
        if not self._responses:
            return _FakeResponse(200, {})
        return self._responses.pop(0)


class PrusaLinkConnectorTests(unittest.TestCase):
    def setUp(self):
        self.printer = {
            "name": "Prusa Device",
            "prusalink_url": "http://localhost:8080",
            "prusalink_api_key": "test-key",
        }

    def test_connect_reports_missing_config(self):
        connector = PrusaLinkConnector(session=_FakeSession([]))
        result = connector.connect({"name": "Prusa Device"})
        self.assertFalse(result["ok"])
        self.assertEqual(result["state"], "missing_config")

    def test_connect_success_reads_version(self):
        session = _FakeSession([_FakeResponse(200, {"server": "PrusaLink", "api": "2.0"})])
        connector = PrusaLinkConnector(session=session)
        result = connector.connect(self.printer)
        self.assertTrue(result["ok"])
        self.assertEqual(result["state"], "ready")
        self.assertEqual(result["server"], "PrusaLink")
        self.assertEqual(result["api_version"], "2.0")
        method, url, kwargs = session.calls[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:8080/api/version")
        self.assertEqual(kwargs["headers"]["X-Api-Key"], "test-key")

    def test_upload_missing_file_raises(self):
        connector = PrusaLinkConnector(session=_FakeSession([]))
        with self.assertRaises(ConnectorOperationError):
            connector.upload(self.printer, "C:/missing-file.gcode")

    def test_upload_success_returns_remote_path(self):
        response_payload = {"files": {"local": {"path": "uploads/demo.gcode"}}}
        session = _FakeSession([_FakeResponse(201, response_payload)])
        connector = PrusaLinkConnector(session=session)
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False) as handle:
            handle.write(b"G28\n")
            path = handle.name
        try:
            result = connector.upload(self.printer, path)
            self.assertTrue(result["ok"])
            self.assertEqual(result["remote_path"], "uploads/demo.gcode")
            self.assertGreaterEqual(result["bytes"], 1)
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_start_print_uses_remote_path(self):
        session = _FakeSession([_FakeResponse(204, None)])
        connector = PrusaLinkConnector(session=session)
        result = connector.start_print(self.printer, remote_path="uploads/demo.gcode")
        self.assertTrue(result["ok"])
        self.assertEqual(result["state"], "submitted")
        method, url, kwargs = session.calls[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:8080/api/files/local/uploads/demo.gcode")
        self.assertEqual(kwargs["json"]["command"], "select")
        self.assertEqual(kwargs["json"]["print"], True)

    def test_pause_resume_cancel_send_job_commands(self):
        session = _FakeSession([_FakeResponse(204, None), _FakeResponse(204, None), _FakeResponse(204, None)])
        connector = PrusaLinkConnector(session=session)
        pause = connector.pause(self.printer)
        resume = connector.resume(self.printer)
        cancel = connector.cancel(self.printer)
        self.assertTrue(pause["ok"])
        self.assertTrue(resume["ok"])
        self.assertTrue(cancel["ok"])
        self.assertEqual(len(session.calls), 3)
        self.assertEqual(session.calls[0][2]["json"], {"command": "pause", "action": "pause"})
        self.assertEqual(session.calls[1][2]["json"], {"command": "pause", "action": "resume"})
        self.assertEqual(session.calls[2][2]["json"], {"command": "cancel"})

    def test_status_parses_response(self):
        payload = {
            "state": "Printing",
            "job": {"file": {"name": "demo.gcode"}},
            "progress": {"completion": 12.5, "printTimeLeft": 321},
        }
        session = _FakeSession([_FakeResponse(200, payload)])
        connector = PrusaLinkConnector(session=session)
        status = connector.status(self.printer)
        self.assertTrue(status["ok"])
        self.assertEqual(status["state"], "printing")
        self.assertEqual(status["file"], "demo.gcode")
        self.assertEqual(status["progress_pct"], 12.5)
        self.assertEqual(status["time_left_s"], 321)

    def test_http_error_maps_to_connector_error(self):
        session = _FakeSession([_FakeResponse(500, {"error": "boom"}, "boom")])
        connector = PrusaLinkConnector(session=session)
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False) as handle:
            handle.write(b"G28\n")
            path = handle.name
        try:
            with self.assertRaises(ConnectorOperationError):
                connector.upload(self.printer, path)
        finally:
            if os.path.exists(path):
                os.remove(path)


if __name__ == "__main__":
    unittest.main()
