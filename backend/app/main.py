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
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
) -> list[TaskResponse]:
    return storage.get_all_tasks(status=status, priority=priority)


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return task


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    existing = storage.get_task_by_id(task_id)
    if existing is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return existing

    if payload.status is not None:
        validate_status_transition(existing.status, payload.status)

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
    return update_task(task_id, payload)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
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
    task = storage.add_task(payload)
    activity_service.record_created(task.id, task.title)
    return task
