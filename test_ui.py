import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QDate
import sys
import os

from main import TaskManager

app = QApplication(sys.argv)

class TestTaskManagerUI(unittest.TestCase):
    def setUp(self):
        # Clean DB file if exists (optional, for clean tests)
        db_path = "tasks.db"
        if os.path.exists(db_path):
            os.remove(db_path)

        self.form = TaskManager()
        self.form.show()

    def add_and_save_task(self, title="UI Add Task", tags="test"):
        self.form.title_input.setText(title)
        self.form.priority_input.setCurrentText("Medium")
        self.form.tags_input.setText(tags)
        self.form.completed_input.setChecked(False)
        self.form.date_picker.setDate(QDate.currentDate().addDays(1))

        QTest.mouseClick(self.form.add_button, Qt.LeftButton)
        QTest.mouseClick(self.form.save_button, Qt.LeftButton)
        QTest.qWait(100)
        self.form.load_tasks_from_db_refresh()

    def test_add_task_button_click(self):
        self.add_and_save_task()
        last_row = self.form.table.rowCount() - 1
        title_item = self.form.table.item(last_row, 0)
        self.assertIsNotNone(title_item)
        self.assertEqual(title_item.text(), "UI Add Task")

    def test_edit_task(self):
        self.add_and_save_task("UI Task To Edit", tags="edit_test")
        last_row = self.form.table.rowCount() - 1
        self.form.table.selectRow(last_row)
        self.form.populate_inputs(last_row, 0)

        self.form.title_input.setText("UI Edited Task")
        self.form.priority_input.setCurrentText("High")
        QTest.mouseClick(self.form.edit_button, Qt.LeftButton)
        QTest.qWait(100)
        self.form.load_tasks_from_db_refresh()

        title_item = self.form.table.item(last_row, 0)
        priority_item = self.form.table.item(last_row, 2)
        self.assertIsNotNone(title_item)
        self.assertEqual(title_item.text(), "UI Edited Task")
        self.assertEqual(priority_item.text(), "High")

    def test_delete_task(self):
        self.add_and_save_task("UI Task To Delete", tags="delete_test")
        initial_count = self.form.table.rowCount()
        last_row = initial_count - 1
        self.form.table.selectRow(last_row)
        self.form.populate_inputs(last_row, 0)

        QTest.mouseClick(self.form.delete_button, Qt.LeftButton)
        QTest.qWait(100)
        self.form.load_tasks_from_db_refresh()

        self.assertEqual(self.form.table.rowCount(), initial_count - 1)

    def test_mark_complete(self):
        self.add_and_save_task("UI Task To Complete", tags="complete_test")
        last_row = self.form.table.rowCount() - 1
        self.form.table.selectRow(last_row)
        self.form.populate_inputs(last_row, 0)

        self.form.completed_input.setChecked(True)
        QTest.mouseClick(self.form.edit_button, Qt.LeftButton)
        QTest.qWait(100)
        self.form.load_tasks_from_db_refresh()

        status_item = self.form.table.item(last_row, 4)
        self.assertIsNotNone(status_item)
        self.assertEqual(status_item.text(), "Yes")

    def test_filter_task(self):
        self.add_and_save_task("UI Unique Filter Task", tags="filter_test")
        self.form.search_input.setText("Unique Filter")
        QTest.mouseClick(self.form.filter_button, Qt.LeftButton)

        self.assertGreaterEqual(self.form.table.rowCount(), 1)
        found_title = self.form.table.item(0, 0).text()
        self.assertIn("UI Unique Filter Task", found_title)

    def tearDown(self):
        self.form.close()

if __name__ == '__main__':
    unittest.main()
