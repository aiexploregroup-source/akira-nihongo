"""あきら にほんご — complete Japanese self-study companion.

Entry point. Run with:  python main.py
"""
from __future__ import annotations

import os
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication

from nihongo_app.core.database import Database
from nihongo_app.ui import i18n
from nihongo_app.ui.intro import IntroScreen
from nihongo_app.ui.logo import logo_pixmap
from nihongo_app.ui.main_window import MainWindow
from nihongo_app.ui.theme import load_application_fonts, theme


def main() -> int:
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    app.setApplicationName("あきら にほんご")
    app.setOrganizationName("Akira Nihongo")
    app.setApplicationVersion("1.1.0")
    app.setWindowIcon(logo_pixmap(256))

    load_application_fonts()
    app.setFont(QFont(theme.font_ui_primary, theme.font_size))

    db = Database()
    i18n.load(db)
    app.setApplicationDisplayName(
        "Akira Nihongo · Journey to N5" if i18n.is_english()
        else "あきら にほんご · N5 への旅")
    window = MainWindow(db)

    def show_window() -> None:
        window.show()
        window.raise_()
        window.activateWindow()

    if os.environ.get("AKIRA_SKIP_INTRO") == "1":
        show_window()
    else:
        intro = IntroScreen()
        intro.finished.connect(show_window)
        intro.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
