import sqlite3
import pytest

import app.database.connection as _db_module
from app.database.migrations import run_migrations
from app.models.student import Student, StudentRepository
from app.models.course import Course, CourseRepository
from app.models.enrollment import Enrollment, EnrollmentRepository
from app.models.grade import Grade, GradeRepository
from app.controllers.student_controller import StudentController
from app.controllers.enrollment_controller import EnrollmentController
from app.controllers.grade_controller import GradeController


@pytest.fixture(autouse=True)
def fresh_db():
    """Inject a fresh in-memory DB into the singleton before each test."""
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    _db_module._connection = conn
    run_migrations()
    yield conn
    _db_module._connection = None
    conn.close()


class TestStudentController:
    def test_create_student_valid(self):
        ctrl = StudentController()
        ok, result = ctrl.create_student({
            "first_name": "Alice",
            "last_name": "Walker",
            "email": "alice@example.com",
            "phone": "",
            "date_of_birth": ""
        })
        assert ok is True
        assert isinstance(result, Student)
        assert result.full_name == "Alice Walker"

    def test_create_student_missing_fields(self):
        ctrl = StudentController()
        ok, result = ctrl.create_student({"first_name": "", "last_name": "", "email": ""})
        assert ok is False
        assert isinstance(result, str)
        assert len(result) > 0

    def test_create_student_invalid_email(self):
        ctrl = StudentController()
        ok, result = ctrl.create_student({
            "first_name": "Bob", "last_name": "Smith", "email": "not-an-email"
        })
        assert ok is False
        assert "email" in result.lower()

    def test_create_student_duplicate_email(self):
        ctrl = StudentController()
        data = {"first_name": "Carol", "last_name": "Jones", "email": "carol@example.com"}
        ctrl.create_student(data)
        ok, result = ctrl.create_student(data)
        assert ok is False
        assert "already exists" in result.lower()


class TestEnrollmentController:
    def test_enroll_student(self):
        s_repo = StudentRepository()
        c_repo = CourseRepository()
        ctrl = EnrollmentController()

        s = s_repo.create(Student(id=None, first_name="Dave", last_name="Lee", email="dave@example.com"))
        c = c_repo.create(Course(id=None, code="PHY101", name="Physics", credits=3))

        ok, msg = ctrl.enroll_student(s.id, c.id)
        assert ok is True

    def test_duplicate_enrollment(self):
        s_repo = StudentRepository()
        c_repo = CourseRepository()
        ctrl = EnrollmentController()

        s = s_repo.create(Student(id=None, first_name="Eve", last_name="Park", email="eve@example.com"))
        c = c_repo.create(Course(id=None, code="BIO201", name="Biology", credits=4))

        ctrl.enroll_student(s.id, c.id)
        ok, msg = ctrl.enroll_student(s.id, c.id)
        assert ok is False
        assert "already enrolled" in msg.lower()


class TestGradeController:
    def test_add_grade_sets_letter_grade(self):
        s_repo = StudentRepository()
        c_repo = CourseRepository()
        e_repo = EnrollmentRepository()
        ctrl = GradeController()

        s = s_repo.create(Student(id=None, first_name="Frank", last_name="Oz", email="frank@example.com"))
        c = c_repo.create(Course(id=None, code="ENG101", name="English", credits=3))
        enr = e_repo.create(Enrollment(id=None, student_id=s.id, course_id=c.id))

        ok, grade = ctrl.add_grade(enr.id, 92.5, "")
        assert ok is True
        assert isinstance(grade, Grade)
        assert grade.letter_grade == "A"
        assert grade.grade == 92.5

    def test_grade_letter_auto_calculated_B(self):
        s_repo = StudentRepository()
        c_repo = CourseRepository()
        e_repo = EnrollmentRepository()
        ctrl = GradeController()

        s = s_repo.create(Student(id=None, first_name="Grace", last_name="Hill", email="grace@example.com"))
        c = c_repo.create(Course(id=None, code="ART101", name="Art", credits=2))
        enr = e_repo.create(Enrollment(id=None, student_id=s.id, course_id=c.id))

        ok, grade = ctrl.add_grade(enr.id, 85.0, "")
        assert ok is True
        assert grade.letter_grade == "B"

    def test_add_grade_invalid_score(self):
        ctrl = GradeController()
        ok, msg = ctrl.add_grade(1, 150.0, "")
        assert ok is False
        assert isinstance(msg, str)
