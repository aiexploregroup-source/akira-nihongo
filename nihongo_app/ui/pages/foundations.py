"""Writing foundations taught one kana or rule at a time."""
from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout

from ...core.database import Database
from ...data.kana import HIRAGANA, KATAKANA, WRITING_SYSTEM
from ..study_deck import StudyDeck, note_card, pair_card
from ..widgets import Chip
from .base import Page

MODES = (
    ("hiragana", "ひらがな"),
    ("katakana", "カタカナ"),
    ("rules", "文字のルール"),
)


class FoundationsPage(Page):
    def __init__(self, db: Database, window=None) -> None:
        super().__init__(db, window)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 26)
        layout.setSpacing(16)

        title = QLabel("文字の基礎 · Writing Foundations")
        title.setObjectName("title")
        sub = QLabel("一枚ずつ、文字とルールを音つきで覚えます。")
        sub.setObjectName("subtitle")
        layout.addWidget(title)
        layout.addWidget(sub)

        modes = QHBoxLayout()
        self.chips: dict[str, Chip] = {}
        for key, label in MODES:
            chip = Chip(label)
            chip.setChecked(key == "hiragana")
            chip.clicked.connect(lambda _=False, k=key: self._select(k))
            self.chips[key] = chip
            modes.addWidget(chip)
        modes.addStretch(1)
        layout.addLayout(modes)

        self.deck = StudyDeck(db)
        self.deck.completed.connect(lambda _=None: self.complete_stop("foundations"))
        layout.addWidget(self.deck, 1)
        self.mode = "hiragana"
        self._build_cards()

    def _select(self, mode: str) -> None:
        self.mode = mode
        for key, chip in self.chips.items():
            chip.setChecked(key == mode)
        self._build_cards()

    def _build_cards(self) -> None:
        if self.mode == "rules":
            cards = [
                note_card("文字のルール", title, f"{subtitle}\n\n{body}")
                for title, subtitle, body in WRITING_SYSTEM
            ]
        else:
            entries = HIRAGANA if self.mode == "hiragana" else KATAKANA
            kicker = "ひらがな" if self.mode == "hiragana" else "カタカナ"
            cards = [
                pair_card(
                    kicker,
                    entry.char,
                    f"{entry.romaji}\n{entry.group}",
                    audio=entry.char,
                    uid=entry.uid,
                )
                for entry in entries
            ]
        self.deck.set_cards(cards)
