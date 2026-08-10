import pytest
from fastapi.testclient import TestClient

from app import activity_storage, comment_storage, storage
from app.main import app


@pytest.fixture(autouse=True)
def _reset_storage(tmp_path, monkeypatch):
    tasks_file = tmp_path / "tasks.json"
    comments_file = tmp_path / "comments.json"
    activity_file = tmp_path / "activity.json"
    tasks_file.write_text("[]", encoding="utf-8")
    comments_file.write_text("[]", encoding="utf-8")
    activity_file.write_text("[]", encoding="utf-8")

    monkeypatch.setattr(storage, "DATA_DIR", tmp_path)
    monkeypatch.setattr(storage, "TASKS_FILE", tasks_file)
    monkeypatch.setattr(comment_storage, "DATA_DIR", tmp_path)
    monkeypatch.setattr(comment_storage, "COMMENTS_FILE", comments_file)
    monkeypatch.setattr(activity_storage, "DATA_DIR", tmp_path)
    monkeypatch.setattr(activity_storage, "ACTIVITY_FILE", activity_file)

    storage._reset()
    comment_storage._reset()
    activity_storage._reset()
    yield
    storage._reset()
    comment_storage._reset()
    activity_storage._reset()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def created_task(client):
    response = client.post("/tasks", json={"title": "fixture task"})
    assert response.status_code == 201
    return response.json()
