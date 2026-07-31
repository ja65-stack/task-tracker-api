# Backend

FastAPI Task Tracker API lives in this folder.

```
backend/
├── app/           # models, storage, routes, services
├── frontend/      # simple HTML UI
├── tests/         # pytest suite
└── requirements.txt
```

Run from this folder:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
