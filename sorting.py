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
    except:
        days_until_due = 999  # Far future if date is invalid/missing

    return (priority_score, 1 / days_until_due)
