import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from printnet_backend.app import create_app  # noqa: E402
from printnet_backend.compat import create_test_client  # noqa: E402
from printnet_backend.qr_assets import generate_qr_assets  # noqa: E402
from printnet_backend.settings import BackendSettings  # noqa: E402


class _SuccessfulSmtpClient:
    last_message = None
    starttls_called = False
    logged_in = None

    def __init__(self, *_args, **_kwargs):
        type(self).last_message = None
        type(self).starttls_called = False
        type(self).logged_in = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def starttls(self):
        type(self).starttls_called = True

    def login(self, username, password):
        type(self).logged_in = (username, password)

    def send_message(self, message):
        type(self).last_message = message


class _FailingSmtpClient(_SuccessfulSmtpClient):
    def send_message(self, message):
        raise RuntimeError("mail transport down")


class AuthEmailDeliveryTests(unittest.TestCase):
    def _client(self, **overrides):
        settings = BackendSettings(
            enable_docs=False,
            super_admin_email="owner@example.com",
            super_admin_password="password-123",
            auth_email_require_smtp=True,
            auth_expose_debug_code=False,
            **overrides,
        )
        return create_test_client(create_app(settings=settings))

    def test_strict_email_delivery_requires_smtp_configuration(self):
        client = self._client()
        response = client.post(
            "/api/v1/auth/login/request-code",
            json={"user_id": "owner@example.com", "password": "password-123"},
        )
        self.assertEqual(response.status_code, 503)
        payload = response.json()
        self.assertEqual(payload["error"]["code"], "BACKEND_ORCHESTRATION_ERROR")
        self.assertIn("AUTH_VERIFICATION_DELIVERY_UNAVAILABLE", payload["error"]["detail"])

    @mock.patch("printnet_backend.services.smtplib.SMTP", new=_SuccessfulSmtpClient)
    def test_strict_email_delivery_uses_smtp_when_configured(self):
        client = self._client(
            smtp_host="smtp.example.com",
            smtp_port=2525,
            smtp_username="smtp-user",
            smtp_password="smtp-pass",
            smtp_starttls=True,
            smtp_use_ssl=False,
        )
        response = client.post(
            "/api/v1/auth/login/request-code",
            json={"user_id": "owner@example.com", "password": "password-123"},
        )
        self.assertEqual(response.status_code, 200)
        challenge = response.json()["challenge"]
        self.assertEqual(challenge["delivery"]["channel"], "smtp")
        self.assertNotIn("debug_code", challenge)
        self.assertTrue(_SuccessfulSmtpClient.starttls_called)
        self.assertEqual(_SuccessfulSmtpClient.logged_in, ("smtp-user", "smtp-pass"))
        self.assertIsNotNone(_SuccessfulSmtpClient.last_message)
        assert _SuccessfulSmtpClient.last_message is not None
        self.assertEqual(_SuccessfulSmtpClient.last_message["To"], "owner@example.com")

    @mock.patch("printnet_backend.services.smtplib.SMTP", new=_FailingSmtpClient)
    def test_strict_email_delivery_fails_clearly_when_smtp_send_breaks(self):
        client = self._client(
            smtp_host="smtp.example.com",
            smtp_port=2525,
            smtp_starttls=False,
        )
        response = client.post(
            "/api/v1/auth/login/request-code",
            json={"user_id": "owner@example.com", "password": "password-123"},
        )
        self.assertEqual(response.status_code, 503)
        payload = response.json()
        self.assertEqual(payload["error"]["code"], "BACKEND_ORCHESTRATION_ERROR")
        self.assertIn("AUTH_VERIFICATION_DELIVERY_FAILED", payload["error"]["detail"])


class QrAssetTests(unittest.TestCase):
    def test_generate_qr_assets_writes_png_and_svg(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            manifest = generate_qr_assets("http://192.168.1.145:8080", temp_dir, stem="lan-share")
            png_path = Path(manifest.png_path)
            svg_path = Path(manifest.svg_path)
            self.assertTrue(png_path.exists())
            self.assertTrue(svg_path.exists())
            self.assertGreater(png_path.stat().st_size, 0)
            self.assertGreater(svg_path.stat().st_size, 0)
            svg_text = svg_path.read_text(encoding="utf-8")
            self.assertIn("<svg", svg_text)
            self.assertEqual(manifest.url, "http://192.168.1.145:8080")


if __name__ == "__main__":
    unittest.main()
