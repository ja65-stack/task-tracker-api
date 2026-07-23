"""Skeleton tests for activity models and JSON storage.

Activity HTTP endpoints are not registered yet.
"""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app import activity_storage
from app.models import ActivityEvent, ActivityEventType, TaskStatus


@pytest.fixture(autouse=True)
def _reset_activity_storage(tmp_path, monkeypatch):
    activity_file = tmp_path / "activity.json"
    activity_file.write_text("[]", encoding="utf-8")
    monkeypatch.setattr(activity_storage, "DATA_DIR", tmp_path)
    monkeypatch.setattr(activity_storage, "ACTIVITY_FILE", activity_file)
    activity_storage._reset()
    yield
    activity_storage._reset()


def test_activity_event_accepts_status_changed_fields():
    event = ActivityEvent(
        id=1,
        task_id=10,
        event_type=ActivityEventType.STATUS_CHANGED,
        summary="status changed",
        from_status=TaskStatus.TODO,
        to_status=TaskStatus.IN_PROGRESS,
        created_at=datetime.now(timezone.utc),
    )
    assert event.event_type == ActivityEventType.STATUS_CHANGED
    assert event.from_status == TaskStatus.TODO
    assert event.to_status == TaskStatus.IN_PROGRESS


def test_activity_event_rejects_invalid_event_type():
    with pytest.raises(ValidationError):
        ActivityEvent(
            id=1,
            task_id=10,
            event_type="renamed",
            summary="bad type",
            created_at=datetime.now(timezone.utc),
        )


def test_append_and_list_events_newest_first():
    first = activity_storage.append_event(
        task_id=1,
        event_type=ActivityEventType.CREATED,
        summary="created",
    )
    second = activity_storage.append_event(
        task_id=1,
        event_type=ActivityEventType.UPDATED,
        summary="updated",
    )

    events = activity_storage.list_events(task_id=1)

    assert [event.id for event in events] == [second.id, first.id]


def test_list_events_can_filter_by_task_id():
    activity_storage.append_event(
        task_id=1,
        event_type=ActivityEventType.CREATED,
        summary="task 1",
    )
    activity_storage.append_event(
        task_id=2,
        event_type=ActivityEventType.CREATED,
        summary="task 2",
    )

    events = activity_storage.list_events(task_id=2)

    assert len(events) == 1
    assert events[0].task_id == 2
