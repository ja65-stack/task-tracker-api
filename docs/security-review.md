# Security review — Task Tracker

Read-only audit notes for the Module 4/5 learning codebase. This is **not** a
claim of production readiness.

## Summary

Most “open API” findings are **accepted course-scope decisions**. The items that
are not merely “we chose no auth” are unbounded string fields (**S1**) and a
possible Docker data-directory permission mismatch (**S4**, not live-verified).

## Findings

| ID | Severity | Classification | File / location | Finding | Evidence | Suggested next step | Confidence |
|----|----------|----------------|-----------------|---------|----------|---------------------|------------|
| S1 | Medium | **Open residual risk** (not merely no-auth) | `app/models.py` | User-controlled `description`, `assignee`, and comment `text` have no max length; only title is capped at 200 and comments reject blank text. | `_normalize_title` enforces blank + max 200; `description`/`assignee` are unbounded `str \| None`; `_normalize_comment_text` rejects blank only. | Document as accepted size risk for the course, or (if explicitly approved) add `max_length` + tests. | High |
| S2 | Medium (course-scope) | **Accepted course-scope / residual risk** | `app/main.py`, `routes/comments.py`, `routes/activity.py`, `AGENTS.md`, `README.md` | No authentication or authorization; any local caller can use full task/comment/activity APIs. | No auth dependencies in routes; docs state no auth/accounts by design. | Keep local-only; do not expose on a public network without a later auth design. | High |
| S3 | Medium | **Accepted course-scope / residual risk** (optional) | `requirements.txt`, `.github/workflows/ci.yml` | Dependencies are unpinned, so installs can drift across machines/time. | Requirements list names only; CI runs `pip install -r requirements.txt`. | Accept for coursework unless pinning is required; optional pin for reproducibility. | High |
| S4 | Medium | **Open residual risk — not live-verified** | `Dockerfile`, `app/storage.py` | Non-root `USER app` after root-owned `COPY app` may block writes to `app/data/*.json`. | Dockerfile copies app then switches user with no `chown`; storage writes JSON under `app/data/`. | Verify with Docker (`POST /tasks` or file write as `app`). Fix ownership only if writes fail. | Medium |
| S5 | Low | **Accepted course-scope / residual risk** | `app/main.py` | CORS allows all headers for configured local frontend origins. | `allow_headers=["*"]` with origins limited to localhost/127.0.0.1 `:8001`/`:5500`. | Accept for local UI; tighten only if origins expand. | High |
| S6 | Low / Informational | **Accepted course-scope / residual risk** | `app/main.py`, README | `/docs` and CRUD APIs are reachable without auth when the server is running. | Standard FastAPI app with included routers; README advertises `/docs`. | Expected for this learning API; keep off public networks. | High |
| S7 | Low / Informational | **Accepted course-scope / residual risk** | `Dockerfile` | Container listens on `0.0.0.0:8000`. | `CMD` uses `--host 0.0.0.0 --port 8000`. | Normal for containers; avoid publishing ports on untrusted networks. | High |

## Classification guide used

- **Accepted course-scope / residual risk:** Documented learning tradeoff (especially no auth, local CORS, open `/docs`, container bind, unpinned deps).
- **Open residual risk:** Not explained away by “no auth alone” (input size limits; Docker write permissions if confirmed).

## Categories with no substantiated issue in the audit

- Secrets committed in inspected config (`.env.example` is non-secret placeholders; `.dockerignore` excludes `.env`)
- Broad bare `except:` handlers in inspected routes
- Frontend rendering of user strings via `innerHTML` (user content uses `textContent`)
- Missing enum validation for task status/priority (enums + transition rules exist)
- Deployment pipeline beyond local CI test job (none present)

## Audit limits

- Static read-only review; tests/app were not re-executed for this document.
- **S4** remains unverified until a working Docker engine confirms JSON write behavior as user `app`.
- No live capture of FastAPI validation error payloads from a running `/docs` session.

## Related project guidance

- Agent/course guardrails: [`AGENTS.md`](../AGENTS.md)
- Runbook / limitations: [`README.md`](../README.md)
