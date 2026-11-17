"""Journey-style home: one clear mission and a gently winding path."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QFont
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton, QScrollArea, QVBoxLayout, QWidget,
)

from ...core.database import Database
from ...data.registry import ALL_LESSONS, LEVEL_BY_KEY
from ..speech import speak
from .. import i18n
from ..i18n import tr
from ..theme import theme, FONT_JP_PRIMARY
from ..widgets import Card, ProgressRing, pill
from .base import Page


@dataclass(frozen=True)
class Stop:
    key: str
    nav_key: str
    title: str
    subtitle: str
    icon: str


@dataclass(frozen=True)
class Chapter:
    key: str
    title: str
    subtitle: str
    icon: str
    stops: tuple[Stop, ...]


STOP_DESCRIPTIONS = {
    "foundations": "ひらがな・カタカナの土台を、少しずつ身につけます。",
    "greetings": "まずは挨拶とおじぎ。日本語の第一歩です。",
    "numbers": "数・時間・日付に馴染んで、会話の幅を広げます。",
    "real-life": "習った言葉を、日常の場面で使ってみましょう。",
}


def _make_stop(key: str) -> Stop:
    level = LEVEL_BY_KEY[key]
    nav_key = level.page
    subtitle = level.en
    if key.startswith("lesson-"):
        subtitle = f"Lesson {level.lesson}"
    return Stop(
        key=key,
        nav_key=nav_key,
        title=level.jp,
        subtitle=subtitle,
        icon=level.icon,
    )


CHAPTERS: tuple[Chapter, ...] = (
    Chapter(
        key="begin",
        title="はじまりの道",
        subtitle="文字と、最初のことば",
        icon="あ",
        stops=tuple(_make_stop(key) for key in
                    ("foundations", "greetings", "numbers")),
    ),
    Chapter(
        key="genki-a",
        title="前半",
        subtitle="L1–L6 · 基本の文型をつくる",
        icon="一",
        stops=tuple(_make_stop(f"lesson-{n}") for n in range(1, 7)),
    ),
    Chapter(
        key="genki-b",
        title="後半",
        subtitle="L7–L12 · 表現の幅を広げる",
        icon="二",
        stops=tuple(_make_stop(f"lesson-{n}") for n in range(7, 13)),
    ),
    Chapter(
        key="apply",
        title="実践の森",
        subtitle="使える日本語へ",
        icon="✦",
        stops=(_make_stop("real-life"),),
    ),
)

ALL_STOPS: tuple[Stop, ...] = tuple(
    stop for chapter in CHAPTERS for stop in chapter.stops
)
STOP_BY_KEY = {stop.key: stop for stop in ALL_STOPS}


class JourneyProgress:
    """Derives a guided journey state from persisted progress."""

    def __init__(self, db: Database) -> None:
        self.db = db
        self.done_lessons = set(db.completed_lessons())
        self.done_stops = set(db.journey_stops())

    def is_done(self, key: str) -> bool:
        if key.startswith("lesson-"):
            return key in self.done_lessons
        return key in self.done_stops

    def status(self, key: str) -> str:
        if self.is_done(key):
            return "done"
        if key == self.current_key():
            return "current"
        return "ahead"

    def current_key(self) -> str:
        for stop in ALL_STOPS:
            if not self.is_done(stop.key):
                return stop.key
        return ALL_STOPS[-1].key

    def completed_count(self) -> int:
        return sum(1 for stop in ALL_STOPS if self.is_done(stop.key))

    @property
    def ratio(self) -> float:
        return self.completed_count() / max(1, len(ALL_STOPS))


def _alpha(color: QColor | str, alpha: int) -> QColor:
    c = QColor(color)
    c.setAlpha(max(0, min(255, int(alpha))))
    return c


class JourneyTrail(QWidget):
    """A dotted, winding path with interactive chapter stops."""

    def __init__(self, chapter: Chapter, progress: JourneyProgress,
                 navigate, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.chapter = chapter
        self.progress = progress
        self._buttons: list[QPushButton] = []
        self._labels: list[QLabel] = []
        self._phase = 0.0

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 12)
        layout.setSpacing(8)

        for index, stop in enumerate(chapter.stops):
            button = QPushButton()
            button.setFixedSize(58, 58)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(lambda _=False, k=stop.nav_key: navigate(k))
            self._buttons.append(button)

            label = QLabel()
            label.setObjectName("journeyLabel")
            self._labels.append(label)
            label.setTextFormat(Qt.TextFormat.RichText)
            label.setWordWrap(True)
            label.setMinimumWidth(120)

            row = QHBoxLayout()
            row.setSpacing(12)
            if index % 2 == 0:
                row.addStretch(1)
                row.addWidget(button)
                row.addWidget(label)
                row.addStretch(2)
                label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
            else:
                row.addStretch(2)
                row.addWidget(label)
                row.addWidget(button)
                row.addStretch(1)
                label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            layout.addLayout(row)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._pulse)
        self._timer.start(44)
        self.refresh(progress)

    def _pulse(self) -> None:
        self._phase = (self._phase + 0.024) % 1.0
        self.update()

    def refresh(self, progress: JourneyProgress) -> None:
        self.progress = progress
        for stop, label in zip(self.chapter.stops, self._labels):
            label.setText(
                f"<b>{tr(stop.title)}</b>"
                f"<br><span style='font-size:12px;'>{tr(stop.subtitle)}</span>")
        for stop, button in zip(self.chapter.stops, self._buttons):
            status = progress.status(stop.key)
            if status == "done":
                button.setObjectName("journeyNodeCompleted")
                button.setText("✓")
                button.setToolTip(f"{stop.title} · 完了")
            elif status == "current":
                button.setObjectName("journeyNodeCurrent")
                button.setText(stop.icon)
                button.setToolTip(f"いまここ · {stop.title}")
            else:
                button.setObjectName("journeyNode")
                button.setText(stop.icon)
                button.setToolTip(f"{stop.title} · いつでも挑戦できます")
            button.setAccessibleName(stop.title)
            button.style().polish(button)
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt naming
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        points = [
            QPointF(button.geometry().center().x(), button.geometry().center().y())
            for button in self._buttons
        ]
        if len(points) < 2:
            return

        pal = theme.palette
        gold = QColor(pal.gold)

        # Soft base trail.
        for a, b in zip(points, points[1:]):
            path = QPainterPath(a)
            mid_y = (a.y() + b.y()) / 2
            path.cubicTo(QPointF(a.x(), mid_y), QPointF(b.x(), mid_y), b)
            painter.setPen(QPen(_alpha(pal.border, 150), 9,
                                Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)

        # Completed portion glows gold.
        for index, (a, b) in enumerate(zip(points, points[1:])):
            if not self.progress.is_done(self.chapter.stops[index].key):
                continue
            path = QPainterPath(a)
            mid_y = (a.y() + b.y()) / 2
            path.cubicTo(QPointF(a.x(), mid_y), QPointF(b.x(), mid_y), b)
            painter.setPen(QPen(_alpha(gold, 55), 10,
                                Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawPath(path)
            painter.setPen(QPen(gold, 4,
                                Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawPath(path)

        # Pulse around the current stop.
        current_key = self.progress.current_key()
        for stop, point in zip(self.chapter.stops, points):
            if stop.key != current_key:
                continue
            for offset in (0.0, 0.5):
                phase = (self._phase + offset) % 1.0
                radius = 34 + phase * 26
                painter.setPen(QPen(_alpha(gold, int(86 * (1 - phase))), 2))
                painter.drawEllipse(point, radius, radius)

    def on_theme_changed(self) -> None:
        self.update()


class ChapterCard(QFrame):
    def __init__(self, chapter: Chapter, progress: JourneyProgress,
                 navigate, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("card")
        self.chapter = chapter
        self.progress = progress

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(10)

        header = QHBoxLayout()
        header.setSpacing(12)
        badge = QLabel(chapter.icon)
        badge.setObjectName("chapterIcon")
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.addWidget(badge)

        text = QVBoxLayout()
        title = QLabel(chapter.title)
        title.setObjectName("section")
        subtitle = QLabel(chapter.subtitle)
        subtitle.setObjectName("caption")
        text.addWidget(title)
        text.addWidget(subtitle)
        header.addLayout(text, 1)

        self.progress_pill = pill("0 / 0", "gold")
        header.addWidget(self.progress_pill)

        self.toggle = QPushButton("⌄")
        self.toggle.setObjectName("ghost")
        self.toggle.setFixedWidth(36)
        self.toggle.setToolTip("章を開く / 閉じる")
        self.toggle.clicked.connect(self._toggle)
        header.addWidget(self.toggle)
        root.addLayout(header)

        self.trail = JourneyTrail(chapter, progress, navigate, self)
        root.addWidget(self.trail)

        self.dots = QLabel()
        self.dots.setObjectName("journeyDots")
        root.addWidget(self.dots)

        self._expanded = True
        self.refresh(progress)

    def _toggle(self) -> None:
        self.set_expanded(not self._expanded)

    def set_expanded(self, expanded: bool) -> None:
        self._expanded = expanded
        self.trail.setVisible(expanded)
        self.dots.setVisible(not expanded)
        self.toggle.setText("⌃" if expanded else "⌄")

    def refresh(self, progress: JourneyProgress) -> None:
        self.progress = progress
        done = sum(1 for stop in self.chapter.stops if progress.is_done(stop.key))
        self.progress_pill.setText(f"{done} / {len(self.chapter.stops)}")
        self.trail.refresh(progress)
        self._render_dots()

    def _render_dots(self) -> None:
        pal = theme.palette
        parts = []
        for stop in self.chapter.stops:
            status = self.progress.status(stop.key)
            color = pal.gold if status == "done" else (
                pal.accent_soft if status == "current" else pal.border)
            parts.append(f'<span style="color:{color};">●</span>')
        self.dots.setText("&nbsp;&nbsp;".join(parts))

    def on_theme_changed(self) -> None:
        self.trail.on_theme_changed()
        self._render_dots()


class DashboardPage(Page):
    def __init__(self, db: Database, window=None) -> None:
        super().__init__(db, window)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        host = QWidget()
        host.setObjectName("root")
        self.layout_ = QVBoxLayout(host)
        self.layout_.setContentsMargins(30, 24, 30, 32)
        self.layout_.setSpacing(16)
        scroll.setWidget(host)
        outer.addWidget(scroll)
        self._active_chapter: str | None = None
        self._build()

    # ------------------------------------------------------------------ build
    def _build(self) -> None:
        hero = Card(object_name="hero")
        hero_row = QHBoxLayout()
        hero_row.setSpacing(24)

        hero_text = QVBoxLayout()
        hero_text.setSpacing(7)
        hour = datetime.now().hour
        greeting = "おはようございます" if hour < 11 else (
            "こんにちは" if hour < 17 else "こんばんは")
        hello = QLabel(greeting)
        hello.setFont(QFont(FONT_JP_PRIMARY, 17, QFont.Weight.Medium))
        hello.setStyleSheet(f"color: {theme.palette.gold};")
        eyebrow = QLabel("今日のミッション")
        eyebrow.setObjectName("accentText")
        eyebrow.setStyleSheet("font-size: 12px; font-weight: 700; letter-spacing: 0.8px;")
        self.mission_title = QLabel("学びの旅をはじめよう")
        self.mission_title.setObjectName("title")
        self.mission_desc = QLabel("ひとつずつ、確実に進めていきます。")
        self.mission_desc.setObjectName("subtitle")
        self.mission_desc.setWordWrap(True)
        self.mission_desc.setMaximumWidth(620)

        hero_text.addWidget(hello)
        hero_text.addWidget(eyebrow)
        hero_text.addWidget(self.mission_title)
        hero_text.addWidget(self.mission_desc)

        actions = QHBoxLayout()
        self.btn_continue = QPushButton("ミッションを始める  →")
        self.btn_continue.setObjectName("primary")
        self.btn_continue.clicked.connect(self._continue)
        btn_quiz = QPushButton("クイズで確認")
        btn_quiz.clicked.connect(lambda: self.navigate("quiz"))
        actions.addWidget(self.btn_continue)
        actions.addWidget(btn_quiz)
        actions.addStretch(1)
        hero_text.addSpacing(6)
        hero_text.addLayout(actions)
        hero_row.addLayout(hero_text, 1)

        self.ring = ProgressRing(0.0, "旅の進捗", size=132)
        hero_row.addWidget(self.ring, 0, Qt.AlignmentFlag.AlignCenter)
        hero.add_layout(hero_row)
        self.layout_.addWidget(hero)

        # Quiet, compact status line instead of a wall of statistic cards.
        strip = QFrame()
        strip.setObjectName("panel")
        strip_layout = QHBoxLayout(strip)
        strip_layout.setContentsMargins(20, 14, 20, 14)
        strip_layout.setSpacing(24)
        self.stat_values: dict[str, QLabel] = {}
        for icon, label, key in (
            ("🔥", "連続学習", "streak"),
            ("▤", "今日のレビュー", "today"),
            ("◎", "正答率", "accuracy"),
            ("✓", "完了した章", "lessons"),
        ):
            cell = QVBoxLayout()
            cell.setSpacing(2)
            value = QLabel("0")
            value.setStyleSheet("font-size: 18px; font-weight: 700;")
            caption = QLabel(f"{icon}  {label}")
            caption.setObjectName("statLabel")
            cell.addWidget(value)
            cell.addWidget(caption)
            strip_layout.addLayout(cell)
            self.stat_values[key] = value
        strip_layout.addStretch(1)
        self.layout_.addWidget(strip)

        heading = QLabel("学びの道のり")
        heading.setObjectName("section")
        self.layout_.addWidget(heading)

        self.chapter_cards: list[ChapterCard] = []
        progress = JourneyProgress(self.db)
        for chapter in CHAPTERS:
            card = ChapterCard(chapter, progress, self.navigate, self)
            self.chapter_cards.append(card)
            self.layout_.addWidget(card)
        self.layout_.addStretch(1)

        self.refresh()

    # ----------------------------------------------------------------- journey
    def _continue(self) -> None:
        progress = JourneyProgress(self.db)
        stop = STOP_BY_KEY[progress.current_key()]
        self.navigate(stop.nav_key)

    @staticmethod
    def _description_for(key: str) -> str:
        if key in STOP_DESCRIPTIONS:
            return STOP_DESCRIPTIONS[key]
        level = LEVEL_BY_KEY.get(key)
        if level:
            return f"{level.en} — 語彙・文法・文化をミッションずつ学びます。"
        return "次の一歩を踏み出しましょう。"

    def _chapter_index_for(self, key: str) -> int:
        for index, chapter in enumerate(CHAPTERS):
            if any(stop.key == key for stop in chapter.stops):
                return index
        return 0

    def refresh(self) -> None:
        if not hasattr(self, "chapter_cards"):
            return
        progress = JourneyProgress(self.db)
        current = STOP_BY_KEY[progress.current_key()]
        self.mission_title.setText(current.title)
        self.mission_desc.setText(self._description_for(current.key))

        self.ring.set_value(progress.ratio)
        stats = self.db.today_stats()
        totals = self.db.totals()
        accuracy = int(100 * totals["correct"] / totals["reviewed"]) if totals["reviewed"] else 0
        self.stat_values["streak"].setText(f"{self.db.streak()} 日")
        self.stat_values["today"].setText(f"{stats['reviewed']} 件")
        self.stat_values["accuracy"].setText(f"{accuracy}%")
        self.stat_values["lessons"].setText(
            f"{len(self.db.completed_lessons())} / {len(ALL_LESSONS)}")

        active = self._chapter_index_for(current.key)
        for card in self.chapter_cards:
            card.refresh(progress)
        if active != self._active_chapter:
            self._active_chapter = active
            for index, card in enumerate(self.chapter_cards):
                card.set_expanded(index == active)

    def on_theme_changed(self) -> None:
        for card in self.chapter_cards:
            card.on_theme_changed()
