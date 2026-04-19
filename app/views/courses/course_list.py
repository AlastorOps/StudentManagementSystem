from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from app.models.course import CourseRepository, Course
from app.controllers.course_controller import CourseController
from app.utils.helpers import format_date
from app.views.courses.course_form import CourseForm


class CourseListView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._repo = CourseRepository()
        self._controller = CourseController()
        self._courses: list[Course] = []
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("Courses")
        f = QFont()
        f.setPointSize(18)
        f.setBold(True)
        title.setFont(f)
        layout.addWidget(title)

        toolbar = QHBoxLayout()
        self._btn_add = QPushButton("Add Course")
        self._btn_add.setObjectName("primaryButton")
        self._btn_add.clicked.connect(self._add_course)
        self._btn_edit = QPushButton("Edit")
        self._btn_edit.clicked.connect(self._edit_course)
        self._btn_delete = QPushButton("Delete")
        self._btn_delete.setObjectName("dangerButton")
        self._btn_delete.clicked.connect(self._delete_course)
        toolbar.addStretch()
        for btn in (self._btn_add, self._btn_edit, self._btn_delete):
            toolbar.addWidget(btn)
        layout.addLayout(toolbar)

        self._table = QTableWidget()
        self._table.setColumnCount(5)
        self._table.setHorizontalHeaderLabels(["Code", "Name", "Credits", "Description", "Created"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.setSortingEnabled(True)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setAlternatingRowColors(True)
        self._table.verticalHeader().setVisible(False)
        layout.addWidget(self._table)

    def _load_data(self):
        self._courses = self._repo.get_all()
        self._table.setRowCount(len(self._courses))
        self._table.setSortingEnabled(False)
        for i, c in enumerate(self._courses):
            self._table.setItem(i, 0, QTableWidgetItem(c.code))
            self._table.setItem(i, 1, QTableWidgetItem(c.name))
            self._table.setItem(i, 2, QTableWidgetItem(str(c.credits)))
            self._table.setItem(i, 3, QTableWidgetItem(c.description or ""))
            self._table.setItem(i, 4, QTableWidgetItem(format_date(c.created_at) if c.created_at else ""))
        self._table.setSortingEnabled(True)
        self._table.sortItems(0, Qt.SortOrder.AscendingOrder)

    def _selected_course(self) -> Course | None:
        row = self._table.currentRow()
        if row < 0 or row >= len(self._courses):
            return None
        return self._courses[row]

    def _add_course(self):
        dlg = CourseForm(parent=self)
        dlg.saved.connect(self._load_data)
        dlg.exec()

    def _edit_course(self):
        course = self._selected_course()
        if not course:
            QMessageBox.information(self, "No selection", "Please select a course to edit.")
            return
        dlg = CourseForm(course=course, parent=self)
        dlg.saved.connect(self._load_data)
        dlg.exec()

    def _delete_course(self):
        course = self._selected_course()
        if not course:
            QMessageBox.information(self, "No selection", "Please select a course to delete.")
            return
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete course '{course.display_name}'? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            ok, msg = self._controller.delete_course(course.id)
            if ok:
                self._load_data()
            else:
                QMessageBox.critical(self, "Error", msg)
