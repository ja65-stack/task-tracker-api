# Docker verification and security log

Live Docker evidence for Task Tracker on branch `final-project`.  
Local Docker Desktop on Windows was often blocked (“virtualization support not
detected”), so **genuine build/run evidence is produced on GitHub Actions
runners** (job `docker` in [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)).

## Commands executed in CI

| Step | Command |
|------|---------|
| Build | `docker build -t task-tracker:ci .` |
| Run | `docker run -d --name tt-ci -p 8000:8000 task-tracker:ci` |
| Health | `curl -sf http://127.0.0.1:8000/health` (retry loop) |
| Non-root | `docker exec tt-ci whoami` (expect `app`) |
| Secrets spot check | Fail if `/.env`, `/app/.env`, or `/build/.env` exists in the image |
| Cleanup | `docker rm -f tt-ci` |

## Results

- Date recorded: **2026-08-10**
- CI workflow run (green): https://github.com/ja65-stack/task-tracker-api/actions/runs/31381717024  
  (also green on push https://github.com/ja65-stack/task-tracker-api/actions/runs/31381710678)
- Build: ☑ PASS
- Run + `/health`: ☑ PASS
- Non-root (`whoami` → `app`): ☑ PASS
- No-baked-secrets spot check: ☑ PASS

## Security notes (static + live)

| Check | Evidence | Result |
|-------|----------|--------|
| Non-root process user | Dockerfile `USER app`; CI `whoami` | **PASS** (live in Actions `docker` job) |
| No `--reload` in production CMD | Dockerfile `CMD` uses uvicorn without `--reload` | PASS (static) |
| `.env` not copied into image | `.dockerignore` has `.env` / `.env.*`; CI spot check | **PASS** (live) |
| Image context excludes tests/frontend noise | `.dockerignore` lists `tests`, `frontend`, IDE folders | PASS (static) |
| Listens on `0.0.0.0:8000` | Expected for containers; keep ports off untrusted networks | Accepted course-scope |

## Relation to local Windows Docker

Local `docker build` / `docker run` remain valid when Docker Desktop +
virtualization work. The **Actions `docker` job** is the authoritative live
execution evidence recorded for this course repo.
