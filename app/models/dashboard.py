from __future__ import annotations
from dataclasses import dataclass, field
from app.database.connection import get_connection


@dataclass
class DashboardStats:
    total_students: int
    total_courses: int
    total_enrollments: int
    avg_grade: str
    recent_grades: list[dict] = field(default_factory=list)


class DashboardRepository:
    def get_stats(self) -> DashboardStats:
        conn = get_connection()
        total_students = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        total_courses = conn.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
        total_enrollments = conn.execute("SELECT COUNT(*) FROM enrollments").fetchone()[0]
        avg_row = conn.execute("SELECT AVG(grade) FROM grades").fetchone()[0]
        avg_grade = f"{avg_row:.1f}" if avg_row is not None else "N/A"
        recent_rows = conn.execute(
            """
            SELECT
                s.first_name || ' ' || s.last_name AS student_name,
                c.code || ' \u2014 ' || c.name AS course_name,
                g.grade,
                g.letter_grade,
                g.graded_at
            FROM grades g
            JOIN enrollments e ON e.id = g.enrollment_id
            JOIN students s ON s.id = e.student_id
            JOIN courses c ON c.id = e.course_id
            ORDER BY g.graded_at DESC
            LIMIT 10
            """
        ).fetchall()
        return DashboardStats(
            total_students=total_students,
            total_courses=total_courses,
            total_enrollments=total_enrollments,
            avg_grade=avg_grade,
            recent_grades=[dict(r) for r in recent_rows],
        )
