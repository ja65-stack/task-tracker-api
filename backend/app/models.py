from enum import Enum

from pydantic import BaseModel, Field, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Task(BaseModel):
    id: int
    title: str = Field(...)
    description: str | None = None
    status: TaskStatus
    priority: TaskPriority
    assignee: str | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError(
                "Title is required and cannot be blank"
            )

        return value