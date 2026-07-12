"""JSON-file persistence for tasks. No database or route logic."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from app.models import Task, TaskCreate, TaskUpdate

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


def list_tasks() -> list[Task]:
    return [Task.model_validate(item) for item in _load_tasks()]


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


def update_task(task_id: int, payload: TaskUpdate) -> Task | None:
    tasks = _load_tasks()
    for index, item in enumerate(tasks):
        if item.get("id") != task_id:
            continue

        updates = payload.model_dump(exclude_unset=True)
        item.update(updates)
        item["updated_at"] = _utc_now().isoformat()
        tasks[index] = item
        _save_tasks(tasks)
        return Task.model_validate(item)

    return None


def delete_task(task_id: int) -> bool:
    tasks = _load_tasks()
    remaining = [item for item in tasks if item.get("id") != task_id]
    if len(remaining) == len(tasks):
        return False
    _save_tasks(remaining)
    return True
