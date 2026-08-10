# Task Tracker API (final-project)

## 1. Project overview

Task Tracker is a **learning** FastAPI backend (Python 3.11) with JSON-file
persistence — not a production deployment.

Current capabilities (branch `final-project`):

- Task CRUD (`/tasks`, plus `PATCH /task/{id}` alias)
- Comments per task
- Activity log (`GET /activity`, `GET /tasks/{id}/activity`)
- Health check at `GET /health`
- Vanilla HTML/CSS/JS frontend under `frontend/`
- GitHub Actions CI and a multi-stage Docker image for the API

This project does **not** add a database, auth, accounts, or cloud deployment.

## 2. Prerequisites

- Git
- Python **3.11** (CI pins 3.11; [VERIFY] local minor versions may work)
- `pip`
- Optional: Docker (for container runs)
- Optional: a second terminal for the static frontend

## 3. Local setup

From the **repository root**:

```bash
git checkout final-project
git pull origin final-project
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Dependencies (from `requirements.txt`): FastAPI, Uvicorn, Pydantic,
python-dotenv, pytest, httpx.

## 4. Run the app locally

From the **repository root**:

```bash
uvicorn app.main:app --reload --port 8000
```

[VERIFY] If `uvicorn` is not on your PATH, use:
`python -m uvicorn app.main:app --reload --port 8000`.

- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

Optional frontend (second terminal, from repo root):

```bash
cd frontend
python -m http.server 8001 --bind 127.0.0.1
```

Open http://127.0.0.1:8001/ (calls the API at `http://127.0.0.1:8000`).

## 5. Run tests

From the **repository root**:

```bash
pytest -v
```

[VERIFY] If needed: `python -m pytest -v`.

## 6. Run with Docker

From the **repository root**:

```bash
docker build -t task-tracker:dev .
docker run --rm -p 8000:8000 --name tt-dev task-tracker:dev
```

Then: http://127.0.0.1:8000/health

The image uses `python:3.11-slim`, runs as non-root user `app`, and starts
`uvicorn app.main:app --host 0.0.0.0 --port 8000` (no `--reload`).

## 7. CI workflow summary

Workflow: `.github/workflows/ci.yml`

- Triggers: `push`, `pull_request`
- Python **3.11**
- Installs `requirements.txt` from the repository root
- Runs `pytest -v` from the repository root
- No deployment steps

## 8. Project structure

```
.
├── .github/workflows/ci.yml
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── AGENTS.md
├── DECISION_NOTE.md
├── README.md
├── docs/
│   ├── verification.md
├── app/
│   ├── main.py              # FastAPI app + task routes + /health
│   ├── models.py
│   ├── storage.py
│   ├── comment_storage.py
│   ├── activity_storage.py
│   ├── business_rules.py
│   ├── data/                # local JSON (gitignored)
│   ├── routes/
│   │   ├── comments.py
│   │   └── activity.py
│   └── services/
│       ├── comment_service.py
│       └── activity_service.py
├── frontend/
│   └── index.html
└── tests/
```

## 9. Project conventions and current limitations

**Conventions**

- JSON file storage (no ORM/DB)
- Pydantic models validate request bodies
- Status transitions are restricted (ToDo→InProgress→Done; Done→InProgress)
- Same-status on PATCH is a no-op (HTTP 200)
- Activity events are recorded on successful create/update/delete/status change
- Docker and CI target Python 3.11; container user is `app`

**Limitations**

- Not production-ready
- No authentication or multi-user accounts
- No relational database
- No deployment pipeline in this module
- Frontend is static and talks to `http://127.0.0.1:8000` only

## 10. Technical notes

- Mid-course decision note: [DECISION_NOTE.md](DECISION_NOTE.md)
- Verification notes / pytest counts: [docs/verification.md](docs/verification.md)
- Security review (Module 5): [docs/security-review.md](docs/security-review.md)
- AI usage / code ownership (Module 5): [docs/ai-usage.md](docs/ai-usage.md)
- AI coding playbook (Module 5): [docs/ai-playbook.md](docs/ai-playbook.md)
- Final AI review / ownership evidence (Module 5): [docs/final-ai-review.md](docs/final-ai-review.md)
- Comments feature plan: [docs/decisions/comments-feature-plan.md](docs/decisions/comments-feature-plan.md)
- Release evidence: [docs/release-evidence.md](docs/release-evidence.md)
