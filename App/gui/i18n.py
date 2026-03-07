from __future__ import annotations

import os
from typing import Mapping

from .locales import LANGUAGES, EN_STRINGS


def _normalize_language(code: object) -> str:
    text = str(code or "").strip().lower()
    if not text:
        return "en"
    if "-" in text:
        text = text.split("-", 1)[0].strip()
    if "_" in text:
        text = text.split("_", 1)[0].strip()
    if text in LANGUAGES:
        return text
    return "en"


_CURRENT_LANGUAGE = _normalize_language(os.environ.get("EON_UI_LANG", "en"))


def set_language(code: object) -> str:
    global _CURRENT_LANGUAGE
    _CURRENT_LANGUAGE = _normalize_language(code)
    return _CURRENT_LANGUAGE


def get_language() -> str:
    return _CURRENT_LANGUAGE


def available_languages() -> tuple[str, ...]:
    return tuple(sorted(LANGUAGES.keys()))


def tr(key: str, default: str = "", **kwargs: object) -> str:
    code = get_language()
    language_map: Mapping[str, str] = LANGUAGES.get(code, EN_STRINGS)
    text = str(language_map.get(key) or EN_STRINGS.get(key) or default or key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception:
            pass
    return text
