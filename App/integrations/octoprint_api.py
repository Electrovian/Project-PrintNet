import os
from pathlib import Path

import requests

def upload_and_print(octoprint_url: str, api_key: str, gcode_path: str) -> str:
    """Upload a G-code file to OctoPrint and start printing.

    If URL or API key are missing, this function only logs the action
    and returns a message, so the prototype is safe by default.
    """
    if not octoprint_url or not api_key:
        return ("OctoPrint URL or API key not configured. "
                "Skipping real upload; G-code is at "
                f"{gcode_path}")

    url = octoprint_url.rstrip("/") + "/api/files/local"
    headers = {"X-Api-Key": api_key}
    filename = Path(gcode_path).name

    with open(gcode_path, "rb") as f:
        files = {"file": (filename, f, "application/octet-stream")}
        data = {"select": "true", "print": "true"}
        r = requests.post(url, headers=headers, files=files, data=data, timeout=30)
        r.raise_for_status()

    return f"Uploaded {filename} to OctoPrint and started print."
