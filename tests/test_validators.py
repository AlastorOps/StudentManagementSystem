import pytest
from app.utils.validators import validate_student, validate_course, validate_grade
from app.utils.helpers import numeric_to_letter


class TestValidateStudent:
    def test_missing_all_required_fields(self):
        errors = validate_student({})
        assert any("first name" in e.lower() for e in errors)
        assert any("last name" in e.lower() for e in errors)
        assert any("email" in e.lower() for e in errors)

    def test_missing_first_name(self):
        errors = validate_student({"first_name": "", "last_name": "Doe", "email": "j@example.com"})
        assert any("first name" in e.lower() for e in errors)

    def test_missing_last_name(self):
        errors = validate_student({"first_name": "John", "last_name": "", "email": "j@example.com"})
        assert any("last name" in e.lower() for e in errors)

    def test_missing_email(self):
        errors = validate_student({"first_name": "John", "last_name": "Doe", "email": ""})
        assert any("email" in e.lower() for e in errors)

    def test_invalid_email(self):
        errors = validate_student({"first_name": "John", "last_name": "Doe", "email": "not-an-email"})
        assert any("email" in e.lower() for e in errors)

    def test_invalid_phone(self):
        errors = validate_student({
            "first_name": "John", "last_name": "Doe",
            "email": "john@example.com", "phone": "abc123!!"
        })
        assert any("phone" in e.lower() for e in errors)

    def test_valid_phone(self):
        errors = validate_student({
            "first_name": "John", "last_name": "Doe",
            "email": "john@example.com", "phone": "+1 555-000-0000"
        })
        assert errors == []

    def test_valid_full_input(self):
        errors = validate_student({
            "first_name": "Jane", "last_name": "Smith",
            "email": "jane@example.com", "phone": "555 123 4567"
        })
        assert errors == []


class TestValidateCourse:
    def test_missing_code(self):
        errors = validate_course({"code": "", "name": "Math", "credits": 3})
        assert any("code" in e.lower() for e in errors)

    def test_code_too_long(self):
        errors = validate_course({"code": "ABCDEFGHIJK", "name": "Math", "credits": 3})
        assert any("code" in e.lower() for e in errors)

    def test_code_with_special_chars(self):
        errors = validate_course({"code": "CS-101", "name": "Math", "credits": 3})
        assert any("code" in e.lower() for e in errors)

    def test_missing_name(self):
        errors = validate_course({"code": "CS101", "name": "", "credits": 3})
        assert any("name" in e.lower() for e in errors)

    def test_credits_too_low(self):
        errors = validate_course({"code": "CS101", "name": "Math", "credits": 0})
        assert any("credits" in e.lower() for e in errors)

    def test_credits_too_high(self):
        errors = validate_course({"code": "CS101", "name": "Math", "credits": 11})
        assert any("credits" in e.lower() for e in errors)

    def test_valid_course(self):
        errors = validate_course({"code": "CS101", "name": "Intro to CS", "credits": 3})
        assert errors == []


class TestValidateGrade:
    def test_grade_below_zero(self):
        errors = validate_grade({"enrollment_id": 1, "grade": -1.0})
        assert any("grade" in e.lower() for e in errors)

    def test_grade_above_100(self):
        errors = validate_grade({"enrollment_id": 1, "grade": 101.0})
        assert any("grade" in e.lower() for e in errors)

    def test_missing_enrollment(self):
        errors = validate_grade({"enrollment_id": None, "grade": 85.0})
        assert any("enrollment" in e.lower() for e in errors)

    def test_valid_grade(self):
        errors = validate_grade({"enrollment_id": 1, "grade": 75.0})
        assert errors == []


class TestNumericToLetter:
    def test_grade_90_is_A(self):
        assert numeric_to_letter(90) == "A"

    def test_grade_100_is_A(self):
        assert numeric_to_letter(100) == "A"

    def test_grade_89_is_B(self):
        assert numeric_to_letter(89) == "B"

    def test_grade_80_is_B(self):
        assert numeric_to_letter(80) == "B"

    def test_grade_79_is_C(self):
        assert numeric_to_letter(79) == "C"

    def test_grade_70_is_C(self):
        assert numeric_to_letter(70) == "C"

    def test_grade_69_is_D(self):
        assert numeric_to_letter(69) == "D"

    def test_grade_60_is_D(self):
        assert numeric_to_letter(60) == "D"

    def test_grade_59_is_F(self):
        assert numeric_to_letter(59) == "F"

    def test_grade_0_is_F(self):
        assert numeric_to_letter(0) == "F"
