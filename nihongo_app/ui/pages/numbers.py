"""Numbers, clocks, dates and time expressions as flashcard decks."""
from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout

from ...core.database import Database
from ...data.intro import (
    DAYS_OF_MONTH, DAYS_OF_WEEK, HOURS, MINUTES, MONTHS, NUMBERS, RELATIVE_TIME,
)
from ..study_deck import StudyDeck, pair_card
from ..widgets import Chip
from .base import Page

MODES = (
    ("count", "数字"),
    ("hours", "時刻"),
    ("minutes", "分"),
    ("dates", "日付・曜日"),
    ("relative", "相対時間"),
)


class NumbersPage(Page):
    def __init__(self, db: Database, window=None) -> None:
        super().__init__(db, window)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 26)
        layout.setSpacing(16)

        title = QLabel("すうじ · Numbers & Time")
        title.setObjectName("title")
        sub = QLabel("一枚ずつ、実際に使う場面ごとに覚えます。")
        sub.setObjectName("subtitle")
        layout.addWidget(title)
        layout.addWidget(sub)

        modes = QHBoxLayout()
        self.chips: dict[str, Chip] = {}
        for key, label in MODES:
            chip = Chip(label)
            chip.setChecked(key == "count")
            chip.clicked.connect(lambda _=False, k=key: self._select(k))
            self.chips[key] = chip
            modes.addWidget(chip)
        modes.addStretch(1)
        layout.addLayout(modes)

        self.deck = StudyDeck(db)
        self.deck.completed.connect(lambda _=None: self.complete_stop("numbers"))
        layout.addWidget(self.deck, 1)
        self.mode = "count"
        self._build_cards()

    def _select(self, mode: str) -> None:
        self.mode = mode
        for key, chip in self.chips.items():
            chip.setChecked(key == mode)
        self._build_cards()

    def _build_cards(self) -> None:
        cards = []
        if self.mode == "count":
            for jp, reading, meaning in NUMBERS:
                cards.append(pair_card(
                    "数字", jp, f"{reading}\n{meaning}",
                    audio=reading, uid=f"n:{jp}"))
        elif self.mode == "hours":
            for display, reading in HOURS:
                cards.append(pair_card("時刻 · じ", display, reading,
                                       audio=reading, uid=f"h:{display}"))
        elif self.mode == "minutes":
            for display, reading in MINUTES:
                cards.append(pair_card("分 · ふん", display, reading,
                                       audio=reading, uid=f"m:{display}"))
        elif self.mode == "dates":
            for jp, reading, romaji, en in DAYS_OF_WEEK:
                cards.append(pair_card(
                    "曜日", jp, f"{reading}\n{romaji} · {en}",
                    audio=reading, uid=f"dow:{jp}"))
            for jp, reading, romaji, en in MONTHS:
                cards.append(pair_card(
                    "月", jp, f"{reading}\n{romaji} · {en}",
                    audio=reading, uid=f"mth:{jp}"))
            for jp, reading in DAYS_OF_MONTH:
                cards.append(pair_card("日", jp, reading, audio=reading, uid=f"dom:{jp}"))
        else:
            for jp, romaji, meaning in RELATIVE_TIME:
                cards.append(pair_card(
                    "相対時間", jp, f"{romaji}\n{meaning}",
                    audio=jp, uid=f"rt:{jp}"))
        self.deck.set_cards(cards)
