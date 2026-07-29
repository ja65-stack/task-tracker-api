# AGENTS.md — Task Tracker

Guidance for AI coding agents working in this repository.

## 1. Project summary

Task Tracker is a learning FastAPI API with JSON-file persistence and a small
vanilla HTML/CSS/JS frontend. It supports:

- Task CRUD (`/tasks`, plus `PATCH /task/{id}` alias)
- Comments per task
- Activity log (`GET /activity`, `GET /tasks/{id}/activity`)
- Health check (`GET /health`)

This is **not** a production system. There is **no** auth, accounts, relational
database, or deployment pipeline in the current codebase.

Primary application code lives under `backend/app/`. Frontend: `backend/frontend/index.html`.

## 2. Tech stack and supported commands

### Stack (confirmed)

- Python / FastAPI / Uvicorn / Pydantic
- pytest + httpx (TestClient)
- JSON file storage (`backend/app/data/*.json`, gitignored)
- Optional Docker image (`backend/Dockerfile`)
- GitHub Actions CI (`.github/workflows/ci.yml`, Python 3.11)

Dependencies are listed in `backend/requirements.txt` (unpinned versions).
No `pyproject.toml` is present.

### Run / test commands (from repository root)

Install:

```bash
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run API (README-supported):

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

If `uvicorn` is not on PATH (not confirmed on every machine):

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

- Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

Frontend (optional second terminal):

```bash
cd backend/frontend
python -m http.server 8001 --bind 127.0.0.1
```

Frontend calls `http://127.0.0.1:8000` (`baseUrl` in `backend/frontend/index.html`).

Tests (README + CI):

```bash
cd backend
pytest -v
```

Docker (README-supported; requires a working Docker engine):

```bash
docker build -t task-tracker:dev ./backend
docker run --rm -p 8000:8000 --name tt-dev task-tracker:dev
```

CI runs `pytest -v` in `backend/` on Python 3.11 for `push` and `pull_request`.

## 3. Business rules visible in code

### Task statuses (`app/models.py`)

- `ToDo`
- `InProgress`
- `Done`

### Task priorities (`app/models.py`)

- `Low`
- `Medium` (default on create)
- `High`

### Status transitions (`app/business_rules.py`)

Allowed pairs only:

- `ToDo` → `InProgress`
- `InProgress` → `Done`
- `Done` → `InProgress`

Same-status transitions are rejected (HTTP 422).
`ToDo` → `Done` is rejected (HTTP 422).

### Validation (`app/models.py`)

- Title required; blank/whitespace rejected; max length 200; stripped
- Create/Update models use `extra="forbid"` (unknown fields rejected)
- Default create status: `ToDo`; default priority: `Medium`
- Comment `text` required; blank/whitespace rejected; stripped
- Invalid enum values for status/priority are rejected by Pydantic (typically HTTP 422 via FastAPI)

### Persistence (`app/storage.py` and related)

- Tasks: `backend/app/data/tasks.json`
- Comments: `backend/app/data/comments.json`
- Activity: `backend/app/data/activity.json`
- Task ids are integers (server-assigned)
- Activity events recorded on successful create / update / delete / status change (`app/main.py` + activity service)

### Frontend note (visible)

- Edit modal omits `status` from PATCH unless the status value actually changed (`originalEditStatus` in `backend/frontend/index.html`), because the API rejects same-to-same status transitions.

## 4. Module 5 guardrails

- **Docs-first:** Prefer reading README, this file, models, routes, and tests before proposing edits.
- **Read-only by default:** Inspect and explain first. Do not modify files unless the user explicitly asks for a change.
- **One task per thread:** Complete one clear request at a time; do not expand into unrelated refactors.
- **No `app/` changes unless explicitly approved:** Do not edit `backend/app/` (or equivalent application logic) without explicit user approval for that change.
- Keep Module 5 work scoped; do not add auth, databases, or deployment unless the user explicitly requires it.

## 5. Security and governance

- Do **not** paste, commit, or expose secrets (API keys, tokens, passwords, private `.env` values).
- `.env` is ignored for Docker builds; `.env.example` only shows non-secret placeholders (`PORT`, `APP_ENV`).
- Do **not** run destructive commands (`rm -rf`, force-push, dropping data) unless the user explicitly requests them and the scope is clear.
- Cite concrete files/paths (and line ranges when helpful) for claims about behavior.
- Do **not** invent findings. If something is not visible in the repo, say **not confirmed**.
- Prefer small, reviewable diffs over rewrites.

## Working directory reminder

Most Python commands must run with cwd `backend/` so `app.main:app` and `tests/` resolve correctly.
