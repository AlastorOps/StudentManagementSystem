from app.models.grade import Grade, GradeRepository
from app.utils.validators import validate_grade
from app.utils.helpers import numeric_to_letter


class GradeController:
    def __init__(self):
        self._repo = GradeRepository()

    def add_grade(self, enrollment_id: int, score: float, notes: str = "") -> tuple[bool, str | Grade]:
        errors = validate_grade({"enrollment_id": enrollment_id, "grade": score})
        if errors:
            return False, "\n".join(errors)
        try:
            grade = Grade(
                id=None,
                enrollment_id=enrollment_id,
                grade=score,
                letter_grade=numeric_to_letter(score),
                notes=notes.strip() or None,
            )
            created = self._repo.create(grade)
            return True, created
        except Exception as e:
            msg = str(e)
            if "UNIQUE" in msg.upper():
                return False, "A grade already exists for this enrollment."
            return False, f"Database error: {msg}"

    def update_grade(self, grade_id: int, score: float, notes: str = "") -> tuple[bool, str | Grade]:
        errors = validate_grade({"enrollment_id": 1, "grade": score})  # enrollment_id placeholder for validation
        if errors:
            return False, "\n".join(errors)
        try:
            existing = self._repo.get_by_id(grade_id)
            if existing is None:
                return False, "Grade not found."
            existing.grade = score
            existing.letter_grade = numeric_to_letter(score)
            existing.notes = notes.strip() or None
            updated = self._repo.update(existing)
            return True, updated
        except Exception as e:
            return False, f"Database error: {str(e)}"

    def delete_grade(self, grade_id: int) -> tuple[bool, str]:
        try:
            self._repo.delete(grade_id)
            return True, "Grade deleted successfully."
        except Exception as e:
            return False, f"Database error: {str(e)}"
