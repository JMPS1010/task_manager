import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QDate
import sys

from main import TaskManager

app = QApplication(sys.argv)

class TestTaskManagerUI(unittest.TestCase):
    def setUp(self):
        self.form = TaskManager()
        self.form.show()

    def test_add_task_button_click(self):
        self.form.title_input.setText("UI Test Task")
        self.form.priority_input.setCurrentText("Medium")
        self.form.tags_input.setText("test")
        self.form.completed_input.setChecked(False)
        self.form.date_picker.setDate(QDate.currentDate().addDays(1))

        QTest.mouseClick(self.form.add_button, Qt.LeftButton)


        last_row = self.form.table.rowCount() - 1
        self.assertGreaterEqual(last_row, 0)

        title_item = self.form.table.item(last_row, 0)
        self.assertEqual(title_item.text(), "UI Test Task")

    def tearDown(self):
        self.form.close()

if __name__ == '__main__':
    unittest.main()
