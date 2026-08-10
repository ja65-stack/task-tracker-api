"""Comment business helpers used by comment routes."""

from __future__ import annotations

from app import comment_storage, storage
from app.models import Comment, CommentCreate


class CommentServiceError(Exception):
    """Base error for comment service failures."""


class TaskNotFoundError(CommentServiceError):
    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Task with id {task_id} not found")


class CommentNotFoundError(CommentServiceError):
    def __init__(self, comment_id: int) -> None:
        self.comment_id = comment_id
        super().__init__(f"Comment with id {comment_id} not found")


def _require_task(task_id: int) -> None:
    if storage.get_task_by_id(task_id) is None:
        raise TaskNotFoundError(task_id)


def list_comments(task_id: int) -> list[Comment]:
    """List comments for an existing task.

    Args:
        task_id: Parent task id.

    Returns:
        list[Comment]: Comments for that task.

    Raises:
        TaskNotFoundError: If the task does not exist.
    """
    _require_task(task_id)
    return comment_storage.list_comments_for_task(task_id)


def add_comment(task_id: int, payload: CommentCreate) -> Comment:
    """Create a comment after verifying the parent task exists.

    Args:
        task_id: Parent task id.
        payload: Comment create payload.

    Returns:
        Comment: Persisted comment.

    Raises:
        TaskNotFoundError: If the task does not exist.
    """
    _require_task(task_id)
    return comment_storage.create_comment(task_id, payload)


def remove_comment(task_id: int, comment_id: int) -> None:
    """Delete a comment owned by ``task_id``.

    Args:
        task_id: Parent task id.
        comment_id: Comment id to remove.

    Returns:
        None

    Raises:
        TaskNotFoundError: If the task does not exist.
        CommentNotFoundError: If the comment is missing or belongs to another
            task.
    """
    _require_task(task_id)
    comment = comment_storage.get_comment(comment_id)
    if comment is None or comment.task_id != task_id:
        raise CommentNotFoundError(comment_id)
    comment_storage.delete_comment(comment_id)
