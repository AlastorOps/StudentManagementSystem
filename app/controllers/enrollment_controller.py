from app.models.enrollment import Enrollment, EnrollmentRepository


class EnrollmentController:
    def __init__(self):
        self._repo = EnrollmentRepository()

    def enroll_student(self, student_id: int, course_id: int) -> tuple[bool, str]:
        try:
            enrollment = Enrollment(id=None, student_id=student_id, course_id=course_id)
            self._repo.create(enrollment)
            return True, "Student enrolled successfully."
        except Exception as e:
            msg = str(e)
            if "UNIQUE" in msg.upper():
                return False, "This student is already enrolled in that course."
            return False, f"Database error: {msg}"

    def unenroll(self, enrollment_id: int) -> tuple[bool, str]:
        try:
            self._repo.delete(enrollment_id)
            return True, "Enrollment removed successfully."
        except Exception as e:
            return False, f"Database error: {str(e)}"
