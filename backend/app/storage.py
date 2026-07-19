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
    tasks = [Task.model_validate(item) for item in _load_tasks()]

    if status is not None:
        tasks = [task for task in tasks if task.status == status]

    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]

    return tasks


def get_task(task_id: int) -> Task | None:
    for item in _load_tasks():
        if item.get("id") == task_id:
            return Task.model_validate(item)
    return None


def create_task(payload: TaskCreate) -> Task:
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
    return create_task(payload)


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[Task]:
    return list_tasks(status=status, priority=priority)


def get_task_by_id(task_id: int | str) -> Task | None:
    parsed_id = _as_int_id(task_id)
    if parsed_id is None:
        return None
    return get_task(parsed_id)


def _reset() -> None:
    """Clear persisted tasks (used by tests)."""
    _ensure_storage()
    TASKS_FILE.write_text("[]", encoding="utf-8")
