import os
import sys
import unittest
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from integrations.email_delivery import (  # noqa: E402
    EmailConfigurationError,
    build_mailto_url,
    send_email_via_smtp,
)


class _DummySmtpClient:
    sent_messages = []
    starttls_called = False
    login_args = None

    def __init__(self, *_args, **_kwargs):
        type(self).sent_messages = []
        type(self).starttls_called = False
        type(self).login_args = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def starttls(self):
        type(self).starttls_called = True

    def login(self, username, password):
        type(self).login_args = (username, password)

    def send_message(self, message):
        type(self).sent_messages.append(message)


class EmailDeliveryUtilityTests(unittest.TestCase):
    def test_build_mailto_url_encodes_subject_and_body(self):
        url = build_mailto_url(
            recipient="demo@example.com",
            subject="Print job handoff: cube -> Alpha",
            body="Line 1\nLine 2",
        )
        self.assertIn("mailto:demo%40example.com", url)
        self.assertIn("subject=Print%20job%20handoff%3A%20cube%20-%3E%20Alpha", url)
        self.assertIn("body=Line%201%0ALine%202", url)

    def test_send_email_requires_smtp_host(self):
        with self.assertRaises(EmailConfigurationError):
            send_email_via_smtp(
                recipient="demo@example.com",
                subject="Test",
                body="Body",
                env={},
            )

    @mock.patch("integrations.email_delivery.smtplib.SMTP", new=_DummySmtpClient)
    def test_send_email_uses_starttls_and_login_when_configured(self):
        env = {
            "BACKEND_SMTP_HOST": "smtp.example.com",
            "BACKEND_SMTP_PORT": "2525",
            "BACKEND_SMTP_USERNAME": "smtp-user",
            "BACKEND_SMTP_PASSWORD": "smtp-pass",
            "BACKEND_SMTP_STARTTLS": "1",
            "BACKEND_SMTP_USE_SSL": "0",
            "BACKEND_AUTH_EMAIL_FROM": "no-reply@example.com",
        }
        result = send_email_via_smtp(
            recipient="demo@example.com",
            subject="Queued job",
            body="Body",
            env=env,
        )
        self.assertEqual(result["sender"], "no-reply@example.com")
        self.assertTrue(_DummySmtpClient.starttls_called)
        self.assertEqual(_DummySmtpClient.login_args, ("smtp-user", "smtp-pass"))
        self.assertEqual(len(_DummySmtpClient.sent_messages), 1)


if __name__ == "__main__":
    unittest.main()
