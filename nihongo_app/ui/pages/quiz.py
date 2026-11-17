"""Multiple-choice quiz engine for vocabulary, grammar and kana."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QGridLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton,
    QScrollArea, QSpinBox, QStackedWidget, QVBoxLayout, QWidget,
)

from ...core.database import Database
from ...core.quiz import build_decks, grammar_questions, kana_questions, vocab_questions
from ...data.registry import ALL_VOCAB
from ..speech import speak
from ..i18n import tr
from ..theme import theme
from ..widgets import Card, ProgressRing, pill
from .base import Page

TYPES = [
    ("vocab_jp_en", "語彙：日本語 → 意味"),
    ("vocab_en_jp", "語彙：意味 → 日本語"),
    ("vocab_romaji_jp", "語彙：ローマ字 → 日本語"),
    ("vocab_jp_romaji", "語彙：日本語 → 読み方"),
    ("grammar", "文法：英文 → 日本文"),
    ("kana_char", "文字：文字 → ローマ字"),
    ("kana_romaji", "文字：ローマ字 → 文字"),
]


class QuizPage(Page):
    def __init__(self, db: Database, window=None) -> None:
        super().__init__(db, window)
        self.questions: list = []
        self.index = 0
        self.score = 0
        self.answered = False
        self.wrong: list[str] = []
        self.pending_deck: str | None = None

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 26)
        layout.setSpacing(16)
        header = QVBoxLayout()
        title = QLabel("クイズ · Practice Test")
        title.setObjectName("title")
        sub = QLabel("語彙・文法・文字をランダム出題。間違えた問題は解説でその場に定着させましょう。")
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
        card = Card("出題設定", "Configure your quiz")
        card.setMaximumWidth(740)
        card.add(QLabel("問題の種類 · Mode"))
        self.type_combo = QComboBox()
        for key, label in TYPES:
            self.type_combo.addItem(label, key.strip())
        card.add(self.type_combo)
        card.add(QLabel("デッキ · Deck（語彙・文法）"))
        self.deck_combo = QComboBox()
        for deck in build_decks():
            self.deck_combo.addItem(deck.title, deck.key)
        card.add(self.deck_combo)
        card.add(QLabel("問題数 · Questions"))
        self.count_spin = QSpinBox()
        self.count_spin.setRange(5, 40)
        self.count_spin.setValue(10)
        card.add(self.count_spin)
        start = QPushButton("クイズを始める  →")
        start.setObjectName("primary")
        start.clicked.connect(self._start)
        card.add(start)
        outer.addWidget(card)
        outer.addStretch(1)
        return host

    def _session(self) -> QWidget:
        host = QWidget()
        host.setObjectName("root")
        layout = QVBoxLayout(host)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        bar = QHBoxLayout()
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(10)
        self.count_label = QLabel("")
        self.count_label.setObjectName("caption")
        self.score_pill = pill("正解 0", "green")
        bar.addWidget(self.progress, 1)
        bar.addWidget(self.count_label)
        bar.addWidget(self.score_pill)
        layout.addLayout(bar)

        self.card = Card(object_name="hero")
        self.card.setMinimumHeight(210)
        self.prompt = QLabel("")
        self.prompt.setObjectName("bigJapanese")
        self.prompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prompt.setWordWrap(True)
        self.sub = QLabel("")
        self.sub.setObjectName("subtitle")
        self.sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card.add(self.sub)
        self.card.add(self.prompt)
        self.speak_btn = QPushButton("🔊  聞く")
        self.speak_btn.setObjectName("ghost")
        self.speak_btn.clicked.connect(lambda: speak(self.prompt.text()))
        self.card.add(self.speak_btn)
        layout.addWidget(self.card)

        self.answer_widget = QWidget()
        self.answer_layout = QGridLayout(self.answer_widget)
        self.answer_layout.setSpacing(10)
        layout.addWidget(self.answer_widget, 1)

        self.explanation = QLabel("")
        self.explanation.setObjectName("meaning")
        self.explanation.setWordWrap(True)
        layout.addWidget(self.explanation)
        self.next_btn = QPushButton("次の問題へ  →")
        self.next_btn.setObjectName("primary")
        self.next_btn.clicked.connect(self._next)
        self.next_btn.hide()
        layout.addWidget(self.next_btn)
        return host

    def _results(self) -> QWidget:
        host = QWidget()
        host.setObjectName("root")
        layout = QVBoxLayout(host)
        layout.setContentsMargins(0, 0, 0, 0)
        card = Card(object_name="hero")
        row = QHBoxLayout()
        self.result_ring = ProgressRing(0.0, "正答率")
        self.result_text = QLabel("")
        self.result_text.setObjectName("section")
        self.result_text.setWordWrap(True)
        row.addWidget(self.result_ring)
        row.addWidget(self.result_text, 1)
        card.add_layout(row)
        self.wrong_label = QLabel("")
        self.wrong_label.setObjectName("meaning")
        self.wrong_label.setWordWrap(True)
        card.add(self.wrong_label)
        again = QPushButton("もう一度  →")
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
        kind = self.type_combo.currentData()
        count = self.count_spin.value()
        deck = self.deck_combo.currentData()
        if kind.startswith("vocab"):
            items = [v for v in ALL_VOCAB if deck == "all" or v.lesson == int(deck.split("-")[1])]
            self.questions = vocab_questions(items, kind.split("_", 1)[1], count)
        elif kind == "grammar":
            lesson = None if deck == "all" else int(deck.split("-")[1])
            self.questions = grammar_questions(count, lesson)
        elif kind == "kana_char":
            self.questions = kana_questions(count, modes=("char_romaji",))
        else:
            self.questions = kana_questions(count, modes=("romaji_char",))
        self.index = 0
        self.score = 0
        self.wrong = []
        self.stack.setCurrentIndex(1)
        self._show_question()

    def _show_question(self) -> None:
        if self.index >= len(self.questions):
            self._finish()
            return
        q = self.questions[self.index]
        self.answered = False
        self.explanation.setText("")
        self.next_btn.hide()
        self.progress.setMaximum(max(1, len(self.questions)))
        self.progress.setValue(self.index)
        self.count_label.setText(f"{self.index + 1} / {len(self.questions)}")
        self.score_pill.setText(tr(f"正解 {self.score}"))
        self.prompt.setText(q.prompt)
        self.sub.setText(q.prompt_sub)
        self.speak_btn.setVisible(q.prompt_is_japanese)
        while self.answer_layout.count():
            item = self.answer_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for i, choice in enumerate(q.choices):
            btn = QPushButton(choice)
            btn.setObjectName("answer")
            btn.setMinimumHeight(58)
            btn.clicked.connect(lambda _=False, idx=i: self._answer(idx))
            self.answer_layout.addWidget(btn, i // 2, i % 2)

    def _answer(self, idx: int) -> None:
        if self.answered:
            return
        self.answered = True
        q = self.questions[self.index]
        correct = idx == q.answer_index
        if correct:
            self.score += 1
            self.explanation.setText(f"✓  {q.explanation}")
            self.explanation.setStyleSheet(f"color: {theme.palette.success};")
        else:
            self.wrong.append(f"{q.prompt} — {q.choices[q.answer_index]}")
            self.explanation.setText(tr(f"✕  正解は「{q.choices[q.answer_index]}」\n{q.explanation}"))
            self.explanation.setStyleSheet(f"color: {theme.palette.danger};")
        self.score_pill.setText(tr(f"正解 {self.score}"))
        self.db.log_activity(reviewed=1, correct=int(correct))
        self.next_btn.show()
        if self.window_ref:
            self.window_ref._update_pills()

    def _next(self) -> None:
        self.index += 1
        self._show_question()

    def _finish(self) -> None:
        total = len(self.questions)
        ratio = self.score / total if total else 0
        self.result_ring.set_value(ratio)
        if ratio >= 0.9:
            message = "見事！ N5 レベルに近づいています。"
        elif ratio >= 0.7:
            message = "良い結果です。間違えた問題を復習しましょう。"
        else:
            message = "繰り返しが上達のコツ。もう一度挑戦しましょう。"
        self.result_text.setText(tr(f"{self.score} / {total} 正解\n{tr(message)}"))
        if self.wrong:
            self.wrong_label.setText(
                tr("復習する問題：") + "\n"
                + "\n".join("• " + w for w in self.wrong[:8]))
        else:
            self.wrong_label.setText(tr("すべて正解しました！"))
        self.stack.setCurrentIndex(2)
