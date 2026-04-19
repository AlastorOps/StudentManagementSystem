from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from app.database.connection import get_connection


@dataclass
class Grade:
    id: Optional[int]
    enrollment_id: int
    grade: float
    letter_grade: str
    graded_at: Optional[str] = None
    notes: Optional[str] = None


class GradeRepository:
    def get_all(self) -> list[Grade]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT id, enrollment_id, grade, letter_grade, graded_at, notes FROM grades ORDER BY graded_at DESC"
        ).fetchall()
        return [Grade(**dict(row)) for row in rows]

    def get_by_id(self, grade_id: int) -> Optional[Grade]:
        conn = get_connection()
        row = conn.execute(
            "SELECT id, enrollment_id, grade, letter_grade, graded_at, notes FROM grades WHERE id = ?",
            (grade_id,),
        ).fetchone()
        return Grade(**dict(row)) if row else None

    def get_by_enrollment(self, enrollment_id: int) -> Optional[Grade]:
        conn = get_connection()
        row = conn.execute(
            "SELECT id, enrollment_id, grade, letter_grade, graded_at, notes FROM grades WHERE enrollment_id = ?",
            (enrollment_id,),
        ).fetchone()
        return Grade(**dict(row)) if row else None

    def create(self, grade: Grade) -> Grade:
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO grades (enrollment_id, grade, letter_grade, notes) VALUES (?, ?, ?, ?)",
            (grade.enrollment_id, grade.grade, grade.letter_grade, grade.notes),
        )
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def update(self, grade: Grade) -> Grade:
        conn = get_connection()
        conn.execute(
            "UPDATE grades SET grade=?, letter_grade=?, notes=? WHERE id=?",
            (grade.grade, grade.letter_grade, grade.notes, grade.id),
        )
        conn.commit()
        return self.get_by_id(grade.id)

    def delete(self, grade_id: int) -> None:
        conn = get_connection()
        conn.execute("DELETE FROM grades WHERE id = ?", (grade_id,))
        conn.commit()

    def get_all_with_details(self) -> list[dict]:
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT
                g.id,
                g.enrollment_id,
                g.grade,
                g.letter_grade,
                g.graded_at,
                g.notes,
                s.first_name || ' ' || s.last_name AS student_name,
                c.code || ' — ' || c.name AS course_display_name
            FROM grades g
            JOIN enrollments e ON e.id = g.enrollment_id
            JOIN students s ON s.id = e.student_id
            JOIN courses c ON c.id = e.course_id
            ORDER BY g.graded_at DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]
