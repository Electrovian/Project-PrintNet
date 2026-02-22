from __future__ import annotations

import importlib
from types import ModuleType

VENDOR_MODULES = [
  "afinia",
  "anker",
  "anycubic",
  "artillery",
  "bbl",
  "biqu",
  "blacklist",
  "blocks",
  "chuanying",
  "co_print",
  "colido",
  "comgrow",
  "construct3d",
  "creality",
  "cubicon",
  "custom",
  "deltamaker",
  "dremel",
  "elegoo",
  "eonarena",
  "eryone",
  "flashforge",
  "flsun",
  "flyingbear",
  "folgertech",
  "geeetech",
  "ginger_additive",
  "global_profiles_data",
  "infimech",
  "iq",
  "kingroon",
  "lulzbot",
  "m3d",
  "magicmaker",
  "mellow",
  "openeye",
  "orcaarena",
  "orcafilamentlibrary",
  "peopoly",
  "phrozen",
  "positron3d",
  "prusa",
  "qidi",
  "raise3d",
  "ratrig",
  "rh3d",
  "rolohaundesign",
  "seckit",
  "snapmaker",
  "sovol",
  "tiertime",
  "tronxy",
  "twotrees",
  "ultimaker",
  "vivedino",
  "volumic",
  "voron",
  "voxelab",
  "vzbot",
  "wanhao",
  "wanhao_france",
  "wemake3d",
  "wondermaker",
  "z_bolt"
]
_MODULE_CACHE: dict[str, ModuleType] = {}

def load_vendor_module(module_name: str) -> ModuleType:
    key = str(module_name).strip()
    if not key:
        raise ValueError('VENDOR_MODULE_EMPTY')
    if key not in VENDOR_MODULES:
        raise KeyError(f'VENDOR_MODULE_NOT_FOUND:{key}')
    cached = _MODULE_CACHE.get(key)
    if cached is not None:
        return cached
    module = importlib.import_module(f'{__name__}.{key}')
    _MODULE_CACHE[key] = module
    return module

__all__ = [
    "VENDOR_MODULES",
    "load_vendor_module",
]
