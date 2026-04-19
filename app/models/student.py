from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from app.database.connection import get_connection


@dataclass
class Student:
    id: Optional[int]
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    created_at: Optional[str] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class StudentRepository:
    def get_all(self) -> list[Student]:
        conn = get_connection()
        rows = conn.execute(
            "SELECT id, first_name, last_name, email, phone, date_of_birth, created_at "
            "FROM students ORDER BY last_name, first_name"
        ).fetchall()
        return [Student(**dict(row)) for row in rows]

    def get_by_id(self, student_id: int) -> Optional[Student]:
        conn = get_connection()
        row = conn.execute(
            "SELECT id, first_name, last_name, email, phone, date_of_birth, created_at "
            "FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()
        return Student(**dict(row)) if row else None

    def create(self, student: Student) -> Student:
        conn = get_connection()
        cursor = conn.execute(
            "INSERT INTO students (first_name, last_name, email, phone, date_of_birth) "
            "VALUES (?, ?, ?, ?, ?)",
            (student.first_name, student.last_name, student.email, student.phone, student.date_of_birth),
        )
        conn.commit()
        return self.get_by_id(cursor.lastrowid)

    def update(self, student: Student) -> Student:
        conn = get_connection()
        conn.execute(
            "UPDATE students SET first_name=?, last_name=?, email=?, phone=?, date_of_birth=? WHERE id=?",
            (student.first_name, student.last_name, student.email, student.phone, student.date_of_birth, student.id),
        )
        conn.commit()
        return self.get_by_id(student.id)

    def delete(self, student_id: int) -> None:
        conn = get_connection()
        conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()

    def search(self, query: str) -> list[Student]:
        conn = get_connection()
        pattern = f"%{query}%"
        rows = conn.execute(
            "SELECT id, first_name, last_name, email, phone, date_of_birth, created_at "
            "FROM students "
            "WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ? "
            "ORDER BY last_name, first_name",
            (pattern, pattern, pattern),
        ).fetchall()
        return [Student(**dict(row)) for row in rows]
