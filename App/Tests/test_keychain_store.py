from __future__ import annotations

import os
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from security.keychain_store import KeychainStore  # noqa: E402


class KeychainStoreTests(unittest.TestCase):
    def test_memory_fallback_round_trip(self):
        store = KeychainStore(service_name="test-eon")
        store._memory_fallback.clear()  # noqa: SLF001
        store.set_secret("printer:token", "abc123")
        self.assertEqual(store.get_secret("printer:token"), "abc123")
        store.delete_secret("printer:token")
        self.assertEqual(store.get_secret("printer:token"), "")

    def test_set_secret_requires_account(self):
        store = KeychainStore(service_name="test-eon")
        with self.assertRaises(ValueError):
            store.set_secret("", "x")


if __name__ == "__main__":
    unittest.main()
