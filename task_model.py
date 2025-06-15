import csv
from enum import Enum
from dataclasses import dataclass
from typing import List
from datetime import datetime

class Priority(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

@dataclass
class Task:
    title: str
    due_date: str  # in format MM/DD/YYYY
    priority: Priority
    tags: str
    completed: bool

    def to_dict(self):
        return {
            "title": self.title,
            "due_date": self.due_date,
            "priority": self.priority.value,
            "tags": self.tags,
            "completed": self.completed,
        }

    @staticmethod
    def from_csv_row(row):
        title, due_date, priority_str, tags, completed_str = row
        # Validate date format
        try:
            datetime.strptime(due_date, "%m/%d/%Y")
        except ValueError:
            due_date = datetime.today().strftime("%m/%d/%Y")

        # Validate priority
        priority = Priority(priority_str) if priority_str in Priority._value2member_map_ else Priority.LOW
        completed = completed_str.strip().lower() == 'true'
        return Task(title, due_date, priority, tags, completed)

def load_tasks_from_csv(filename: str) -> List[Task]:
    tasks = []
    try:
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                tasks.append(Task.from_csv_row(row))
    except FileNotFoundError:
        pass
    return tasks

def save_tasks_to_csv(filename: str, tasks: List[Task]) -> None:
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Due Date', 'Priority', 'Tags', 'Completed'])
        for task in tasks:
            writer.writerow([task.title, task.due_date, task.priority.value, task.tags, str(task.completed)])
