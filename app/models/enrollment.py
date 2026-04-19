from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from app.database.connection import get_connection


@dataclass
class Enrollment:
    id: Optional[int]
    student_id: int
    course_id: int
    enrolled_at: Optional[str] = None


class EnrollmentRepository:
    def get_all(self) -> list[Enrollment]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT id, student_id, course_id, enrolled_at FROM enrollments ORDER BY enrolled_at DESC"
        ).fetchall()
        return [Enrollment(**dict(row)) for row in rows]

    def get_by_id(self, enrollment_id: int) -> Optional[Enrollment]:
        conn = get_connection()
        row = conn.execute(
            "SELECT id, student_id, course_id, enrolled_at FROM enrollments WHERE id = ?",
            (enrollment_id,),
        ).fetchone()
        return Enrollment(**dict(row)) if row else None

    def get_by_student(self, student_id: int) -> list[Enrollment]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT id, student_id, course_id, enrolled_at FROM enrollments WHERE student_id = ?",
            (student_id,),
        ).fetchall()
        return [Enrollment(**dict(row)) for row in rows]

    def get_by_course(self, course_id: int) -> list[Enrollment]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT id, student_id, course_id, enrolled_at FROM enrollments WHERE course_id = ?",
            (course_id,),
        ).fetchall()
        return [Enrollment(**dict(row)) for row in rows]

    def create(self, enrollment: Enrollment) -> Enrollment:
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)",
            (enrollment.student_id, enrollment.course_id),
        )
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def delete(self, enrollment_id: int) -> None:
        conn = get_connection()
        conn.execute("DELETE FROM enrollments WHERE id = ?", (enrollment_id,))
        conn.commit()

    def get_all_with_names(self) -> list[dict]:
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT
                e.id,
                e.student_id,
                e.course_id,
                e.enrolled_at,
                s.first_name || ' ' || s.last_name AS student_name,
                c.code || ' — ' || c.name AS course_display_name
            FROM enrollments e
            JOIN students s ON s.id = e.student_id
            JOIN courses c ON c.id = e.course_id
            ORDER BY e.enrolled_at DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]
