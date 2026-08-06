# Final AI Review and Ownership Evidence

Module 5 close-out for Task Tracker on branch `Module_4`. Grounded in
[`AGENTS.md`](../AGENTS.md), [`docs/security-review.md`](security-review.md),
[`docs/ai-usage.md`](ai-usage.md), [`docs/ai-playbook.md`](ai-playbook.md),
[`docs/release-evidence.md`](release-evidence.md), and course work on Comments,
Activity Log, CI, and docs.

## AGENTS.md guardrails

- Repo-specific stack and commands included: **yes** (FastAPI/Pydantic/pytest,
  JSON files, CI Python 3.11, optional Docker, run/test commands with cwd
  `backend/`)
- Docs-first/read-first guardrail included: **yes** (docs-first; read-only by
  default; inspect before edits)
- Unexpected app/frontend edits rule included: **yes** (no `backend/app/`
  changes unless explicitly approved; Module 5 scope; no inventing findings)

## AI code review mini-log

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| Put comments models/routes only in `main.py` + `storage.py` (greenfield plan on sparse branch) | Useful (partial) / Needs-Resequencing vs Mid-Course | Fit the tasks-only checkout, but Mid-Course already used `comment_storage` + router + service | Compared to shipped Mid-Course; kept split layout; did not re-implement from the sparse-branch plan |
| Comment fields should be `author` / `body` / UUID `id` | Wrong for this repo’s shipped Feature 1 | Assignment-style plan; Mid-Course uses `text`, int ids, and delete | Graded plan vs code; kept Mid-Course `text` + int ids |
| README VERIFY: “No `docs/decisions/` directory” | Wrong (stale) | Directory existed after comments plan was added | Replaced VERIFY line with link to `docs/decisions/comments-feature-plan.md` |
| Strategy A architecture = full product description | Useful for checkout / incomplete for course system | Missed comments/activity/CI that `AGENTS.md` documents | Chose Strategy B for course-facing architecture; kept A/C as comparison artifacts |
| Docker is required to finish Module 4/5 | Noise / Wrong as a hard gate | Engine often missing (Windows virt / cloud) | Marked Docker optional; recorded “not confirmed live” in release evidence |

## AI security mini-review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| S1 — unbounded `description` / `assignee` / comment `text` | `backend/app/models.py` | Valid (open residual) | Title capped at 200; other strings not | Accept for course or add max_length only if approved |
| S2 — no authentication | `main.py`, comment/activity routes, README, AGENTS | Valid course-scope residual | Learning app by design | Keep local-only; do not publish without auth design |
| S3 — unpinned dependencies | `requirements.txt`, CI install step | Valid residual / Noise if treated as “critical vuln” | Drift risk, not an exploit by itself | Accept unless pinning required |
| S4 — non-root `USER app` may block JSON writes | `Dockerfile`, storage under `app/data/` | Valid concern; **not live-verified** | No Docker engine in evidence pass | Verify when Docker works; fix ownership only if writes fail |
| S5 — CORS `allow_headers=["*"]` | `main.py` | Noise for local course UI | Origins limited to localhost frontend ports | Accept |
| S6 / S7 — open `/docs`, container `0.0.0.0` | `main.py`, Dockerfile | Noise / expected learning setup | Documented, not a secret leak | Keep off untrusted networks |

## Manual security check

I treated “no auth” as an accepted course decision, not a surprise finding. What
I checked myself: title vs unbounded strings in `models.py` (S1); `.env` not
baked via `.dockerignore`; frontend user text via `textContent` (called out as
no substantiated `innerHTML` issue in the security review); CI has no
`continue-on-error` / `|| true` masking pytest; release evidence recorded live
`/health` ok and **73** pytest passes, with Docker left **not confirmed**. That
matters because it separates real residual risk (input size, unverified Docker
writes) from scary-but-expected learning-app behavior.

## One AI output I rejected or corrected

AI (and an assignment-style comments plan) pushed a greenfield comment shape
(`author` / `body` / UUID) and sometimes implied implementing on a branch that
did not match Mid-Course. I did not accept that as the truth of this repo. I
compared the generic plan, the repo-grounded plan, and Mid-Course code, kept the
shipped `text` + integer ids + delete API/UI, and used the plans for grading—not
as a silent rewrite of working Feature 1.

Another correction: title-only edit was not “fine” until we reproduced
`422 Invalid status transition from ToDo to ToDo` and fixed the frontend to omit
unchanged `status` (`originalEditStatus`).

## Three AI usage rules

1. Never paste: credentials, tokens, private `.env` values, or identifying
   personal paths (e.g. full `C:\Users\…`).
2. Always verify: CI critical lines (`working-directory: backend`, quoted
   `"3.11"`, `pytest -v` must fail the job) and any claim against files or a
   failing signal before I accept a fix.
3. Record AI contributions by: ownership notes in `docs/ai-usage.md`, the
   playbook Decision Card, security/release evidence docs, and explicit
   Useful / Noise / Wrong grades—not by pasting secrets into chat.

## Ownership statement

I am comfortable submitting this repository as my work because I can explain the
core Task Tracker behavior (statuses, transitions, comments, activity, JSON
storage) and the Module 4/5 delivery (CI, Docker files, docs) in my own words. AI
helped draft plans, workflows, and reviews, but I graded those outputs against
the real branch and tests—including rejecting wrong comment schemas and a stale
README VERIFY line. I reproduced the title-only **422** before accepting the
PATCH fix, and I recorded what was live-verified versus not confirmed (especially
Docker). My rule remains: AI can draft; I decide—and I own what ships.
