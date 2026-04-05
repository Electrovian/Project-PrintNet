from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


class WorkerSmokeTests(unittest.TestCase):
    def test_worker_smoke_entrypoint(self):
        script = Path(ROOT) / "scripts" / "worker_smoke.py"
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        result = subprocess.run(
            [
                sys.executable,
                str(script),
                "--backend-timeout",
                "45",
                "--worker-timeout",
                "30",
                "--worker-cycles",
                "1",
            ],
            cwd=ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"worker smoke failed with output:\n{result.stdout}",
        )
        self.assertIn("worker starting", result.stdout)
        self.assertIn("worker auth session created", result.stdout)
        self.assertIn("worker cycle ok", result.stdout)
        self.assertIn("worker smoke complete cycles=1", result.stdout)


if __name__ == "__main__":
    unittest.main()
