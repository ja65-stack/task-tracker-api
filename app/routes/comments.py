"""Comment API routes: list, add, and delete comments for a task."""

from fastapi import APIRouter, HTTPException, status

from app.models import CommentCreate, CommentResponse
from app.services import comment_service
from app.services.comment_service import CommentNotFoundError, TaskNotFoundError

router = APIRouter(tags=["comments"])


def _not_found(exc: Exception) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exc),
    )


@router.get(
    "/tasks/{task_id}/comments",
    response_model=list[CommentResponse],
)
def list_task_comments(task_id: int) -> list[CommentResponse]:
    """List comments for a task.

    Args:
        task_id: Parent task id.

    Returns:
        list[CommentResponse]: Comments for that task.

    Raises:
        HTTPException: 404 if the task does not exist.

    Example:
        ``GET /tasks/1/comments``
    """
    try:
        return comment_service.list_comments(task_id)
    except TaskNotFoundError as exc:
        raise _not_found(exc) from exc


@router.post(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_comment(task_id: int, payload: CommentCreate) -> CommentResponse:
    """Add a comment to a task.

    Args:
        task_id: Parent task id.
        payload: Comment body; ``text`` must be non-blank (model-validated).

    Returns:
        CommentResponse: Persisted comment with server-owned id and created_at.

    Raises:
        HTTPException: 404 if the task does not exist.

    Example:
        ``POST /tasks/1/comments`` with ``{"text": "Looks good"}``
    """
    try:
        return comment_service.add_comment(task_id, payload)
    except TaskNotFoundError as exc:
        raise _not_found(exc) from exc


@router.delete(
    "/tasks/{task_id}/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task_comment(task_id: int, comment_id: int) -> None:
    """Delete a comment that belongs to the given task.

    Args:
        task_id: Parent task id.
        comment_id: Comment id to remove.

    Returns:
        None: Empty body with HTTP 204 on success.

    Raises:
        HTTPException: 404 if the task is missing, the comment is missing, or
            the comment exists but is not owned by ``task_id``.

    Example:
        ``DELETE /tasks/1/comments/3``
    """
    try:
        comment_service.remove_comment(task_id, comment_id)
    except (TaskNotFoundError, CommentNotFoundError) as exc:
        raise _not_found(exc) from exc
