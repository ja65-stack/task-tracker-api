# Backend

FastAPI Task Tracker API lives in this folder.

## Folder structure (comments skeleton)

```
backend/
├── app/
│   ├── main.py                 # FastAPI app (task routes live here today)
│   ├── models.py               # Task + Comment Pydantic models
│   ├── storage.py              # tasks.json helpers
│   ├── comment_storage.py      # comments.json helpers
│   ├── routes/
│   │   ├── tasks.py
│   │   └── comments.py         # router stub (no comment endpoints yet)
│   ├── services/
│   │   ├── task_service.py
│   │   └── comment_service.py  # list/add/delete helpers for future routes
│   └── data/
│       ├── tasks.json
│       └── comments.json
├── frontend/
├── tests/
└── requirements.txt
```

## Run from this folder

```bash
pip install -r requirements.txt
py -m uvicorn app.main:app --reload
```

If you pin versions in `requirements.txt`, verify installed versions with `pip freeze` after installation.

