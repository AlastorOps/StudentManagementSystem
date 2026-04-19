from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class _NumericItem(QTableWidgetItem):
    """QTableWidgetItem that sorts by numeric value instead of text."""
    def __lt__(self, other: QTableWidgetItem) -> bool:
        try:
            return int(self.text()) < int(other.text())
        except ValueError:
            return super().__lt__(other)

from app.models.student import StudentRepository, Student
from app.controllers.student_controller import StudentController
from app.utils.helpers import format_date
from app.utils.exporters import export_students_to_csv
from app.views.students.student_form import StudentForm
from app.views.students.student_detail import StudentDetail


class StudentListView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._repo = StudentRepository()
        self._controller = StudentController()
        self._students: list[Student] = []
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("Students")
        f = QFont()
        f.setPointSize(18)
        f.setBold(True)
        title.setFont(f)
        layout.addWidget(title)

        # Toolbar row
        toolbar = QHBoxLayout()
        self._search = QLineEdit()
        self._search.setPlaceholderText("Search by name or email...")
        self._search.textChanged.connect(self._on_search)
        toolbar.addWidget(self._search)

        self._btn_add = QPushButton("Add Student")
        self._btn_add.setObjectName("primaryButton")
        self._btn_add.clicked.connect(self._add_student)

        self._btn_edit = QPushButton("Edit")
        self._btn_edit.clicked.connect(self._edit_student)

        self._btn_delete = QPushButton("Delete")
        self._btn_delete.setObjectName("dangerButton")
        self._btn_delete.clicked.connect(self._delete_student)

        self._btn_detail = QPushButton("View Detail")
        self._btn_detail.clicked.connect(self._view_detail)

        self._btn_export = QPushButton("Export to CSV")
        self._btn_export.clicked.connect(self._export_csv)

        for btn in (self._btn_add, self._btn_edit, self._btn_delete, self._btn_detail, self._btn_export):
            toolbar.addWidget(btn)

        layout.addLayout(toolbar)

        # Table
        self._table = QTableWidget()
        self._table.setColumnCount(6)
        self._table.setHorizontalHeaderLabels(["ID", "Full Name", "Email", "Phone", "Date of Birth", "Created"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.setSortingEnabled(True)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setAlternatingRowColors(True)
        self._table.verticalHeader().setVisible(False)
        self._table.doubleClicked.connect(self._view_detail)
        layout.addWidget(self._table)

    def _load_data(self, students: list[Student] | None = None):
        if students is None:
            students = self._repo.get_all()
        self._students = students
        self._table.setSortingEnabled(False)
        self._table.setRowCount(len(students))
        for i, s in enumerate(students):
            self._table.setItem(i, 0, _NumericItem(str(s.id)))
            self._table.setItem(i, 1, QTableWidgetItem(s.full_name))
            self._table.setItem(i, 2, QTableWidgetItem(s.email))
            self._table.setItem(i, 3, QTableWidgetItem(s.phone or ""))
            self._table.setItem(i, 4, QTableWidgetItem(format_date(s.date_of_birth) if s.date_of_birth else ""))
            self._table.setItem(i, 5, QTableWidgetItem(format_date(s.created_at) if s.created_at else ""))
        self._table.setSortingEnabled(True)
        self._table.sortItems(0, Qt.SortOrder.AscendingOrder)

    def _on_search(self, text: str):
        if text.strip():
            self._load_data(self._repo.search(text.strip()))
        else:
            self._load_data()

    def _selected_student(self) -> Student | None:
        row = self._table.currentRow()
        if row < 0 or row >= len(self._students):
            return None
        return self._students[row]

    def _add_student(self):
        dlg = StudentForm(parent=self)
        dlg.saved.connect(lambda: self._load_data())
        dlg.exec()

    def _edit_student(self):
        student = self._selected_student()
        if not student:
            QMessageBox.information(self, "No selection", "Please select a student to edit.")
            return
        dlg = StudentForm(student=student, parent=self)
        dlg.saved.connect(lambda: self._load_data())
        dlg.exec()

    def _delete_student(self):
        student = self._selected_student()
        if not student:
            QMessageBox.information(self, "No selection", "Please select a student to delete.")
            return
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete student '{student.full_name}'? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            ok, msg = self._controller.delete_student(student.id)
            if ok:
                self._load_data()
            else:
                QMessageBox.critical(self, "Error", msg)

    def _view_detail(self):
        student = self._selected_student()
        if not student:
            QMessageBox.information(self, "No selection", "Please select a student to view.")
            return
        dlg = StudentDetail(student=student, parent=self)
        dlg.exec()

    def _export_csv(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Export Students", "students.csv", "CSV Files (*.csv)")
        if filepath:
            students = self._repo.get_all()
            ok = export_students_to_csv(students, filepath)
            if ok:
                QMessageBox.information(self, "Exported", f"Students exported to:\n{filepath}")
            else:
                QMessageBox.critical(self, "Error", "Failed to export students.")
