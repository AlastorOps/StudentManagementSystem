from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QDateEdit, QLabel, QPushButton, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal, QRegularExpression
from PyQt6.QtGui import QFont, QRegularExpressionValidator

from app.models.student import Student
from app.controllers.student_controller import StudentController


class StudentForm(QDialog):
    saved = pyqtSignal()

    def __init__(self, student: Student | None = None, parent=None):
        super().__init__(parent)
        self._student = student
        self._controller = StudentController()
        self._error_labels: dict[str, QLabel] = {}
        self.setWindowTitle("Edit Student" if student else "Add Student")
        self.setMinimumWidth(420)
        self.setModal(True)
        self._build_ui()
        if student:
            self._populate(student)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("Edit Student" if self._student else "Add Student")
        f = QFont()
        f.setPointSize(14)
        f.setBold(True)
        title.setFont(f)
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(8)

        name_validator = QRegularExpressionValidator(QRegularExpression(r"[A-Za-z\s\-']*"))
        phone_validator = QRegularExpressionValidator(QRegularExpression(r"[\d\+\-\s()]*"))

        self._first_name = QLineEdit()
        self._first_name.setPlaceholderText("First name")
        self._first_name.setValidator(name_validator)
        self._err_first_name = self._make_error_label()
        form.addRow("First Name *", self._first_name)
        form.addRow("", self._err_first_name)

        self._last_name = QLineEdit()
        self._last_name.setPlaceholderText("Last name")
        self._last_name.setValidator(name_validator)
        self._err_last_name = self._make_error_label()
        form.addRow("Last Name *", self._last_name)
        form.addRow("", self._err_last_name)

        self._email = QLineEdit()
        self._email.setPlaceholderText("email@example.com")
        self._err_email = self._make_error_label()
        form.addRow("Email *", self._email)
        form.addRow("", self._err_email)

        self._phone = QLineEdit()
        self._phone.setPlaceholderText("0123456789")
        self._phone.setValidator(phone_validator)
        self._err_phone = self._make_error_label()
        form.addRow("Phone", self._phone)
        form.addRow("", self._err_phone)

        self._dob = QDateEdit()
        self._dob.setCalendarPopup(True)
        self._dob.setDisplayFormat("yyyy-MM-dd")
        self._dob.setDate(QDate.currentDate())
        self._dob.setSpecialValueText(" ")
        self._dob.setMinimumDate(QDate(1900, 1, 1))
        form.addRow("Date of Birth", self._dob)

        layout.addLayout(form)

        # Buttons
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self._submit)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def _make_error_label(self) -> QLabel:
        lbl = QLabel("")
        lbl.setObjectName("errorLabel")
        lbl.setWordWrap(True)
        return lbl

    def _populate(self, student: Student):
        self._first_name.setText(student.first_name)
        self._last_name.setText(student.last_name)
        self._email.setText(student.email)
        self._phone.setText(student.phone or "")
        if student.date_of_birth:
            try:
                self._dob.setDate(QDate.fromString(student.date_of_birth[:10], "yyyy-MM-dd"))
            except Exception:
                pass

    def _clear_errors(self):
        for lbl in [self._err_first_name, self._err_last_name, self._err_email, self._err_phone]:
            lbl.setText("")

    def _submit(self):
        self._clear_errors()
        dob_text = self._dob.date().toString("yyyy-MM-dd")
        data = {
            "first_name": self._first_name.text(),
            "last_name": self._last_name.text(),
            "email": self._email.text(),
            "phone": self._phone.text(),
            "date_of_birth": dob_text,
        }

        if self._student:
            ok, result = self._controller.update_student(self._student.id, data)
        else:
            ok, result = self._controller.create_student(data)

        if ok:
            self.saved.emit()
            self.accept()
        else:
            # Try to map errors to fields
            error_msg = str(result)
            if "first name" in error_msg.lower():
                self._err_first_name.setText(error_msg)
            elif "last name" in error_msg.lower():
                self._err_last_name.setText(error_msg)
            elif "email" in error_msg.lower():
                self._err_email.setText(error_msg)
            elif "phone" in error_msg.lower():
                self._err_phone.setText(error_msg)
            else:
                QMessageBox.critical(self, "Error", error_msg)
