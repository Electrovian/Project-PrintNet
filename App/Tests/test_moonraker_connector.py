import os
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from connectors.errors import ConnectorOperationError  # noqa: E402
from connectors.moonraker import MoonrakerConnector  # noqa: E402


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


class MoonrakerConnectorTests(unittest.TestCase):
    def setUp(self):
        self.printer = {
            "name": "Moon Device",
            "moonraker_url": "http://localhost:7125",
        }

    def test_connect_reports_missing_config(self):
        connector = MoonrakerConnector(session=_FakeSession([]))
        result = connector.connect({"name": "Moon Device"})
        self.assertFalse(result["ok"])
        self.assertEqual(result["state"], "missing_config")

    def test_connect_success_reads_server_info(self):
        payload = {"result": {"moonraker_version": "v0.9.3"}}
        session = _FakeSession([_FakeResponse(200, payload)])
        connector = MoonrakerConnector(session=session)
        result = connector.connect(self.printer)
        self.assertTrue(result["ok"])
        self.assertEqual(result["state"], "ready")
        self.assertEqual(result["version"], "v0.9.3")
        method, url, _kwargs = session.calls[0]
        self.assertEqual(method, "GET")
        self.assertEqual(url, "http://localhost:7125/server/info")

    def test_upload_missing_file_raises(self):
        connector = MoonrakerConnector(session=_FakeSession([]))
        with self.assertRaises(ConnectorOperationError):
            connector.upload(self.printer, "C:/missing-file.gcode")

    def test_upload_success_returns_remote_path(self):
        payload = {"result": {"item": {"path": "gcodes/demo.gcode"}}}
        session = _FakeSession([_FakeResponse(201, payload)])
        connector = MoonrakerConnector(session=session)
        with tempfile.NamedTemporaryFile(suffix=".gcode", delete=False) as handle:
            handle.write(b"G28\n")
            path = handle.name
        try:
            result = connector.upload(self.printer, path)
            self.assertTrue(result["ok"])
            self.assertEqual(result["remote_path"], "gcodes/demo.gcode")
            self.assertGreaterEqual(result["bytes"], 1)
            method, url, kwargs = session.calls[0]
            self.assertEqual(method, "POST")
            self.assertEqual(url, "http://localhost:7125/server/files/upload")
            self.assertEqual(kwargs["data"]["root"], "gcodes")
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_start_print_uses_filename_query(self):
        session = _FakeSession([_FakeResponse(200, {"result": "ok"})])
        connector = MoonrakerConnector(session=session)
        result = connector.start_print(self.printer, remote_path="gcodes/demo.gcode")
        self.assertTrue(result["ok"])
        method, url, _kwargs = session.calls[0]
        self.assertEqual(method, "POST")
        self.assertEqual(url, "http://localhost:7125/printer/print/start?filename=gcodes/demo.gcode")

    def test_pause_resume_cancel_send_expected_endpoints(self):
        session = _FakeSession([_FakeResponse(200, {}), _FakeResponse(200, {}), _FakeResponse(200, {})])
        connector = MoonrakerConnector(session=session)
        pause = connector.pause(self.printer)
        resume = connector.resume(self.printer)
        cancel = connector.cancel(self.printer)
        self.assertTrue(pause["ok"])
        self.assertTrue(resume["ok"])
        self.assertTrue(cancel["ok"])
        self.assertEqual(session.calls[0][1], "http://localhost:7125/printer/print/pause")
        self.assertEqual(session.calls[1][1], "http://localhost:7125/printer/print/resume")
        self.assertEqual(session.calls[2][1], "http://localhost:7125/printer/print/cancel")

    def test_status_parses_state_file_and_progress(self):
        payload = {
            "result": {
                "status": {
                    "print_stats": {"state": "printing", "filename": "demo.gcode", "print_duration": 50.0},
                    "virtual_sdcard": {"progress": 0.5},
                }
            }
        }
        session = _FakeSession([_FakeResponse(200, payload)])
        connector = MoonrakerConnector(session=session)
        status = connector.status(self.printer)
        self.assertTrue(status["ok"])
        self.assertEqual(status["state"], "printing")
        self.assertEqual(status["file"], "demo.gcode")
        self.assertEqual(status["progress_pct"], 50.0)
        self.assertEqual(status["time_left_s"], 50)

    def test_http_error_maps_to_connector_error(self):
        session = _FakeSession([_FakeResponse(500, {"error": "boom"}, "boom")])
        connector = MoonrakerConnector(session=session)
        with self.assertRaises(ConnectorOperationError):
            connector.status(self.printer)


if __name__ == "__main__":
    unittest.main()
