# Backend

FastAPI Task Tracker API lives in this folder (branch `Mid-Course-Project`).

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

Comment baseline:

```bash
py -m pytest tests/test_comments_baseline.py -v
```

If you pin versions in `requirements.txt`, verify installed versions with `pip freeze` after installation.

See the root `README.md` for the full project run guide.
