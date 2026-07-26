# Backend

FastAPI Task Tracker API lives in this folder (branch `Mid-Course-Project`).

## Folder structure

```
backend/
├── app/
│   ├── models.py               # Task + Comment + Activity models
│   ├── storage.py
│   ├── comment_storage.py
│   ├── activity_storage.py     # activity.json helpers
│   ├── routes/
│   │   ├── comments.py
│   │   └── activity.py         # GET /activity and per-task activity
│   ├── services/
│   │   ├── comment_service.py
│   │   └── activity_service.py
│   └── data/                   # *.json gitignored; created on first use
├── frontend/                   # Kanban + comments + activity UI
├── tests/
│   └── test_activity.py
└── requirements.txt
```

## How to run

### Backend

```bash
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload
```

- Docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

### Frontend

In a second terminal:

```bash
cd frontend
py -m http.server 8001 --bind 127.0.0.1
```

Open http://127.0.0.1:8001/

### Tests

```bash
py -m pytest tests/ -q
```

Activity log tests:

```bash
py -m pytest tests/test_activity.py -q
```

Versions in `requirements.txt` are unpinned. If you add pins later, verify with `pip freeze` after installation.

See the root `README.md` for the full project run guide.
