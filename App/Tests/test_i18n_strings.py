from __future__ import annotations

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from gui.i18n import available_languages, set_language, tr  # noqa: E402


def test_available_languages_include_expected_codes() -> None:
    langs = set(available_languages())
    assert "de" in langs
    assert "en" in langs
    assert "es" in langs
    assert "fr" in langs
    assert "ru" in langs


def test_spanish_translation_is_used_when_selected() -> None:
    set_language("es")
    assert tr("activity.title") == "Actividad"
    assert tr("topbar.mode.prepare") == "Preparar"
    set_language("en")


def test_new_language_translations_are_used_when_selected() -> None:
    set_language("fr")
    assert tr("topbar.file") == "Fichier"

    set_language("de")
    assert tr("topbar.file") == "Datei"

    set_language("ru")
    assert tr("topbar.file") == "Файл"
    set_language("en")


def test_unknown_language_falls_back_to_english() -> None:
    set_language("zz")
    assert tr("topbar.file") == "File"
    set_language("en")
