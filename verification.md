# Verification — Mid-Course-Project

Evidence from an actual pytest run and frontend checks for Comments + Activity Log.

## Pytest summary (actual run)

Command:

```bash
cd backend
python3 -m pytest tests/ -q
```

**Result: 73 passed**

| File | Passed |
|------|--------|
| `tests/test_activity.py` | 14 |
| `tests/test_comments.py` | 11 |
| `tests/test_comments_baseline.py` | 8 |
| `tests/test_health.py` | 1 |
| `tests/test_models.py` | 8 |
| `tests/test_storage.py` | 12 |
| `tests/test_tasks.py` | 19 |
| **Total** | **73** |

Notes on earlier incorrect counts:

- **59** was the suite total *before* activity tests were added (`11+8+1+8+12+19 = 59`).
- A later draft claimed **59** while also listing activity rows in a way that did not match the table total (**69**).
- Current collected/run total is **73** (`14+11+8+1+8+12+19`).

`backend/tests/Verify_a.py` is a manual script and is **not** collected by pytest.

## Frontend verification

| Scenario | Result | Notes |
|----------|--------|-------|
| Board loads tasks from API | PASS | `GET /tasks` |
| Edit title/description only (status unchanged) → Save | **PASS (fixed)** | Previously **FAIL**: form resent `status`, API returned `422` same-to-same (e.g. `InProgress → InProgress`). Fix: (1) frontend omits unchanged status on PATCH; (2) backend skips transition validation when status is unchanged (no-op). Pull `final-project`, restart API, hard-refresh frontend. |
| Edit with a real status change → Save | PASS | Status included only when different from original |
| Comments list / add / delete in modal | PASS | |
| Global Activity panel + per-task activity | PASS | Deletes appear on global feed; per-task feed 404s after delete |

## Correction log

- Marked the “title-only edit without status change” scenario as a real frontend bug (it was incorrectly treated as passing).
- Corrected pytest totals to match `python3 -m pytest tests/ -q` → **73 passed**.
