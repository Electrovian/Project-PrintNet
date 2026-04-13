import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from gui.Windows.controller.ui import UiMixin, _load_files_view_cache  # noqa: E402
except Exception:
    UiMixin = None
    _load_files_view_cache = None


class _ViewerStub:
    def __init__(self, models=None):
        self.models = {
            int(model_id): dict(payload or {})
            for model_id, payload in dict(models or {}).items()
        }


class _FilesViewStub:
    def __init__(self):
        self._models = []

    def refresh_from_viewer(self, viewer):
        models = []
        for model_id in sorted(dict(getattr(viewer, "models", {}) or {}).keys()):
            payload = dict(viewer.models.get(int(model_id), {}) or {})
            models.append(
                {
                    "id": int(model_id),
                    "name": payload.get("name") or f"Model {model_id}",
                    "path": payload.get("path") or "",
                    "plate": str(payload.get("plate") or ""),
                }
            )
        self.set_models(models)

    def set_models(self, models):
        self._models = [dict(item) for item in list(models or []) if isinstance(item, dict)]

    def models_snapshot(self):
        return [dict(item) for item in self._models]


class _FilesController(UiMixin if UiMixin is not None else object):
    def __init__(self, *, cache_path: Path, models=None):
        self.viewer = _ViewerStub(models)
        self.files_view = _FilesViewStub()
        self._files_view_cache_file = cache_path


@unittest.skipIf(UiMixin is None or _load_files_view_cache is None, "files view controller unavailable")
class FilesViewPersistenceTests(unittest.TestCase):
    def test_files_page_restores_cached_rows_when_viewer_is_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp).joinpath("files_view_cache.json")
            controller = _FilesController(
                cache_path=cache_path,
                models={
                    7: {
                        "name": "gearbox.stl",
                        "path": "C:/tmp/gearbox.stl",
                        "plate": "01",
                    }
                },
            )

            controller._refresh_files_view(prefer_cache=False)
            expected_rows = controller.files_view.models_snapshot()

            controller.viewer = _ViewerStub({})
            controller.files_view = _FilesViewStub()
            controller._refresh_files_view(prefer_cache=True)

            cached = _load_files_view_cache(cache_path)
            self.assertTrue(cached["available"])
            self.assertEqual(cached["models"], expected_rows)
            self.assertEqual(controller.files_view.models_snapshot(), expected_rows)

    def test_explicit_empty_refresh_clears_cached_rows_instead_of_restoring_stale_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache_path = Path(tmp).joinpath("files_view_cache.json")
            controller = _FilesController(
                cache_path=cache_path,
                models={
                    3: {
                        "name": "bracket.stl",
                        "path": "C:/tmp/bracket.stl",
                        "plate": "02",
                    }
                },
            )

            controller._refresh_files_view(prefer_cache=False)
            controller.viewer = _ViewerStub({})
            controller._refresh_files_view(prefer_cache=False)

            cached = _load_files_view_cache(cache_path)
            self.assertTrue(cached["available"])
            self.assertEqual(cached["models"], [])
            self.assertEqual(controller.files_view.models_snapshot(), [])

            controller._refresh_files_view(prefer_cache=True)
            self.assertEqual(controller.files_view.models_snapshot(), [])


if __name__ == "__main__":
    unittest.main()
