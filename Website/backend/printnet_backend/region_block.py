from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable, Mapping, Sequence


DEFAULT_STATE_HEADER_KEYS: tuple[str, ...] = (
    "x-us-state",
    "x-state",
    "x-geo-state",
    "x-region-code",
    "x-geo-region",
    "x-geo-region-code",
    "cloudfront-viewer-country-region",
    "x-vercel-ip-country-region",
)

_US_REGION_RE = re.compile(r"\bUS[-_]?([A-Z]{2})\b")


@dataclass(frozen=True)
class RegionComplianceDecision:
    allowed: bool
    reason_code: str
    detail: str
    state_code: str
    unknown_policy: str
    blocked_state_codes: tuple[str, ...]


def normalize_state_code(value: object) -> str:
    text = str(value or "").strip().upper()
    if not text:
        return ""
    if "," in text:
        text = text.split(",", 1)[0].strip()
    match = _US_REGION_RE.search(text)
    if match:
        return match.group(1)
    if text.startswith("US-") and len(text) >= 5:
        text = text[3:].strip()
    if len(text) == 2 and text.isalpha():
        return text
    return ""


def normalize_unknown_policy(value: object, *, default: str = "deny") -> str:
    text = str(value or "").strip().lower()
    if text in ("allow", "permit", "true", "1", "yes", "on"):
        return "allow"
    if text in ("deny", "block", "false", "0", "no", "off"):
        return "deny"
    fallback = str(default or "").strip().lower()
    if fallback in ("allow", "deny"):
        return fallback
    return "deny"


def _normalize_header_keys(header_keys: Sequence[str] | None) -> tuple[str, ...]:
    source = list(header_keys or DEFAULT_STATE_HEADER_KEYS)
    normalized: list[str] = []
    seen: set[str] = set()
    for item in source:
        key = str(item or "").strip().lower()
        if not key:
            continue
        if key in seen:
            continue
        seen.add(key)
        normalized.append(key)
    if not normalized:
        return DEFAULT_STATE_HEADER_KEYS
    return tuple(normalized)


def _header_lookup(headers: Mapping[str, object]) -> dict[str, object]:
    lookup: dict[str, object] = {}
    try:
        items = headers.items()
    except Exception:
        return lookup
    for key, value in items:
        name = str(key or "").strip().lower()
        if not name:
            continue
        lookup[name] = value
    return lookup


def read_request_state_code(
    headers: Mapping[str, object],
    *,
    trusted_header_keys: Sequence[str] | None = None,
) -> str:
    normalized_header_keys = _normalize_header_keys(trusted_header_keys)
    lookup = _header_lookup(headers)
    for key in normalized_header_keys:
        raw = headers.get(key)
        if raw is None:
            raw = lookup.get(key)
        if raw is None:
            continue
        normalized = normalize_state_code(raw)
        if normalized:
            return normalized
    return ""


def _normalize_state_codes(values: Iterable[object]) -> tuple[str, ...]:
    normalized: list[str] = []
    seen: set[str] = set()
    for item in values:
        code = normalize_state_code(item)
        if not code or code in seen:
            continue
        seen.add(code)
        normalized.append(code)
    return tuple(normalized)


def evaluate_region_compliance(
    *,
    headers: Mapping[str, object],
    region_block_enabled: bool,
    blocked_state_codes: Sequence[object],
    unknown_policy: str,
    trusted_header_keys: Sequence[str] | None = None,
) -> RegionComplianceDecision:
    normalized_blocked = _normalize_state_codes(blocked_state_codes)
    policy = normalize_unknown_policy(unknown_policy)

    if not bool(region_block_enabled):
        return RegionComplianceDecision(
            allowed=True,
            reason_code="REGION_BLOCK_DISABLED",
            detail="Region blocking is disabled.",
            state_code="",
            unknown_policy=policy,
            blocked_state_codes=normalized_blocked,
        )

    state_code = read_request_state_code(headers, trusted_header_keys=trusted_header_keys)
    if state_code and state_code in set(normalized_blocked):
        return RegionComplianceDecision(
            allowed=False,
            reason_code="REGION_BLOCKED",
            detail=f"REGION_BLOCKED: access from US-{state_code} is not available.",
            state_code=state_code,
            unknown_policy=policy,
            blocked_state_codes=normalized_blocked,
        )
    if not state_code:
        if policy == "deny":
            return RegionComplianceDecision(
                allowed=False,
                reason_code="REGION_GEO_UNDETERMINED",
                detail="REGION_GEO_UNDETERMINED: unable to determine requester region.",
                state_code="",
                unknown_policy=policy,
                blocked_state_codes=normalized_blocked,
            )
        return RegionComplianceDecision(
            allowed=True,
            reason_code="REGION_GEO_UNDETERMINED",
            detail="REGION_GEO_UNDETERMINED: requester region is unknown; request allowed by policy.",
            state_code="",
            unknown_policy=policy,
            blocked_state_codes=normalized_blocked,
        )

    return RegionComplianceDecision(
        allowed=True,
        reason_code="REGION_ALLOWED",
        detail=f"REGION_ALLOWED: access allowed for US-{state_code}.",
        state_code=state_code,
        unknown_policy=policy,
        blocked_state_codes=normalized_blocked,
    )
