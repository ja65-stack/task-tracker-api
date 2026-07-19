"""Comment API routes will be registered in a later implementation step.

Intended endpoints (not wired yet):
- GET    /tasks/{task_id}/comments
- POST   /tasks/{task_id}/comments
- DELETE /tasks/{task_id}/comments/{comment_id}
"""

from fastapi import APIRouter

router = APIRouter(tags=["comments"])
