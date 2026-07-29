# AI usage & code ownership — Task Tracker

Module 5 notes on **understanding AI-generated code**, separate from the
governance retrospective (what was shared / risk levels).

Related:

- Agent guardrails: [`AGENTS.md`](../AGENTS.md)
- Security review: [`docs/security-review.md`](security-review.md)
- CI workflow file: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)

## What this file is (and is not)

| This file (`ai-usage.md`) | Governance retrospective |
|---------------------------|--------------------------|
| Which AI-generated blocks I reviewed | What I pasted into AI tools |
| Lines I can explain in my own words | Risk level of shared items (Low/Medium/High) |
| Check questions for ownership | Safer future paste habits |

## Owned artifact: Module 4 CI workflow

**Source:** AI-assisted draft of `.github/workflows/ci.yml` (Python 3.11, `pytest -v` in `backend/`).

### Three lines to understand before committing

| Priority | Line(s) | Why first | Check question | I own this? |
|----------|---------|-----------|----------------|-------------|
| 1 | `working-directory: backend` | Install/tests must run where `requirements.txt` and `app/` live | If this line were deleted, what exact failure would you expect on `pip install -r requirements.txt`? | ☐ Yes / ☐ Not yet |
| 2 | `python-version: "3.11"` | Pins CI Python; avoids silent version drift | Why is `"3.11"` written in quotes instead of `3.11` as a bare number? | ☐ Yes / ☐ Not yet |
| 3 | `run: pytest -v` | Real quality gate; without it CI only sets up the environment | If a test fails, should this workflow still show a green check? Why or why not? | ☐ Yes / ☐ Not yet |

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

Full walkthrough was done in the Module 5 AI-usage session; mark “I own this?” only when you can explain the row without looking it up.

### Answers to check (fill after you attempt them yourself)

1. *working-directory:* _______________________________________________
2. *quoted 3.11:* _______________________________________________
3. *failed test / green check:* _______________________________________________

## Other AI-assisted artifacts (ownership TBD)

Track briefly; deepen only if the course asks:

| Artifact | Path | Reviewed line-by-line? |
|----------|------|------------------------|
| Dockerfile | `backend/Dockerfile` | ☐ |
| AGENTS.md | `AGENTS.md` | ☐ |
| Security review doc | `docs/security-review.md` | ☐ |
| Activity / comments feature code | `backend/app/`, `backend/frontend/index.html` | ☐ (scope as assigned) |

## Rule of thumb

Do not commit AI-generated CI/Docker/app changes until you can explain the **critical lines** above in your own words.
