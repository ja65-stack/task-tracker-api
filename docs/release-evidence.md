# Release Evidence

## Baseline

- Branch: `Module_4`
- Date: _______________
- Local app run command: `cd backend && uvicorn app.main:app --reload --port 8000`
- `/health` result: _______________
- Frontend check: _______________
- Test command: `cd backend && pytest -v`
- Test result: _______________

## CI evidence

- Workflow file: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
- Latest run link or note: _______________
- Test command used by CI: `pytest -v` (job `defaults.run.working-directory: backend`; Python `"3.11"`)
- Shortcut check: no `continue-on-error` / no `|| true` / pytest is not skipped.
  - [ ] Confirmed in workflow file (static review)
  - [ ] Confirmed on latest green run (live)

## Docker evidence

- Build command: `docker build -t task-tracker:dev ./backend`
- Run command: `docker run --rm -p 8000:8000 --name tt-dev task-tracker:dev`
- `/health` check: _______________
- Non-root check, if implemented: Dockerfile uses `USER app` — live confirm: _______________
- No-baked-secrets check: _______________

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |
