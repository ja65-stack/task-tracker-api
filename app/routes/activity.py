"""Activity API routes: global and per-task activity feeds."""

from fastapi import APIRouter, HTTPException, status

from app.models import ActivityResponse
from app.services import activity_service
from app.services.activity_service import TaskNotFoundError

router = APIRouter(tags=["activity"])


def _not_found(exc: Exception) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


@router.get("/activity", response_model=list[ActivityResponse])
def list_activity() -> list[ActivityResponse]:
    """Return the global activity feed, newest first.

    Returns:
        list[ActivityResponse]: All activity events.

    Example:
        ``GET /activity``
    """
    return activity_service.list_all_activity()


@router.get(
    "/tasks/{task_id}/activity",
    response_model=list[ActivityResponse],
)
def list_activity_for_task(task_id: int) -> list[ActivityResponse]:
    """Return activity events for one task, newest first.

    Args:
        task_id: Task id that must still exist.

    Returns:
        list[ActivityResponse]: Events for that task.

    Raises:
        HTTPException: 404 if the task does not exist (including after delete).

    Example:
        ``GET /tasks/1/activity``
    """
    try:
        return activity_service.list_task_activity(task_id)
    except TaskNotFoundError as exc:
        raise _not_found(exc) from exc
