from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox,
    QDoubleSpinBox, QTextEdit, QLabel, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont

from app.models.enrollment import EnrollmentRepository
from app.models.grade import Grade, GradeRepository
from app.models.student import StudentRepository
from app.models.course import CourseRepository
from app.controllers.grade_controller import GradeController
from app.utils.helpers import numeric_to_letter


class GradeForm(QDialog):
    saved = pyqtSignal()

    def __init__(self, grade: Grade | None = None, parent=None):
        super().__init__(parent)
        self._grade = grade
        self._controller = GradeController()
        self._enrollment_repo = EnrollmentRepository()
        self._student_repo = StudentRepository()
        self._course_repo = CourseRepository()
        self.setWindowTitle("Edit Grade" if grade else "Add Grade")
        self.setMinimumWidth(440)
        self.setModal(True)
        self._build_ui()
        if grade:
            self._populate(grade)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("Edit Grade" if self._grade else "Add Grade")
        f = QFont()
        f.setPointSize(14)
        f.setBold(True)
        title.setFont(f)
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(8)

        # Enrollment combo
        self._enrollment_combo = QComboBox()
        self._enrollment_ids: list[int] = []
        enrollments = self._enrollment_repo.get_all_with_names()
        for enr in enrollments:
            label = f"{enr['student_name']} — {enr['course_display_name']}"
            self._enrollment_combo.addItem(label)
            self._enrollment_ids.append(enr["id"])

        if self._grade:
            self._enrollment_combo.setEnabled(False)

        form.addRow("Enrollment *", self._enrollment_combo)

        # Score
        self._score_spin = QDoubleSpinBox()
        self._score_spin.setRange(0.0, 100.0)
        self._score_spin.setDecimals(1)
        self._score_spin.setSingleStep(0.5)
        self._score_spin.setValue(75.0)
        self._score_spin.valueChanged.connect(self._update_letter)
        form.addRow("Grade (0–100) *", self._score_spin)

        # Letter grade preview
        self._letter_label = QLabel(numeric_to_letter(75.0))
        self._letter_label.setObjectName("letterGradePreview")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self._letter_label.setFont(font)
        form.addRow("Letter Grade", self._letter_label)

        # Notes
        self._notes = QTextEdit()
        self._notes.setPlaceholderText("Optional notes...")
        self._notes.setFixedHeight(70)
        form.addRow("Notes", self._notes)

        self._err_label = QLabel("")
        self._err_label.setObjectName("errorLabel")
        self._err_label.setWordWrap(True)
        form.addRow("", self._err_label)

        layout.addLayout(form)

        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self._submit)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def _update_letter(self, value: float):
        self._letter_label.setText(numeric_to_letter(value))

    def _populate(self, grade: Grade):
        # Select matching enrollment in combo
        for i, eid in enumerate(self._enrollment_ids):
            if eid == grade.enrollment_id:
                self._enrollment_combo.setCurrentIndex(i)
                break
        self._score_spin.setValue(grade.grade)
        self._notes.setPlainText(grade.notes or "")

    def _submit(self):
        self._err_label.setText("")
        score = self._score_spin.value()
        notes = self._notes.toPlainText()

        if self._grade:
            ok, result = self._controller.update_grade(self._grade.id, score, notes)
        else:
            if not self._enrollment_ids:
                self._err_label.setText("No enrollments available.")
                return
            enrollment_id = self._enrollment_ids[self._enrollment_combo.currentIndex()]
            ok, result = self._controller.add_grade(enrollment_id, score, notes)

        if ok:
            self.saved.emit()
            self.accept()
        else:
            self._err_label.setText(str(result))
