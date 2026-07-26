# Decision note — Mid-Course features

How **Comments** and **Activity Log** were implemented on `Mid-Course-Project`, using a small loop: **ask → inspect → run · test · refine**.

## Shared approach

1. **Ask** — State the next tiny goal (one API slice or one UI step). Prefer clear contracts over large rewrites. Correct AI assumptions early (example: Activity Log uses **Option A — JSON `activity.json`**, not SQLite).
2. **Inspect** — Read the current models, storage, routes, and `frontend/index.html` before changing anything. Keep edits local; do not rewrite whole files.
3. **Run · test · refine** — Start the API (`:8000`) and frontend (`:8001`), hit `/docs`, run pytest + short break/edge checks, then adjust only what failed or felt unclear.

Both features stay vanilla on the frontend (no new frameworks, auth, or realtime). Backend stays FastAPI + Pydantic + JSON files.

## Feature 1 — Comments

| Step | What happened |
|------|----------------|
| Ask | List / add / delete comments per task; reject blank text; show them in the edit modal. |
| Inspect | Reused the task pattern: models → `comment_storage` → service → routes; modal already existed for edits. |
| Run · test · refine | Wired routes, then UI in small drafts (list → add → delete → card counts). Baseline + break checks covered blank text, 404s, and delete/re-delete. |

**Decision:** Comments are task-scoped only. Server owns `id`, `task_id`, and `created_at`.

## Feature 2 — Activity Log

| Step | What happened |
|------|----------------|
| Ask | Record create / update / delete / status-change; expose `GET /activity` and `GET /tasks/{id}/activity`; small UI feed. |
| Inspect | Mirrored comments storage shape; hooks sit on successful task writes in `main.py`. Invalid status transitions must not append events. |
| Run · test · refine | Backend tests first, then UI (global panel → per-task modal). Break tests confirmed from/to on status changes and that **deletes are recorded** on the global feed (per-task feed 404s after delete). |

**Decision:** Read + record only (no clear-history endpoint). Storage is JSON (**Option A**). Status changes store `from_status` / `to_status`.

## Takeaway

The loop kept scope honest: ask for one slice, inspect what already works, run it, test the contract, refine. That is how both features stayed readable and reviewable instead of becoming a full rewrite.
