# Student Management System

A desktop CRUD application for managing students, courses, enrollments, and grades with a PyQt6 interface and SQLite storage.

## Overview

This project is a local desktop system built around a simple layered structure:

- `views` handle the PyQt6 user interface
- `controllers` coordinate validation and persistence
- `models` define entities and repository access
- `database` manages the SQLite connection and schema setup
- `utils` provides validation, formatting, and CSV export helpers

On startup, the application automatically creates the database schema if it does not already exist, then launches the main window with the light theme enabled by default.

## Features

- Dashboard with:
  - total students
  - total courses
  - total enrollments
  - average grade
  - latest 10 graded records
- Student management:
  - create, edit, delete, and view details
  - search by first name, last name, or email
  - export student data to CSV
- Course management:
  - create, edit, and delete courses
- Enrollment management:
  - enroll a student into a course
  - prevent duplicate enrollments
  - remove enrollments
- Grade management:
  - add, edit, and delete grades
  - automatic numeric-to-letter grade conversion
  - one grade per enrollment
- Theme support:
  - light theme
  - dark theme toggle from the sidebar

## Tech Stack

- Python 3
- PyQt6
- SQLite
- pytest

## Requirements

From `requirements.txt`:

```txt
PyQt6>=6.6.0
pytest>=9.0
```

## Project Structure

```text
StudentManagementSytem/
├─ app/
│  ├─ assets/
│  │  └─ styles/
│  ├─ config/
│  │  └─ settings.py
│  ├─ controllers/
│  ├─ database/
│  │  ├─ connection.py
│  │  └─ migrations.py
│  ├─ models/
│  ├─ utils/
│  └─ views/
├─ database/
│  └─ student_db.sqlite
├─ tests/
├─ main.py
├─ requirements.txt
└─ README.md
```

## Installation

1. Create and activate a virtual environment.
2. Install dependencies.

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Running the App

```powershell
python main.py
```

What happens on launch:

- SQLite database file is created at `database/student_db.sqlite` if needed
- migrations run automatically
- the main PyQt6 window opens
- the app starts in light mode

## Testing

Run the test suite with:

```powershell
pytest
```

The tests cover:

- repository behavior
- controller behavior
- validation rules

The test suite uses an in-memory SQLite database, so it does not depend on your local `student_db.sqlite` file.

## Database Schema

The app creates these tables automatically:

- `students`
- `courses`
- `enrollments`
- `grades`

Relationships:

- an enrollment links one student to one course
- a grade belongs to one enrollment
- deleting a student or course cascades through enrollments
- deleting an enrollment cascades through grades

## Validation Rules

Current validation implemented in `app/utils/validators.py`:

- Student:
  - first and last name are required
  - names allow letters, spaces, hyphens, and apostrophes
  - email is required and must be valid
  - phone is optional but restricted to digits, spaces, dashes, and `+`
- Course:
  - code is required
  - code must be alphanumeric and at most 10 characters
  - name is required
  - credits must be between 1 and 10
- Grade:
  - enrollment is required
  - grade must be a valid number between 0 and 100

## Notes

- The project name uses the folder spelling `StudentManagementSytem`, but the application title is `Student Management System`.
- SQLite is configured with foreign keys enabled and WAL journal mode.
- Student export currently supports CSV output.

## Entry Points

- App startup: [main.py](/abs/path/c:/Users/Alastor/Desktop/Personal%20Project/StudentManagementSytem/main.py)
- App settings: [app/config/settings.py](/abs/path/c:/Users/Alastor/Desktop/Personal%20Project/StudentManagementSytem/app/config/settings.py)
- Schema setup: [app/database/migrations.py](/abs/path/c:/Users/Alastor/Desktop/Personal%20Project/StudentManagementSytem/app/database/migrations.py)

