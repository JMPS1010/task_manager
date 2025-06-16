import sqlite3
from task_model import Task, Priority

DB_NAME = "tasks.db"

def create_tasks_table():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                title TEXT NOT NULL,
                due_date TEXT NOT NULL,
                priority TEXT NOT NULL,
                tags TEXT,
                completed INTEGER
            )
        """)
        conn.commit()

def load_tasks_from_db():
    create_tasks_table()  # ensure the table exists
    tasks = []
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, due_date, priority, tags, completed FROM tasks")
        for title, due_date, priority, tags, completed in cursor.fetchall():
            tasks.append(Task(
                title=title,
                due_date=due_date,
                priority=Priority(priority),
                tags=tags,
                completed=bool(completed)
            ))
    return tasks

def save_tasks_to_db(tasks):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks")
        for task in tasks:
            cursor.execute("""
                INSERT INTO tasks (title, due_date, priority, tags, completed)
                VALUES (?, ?, ?, ?, ?)
            """, (task.title, task.due_date, task.priority.value, task.tags, int(task.completed)))
        conn.commit()


def task_exists_in_db(task):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tasks WHERE title = ? AND due_date = ?", (task.title, task.due_date))
        return cursor.fetchone()[0] > 0



def update_task_in_db(original_task, updated_task):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tasks SET title = ?, due_date = ?, priority = ?, tags = ?, completed = ?
            WHERE title = ? AND due_date = ?
        """, (
            updated_task.title, updated_task.due_date, updated_task.priority.value,
            updated_task.tags, int(updated_task.completed),
            original_task.title, original_task.due_date
        ))
        conn.commit()

def delete_task_from_db(task):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE title = ? AND due_date = ?", (task.title, task.due_date))
        conn.commit()
