import time

from app.models import TaskCreate, TaskPriority, TaskStatus, TaskUpdate
from app import storage


def test_add_task_returns_task_with_id_and_timestamps():
    task = storage.add_task(TaskCreate(title="First task"))

    assert task.id == 1
    assert task.title == "First task"
    assert task.description is None
    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.MEDIUM
    assert task.created_at == task.updated_at


def test_get_all_tasks_returns_all_tasks():
    storage.add_task(TaskCreate(title="One"))
    storage.add_task(TaskCreate(title="Two"))

    tasks = storage.get_all_tasks()

    assert len(tasks) == 2


def test_get_all_tasks_filters_by_status():
    storage.add_task(TaskCreate(title="Todo task", status=TaskStatus.TODO))
    storage.add_task(TaskCreate(title="Done task", status=TaskStatus.DONE))

    tasks = storage.get_all_tasks(status=TaskStatus.DONE)

    assert len(tasks) == 1
    assert tasks[0].title == "Done task"


def test_get_all_tasks_filters_by_priority():
    storage.add_task(TaskCreate(title="Low", priority=TaskPriority.LOW))
    storage.add_task(TaskCreate(title="High", priority=TaskPriority.HIGH))

    tasks = storage.get_all_tasks(priority=TaskPriority.HIGH)

    assert len(tasks) == 1
    assert tasks[0].title == "High"


def test_get_task_by_id():
    created = storage.add_task(TaskCreate(title="Lookup me"))

    found = storage.get_task_by_id(created.id)

    assert found == created


def test_get_task_by_id_returns_none_when_missing():
    assert storage.get_task_by_id("missing-id") is None


def test_update_task_applies_partial_changes():
    created = storage.add_task(TaskCreate(title="Original"))

    updated = storage.update_task(
        created.id,
        TaskUpdate(title="Updated", status=TaskStatus.IN_PROGRESS),
    )

    assert updated is not None
    assert updated.title == "Updated"
    assert updated.status == TaskStatus.IN_PROGRESS


def test_update_task_updates_updated_at():
    created = storage.add_task(TaskCreate(title="Timestamp test"))
    time.sleep(0.01)

    updated = storage.update_task(created.id, TaskUpdate(title="Changed"))

    assert updated is not None
    assert updated.updated_at > created.updated_at


def test_update_task_with_no_changes_returns_existing_task():
    created = storage.add_task(TaskCreate(title="No change"))

    updated = storage.update_task(created.id, TaskUpdate())

    assert updated == created


def test_update_task_returns_none_when_missing():
    result = storage.update_task("missing-id", TaskUpdate(title="Nope"))

    assert result is None


def test_delete_task():
    created = storage.add_task(TaskCreate(title="Delete me"))

    deleted = storage.delete_task(created.id)

    assert deleted is True
    assert storage.get_task_by_id(created.id) is None


def test_delete_task_returns_false_when_missing():
    assert storage.delete_task("missing-id") is False
