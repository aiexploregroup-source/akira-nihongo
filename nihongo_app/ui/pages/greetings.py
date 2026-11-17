"""Greetings and bowing culture as interactive flashcards."""
from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout

from ...core.database import Database
from ...data.intro import BOWING_NOTES, GREETINGS
from ..study_deck import StudyDeck, note_card, phrase_card
from ..widgets import Chip
from .base import Page


class GreetingsPage(Page):
    def __init__(self, db: Database, window=None) -> None:
        super().__init__(db, window)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 26)
        layout.setSpacing(16)

        title = QLabel("あいさつ · Greetings")
        title.setObjectName("title")
        sub = QLabel("一枚ずつ、場面に合った表現を音と意味で覚えます。")
        sub.setObjectName("subtitle")
        layout.addWidget(title)
        layout.addWidget(sub)

        modes = QHBoxLayout()
        self.chips: dict[str, Chip] = {}
        for key, label in (("phrases", "あいさつ"), ("culture", "おじぎの文化")):
            chip = Chip(label)
            chip.setChecked(key == "phrases")
            chip.clicked.connect(lambda _=False, k=key: self._select(k))
            self.chips[key] = chip
            modes.addWidget(chip)
        modes.addStretch(1)
        layout.addLayout(modes)

        self.deck = StudyDeck(db)
        self.deck.completed.connect(lambda _=None: self.complete_stop("greetings"))
        layout.addWidget(self.deck, 1)
        self.mode = "phrases"
        self._build_cards()

    def _select(self, mode: str) -> None:
        self.mode = mode
        for key, chip in self.chips.items():
            chip.setChecked(key == mode)
        self._build_cards()

    def _build_cards(self) -> None:
        if self.mode == "culture":
            cards = [
                note_card("文化 · おじぎ", f"おじぎ {index + 1}", note)
                for index, note in enumerate(BOWING_NOTES)
            ]
        else:
            cards = [
                phrase_card("あいさつ", phrase.jp, phrase.romaji,
                            phrase.meaning, phrase.group, uid=f"p:{phrase.jp}")
                for phrase in GREETINGS
            ]
        self.deck.set_cards(cards)
