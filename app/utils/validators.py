import re


def validate_student(data: dict) -> list[str]:
    errors = []

    first_name = (data.get("first_name") or "").strip()
    last_name = (data.get("last_name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()

    if not first_name:
        errors.append("First name is required.")
    elif not re.match(r"^[A-Za-z\s\-']+$", first_name):
        errors.append("First name must contain only letters.")
    if not last_name:
        errors.append("Last name is required.")
    elif not re.match(r"^[A-Za-z\s\-']+$", last_name):
        errors.append("Last name must contain only letters.")
    if not email:
        errors.append("Email is required.")
    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        errors.append("Email address is not valid.")
    if phone and not re.match(r"^[\d\s\-\+]+$", phone):
        errors.append("Phone must contain only digits, spaces, dashes, or plus sign.")

    return errors


def validate_course(data: dict) -> list[str]:
    errors = []

    code = (data.get("code") or "").strip()
    name = (data.get("name") or "").strip()
    credits = data.get("credits")

    if not code:
        errors.append("Course code is required.")
    elif not re.match(r"^[A-Za-z0-9]{1,10}$", code):
        errors.append("Course code must be alphanumeric and at most 10 characters.")
    if not name:
        errors.append("Course name is required.")
    try:
        credits_int = int(credits)
        if credits_int < 1 or credits_int > 10:
            errors.append("Credits must be between 1 and 10.")
    except (TypeError, ValueError):
        errors.append("Credits must be a valid number.")

    return errors


def validate_score(score) -> list[str]:
    errors = []
    try:
        grade_float = float(score)
        if grade_float < 0.0 or grade_float > 100.0:
            errors.append("Grade must be between 0.0 and 100.0.")
    except (TypeError, ValueError):
        errors.append("Grade must be a valid number.")
    return errors


def validate_grade(data: dict) -> list[str]:
    errors = []
    if not data.get("enrollment_id"):
        errors.append("Enrollment is required.")
    errors.extend(validate_score(data.get("grade")))
    return errors
