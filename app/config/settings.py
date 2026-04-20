from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = str(_PROJECT_ROOT / "database" / "student_db.sqlite")
APP_NAME = "Student Management System"
VERSION = "1.0.0"
