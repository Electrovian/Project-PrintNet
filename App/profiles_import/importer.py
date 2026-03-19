from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import ImportFailure, ImportReport, ResolvedProfile


def _normalize_id(payload: dict[str, Any], fallback: str) -> str:
    value = str(payload.get("id", "") or payload.get("name", "")).strip()
    return value or fallback


def _infer_category(path: Path, payload: dict[str, Any]) -> str:
    stem = path.stem.casefold()
    if {"bed_x", "bed_y", "bed_z"} & set(payload.keys()):
        return "machine"
    if {"layer_height", "print_speed", "infill_density"} & set(payload.keys()):
        return "process"
    if {"filament_type", "filament_diameter", "temperature"} & set(payload.keys()):
        return "filament"
    if "machine" in stem:
        return "machine"
    if "process" in stem:
        return "process"
    if "filament" in stem:
        return "filament"
    return "unknown"


def _detect_machine_inheritance_cycles(machines: list[dict[str, Any]]) -> list[ImportFailure]:
    by_id: dict[str, dict[str, Any]] = {}
    for idx, machine in enumerate(machines):
        machine_id = _normalize_id(machine, f"machine-{idx}")
        by_id[machine_id] = machine

    failures: list[ImportFailure] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(machine_id: str):
        if machine_id in visited:
            return
        if machine_id in visiting:
            failures.append(
                ImportFailure(
                    category="inherit_cycle",
                    message=f"Machine inheritance cycle detected at {machine_id}",
                )
            )
            return
        visiting.add(machine_id)
        machine = by_id.get(machine_id)
        parent_id = str((machine or {}).get("inherits", "")).strip()
        if parent_id and parent_id in by_id:
            visit(parent_id)
        visiting.remove(machine_id)
        visited.add(machine_id)

    for machine_id in list(by_id.keys()):
        visit(machine_id)
    return failures


def _collect_nozzles(machines: list[dict[str, Any]]) -> list[str]:
    nozzles: list[str] = []
    seen = set()
    for machine in machines:
        raw_values = machine.get("nozzles", ["0.4"])
        if not isinstance(raw_values, (list, tuple)):
            raw_values = [raw_values]
        for item in raw_values:
            nozzle = str(item).strip()
            if not nozzle:
                continue
            if nozzle in seen:
                continue
            seen.add(nozzle)
            nozzles.append(nozzle)
    return nozzles


def _resolve_profiles(
    machines: list[dict[str, Any]],
    processes: list[dict[str, Any]],
    filaments: list[dict[str, Any]],
) -> list[ResolvedProfile]:
    if not machines:
        return []
    process_pool = processes or [{"id": "process-default"}]
    filament_pool = filaments or [{"id": "filament-default"}]
    resolved: list[ResolvedProfile] = []

    for midx, machine in enumerate(machines):
        machine_id = _normalize_id(machine, f"machine-{midx}")
        raw_nozzles = machine.get("nozzles", ["0.4"])
        if not isinstance(raw_nozzles, (list, tuple)):
            raw_nozzles = [raw_nozzles]
        nozzles = [str(item).strip() for item in raw_nozzles if str(item).strip()] or ["0.4"]

        for nozzle in nozzles:
            for pidx, process in enumerate(process_pool):
                process_id = _normalize_id(process, f"process-{pidx}")
                for fidx, filament in enumerate(filament_pool):
                    filament_id = _normalize_id(filament, f"filament-{fidx}")
                    settings = {
                        "machine": dict(machine),
                        "process": dict(process),
                        "filament": dict(filament),
                        "nozzle": nozzle,
                    }
                    resolved.append(
                        ResolvedProfile(
                            machine_id=machine_id,
                            nozzle=nozzle,
                            process_id=process_id,
                            filament_id=filament_id,
                            settings=settings,
                        )
                    )
    return resolved


def import_profiles(source_path: str, import_version: str = "v1") -> ImportReport:
    _ = import_version
    root = Path(str(source_path)).expanduser()
    failures: list[ImportFailure] = []
    machines: list[dict[str, Any]] = []
    processes: list[dict[str, Any]] = []
    filaments: list[dict[str, Any]] = []

    if not root.exists() or not root.is_dir():
        failures.append(
            ImportFailure(
                category="missing_source",
                message=f"Profile source path does not exist: {root}",
                path=str(root),
            )
        )
        return ImportReport(success=False, failures=failures)

    for path in sorted(root.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(
                ImportFailure(
                    category="invalid_json",
                    message=str(exc),
                    path=str(path),
                )
            )
            continue
        except OSError as exc:
            failures.append(
                ImportFailure(
                    category="read_error",
                    message=str(exc),
                    path=str(path),
                )
            )
            continue

        if not isinstance(payload, dict):
            failures.append(
                ImportFailure(
                    category="invalid_document",
                    message="Profile document must be a JSON object.",
                    path=str(path),
                )
            )
            continue

        category = _infer_category(path, payload)
        if category == "machine":
            machines.append(payload)
        elif category == "process":
            processes.append(payload)
        elif category == "filament":
            filaments.append(payload)

    failures.extend(_detect_machine_inheritance_cycles(machines))
    nozzles = _collect_nozzles(machines)
    resolved_profiles = _resolve_profiles(machines, processes, filaments)

    return ImportReport(
        success=len(failures) == 0,
        machines=machines,
        processes=processes,
        filaments=filaments,
        nozzles=nozzles,
        resolved_profiles=resolved_profiles,
        failures=failures,
    )
