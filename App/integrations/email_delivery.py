from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from typing import Mapping
from urllib.parse import quote


class EmailDeliveryError(RuntimeError):
    """Email delivery failed."""


class EmailConfigurationError(EmailDeliveryError):
    """Email delivery could not start because configuration is incomplete."""


def _read_bool(value: object, *, default: bool) -> bool:
    text = str(value if value is not None else ("1" if default else "0")).strip().lower()
    if text in ("1", "true", "yes", "on"):
        return True
    if text in ("0", "false", "no", "off"):
        return False
    return bool(default)


def smtp_settings_from_env(env: Mapping[str, str] | None = None) -> dict[str, object]:
    source = env or os.environ
    host = str(source.get("BACKEND_SMTP_HOST", "") or "").strip()
    port_raw = str(source.get("BACKEND_SMTP_PORT", "587") or "587").strip()
    try:
        port = int(port_raw)
    except Exception:
        port = 587
    if port <= 0:
        port = 587
    username = str(source.get("BACKEND_SMTP_USERNAME", "") or "").strip()
    password = str(source.get("BACKEND_SMTP_PASSWORD", "") or "")
    sender = str(source.get("BACKEND_AUTH_EMAIL_FROM", "") or "").strip() or username or "no-reply@printnet.local"
    starttls = _read_bool(source.get("BACKEND_SMTP_STARTTLS", "1"), default=True)
    use_ssl = _read_bool(source.get("BACKEND_SMTP_USE_SSL", "0"), default=False)
    return {
        "host": host,
        "port": port,
        "username": username,
        "password": password,
        "sender": sender,
        "starttls": starttls,
        "use_ssl": use_ssl,
    }


def send_email_via_smtp(
    *,
    recipient: str,
    subject: str,
    body: str,
    env: Mapping[str, str] | None = None,
) -> dict[str, object]:
    normalized_recipient = str(recipient or "").strip()
    if not normalized_recipient:
        raise EmailConfigurationError("Recipient email address is required.")

    normalized_subject = str(subject or "").strip() or "EON-OpenSlicer message"
    normalized_body = str(body or "").strip()
    settings = smtp_settings_from_env(env)
    host = str(settings.get("host", "") or "").strip()
    if not host:
        raise EmailConfigurationError("SMTP is not configured.")

    message = EmailMessage()
    message["From"] = str(settings.get("sender", "no-reply@printnet.local"))
    message["To"] = normalized_recipient
    message["Subject"] = normalized_subject
    message.set_content(normalized_body)

    try:
        if bool(settings.get("use_ssl", False)):
            client = smtplib.SMTP_SSL(host, int(settings.get("port", 587)), timeout=10)
        else:
            client = smtplib.SMTP(host, int(settings.get("port", 587)), timeout=10)
        with client:
            if bool(settings.get("starttls", True)) and not bool(settings.get("use_ssl", False)):
                client.starttls()
            username = str(settings.get("username", "") or "").strip()
            if username:
                client.login(username, str(settings.get("password", "") or ""))
            client.send_message(message)
    except Exception as exc:
        raise EmailDeliveryError(f"SMTP send failed: {exc}") from exc

    return dict(settings)


def build_mailto_url(*, recipient: str, subject: str, body: str) -> str:
    normalized_recipient = str(recipient or "").strip()
    if not normalized_recipient:
        raise EmailConfigurationError("Recipient email address is required.")
    normalized_subject = str(subject or "").strip()
    normalized_body = str(body or "")
    return (
        f"mailto:{quote(normalized_recipient)}"
        f"?subject={quote(normalized_subject)}"
        f"&body={quote(normalized_body)}"
    )
