"""JSON-file persistence for activity events. No database or route logic."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from app.models import ActivityEvent, ActivityEventType, TaskStatus

DATA_DIR = Path(__file__).resolve().parent / "data"
ACTIVITY_FILE = DATA_DIR / "activity.json"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not ACTIVITY_FILE.exists():
        ACTIVITY_FILE.write_text("[]", encoding="utf-8")


def _load_events() -> list[dict]:
    _ensure_storage()
    with ACTIVITY_FILE.open(encoding="utf-8") as handle:
        return json.load(handle)


def _save_events(events: list[dict]) -> None:
    _ensure_storage()
    with ACTIVITY_FILE.open("w", encoding="utf-8") as handle:
        json.dump(events, handle, indent=2, default=str)


def list_events(task_id: int | None = None) -> list[ActivityEvent]:
    events = [ActivityEvent.model_validate(item) for item in _load_events()]
    if task_id is not None:
        events = [event for event in events if event.task_id == task_id]
    return sorted(events, key=lambda event: event.created_at, reverse=True)


def append_event(
    *,
    task_id: int,
    event_type: ActivityEventType,
    summary: str,
    from_status: TaskStatus | None = None,
    to_status: TaskStatus | None = None,
) -> ActivityEvent:
    events = _load_events()
    next_id = max((item["id"] for item in events), default=0) + 1
    event = ActivityEvent(
        id=next_id,
        task_id=task_id,
        event_type=event_type,
        summary=summary,
        from_status=from_status,
        to_status=to_status,
        created_at=_utc_now(),
    )
    events.append(json.loads(event.model_dump_json()))
    _save_events(events)
    return event


def _reset() -> None:
    """Clear persisted activity events (used by tests)."""
    _ensure_storage()
    ACTIVITY_FILE.write_text("[]", encoding="utf-8")
