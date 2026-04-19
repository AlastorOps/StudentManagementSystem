from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from app.models.student import Student, StudentRepository
from app.models.enrollment import EnrollmentRepository
from app.models.grade import GradeRepository
from app.models.course import CourseRepository
from app.utils.helpers import format_date


class StudentDetail(QDialog):
    def __init__(self, student: Student, parent=None):
        super().__init__(parent)
        self._student = student
        self.setWindowTitle(f"Student Detail — {student.full_name}")
        self.setMinimumSize(560, 420)
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Title
        title = QLabel(self._student.full_name)
        f = QFont()
        f.setPointSize(16)
        f.setBold(True)
        title.setFont(f)
        layout.addWidget(title)

        # Info
        form = QFormLayout()
        form.setSpacing(6)
        s = self._student

        def info_row(label, value):
            val_lbl = QLabel(value or "—")
            val_lbl.setWordWrap(True)
            form.addRow(f"<b>{label}</b>", val_lbl)

        info_row("Email", s.email)
        info_row("Phone", s.phone)
        info_row("Date of Birth", format_date(s.date_of_birth) if s.date_of_birth else None)
        info_row("Registered", format_date(s.created_at) if s.created_at else None)
        layout.addLayout(form)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(sep)

        enrollments_label = QLabel("Enrollments & Grades")
        ef = QFont()
        ef.setPointSize(12)
        ef.setBold(True)
        enrollments_label.setFont(ef)
        layout.addWidget(enrollments_label)

        # Enrollments table
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Course", "Enrolled", "Grade", "Letter"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)

        enrollment_repo = EnrollmentRepository()
        grade_repo = GradeRepository()
        course_repo = CourseRepository()

        enrollments = enrollment_repo.get_by_student(self._student.id)
        table.setRowCount(len(enrollments))
        for i, enr in enumerate(enrollments):
            course = course_repo.get_by_id(enr.course_id)
            grade = grade_repo.get_by_enrollment(enr.id)
            table.setItem(i, 0, QTableWidgetItem(course.display_name if course else "Unknown"))
            table.setItem(i, 1, QTableWidgetItem(format_date(enr.enrolled_at) if enr.enrolled_at else ""))
            table.setItem(i, 2, QTableWidgetItem(f"{grade.grade:.1f}" if grade else "Not graded"))
            table.setItem(i, 3, QTableWidgetItem(grade.letter_grade if grade else ""))

        layout.addWidget(table)

        close_btn = QPushButton("Close")
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)
