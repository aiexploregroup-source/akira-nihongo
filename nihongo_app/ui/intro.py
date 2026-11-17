"""Cinematic, skipable startup sequence for Akira Nihongo."""
from __future__ import annotations

import math
import random

from PySide6.QtCore import (
    QElapsedTimer, QPointF, QRectF, Qt, QTimer, Signal,
)
from PySide6.QtGui import (
    QBrush, QColor, QLinearGradient, QPainter, QPainterPath,
    QPen, QRadialGradient,
)
from PySide6.QtWidgets import QApplication, QWidget

from .logo import logo_pixmap
from .theme import theme


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def _ease(value: float) -> float:
    value = _clamp(value)
    return 1 - (1 - value) ** 3


def _ease_out_back(value: float) -> float:
    value = _clamp(value)
    c1, c3 = 1.35, 2.35
    return 1 + c3 * (value - 1) ** 3 + c1 * (value - 1) ** 2


def _with_alpha(color: QColor | str, alpha: int) -> QColor:
    c = QColor(color)
    c.setAlpha(max(0, min(255, int(alpha))))
    return c


class IntroScreen(QWidget):
    """Frameless animated brand moment shown before the main window."""

    finished = Signal()

    DURATION_MS = 3400

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(
            parent,
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool,
        )
        self.setObjectName("intro")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setStyleSheet("QWidget#intro { background: transparent; }")
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setToolTip("クリック / 任意のキーでスキップ")

        screen = QApplication.primaryScreen()
        available = screen.availableGeometry() if screen else self.geometry()
        width = min(940, max(560, int(available.width() * 0.66)))
        height = min(580, max(420, int(available.height() * 0.68)))
        self.resize(width, height)
        self.move(
            available.x() + (available.width() - width) // 2,
            available.y() + (available.height() - height) // 2,
        )

        rng = random.Random(20261117)
        self._particles = [
            (rng.random(), rng.random(), rng.uniform(0.8, 2.6), rng.uniform(0, math.tau))
            for _ in range(46)
        ]
        self._elapsed = QElapsedTimer()
        self._timer = QTimer(self)
        self._timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._timer.timeout.connect(self._tick)
        self._done = False
        self._elapsed.start()
        self._timer.start(26)

    # ------------------------------------------------------------------ paint
    def paintEvent(self, event) -> None:  # noqa: N802 - Qt naming
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        rect = self.rect().adjusted(1, 1, -1, -1)
        p = theme.palette
        t = _clamp(self._elapsed.elapsed() / self.DURATION_MS)
        gold = QColor(p.gold)
        gold_soft = QColor(p.accent_soft)

        # Lacquer-and-gold base.
        background = QLinearGradient(0, 0, self.width(), self.height())
        background.setColorAt(0.0, QColor("#141A27"))
        background.setColorAt(0.52, QColor("#0D111A"))
        background.setColorAt(1.0, QColor("#191522"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(background))
        painter.drawRoundedRect(rect, 30, 30)

        # Slow aurora ribbons give the intro depth without visual noise.
        for index in range(3):
            base_y = self.height() * (0.16 + index * 0.24)
            drift = math.sin(t * 3.2 + index * 1.7) * 20
            ribbon = QPainterPath()
            ribbon.moveTo(-20, base_y + drift)
            ribbon.cubicTo(
                self.width() * 0.28, base_y - 84 + drift,
                self.width() * 0.66, base_y + 96 + drift,
                self.width() + 20, base_y - 28 + drift,
            )
            ribbon.lineTo(self.width() + 20, self.height() + 20)
            ribbon.lineTo(-20, self.height() + 20)
            ribbon.closeSubpath()
            painter.setBrush(_with_alpha(gold, 7 if index == 1 else 4))
            painter.drawPath(ribbon)

        # Drifting motes.
        for px, py, radius, phase in self._particles:
            x = (px * self.width() + math.sin(t * 2.1 + phase) * 18) % self.width()
            y = (py * self.height() - t * self.height() * 0.22 + phase * 7) % self.height()
            alpha = 22 + int(46 * abs(math.sin(t * 2.4 + phase)))
            painter.setBrush(_with_alpha(gold_soft, alpha))
            painter.drawEllipse(QPointF(x, y), radius, radius)

        center_x = self.width() / 2
        logo_center_y = self.height() * 0.47
        logo_base = min(self.width(), self.height()) * 0.40

        # Expanding halo rings.
        for index in range(3):
            phase = (t * 1.15 + index / 3) % 1
            radius = logo_base * (0.62 + phase * 0.72)
            alpha = int(62 * (1 - phase))
            painter.setPen(QPen(_with_alpha(gold, alpha), 1.4))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(QPointF(center_x, logo_center_y), radius, radius)

        # Soft light behind the emblem.
        halo = QRadialGradient(center_x, logo_center_y, logo_base * 1.08)
        halo.setColorAt(0.0, _with_alpha(gold, 56))
        halo.setColorAt(0.55, _with_alpha(gold, 18))
        halo.setColorAt(1.0, _with_alpha(gold, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(halo))
        painter.drawEllipse(QPointF(center_x, logo_center_y),
                            logo_base * 1.12, logo_base * 1.12)

        # Emblem entrance.
        scale = 0.68 + 0.32 * _ease_out_back(t / 0.34)
        target = max(96, int(logo_base * scale))
        source = logo_pixmap(320)
        pixmap = source.scaled(target, target, Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)
        painter.setOpacity(_ease(t / 0.16))
        painter.drawPixmap(
            int(center_x - pixmap.width() / 2),
            int(logo_center_y - pixmap.height() / 2),
            pixmap,
        )
        painter.setOpacity(1.0)

        # Rising progress arc.
        arc_size = logo_base * 1.34
        arc_rect = QRectF(center_x - arc_size / 2, logo_center_y - arc_size / 2,
                          arc_size, arc_size)
        painter.setPen(QPen(_with_alpha(p.surface3, 210), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawArc(arc_rect, 0, 360 * 16)
        arc_pen = QPen(gold, 4)
        arc_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(arc_pen)
        painter.drawArc(arc_rect, -90 * 16, -int(360 * 16 * _ease(t)))

        # No lettering: the emblem and its motion carry the whole intro.
        # A quiet rail completes the visual rhythm without adding text.
        rail_width = self.width() * 0.30
        rail_x = (self.width() - rail_width) / 2
        rail_y = self.height() - 52
        rail = QRectF(rail_x, rail_y, rail_width, 3)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(p.surface3))
        painter.drawRoundedRect(rail, 1.5, 1.5)
        fill_width = max(3.0, rail_width * _ease(t))
        painter.setBrush(QBrush(gold_soft))
        painter.drawRoundedRect(QRectF(rail_x, rail_y, fill_width, 3), 1.5, 1.5)

    # ------------------------------------------------------------------ flow
    def _tick(self) -> None:
        if self._done:
            return
        self.update()
        if self._elapsed.elapsed() >= self.DURATION_MS:
            self.finish()

    def finish(self) -> None:
        """End the sequence once; safe to call from click, key or timer."""
        if self._done:
            return
        self._done = True
        self._timer.stop()
        self.hide()
        self.finished.emit()

    def mousePressEvent(self, event) -> None:  # noqa: N802 - Qt naming
        self.finish()

    def keyPressEvent(self, event) -> None:  # noqa: N802 - Qt naming
        self.finish()
