"""Application shell: branded menu bar, responsive navigation and page stack."""
from __future__ import annotations

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QAction, QFont, QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMenu, QPushButton,
    QScrollArea, QStackedWidget, QVBoxLayout, QWidget, QApplication,
)

from ..data.registry import LEVELS, LEVEL_BY_KEY
from ..core.database import Database
from .pages.base import Page
from .logo import clear_logo_cache, logo_pixmap
from . import i18n
from .i18n import apply_language, LANG_LABELS, tr
from .theme import theme, set_theme
from .widgets import NavButton, pill

APP_NAME = "あきら にほんご"

NAV_GROUPS: list[tuple[str, list[tuple[str, str, str]]]] = [
    ("学習", [
        ("dashboard", "⌂", "学びの旅"),
        ("foundations", "あ", "文字の基礎"),
        ("greetings", "◉", "あいさつ"),
        ("numbers", "0", "すうじ"),
    ]),
    ("章", [
        (f"lesson-{n}", str(n), f"L{n} · {LEVEL_BY_KEY[f'lesson-{n}'].jp}")
        for n in range(1, 13)
    ]),
    ("実践", [
        ("real_life", "✦", "実践日本語"),
    ]),
    ("練習", [
        ("kana_practice", "あ", "文字の練習"),
        ("flashcards", "▤", "フラッシュカード"),
        ("quiz", "✓", "クイズ"),
    ]),
    ("その他", [
        ("search", "⌕", "検索"),
        ("settings", "⚙", "設定"),
    ]),
]

PAGE_TITLES: dict[str, tuple[str, str]] = {
    "dashboard": ("学びの旅", "今日の一歩から、N5 へ"),
    "kana_practice": ("文字の練習", "ひらがな・カタカナをやさしく反復"),
    "flashcards": ("フラッシュカード", "間隔反復で語彙を定着させる"),
    "quiz": ("クイズ", "語彙・文法・文字をまとめて確認"),
    "search": ("検索", "教材全体をひとつの検索欄から"),
    "settings": ("設定", "外観・目標・データの管理"),
}


class MainWindow(QMainWindow):
    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db
        i18n.load(db)
        self.setWindowTitle(f"{APP_NAME} · N5 への旅")
        self.setWindowIcon(logo_pixmap(256))
        self.resize(1440, 900)
        self.setMinimumSize(760, 560)
        self._compact = False
        self._pages: dict[str, Page] = {}
        self._nav_buttons: dict[str, NavButton] = {}
        self._current_key = "dashboard"

        self._build_menu_bar()
        self._build_ui()
        self._apply_theme()
        self.navigate("dashboard")
        apply_language(self)

        self.shortcut_search = QShortcut(QKeySequence("Ctrl+K"), self)
        self.shortcut_search.activated.connect(self._focus_search)

    # ------------------------------------------------------------------ menu
    def _build_menu_bar(self) -> None:
        bar = self.menuBar()
        bar.setObjectName("mainMenuBar")

        self._brand_action = QAction(QIcon(logo_pixmap(32)), APP_NAME, self)
        self._brand_action.setToolTip("学びの旅へ戻る")
        self._brand_action.triggered.connect(lambda: self.navigate("dashboard"))
        bar.addAction(self._brand_action)

        def add_menu(title: str) -> QMenu:
            menu = bar.addMenu(title)
            assert menu is not None
            return menu

        def add(menu: QMenu, text: str, key: str, shortcut: str | None = None) -> None:
            action = QAction(text, self)
            if shortcut:
                action.setShortcut(QKeySequence(shortcut))
            action.triggered.connect(lambda _=False, k=key: self.navigate(k))
            menu.addAction(action)

        journey = add_menu("旅")
        add(journey, "ホーム · 学びの旅", "dashboard")
        journey.addSeparator()
        add(journey, "文字の基礎", "foundations")
        add(journey, "あいさつ", "greetings")
        add(journey, "すうじ", "numbers")
        journey.addSeparator()
        lessons = journey.addMenu("12 章")
        assert lessons is not None
        for number in range(1, 13):
            level = LEVEL_BY_KEY[f"lesson-{number}"]
            add(lessons, f"L{number} · {level.jp}", level.key)
        journey.addSeparator()
        add(journey, "実践日本語", "real_life")

        practice = add_menu("練習")
        add(practice, "文字の練習", "kana_practice")
        add(practice, "フラッシュカード", "flashcards")
        add(practice, "クイズ", "quiz")

        view = add_menu("表示")
        self._theme_action = QAction("テーマを切り替え", self)
        self._theme_action.setShortcut(QKeySequence("Ctrl+T"))
        self._theme_action.triggered.connect(self.toggle_theme)
        view.addAction(self._theme_action)
        search_action = QAction("検索", self)
        search_action.setShortcut(QKeySequence("Ctrl+K"))
        search_action.triggered.connect(self._focus_search)
        view.addAction(search_action)
        view.addSeparator()
        add(view, "設定", "settings")

        help_menu = add_menu("ヘルプ")
        about = QAction(f"{APP_NAME} について", self)
        about.triggered.connect(self._show_about)
        help_menu.addAction(about)

        # Persistent system-language switch, always visible in the menu bar.
        self._language_action = QAction(
            LANG_LABELS.get(i18n.current(), LANG_LABELS["ja"]), self)
        self._language_action.setObjectName("languageAction")
        self._language_action.setToolTip("表示言語を切り替える / Switch display language")
        self._language_action.triggered.connect(self.toggle_language)
        bar.addAction(self._language_action)

    # ------------------------------------------------------------------ build
    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("root")
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.nav_frame = QFrame()
        self.nav_frame.setObjectName("navRail")
        self.nav_frame.setFixedWidth(250)
        nav_layout = QVBoxLayout(self.nav_frame)
        nav_layout.setContentsMargins(14, 16, 12, 14)
        nav_layout.setSpacing(6)
        root.addWidget(self.nav_frame)

        brand_row = QHBoxLayout()
        self._brand_logo = QLabel()
        self._brand_logo.setPixmap(logo_pixmap(44))
        brand_title = QLabel(APP_NAME)
        brand_title.setFont(QFont(theme.font_jp_primary, 17, QFont.Weight.DemiBold))
        brand_title.setStyleSheet(f"color: {theme.palette.text};")
        brand_sub = QLabel("ゼロから N5 へ")
        brand_sub.setObjectName("caption")
        self._brand_col = QWidget()
        col = QVBoxLayout(self._brand_col)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(1)
        col.addWidget(brand_title)
        col.addWidget(brand_sub)
        brand_row.addWidget(self._brand_logo)
        brand_row.addSpacing(9)
        brand_row.addWidget(self._brand_col)
        nav_layout.addLayout(brand_row)

        line = QFrame()
        line.setObjectName("divider")
        nav_layout.addWidget(line)

        nav_scroll = QScrollArea()
        nav_scroll.setWidgetResizable(True)
        nav_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        nav_holder = QWidget()
        nav_holder_layout = QVBoxLayout(nav_holder)
        nav_holder_layout.setContentsMargins(0, 4, 4, 4)
        nav_holder_layout.setSpacing(12)
        nav_scroll.setWidget(nav_holder)
        nav_layout.addWidget(nav_scroll, 1)
        self.nav_scroll = nav_scroll

        for group_title, entries in NAV_GROUPS:
            group_label = QLabel(group_title)
            group_label.setObjectName("caption")
            group_label.setStyleSheet(
                "font-size: 11px; font-weight: 700; letter-spacing: 0.8px;")
            nav_holder_layout.addWidget(group_label)
            for key, icon, text in entries:
                button = NavButton(f"{icon}   {text}")
                button._full_text = f"{icon}   {text}"
                button._icon_text = icon
                button.clicked.connect(lambda _=False, k=key: self.navigate(k))
                nav_holder_layout.addWidget(button)
                self._nav_buttons[key] = button

        bottom_row = QHBoxLayout()
        self.btn_theme = QPushButton("◐")
        self.btn_theme.setObjectName("ghost")
        self.btn_theme.setToolTip("テーマを切り替え (Ctrl+T)")
        self.btn_theme.clicked.connect(self.toggle_theme)
        bottom_row.addWidget(self.btn_theme)
        bottom_row.addStretch(1)
        nav_layout.addLayout(bottom_row)

        content_col = QVBoxLayout()
        content_col.setContentsMargins(0, 0, 0, 0)
        content_col.setSpacing(0)
        root.addLayout(content_col, 1)

        top = QFrame()
        top.setObjectName("topBar")
        top.setFixedHeight(68)
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(26, 0, 22, 0)
        top_layout.setSpacing(14)
        content_col.addWidget(top)

        self.crumb_title = QLabel("学びの旅")
        self.crumb_title.setStyleSheet("font-size: 16px; font-weight: 700;")
        self.crumb_sub = QLabel("今日の一歩から、N5 へ")
        self.crumb_sub.setObjectName("caption")
        crumb_col = QVBoxLayout()
        crumb_col.setSpacing(0)
        crumb_col.addWidget(self.crumb_title)
        crumb_col.addWidget(self.crumb_sub)
        top_layout.addLayout(crumb_col)
        self._crumb_col = crumb_col
        top_layout.addStretch(1)

        self.search = QLineEdit()
        self.search.setObjectName("search")
        self.search.setPlaceholderText("⌕  ことばを探す…  (Ctrl+K)")
        self.search.returnPressed.connect(self._on_search)
        top_layout.addWidget(self.search)

        self.goal_pill = pill("今日の目標 0%", "green")
        top_layout.addWidget(self.goal_pill)
        self.streak_pill = pill("🔥 0 日", "gold")
        top_layout.addWidget(self.streak_pill)

        self.stack = QStackedWidget()
        content_col.addWidget(self.stack, 1)

        self.statusBar().showMessage(f"{APP_NAME} · ゼロから N5 への旅")

    # ---------------------------------------------------------------- navigate
    def _get_page(self, key: str, **kwargs) -> Page:
        if key in self._pages:
            return self._pages[key]
        from .pages import (
            dashboard, foundations, greetings, numbers, lesson, real_life,
            kana_practice, flashcards, quiz, search_page, settings_page,
        )
        mapping = {
            "dashboard": dashboard.DashboardPage,
            "foundations": foundations.FoundationsPage,
            "greetings": greetings.GreetingsPage,
            "numbers": numbers.NumbersPage,
            "real_life": real_life.RealLifePage,
            "kana_practice": kana_practice.KanaPracticePage,
            "flashcards": flashcards.FlashcardsPage,
            "quiz": quiz.QuizPage,
            "search": search_page.SearchPage,
            "settings": settings_page.SettingsPage,
        }
        if key in mapping:
            page = mapping[key](self.db, self)
        elif key.startswith("lesson-"):
            page = lesson.LessonPage(self.db, self, lesson=int(key.split("-")[1]))
        else:
            page = dashboard.DashboardPage(self.db, self)
        if hasattr(page, "initial_query") and "query" in kwargs:
            page.initial_query = kwargs["query"]
        self._pages[key] = page
        self.stack.addWidget(page)
        return page

    def navigate(self, key: str, **kwargs) -> None:
        if key.startswith("lesson-") and key not in self._pages:
            self._get_page(key)
        page = self._get_page(key, **kwargs)
        if hasattr(page, "on_navigated"):
            page.on_navigated(**kwargs)
        page.refresh()
        self.stack.setCurrentWidget(page)
        self._current_key = key
        self._update_breadcrumb(key)
        for nav_key, button in self._nav_buttons.items():
            button.setChecked(nav_key == key)
        self._update_pills()
        apply_language(self)

    def _update_breadcrumb(self, key: str) -> None:
        if key in PAGE_TITLES:
            title, sub = PAGE_TITLES[key]
        elif key in LEVEL_BY_KEY:
            level = LEVEL_BY_KEY[key]
            title = level.jp
            sub = f"{level.stage} · {level.en}"
        else:
            title, sub = APP_NAME, ""
        self.crumb_title.setText(title)
        self.crumb_sub.setText(sub)

    def _update_pills(self) -> None:
        goal = self.db.get_setting("daily_goal", 20)
        done = self.db.today_stats()["reviewed"]
        pct = min(100, int(100 * done / goal)) if goal else 0
        self.goal_pill.setText(f"今日の目標 {pct}%")
        self.streak_pill.setText(f"🔥 {self.db.streak()} 日")

    def refresh_all(self) -> None:
        self._update_pills()
        for page in self._pages.values():
            page.refresh()
        apply_language(self)

    def toggle_language(self) -> None:
        """Switch the whole interface between Japanese and English."""
        i18n.toggle(self.db)
        self.refresh_all()

    # ------------------------------------------------------------------ theme
    def _apply_theme(self) -> None:
        app = QApplication.instance()
        if app is not None:
            app.setStyleSheet(set_theme(self.db.get_setting("dark_theme", True),
                                        self.db.get_setting("font_size", 14)))
        clear_logo_cache()
        self._brand_action.setIcon(QIcon(logo_pixmap(32)))
        self.setWindowIcon(logo_pixmap(256))
        self._brand_logo.setPixmap(logo_pixmap(44))
        for page in self._pages.values():
            page.on_theme_changed()

    def toggle_theme(self) -> None:
        new = not self.db.get_setting("dark_theme", True)
        self.db.set_setting("dark_theme", new)
        self._apply_theme()

    # ------------------------------------------------------------------ events
    def _focus_search(self) -> None:
        self.search.setFocus()
        self.search.selectAll()

    def _on_search(self) -> None:
        query = self.search.text().strip()
        if query:
            self.navigate("search", query=query)

    def _show_about(self) -> None:
        from PySide6.QtWidgets import QMessageBox
        if i18n.is_english():
            title = f"About {APP_NAME}"
            body = (
                f"{APP_NAME}\n\n"
                "A self-study journey covering lessons, characters, grammar "
                "and real-life conversation in one place.\n\n"
                "Curriculum based on Genki I (3rd Edition).\n\n"
                "Version 1.1.0"
            )
        else:
            title = f"{APP_NAME} について"
            body = (
                f"{APP_NAME}\n\n"
                "レッスン、文字、文法、実践会話を\n"
                "ひとつの旅としてまとめた学習アプリです。\n\n"
                "Version 1.1.0"
            )
        QMessageBox.information(self, title, body)

    def resizeEvent(self, event) -> None:  # noqa: N802 - Qt naming
        super().resizeEvent(event)
        compact = self.width() < 1040
        if compact == self._compact:
            return
        self._compact = compact
        self.nav_frame.setFixedWidth(68 if compact else 250)
        for key, button in self._nav_buttons.items():
            button.setText(button._icon_text if compact else tr(button._full_text))
            button.setToolTip(tr(button._full_text))
            button.setProperty("compact", compact)
            button.style().polish(button)
        self._brand_col.setVisible(not compact)
        self.search.setMinimumWidth(140 if compact else 250)
