# Task Tracker — Architecture (Strategy A)

Branch context: `cursor/restore-pydantic-models-e2a8` (tasks-only snapshot inspected).

## 1. What the app does

Task Tracker is a small learning FastAPI API plus a vanilla HTML/JS Kanban UI. Users create, list, update, and delete tasks with status (`ToDo` / `InProgress` / `Done`), priority, optional description and assignee. Data is stored in a local JSON file—not a database. There is no authentication.

## 2. Data model

**Task** (only persisted entity observed)

| Field | Notes |
|-------|--------|
| `id` | Server int, auto-increment |
| `title` | Required; strip; max 200; blank rejected |
| `description` | Optional string |
| `status` | `ToDo` \| `InProgress` \| `Done` (default `ToDo` on create) |
| `priority` | `Low` \| `Medium` \| `High` (default `Medium`) |
| `assignee` | Optional string |
| `created_at` / `updated_at` | Server UTC datetimes |

Write DTOs: `TaskCreate`, `TaskUpdate` (`extra="forbid"`). Response alias: `TaskResponse = Task`.

## 3. Request flow — create task

1. Frontend (`index.html`) `POST`s JSON to `http://localhost:8000/tasks` (New Task modal).
2. FastAPI validates body as `TaskCreate` (Pydantic); invalid → `422`.
3. `main.create_task` calls `storage.add_task` / `create_task`.
4. Storage loads `app/data/tasks.json`, assigns next `id`, sets timestamps, appends, saves.
5. API returns `201` with full `Task` JSON; UI refreshes the board via `GET /tasks`.

## 4. Key files

| File | Role |
|------|------|
| `app/main.py` | FastAPI app, CORS, all live HTTP routes |
| `app/models.py` | Pydantic Task models + title validation |
| `app/storage.py` | JSON load/save CRUD for tasks |
| `app/business_rules.py` | Allowed status transitions on PATCH |
| `app/data/tasks.json` | On-disk task list |
| `frontend/index.html` | Kanban UI + modal + `fetch` client |
| `tests/conftest.py` | Temp `tasks.json` + TestClient fixtures |
| `tests/test_tasks.py` | API contract tests |
| `README.md` | Run instructions (`uvicorn` from `./` (repo root)) |

## 5. Conventions

- **Validation:** Pydantic on create/update; title strip/blank/length; unknown fields forbidden.
- **Status rules:** PATCH with new status must be a valid transition (`ToDo→InProgress→Done`, `Done→InProgress`); else `422` from `business_rules`.
- **Storage:** Single JSON array file; no ORM; IDs are ints.
- **Errors:** Missing task → `404` with `Task with id … not found`; validation → `422`; delete success → `204`.
- **Frontend/backend:** Separate static page calling REST over CORS (`:8001` / `:5500` origins); board columns mirror status values.

## 6. Not visible or assumptions

- `routes/tasks.py`, `services/task_service.py`, `schemas.py`, `validators.py` exist as stubs—**not** on the create path.
- Comments/activity features are **not** present on this branch (other branches may differ).
- Production deploy, auth, multi-user tenancy, and DB backups were **not** observed.
- Whether `tasks.json` is always gitignored in every environment was not fully confirmed beyond local data usage + test isolation.
