import unittest
import os
import csv
from datetime import datetime, timedelta
from task_model import Task, Priority, load_tasks_from_csv, save_tasks_to_csv
from sorting import compute_urgency

class TestTaskManagerLogic(unittest.TestCase):

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

    def test_save_and_load_csv(self):
        test_file = "test_tasks.csv"
        original_tasks = [
            Task("Test 1", "01/01/2099", Priority.HIGH, "urgent", False),
            Task("Test 2", "02/02/2099", Priority.LOW, "", True)
        ]

        save_tasks_to_csv(test_file, original_tasks)
        loaded_tasks = load_tasks_from_csv(test_file)

        self.assertEqual(len(original_tasks), len(loaded_tasks))
        for orig, loaded in zip(original_tasks, loaded_tasks):
            self.assertEqual(orig.title, loaded.title)
            self.assertEqual(orig.due_date, loaded.due_date)
            self.assertEqual(orig.priority, loaded.priority)
            self.assertEqual(orig.tags, loaded.tags)
            self.assertEqual(orig.completed, loaded.completed)

        os.remove(test_file)

if __name__ == '__main__':
    unittest.main()
