from .discovery import (
    ProfileDiscoveryError,
    PrinterProfileDiscoveryReport,
    VendorProfileDiscovery,
    discover_printer_profile_files,
)
from .inheritance import (
    ProfileInheritanceError,
    ProfileInheritanceReport,
    ResolvedProfileDocument,
    discover_and_resolve_profile_inheritance,
    resolve_profile_inheritance,
)
from .mapping import (
    MappedProfileSettings,
    ProfileMappingError,
    ProfileSettingsMappingReport,
    discover_resolve_and_map_profiles,
    map_resolved_profiles_to_settings,
)
from .storage import (
    ProfileStorageError,
    ProfileStorageIndex,
    ProfileStorageRecord,
    build_profile_storage_index,
    discover_resolve_map_build_and_persist_profile_storage_index,
    load_profile_storage_index,
    persist_profile_storage_index,
    query_profile_storage_index,
)
from .parsing import (
    ProfileParsingError,
    VendorIndexEntry,
    VendorIndexParseResult,
    VendorProfileParseReport,
    VendorProfileParseResult,
    discover_and_parse_vendor_profiles,
    parse_vendor_index_file,
    parse_vendor_profile_files,
)
from .json_catalog import (
    JsonConfigCatalogError,
    JsonConfigCatalogReport,
    discover_json_config_catalog,
)

try:
    from .importer import import_profiles  # type: ignore
except Exception:  # pragma: no cover - optional during staged migration
    import_profiles = None  # type: ignore

try:
    from .models import ImportReport, ResolvedProfile  # type: ignore
except Exception:  # pragma: no cover - optional during staged migration
    ImportReport = None  # type: ignore
    ResolvedProfile = None  # type: ignore

__all__ = [
    "ProfileDiscoveryError",
    "PrinterProfileDiscoveryReport",
    "VendorProfileDiscovery",
    "discover_printer_profile_files",
    "ProfileParsingError",
    "VendorIndexEntry",
    "VendorIndexParseResult",
    "VendorProfileParseReport",
    "VendorProfileParseResult",
    "discover_and_parse_vendor_profiles",
    "parse_vendor_index_file",
    "parse_vendor_profile_files",
    "JsonConfigCatalogError",
    "JsonConfigCatalogReport",
    "discover_json_config_catalog",
    "ProfileInheritanceError",
    "ProfileInheritanceReport",
    "ResolvedProfileDocument",
    "discover_and_resolve_profile_inheritance",
    "resolve_profile_inheritance",
    "MappedProfileSettings",
    "ProfileMappingError",
    "ProfileSettingsMappingReport",
    "discover_resolve_and_map_profiles",
    "map_resolved_profiles_to_settings",
    "ProfileStorageError",
    "ProfileStorageIndex",
    "ProfileStorageRecord",
    "build_profile_storage_index",
    "discover_resolve_map_build_and_persist_profile_storage_index",
    "load_profile_storage_index",
    "persist_profile_storage_index",
    "query_profile_storage_index",
    "ImportReport",
    "ResolvedProfile",
    "import_profiles",
]
