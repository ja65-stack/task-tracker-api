# Personal AI coding playbook

How I use AI on Task Tracker.

## 1. When I reach for AI first

- I need a first-pass endpoint outline (paths, body, errors) before I touch the repo—e.g. I planned `POST`/`GET /tasks/{task_id}/comments` (body, errors, 201) before wiring `comment_storage` / routes.
- I need help finding the right file or path on GitHub—e.g. I looked for `docs/decisions/comments-feature-plan` when it still only lived in chat.
- I need a plan or a failing test before I change anything.
- I’m comparing two choices—e.g. I compared the generic comments plan, the repo-grounded plan, and what Mid-Course actually shipped (`text` + int ids + delete vs `author`/`body`/UUID).

## 2. When I do not reach for AI

- Tiny edits I already understand—e.g. stop sending unchanged `status` on PATCH (`originalEditStatus` in `backend/frontend/index.html`) after same-to-same `ToDo → ToDo` returned 422.

## 3. My non-negotiables

- I never commit AI-generated code I haven’t reviewed and can’t explain—e.g. Module 5 CI ownership: `working-directory: backend`, quoted `"3.11"`, and `pytest -v` in `.github/workflows/ci.yml` before calling CI “done” (`docs/ai-usage.md`).
- I reproduce a failing test or exact error before asking AI for a fix—e.g. title-only edit → 422 `Invalid status transition from ToDo to ToDo`, then the PATCH omit-status fix.

## 4. My review rules

- Before I accept a change, I read the diff and check one happy path and one failure—e.g. comments list/add 201 + server fields; blank `text` → 422; missing task → 404 (`test_comments.py` / baseline).

## 5. What I am still figuring out

- How much AI drafting is useful before I open the files and write v1—e.g. architecture strategies A/B/C scoped the same app differently.

## Decision Card

- For a new feature I reach for: a structured-context strategy—user story → roles → short interview → tasks → then prompt before any code.
- For a code review I reach for: a senior-reviewer role that gives findings and optional patch drafts—I still decide merge/reject.
- For debugging I reach for: the failing signal first (error, failing test, or repro)—then AI for next checks, not a full rewrite.
- For infrastructure I reach for: a checklist first (commands, env, failure modes)—then AI only to draft or explain config I already decided to use.
- I will never paste credentials, tokens, or private personal data into an AI tool.
- My one rule is: AI can draft; I decide.

I will re-read this playbook on **September 1, 2026**.
