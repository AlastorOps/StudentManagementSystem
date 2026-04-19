# Student Management System

## Overview

A desktop-based Student Management System built with Python. The application follows a modular architecture separating concerns into controllers, models, views, and utilities.

## Features

* Student management (add, update, delete, view)
* Course management
* Enrollment handling
* Grade tracking
* GUI-based interface
* Data persistence using SQLite

## Project Structure

```
app/
  controllers/    # Business logic
  models/         # Data models
  views/          # GUI components
  database/       # DB connection and migrations
  config/         # App configuration
  utils/          # Helpers and validators

tests/            # Unit tests
main.py           # Entry point
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/AlastorOps/StudentManagementSystem.git
cd StudentManagementSystem
```

2. Create virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Database

* Uses SQLite
* Database file is auto-created on first run
* No manual setup required

## Testing

Run tests using:

```bash
pytest
```

## .gitignore Notes

The following are excluded:

* SQLite database files
* Python cache files (**pycache**)
* Virtual environments

## Future Improvements

* Add authentication system
* Export reports (PDF/Excel)
* Improve UI/UX
* Implement role-based access

## License

This project is for educational purposes.
