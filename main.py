# main.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QMessageBox, QWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import QDate
from PyQt5 import uic
from task_model import Priority, Task
from db import save_tasks_to_db, load_tasks_from_db, update_task_in_db, delete_task_from_db
from theme_manager import ThemeManager
from sorting import compute_urgency

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.tasks = load_tasks_from_db()
        self.displayed_tasks = []

        self.date_picker.setMinimumDate(QDate.currentDate())
        self.date_picker.setDate(QDate.currentDate())

        self.is_dark_mode = True
        ThemeManager.apply_dark(self)
        self.theme_toggle_button.setText("Light Mode 🌞")
        self.theme_toggle_button.clicked.connect(self.toggle_theme)

        self.smart_sort_checkbox.setChecked(True)
        self.smart_sort_checkbox.stateChanged.connect(lambda _: self.refresh_table())

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.add_button.clicked.connect(self.add_task)
        self.edit_button.clicked.connect(self.edit_task)
        self.delete_button.clicked.connect(self.delete_task)
        self.save_button.clicked.connect(self.save_tasks)
        self.load_button.clicked.connect(self.load_tasks_from_db_refresh)
        self.filter_button.clicked.connect(self.filter_tasks)
        self.table.cellClicked.connect(self.populate_inputs)

        self.refresh_table()

    def toggle_theme(self):
        if self.is_dark_mode:
            ThemeManager.apply_light(self)
            self.theme_toggle_button.setText("Dark Mode 🌙")
        else:
            ThemeManager.apply_dark(self)
            self.theme_toggle_button.setText("Light Mode 🌞")
        self.is_dark_mode = not self.is_dark_mode

    def refresh_table(self, tasks=None):
        if tasks is None:
            tasks = self.tasks

        if self.smart_sort_checkbox.isChecked():
            sorted_tasks = sorted(tasks, key=lambda t: (t.completed, -compute_urgency(t)[0], -compute_urgency(t)[1]))
        else:
            sorted_tasks = sorted(tasks, key=lambda t: (t.completed,))

        self.displayed_tasks = sorted_tasks
        self.table.setRowCount(0)

        for task in sorted_tasks:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)

            items = [
                QTableWidgetItem(task.title),
                QTableWidgetItem(task.due_date),
                QTableWidgetItem(task.priority.value),
                QTableWidgetItem(task.tags),
                QTableWidgetItem("Yes" if task.completed else "No")
            ]

            if task.completed:
                for item in items:
                    font = item.font()
                    font.setStrikeOut(True)
                    item.setFont(font)
                    item.setForeground(QBrush(QColor("gray")))

            for col, item in enumerate(items):
                self.table.setItem(row_position, col, item)

    def get_task_from_inputs(self):
        return Task(
            self.title_input.text(),
            self.date_picker.date().toString("MM/dd/yyyy"),
            Priority(self.priority_input.currentText()),
            self.tags_input.text(),
            self.completed_input.isChecked()
        )

    def add_task(self):
        if self.date_picker.date() < QDate.currentDate():
            QMessageBox.warning(self, "Invalid Date", "Please choose a future date.")
            return

        task = self.get_task_from_inputs()
        if task.title.strip() == "":
            QMessageBox.warning(self, "Input Error", "Task title cannot be empty.")
            return

        if any(t.title == task.title and t.due_date == task.due_date for t in self.tasks):
            QMessageBox.warning(self, "Duplicate Task", "This task already exists.")
            return

        self.tasks.append(task)
        self.refresh_table()
        self.clear_inputs()

    def edit_task(self):
        row = self.table.currentRow()
        if 0 <= row < len(self.displayed_tasks):
            original_task = self.displayed_tasks[row]
            updated_task = self.get_task_from_inputs()

            # Update in memory
            for i, t in enumerate(self.tasks):
                if t.title == original_task.title and t.due_date == original_task.due_date:
                    self.tasks[i] = updated_task
                    break

            # Check if original_task exists in DB
            from db import task_exists_in_db
            if task_exists_in_db(original_task):
                update_task_in_db(original_task, updated_task)

            self.load_tasks_from_db_refresh()
            self.clear_inputs()


    def delete_task(self):
        row = self.table.currentRow()
        if 0 <= row < len(self.displayed_tasks):
            task_to_delete = self.displayed_tasks[row]
            # Always attempt to delete from DB
            delete_task_from_db(task_to_delete)
            # Also remove from in-memory list
            self.tasks = [t for t in self.tasks if not (t.title == task_to_delete.title and t.due_date == task_to_delete.due_date)]
            self.load_tasks_from_db_refresh()
            self.clear_inputs()


    def filter_tasks(self):
        keyword = self.search_input.text().lower()
        filtered = [
            task for task in self.tasks if
            keyword in task.title.lower() or
            keyword in task.tags.lower() or
            keyword in task.priority.value.lower()
        ]
        self.refresh_table(filtered)

    def populate_inputs(self, row, _):
        if 0 <= row < len(self.displayed_tasks):
            task = self.displayed_tasks[row]
            self.title_input.setText(task.title)
            self.date_picker.setDate(QDate.fromString(task.due_date, "MM/dd/yyyy"))
            self.priority_input.setCurrentText(task.priority.value)
            self.tags_input.setText(task.tags)
            self.completed_input.setChecked(task.completed)

    def clear_inputs(self):
        self.title_input.clear()
        self.date_picker.setDate(QDate.currentDate())
        self.priority_input.setCurrentIndex(0)
        self.tags_input.clear()
        self.completed_input.setChecked(False)

    def load_tasks_from_db_refresh(self):
        self.tasks = load_tasks_from_db()
        self.refresh_table()

    def save_tasks(self):
        save_tasks_to_db(self.tasks)
        QMessageBox.information(self, "Saved", "Tasks saved to database.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec_())
