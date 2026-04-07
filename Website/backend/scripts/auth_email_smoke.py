from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request


def _http_json(url: str, *, method: str = "GET", body: object | None = None, timeout: float = 15.0) -> dict:
    payload = None
    headers = {}
    if body is not None:
        payload = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=payload, headers=headers, method=method.upper())
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _mailpit_messages(mailpit_base_url: str) -> list[dict]:
    payload = _http_json(f"{mailpit_base_url.rstrip('/')}/api/v1/messages")
    messages = payload.get("messages")
    if not isinstance(messages, list):
        return []
    return [dict(item) for item in messages if isinstance(item, dict)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend-base-url", required=True, help="Example: http://192.168.1.145:8000/api/v1")
    parser.add_argument("--mailpit-base-url", default="http://127.0.0.1:8025")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--timeout-seconds", type=float, default=30.0)
    args = parser.parse_args()

    backend_base = str(args.backend_base_url or "").rstrip("/")
    mailpit_base = str(args.mailpit_base_url or "").rstrip("/")
    user_id = str(args.user_id or "").strip()
    password = str(args.password or "")

    before = _mailpit_messages(mailpit_base)
    before_ids = {str(item.get("ID", "")).strip() for item in before}

    challenge_payload = _http_json(
        f"{backend_base}/auth/login/request-code",
        method="POST",
        body={"user_id": user_id, "password": password},
    )
    challenge = dict(challenge_payload.get("challenge") or {})
    delivery = dict(challenge.get("delivery") or {})
    if str(delivery.get("channel", "")).strip().lower() != "smtp":
        raise RuntimeError(f"Expected SMTP delivery, got {delivery!r}")

    deadline = time.time() + max(1.0, float(args.timeout_seconds))
    matched = None
    while time.time() < deadline:
        for item in _mailpit_messages(mailpit_base):
            message_id = str(item.get("ID", "")).strip()
            if not message_id or message_id in before_ids:
                continue
            to_rows = item.get("To") or []
            recipients = {
                str(entry.get("Address", "")).strip().lower()
                for entry in to_rows
                if isinstance(entry, dict)
            }
            subject = str(item.get("Subject", "")).strip()
            if user_id.lower() in recipients and subject == "EON PrintNet verification code":
                matched = item
                break
        if matched is not None:
            break
        time.sleep(0.5)

    if matched is None:
        raise RuntimeError("Verification email did not appear in Mailpit before timeout.")

    result = {
        "ok": True,
        "challenge_id": str(challenge.get("challenge_id", "")).strip(),
        "delivery_channel": str(delivery.get("channel", "")).strip(),
        "delivery_destination": str(delivery.get("destination", "")).strip(),
        "mailpit_message_id": str(matched.get("ID", "")).strip(),
        "mailpit_subject": str(matched.get("Subject", "")).strip(),
        "mailpit_snippet": str(matched.get("Snippet", "")).strip(),
    }
    print(json.dumps(result, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        print(body or str(exc), file=sys.stderr)
        raise
