# Release Evidence

## Baseline

- Branch: `Module_4`
- Date: 2026-08-06
- Local app run command: `uvicorn app.main:app --reload --port 8000`  
  (this evidence run used: `python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000`)
- `/health` result: **PASS** — `GET http://127.0.0.1:8000/health` returned  
  `{"status":"ok","timestamp":"2026-08-06T15:41:02.727038+00:00"}` (2026-08-06 cloud agent run)
- Frontend check: **PASS (prior recorded evidence)** — see [`verification.md`](../verification.md): board loads tasks; title-only edit fixed (`originalEditStatus` omits unchanged `status` after 422 `ToDo → ToDo`); comments list/add/delete in modal; global + per-task activity. Not re-driven in the browser in this 2026-08-06 evidence pass.
- Test command: `python3 -m pytest -v`
- Test result: **73 passed**, 4 warnings, in 0.39s (2026-08-06). Matches [`verification.md`](../verification.md) total.

## CI evidence

- Workflow file: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
- Latest run link or note: **success** on push to `Module_4` —  
  https://github.com/ja65-stack/task-tracker-api/actions/runs/31116636319  
  (“Add docs/release-evidence.md baseline template”, completed 2026-08-06)
- Test command used by CI: `pytest -v` (job `defaults.run.working-directory: .  # repo root (layout flattened)`; Python `"3.11"`)
- Shortcut check: no `continue-on-error` / no `|| true` / pytest is not skipped.
  - [x] Confirmed in workflow file (static review of `.github/workflows/ci.yml`)
  - [x] Confirmed on latest green run (live Actions conclusion: `success`)

## Docker evidence

- Build command: `docker build -t task-tracker:dev .`
- Run command: `docker run --rm -p 8000:8000 --name tt-dev task-tracker:dev`
- `/health` check: **Not confirmed live** — Docker engine unavailable in this cloud environment; on the Windows workstation Docker Desktop / virtualization was often not detected earlier in the course. README commands remain the intended path when an engine is available.
- Non-root check, if implemented: Dockerfile declares `USER app` — **static PASS**; live `whoami`/process user inside a running container **not confirmed** (no engine here).
- No-baked-secrets check: **static PASS** — `.dockerignore` excludes `.env` and `.env.*`; Dockerfile copies `requirements.txt` + `app/` only (no secret files observed in those COPY lines). Live image inspect **not confirmed**.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| Local API `/health` returns ok | Live curl to `127.0.0.1:8000/health` on 2026-08-06 | PASS | None |
| Full pytest suite green on Module_4 | `python3 -m pytest -v` → 73 passed | PASS | None |
| CI runs pytest and fails the job on test failure | `.github/workflows/ci.yml` + Actions run 31116636319 success | PASS | None |
| Title-only edit does not 422 on same status | `verification.md` + frontend `originalEditStatus` fix | PASS (after fix) | Frontend omits unchanged `status` from PATCH |
| Docker image builds/runs and `/health` works | Attempted in cloud; prior Windows virt issues | Not confirmed live | Left Docker optional in docs / AGENTS |
| Docs claimed no `docs/decisions/` | README VERIFY line vs repo | FAIL (stale) | Replaced with link to `docs/decisions/comments-feature-plan.md` |
| Comments exist with author/body UUID shape | Mid-Course code vs assignment-style plan | Reality: `text` + int ids + delete | Plan grading noted mismatch; shipped Mid-Course shape kept |
| Performance review `.docx` should not stay in repo | User request | Removed | Deleted from `docs/forms/` and artifacts |
