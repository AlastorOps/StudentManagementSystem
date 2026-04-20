import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from app.database.migrations import run_migrations
from app.views.main_window import MainWindow
from app.config.settings import APP_NAME


def main():
    run_migrations()

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    qss_path = os.path.join(base_path, "app", "assets", "styles", "theme_light.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
