"""Kana drill: recognition multiple-choice and romaji typing."""
from __future__ import annotations

import random

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSpinBox, QStackedWidget, QVBoxLayout, QWidget,
)

from ...core.database import Database
from ...core.quiz import kana_questions, kana_typing_targets
from ...data.kana import ALL_KANA
from ..speech import speak
from ..i18n import tr
from ..theme import theme
from ..widgets import Card, ProgressRing, jp_label, pill
from .base import Page

VARIANTS = {
    "si": "shi", "ti": "chi", "tu": "tsu", "hu": "fu", "zi": "ji",
    "sya": "sha", "syu": "shu", "syo": "sho", "tya": "cha", "tyu": "chu",
    "tyo": "cho", "zya": "ja", "zyu": "ju", "zyo": "jo", "di": "ji", "du": "zu",
}


def normalize(text: str) -> str:
    text = text.strip().lower().replace(" ", "")
    return VARIANTS.get(text, text)


class KanaPracticePage(Page):
    def __init__(self, db: Database, window=None) -> None:
        super().__init__(db, window)
        self.questions = []
        self.typing = []
        self.index = 0
        self.score = 0
        self.answered = False
        self.mode = "choice"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 26)
        layout.setSpacing(16)
        header = QVBoxLayout()
        title = QLabel("文字の練習 · Kana Drill")
        title.setObjectName("title")
        sub = QLabel("ひらがな・カタカナを、認識と入力の両方で素早く思い出せるようにしましょう。")
        sub.setObjectName("subtitle")
        header.addWidget(title)
        header.addWidget(sub)
        layout.addLayout(header)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._setup())
        self.stack.addWidget(self._session())
        self.stack.addWidget(self._results())
        layout.addWidget(self.stack, 1)

    # ------------------------------------------------------------------ setup
    def _setup(self) -> QWidget:
        host = QWidget()
        host.setObjectName("root")
        outer = QVBoxLayout(host)
        outer.setContentsMargins(0, 0, 0, 0)
        card = Card("練習の設定", "Choose your drill")
        card.setMaximumWidth(760)
        grid = QGridLayout()
        grid.setSpacing(12)
        grid.addWidget(QLabel("文字 · Script"), 0, 0)
        self.script_combo = QComboBox()
        self.script_combo.addItems(["ひらがな", "カタカナ", "両方"])
        grid.addWidget(self.script_combo, 0, 1)
        grid.addWidget(QLabel("種類 · Type"), 1, 0)
        self.kind_combo = QComboBox()
        self.kind_combo.addItems(["基本", "基本 + 濁音", "すべて（拗音含む）"])
        grid.addWidget(self.kind_combo, 1, 1)
        grid.addWidget(QLabel("形式 · Mode"), 2, 0)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["選択（文字 → ローマ字）", "入力（ローマ字 → 文字）", "ミックス"])
        grid.addWidget(self.mode_combo, 2, 1)
        grid.addWidget(QLabel("問題数 · Questions"), 3, 0)
        self.count_spin = QSpinBox()
        self.count_spin.setRange(5, 40)
        self.count_spin.setValue(10)
        grid.addWidget(self.count_spin, 3, 1)
        card.add_layout(grid)
        start = QPushButton("練習を始める  →")
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
        layout.setSpacing(14)
        bar = QHBoxLayout()
        self.progress_label = QLabel("")
        self.progress_label.setObjectName("caption")
        self.score_label = pill("正解 0", "green")
        bar.addWidget(self.progress_label)
        bar.addStretch(1)
        bar.addWidget(self.score_label)
        layout.addLayout(bar)

        self.card = Card(object_name="hero")
        self.card.setMinimumHeight(300)
        self.prompt_label = QLabel("")
        self.prompt_label.setObjectName("bigJapanese")
        self.prompt_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prompt_sub = QLabel("")
        self.prompt_sub.setObjectName("subtitle")
        self.prompt_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card.add(self.prompt_sub)
        self.card.add(self.prompt_label)
        self.speak_btn = QPushButton("🔊  発音")
        self.speak_btn.setObjectName("ghost")
        self.speak_btn.clicked.connect(lambda: speak(self.prompt_label.text()))
        self.card.add(self.speak_btn)
        layout.addWidget(self.card, 1)

        self.answer_area = QWidget()
        self.answer_layout = QVBoxLayout(self.answer_area)
        self.answer_layout.setContentsMargins(0, 0, 0, 0)
        self.answer_layout.setSpacing(9)
        layout.addWidget(self.answer_area)

        self.typing_edit = QLineEdit()
        self.typing_edit.setPlaceholderText("ローマ字で入力して Enter…")
        self.typing_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.typing_edit.returnPressed.connect(self._check_typing)
        self.typing_edit.hide()
        layout.addWidget(self.typing_edit)

        self.feedback = QLabel("")
        self.feedback.setObjectName("meaning")
        self.feedback.setWordWrap(True)
        layout.addWidget(self.feedback)

        self.next_btn = QPushButton("次へ  →")
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
        card.setMaximumWidth(720)
        self.result_ring = ProgressRing(0.0, "正答率")
        ring_row = QHBoxLayout()
        ring_row.addWidget(self.result_ring)
        self.result_text = QLabel("")
        self.result_text.setObjectName("section")
        self.result_text.setWordWrap(True)
        ring_row.addWidget(self.result_text, 1)
        card.add_layout(ring_row)
        again = QPushButton("もう一度  →")
        again.setObjectName("primary")
        again.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        card.add(again)
        layout.addWidget(card)
        layout.addStretch(1)
        return host

    # ---------------------------------------------------------------- session
    def _start(self) -> None:
        script = {0: "hiragana", 1: "katakana", 2: None}[self.script_combo.currentIndex()]
        kinds = {
            0: ("basic",), 1: ("basic", "voiced"), 2: ("basic", "voiced", "contracted"),
        }[self.kind_combo.currentIndex()]
        count = self.count_spin.value()
        self.mode = {0: "choice", 1: "typing", 2: "mix"}[self.mode_combo.currentIndex()]
        pool = [k for k in ALL_KANA if k.kind in kinds
                and (script is None or k.script == script)]
        self.questions = []
        self.typing = []
        if self.mode in ("choice", "mix"):
            self.questions = kana_questions(count, script, ("char_romaji",), kinds)
        if self.mode in ("typing", "mix"):
            self.typing = kana_typing_targets(script, count, kinds)
        self.index = 0
        self.score = 0
        self.answered = False
        self.stack.setCurrentIndex(1)
        self._show_question()

    def _show_question(self) -> None:
        total = len(self.questions) + len(self.typing)
        if self.index >= total:
            self._finish()
            return
        self.answered = False
        self.feedback.setText("")
        self.next_btn.hide()
        self.score_label.setText(tr(f"正解 {self.score}"))
        self.progress_label.setText(tr(f"問題 {self.index + 1} / {total}"))
        while self.answer_layout.count():
            item = self.answer_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.typing_edit.hide()
        self.typing_edit.clear()
        self.speak_btn.show()

        if self.index < len(self.questions):
            q = self.questions[self.index]
            self.prompt_label.setText(q.prompt)
            self.prompt_label.setStyleSheet("font-size: 92px;")
            self.prompt_sub.setText(tr("この文字は？"))
            grid = QGridLayout()
            for i, choice in enumerate(q.choices):
                btn = QPushButton(choice)
                btn.setObjectName("answer")
                btn.clicked.connect(lambda _=False, idx=i: self._answer(idx))
                grid.addWidget(btn, i // 2, i % 2)
            self.answer_layout.addLayout(grid)
        else:
            kana = self.typing[self.index - len(self.questions)]
            self.prompt_label.setText(kana.romaji)
            self.prompt_label.setStyleSheet("font-size: 52px;")
            self.prompt_sub.setText(tr("ひらがな / カタカナで入力（ローマ字）"))
            self.typing_edit.show()
            self.typing_edit.setFocus()
            self.speak_btn.hide()

    def _answer(self, idx: int) -> None:
        if self.answered:
            return
        self.answered = True
        q = self.questions[self.index]
        correct = idx == q.answer_index
        self._resolve(correct, q.explanation)

    def _check_typing(self) -> None:
        if self.answered:
            return
        kana = self.typing[self.index - len(self.questions)]
        self.answered = True
        correct = normalize(self.typing_edit.text()) == normalize(kana.romaji)
        self._resolve(correct, f"{kana.romaji} = {kana.char} · {kana.group}")

    def _resolve(self, correct: bool, explanation: str) -> None:
        if correct:
            self.score += 1
            self.feedback.setText(tr(f"✓  正解！  {explanation}"))
            self.feedback.setStyleSheet(f"color: {theme.palette.success}; font-weight: 700;")
        else:
            self.feedback.setText(tr(f"✕  もう一度。  {explanation}"))
            self.feedback.setStyleSheet(f"color: {theme.palette.danger}; font-weight: 700;")
        self.score_label.setText(tr(f"正解 {self.score}"))
        self.db.log_activity(reviewed=1, correct=int(correct))
        self.next_btn.show()
        if self.window_ref:
            self.window_ref._update_pills()

    def _next(self) -> None:
        self.index += 1
        self._show_question()

    def _finish(self) -> None:
        total = len(self.questions) + len(self.typing)
        ratio = self.score / total if total else 0
        self.result_ring.set_value(ratio)
        if ratio >= 0.9:
            msg = "素晴らしい！ 文字がしっかり身についています。"
        elif ratio >= 0.7:
            msg = "いい調子です。間違えた文字を復習しましょう。"
        else:
            msg = "もう一度挑戦して、一文字ずつ覚えていきましょう。"
        self.result_text.setText(tr(f"{self.score} / {total} 正解\n{tr(msg)}"))
        self.stack.setCurrentIndex(2)

    def refresh(self) -> None:
        if self.stack.currentIndex() == 2:
            pass
