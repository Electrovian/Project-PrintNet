from .en import STRINGS as EN_STRINGS
from .es import STRINGS as ES_STRINGS
from .fr import STRINGS as FR_STRINGS
from .de import STRINGS as DE_STRINGS
from .ru import STRINGS as RU_STRINGS

LANGUAGES = {
    "de": DE_STRINGS,
    "en": EN_STRINGS,
    "es": ES_STRINGS,
    "fr": FR_STRINGS,
    "ru": RU_STRINGS,
}

__all__ = [
    "LANGUAGES",
    "EN_STRINGS",
    "ES_STRINGS",
    "FR_STRINGS",
    "DE_STRINGS",
    "RU_STRINGS",
]
