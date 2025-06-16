import unittest
import sqlite3
import os
from datetime import datetime, timedelta


from task_model import Task, Priority
from db import update_task_in_db, delete_task_from_db, load_tasks_from_db

from sorting import compute_urgency

DB_FILE = "tasks.db"

def insert_task_to_db(task):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, due_date, priority, tags, completed) VALUES (?, ?, ?, ?, ?)",
        (task.title, task.due_date, task.priority.value, task.tags, int(task.completed))
    )
    conn.commit()
    conn.close()

class TestTaskManagerLogic(unittest.TestCase):

    def setUp(self):
        self.clear_db()

    def clear_db(self):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks")
        conn.commit()
        conn.close()

    def test_priority_score_ordering(self):
        high = Task("High Task", "12/31/2099", Priority.HIGH, "", False)
        med = Task("Med Task", "12/31/2099", Priority.MEDIUM, "", False)
        low = Task("Low Task", "12/31/2099", Priority.LOW, "", False)

        self.assertGreater(compute_urgency(high), compute_urgency(med))
        self.assertGreater(compute_urgency(med), compute_urgency(low))

    def test_due_date_urgency(self):
        today = datetime.today()
        task_soon = Task("Soon", (today + timedelta(days=1)).strftime("%m/%d/%Y"), Priority.MEDIUM, "", False)
        task_later = Task("Later", (today + timedelta(days=10)).strftime("%m/%d/%Y"), Priority.MEDIUM, "", False)

        self.assertGreater(compute_urgency(task_soon), compute_urgency(task_later))

    def test_completed_task_is_not_more_urgent(self):
        future_date = (datetime.today() + timedelta(days=5)).strftime("%m/%d/%Y")
        active_task = Task("Active", future_date, Priority.HIGH, "", False)
        done_task = Task("Done", future_date, Priority.HIGH, "", True)

        self.assertEqual(compute_urgency(active_task), compute_urgency(done_task))

    def test_completed_task_sorting(self):
        future_date = (datetime.today() + timedelta(days=5)).strftime("%m/%d/%Y")
        task_a = Task("A", future_date, Priority.HIGH, "", False)
        task_b = Task("B", future_date, Priority.MEDIUM, "", False)
        task_c = Task("C", future_date, Priority.LOW, "", False)
        task_done = Task("Done", future_date, Priority.HIGH, "", True)

        tasks = [task_done, task_b, task_c, task_a]
        sorted_tasks = sorted(tasks, key=lambda t: (t.completed, -compute_urgency(t)[0], -compute_urgency(t)[1]))

        self.assertEqual(sorted_tasks[-1].title, "Done")
        self.assertTrue(sorted_tasks[-1].completed)
        self.assertEqual(sorted_tasks[0].title, "A")

    def test_save_and_load_sqlite(self):
        task1 = Task("DB Task 1", "01/01/2099", Priority.HIGH, "urgent", False)
        task2 = Task("DB Task 2", "02/02/2099", Priority.LOW, "info", True)

        insert_task_to_db(task1)
        insert_task_to_db(task2)

        tasks = load_tasks_from_db()
        self.assertEqual(len(tasks), 2)

        titles = [t.title for t in tasks]
        self.assertCountEqual(titles, ["DB Task 1", "DB Task 2"])

        task1_loaded = next(t for t in tasks if t.title == "DB Task 1")
        self.assertEqual(task1_loaded.priority, Priority.HIGH)
        self.assertEqual(task1_loaded.tags, "urgent")
        self.assertFalse(task1_loaded.completed)

    def test_update_task_in_db(self):
        original = Task("Original", "12/31/2099", Priority.MEDIUM, "work", False)
        insert_task_to_db(original)

        updated = Task("Updated", "01/01/2100", Priority.HIGH, "urgent", True)
        update_task_in_db(original, updated)

        tasks = load_tasks_from_db()
        self.assertEqual(len(tasks), 1)
        task = tasks[0]
        self.assertEqual(task.title, "Updated")
        self.assertEqual(task.due_date, "01/01/2100")
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(task.tags, "urgent")
        self.assertTrue(task.completed)

    def test_delete_task_from_db(self):
        task = Task("To Delete", "12/12/2099", Priority.LOW, "test", False)
        insert_task_to_db(task)

        delete_task_from_db(task)
        tasks = load_tasks_from_db()

        self.assertEqual(len(tasks), 0)
        titles = [t.title for t in tasks]
        self.assertNotIn("To Delete", titles)

if __name__ == '__main__':
    unittest.main()
