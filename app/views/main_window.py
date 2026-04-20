from pathlib import Path

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame, QApplication
)
from PyQt6.QtCore import Qt

from app.config.settings import APP_NAME, VERSION
from app.views.dashboard import DashboardView
from app.views.students.student_list import StudentListView
from app.views.courses.course_list import CourseListView
from app.views.enrollments.enrollment_list import EnrollmentListView
from app.views.grades.grade_list import GradeListView

_STYLES_DIR = Path(__file__).parent.parent / "assets" / "styles"


class NavButton(QPushButton):
    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setFixedHeight(48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName("navButton")

    def set_active(self, active: bool):
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1000, 650)
        self._dark_mode = False
        self._build_ui()
        self._nav_buttons[0].set_active(True)

    def _build_ui(self):
        central = QWidget()
        central.setObjectName("appShell")
        self.setCentralWidget(central)
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 20)
        sidebar_layout.setSpacing(4)

        brand_card = QFrame()
        brand_card.setObjectName("sidebarBrand")
        brand_layout = QVBoxLayout(brand_card)
        brand_layout.setContentsMargins(16, 16, 16, 16)
        brand_layout.setSpacing(2)

        eyebrow = QLabel("Campus Console")
        eyebrow.setObjectName("sidebarEyebrow")
        title_label = QLabel(APP_NAME)
        title_label.setObjectName("sidebarTitle")
        title_label.setWordWrap(True)
        version_label = QLabel(f"Version {VERSION}")
        version_label.setObjectName("sidebarVersion")

        brand_layout.addWidget(eyebrow)
        brand_layout.addWidget(title_label)
        brand_layout.addWidget(version_label)
        sidebar_layout.addWidget(brand_card)

        nav_items = [
            ("Dashboard", 0),
            ("Students", 1),
            ("Courses", 2),
            ("Enrollments", 3),
            ("Grades", 4),
        ]
        self._nav_buttons: list[NavButton] = []
        for label, index in nav_items:
            btn = NavButton(label)
            btn.clicked.connect(lambda checked, i=index: self._switch_page(i))
            self._nav_buttons.append(btn)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        self._theme_btn = QPushButton("Switch to Night Mode")
        self._theme_btn.setObjectName("themeToggleButton")
        self._theme_btn.setFixedHeight(42)
        self._theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._theme_btn.clicked.connect(self._toggle_theme)
        sidebar_layout.addWidget(self._theme_btn)

        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self._stack = QStackedWidget()
        self._stack.setObjectName("stackContainer")
        self._dashboard = DashboardView()
        self._students = StudentListView()
        self._courses = CourseListView()
        self._enrollments = EnrollmentListView()
        self._grades = GradeListView()

        self._stack.addWidget(self._dashboard)
        self._stack.addWidget(self._students)
        self._stack.addWidget(self._courses)
        self._stack.addWidget(self._enrollments)
        self._stack.addWidget(self._grades)
        content_layout.addWidget(self._stack)

        root_layout.addWidget(sidebar)
        root_layout.addWidget(content_frame)

        self.statusBar().showMessage(f"{APP_NAME}  v{VERSION}")

    def _switch_page(self, index: int):
        for i, btn in enumerate(self._nav_buttons):
            btn.set_active(i == index)
        self._stack.setCurrentIndex(index)
        if index == 0:
            self._dashboard.refresh()

    def _toggle_theme(self):
        self._dark_mode = not self._dark_mode
        theme_file = "theme_dark.qss" if self._dark_mode else "theme_light.qss"
        qss_path = _STYLES_DIR / theme_file
        if qss_path.exists():
            with open(qss_path, "r", encoding="utf-8") as f:
                QApplication.instance().setStyleSheet(f.read())
        label = "Switch to Day Mode" if self._dark_mode else "Switch to Night Mode"
        self._theme_btn.setText(label)
