"""Activity API routes will be registered in a later implementation step.

Intended endpoints (not wired yet):
- GET /activity
- GET /tasks/{task_id}/activity
"""

from fastapi import APIRouter

router = APIRouter(tags=["activity"])
