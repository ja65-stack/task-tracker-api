# Release Evidence

## Baseline

- Branch: `final-project` (formerly `Module_4`)
- Date: 2026-08-06 (baseline); Docker live evidence updated **2026-08-10**
- Local app run command: `uvicorn app.main:app --reload --port 8000`  
  (baseline evidence run used: `python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000`)
- `/health` result: **PASS** — `GET http://127.0.0.1:8000/health` returned  
  `{"status":"ok","timestamp":"2026-08-06T15:41:02.727038+00:00"}` (2026-08-06 cloud agent run)
- Frontend check: **PASS (prior recorded evidence)** — see [`verification.md`](verification.md): board loads tasks; title-only edit fixed (`originalEditStatus` omits unchanged `status` after 422 `ToDo → ToDo`); comments list/add/delete in modal; global + per-task activity. Not re-driven in the browser in this 2026-08-06 evidence pass.
- Test command: `python3 -m pytest -v`
- Test result: **73 passed**, 4 warnings, in 0.39s (2026-08-06). Matches [`verification.md`](verification.md) total. (Suite later **76 passed** after null-title / same-status fixes.)

## CI evidence

- Workflow file: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
- Latest green run (includes `test` + `docker` jobs):  
  https://github.com/ja65-stack/task-tracker-api/actions/runs/31381717024  
  (2026-08-10; conclusion: **success**)
- Earlier pytest-only green example:  
  https://github.com/ja65-stack/task-tracker-api/actions/runs/31116636319
- Test command used by CI: `pytest -v` at repository root; Python `"3.11"`
- Docker job in same workflow: build, run, `/health`, non-root `whoami`, no-baked-`.env` check  
  (details: [`docker-verification.md`](docker-verification.md))
- Shortcut check: no `continue-on-error` / no `|| true` / pytest is not skipped.
  - [x] Confirmed in workflow file (static review of `.github/workflows/ci.yml`)
  - [x] Confirmed on latest green run (live Actions conclusion: `success`)

## Docker evidence

- Build command: `docker build -t task-tracker:ci .` (CI) / `docker build -t task-tracker:dev .` (local README)
- Run command: `docker run -d --name tt-ci -p 8000:8000 task-tracker:ci` (CI)
- `/health` check: **PASS (live on GitHub Actions)** — job `docker` curled `http://127.0.0.1:8000/health` successfully  
  Run: https://github.com/ja65-stack/task-tracker-api/actions/runs/31381717024
- Non-root check: **PASS (live)** — `docker exec tt-ci whoami` → `app`
- No-baked-secrets check: **PASS (live spot check + static)** — `.dockerignore` excludes `.env` / `.env.*`; CI confirmed no `.env` at checked image paths
- Full log: [`docker-verification.md`](docker-verification.md)
- Local Windows Docker Desktop: still often blocked by missing virtualization; CI runners provide the required genuine execution evidence

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| Local API `/health` returns ok | Live curl to `127.0.0.1:8000/health` on 2026-08-06 | PASS | None |
| Full pytest suite green | `pytest -v` + CI `test` job | PASS | None |
| CI runs pytest and fails the job on test failure | `.github/workflows/ci.yml` + green Actions runs | PASS | None |
| Title-only edit does not 422 on same status | `verification.md` + frontend/backend same-status handling | PASS (after fix) | Omit unchanged status; same-status no-op |
| Docker image builds/runs and `/health` works | Actions job `docker` run 31381717024 | **PASS (live)** | Added CI `docker` job; recorded in docker-verification.md |
| Non-root container user | CI `whoami` → `app` | PASS | None (Dockerfile already had `USER app`) |
| Docs claimed no `docs/decisions/` | README VERIFY line vs repo | FAIL (stale) | Replaced with link to comments feature plan |
| Comments exist with author/body UUID shape | Mid-Course code vs assignment-style plan | Reality: `text` + int ids + delete | Plan grading noted mismatch; shipped Mid-Course shape kept |
| Performance review `.docx` should not stay in repo | User request | Removed | Deleted from `docs/forms/` and artifacts |
| `verification.md` location | Was at repo root | Moved | Now `docs/verification.md` |
