from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.business_rules import validate_status_transition
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate
from app.routes.activity import router as activity_router
from app.routes.comments import router as comments_router
from app.services import activity_service


app = FastAPI(
    title="Task Tracker API",
    description=(
        "Task Tracker REST API learning project with task CRUD, "
        "task comments, and an activity log for create/update/"
        "delete/status-change events."
    ),
    version="0.1.0",
)

app.include_router(comments_router)
app.include_router(activity_router)


origins = [
    "http://localhost:8001",
    "http://127.0.0.1:8001",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Return API liveness information.

    Returns:
        dict: Mapping with ``status`` set to ``"ok"`` and a UTC ``timestamp``.

    Example:
        ``GET /health`` → ``{"status": "ok", "timestamp": "..."}``
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
) -> list[TaskResponse]:
    """List tasks, optionally filtered by status and/or priority.

    Args:
        status: Optional task status filter.
        priority: Optional task priority filter.

    Returns:
        list[TaskResponse]: Matching tasks from storage.

    Example:
        ``GET /tasks``
        ``GET /tasks?status=ToDo&priority=High``
    """
    return storage.get_all_tasks(status=status, priority=priority)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Fetch a single task by id.

    Args:
        task_id: Task identifier from the path (parsed as an integer in storage).

    Returns:
        TaskResponse: The matching task.

    Raises:
        HTTPException: 404 if the task does not exist or ``task_id`` is not an int.

    Example:
        ``GET /tasks/1``
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Partially update a task and record activity for successful writes.

    If the body has no set fields, returns the existing task unchanged and does
    not append activity. When ``status`` is present, validates the transition
    before updating. A status change records ``status_changed``; any other
    changed fields record ``updated`` (both may be recorded for one request).

    Args:
        task_id: Task identifier from the path.
        payload: Partial update fields (extra fields forbidden by the model).

    Returns:
        TaskResponse: The task after update, or the unchanged task if empty body.

    Raises:
        HTTPException: 404 if the task is missing; 422 if status transition is
            invalid.

    Example:
        ``PATCH /tasks/1`` with ``{"title": "Renamed"}``
        ``PATCH /tasks/1`` with ``{"status": "InProgress"}``
    """
    existing = storage.get_task_by_id(task_id)
    if existing is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return existing

    # Only validate real status changes. Same-to-same (e.g. InProgress →
    # InProgress) is a no-op so modal edits that resend the current status
    # (title/description-only) do not 422.
    if "status" in updates and updates["status"] != existing.status:
        validate_status_transition(existing.status, updates["status"])

    task = storage.update_task(task_id, payload)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    status_changed = (
        "status" in updates and updates["status"] != existing.status
    )
    other_updates = {key: value for key, value in updates.items() if key != "status"}

    if status_changed:
        activity_service.record_status_changed(
            task.id,
            task.title,
            existing.status,
            task.status,
        )
    if other_updates:
        activity_service.record_updated(task.id, task.title)

    return task


@app.patch("/task/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task_alias(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Alias of ``PATCH /tasks/{task_id}`` that delegates to ``update_task``.

    Args:
        task_id: Task identifier from the path.
        payload: Partial update fields.

    Returns:
        TaskResponse: Result of ``update_task``.

    Raises:
        HTTPException: Same as ``update_task`` (404 / 422).

    Example:
        ``PATCH /task/1`` with ``{"priority": "High"}``
    """
    return update_task(task_id, payload)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    """Delete a task and append a ``deleted`` activity event on success.

    Args:
        task_id: Task identifier from the path.

    Returns:
        None: Empty body with HTTP 204 on success.

    Raises:
        HTTPException: 404 if the task does not exist or delete did not remove a
            row.

    Example:
        ``DELETE /tasks/1``
    """
    existing = storage.get_task_by_id(task_id)
    if existing is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    if not storage.delete_task(task_id):
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    activity_service.record_deleted(existing.id, existing.title)


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a task and append a ``created`` activity event.

    Args:
        payload: New task fields. Title is required (blank titles rejected by the
            model).

    Returns:
        TaskResponse: The persisted task including server-owned id and timestamps.

    Note:
        [VERIFY] Invalid bodies are rejected by FastAPI/Pydantic before this
        handler runs (typically HTTP 422).

    Example:
        ``POST /tasks`` with ``{"title": "New work"}``
    """
    task = storage.add_task(payload)
    activity_service.record_created(task.id, task.title)
    return task
