# Task Tracker — Architecture (Strategy C)

Scope: only `backend/app/main.py`, `backend/app/models.py`, `backend/app/storage.py`.

## 1. What the app does

Task Tracker API is a Module 1 FastAPI learning service that exposes health and task CRUD HTTP endpoints (list/filter, get, create, patch—including a `/task/{id}` alias—and delete). Tasks are validated with Pydantic models and persisted to a local JSON file. There is no comment or activity surface in the three files read.

## 2. Data model

**Task** (sole entity in these files)

| Field | Visible rules |
|-------|----------------|
| `id` | `int`; server-assigned in storage (`max(id)+1`) |
| `title` | required; strip; blank rejected; max 200 |
| `description` | optional `str \| None` |
| `status` | `ToDo` \| `InProgress` \| `Done`; create default `ToDo` |
| `priority` | `Low` \| `Medium` \| `High`; create default `Medium` |
| `assignee` | optional `str \| None` |
| `created_at` / `updated_at` | `datetime`; set by storage on create; `updated_at` refreshed on update |

DTOs: `TaskCreate` / `TaskUpdate` with `extra="forbid"`. `TaskResponse = Task`.

## 3. Request flow — create task

1. Client `POST /tasks` with a JSON body matching `TaskCreate`.
2. FastAPI/Pydantic validates the body in `main.create_task`; failures are not custom-handled in these files (framework response **not visible from the files I read** beyond using `TaskCreate`).
3. Handler calls `storage.add_task` → `create_task`.
4. Storage ensures `data/tasks.json`, loads the array, allocates next int `id`, sets UTC `created_at`/`updated_at`, appends, saves.
5. Handler returns the `Task` with HTTP `201 Created`.

## 4. Key files

| File | Role (only as referenced/read) |
|------|--------------------------------|
| `backend/app/main.py` | FastAPI app, CORS, health + task routes |
| `backend/app/models.py` | Task enums, entities, create/update DTOs |
| `backend/app/storage.py` | JSON-file task CRUD |
| `backend/app/data/tasks.json` | Persistence path used by storage |
| `backend/app/business_rules.py` | Imported for `validate_status_transition` on PATCH |

Other project files (frontend, tests, README, comments/activity modules): **not visible from the files I read.**

## 5. Conventions

- **Validation:** Title normalize in models; create/update forbid unknown fields; enums constrain status/priority.
- **Storage:** JSON array at `DATA_DIR/tasks.json`; load/validate into `Task`; no database in these files.
- **Errors (visible):** Missing task on get/patch/delete → `404` with `Task with id {task_id} not found`. Delete success → `204`. Create success → `201`. PATCH may call `validate_status_transition` when status is set; allowed pairs and that function’s status codes: **not visible from the files I read.**
- **Frontend/backend:** CORS allows `localhost`/`127.0.0.1` ports `8001` and `5500`, methods GET/POST/PATCH/DELETE/OPTIONS. Actual UI code and how users click “create”: **not visible from the files I read.**

## 6. Not visible or assumptions

- Allowed status transition matrix and exact transition error bodies: **not visible from the files I read** (`business_rules` not opened).
- Auth, deployment, CI, Docker, comments, activity: **not visible from the files I read.**
- Whether create validation failures return 422: **not visible from the files I read** (no explicit handler; not inferred).
- Frontend structure, `baseUrl`, and board UX: **not visible from the files I read.**
- Tests, gitignore of `tasks.json`, multi-writer safety: **not visible from the files I read.**
