from datetime import datetime
from task_model import Priority

PRIORITY_MAP = {
    Priority.HIGH: 3,
    Priority.MEDIUM: 2,
    Priority.LOW: 1
}


def compute_urgency(task):
    priority_score = PRIORITY_MAP.get(task.priority, 0)

    try:
        due_date = datetime.strptime(task.due_date, "%m/%d/%Y")
        days_until_due = max((due_date - datetime.today()).days, 1)
    except ValueError:
        days_until_due = 999  # handle bad format gracefully

    # You could return a tuple for stable sorting (e.g., first by priority, then by days)
    return (priority_score, 1 / days_until_due)
