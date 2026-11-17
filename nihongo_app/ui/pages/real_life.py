"""Real-life Japanese scenarios as interactive flashcard sessions."""
from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QVBoxLayout

from ...core.database import Database
from ...data.real_life import SCENARIOS
from ..study_deck import StudyDeck, note_card, phrase_card
from .base import Page


class RealLifePage(Page):
    def __init__(self, db: Database, window=None) -> None:
        super().__init__(db, window)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 26)
        layout.setSpacing(16)

        title = QLabel("実践日本語 · Real-Life Japanese")
        title.setObjectName("title")
        sub = QLabel("場面を選んで、表現を一枚ずつ練習します。")
        sub.setObjectName("subtitle")
        layout.addWidget(title)
        layout.addWidget(sub)

        choose = QHBoxLayout()
        self.scenario_combo = QComboBox()
        for scenario in SCENARIOS:
            self.scenario_combo.addItem(
                f"{scenario.icon}  {scenario.title_jp} · {scenario.title_en}",
                scenario.key,
            )
        self.scenario_combo.currentIndexChanged.connect(self._build_cards)
        self.scenario_label = QLabel("")
        self.scenario_label.setObjectName("caption")
        choose.addWidget(self.scenario_combo, 1)
        choose.addWidget(self.scenario_label)
        layout.addLayout(choose)

        self.deck = StudyDeck(db)
        self.deck.completed.connect(lambda _=None: self.complete_stop("real-life"))
        layout.addWidget(self.deck, 1)
        self._build_cards()

    def _build_cards(self) -> None:
        key = self.scenario_combo.currentData()
        scenario = next((s for s in SCENARIOS if s.key == key), SCENARIOS[0])
        self.scenario_label.setText(
            f"{len(scenario.phrases)} 表現 · {len(scenario.tips)} コツ")
        cards = [
            phrase_card(
                scenario.title_jp,
                phrase.jp,
                phrase.romaji,
                phrase.meaning,
                phrase.group or scenario.title_en,
                uid=f"sc:{scenario.key}:{phrase.jp}",
            )
            for phrase in scenario.phrases
        ]
        cards.extend(
            note_card("使い方のコツ", f"コツ {index + 1}", tip,
                      uid=f"tip:{scenario.key}:{index}")
            for index, tip in enumerate(scenario.tips)
        )
        self.deck.set_cards(cards)
