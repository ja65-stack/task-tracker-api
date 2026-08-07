"""JSON-file persistence for task comments. No database or route logic."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from app.models import Comment, CommentCreate

DATA_DIR = Path(__file__).resolve().parent / "data"
COMMENTS_FILE = DATA_DIR / "comments.json"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not COMMENTS_FILE.exists():
        COMMENTS_FILE.write_text("[]", encoding="utf-8")


def _load_comments() -> list[dict]:
    _ensure_storage()
    with COMMENTS_FILE.open(encoding="utf-8") as handle:
        return json.load(handle)


def _save_comments(comments: list[dict]) -> None:
    _ensure_storage()
    with COMMENTS_FILE.open("w", encoding="utf-8") as handle:
        json.dump(comments, handle, indent=2, default=str)


def list_comments_for_task(task_id: int) -> list[Comment]:
    """Return comments whose ``task_id`` matches.

    Args:
        task_id: Parent task id.

    Returns:
        list[Comment]: Matching comments in storage file order. [VERIFY] not
        sorted by ``created_at``.
    """
    return [
        Comment.model_validate(item)
        for item in _load_comments()
        if item.get("task_id") == task_id
    ]


def get_comment(comment_id: int) -> Comment | None:
    """Return a comment by id, or None if missing.

    Args:
        comment_id: Comment id to look up.

    Returns:
        Comment | None: Matching comment, or None when not found.
    """
    for item in _load_comments():
        if item.get("id") == comment_id:
            return Comment.model_validate(item)
    return None


def create_comment(task_id: int, payload: CommentCreate) -> Comment:
    """Append a comment with the next id and UTC ``created_at``.

    Args:
        task_id: Parent task id stored on the comment (caller must ensure the
            task exists).
        payload: Comment text.

    Returns:
        Comment: Persisted comment.
    """
    comments = _load_comments()
    next_id = max((item["id"] for item in comments), default=0) + 1
    comment = Comment(
        id=next_id,
        task_id=task_id,
        text=payload.text,
        created_at=_utc_now(),
    )
    comments.append(json.loads(comment.model_dump_json()))
    _save_comments(comments)
    return comment


def delete_comment(comment_id: int) -> bool:
    """Delete a comment by id.

    Args:
        comment_id: Comment id to remove.

    Returns:
        bool: True if removed; False if no matching id.
    """
    comments = _load_comments()
    remaining = [item for item in comments if item.get("id") != comment_id]
    if len(remaining) == len(comments):
        return False
    _save_comments(remaining)
    return True


def _reset() -> None:
    """Clear persisted comments (used by tests)."""
    _ensure_storage()
    COMMENTS_FILE.write_text("[]", encoding="utf-8")
