import pytest
from pydantic import ValidationError

from app.models import TaskCreate, TaskPriority, TaskStatus, TaskUpdate


def test_task_create_strips_title():
    task = TaskCreate(title="  Buy milk  ")
    assert task.title == "Buy milk"


def test_task_create_rejects_blank_title():
    with pytest.raises(ValidationError):
        TaskCreate(title="   ")


def test_task_create_rejects_title_over_200_characters():
    with pytest.raises(ValidationError):
        TaskCreate(title="a" * 201)


def test_task_create_defaults():
    task = TaskCreate(title="Write tests")
    assert task.description is None
    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.MEDIUM
    assert task.assignee is None


def test_task_create_forbids_extra_fields():
    with pytest.raises(ValidationError):
        TaskCreate(title="Valid", unexpected="field")


def test_task_update_validates_title_when_provided():
    task = TaskUpdate(title="  Updated  ")
    assert task.title == "Updated"


def test_task_update_rejects_blank_title_when_provided():
    with pytest.raises(ValidationError):
        TaskUpdate(title="   ")


def test_task_update_allows_omitted_title():
    task = TaskUpdate(status=TaskStatus.DONE)
    assert task.title is None
