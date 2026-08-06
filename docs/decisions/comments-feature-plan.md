# Comments on tasks — feature plan

Suitable draft for `docs/decisions/comments-feature-plan.md`.  
Branch observed: `cursor/restore-pydantic-models-e2a8`. **No comments feature exists today** (no matches for comment/activity in app, tests, or frontend).

---

## 1. Data Model

### Existing patterns to mirror

In `backend/app/models.py`:

- Persisted entity `Task` owns server fields (`id`, `created_at`, `updated_at`).
- Write DTOs `TaskCreate` / `TaskUpdate` use `ConfigDict(extra="forbid")`.
- String fields are normalized with strip + blank reject + max length via `@field_validator` (see `_normalize_title` / `TITLE_MAX_LENGTH = 200`).
- `TaskResponse = Task` is the route response alias.

`backend/app/schemas.py` is a stub (“schemas will be added…”). Live request/response models live in `models.py`, not `schemas.py`.

### Proposed comment models (same file / same style)

Add to `backend/app/models.py` (preferred over the empty `schemas.py`, unless the team decides to start using that stub):

| Model | Role | Fields |
|-------|------|--------|
| `Comment` | Persisted + API response | `id: str` (UUID), `task_id: str`, `author: str`, `body: str`, `created_at: datetime` (UTC) |
| `CommentCreate` | Request body | `author`, `body` only; `extra="forbid"` |
| `CommentResponse` | Alias | `CommentResponse = Comment` (same pattern as `TaskResponse`) |

**Validation (mirror title rules):**

- `author`: required; strip; reject blank; length 1–100.
- `body`: required; strip; reject blank; length 1–2000.
- Clients must not set `id` or `created_at` (omit from `CommentCreate`; forbid extras).

### Fit with task identity (important mismatch)

- Today `Task.id` is an **`int`**, assigned in `storage.create_task` as `max(id)+1` (`backend/app/storage.py`).
- Spec wants comment `task_id` as a **string** reference.

**Recommended shape:** store/expose `task_id` as a **string** that equals `str(task.id)` (e.g. `"3"`), and resolve the parent via existing `storage.get_task_by_id`, which already accepts `int | str` and parses with `_as_int_id`. Do **not** change `Task.id` to UUID for this feature.

Constants: e.g. `AUTHOR_MAX_LENGTH = 100`, `BODY_MAX_LENGTH = 2000` next to `TITLE_MAX_LENGTH`.

### Persistence placement

Today only `TASKS_FILE = …/data/tasks.json` exists. Prefer a **sibling file** for comments (keeps task documents unchanged and matches “JSON-file persistence” in README), e.g. `backend/app/data/comments.json`, with CRUD helpers in `backend/app/storage.py` (or a new `comment` section in the same module—storage is currently task-only and documented as “JSON-file persistence for tasks”).

Nested `comments: []` inside each task object is possible but would force rewriting task records on every comment and complicate `delete_task` / partial updates; separate file fits current storage style better.

`backend/app/services/task_service.py` and `backend/app/routes/tasks.py` are stubs; **live wiring is in `main.py` + `storage.py`**. Plan should follow that unless the team chooses to finally split routes.

---

## 2. API Routes

Register on the FastAPI app in `backend/app/main.py` (where all task routes live today), under a clear tag such as `comments`. CORS already allows `POST` / `GET` / `DELETE` from frontend origins (`http://127.0.0.1:8001`, etc.).

### MVP routes (aligned with existing task conventions)

#### `POST /tasks/{task_id}/comments`

- **Purpose:** Create a comment on an existing task.
- **Path param:** `task_id: str` (same style as `get_task` / `update_task`).
- **Request body (`CommentCreate`):**

```json
{ "author": "…", "body": "…" }
```

- **Success:** `201 Created`, `response_model=CommentResponse` (same pattern as `POST /tasks` → `201`).
- **Response body:** full comment including server `id` (UUID string), `task_id`, `author`, `body`, `created_at` (UTC).
- **Errors:**
  - Task missing → `404`, detail like existing `Task with id {task_id} not found`.
  - Validation (blank/too long/extra fields) → `422` (Pydantic / FastAPI), same as blank title.
  - Non-integer / unparsable `task_id` that cannot resolve a task → treated as not found via current `_as_int_id` behavior (returns `None`).

#### `GET /tasks/{task_id}/comments`

- **Purpose:** List comments for one task.
- **Success:** `200`, `list[CommentResponse]`.
- **Empty task with no comments:** `200` + `[]` (mirror `GET /tasks` empty list).
- **Missing task:** `404` with the same task-not-found detail (do not return `[]` for unknown tasks—avoids confusing “no comments” with “no task”).
- **Ordering:** decide in Open Questions; recommend ascending `created_at` for thread UI.

### Optional / not required for MVP

| Method | Path | Notes |
|--------|------|--------|
| `GET /comments/{comment_id}` | Single fetch | Not needed if UI always loads by task |
| `DELETE /comments/{comment_id}` | Delete | Only if product wants it |
| Nested delete on task delete | Cascade | See Migration / Open Questions |

No auth exists in this app (README: learning Module 1 CRUD). `author` is free text, like optional `assignee` on tasks—not a verified user.

**Do not** add comment endpoints only in the stub `backend/app/routes/tasks.py` unless also wiring a router into `main.py` (currently unused).

---

## 3. Tests

Follow existing style: pytest + `TestClient` from `backend/tests/conftest.py`; autouse fixture resets `tasks.json` under `tmp_path`. **Extend that fixture** to also reset a comments file (monkeypatch `COMMENTS_FILE` the same way as `TASKS_FILE`).

Naming mirrors `backend/tests/test_tasks.py` / `test_models.py` (`test_<action>_<condition>_returns_<status>`).

Suggested new files: `backend/tests/test_comments.py` (API) and model cases either there or in `test_models.py`; storage helpers in `test_storage.py` or `test_comment_storage.py`.

### Happy path

- `test_create_comment_on_existing_task_returns_201_with_full_body`
- `test_create_comment_sets_server_id_and_created_at`
- `test_create_comment_task_id_matches_parent_task`
- `test_list_comments_for_task_returns_200_and_items`
- `test_list_comments_empty_for_existing_task_returns_200_and_empty_list`
- `test_list_comments_ordered_by_created_at_ascending` *(if that sort is chosen)*

### Validation

- `test_create_comment_missing_author_returns_422`
- `test_create_comment_missing_body_returns_422`
- `test_create_comment_blank_author_returns_422`
- `test_create_comment_blank_body_returns_422`
- `test_create_comment_author_over_100_characters_returns_422`
- `test_create_comment_body_over_2000_characters_returns_422`
- `test_create_comment_unknown_field_returns_422` *(extra="forbid")*
- `test_comment_create_strips_author_and_body` *(unit, like `test_task_create_strips_title`)*

### Edge cases

- `test_create_comment_missing_task_returns_404_with_detail`
- `test_list_comments_missing_task_returns_404_with_detail`
- `test_list_comments_does_not_include_other_tasks_comments`
- `test_create_comment_ignores_or_forbids_client_supplied_id_and_created_at`
- `test_delete_task_behavior_with_existing_comments` *(assert cascade vs orphan vs block—once decided)*
- `test_cors_preflight_allows_post_comments_from_frontend_origin` *(optional; PATCH CORS already covered)*

Use the existing `created_task` fixture (or compose on it) so every comment test has a real parent task from `POST /tasks`.

---

## 4. Frontend Changes

**File that would change:** `backend/frontend/index.html` only (single-page kanban; no other frontend modules observed).

**Current UX hooks:**

- Cards built in `createCard(task)`; Edit opens `#taskEditModal`.
- API base: `const baseUrl = 'http://localhost:8000'`.
- Errors surfaced via `#taskEditError` + `getErrorMessage`.
- Static sample cards in HTML are replaced on `fetchTasks()`; comments UI should be driven by JS after load, not hard-coded samples.

**What the user would see (MVP proposal):**

1. On each card (or inside the edit modal when a task is open): a **Comments** section.
2. List of existing comments: author, body, and a readable `created_at`.
3. Small form: Author (required), Body (required), Submit.
4. After successful `POST`, refresh that task’s comment list (or append the returned comment).
5. Validation / 404 / network failures shown in a small error line (reuse `getErrorMessage` pattern).

**Practical placement:** Extend `#taskEditModal` with a comments block visible only when editing an existing task (`activeTaskId` set)—New Task has no id yet, so comments only after create. Alternatively a separate “View comments” control on the card; the modal reuse is lower surface area.

**CORS:** Frontend origins already listed; `POST` is already in `allow_methods`. No CORS change required for create/list unless new methods are added.

**Out of scope unless decided:** comment edit/delete UI, realtime, markdown.

---

## 5. Migration Notes

- Existing `backend/app/data/tasks.json` is currently `[]` in the tree; shape of each task has **no** comment fields. **Do not require rewriting historical task objects** if comments live in a separate `comments.json`.
- New file `backend/app/data/comments.json` (or agreed name): initialize as `[]` when missing, same `_ensure_storage` pattern as tasks.
- `.gitignore` / data policy: confirm whether `app/data/*.json` is ignored locally (not fully visible from README alone beyond “Persisted tasks”); tests already avoid the real file via `tmp_path`.
- `storage.delete_task` today only removes the task row. Implementers must define what happens to comments with that `task_id` (cascade delete recommended for file store consistency).
- `conftest.py` must monkeypatch and reset the comments path; otherwise API tests will leak state or hit the wrong file.
- No SQL/Alembic migration exists; this is a **file-shape** change only.
- Task IDs remain ints; comment `task_id` strings must stay compatible with `_as_int_id` / `get_task_by_id`.

---

## 6. Open Questions

1. **Delete policy:** When `DELETE /tasks/{task_id}` succeeds, should comments for that `task_id` be cascade-deleted, left orphaned, or should delete be blocked while comments exist?
2. **Immutability:** Is MVP create+list only, or are edit/delete of comments in scope?
3. **`task_id` type in JSON:** Store as string `"1"` always, or as JSON number `1` while typing the Pydantic field as `str` (coercion)? Need one canonical on-disk form for stable tests.
4. **List sort:** Oldest-first (thread) vs newest-first?
5. **Route layout:** Keep adding endpoints in `main.py`, or finally move task+comment routes into `backend/app/routes/` and include a router (stubs exist but are unused)?
6. **Models vs schemas:** Keep comment models in `models.py` (current convention) or start populating the empty `schemas.py`?
7. **Activity / audit:** This branch has **no** activity log. Should creating a comment also write an activity event later, or stay comments-only?
8. **Frontend base URL:** Code uses `http://localhost:8000`; CORS also allows `127.0.0.1`. Should comment work assume the same `baseUrl` quirk as tasks?

---

## Files read

- `README.md`, `backend/README.md`
- `backend/app/main.py`
- `backend/app/models.py`
- `backend/app/storage.py`
- `backend/app/business_rules.py`
- `backend/app/schemas.py`, `backend/app/validators.py`
- `backend/app/routes/tasks.py`, `backend/app/services/task_service.py`
- `backend/app/data/tasks.json`
- `backend/tests/conftest.py`, `test_tasks.py`, `test_models.py`, `test_storage.py`, `test_health.py`
- `backend/frontend/index.html`
- Repo layout / branch via `git` (`AGENTS.md` **not present** on this branch)

---

## Assumptions to verify

1. **Assumption:** Implementation should target this branch’s codebase (tasks-only, int ids, routes in `main.py`), not another branch that may already have comments/activity (`Module_4` was not checked out here).
2. **Assumption:** `AGENTS.md` is intentionally absent here; no agent guardrails from that file apply on this branch until added.
3. **Assumption:** Comment models belong in `models.py` beside Task models because that is where live API models actually live.
4. **Assumption:** Separate `comments.json` is preferred over nesting comments inside each task object.
5. **Assumption:** MVP HTTP surface is `POST` + `GET` under `/tasks/{task_id}/comments`, matching how tasks nest by id in URLs today.
6. **Assumption:** `task_id` on comments is the string form of the existing integer task id, not a new UUID for tasks.
7. **Assumption:** Frontend work is confined to `backend/frontend/index.html` and attaches comments to the existing edit modal or card actions.
8. **Assumption:** No authentication will gate `author`; it remains a required free-text field.
9. **Assumption:** Test isolation will extend the existing `tmp_path` + monkeypatch pattern in `conftest.py` rather than introducing a DB or new test runner.
10. **Unverified from files:** Whether local `app/data/*.json` is gitignored in all environments; only `tasks.json` content (`[]`) was observed. Confirm before relying on committed seed comment data.
