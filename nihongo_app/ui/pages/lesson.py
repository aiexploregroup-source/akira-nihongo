"""Lesson teaching as interactive flashcards — no static tables or lists."""
from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from ...core.database import Database
from ...data.registry import LESSON_BY_NUMBER
from ..study_deck import StudyDeck, note_card, phrase_card
from ..theme import theme
from ..widgets import Card, Chip, pill
from .base import Page

MODES = (
    ("all", "すべて"),
    ("vocab", "語彙"),
    ("grammar", "文法"),
    ("culture", "文化"),
    ("useful", "表現"),
)


class LessonPage(Page):
    def __init__(self, db: Database, window=None, lesson: int = 1) -> None:
        super().__init__(db, window)
        self.lesson = LESSON_BY_NUMBER[lesson]
        self.mode = "all"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 26)
        layout.setSpacing(16)

        header = Card(object_name="hero")
        head_row = QHBoxLayout()
        number = QLabel(str(self.lesson.number))
        number.setStyleSheet(
            f"font-size: 34px; font-weight: 800; color: {theme.palette.gold};")
        title_col = QVBoxLayout()
        jp = QLabel(self.lesson.title_jp)
        jp.setObjectName("japanese")
        jp.setStyleSheet(
            f"font-family: {theme.font_jp_primary}; font-size: 22px; font-weight: 600;")
        en = QLabel(f"Lesson {self.lesson.number} · {self.lesson.title_en}")
        en.setObjectName("subtitle")
        title_col.addWidget(jp)
        title_col.addWidget(en)
        head_row.addWidget(number)
        head_row.addSpacing(10)
        head_row.addLayout(title_col)
        head_row.addStretch(1)
        counts = QHBoxLayout()
        counts.addWidget(pill(f"語彙 {len(self.lesson.vocab)}", "accent"))
        counts.addWidget(pill(f"文法 {len(self.lesson.grammar)}", "gold"))
        counts.addWidget(pill(f"表現 {len(self.lesson.useful)}", "green"))
        head_row.addLayout(counts)
        header.add_layout(head_row)

        actions = QHBoxLayout()
        self.btn_done = QPushButton("✓  この章を完了")
        self.btn_done.setObjectName("primary")
        self.btn_done.clicked.connect(self._toggle_done)
        btn_cards = QPushButton("▤  復習カード")
        btn_cards.clicked.connect(self._open_cards)
        btn_quiz = QPushButton("✓  クイズ")
        btn_quiz.clicked.connect(self._open_quiz)
        actions.addWidget(self.btn_done)
        actions.addWidget(btn_cards)
        actions.addWidget(btn_quiz)
        actions.addStretch(1)
        header.add_layout(actions)
        layout.addWidget(header)

        modes = QHBoxLayout()
        self.chips: dict[str, Chip] = {}
        for key, label in MODES:
            chip = Chip(label)
            chip.setChecked(key == "all")
            chip.clicked.connect(lambda _=False, k=key: self._select(k))
            self.chips[key] = chip
            modes.addWidget(chip)
        modes.addStretch(1)
        layout.addLayout(modes)

        self.deck = StudyDeck(db)
        layout.addWidget(self.deck, 1)
        self._build_cards()

    # ------------------------------------------------------------------ cards
    def _select(self, mode: str) -> None:
        self.mode = mode
        for key, chip in self.chips.items():
            chip.setChecked(key == mode)
        self._build_cards()

    def _build_cards(self) -> None:
        cards = []
        if self.mode in ("all", "vocab"):
            cards.extend(self._vocab_cards())
        if self.mode in ("all", "grammar"):
            cards.extend(self._grammar_cards())
        if self.mode in ("all", "culture"):
            cards.extend(self._culture_cards())
        if self.mode in ("all", "useful"):
            cards.extend(self._useful_cards())
        self.deck.set_cards(cards)

    def _vocab_cards(self):
        return [
            phrase_card("語彙", item.jp, item.romaji, item.meaning,
                        item.category, uid=item.uid)
            for item in self.lesson.vocab
        ]

    def _grammar_cards(self):
        cards = []
        for point in self.lesson.grammar:
            body = point.explanation
            if point.examples:
                body += "\n\n" + "\n".join(
                    f"{jp} — {en}" for jp, en in point.examples
                )
            cards.append(note_card("文法", point.title, body, uid=point.uid))
        return cards

    def _culture_cards(self):
        return [
            note_card("文化", f"文化ノート {index + 1}", note,
                      uid=f"culture-{self.lesson.number}-{index}")
            for index, note in enumerate(self.lesson.culture)
        ]

    def _useful_cards(self):
        return [
            phrase_card("表現", phrase.jp, phrase.romaji, phrase.meaning,
                        phrase.group, uid=f"u:{self.lesson.number}:{phrase.jp}")
            for phrase in self.lesson.useful
        ]

    # ---------------------------------------------------------------- actions
    def _toggle_done(self) -> None:
        done = self.db.lesson_done(self.lesson.uid)
        self.db.mark_lesson(self.lesson.uid, not done)
        self.refresh()
        if self.window_ref:
            self.window_ref.refresh_all()

    def _open_cards(self) -> None:
        self.navigate("flashcards", deck=f"lesson-{self.lesson.number}")

    def _open_quiz(self) -> None:
        self.navigate("quiz", deck=f"lesson-{self.lesson.number}")

    def refresh(self) -> None:
        if not hasattr(self, "btn_done"):
            return
        done = self.db.lesson_done(self.lesson.uid)
        self.btn_done.setText("✓  完了しました" if done else "✓  この章を完了")
        self.btn_done.setObjectName("ghost" if done else "primary")
        self.btn_done.style().polish(self.btn_done)
