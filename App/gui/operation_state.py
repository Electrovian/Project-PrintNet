from __future__ import annotations


OPERATION_STATES: tuple[str, ...] = (
    "idle",
    "slicing",
    "uploading",
    "printing",
    "failure",
)

_TRANSITIONS: dict[str, set[str]] = {
    "idle": {"idle", "slicing", "failure"},
    "slicing": {"idle", "uploading", "failure"},
    "uploading": {"idle", "printing", "failure"},
    "printing": {"idle", "failure"},
    "failure": {"idle", "slicing"},
}

_LABELS: dict[str, str] = {
    "idle": "Idle",
    "slicing": "Slicing",
    "uploading": "Uploading",
    "printing": "Printing",
    "failure": "Failure",
}

_DEFAULT_MESSAGES: dict[str, str] = {
    "idle": "Ready.",
    "slicing": "Preparing print data.",
    "uploading": "Uploading to printer.",
    "printing": "Print in progress.",
    "failure": "Operation failed.",
}


def normalize_operation_state(state: str | None) -> str:
    value = str(state or "").strip().lower()
    if value in OPERATION_STATES:
        return value
    return "idle"


def can_transition(current_state: str | None, next_state: str | None) -> bool:
    current = normalize_operation_state(current_state)
    target = normalize_operation_state(next_state)
    return target in _TRANSITIONS.get(current, set())


def operation_state_label(state: str | None) -> str:
    normalized = normalize_operation_state(state)
    return _LABELS.get(normalized, "Idle")


def default_operation_message(state: str | None) -> str:
    normalized = normalize_operation_state(state)
    return _DEFAULT_MESSAGES.get(normalized, _DEFAULT_MESSAGES["idle"])


__all__ = [
    "can_transition",
    "default_operation_message",
    "normalize_operation_state",
    "operation_state_label",
]
