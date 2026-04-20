from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from app.models.dashboard import DashboardRepository
from app.utils.helpers import format_date


class StatCard(QFrame):
    def __init__(self, title: str, accent: str, parent=None):
        super().__init__(parent)
        self.setObjectName("statCard")
        self.setProperty("accent", accent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(118)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)
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
        layout.setSpacing(18)

        hero = QFrame()
        hero.setObjectName("dashboardHero")
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(24, 22, 24, 22)
        hero_layout.setSpacing(4)

        title = QLabel("Dashboard")
        title.setObjectName("dashboardTitle")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)

        subtitle = QLabel("Track students, courses, enrollments, and recent grading activity from one place.")
        subtitle.setObjectName("dashboardSubtitle")
        subtitle.setWordWrap(True)

        hero_layout.addWidget(title)
        hero_layout.addWidget(subtitle)
        layout.addWidget(hero)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(16)

        self._card_students = StatCard("Total Students", "sage")
        self._card_courses = StatCard("Total Courses", "sand")
        self._card_enrollments = StatCard("Total Enrollments", "clay")
        self._card_avg_grade = StatCard("Average Grade", "mist")

        for card in (self._card_students, self._card_courses, self._card_enrollments, self._card_avg_grade):
            cards_row.addWidget(card)

        layout.addLayout(cards_row)

        table_card = QFrame()
        table_card.setObjectName("tableCard")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(18, 18, 18, 18)
        table_layout.setSpacing(12)

        recent_label = QLabel("Recent Grades")
        recent_label.setObjectName("sectionTitle")
        recent_font = QFont()
        recent_font.setPointSize(13)
        recent_font.setBold(True)
        recent_label.setFont(recent_font)

        recent_subtitle = QLabel("Latest 10 graded records")
        recent_subtitle.setObjectName("sectionSubtitle")

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

        table_layout.addWidget(recent_label)
        table_layout.addWidget(recent_subtitle)
        table_layout.addWidget(self._table)
        layout.addWidget(table_card)

    def refresh(self):
        stats = DashboardRepository().get_stats()

        self._card_students.set_value(str(stats.total_students))
        self._card_courses.set_value(str(stats.total_courses))
        self._card_enrollments.set_value(str(stats.total_enrollments))
        self._card_avg_grade.set_value(stats.avg_grade)

        self._table.setRowCount(len(stats.recent_grades))
        for row_idx, row in enumerate(stats.recent_grades):
            self._table.setItem(row_idx, 0, QTableWidgetItem(str(row["student_name"])))
            self._table.setItem(row_idx, 1, QTableWidgetItem(str(row["course_name"])))
            self._table.setItem(row_idx, 2, QTableWidgetItem(f"{row['grade']:.1f}"))
            self._table.setItem(row_idx, 3, QTableWidgetItem(str(row["letter_grade"])))
            self._table.setItem(row_idx, 4, QTableWidgetItem(format_date(str(row["graded_at"])) if row["graded_at"] else ""))
