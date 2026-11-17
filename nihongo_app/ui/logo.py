"""Akira Nihongo emblem — a pure vector-style mark with no lettering."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import (
    QBrush, QColor, QImage, QLinearGradient, QPainter, QPainterPath, QPen,
    QPixmap, QRadialGradient,
)

from .theme import theme

_cache: dict[int, QPixmap] = {}
VECTOR_LOGO_PATH = Path(__file__).resolve().parents[1] / "resources" / "akira_logo.svg"


def vector_logo_path() -> Path:
    """Return the editable SVG source of the mark."""
    return VECTOR_LOGO_PATH


def _tint(color: QColor | str, alpha: int) -> QColor:
    c = QColor(color)
    c.setAlpha(alpha)
    return c


def _draw_mark(size: int) -> QPixmap:
    image = QImage(size, size, QImage.Format.Format_ARGB32_Premultiplied)
    image.fill(Qt.GlobalColor.transparent)
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
    scale = size / 512.0
    painter.scale(scale, scale)

    pal = theme.palette
    gold = QColor(pal.gold)
    gold_light = QColor(pal.accent_soft)

    # Warm ambient bloom.
    glow = QRadialGradient(256, 236, 235)
    glow.setColorAt(0.0, _tint(gold, 46))
    glow.setColorAt(0.55, _tint(gold, 14))
    glow.setColorAt(1.0, _tint(gold, 0))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QBrush(glow))
    painter.drawEllipse(QRectF(6, 6, 500, 500))

    # Lacquer disc and fine double rim.
    disc = QLinearGradient(0, 40, 0, 470)
    disc.setColorAt(0.0, QColor("#222A44"))
    disc.setColorAt(0.55, QColor("#141A2B"))
    disc.setColorAt(1.0, QColor("#0B0F19"))
    painter.setBrush(QBrush(disc))
    painter.drawEllipse(QRectF(52, 52, 408, 408))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.setPen(QPen(gold, 3))
    painter.drawEllipse(QRectF(52, 52, 408, 408))
    painter.setPen(QPen(_tint(gold, 90), 1.4))
    painter.drawEllipse(QRectF(68, 68, 376, 376))

    # Rising sun above a quiet horizon.
    sun = QLinearGradient(0, 150, 0, 330)
    sun.setColorAt(0.0, gold_light)
    sun.setColorAt(1.0, gold)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QBrush(sun))
    painter.drawChord(QRectF(126, 132, 260, 260), 30 * 16, 120 * 16)
    painter.setPen(QPen(_tint(gold, 170), 2.2,
                        Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
    for y, half in ((322, 132), (338, 96), (352, 62)):
        painter.drawLine(256 - half, y, 256 + half, y)

    # The mark itself: an abstract ascending brushstroke, not a character.
    ascent = QPainterPath()
    ascent.moveTo(158, 322)
    ascent.cubicTo(190, 232, 222, 172, 258, 132)
    ascent.cubicTo(298, 176, 330, 236, 362, 322)

    cross = QPainterPath()
    cross.moveTo(186, 266)
    cross.cubicTo(236, 244, 300, 244, 348, 268)

    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.setPen(QPen(_tint(gold, 70), 36,
                        Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                        Qt.PenJoinStyle.RoundJoin))
    painter.drawPath(ascent)
    painter.setPen(QPen(gold_light, 26,
                        Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                        Qt.PenJoinStyle.RoundJoin))
    painter.drawPath(ascent)

    painter.setPen(QPen(_tint(gold, 70), 26,
                        Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                        Qt.PenJoinStyle.RoundJoin))
    painter.drawPath(cross)
    painter.setPen(QPen(gold, 17,
                        Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                        Qt.PenJoinStyle.RoundJoin))
    painter.drawPath(cross)

    # Finishing swash and Polaris point.
    swash = QPainterPath()
    swash.moveTo(126, 392)
    swash.cubicTo(190, 366, 322, 366, 388, 392)
    painter.setPen(QPen(_tint(gold, 205), 4,
                        Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
    painter.drawPath(swash)

    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QBrush(gold_light))
    painter.drawEllipse(QRectF(250, 74, 12, 12))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.setPen(QPen(_tint(gold, 120), 2))
    painter.drawEllipse(QRectF(246, 70, 20, 20))

    painter.end()
    return QPixmap.fromImage(image)


def logo_pixmap(size: int = 128) -> QPixmap:
    if size not in _cache:
        _cache[size] = _draw_mark(max(64, size))
    return _cache[size]


def clear_logo_cache() -> None:
    _cache.clear()


def save_logo(path: str, size: int = 512) -> bool:
    return logo_pixmap(size).save(path)
