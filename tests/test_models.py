import sqlite3
import pytest

import app.database.connection as _db_module
from app.database.migrations import run_migrations
from app.models.student import Student, StudentRepository
from app.models.course import Course, CourseRepository
from app.models.grade import Grade, GradeRepository
from app.models.enrollment import Enrollment, EnrollmentRepository


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


class TestStudentRepository:
    def test_create_and_get_by_id(self):
        repo = StudentRepository()
        s = Student(id=None, first_name="Alice", last_name="Brown", email="alice@example.com")
        created = repo.create(s)
        assert created.id is not None
        assert created.first_name == "Alice"
        assert created.last_name == "Brown"
        fetched = repo.get_by_id(created.id)
        assert fetched.email == "alice@example.com"

    def test_get_all(self):
        repo = StudentRepository()
        repo.create(Student(id=None, first_name="A", last_name="One", email="a@example.com"))
        repo.create(Student(id=None, first_name="B", last_name="Two", email="b@example.com"))
        all_students = repo.get_all()
        assert len(all_students) == 2

    def test_update(self):
        repo = StudentRepository()
        s = repo.create(Student(id=None, first_name="Old", last_name="Name", email="old@example.com"))
        s.first_name = "New"
        updated = repo.update(s)
        assert updated.first_name == "New"

    def test_delete(self):
        repo = StudentRepository()
        s = repo.create(Student(id=None, first_name="Del", last_name="Me", email="del@example.com"))
        repo.delete(s.id)
        assert repo.get_by_id(s.id) is None

    def test_search(self):
        repo = StudentRepository()
        repo.create(Student(id=None, first_name="John", last_name="Doe", email="john@example.com"))
        repo.create(Student(id=None, first_name="Jane", last_name="Doe", email="jane@example.com"))
        results = repo.search("John")
        assert len(results) == 1
        assert results[0].first_name == "John"


class TestGradeRepositoryWithDetails:
    def test_get_all_with_details_returns_joined_data(self):
        student_repo = StudentRepository()
        course_repo = CourseRepository()
        enrollment_repo = EnrollmentRepository()
        grade_repo = GradeRepository()

        s = student_repo.create(Student(id=None, first_name="Bob", last_name="Jones", email="bob@test.com"))
        c = course_repo.create(Course(id=None, code="MATH101", name="Calculus", credits=4))
        enr = enrollment_repo.create(Enrollment(id=None, student_id=s.id, course_id=c.id))
        grade_repo.create(Grade(id=None, enrollment_id=enr.id, grade=88.5, letter_grade="B"))

        details = grade_repo.get_all_with_details()
        assert len(details) == 1
        assert details[0]["student_name"] == "Bob Jones"
        assert "MATH101" in details[0]["course_display_name"]
        assert details[0]["grade"] == 88.5
        assert details[0]["letter_grade"] == "B"


class TestModelProperties:
    def test_student_full_name(self):
        s = Student(id=1, first_name="Jane", last_name="Smith", email="j@j.com")
        assert s.full_name == "Jane Smith"

    def test_course_display_name(self):
        c = Course(id=1, code="CS101", name="Intro to CS", credits=3)
        assert c.display_name == "CS101 — Intro to CS"
