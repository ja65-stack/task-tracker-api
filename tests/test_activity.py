"""Activity model, storage, and API tests."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app import activity_storage
from app.models import ActivityEvent, ActivityEventType, TaskStatus


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


def test_get_activity_empty_returns_200_and_empty_list(client):
    response = client.get("/activity")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task_appends_created_activity_event(client):
    created = client.post("/tasks", json={"title": "New work"}).json()

    response = client.get("/activity")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    event = body[0]
    assert event["event_type"] == "created"
    assert event["task_id"] == created["id"]
    assert set(event.keys()) >= {
        "id",
        "task_id",
        "event_type",
        "summary",
        "created_at",
    }


def test_patch_title_appends_updated_activity_for_task(client, created_task):
    task_id = created_task["id"]
    other = client.post("/tasks", json={"title": "Other task"}).json()

    response = client.patch(f"/tasks/{task_id}", json={"title": "Renamed"})
    assert response.status_code == 200

    task_activity = client.get(f"/tasks/{task_id}/activity")
    assert task_activity.status_code == 200
    body = task_activity.json()
    assert all(item["task_id"] == task_id for item in body)
    assert any(item["event_type"] == "updated" for item in body)
    assert all(item["task_id"] != other["id"] for item in body)


def test_valid_status_transition_appends_status_changed_event(client, created_task):
    task_id = created_task["id"]
    before = client.get(f"/tasks/{task_id}/activity").json()

    response = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})
    assert response.status_code == 200

    after = client.get(f"/tasks/{task_id}/activity").json()
    new_events = after[: len(after) - len(before)]
    status_events = [
        event
        for event in new_events
        if event["event_type"] == "status_changed"
    ]
    assert len(status_events) == 1
    assert status_events[0]["from_status"] == "ToDo"
    assert status_events[0]["to_status"] == "InProgress"


def test_invalid_status_transition_does_not_append_activity(client, created_task):
    task_id = created_task["id"]
    before = client.get("/activity").json()

    response = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    assert response.status_code == 422

    after = client.get("/activity").json()
    assert len(after) == len(before)


def test_get_task_activity_missing_task_returns_404(client):
    response = client.get("/tasks/9999/activity")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_task_activity_returns_created_event_newest_first(client, created_task):
    """GET /tasks/{id}/activity returns that task's events, newest first."""
    task_id = created_task["id"]

    response = client.patch(f"/tasks/{task_id}", json={"title": "Renamed for activity"})
    assert response.status_code == 200

    task_activity = client.get(f"/tasks/{task_id}/activity")
    assert task_activity.status_code == 200
    body = task_activity.json()

    assert len(body) >= 2
    assert all(event["task_id"] == task_id for event in body)
    assert body[0]["event_type"] == "updated"
    assert any(event["event_type"] == "created" for event in body)
    created_at_values = [event["created_at"] for event in body]
    assert created_at_values == sorted(created_at_values, reverse=True)


def test_get_task_activity_after_delete_returns_404(client, created_task):
    """After delete, per-task activity is gone; deleted event stays on GET /activity."""
    task_id = created_task["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    task_activity = client.get(f"/tasks/{task_id}/activity")
    assert task_activity.status_code == 404
    assert "not found" in task_activity.json()["detail"].lower()

    global_activity = client.get("/activity").json()
    assert any(
        event["event_type"] == "deleted" and event["task_id"] == task_id
        for event in global_activity
    )


def test_delete_task_appends_deleted_activity_event(client, created_task):
    task_id = created_task["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    activity = client.get("/activity").json()
    assert any(
        event["event_type"] == "deleted" and event["task_id"] == task_id
        for event in activity
    )


def test_delete_missing_task_does_not_append_activity(client):
    before = client.get("/activity").json()

    response = client.delete("/tasks/9999")
    assert response.status_code == 404

    after = client.get("/activity").json()
    assert len(after) == len(before)
