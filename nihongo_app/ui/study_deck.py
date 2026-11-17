"""Single-card interactive study deck used by every teaching page."""
from __future__ import annotations

import html
import random
from dataclasses import dataclass

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QProgressBar, QPushButton, QScrollArea,
    QVBoxLayout, QWidget,
)

from ..core.srs import schedule
from .speech import speak
from .theme import theme, FONT_JP_PRIMARY


@dataclass(frozen=True)
class StudyCard:
    front: str
    back: str
    kicker: str = ""
    audio: str | None = None
    uid: str | None = None


def esc(value: object) -> str:
    return html.escape(str(value)).replace("\n", "<br>")


def scroll_center(widget: QWidget, max_width: int = 1040) -> QScrollArea:
    """Wrap a widget in a scroll area that centres it when space allows.

    The host stretches above and below the content, so the card sits in the
    middle of the canvas on large screens, while small screens get a normal
    vertical scrollbar instead of clipped content.
    """
    scroll = QScrollArea()
    scroll.setObjectName("studyScroll")
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    host = QWidget()
    host.setObjectName("studyHost")
    host_layout = QVBoxLayout(host)
    host_layout.setContentsMargins(22, 14, 22, 14)
    host_layout.setSpacing(0)
    host_layout.addStretch(1)
    widget.setMaximumWidth(max_width)
    host_layout.addWidget(widget, 0, Qt.AlignmentFlag.AlignHCenter)
    host_layout.addStretch(1)
    scroll.setWidget(host)
    return scroll


def phrase_card(kicker: str, jp: str, romaji: str, meaning: str,
                 group: str = "", uid: str | None = None,
                 audio: str | None = None) -> StudyCard:
    back = (
        f"<div style='font-size:15px;'>{esc(romaji)}</div>"
        f"<div style='margin-top:9px; font-size:17px;'>{esc(meaning)}</div>"
    )
    if group:
        back += f"<div style='margin-top:9px; font-size:12px;'>{esc(group)}</div>"
    return StudyCard(front=esc(jp), back=back, kicker=kicker,
                     audio=audio if audio is not None else jp, uid=uid)


def note_card(kicker: str, title: str, body: str,
              uid: str | None = None) -> StudyCard:
    return StudyCard(front=esc(title), back=esc(body), kicker=kicker, uid=uid)


def pair_card(kicker: str, front: str, back: str,
              audio: str | None = None, uid: str | None = None,
              front_is_japanese: bool = True) -> StudyCard:
    return StudyCard(front=esc(front), back=esc(back), kicker=kicker,
                     audio=audio, uid=uid)


class _CardSurface(QFrame):
    clicked = Signal()

    def mousePressEvent(self, event) -> None:  # noqa: N802 - Qt naming
        self.clicked.emit()
        super().mousePressEvent(event)


class StudyDeck(QWidget):
    """Flip, hear, rate and move through content one card at a time."""

    completed = Signal(int)

    def __init__(self, db=None, track: bool = True,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.db = db
        self.track = track
        self.setObjectName("root")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.cards: list[StudyCard] = []
        self.index = 0
        self.revealed = False
        self._build()

    def _build(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        canvas = QWidget()
        canvas.setObjectName("studyCanvas")
        layout = QVBoxLayout(canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        progress_row = QHBoxLayout()
        self.progress = QProgressBar()
        self.progress.setFixedHeight(8)
        self.progress.setTextVisible(False)
        self.count = QLabel("")
        self.count.setObjectName("caption")
        self.shuffle_btn = QPushButton("シャッフル")
        self.shuffle_btn.setObjectName("ghost")
        self.shuffle_btn.clicked.connect(self.shuffle)
        progress_row.addWidget(self.progress, 1)
        progress_row.addWidget(self.count)
        progress_row.addWidget(self.shuffle_btn)
        layout.addLayout(progress_row)

        self.surface = _CardSurface()
        self.surface.setObjectName("hero")
        self.surface.setMinimumHeight(330)
        self.surface.setCursor(Qt.CursorShape.PointingHandCursor)
        self.surface.clicked.connect(self.reveal)
        card_layout = QVBoxLayout(self.surface)
        card_layout.setContentsMargins(30, 26, 30, 26)
        card_layout.setSpacing(14)

        self.kicker = QLabel("")
        self.kicker.setObjectName("studyKicker")
        self.kicker.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.front = QLabel("")
        self.front.setObjectName("studyFront")
        self.front.setFont(QFont(FONT_JP_PRIMARY, 42, QFont.Weight.DemiBold))
        self.front.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.front.setWordWrap(True)
        self.front.setTextFormat(Qt.TextFormat.RichText)

        self.back = QLabel("")
        self.back.setObjectName("studyBack")
        self.back.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.back.setWordWrap(True)
        self.back.setTextFormat(Qt.TextFormat.RichText)
        self.back.hide()

        self.hint = QLabel("カードをタップして答えを見る")
        self.hint.setObjectName("studyHint")
        self.hint.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card_layout.addStretch(1)
        card_layout.addWidget(self.kicker)
        card_layout.addWidget(self.front)
        card_layout.addWidget(self.back)
        card_layout.addWidget(self.hint)
        card_layout.addStretch(1)
        layout.addWidget(self.surface)

        controls = QHBoxLayout()
        self.prev_btn = QPushButton("←  前へ")
        self.prev_btn.clicked.connect(self.previous)
        self.reveal_btn = QPushButton("答えを見る  ▼")
        self.reveal_btn.setObjectName("primary")
        self.reveal_btn.clicked.connect(self.reveal)
        self.audio_btn = QPushButton("🔊  聞く")
        self.audio_btn.setObjectName("ghost")
        self.audio_btn.clicked.connect(self.speak)
        self.next_btn = QPushButton("次へ  →")
        self.next_btn.clicked.connect(self.next)
        controls.addWidget(self.prev_btn)
        controls.addWidget(self.reveal_btn)
        controls.addWidget(self.audio_btn)
        controls.addStretch(1)
        controls.addWidget(self.next_btn)
        layout.addLayout(controls)

        rating = QHBoxLayout()
        self.again_btn = QPushButton("もう一度")
        self.again_btn.setObjectName("danger")
        self.again_btn.clicked.connect(lambda: self.rate(1))
        self.known_btn = QPushButton("できた")
        self.known_btn.setObjectName("primary")
        self.known_btn.clicked.connect(lambda: self.rate(4))
        rating.addWidget(self.again_btn)
        rating.addWidget(self.known_btn)
        rating.addStretch(1)
        layout.addLayout(rating)
        self.rating_widgets = (self.again_btn, self.known_btn)
        for widget in self.rating_widgets:
            widget.hide()

        outer.addWidget(scroll_center(canvas))

    # ------------------------------------------------------------------ cards
    def set_cards(self, cards: list[StudyCard]) -> None:
        # Drop exact duplicates so a deck never shows the same card twice.
        unique: list[StudyCard] = []
        seen: set[tuple[str, str, str]] = set()
        for card in cards:
            key = (card.kicker, card.front, card.back)
            if key in seen:
                continue
            seen.add(key)
            unique.append(card)
        self.cards = unique
        self.index = 0
        self._show()

    @property
    def current(self) -> StudyCard | None:
        if not self.cards:
            return None
        return self.cards[self.index]

    def _show(self) -> None:
        self.revealed = False
        self.back.hide()
        self.hint.show()
        self.reveal_btn.show()
        for widget in self.rating_widgets:
            widget.hide()

        card = self.current
        if card is None:
            self.kicker.setText("")
            self.front.setText("カードがありません")
            self.count.setText("0 / 0")
            self.progress.setMaximum(1)
            self.progress.setValue(0)
            self.audio_btn.setEnabled(False)
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
            self.reveal_btn.setEnabled(False)
            return

        self.kicker.setText(card.kicker)
        self.front.setText(card.front)
        self.back.setText(card.back)
        self.progress.setMaximum(max(1, len(self.cards)))
        self.progress.setValue(self.index + 1)
        self.count.setText(f"{self.index + 1} / {len(self.cards)}")
        self.audio_btn.setEnabled(bool(card.audio))
        self.prev_btn.setEnabled(True)
        self.next_btn.setEnabled(True)
        self.reveal_btn.setEnabled(True)
        self.setFocus()

    def reveal(self) -> None:
        if self.revealed or self.current is None:
            return
        self.revealed = True
        self.back.show()
        self.hint.hide()
        self.reveal_btn.hide()
        for widget in self.rating_widgets:
            widget.show()

    def next(self) -> None:
        if not self.cards:
            return
        self.index = (self.index + 1) % len(self.cards)
        self._show()

    def previous(self) -> None:
        if not self.cards:
            return
        self.index = (self.index - 1) % len(self.cards)
        self._show()

    def shuffle(self) -> None:
        if not self.cards:
            return
        random.shuffle(self.cards)
        self.index = 0
        self._show()

    def speak(self) -> None:
        card = self.current
        if card and card.audio:
            speak(card.audio)

    def rate(self, quality: int) -> None:
        card = self.current
        if card is not None and self.db is not None and self.track:
            if card.uid:
                self.db.save_review(schedule(self.db.get_review(card.uid), quality))
            self.db.log_activity(reviewed=1, correct=int(quality >= 3))
        before = self.index
        self.next()
        if self.index == 0 and len(self.cards) > 1:
            self.completed.emit(len(self.cards))

    def keyPressEvent(self, event) -> None:  # noqa: N802 - Qt naming
        key = event.key()
        if key in (Qt.Key.Key_Space, Qt.Key.Key_Return):
            if self.revealed:
                self.rate(4)
            else:
                self.reveal()
        elif key == Qt.Key.Key_Right:
            self.next()
        elif key == Qt.Key.Key_Left:
            self.previous()
        else:
            super().keyPressEvent(event)
