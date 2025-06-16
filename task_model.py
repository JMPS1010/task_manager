# task_model.py
from enum import Enum

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Task:
    def __init__(self, title, due_date, priority, tags="", completed=False):
        self.title = title
        self.due_date = due_date
        self.priority = priority  
        self.tags = tags
        self.completed = completed
