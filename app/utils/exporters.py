import csv
from app.models.student import Student


def export_students_to_csv(students: list[Student], filepath: str) -> bool:
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "First Name", "Last Name", "Email", "Phone", "Date of Birth", "Created At"])
            for s in students:
                writer.writerow([s.id, s.first_name, s.last_name, s.email, s.phone or "", s.date_of_birth or "", s.created_at or ""])
        return True
    except Exception:
        return False
