# AI usage & code ownership — Task Tracker

Module 5 notes on **how I use AI on this course repo** and **what I must
understand before I accept generated code**.

This file is **not** the full governance sharing/risk worksheet. It records
ownership habits and three personal rules grounded in course work on this
project (Comments / Activity Log / Module 4 CI / Module 5 docs).

Related:

- Agent guardrails: [`AGENTS.md`](../AGENTS.md)
- Security review: [`security-review.md`](security-review.md)
- CI workflow: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
- Project README: [`README.md`](../README.md)

## What this file is (and is not)

| This file (`ai-usage.md`) | Governance retrospective |
|---------------------------|--------------------------|
| Which AI-generated blocks I reviewed | What I pasted into AI tools |
| Lines I can explain in my own words | Risk level of shared items (Low/Medium/High) |
| Check questions + written answers | Safer paste habits over the whole course |
| Personal AI usage rules below | Course-wide sharing inventory |

---

## My three personal AI usage rules

Concrete enough that a teammate could spot a violation.

### 1. What I will never paste into AI tools

- I will **never** paste credentials, tokens, API keys, private `.env` values,
  production config, or real customer/user data.
- I will **never** paste a full local absolute path that includes my Windows
  username (for example `C:\Users\ja65\...`). I will use a repo-relative path
  such as `backend/` or a placeholder like `C:\Users\<you>\...` instead.
- I will **never** paste a git clone or Actions URL that embeds an access token.

If I only need help with an error, I paste the **error type and a short
snippet**, not my whole machine path or any secret-bearing log line.

### 2. What I will always verify before accepting

Before I accept or commit **AI-generated GitHub Actions CI YAML** for this
repo, I must correctly answer all three checks for
[`.github/workflows/ci.yml`](../.github/workflows/ci.yml):

1. If `working-directory: backend` were removed, what exact failure would
   `pip install -r requirements.txt` hit?
2. Why is `python-version: "3.11"` written in quotes instead of as a bare
   number?
3. If a test fails, should the workflow still show a green check? Why or why
   not?

I do **not** merge CI changes until those answers are written in this file
(section below) and I can explain them without looking them up.

For other AI-generated blocks (Docker, docs, app code when approved), I at
least identify the critical lines and mark ownership in the artifact table
before I rely on them.

### 3. How I will record AI contributions

- For the CI workflow, I record ownership in **this file**: checkboxes, written
  answers to the three questions, and the date I marked them owned.
- I keep a short list of other AI-assisted artifacts (path + whether I
  reviewed critical lines).
- Governance sharing/risk inventory stays separate (course worksheet); this
  file stays focused on **verification and ownership**.

**Done signal for CI ownership:** all three “I own this?” boxes are Yes, and
the three answers are filled in below—not left as blank lines.

---

## Owned artifact: Module 4 CI workflow

**Source:** AI-assisted draft of `.github/workflows/ci.yml`
(Python 3.11, `pytest -v` in `backend/`).

### Three lines to understand before committing

| Priority | Line(s) | Why first | Check question | I own this? |
|----------|---------|-----------|----------------|-------------|
| 1 | `working-directory: backend` | Install/tests must run where `requirements.txt` and `app/` live | If this line were deleted, what exact failure would you expect on `pip install -r requirements.txt`? | ☑ Yes |
| 2 | `python-version: "3.11"` | Pins CI Python; avoids silent version drift | Why is `"3.11"` written in quotes instead of `3.11` as a bare number? | ☑ Yes |
| 3 | `run: pytest -v` | Real quality gate; without it CI only sets up the environment | If a test fails, should this workflow still show a green check? Why or why not? | ☑ Yes |

### Line-by-line notes (summary)

| Line(s) | What it does | What could break if wrong |
|---------|--------------|---------------------------|
| `name: CI` | Label in GitHub Actions UI | Clarity only |
| `on: push` / `pull_request` | When the workflow runs | CI never runs, or misses PR checks |
| `runs-on: ubuntu-latest` | GitHub-hosted Ubuntu runner | OS/path assumptions; image version can move over time |
| `working-directory: backend` | All `run` steps start in `backend/` | Root-relative `requirements.txt` / `pytest` fail |
| `actions/checkout@v4` | Clones the repo onto the runner | Later steps have no code |
| `actions/setup-python@v5` + `python-version: "3.11"` | Installs Python 3.11 | Wrong/missing Python |
| `pip install -r requirements.txt` | Installs app/test dependencies | Import/pytest failures |
| `pytest -v` | Runs the test suite; failures fail the job | False confidence if removed or masked |

### My answers

Date owned: 2026-07-29

1. **working-directory:**  
   Without `working-directory: backend`, `pip install -r requirements.txt`
   runs from the **repo root**. There is no `requirements.txt` at the root, so
   the step fails with a file-not-found error. Even if install were fixed,
   `pytest` from root would not see `backend/app` the way the project expects.

2. **quoted `"3.11"`:**  
   Quotes force a **string**. A bare YAML float like `3.10` can be parsed as
   `3.1`, so setup-python might install the wrong (or missing) version. `"3.11"`
   keeps the pin exact.

3. **failed test / green check:**  
   **No.** If `pytest -v` exits non-zero, the job must fail and the check must
   be red. A green workflow with failing tests would only prove that checkout,
   Python, and pip ran—not that the app still works.

### Study key (for self-check; answers above match this intent)

1. Pip would look for `requirements.txt` in the **repo root**, not `backend/`,
   and fail with a file-not-found style error (tests/`app` imports would also
   be wrong if you ran pytest from root without that default).
2. Quotes keep the value a **string**. A bare YAML number like `3.10` can be
   parsed as `3.1`, which is the wrong Python version.
3. **No.** A failing `pytest` must fail the job so the workflow is red. A green
   check with failing tests would mean CI is only “setup theater.”

---

## Other AI-assisted artifacts (ownership tracker)

| Artifact | Path | Critical lines reviewed? | Date |
|----------|------|--------------------------|------|
| Dockerfile | `backend/Dockerfile` | ☑ Yes (multi-stage, `USER app`, no `--reload`) | 2026-07-29 |
| AGENTS.md | `AGENTS.md` | ☑ Yes (ban limited to `backend/app/`, no destructive cmds) | 2026-07-29 |
| Security review | `docs/security-review.md` | ☑ Yes (S1–S7; open residual S1 / unverified S4) | 2026-07-29 |
| Activity / comments feature | `backend/app/`, `backend/frontend/index.html` | ☑ Yes (status PATCH omit-if-unchanged; activity after delete) | 2026-07-29 |

Per `AGENTS.md`: do not edit `backend/app/` unless explicitly approved.

---

## Rule of thumb

Do not commit AI-generated CI (or other generated changes) until the
**verify-before-accept** rule above is satisfied and recorded in this file.
