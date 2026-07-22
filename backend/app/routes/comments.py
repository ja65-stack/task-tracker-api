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
    try:
        return comment_service.add_comment(task_id, payload)
    except TaskNotFoundError as exc:
        raise _not_found(exc) from exc


@router.delete(
    "/tasks/{task_id}/comments/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task_comment(task_id: int, comment_id: int) -> None:
    try:
        comment_service.remove_comment(task_id, comment_id)
    except (TaskNotFoundError, CommentNotFoundError) as exc:
        raise _not_found(exc) from exc
