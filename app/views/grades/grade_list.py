from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from app.models.grade import GradeRepository, Grade
from app.controllers.grade_controller import GradeController
from app.utils.helpers import format_date
from app.views.grades.grade_form import GradeForm


class GradeListView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._repo = GradeRepository()
        self._controller = GradeController()
        self._rows: list[dict] = []
        self._grades: list[Grade] = []
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("Grades")
        f = QFont()
        f.setPointSize(18)
        f.setBold(True)
        title.setFont(f)
        layout.addWidget(title)

        toolbar = QHBoxLayout()
        self._btn_add = QPushButton("Add Grade")
        self._btn_add.setObjectName("primaryButton")
        self._btn_add.clicked.connect(self._add_grade)
        self._btn_edit = QPushButton("Edit")
        self._btn_edit.clicked.connect(self._edit_grade)
        self._btn_delete = QPushButton("Delete")
        self._btn_delete.setObjectName("dangerButton")
        self._btn_delete.clicked.connect(self._delete_grade)
        toolbar.addStretch()
        for btn in (self._btn_add, self._btn_edit, self._btn_delete):
            toolbar.addWidget(btn)
        layout.addLayout(toolbar)

        self._table = QTableWidget()
        self._table.setColumnCount(6)
        self._table.setHorizontalHeaderLabels(["Student", "Course", "Grade", "Letter", "Date", "Notes"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.setSortingEnabled(True)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setAlternatingRowColors(True)
        self._table.verticalHeader().setVisible(False)
        layout.addWidget(self._table)

    def _load_data(self):
        self._rows = self._repo.get_all_with_details()
        self._grades = self._repo.get_all()
        self._table.setRowCount(len(self._rows))
        self._table.setSortingEnabled(False)
        for i, row in enumerate(self._rows):
            self._table.setItem(i, 0, QTableWidgetItem(str(row["student_name"])))
            self._table.setItem(i, 1, QTableWidgetItem(str(row["course_display_name"])))
            self._table.setItem(i, 2, QTableWidgetItem(f"{row['grade']:.1f}"))
            self._table.setItem(i, 3, QTableWidgetItem(str(row["letter_grade"])))
            self._table.setItem(i, 4, QTableWidgetItem(format_date(str(row["graded_at"])) if row["graded_at"] else ""))
            self._table.setItem(i, 5, QTableWidgetItem(str(row["notes"] or "")))
        self._table.setSortingEnabled(True)
        self._table.sortItems(0, Qt.SortOrder.AscendingOrder)

    def _selected_grade(self) -> Grade | None:
        row = self._table.currentRow()
        if row < 0 or row >= len(self._grades):
            return None
        return self._grades[row]

    def _add_grade(self):
        dlg = GradeForm(parent=self)
        dlg.saved.connect(self._load_data)
        dlg.exec()

    def _edit_grade(self):
        grade = self._selected_grade()
        if not grade:
            QMessageBox.information(self, "No selection", "Please select a grade to edit.")
            return
        dlg = GradeForm(grade=grade, parent=self)
        dlg.saved.connect(self._load_data)
        dlg.exec()

    def _delete_grade(self):
        grade = self._selected_grade()
        if not grade:
            QMessageBox.information(self, "No selection", "Please select a grade to delete.")
            return
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            "Delete this grade record? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            ok, msg = self._controller.delete_grade(grade.id)
            if ok:
                self._load_data()
            else:
                QMessageBox.critical(self, "Error", msg)
