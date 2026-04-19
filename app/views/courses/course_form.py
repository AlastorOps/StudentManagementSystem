from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QSpinBox, QTextEdit, QLabel, QPushButton,
    QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont

from app.models.course import Course
from app.controllers.course_controller import CourseController


class CourseForm(QDialog):
    saved = pyqtSignal()

    def __init__(self, course: Course | None = None, parent=None):
        super().__init__(parent)
        self._course = course
        self._controller = CourseController()
        self.setWindowTitle("Edit Course" if course else "Add Course")
        self.setMinimumWidth(420)
        self.setModal(True)
        self._build_ui()
        if course:
            self._populate(course)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("Edit Course" if self._course else "Add Course")
        f = QFont()
        f.setPointSize(14)
        f.setBold(True)
        title.setFont(f)
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(8)

        self._code = QLineEdit()
        self._code.setPlaceholderText("e.g. CS101")
        self._code.setMaxLength(10)
        self._err_code = self._make_error()
        form.addRow("Code *", self._code)
        form.addRow("", self._err_code)

        self._name = QLineEdit()
        self._name.setPlaceholderText("Course name")
        self._err_name = self._make_error()
        form.addRow("Name *", self._name)
        form.addRow("", self._err_name)

        self._description = QTextEdit()
        self._description.setPlaceholderText("Optional description...")
        self._description.setFixedHeight(80)
        form.addRow("Description", self._description)

        self._credits = QSpinBox()
        self._credits.setRange(1, 10)
        self._credits.setValue(3)
        self._err_credits = self._make_error()
        form.addRow("Credits *", self._credits)
        form.addRow("", self._err_credits)

        layout.addLayout(form)

        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btn_box.accepted.connect(self._submit)
        btn_box.rejected.connect(self.reject)
        layout.addWidget(btn_box)

    def _make_error(self) -> QLabel:
        lbl = QLabel("")
        lbl.setObjectName("errorLabel")
        lbl.setWordWrap(True)
        return lbl

    def _populate(self, course: Course):
        self._code.setText(course.code)
        self._name.setText(course.name)
        self._description.setPlainText(course.description or "")
        self._credits.setValue(course.credits)

    def _clear_errors(self):
        for lbl in [self._err_code, self._err_name, self._err_credits]:
            lbl.setText("")

    def _submit(self):
        self._clear_errors()
        data = {
            "code": self._code.text(),
            "name": self._name.text(),
            "description": self._description.toPlainText(),
            "credits": self._credits.value(),
        }

        if self._course:
            ok, result = self._controller.update_course(self._course.id, data)
        else:
            ok, result = self._controller.create_course(data)

        if ok:
            self.saved.emit()
            self.accept()
        else:
            error_msg = str(result)
            if "code" in error_msg.lower():
                self._err_code.setText(error_msg)
            elif "name" in error_msg.lower():
                self._err_name.setText(error_msg)
            elif "credits" in error_msg.lower():
                self._err_credits.setText(error_msg)
            else:
                QMessageBox.critical(self, "Error", error_msg)
