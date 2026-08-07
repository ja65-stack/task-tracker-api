"""JSON-file persistence for tasks. No database or route logic."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from app.models import Task, TaskCreate, TaskPriority, TaskStatus, TaskUpdate

DATA_DIR = Path(__file__).resolve().parent / "data"
TASKS_FILE = DATA_DIR / "tasks.json"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("[]", encoding="utf-8")


def _load_tasks() -> list[dict]:
    _ensure_storage()
    with TASKS_FILE.open(encoding="utf-8") as handle:
        return json.load(handle)


def _save_tasks(tasks: list[dict]) -> None:
    _ensure_storage()
    with TASKS_FILE.open("w", encoding="utf-8") as handle:
        json.dump(tasks, handle, indent=2, default=str)


def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[Task]:
    """Load tasks from ``tasks.json``, optionally filtered.

    Args:
        status: If set, keep only tasks with this status.
        priority: If set, keep only tasks with this priority.

    Returns:
        list[Task]: Matching tasks in storage file order. [VERIFY] not sorted.
    """
    tasks = [Task.model_validate(item) for item in _load_tasks()]

    if status is not None:
        tasks = [task for task in tasks if task.status == status]

    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]

    return tasks


def get_task(task_id: int) -> Task | None:
    """Return a task by integer id, or None if missing.

    Args:
        task_id: Task id to look up.

    Returns:
        Task | None: Matching task, or None when not found.
    """
    for item in _load_tasks():
        if item.get("id") == task_id:
            return Task.model_validate(item)
    return None


def create_task(payload: TaskCreate) -> Task:
    """Persist a new task with the next id and UTC timestamps.

    Args:
        payload: Client-provided task fields.

    Returns:
        Task: Newly stored task.
    """
    tasks = _load_tasks()
    next_id = max((item["id"] for item in tasks), default=0) + 1
    now = _utc_now()
    task = Task(
        id=next_id,
        created_at=now,
        updated_at=now,
        **payload.model_dump(),
    )
    tasks.append(json.loads(task.model_dump_json()))
    _save_tasks(tasks)
    return task


def _as_int_id(task_id: int | str) -> int | None:
    try:
        return int(task_id)
    except (TypeError, ValueError):
        return None


def update_task(task_id: int | str, payload: TaskUpdate) -> Task | None:
    """Apply set fields from ``payload`` to a task and bump ``updated_at``.

    Args:
        task_id: Task id (non-integer values yield None).
        payload: Partial update; unset fields are left unchanged.

    Returns:
        Task | None: Updated task, existing task if no fields set, or None if
        missing / invalid id.
    """
    parsed_id = _as_int_id(task_id)
    if parsed_id is None:
        return None

    tasks = _load_tasks()
    for index, item in enumerate(tasks):
        if item.get("id") != parsed_id:
            continue

        updates = payload.model_dump(exclude_unset=True)
        if not updates:
            return Task.model_validate(item)

        item.update(updates)
        item["updated_at"] = _utc_now().isoformat()
        tasks[index] = item
        _save_tasks(tasks)
        return Task.model_validate(item)

    return None


def delete_task(task_id: int | str) -> bool:
    """Remove a task by id.

    Args:
        task_id: Task id (non-integer values yield False).

    Returns:
        bool: True if a row was removed; False if missing or id not an int.
    """
    parsed_id = _as_int_id(task_id)
    if parsed_id is None:
        return False

    tasks = _load_tasks()
    remaining = [item for item in tasks if item.get("id") != parsed_id]
    if len(remaining) == len(tasks):
        return False
    _save_tasks(remaining)
    return True


# Compatibility aliases used by existing routes/tests
def add_task(payload: TaskCreate) -> Task:
    """Compatibility alias for ``create_task``.

    Args:
        payload: Client-provided task fields.

    Returns:
        Task: Newly stored task.
    """
    return create_task(payload)


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[Task]:
    """Compatibility alias for ``list_tasks``.

    Args:
        status: Optional status filter.
        priority: Optional priority filter.

    Returns:
        list[Task]: Matching tasks.
    """
    return list_tasks(status=status, priority=priority)


def get_task_by_id(task_id: int | str) -> Task | None:
    """Resolve ``task_id`` to int and return ``get_task``.

    Args:
        task_id: Task id as int or digit string.

    Returns:
        Task | None: Matching task, or None if invalid/missing.
    """
    parsed_id = _as_int_id(task_id)
    if parsed_id is None:
        return None
    return get_task(parsed_id)


def _reset() -> None:
    """Clear persisted tasks (used by tests)."""
    _ensure_storage()
    TASKS_FILE.write_text("[]", encoding="utf-8")
