class ThemeManager:
    LIGHT_THEME = """
    QWidget {
        background-color: #f5f5f5;
        color: #1a1a1a;
        font-size: 12pt;
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton, QToolButton {
        background-color: #ffffff;
        color: #333;
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 6px 10px;
    }
    QPushButton:hover, QToolButton:hover {
        background-color: #f0f0f0;
    }
    QLineEdit, QComboBox {
        background-color: #ffffff;
        color: #1a1a1a;
        border: 1px solid #ccc;
        padding: 4px;
        border-radius: 4px;
    }
    QCheckBox {
        padding-left: 4px;
    }
    QTableWidget {
        background-color: #ffffff;
        color: #1a1a1a;
        gridline-color: #ccc;
        border: 1px solid #ddd;
        selection-background-color: #e0e0e0;
    }
    QHeaderView::section {
        background-color: #eaeaea;
        color: #333;
        padding: 6px;
        border: 1px solid #ccc;
    }
    """

    DARK_THEME = """
    QWidget {
        background-color: #1f1f1f;
        color: #f0f0f0;
        font-size: 12pt;
        font-family: 'Segoe UI', sans-serif;
    }
    QPushButton, QToolButton {
        background-color: #2e2e2e;
        color: #eaeaea;
        border: 1px solid #555;
        border-radius: 6px;
        padding: 6px 10px;
    }
    QPushButton:hover, QToolButton:hover {
        background-color: #3a3a3a;
    }
    QLineEdit, QComboBox {
        background-color: #2a2a2a;
        color: #ffffff;
        border: 1px solid #555;
        padding: 4px;
        border-radius: 4px;
    }
    QCheckBox {
        padding-left: 4px;
        color: #e0e0e0;
    }
    QTableWidget {
        background-color: #1e1e1e;
        color: #ffffff;
        gridline-color: #444;
        border: 1px solid #444;
        selection-background-color: #3b3b3b;
    }
    QHeaderView::section {
        background-color: #333;
        color: #f0f0f0;
        padding: 6px;
        border: 1px solid #444;
    }
    QCalendarWidget {
        background-color: #2e2e2e;
        color: white;
        border: 1px solid #444;
        selection-background-color: #3b3b3b;
        selection-color: white;
    }
    QCalendarWidget QWidget#qt_calendar_navigationbar {
        background-color: #333;
        color: white;
    }
    QCalendarWidget QToolButton {
        background-color: #444;
        color: white;
        border: none;
        padding: 5px;
    }
    QCalendarWidget QToolButton:hover {
        background-color: #555;
    }
    QCalendarWidget QSpinBox {
        background-color: #2e2e2e;
        color: white;
        border: 1px solid #555;
    }
    QCalendarWidget QMenu {
        background-color: #2e2e2e;
        color: white;
    }
    QCalendarWidget QAbstractItemView {
        background-color: #2e2e2e;
        color: white;
        selection-background-color: #555;
        selection-color: white;
        gridline-color: #444;
    }
    """

    @staticmethod
    def apply_dark(widget):
        widget.setStyleSheet(ThemeManager.DARK_THEME)

    @staticmethod
    def apply_light(widget):
        widget.setStyleSheet(ThemeManager.LIGHT_THEME)
