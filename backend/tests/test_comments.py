def test_list_comments_empty_returns_200_and_empty_list(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}/comments")

    assert response.status_code == 200
    assert response.json() == []


def test_add_comment_returns_201_with_server_fields(client, created_task):
    response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "Needs review"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["text"] == "Needs review"
    assert body["task_id"] == created_task["id"]
    assert "id" in body
    assert "created_at" in body


def test_add_comment_appears_in_list(client, created_task):
    created = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "First note"},
    ).json()

    response = client.get(f"/tasks/{created_task['id']}/comments")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["id"] == created["id"]
    assert body[0]["text"] == "First note"


def test_add_comment_blank_text_returns_422(client, created_task):
    response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "   "},
    )

    assert response.status_code == 422


def test_add_comment_missing_text_returns_422(client, created_task):
    response = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={},
    )

    assert response.status_code == 422


def test_list_comments_missing_task_returns_404(client):
    response = client.get("/tasks/9999/comments")

    assert response.status_code == 404


def test_add_comment_missing_task_returns_404(client):
    response = client.post(
        "/tasks/9999/comments",
        json={"text": "orphan note"},
    )

    assert response.status_code == 404


def test_delete_comment_returns_204_and_removes_from_list(client, created_task):
    created = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "Delete me"},
    ).json()

    delete_response = client.delete(
        f"/tasks/{created_task['id']}/comments/{created['id']}"
    )
    assert delete_response.status_code == 204

    list_response = client.get(f"/tasks/{created_task['id']}/comments")
    assert list_response.status_code == 200
    assert list_response.json() == []


def test_delete_comment_missing_comment_returns_404(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}/comments/9999")

    assert response.status_code == 404


def test_delete_comment_missing_task_returns_404(client):
    response = client.delete("/tasks/9999/comments/1")

    assert response.status_code == 404


def test_delete_comment_twice_returns_404(client, created_task):
    created = client.post(
        f"/tasks/{created_task['id']}/comments",
        json={"text": "Once"},
    ).json()

    first = client.delete(
        f"/tasks/{created_task['id']}/comments/{created['id']}"
    )
    second = client.delete(
        f"/tasks/{created_task['id']}/comments/{created['id']}"
    )

    assert first.status_code == 204
    assert second.status_code == 404
