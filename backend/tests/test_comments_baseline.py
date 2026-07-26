"""
Baseline check for the Mid-Course-Project comment feature.

Acceptance baseline covered here:
1. List comments for a task (empty + after create)
2. Add comment with server-owned id/task_id/created_at
3. Reject blank / missing comment text (422)
4. Delete comment (204) and confirm removal
5. Missing task/comment returns 404

Run:
  py -m pytest tests/test_comments_baseline.py -q
"""

from pydantic import ValidationError
import pytest

from app.models import CommentCreate


def test_baseline_comment_model_rejects_blank_text():
    with pytest.raises(ValidationError):
        CommentCreate(text="   ")

    with pytest.raises(ValidationError):
        CommentCreate(text="")


def test_baseline_comment_model_strips_text():
    comment = CommentCreate(text="  Needs review  ")
    assert comment.text == "Needs review"


def test_baseline_comment_api_happy_path_list_add_delete(client, created_task):
    task_id = created_task["id"]

    empty = client.get(f"/tasks/{task_id}/comments")
    assert empty.status_code == 200
    assert empty.json() == []

    created = client.post(
        f"/tasks/{task_id}/comments",
        json={"text": "Baseline note"},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["text"] == "Baseline note"
    assert body["task_id"] == task_id
    assert isinstance(body["id"], int)
    assert "created_at" in body
    assert set(body.keys()) >= {"id", "task_id", "text", "created_at"}

    listed = client.get(f"/tasks/{task_id}/comments")
    assert listed.status_code == 200
    comments = listed.json()
    assert len(comments) == 1
    assert comments[0]["id"] == body["id"]

    deleted = client.delete(f"/tasks/{task_id}/comments/{body['id']}")
    assert deleted.status_code == 204

    after_delete = client.get(f"/tasks/{task_id}/comments")
    assert after_delete.status_code == 200
    assert after_delete.json() == []


def test_baseline_comment_api_rejects_blank_text(client, created_task):
    response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "   "},
    )
    assert response.status_code == 422

    listed = client.get(f"/tasks/{created_task['id']}/comments")
    assert listed.status_code == 200
    assert listed.json() == []


def test_baseline_comment_api_rejects_missing_text(client, created_task):
    response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={},
    )
    assert response.status_code == 422


def test_baseline_comment_api_missing_task_returns_404(client):
    assert client.get("/tasks/9999/comments").status_code == 404
    assert (
        client.post("/tasks/9999/comments", json={"text": "orphan"}).status_code
        == 404
    )
    assert client.delete("/tasks/9999/comments/1").status_code == 404


def test_baseline_comment_api_missing_comment_returns_404(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}/comments/9999")
    assert response.status_code == 404


def test_baseline_comment_api_redelete_returns_404(client, created_task):
    created = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "temp"},
    ).json()

    first = client.delete(
        f"/tasks/{created_task['id']}/comments/{created['id']}"
    )
    second = client.delete(
        f"/tasks/{created_task['id']}/comments/{created['id']}"
    )

    assert first.status_code == 204
    assert second.status_code == 404
