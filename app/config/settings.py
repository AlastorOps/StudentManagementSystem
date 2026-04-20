from pathlib import Path
import sys

if getattr(sys, 'frozen', False):
    _PROJECT_ROOT = Path(sys.executable).parent
else:
    _PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DB_PATH = str(_PROJECT_ROOT / "database" / "student_db.sqlite")
APP_NAME = "Student Management System"
VERSION = "1.0.0"
