from fastapi import HTTPException, status

from app.models import TaskStatus

VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
})


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    """Ensure ``current`` → ``new`` is an allowed status transition.

    Allowed pairs: ToDo→InProgress, InProgress→Done, Done→InProgress.
    Same status (``current == new``) is always allowed as a no-op.

    Args:
        current: Existing task status.
        new: Requested task status.

    Returns:
        None: Returns normally when the transition is allowed or is a no-op.

    Raises:
        HTTPException: 422 when ``(current, new)`` is not in ``VALID_TRANSITIONS``
            and is not the same status.
    """
    # Normalize so str/enum mixes still count as same-status no-ops.
    current_value = getattr(current, "value", current)
    new_value = getattr(new, "value", new)
    if current_value == new_value:
        return

    if (current, new) not in VALID_TRANSITIONS:
        allowed = sorted({f"{f.value}->{t.value}" for f, t in VALID_TRANSITIONS})
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Invalid status transition from {current_value} to {new_value}. "
                f"Allowed transitions: {allowed}"
            ),
        )
