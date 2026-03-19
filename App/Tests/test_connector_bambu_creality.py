from __future__ import annotations

import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from connectors.bambu_lan import BambuLanConnector  # noqa: E402
from connectors.creality import CrealityConnector  # noqa: E402


class _FakeResponse:
    def __init__(self, *, status_code: int = 200, payload: dict | None = None):
        self.status_code = int(status_code)
        self._payload = dict(payload or {})
        self.text = ""

    def json(self):
        return dict(self._payload)


class _FakeSession:
    def __init__(self):
        self.calls = []

    def request(self, method, url, **kwargs):
        self.calls.append({"method": method, "url": url, "kwargs": kwargs})
        if str(url).endswith("/api/v1/status"):
            return _FakeResponse(payload={"state": "idle", "progress_pct": 0, "file": ""})
        if str(url).endswith("/status"):
            return _FakeResponse(payload={"name": "Bambu"})
        if str(url).endswith("/api/v1/files/upload"):
            return _FakeResponse(payload={"remote_path": "job.gcode"})
        return _FakeResponse(payload={"ok": True})


class ConnectorBambuCrealityTests(unittest.TestCase):
    def test_bambu_connect_and_status(self):
        session = _FakeSession()
        connector = BambuLanConnector(session=session)
        connect_payload = connector.connect({"name": "Bambu", "bambu_url": "http://10.0.0.5:9999"})
        status_payload = connector.status({"name": "Bambu", "bambu_url": "http://10.0.0.5:9999"})
        self.assertTrue(connect_payload["ok"])
        self.assertEqual(status_payload["state"], "idle")

    def test_creality_routes_to_octoprint_delegate(self):
        connector = CrealityConnector()
        captured = {}

        def _connect(mapped):
            captured.update(mapped)
            return {"ok": True, "state": "ready"}

        connector._octoprint.connect = _connect  # type: ignore[method-assign]
        payload = connector.connect(
            {
                "name": "Creality K1",
                "connector_type": "creality",
                "creality_protocol": "octoprint",
                "creality_url": "http://10.0.0.77",
                "creality_api_key": "abc",
            }
        )
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["protocol"], "octoprint")
        self.assertEqual(captured.get("octoprint_url"), "http://10.0.0.77")
        self.assertEqual(captured.get("octoprint_api_key"), "abc")


if __name__ == "__main__":
    unittest.main()
