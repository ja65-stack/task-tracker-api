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

- Date recorded: _______________
- CI workflow run (green): _______________
- Build: ☐ PASS / ☐ FAIL
- Run + `/health`: ☐ PASS / ☐ FAIL
- Non-root (`whoami` → `app`): ☐ PASS / ☐ FAIL
- No-baked-secrets spot check: ☐ PASS / ☐ FAIL

*(Fill the blanks after the first green `docker` job run; see
[`release-evidence.md`](release-evidence.md).)*

## Security notes (static + live)

| Check | Evidence | Result |
|-------|----------|--------|
| Non-root process user | Dockerfile `USER app`; CI `whoami` | Declared in Dockerfile; live-confirmed in CI when job is green |
| No `--reload` in production CMD | Dockerfile `CMD` uses uvicorn without `--reload` | PASS (static) |
| `.env` not copied into image | `.dockerignore` has `.env` / `.env.*`; CI spot check | PASS when CI job is green |
| Image context excludes tests/frontend noise | `.dockerignore` lists `tests`, `frontend`, IDE folders | PASS (static) |
| Listens on `0.0.0.0:8000` | Expected for containers; keep ports off untrusted networks | Accepted course-scope |

## Relation to local Windows Docker

Local `docker build` / `docker run` remain valid when Docker Desktop +
virtualization work. Until then, the **Actions `docker` job** is the
authoritative live execution evidence for this course repo.
