# Task Tracker API

## Project Description

Task Tracker is a learning project built with Python and FastAPI.

The current implementation on branch `Mid-Course-Project` provides:

- FastAPI task CRUD routes
- Pydantic v2 task and comment models
- JSON file persistence for tasks and comments
- Task comment list/add/delete API
- Activity log API (`GET /activity`, `GET /tasks/{id}/activity`) recorded on task create/update/delete/status change
- A simple vanilla HTML/CSS/JS frontend (Kanban, edit modal with comments, global + per-task activity)

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app + task routes
│   ├── models.py               # Task + Comment Pydantic models
│   ├── storage.py              # tasks.json helpers
│   ├── comment_storage.py      # comments.json helpers
│   ├── activity_storage.py     # activity.json helpers
│   ├── business_rules.py
│   ├── data/                   # local JSON data (gitignored)
│   ├── routes/
│   │   ├── comments.py         # comment list/add/delete routes
│   │   └── activity.py         # GET /activity and per-task activity
│   └── services/
│       ├── comment_service.py
│       └── activity_service.py
├── frontend/
│   └── index.html
├── tests/
└── requirements.txt
```

## How to run

Use branch `Mid-Course-Project`:

```bash
git checkout Mid-Course-Project
git pull origin Mid-Course-Project
```

### 1. Backend (API)

From the repo root:

```bash
cd backend
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload
```

If `py` is not found, try `python` or `python3` instead.

- API base: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

Keep this terminal running while you use the frontend.

### 2. Frontend

In a **second** terminal, serve the frontend folder (example on port 8001):

```bash
cd backend/frontend
py -m http.server 8001 --bind 127.0.0.1
```

Then open: http://127.0.0.1:8001/

The page calls the API at `http://127.0.0.1:8000`. CORS already allows origins on ports `8001` and `5500`.

You can also open `backend/frontend/index.html` with VS Code/Cursor Live Server (port 5500).

### 3. Tests

With dependencies installed, from `backend/`:

```bash
cd backend
py -m pytest tests/ -q
```

Useful subsets:

```bash
py -m pytest tests/test_comments.py tests/test_comments_baseline.py -q
py -m pytest tests/test_comments_baseline.py -v
```

### Quick verification checklist

1. `http://127.0.0.1:8000/docs` shows **tasks** and **comments** endpoints
2. Frontend board loads tasks from the API
3. Edit a task → Comments panel lists/adds/deletes comments
4. `py -m pytest tests/ -q` passes

### Viewing the `backend` folder in Explorer

The API code is under **`backend/`** at the repo root (next to `README.md`).

1. Open the **repository root** (`task-tracker-api`), not a subfolder.
2. Or open **`task-tracker-api.code-workspace`** — Explorer then shows a top-level **backend** entry.
3. **Agents Window:** `Ctrl+G` (Windows/Linux) or `Cmd+G` (Mac), then expand the repo root.
4. If `backend` still does not appear: `Ctrl/Cmd+Shift+P` → **Developer: Reload Window**.

If you already opened the `backend` folder itself, Explorer will show `app/`, `tests/`, `frontend/` directly (there will be no nested folder named `backend`).
