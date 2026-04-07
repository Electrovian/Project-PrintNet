from __future__ import annotations

import argparse
import importlib
import importlib.util
import sys
from dataclasses import dataclass
from typing import Iterable

REQUIRED_MODULES = ("toga", "requests")
OPTIONAL_MODULES = ("briefcase",)


@dataclass(frozen=True)
class ModuleStatus:
    name: str
    required: bool
    available: bool


@dataclass(frozen=True)
class PreflightResult:
    module_statuses: tuple[ModuleStatus, ...]
    import_status: str = "skipped"
    import_detail: str = ""

    @property
    def ok(self) -> bool:
        if self.import_status == "failed":
            return False
        return all(status.available for status in self.module_statuses if status.required)

    @property
    def missing_required(self) -> tuple[str, ...]:
        return tuple(status.name for status in self.module_statuses if status.required and not status.available)

    @property
    def missing_optional(self) -> tuple[str, ...]:
        return tuple(status.name for status in self.module_statuses if not status.required and not status.available)


def _module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def evaluate_preflight(*, require_briefcase: bool = False, import_app: bool = True) -> PreflightResult:
    statuses: list[ModuleStatus] = []
    for module_name in REQUIRED_MODULES:
        statuses.append(ModuleStatus(name=module_name, required=True, available=_module_available(module_name)))
    for module_name in OPTIONAL_MODULES:
        statuses.append(ModuleStatus(name=module_name, required=require_briefcase, available=_module_available(module_name)))

    import_status = "skipped"
    import_detail = ""
    if import_app and not any(status.required and not status.available for status in statuses):
        try:
            module = importlib.import_module("Mobile.app_mobile")
            if not callable(getattr(module, "main", None)):
                import_status = "failed"
                import_detail = "Mobile.app_mobile.main is missing or not callable."
            else:
                import_status = "ok"
        except Exception as exc:  # pragma: no cover - exercised through CLI / failure paths
            import_status = "failed"
            import_detail = str(exc)
    elif import_app:
        import_status = "skipped"
        import_detail = "Skipped because required modules are missing."
    else:
        import_status = "skipped"
        import_detail = "Skipped by request."

    return PreflightResult(
        module_statuses=tuple(statuses),
        import_status=import_status,
        import_detail=import_detail,
    )


def format_report(result: PreflightResult) -> str:
    lines = ["Mobile launch preflight:"]
    for status in result.module_statuses:
        kind = "required" if status.required else "optional"
        state = "ok" if status.available else "missing"
        lines.append(f"- {status.name} ({kind}): {state}")
    if result.import_status == "ok":
        lines.append("- Mobile.app_mobile import: ok")
    elif result.import_status == "failed":
        lines.append(f"- Mobile.app_mobile import: failed ({result.import_detail})")
    else:
        lines.append(f"- Mobile.app_mobile import: skipped ({result.import_detail})")
    if result.missing_required:
        lines.append(f"Missing required modules: {', '.join(result.missing_required)}")
    if result.missing_optional:
        lines.append(f"Missing optional modules: {', '.join(result.missing_optional)}")
    lines.append("Result: PASS" if result.ok else "Result: FAIL")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check mobile launch dependencies and app importability.")
    parser.add_argument(
        "--require-briefcase",
        action="store_true",
        help="Treat briefcase as a required dependency instead of optional.",
    )
    parser.add_argument(
        "--skip-import-check",
        action="store_true",
        help="Only validate package availability and skip importing Mobile.app_mobile.",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    result = evaluate_preflight(
        require_briefcase=bool(args.require_briefcase),
        import_app=not bool(args.skip_import_check),
    )
    print(format_report(result))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
