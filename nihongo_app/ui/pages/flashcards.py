"""Spaced-repetition vocabulary flashcards."""
from __future__ import annotations

import random

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QHBoxLayout, QLabel, QProgressBar, QPushButton,
    QStackedWidget, QVBoxLayout, QWidget,
)

from ...core.database import Database
from ...core.quiz import build_decks
from ...core.srs import schedule
from ...data.registry import ALL_VOCAB, LESSON_BY_NUMBER
from ..speech import speak
from ..i18n import tr
from ..study_deck import scroll_center
from ..theme import theme
from ..widgets import Card, ProgressRing, jp_label, pill
from .base import Page


class FlashcardsPage(Page):
    def __init__(self, db: Database, window=None) -> None:
        super().__init__(db, window)
        self.queue: list = []
        self.index = 0
        self.revealed = False
        self.session_reviewed = 0
        self.session_correct = 0
        self.pending_deck: str | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 26)
        layout.setSpacing(16)
        header = QVBoxLayout()
        title = QLabel("フラッシュカード · Spaced Repetition")
        title.setObjectName("title")
        sub = QLabel("忘れる直前に復習する SM-2 方式で、語彙を長期記憶に定着させます。")
        sub.setObjectName("subtitle")
        header.addWidget(title)
        header.addWidget(sub)
        layout.addLayout(header)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._setup())
        self.stack.addWidget(self._session())
        self.stack.addWidget(self._results())
        layout.addWidget(self.stack, 1)

    def _setup(self) -> QWidget:
        host = QWidget()
        host.setObjectName("root")
        outer = QVBoxLayout(host)
        outer.setContentsMargins(0, 0, 0, 0)
        card = Card("デッキを選ぶ", "Choose a deck and start reviewing")
        card.setMaximumWidth(720)
        self.deck_combo = QComboBox()
        for deck in build_decks():
            self.deck_combo.addItem(f"{deck.title} — {deck.subtitle}", deck.key)
        card.add(QLabel("デッキ · Deck"))
        card.add(self.deck_combo)
        self.direction_combo = QComboBox()
        self.direction_combo.addItems(["日本語 → 意味", "意味 → 日本語", "ローマ字 → 日本語"])
        card.add(QLabel("出題方向 · Direction"))
        card.add(self.direction_combo)
        self.due_only = QCheckBox("復習が届いているカードだけ出す")
        self.due_only.setChecked(False)
        card.add(self.due_only)
        start = QPushButton("レビューを始める  →")
        start.setObjectName("primary")
        start.clicked.connect(self._start)
        card.add(start)
        outer.addWidget(card)
        outer.addStretch(1)
        return host

    def _session(self) -> QWidget:
        inner = QWidget()
        inner.setObjectName("root")
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)
        bar = QHBoxLayout()
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(10)
        self.count_label = QLabel("")
        self.count_label.setObjectName("caption")
        bar.addWidget(self.progress, 1)
        bar.addWidget(self.count_label)
        layout.addLayout(bar)

        self.card = Card(object_name="hero")
        self.card.setMinimumHeight(320)
        self.front_label = QLabel("")
        self.front_label.setObjectName("bigJapanese")
        self.front_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.front_sub = QLabel("")
        self.front_sub.setObjectName("subtitle")
        self.front_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.back_label = QLabel("")
        self.back_label.setObjectName("japanese")
        self.back_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.back_label.setWordWrap(True)
        self.back_label.hide()
        self.card.add(self.front_sub)
        self.card.add(self.front_label)
        self.card.add(self.back_label)
        self.card.stretch()
        layout.addWidget(self.card, 1)

        reveal_row = QHBoxLayout()
        self.reveal_btn = QPushButton("答えを見る  ▼")
        self.reveal_btn.setObjectName("primary")
        self.reveal_btn.clicked.connect(self._reveal)
        self.speak_button = QPushButton("🔊  聞く")
        self.speak_button.setObjectName("ghost")
        self.speak_button.clicked.connect(self._speak)
        reveal_row.addWidget(self.reveal_btn)
        reveal_row.addWidget(self.speak_button)
        reveal_row.addStretch(1)
        layout.addLayout(reveal_row)

        rating_row = QHBoxLayout()
        self.rating_buttons: list[QPushButton] = []
        for label, quality, color in [
            ("もう一度", 0, "danger"), ("むずかしい", 3, ""),
            ("できた", 4, "primary"), ("簡単", 5, ""),
        ]:
            btn = QPushButton(label)
            if color:
                btn.setObjectName(color)
            btn.clicked.connect(lambda _=False, q=quality: self._rate(q))
            btn.hide()
            self.rating_buttons.append(btn)
            rating_row.addWidget(btn)
        layout.addLayout(rating_row)

        host = QWidget()
        host.setObjectName("root")
        host_layout = QVBoxLayout(host)
        host_layout.setContentsMargins(0, 0, 0, 0)
        host_layout.addWidget(scroll_center(inner, max_width=980))
        return host

    def _results(self) -> QWidget:
        host = QWidget()
        host.setObjectName("root")
        layout = QVBoxLayout(host)
        layout.setContentsMargins(0, 0, 0, 0)
        card = Card(object_name="hero")
        card.setMaximumWidth(720)
        self.result_ring = ProgressRing(0.0, "正答率")
        row = QHBoxLayout()
        row.addWidget(self.result_ring)
        self.result_text = QLabel("")
        self.result_text.setObjectName("section")
        self.result_text.setWordWrap(True)
        row.addWidget(self.result_text, 1)
        card.add_layout(row)
        again = QPushButton("別のデッキを選ぶ  →")
        again.setObjectName("primary")
        again.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        card.add(again)
        layout.addWidget(card)
        layout.addStretch(1)
        return host

    def on_navigated(self, deck: str | None = None, **kwargs) -> None:
        if deck:
            self.pending_deck = deck

    def refresh(self) -> None:
        if self.pending_deck:
            index = self.deck_combo.findData(self.pending_deck)
            if index >= 0:
                self.deck_combo.setCurrentIndex(index)
            self.pending_deck = None
            if self.stack.currentIndex() == 0:
                self._start()

    def _start(self) -> None:
        deck_key = self.deck_combo.currentData()
        items = [v for v in ALL_VOCAB if deck_key == "all" or v.lesson == int(deck_key.split("-")[1])]
        if self.due_only.isChecked():
            due = set(self.db.due_items([v.uid for v in items]))
            items = [v for v in items if v.uid in due]
        if not items:
            items = [v for v in ALL_VOCAB if deck_key == "all" or v.lesson == int(deck_key.split("-")[1])]
        random.shuffle(items)
        self.queue = items[:40]
        self.index = 0
        self.session_reviewed = 0
        self.session_correct = 0
        self.stack.setCurrentIndex(1)
        self._show_card()

    def _show_card(self) -> None:
        if self.index >= len(self.queue):
            self._finish()
            return
        item = self.queue[self.index]
        self.current = item
        self.revealed = False
        self.back_label.hide()
        self.reveal_btn.show()
        self.reveal_btn.setText(tr("答えを見る  ▼"))
        for btn in self.rating_buttons:
            btn.hide()
        direction = self.direction_combo.currentIndex()
        if direction == 0:
            front, sub = item.jp, f"{item.lesson} · {item.category}"
            back = f"{item.romaji}\n{item.meaning}"
            self.front_label.setObjectName("bigJapanese")
            self.front_label.setStyleSheet("font-size: 62px;")
        elif direction == 1:
            front, sub = item.meaning, f"{item.lesson} · meaning"
            back = f"{item.jp}\n{item.romaji}"
            self.front_label.setObjectName("title")
            self.front_label.setStyleSheet("font-size: 32px;")
        else:
            front, sub = item.romaji, "romaji reading"
            back = f"{item.jp}\n{item.meaning}"
            self.front_label.setObjectName("title")
            self.front_label.setStyleSheet("font-size: 42px; font-style: italic;")
        self.front_label.setText(front)
        self.front_sub.setText(sub)
        self.back_label.setText(back)
        self.progress.setMaximum(max(1, len(self.queue)))
        self.progress.setValue(self.index)
        self.count_label.setText(f"{self.index + 1} / {len(self.queue)}")
        self.style().polish(self.front_label)

    def _reveal(self) -> None:
        self.revealed = True
        self.back_label.show()
        self.reveal_btn.hide()
        for btn in self.rating_buttons:
            btn.show()

    def _speak(self) -> None:
        speak(self.current.jp)

    def _rate(self, quality: int) -> None:
        result = self.db.get_review(self.current.uid)
        self.db.save_review(schedule(result, quality))
        correct = int(quality >= 3)
        self.db.log_activity(reviewed=1, correct=correct)
        self.session_reviewed += 1
        self.session_correct += correct
        self.index += 1
        self._show_card()

    def _finish(self) -> None:
        ratio = self.session_correct / self.session_reviewed if self.session_reviewed else 0
        self.result_ring.set_value(ratio)
        self.result_text.setText(tr(
            f"{self.session_reviewed} 枚のカードを復習しました。\n"
            f"正答率 {int(ratio * 100)}% · 次回の復習日は自動で設定されます。"))
        self.stack.setCurrentIndex(2)
        if self.window_ref:
            self.window_ref.refresh_all()
