from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from app.models.enrollment import EnrollmentRepository
from app.controllers.enrollment_controller import EnrollmentController
from app.utils.helpers import format_date
from app.views.enrollments.enrollment_form import EnrollmentForm


class EnrollmentListView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._repo = EnrollmentRepository()
        self._controller = EnrollmentController()
        self._rows: list[dict] = []
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("Enrollments")
        f = QFont()
        f.setPointSize(18)
        f.setBold(True)
        title.setFont(f)
        layout.addWidget(title)

        toolbar = QHBoxLayout()
        self._btn_add = QPushButton("Add Enrollment")
        self._btn_add.setObjectName("primaryButton")
        self._btn_add.clicked.connect(self._add_enrollment)
        self._btn_delete = QPushButton("Delete")
        self._btn_delete.setObjectName("dangerButton")
        self._btn_delete.clicked.connect(self._delete_enrollment)
        toolbar.addStretch()
        toolbar.addWidget(self._btn_add)
        toolbar.addWidget(self._btn_delete)
        layout.addLayout(toolbar)

        self._table = QTableWidget()
        self._table.setColumnCount(3)
        self._table.setHorizontalHeaderLabels(["Student Name", "Course", "Enrolled Date"])
        self._table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._table.setSortingEnabled(True)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setAlternatingRowColors(True)
        self._table.verticalHeader().setVisible(False)
        layout.addWidget(self._table)

    def _load_data(self):
        self._rows = self._repo.get_all_with_names()
        self._table.setRowCount(len(self._rows))
        self._table.setSortingEnabled(False)
        for i, row in enumerate(self._rows):
            name_item = QTableWidgetItem(str(row["student_name"]))
            name_item.setData(Qt.ItemDataRole.UserRole, row["id"])
            self._table.setItem(i, 0, name_item)
            self._table.setItem(i, 1, QTableWidgetItem(str(row["course_display_name"])))
            self._table.setItem(i, 2, QTableWidgetItem(format_date(str(row["enrolled_at"])) if row["enrolled_at"] else ""))
        self._table.setSortingEnabled(True)
        self._table.sortItems(0, Qt.SortOrder.AscendingOrder)

    def _selected_enrollment_id(self) -> int | None:
        row = self._table.currentRow()
        if row < 0:
            return None
        name_item = self._table.item(row, 0)
        if name_item is None:
            return None
        return name_item.data(Qt.ItemDataRole.UserRole)

    def _add_enrollment(self):
        dlg = EnrollmentForm(parent=self)
        dlg.saved.connect(self._load_data)
        dlg.exec()

    def _delete_enrollment(self):
        enrollment_id = self._selected_enrollment_id()
        if enrollment_id is None:
            QMessageBox.information(self, "No selection", "Please select an enrollment to delete.")
            return
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            "Remove this enrollment? Grades for this enrollment will also be deleted.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            ok, msg = self._controller.unenroll(enrollment_id)
            if ok:
                self._load_data()
            else:
                QMessageBox.critical(self, "Error", msg)
