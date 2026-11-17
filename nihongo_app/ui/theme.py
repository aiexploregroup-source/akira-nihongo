"""Akira Nihongo — design tokens, fonts and premium stylesheet."""
from __future__ import annotations

from pathlib import Path
from string import Template

from PySide6.QtGui import QFontDatabase

FONT_UI_PRIMARY = "Inter"
FONT_JP_PRIMARY = "Noto Sans JP"
FONT_UI = '"Inter", "Segoe UI Variable Text", "Segoe UI", "Noto Sans JP", sans-serif'
FONT_JP = '"Noto Sans JP", "Yu Gothic UI", "Meiryo", "Hiragino Kaku Gothic ProN", sans-serif'
FONT_MONO = '"JetBrains Mono", "Cascadia Mono", "Consolas", monospace'


class Palette:
    """Warm, low-glare palette. `accent` is the gold brand colour."""

    def __init__(self, dark: bool = True) -> None:
        if dark:
            self.bg = "#0E1116"
            self.bg_alt = "#12161E"
            self.surface = "#171C26"
            self.surface2 = "#1D2330"
            self.surface3 = "#272F40"
            self.border = "#313B4C"
            self.text = "#F3F0EA"
            self.muted = "#A9AFBC"
            self.faint = "#7D8697"
            self.accent = "#E9C07A"
            self.accent_soft = "#F6DCA8"
            self.accent_dim = "#3A3022"
            self.cyan = "#7FD8C4"
            self.gold = "#E9C07A"
            self.success = "#8BD8A6"
            self.danger = "#F28B9B"
            self.violet = "#A596F5"
            self.shadow = "#05070A"
            self.nav = "#10151D"
            self.hover = "#242C3A"
            self.input_bg = "#141924"
        else:
            self.bg = "#F7F5F0"
            self.bg_alt = "#F1EEE7"
            self.surface = "#FFFFFF"
            self.surface2 = "#FBF9F4"
            self.surface3 = "#ECE7DC"
            self.border = "#DED8CC"
            self.text = "#23262C"
            self.muted = "#6E7280"
            self.faint = "#9A9EAA"
            self.accent = "#9A6B22"
            self.accent_soft = "#7A5418"
            self.accent_dim = "#F3E7D0"
            self.cyan = "#177E70"
            self.gold = "#9A6B22"
            self.success = "#2F7D50"
            self.danger = "#B23A4C"
            self.violet = "#6C5CC4"
            self.shadow = "#CFC8BA"
            self.nav = "#FFFFFF"
            self.hover = "#F3EFE6"
            self.input_bg = "#FFFFFF"


QSS_TEMPLATE = Template(r"""
* { font-family: $font_ui; font-size: ${font_px}px; color: $text; }
QWidget#root { background: $bg; }
QWidget { background: transparent; }

QMenuBar { background: $nav; border-bottom: 1px solid $border; padding: 3px 8px; }
QMenuBar::item { padding: 7px 12px; border-radius: 8px; color: $muted; font-weight: 600; }
QMenuBar::item:selected { background: $hover; color: $text; }
QMenu { background: $surface; border: 1px solid $border; border-radius: 12px; padding: 6px; }
QMenu::item { padding: 9px 16px; border-radius: 8px; }
QMenu::item:selected { background: $accent_dim; color: $accent_soft; }
QMenu::separator { height: 1px; background: $border; margin: 5px 8px; }

QFrame#card, QFrame#hero, QFrame#panel, QFrame#mission {
    background: $surface;
    border: 1px solid $border;
    border-radius: 20px;
}
QFrame#hero {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
        stop:0 $surface2, stop:0.6 $surface, stop:1 $accent_dim);
    border: 1px solid $border;
}
QFrame#panel { background: $surface2; border-radius: 16px; }
QFrame#mission { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 $accent_dim, stop:1 $surface); border: 1px solid $accent; }
QFrame#divider { background: $border; max-height: 1px; }
QFrame#navRail { background: $nav; border-right: 1px solid $border; }
QFrame#topBar { background: $bg_alt; border-bottom: 1px solid $border; }

QLabel { background: transparent; }
QLabel#title { font-size: 25px; font-weight: 700; letter-spacing: -0.3px; }
QLabel#subtitle { color: $muted; font-size: 13px; }
QLabel#section { font-size: 17px; font-weight: 700; }
QLabel#sectionSub { color: $muted; font-size: 13px; }
QLabel#statValue { font-size: 26px; font-weight: 700; color: $accent; }
QLabel#statLabel { color: $muted; font-size: 12px; font-weight: 600; }
QLabel#bigJapanese { font-family: $font_jp; font-size: 40px; font-weight: 500; }
QLabel#japanese { font-family: $font_jp; font-size: 17px; }
QLabel#japaneseSmall { font-family: $font_jp; font-size: 14px; }
QLabel#romaji { color: $cyan; font-size: 12px; font-style: italic; }
QLabel#meaning { font-size: 13px; }
QLabel#caption { color: $faint; font-size: 12px; }
QLabel#accentText { color: $accent; font-weight: 700; }
QLabel#goldText { color: $gold; font-weight: 700; }
QLabel#successText { color: $success; font-weight: 700; }
QLabel#dangerText { color: $danger; font-weight: 700; }
QLabel#journeyLabel { color: $text; font-size: 14px; }
QLabel#journeyLabel span { color: $muted; }
QLabel#journeyDots { color: $border; font-size: 18px; letter-spacing: 2px; }
QLabel#studyKicker { color: $accent; font-size: 12px; font-weight: 700; letter-spacing: 0.9px; }
QLabel#studyFront { font-family: $font_jp; font-size: 42px; font-weight: 600; }
QLabel#studyBack { font-family: $font_jp; font-size: 16px; }
QLabel#studyHint { color: $faint; font-size: 12px; }
QLabel#chapterIcon {
    background: $accent_dim; color: $accent_soft; border: 1px solid $accent;
    border-radius: 15px; min-width: 46px; max-width: 46px;
    min-height: 46px; max-height: 46px;
    font-family: $font_jp; font-size: 21px; font-weight: 700;
}

QPushButton {
    background: transparent; color: $text; border: 1px solid $border;
    border-radius: 11px; padding: 9px 15px; font-weight: 600;
}
QPushButton:hover { background: $hover; border-color: $accent; }
QPushButton:pressed { background: $surface3; }
QPushButton:disabled { color: $faint; border-color: $border; }
QPushButton#primary {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 $accent,stop:1 $accent_soft);
    color: #1B1710; border: 1px solid $accent;
}
QPushButton#primary:hover { background: $accent_soft; }
QPushButton#ghost { background: transparent; border: 1px solid transparent; color: $muted; }
QPushButton#ghost:hover { background: $hover; color: $text; }
QPushButton#danger { background: transparent; border: 1px solid $danger; color: $danger; }
QPushButton#danger:hover { background: $danger; color: $text; }

QPushButton#navItem {
    background: transparent; border: none; border-left: 3px solid transparent;
    border-radius: 0 10px 10px 0; padding: 9px 12px;
    text-align: left; color: $muted; font-weight: 600;
}
QPushButton#navItem:hover { background: $hover; color: $text; }
QPushButton#navItem:checked {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 $accent_dim,stop:1 transparent);
    border-left: 3px solid $accent; color: $accent_soft;
}
QPushButton#kanaTile {
    background: $surface; border: 1px solid $border; border-radius: 14px;
    padding: 8px; min-width: 72px; min-height: 74px;
}
QPushButton#kanaTile:hover { background: $accent_dim; border-color: $accent; }
QPushButton#answer {
    background: $surface; border: 1px solid $border; border-radius: 13px;
    padding: 13px; text-align: left; font-size: 14px;
}
QPushButton#answer:hover { background: $hover; border-color: $accent; }
QPushButton#answer:checked { background: $accent_dim; border-color: $accent; color: $accent_soft; }
QPushButton#chip {
    background: transparent; border: 1px solid $border; border-radius: 17px;
    padding: 6px 14px; color: $muted; font-size: 12px;
}
QPushButton#chip:checked { background: $accent_dim; color: $accent_soft; border-color: $accent; }
QPushButton#journeyNode {
    background: $surface; border: 2px solid $border; border-radius: 29px;
    min-width: 58px; max-width: 58px; min-height: 58px; max-height: 58px;
    color: $muted; font-size: 15px; font-weight: 700;
}
QPushButton#journeyNode:hover { border-color: $accent; background: $surface2; color: $accent_soft; }
QPushButton#journeyNodeCompleted {
    background: $accent_dim; border: 2px solid $accent; border-radius: 29px;
    min-width: 58px; max-width: 58px; min-height: 58px; max-height: 58px;
    color: $accent_soft; font-size: 21px; font-weight: 800;
}
QPushButton#journeyNodeCompleted:hover { background: $accent; color: #1B1710; }
QPushButton#journeyNodeCurrent {
    background: $accent; border: 2px solid $accent_soft; border-radius: 29px;
    min-width: 58px; max-width: 58px; min-height: 58px; max-height: 58px;
    color: #1B1710; font-size: 16px; font-weight: 800;
}
QPushButton#journeyNodeCurrent:hover { background: $accent_soft; }

QLabel#pill {
    background: $accent_dim; color: $accent_soft; border-radius: 12px;
    padding: 5px 11px; font-size: 12px; font-weight: 700;
}
QLabel#pillGold {
    background: $accent_dim; color: $gold; border-radius: 12px;
    padding: 5px 11px; font-size: 12px; font-weight: 700;
}
QLabel#pillGreen {
    background: $surface3; color: $success; border-radius: 12px;
    padding: 5px 11px; font-size: 12px; font-weight: 700;
}

QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDateEdit, QComboBox {
    background: $input_bg; border: 1px solid $border; border-radius: 11px;
    padding: 10px 13px; selection-background-color: $accent; color: $text;
}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDateEdit:focus, QComboBox:focus {
    border-color: $accent;
}
QLineEdit#search {
    background: $input_bg; border: 1px solid $border; border-radius: 23px;
    padding: 10px 17px; min-width: 240px;
}
QComboBox::drop-down { border: none; width: 22px; }
QComboBox QAbstractItemView {
    background: $surface; border: 1px solid $border; border-radius: 11px;
    selection-background-color: $accent_dim; padding: 5px;
}

QTabWidget::pane { border: none; background: transparent; }
QTabBar { qproperty-drawBase: 0; }
QTabBar::tab {
    background: transparent; color: $muted; border: 1px solid transparent;
    border-radius: 11px; padding: 9px 17px; margin-right: 5px; font-weight: 600;
}
QTabBar::tab:hover { background: $hover; color: $text; }
QTabBar::tab:selected { background: $accent_dim; color: $accent_soft; border-color: $accent; }

QScrollArea { border: none; background: transparent; }
QScrollBar:vertical { background: transparent; width: 10px; margin: 4px; }
QScrollBar::handle:vertical { background: $surface3; border-radius: 5px; min-height: 30px; }
QScrollBar::handle:vertical:hover { background: $accent; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: transparent; height: 10px; margin: 4px; }
QScrollBar::handle:horizontal { background: $surface3; border-radius: 5px; min-width: 30px; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

QListWidget, QTableWidget, QTreeWidget {
    background: $surface; border: 1px solid $border; border-radius: 15px;
    padding: 5px; gridline-color: $border;
}
QListWidget::item { padding: 11px; border-radius: 9px; }
QListWidget::item:hover { background: $hover; }
QListWidget::item:selected { background: $accent_dim; color: $accent_soft; }
QTableWidget::item { padding: 9px; border-bottom: 1px solid $border; }
QHeaderView::section {
    background: $surface2; color: $muted; border: none; border-bottom: 1px solid $border;
    padding: 10px; font-weight: 700;
}

QProgressBar {
    background: $surface3; border-radius: 7px; height: 10px; text-align: center;
    border: none; color: transparent;
}
QProgressBar::chunk { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
    stop:0 $accent, stop:1 $accent_soft); border-radius: 7px; }

QCheckBox { spacing: 9px; font-weight: 600; }
QCheckBox::indicator {
    width: 19px; height: 19px; border-radius: 6px;
    border: 1px solid $border; background: $input_bg;
}
QCheckBox::indicator:checked { background: $accent; border-color: $accent; }
QRadioButton { spacing: 8px; }
QRadioButton::indicator { width: 16px; height: 16px; }
QToolTip {
    background: $surface3; color: $text; border: 1px solid $accent;
    border-radius: 9px; padding: 7px;
}
QStatusBar { color: $muted; }
""")


class Theme:
    def __init__(self, dark: bool = True, font_size: int = 14) -> None:
        self.dark = dark
        self.font_size = font_size
        self.palette = Palette(dark)
        self.font_ui = FONT_UI
        self.font_jp = FONT_JP
        self.font_mono = FONT_MONO
        self.font_ui_primary = FONT_UI_PRIMARY
        self.font_jp_primary = FONT_JP_PRIMARY

    def stylesheet(self) -> str:
        p = self.palette
        return QSS_TEMPLATE.substitute(
            font_ui=FONT_UI, font_jp=FONT_JP, font_px=self.font_size,
            bg=p.bg, bg_alt=p.bg_alt, surface=p.surface, surface2=p.surface2,
            surface3=p.surface3, border=p.border, text=p.text, muted=p.muted,
            faint=p.faint, accent=p.accent, accent_soft=p.accent_soft,
            accent_dim=p.accent_dim, cyan=p.cyan, gold=p.gold, success=p.success,
            danger=p.danger, nav=p.nav, hover=p.hover, input_bg=p.input_bg,
        )


theme = Theme()


def set_theme(dark: bool, font_size: int = 14) -> str:
    global theme
    theme = Theme(dark, font_size)
    return theme.stylesheet()


def load_application_fonts() -> None:
    """Load bundled fonts and any extra fonts dropped into resources/fonts."""
    root = Path(__file__).resolve().parents[1] / "resources" / "fonts"
    if root.exists():
        for font_file in root.rglob("*"):
            if font_file.suffix.lower() in (".ttf", ".otf", ".ttc"):
                QFontDatabase.addApplicationFont(str(font_file))
