from app.models.course import Course, CourseRepository
from app.utils.validators import validate_course


class CourseController:
    def __init__(self):
        self._repo = CourseRepository()

    def create_course(self, data: dict) -> tuple[bool, str | Course]:
        errors = validate_course(data)
        if errors:
            return False, "\n".join(errors)
        try:
            course = Course(
                id=None,
                code=data["code"].strip().upper(),
                name=data["name"].strip(),
                description=(data.get("description") or "").strip() or None,
                credits=int(data["credits"]),
            )
            created = self._repo.create(course)
            return True, created
        except Exception as e:
            msg = str(e)
            if "UNIQUE" in msg.upper():
                return False, "A course with that code already exists."
            return False, f"Database error: {msg}"

    def update_course(self, course_id: int, data: dict) -> tuple[bool, str | Course]:
        errors = validate_course(data)
        if errors:
            return False, "\n".join(errors)
        try:
            course = Course(
                id=course_id,
                code=data["code"].strip().upper(),
                name=data["name"].strip(),
                description=(data.get("description") or "").strip() or None,
                credits=int(data["credits"]),
            )
            updated = self._repo.update(course)
            return True, updated
        except Exception as e:
            msg = str(e)
            if "UNIQUE" in msg.upper():
                return False, "A course with that code already exists."
            return False, f"Database error: {msg}"

    def delete_course(self, course_id: int) -> tuple[bool, str]:
        try:
            self._repo.delete(course_id)
            return True, "Course deleted successfully."
        except Exception as e:
            return False, f"Database error: {str(e)}"
