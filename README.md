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
  app/
    models.py          # Pydantic v2 task models
    storage.py         # JSON file CRUD helpers
    data/tasks.json    # Persisted tasks
    main.py            # FastAPI app + routes
    business_rules.py  # Status transition rules
  frontend/
  tests/
```

## Run

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
