from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox,
    QLabel, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont

from app.models.student import StudentRepository
from app.models.course import CourseRepository
from app.controllers.enrollment_controller import EnrollmentController


class EnrollmentForm(QDialog):
    saved = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._controller = EnrollmentController()
        self._student_repo = StudentRepository()
        self._course_repo = CourseRepository()
        self.setWindowTitle("Enroll Student")
        self.setMinimumWidth(400)
        self.setModal(True)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("Enroll Student in Course")
        f = QFont()
        f.setPointSize(14)
        f.setBold(True)
        title.setFont(f)
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(8)

        self._student_combo = QComboBox()
        students = self._student_repo.get_all()
        self._student_ids = []
        for s in students:
            self._student_combo.addItem(s.full_name)
            self._student_ids.append(s.id)
        form.addRow("Student *", self._student_combo)

        self._course_combo = QComboBox()
        courses = self._course_repo.get_all()
        self._course_ids = []
        for c in courses:
            self._course_combo.addItem(c.display_name)
            self._course_ids.append(c.id)
        form.addRow("Course *", self._course_combo)

        self._err_label = QLabel("")
        self._err_label.setObjectName("errorLabel")
        self._err_label.setWordWrap(True)
        form.addRow("", self._err_label)

        layout.addLayout(form)

        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self._submit)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def _submit(self):
        self._err_label.setText("")
        if not self._student_ids or not self._course_ids:
            self._err_label.setText("No students or courses available.")
            return

        student_id = self._student_ids[self._student_combo.currentIndex()]
        course_id = self._course_ids[self._course_combo.currentIndex()]

        ok, msg = self._controller.enroll_student(student_id, course_id)
        if ok:
            self.saved.emit()
            self.accept()
        else:
            self._err_label.setText(msg)
