# Task Tracker — Architecture (Strategy B)

Source of truth for this page: provided `AGENTS.md` (structured context).  
Checked out branch when writing: `cursor/restore-pydantic-models-e2a8` (no local `AGENTS.md`).

## 1. What the app does

Task Tracker is a learning FastAPI API with JSON-file persistence and a vanilla HTML/CSS/JS frontend. It supports task CRUD (including a `PATCH /task/{id}` alias), comments per task, an activity log (`GET /activity`, `GET /tasks/{id}/activity`), and a health check. It is not a production system: no auth, accounts, relational database, or deployment pipeline.

## 2. Data model

**Task** — `id` (server int); `title` (required, stripped, max 200); optional `description` / `assignee`; `status` (`ToDo` / `InProgress` / `Done`, default `ToDo`); `priority` (`Low` / `Medium` / `High`, default `Medium`); server timestamps.

**Comment** — task-scoped; required `text` (stripped; blank rejected). Server owns identity / linkage / timestamps per AGENTS persistence notes (exact field list beyond `text` not fully spelled in AGENTS).

**Activity event** — recorded on successful task create / update / delete / status change; exposed globally and per-task.

Statuses/priorities and allowed transitions live in `app/models.py` and `app/business_rules.py`.

## 3. Request flow — create task

1. UI (or client) `POST`s a create payload to `/tasks` on the API (`:8000`).
2. Pydantic validates create fields (`extra="forbid"`; title rules; enum defaults).
3. On success, the task is persisted to `backend/app/data/tasks.json` with a server-assigned integer id.
4. An activity event is recorded for the successful create (`app/main.py` + activity service).
5. API returns the created task; the Kanban UI refreshes from task list endpoints. Frontend is typically served on `:8001` and calls `http://127.0.0.1:8000`.

## 4. Key files

| File | Role |
|------|------|
| `AGENTS.md` | Agent/project conventions and confirmed stack |
| `backend/app/main.py` | App entry; wires routes; activity hooks on successful writes |
| `backend/app/models.py` | Task/comment (and related) validation and enums |
| `backend/app/business_rules.py` | Allowed status transition pairs |
| `backend/app/storage.py` | Task JSON persistence |
| `backend/app/data/*.json` | `tasks.json`, `comments.json`, `activity.json` (gitignored) |
| `backend/frontend/index.html` | Kanban + edit modal; omits unchanged status on PATCH |
| `backend/requirements.txt` | Unpinned Python deps |
| `.github/workflows/ci.yml` | CI: Python 3.11, `pytest -v` in `backend/` |

## 5. Conventions

- **Validation:** Title/comment text strip + blank reject; title max 200; unknown create/update fields forbidden; invalid enums → typically HTTP 422.
- **Status:** Only `ToDo→InProgress`, `InProgress→Done`, `Done→InProgress`; same-status and `ToDo→Done` → 422. Frontend omits `status` from PATCH unless it changed (`originalEditStatus`).
- **Storage:** JSON files under `backend/app/data/`; integer task ids; no ORM.
- **Errors:** Transition/validation failures → 422; missing resources handled as not-found style HTTP errors (exact detail strings: see routes when implementing).
- **Frontend/backend:** Separate static frontend; CORS-friendly local origins; API on 8000, UI often on 8001.
- **Ops:** Optional Docker; CI on push/PR; run Python tools with cwd `backend/`.

## 6. Not visible or assumptions

- This working tree does **not** contain `AGENTS.md` or comment/activity modules; those are confirmed in the **provided** AGENTS text (and appear on fuller branches such as `Module_4` / Mid-Course)—treat this doc as describing that documented system, not the sparse checkout alone.
- Full Comment/Activity field lists (beyond AGENTS bullets) were **not** re-derived here.
- Exact HTTP status/detail for every comment/activity miss path: **not confirmed** from AGENTS alone.
- Docker “works on every machine”: AGENTS marks engine as required / not universal.
- Unpinned dependency versions → reproducible builds **not confirmed**.
