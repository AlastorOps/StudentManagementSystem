from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from app.database.connection import get_connection


@dataclass
class Course:
    id: Optional[int]
    code: str
    name: str
    description: Optional[str] = None
    credits: int = 3
    created_at: Optional[str] = None

    @property
    def display_name(self) -> str:
        return f"{self.code} — {self.name}"


class CourseRepository:
    def get_all(self) -> list[Course]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT id, code, name, description, credits, created_at FROM courses ORDER BY code"
        ).fetchall()
        return [Course(**dict(row)) for row in rows]

    def get_by_id(self, course_id: int) -> Optional[Course]:
        conn = get_connection()
        row = conn.execute(
            "SELECT id, code, name, description, credits, created_at FROM courses WHERE id = ?",
            (course_id,),
        ).fetchone()
        return Course(**dict(row)) if row else None

    def create(self, course: Course) -> Course:
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO courses (code, name, description, credits) VALUES (?, ?, ?, ?)",
            (course.code, course.name, course.description, course.credits),
        )
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def update(self, course: Course) -> Course:
        conn = get_connection()
        conn.execute(
            "UPDATE courses SET code=?, name=?, description=?, credits=? WHERE id=?",
            (course.code, course.name, course.description, course.credits, course.id),
        )
        conn.commit()
        return self.get_by_id(course.id)

    def delete(self, course_id: int) -> None:
        conn = get_connection()
        conn.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        conn.commit()
