# Task Tracker API

## Project Description

Task Tracker is a Module 1 learning project built with Python and FastAPI.

The current implementation provides:

- FastAPI application setup with task CRUD routes
- Pydantic v2 models (`Task`, `TaskCreate`, `TaskUpdate`)
- JSON file persistence under `backend/app/data/tasks.json`
- Health check endpoint and a simple frontend

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app + CRUD routes
│   ├── models.py            # Pydantic v2 Task models
│   ├── storage.py           # JSON file CRUD helpers
│   ├── business_rules.py    # Status transition rules
│   ├── schemas.py
│   ├── validators.py
│   ├── data/
│   │   └── tasks.json       # Persisted tasks
│   ├── routes/
│   │   └── tasks.py
│   └── services/
│       └── task_service.py
├── frontend/
│   └── index.html
├── tests/
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_models.py
│   ├── test_storage.py
│   └── test_tasks.py
└── requirements.txt
```

### Viewing the `backend` folder in Explorer

The API code is under **`backend/`** at the repo root (next to `README.md`).

1. Open the **repository root** (`task-tracker-api`), not a subfolder.
2. Or open **`task-tracker-api.code-workspace`** — Explorer then shows a top-level **backend** entry.
3. **Agents Window:** `Ctrl+G` (Windows/Linux) or `Cmd+G` (Mac), then expand the repo root.
4. If `backend` still does not appear: `Ctrl/Cmd+Shift+P` → **Developer: Reload Window**.

If you already opened the `backend` folder itself, Explorer will show `app/`, `tests/`, `frontend/` directly (there will be no nested folder named `backend`).

## Run

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
