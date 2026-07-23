"""Activity helpers used by activity routes and task write hooks."""

from __future__ import annotations

from app import activity_storage, storage
from app.models import ActivityEvent, ActivityEventType, TaskStatus


class ActivityServiceError(Exception):
    """Base error for activity service failures."""


class TaskNotFoundError(ActivityServiceError):
    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Task with id {task_id} not found")


def _require_task(task_id: int) -> None:
    if storage.get_task_by_id(task_id) is None:
        raise TaskNotFoundError(task_id)


def list_all_activity() -> list[ActivityEvent]:
    return activity_storage.list_events()


def list_task_activity(task_id: int) -> list[ActivityEvent]:
    _require_task(task_id)
    return activity_storage.list_events(task_id=task_id)


def record_created(task_id: int, title: str) -> ActivityEvent:
    return activity_storage.append_event(
        task_id=task_id,
        event_type=ActivityEventType.CREATED,
        summary=f'Task created: "{title}"',
    )


def record_updated(task_id: int, title: str) -> ActivityEvent:
    return activity_storage.append_event(
        task_id=task_id,
        event_type=ActivityEventType.UPDATED,
        summary=f'Task updated: "{title}"',
    )


def record_deleted(task_id: int, title: str) -> ActivityEvent:
    return activity_storage.append_event(
        task_id=task_id,
        event_type=ActivityEventType.DELETED,
        summary=f'Task deleted: "{title}"',
    )


def record_status_changed(
    task_id: int,
    title: str,
    from_status: TaskStatus,
    to_status: TaskStatus,
) -> ActivityEvent:
    return activity_storage.append_event(
        task_id=task_id,
        event_type=ActivityEventType.STATUS_CHANGED,
        summary=(
            f'Task "{title}" status changed from '
            f"{from_status.value} to {to_status.value}"
        ),
        from_status=from_status,
        to_status=to_status,
    )
