from app.models.student import Student, StudentRepository
from app.utils.validators import validate_student


class StudentController:
    def __init__(self):
        self._repo = StudentRepository()

    def create_student(self, data: dict) -> tuple[bool, str | Student]:
        errors = validate_student(data)
        if errors:
            return False, "\n".join(errors)
        try:
            student = Student(
                id=None,
                first_name=data["first_name"].strip(),
                last_name=data["last_name"].strip(),
                email=data["email"].strip(),
                phone=(data.get("phone") or "").strip() or None,
                date_of_birth=data.get("date_of_birth") or None,
            )
            created = self._repo.create(student)
            return True, created
        except Exception as e:
            msg = str(e)
            if "UNIQUE" in msg.upper():
                return False, "A student with that email already exists."
            return False, f"Database error: {msg}"

    def update_student(self, student_id: int, data: dict) -> tuple[bool, str | Student]:
        errors = validate_student(data)
        if errors:
            return False, "\n".join(errors)
        try:
            student = Student(
                id=student_id,
                first_name=data["first_name"].strip(),
                last_name=data["last_name"].strip(),
                email=data["email"].strip(),
                phone=(data.get("phone") or "").strip() or None,
                date_of_birth=data.get("date_of_birth") or None,
            )
            updated = self._repo.update(student)
            return True, updated
        except Exception as e:
            msg = str(e)
            if "UNIQUE" in msg.upper():
                return False, "A student with that email already exists."
            return False, f"Database error: {msg}"

    def delete_student(self, student_id: int) -> tuple[bool, str]:
        try:
            self._repo.delete(student_id)
            return True, "Student deleted successfully."
        except Exception as e:
            return False, f"Database error: {str(e)}"
