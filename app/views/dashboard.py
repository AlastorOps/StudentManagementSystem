from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from app.database.connection import get_connection
from app.utils.helpers import format_date


class StatCard(QFrame):
    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(110)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._value_label = QLabel("0")
        self._value_label.setObjectName("statValue")
        self._value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_font = QFont()
        value_font.setPointSize(28)
        value_font.setBold(True)
        self._value_label.setFont(value_font)

        self._title_label = QLabel(title)
        self._title_label.setObjectName("statTitle")
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self._value_label)
        layout.addWidget(self._title_label)

    def set_value(self, value: str):
        self._value_label.setText(value)


class DashboardView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dashboardView")
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Title
        title = QLabel("Dashboard")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Stat cards row
        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        self._card_students = StatCard("Total Students")
        self._card_courses = StatCard("Total Courses")
        self._card_enrollments = StatCard("Total Enrollments")
        self._card_avg_grade = StatCard("Average Grade")

        for card in (self._card_students, self._card_courses, self._card_enrollments, self._card_avg_grade):
            cards_row.addWidget(card)

        layout.addLayout(cards_row)

        # Recent grades table
        recent_label = QLabel("Recent Grades (last 10)")
        recent_font = QFont()
        recent_font.setPointSize(13)
        recent_font.setBold(True)
        recent_label.setFont(recent_font)
        layout.addWidget(recent_label)

        self._table = QTableWidget()
        self._table.setObjectName("dashboardTable")
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels(["Student", "Course", "Score", "Grade", "Date"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.setSortingEnabled(True)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setAlternatingRowColors(True)
        self._table.verticalHeader().setVisible(False)
        layout.addWidget(self._table)

    def refresh(self):
        conn = get_connection()

        total_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        total_courses = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
        total_enrollments = conn.execute("SELECT COUNT(*) FROM enrollments").fetchone()[0]
        avg_row = conn.execute("SELECT AVG(grade) FROM grades").fetchone()[0]
        avg_grade = f"{avg_row:.1f}" if avg_row is not None else "N/A"

        self._card_students.set_value(str(total_students))
        self._card_courses.set_value(str(total_courses))
        self._card_enrollments.set_value(str(total_enrollments))
        self._card_avg_grade.set_value(avg_grade)

        # Recent grades
        rows = conn.execute(
            """
            SELECT
                s.first_name || ' ' || s.last_name AS student_name,
                c.code || ' — ' || c.name AS course_name,
                g.grade,
                g.letter_grade,
                g.graded_at
            FROM grades g
            JOIN enrollments e ON e.id = g.enrollment_id
            JOIN students s ON s.id = e.student_id
            JOIN courses c ON c.id = e.course_id
            ORDER BY g.graded_at DESC
            LIMIT 10
            """
        ).fetchall()

        self._table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            self._table.setItem(row_idx, 0, QTableWidgetItem(str(row[0])))
            self._table.setItem(row_idx, 1, QTableWidgetItem(str(row[1])))
            self._table.setItem(row_idx, 2, QTableWidgetItem(f"{row[2]:.1f}"))
            self._table.setItem(row_idx, 3, QTableWidgetItem(str(row[3])))
            self._table.setItem(row_idx, 4, QTableWidgetItem(format_date(str(row[4]))))
