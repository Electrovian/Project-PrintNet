from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Any

from .errors import BackendValidationError
from .models import utc_now_iso

_REDACTED = "***REDACTED***"


def _as_non_empty_text(value: object, *, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise BackendValidationError(f"{field} is required.")
    return text


def _as_bounded_int(value: object, *, field: str, minimum: int, maximum: int) -> int:
    if isinstance(value, bool):
        raise BackendValidationError(f"{field} must be an integer.")
    if isinstance(value, int):
        parsed = value
    elif isinstance(value, float):
        parsed = int(round(value))
    else:
        text = str(value or "").strip()
        if not text:
            raise BackendValidationError(f"{field} must be an integer.")
        try:
            parsed = int(round(float(text)))
        except Exception as exc:
            raise BackendValidationError(f"{field} must be an integer.") from exc
    if parsed < minimum or parsed > maximum:
        raise BackendValidationError(f"{field} must be between {minimum} and {maximum}.")
    return parsed


def _as_non_negative_float(value: object, *, field: str) -> float:
    if isinstance(value, bool):
        raise BackendValidationError(f"{field} must be >= 0.")
    if isinstance(value, (int, float)):
        parsed = float(value)
    else:
        text = str(value or "").strip()
        if not text:
            raise BackendValidationError(f"{field} must be >= 0.")
        try:
            parsed = float(text)
        except Exception as exc:
            raise BackendValidationError(f"{field} must be >= 0.") from exc
    if parsed < 0.0:
        raise BackendValidationError(f"{field} must be >= 0.")
    return parsed


def _as_bool(value: object, *, field: str) -> bool:
    if isinstance(value, bool):
        return value
    text = str(value or "").strip().lower()
    if text in ("1", "true", "yes", "on"):
        return True
    if text in ("0", "false", "no", "off"):
        return False
    raise BackendValidationError(f"{field} must be true/false.")


def _is_sensitive_key(name: str) -> bool:
    key = str(name or "").strip().lower()
    if not key:
        return False
    sensitive_markers = (
        "auth",
        "token",
        "secret",
        "password",
        "passwd",
        "api_key",
        "apikey",
        "credential",
        "private_key",
    )
    for marker in sensitive_markers:
        if marker in key:
            return True
    return False


def redact_sensitive_fields(payload: object) -> object:
    if isinstance(payload, Mapping):
        root_map: dict[str, Any] = {}
        root: object = root_map
        stack: list[tuple[str, Any, Any]] = [("map", payload, root_map)]
    elif isinstance(payload, list):
        root_list: list[Any] = []
        root = root_list
        stack = [("list", payload, root_list)]
    else:
        return payload

    while stack:
        kind, source, target = stack.pop()
        if kind == "map":
            items = source.items()
            for raw_key, value in items:
                key = str(raw_key)
                if _is_sensitive_key(key):
                    target[key] = _REDACTED
                    continue
                if isinstance(value, Mapping):
                    child_map: dict[str, Any] = {}
                    target[key] = child_map
                    stack.append(("map", value, child_map))
                    continue
                if isinstance(value, list):
                    child_list: list[Any] = []
                    target[key] = child_list
                    stack.append(("list", value, child_list))
                    continue
                target[key] = value
            continue

        for value in source:
            if isinstance(value, Mapping):
                child_map = {}
                target.append(child_map)
                stack.append(("map", value, child_map))
                continue
            if isinstance(value, list):
                child_list = []
                target.append(child_list)
                stack.append(("list", value, child_list))
                continue
            target.append(value)

    return root


@dataclass
class MetricCounter:
    event: str
    status: str
    count: int
    total_duration_ms: float
    last_duration_ms: float
    last_seen_utc: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AuditRecord:
    created_at_utc: str
    actor: str
    action: str
    resource: str
    outcome: str
    details: object

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ReleaseReadinessCheck:
    name: str
    passed: bool
    detail: str
    updated_at_utc: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ObservabilityState:
    def __init__(
        self,
        *,
        max_audit_records: int = 200,
        max_metric_keys: int = 256,
        required_release_checks: tuple[str, ...] = (),
    ):
        self._max_audit_records = _as_bounded_int(
            max_audit_records,
            field="max_audit_records",
            minimum=10,
            maximum=5000,
        )
        self._max_metric_keys = _as_bounded_int(
            max_metric_keys,
            field="max_metric_keys",
            minimum=10,
            maximum=5000,
        )
        self._required_release_checks = tuple(
            _as_non_empty_text(item, field="required_release_checks")
            for item in required_release_checks
        )
        self._metrics: dict[str, MetricCounter] = {}
        self._audit: list[AuditRecord] = []
        self._release_checks: dict[str, ReleaseReadinessCheck] = {}

        for check_name in self._required_release_checks:
            self._release_checks[check_name] = ReleaseReadinessCheck(
                name=check_name,
                passed=False,
                detail="pending",
                updated_at_utc=utc_now_iso(),
            )

    def record_metric(self, *, event: object, status: object, duration_ms: object | None = None) -> MetricCounter:
        event_name = _as_non_empty_text(event, field="event")
        status_name = _as_non_empty_text(status, field="status").lower()
        duration_value = 0.0
        if duration_ms is not None:
            duration_value = _as_non_negative_float(duration_ms, field="duration_ms")

        key = f"{event_name}|{status_name}"
        now = utc_now_iso()
        current = self._metrics.get(key)
        if current is None:
            if len(self._metrics) >= self._max_metric_keys:
                raise BackendValidationError("metric key limit reached.")
            current = MetricCounter(
                event=event_name,
                status=status_name,
                count=0,
                total_duration_ms=0.0,
                last_duration_ms=0.0,
                last_seen_utc=now,
            )
            self._metrics[key] = current

        current.count += 1
        current.total_duration_ms += duration_value
        current.last_duration_ms = duration_value
        current.last_seen_utc = now
        return current

    def metrics_snapshot(self) -> dict[str, Any]:
        rows = list(self._metrics.values())
        rows.sort(key=lambda item: (item.event, item.status))
        return {
            "metric_count": len(rows),
            "metrics": [item.to_dict() for item in rows],
        }

    def append_audit(
        self,
        *,
        actor: object,
        action: object,
        resource: object,
        outcome: object,
        details: object | None = None,
    ) -> AuditRecord:
        record = AuditRecord(
            created_at_utc=utc_now_iso(),
            actor=_as_non_empty_text(actor, field="actor"),
            action=_as_non_empty_text(action, field="action"),
            resource=_as_non_empty_text(resource, field="resource"),
            outcome=_as_non_empty_text(outcome, field="outcome"),
            details=redact_sensitive_fields(details if details is not None else {}),
        )
        self._audit.append(record)
        while len(self._audit) > self._max_audit_records:
            self._audit.pop(0)
        return record

    def list_audit(self, *, limit: object = 50) -> list[dict[str, Any]]:
        max_limit = self._max_audit_records
        normalized_limit = _as_bounded_int(limit, field="limit", minimum=1, maximum=max_limit)
        rows = self._audit[-normalized_limit:]
        rows = list(reversed(rows))
        return [item.to_dict() for item in rows]

    def set_release_check(self, *, name: object, passed: object, detail: object = "") -> ReleaseReadinessCheck:
        check_name = _as_non_empty_text(name, field="check_name")
        state = _as_bool(passed, field="passed")
        text = str(detail or "").strip()
        check = ReleaseReadinessCheck(
            name=check_name,
            passed=state,
            detail=text,
            updated_at_utc=utc_now_iso(),
        )
        self._release_checks[check_name] = check
        return check

    def release_snapshot(self) -> dict[str, Any]:
        rows = list(self._release_checks.values())
        rows.sort(key=lambda item: item.name.lower())
        row_map = {item.name: item for item in rows}
        missing_required: list[str] = []
        failing_required: list[str] = []
        for check_name in self._required_release_checks:
            check = row_map.get(check_name)
            if check is None:
                missing_required.append(check_name)
                continue
            if not check.passed:
                failing_required.append(check_name)
        ready = len(missing_required) == 0 and len(failing_required) == 0
        return {
            "required_checks": list(self._required_release_checks),
            "missing_required": missing_required,
            "failing_required": failing_required,
            "ready": ready,
            "checks": [item.to_dict() for item in rows],
        }
