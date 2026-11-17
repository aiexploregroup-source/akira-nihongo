"""Reusable premium UI widgets."""
from __future__ import annotations

from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QColor, QFont, QPainter, QPen, QBrush
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QProgressBar, QPushButton, QVBoxLayout, QWidget,
)

from .theme import theme


class Card(QFrame):
    def __init__(self, title: str | None = None, subtitle: str | None = None,
                 object_name: str = "card", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName(object_name)
        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(22, 20, 22, 20)
        self.root.setSpacing(12)
        if title:
            lbl = QLabel(title)
            lbl.setObjectName("section")
            self.root.addWidget(lbl)
        if subtitle:
            sub = QLabel(subtitle)
            sub.setObjectName("subtitle")
            sub.setWordWrap(True)
            self.root.addWidget(sub)
        self.content = QVBoxLayout()
        self.content.setSpacing(9)
        self.root.addLayout(self.content)

    def add(self, widget: QWidget) -> None:
        self.content.addWidget(widget)

    def add_layout(self, layout) -> None:
        self.content.addLayout(layout)

    def stretch(self) -> None:
        self.content.addStretch(1)


class Panel(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("panel")
        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(14, 12, 14, 12)
        self.layout_.setSpacing(8)

    def add(self, widget: QWidget) -> None:
        self.layout_.addWidget(widget)


class NavButton(QPushButton):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("navItem")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class Chip(QPushButton):
    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("chip")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


def pill(text: str, kind: str = "accent") -> QLabel:
    label = QLabel(text)
    label.setObjectName({"accent": "pill", "gold": "pillGold", "green": "pillGreen"}[kind])
    return label


def jp_label(text: str, size: int = 18, parent: QWidget | None = None) -> QLabel:
    label = QLabel(text, parent)
    label.setObjectName("japanese")
    font = QFont(theme.font_jp_primary, size)
    label.setFont(font)
    label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    return label


class KanaTile(QPushButton):
    def __init__(self, char: str, romaji: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("kanaTile")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.char = char
        self.romaji = romaji
        p = theme.palette
        self.setText(
            f'<div style="text-align:center; line-height:115%;">'
            f'<span style="font-family:{theme.font_jp_primary}; font-size:33px;">{char}</span>'
            f'<br><span style="color:{p.cyan}; font-size:11px;">{romaji}</span></div>'
        )
        self.setToolTip(f"{char} · {romaji}")


class StatCard(Card):
    def __init__(self, value: str, label: str, icon: str = "◆",
                 parent: QWidget | None = None) -> None:
        super().__init__(object_name="panel", parent=parent)
        row = QHBoxLayout()
        ico = QLabel(icon)
        ico.setObjectName("accentText")
        ico.setStyleSheet("font-size: 20px;")
        val = QLabel(value)
        val.setObjectName("statValue")
        row.addWidget(ico)
        row.addStretch(1)
        self.value_label = val
        lbl = QLabel(label)
        lbl.setObjectName("statLabel")
        self.content.addLayout(row)
        self.content.addWidget(val)
        self.content.addWidget(lbl)

    def set_value(self, value: str) -> None:
        self.value_label.setText(value)


class SectionHeader(QWidget):
    def __init__(self, title: str, subtitle: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        col = QVBoxLayout()
        t = QLabel(title)
        t.setObjectName("title")
        s = QLabel(subtitle)
        s.setObjectName("subtitle")
        col.addWidget(t)
        col.addWidget(s)
        layout.addLayout(col)
        layout.addStretch(1)

    def add_widget(self, widget: QWidget) -> None:
        self.layout().addWidget(widget)


class ProgressRing(QWidget):
    value_changed = Signal(float)

    def __init__(self, value: float = 0.0, label: str = "",
                 size: int = 132, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._value = max(0.0, min(1.0, value))
        self._label = label
        self.setFixedSize(size, size)

    def set_value(self, value: float) -> None:
        self._value = max(0.0, min(1.0, value))
        self.value_changed.emit(self._value)
        self.update()

    def set_label(self, label: str) -> None:
        self._label = label
        self.update()

    def paintEvent(self, event) -> None:
        p = theme.palette
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(10, 10, self.width() - 20, self.height() - 20)
        pen = QPen(QColor(p.surface3), 13)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawArc(rect, 0, 360 * 16)
        pen = QPen(QColor(p.accent), 13)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.drawArc(rect, 90 * 16, -int(360 * 16 * self._value))
        painter.setPen(QColor(p.text))
        value_size = 24 if self.width() <= 140 else 27
        font = QFont(theme.font_ui_primary, value_size, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{int(self._value * 100)}%")
        font = QFont(theme.font_ui_primary, 10)
        painter.setFont(font)
        painter.setPen(QColor(p.muted))
        painter.drawText(QRectF(10, self.height() - 34, self.width() - 20, 22),
                         Qt.AlignmentFlag.AlignCenter, self._label)


class SparkBars(QWidget):
    def __init__(self, values: list[int], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.values = values
        self.setFixedHeight(92)

    def set_values(self, values: list[int]) -> None:
        self.values = values
        self.update()

    def paintEvent(self, event) -> None:
        p = theme.palette
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if not self.values:
            return
        maximum = max(max(self.values), 1)
        count = len(self.values)
        gap = 8
        bar_w = (self.width() - gap * (count - 1)) / count
        for i, value in enumerate(self.values):
            x = i * (bar_w + gap)
            h = max(5, (value / maximum) * (self.height() - 22))
            y = self.height() - h - 16
            color = QColor(p.accent) if i == count - 1 else QColor(p.surface3)
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(x, y, bar_w, h), 5, 5)
            painter.setPen(QColor(p.faint))
            font = QFont(theme.font_ui_primary, 9)
            painter.setFont(font)
            painter.drawText(QRectF(x, self.height() - 14, bar_w, 14),
                             Qt.AlignmentFlag.AlignCenter, str(value))


class SkillBar(QWidget):
    def __init__(self, label: str, value: int, total: int, color: str = "accent",
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        row = QHBoxLayout()
        name = QLabel(label)
        count = QLabel(f"{value} / {total}")
        count.setObjectName("caption")
        row.addWidget(name)
        row.addStretch(1)
        row.addWidget(count)
        layout.addLayout(row)
        bar = QProgressBar()
        bar.setFixedHeight(8)
        bar.setValue(int(100 * value / total) if total else 0)
        bar.setTextVisible(False)
        if color == "gold":
            bar.setStyleSheet(
                f"QProgressBar::chunk {{ background: {theme.palette.gold}; }}")
        layout.addWidget(bar)


class EmptyState(QWidget):
    def __init__(self, icon: str, title: str, message: str,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 46px; color: {theme.palette.accent};")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label = QLabel(title)
        title_label.setObjectName("section")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg = QLabel(message)
        msg.setObjectName("subtitle")
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg.setWordWrap(True)
        layout.addStretch(1)
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(msg)
        layout.addStretch(1)
