from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable

from .errors import BackendOrchestrationError, BackendValidationError
from .models import utc_now_iso


def _as_non_empty_text(value: object, *, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise BackendValidationError(f"{field} is required.")
    return text


def _as_positive_int(value: object, *, field: str, minimum: int = 1, maximum: int = 1000) -> int:
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
        except Exception as exc:  # pragma: no cover - defensive branch
            raise BackendValidationError(f"{field} must be an integer.") from exc
    if parsed < minimum or parsed > maximum:
        raise BackendValidationError(f"{field} must be between {minimum} and {maximum}.")
    return parsed


@dataclass(frozen=True)
class WorkerHeartbeat:
    worker_id: str
    last_seen_utc: str
    ttl_seconds: int

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class WorkerCycleResult:
    worker_id: str
    tick_id: int
    queue_depth_before: int
    queue_depth_after: int
    claimed: int
    completed: int
    processed_job_ids: tuple[str, ...]
    heartbeat_utc: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class InMemoryQueueOrchestrator:
    def __init__(
        self,
        *,
        heartbeat_ttl_seconds: int = 60,
        max_jobs_per_tick: int = 1,
    ):
        self._heartbeat_ttl_seconds = _as_positive_int(
            heartbeat_ttl_seconds,
            field="heartbeat_ttl_seconds",
            minimum=1,
            maximum=86400,
        )
        self._max_jobs_per_tick = _as_positive_int(
            max_jobs_per_tick,
            field="max_jobs_per_tick",
            minimum=1,
            maximum=100,
        )
        self._tick_counter = 0
        self._queue_order: list[str] = []
        self._queued_ids: set[str] = set()
        self._heartbeats: dict[str, WorkerHeartbeat] = {}

    @property
    def max_jobs_per_tick(self) -> int:
        return self._max_jobs_per_tick

    @property
    def heartbeat_ttl_seconds(self) -> int:
        return self._heartbeat_ttl_seconds

    def enqueue(self, job_id: str) -> bool:
        normalized = _as_non_empty_text(job_id, field="job_id")
        if normalized in self._queued_ids:
            return False
        self._queued_ids.add(normalized)
        self._queue_order.append(normalized)
        return True

    def queue_depth(self) -> int:
        return len(self._queued_ids)

    def pending_job_ids(self) -> tuple[str, ...]:
        rows: list[str] = []
        for job_id in self._queue_order:
            if job_id in self._queued_ids:
                rows.append(job_id)
        return tuple(rows)

    def record_heartbeat(self, worker_id: str) -> WorkerHeartbeat:
        normalized = _as_non_empty_text(worker_id, field="worker_id")
        heartbeat = WorkerHeartbeat(
            worker_id=normalized,
            last_seen_utc=utc_now_iso(),
            ttl_seconds=self._heartbeat_ttl_seconds,
        )
        self._heartbeats[normalized] = heartbeat
        return heartbeat

    def list_heartbeats(self) -> tuple[WorkerHeartbeat, ...]:
        rows = list(self._heartbeats.values())
        rows.sort(key=lambda item: item.worker_id.lower())
        return tuple(rows)

    def run_cycle(
        self,
        *,
        worker_id: str,
        max_jobs: object | None,
        process_job: Callable[[str], None],
    ) -> WorkerCycleResult:
        normalized_worker = _as_non_empty_text(worker_id, field="worker_id")
        normalized_max_jobs = self._max_jobs_per_tick
        if max_jobs is not None:
            normalized_max_jobs = _as_positive_int(
                max_jobs,
                field="max_jobs",
                minimum=1,
                maximum=100,
            )

        depth_before = self.queue_depth()
        heartbeat = self.record_heartbeat(normalized_worker)
        self._tick_counter += 1

        processed: list[str] = []
        claimed = 0
        completed = 0

        for _ in range(normalized_max_jobs):
            job_id = self._pop_next_job_id()
            if not job_id:
                break
            claimed += 1
            try:
                process_job(job_id)
            except Exception as exc:
                self.enqueue(job_id)
                raise BackendOrchestrationError(
                    f"QUEUE_WORKER_PROCESS_FAILED: failed while processing {job_id}."
                ) from exc
            processed.append(job_id)
            completed += 1

        return WorkerCycleResult(
            worker_id=normalized_worker,
            tick_id=self._tick_counter,
            queue_depth_before=depth_before,
            queue_depth_after=self.queue_depth(),
            claimed=claimed,
            completed=completed,
            processed_job_ids=tuple(processed),
            heartbeat_utc=heartbeat.last_seen_utc,
        )

    def _pop_next_job_id(self) -> str:
        while self._queue_order:
            job_id = self._queue_order.pop(0)
            if job_id in self._queued_ids:
                self._queued_ids.remove(job_id)
                return job_id
        return ""
