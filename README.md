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

### Viewing folders in Cursor Explorer

- **Agents Window:** press `Ctrl+G` (Windows/Linux) or `Cmd+G` (Mac) to open the file tree.
- **Classic IDE:** `Ctrl/Cmd+Shift+P` → **Open IDE**, then use the left Explorer panel.
- If a folder looks empty, expand the repo root again or reload the window (`Developer: Reload Window`).

## Run

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
