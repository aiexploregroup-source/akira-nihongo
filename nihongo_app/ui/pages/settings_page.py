"""Settings, data maintenance and about page."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from PySide6.QtWidgets import (
    QCheckBox, QFileDialog, QHBoxLayout, QLabel, QMessageBox, QPushButton,
    QScrollArea, QSpinBox, QVBoxLayout, QWidget,
)

from ...core.database import Database
from ...data.registry import ALL_GRAMMAR, ALL_LESSONS, ALL_PHRASES, ALL_VOCAB
from ..i18n import tr
from ..theme import theme
from ..widgets import Card, Panel, pill
from .base import Page


class SettingsPage(Page):
    def __init__(self, db: Database, window=None) -> None:
        super().__init__(db, window)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 26)
        layout.setSpacing(14)
        title = QLabel("設定 · Settings")
        title.setObjectName("title")
        sub = QLabel("外観、学習目標、データの管理。")
        sub.setObjectName("subtitle")
        layout.addWidget(title)
        layout.addWidget(sub)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        host = QWidget()
        host.setObjectName("root")
        grid = QVBoxLayout(host)
        grid.setContentsMargins(4, 4, 4, 4)
        grid.setSpacing(16)
        scroll.setWidget(host)
        layout.addWidget(scroll, 1)

        # Appearance
        appearance = Card("外観 · Appearance")
        self.dark_check = QCheckBox("ダークテーマを使う（あきら Premium）")
        self.dark_check.setChecked(db.get_setting("dark_theme", True))
        self.dark_check.stateChanged.connect(self._theme_changed)
        appearance.add(self.dark_check)
        font_row = QHBoxLayout()
        font_row.addWidget(QLabel("文字サイズ · Font size"))
        self.font_spin = QSpinBox()
        self.font_spin.setRange(11, 19)
        self.font_spin.setValue(db.get_setting("font_size", 14))
        self.font_spin.valueChanged.connect(self._font_changed)
        font_row.addWidget(self.font_spin)
        font_row.addStretch(1)
        appearance.add_layout(font_row)
        grid.addWidget(appearance)

        # Learning
        learning = Card("学習 · Learning")
        goal_row = QHBoxLayout()
        goal_row.addWidget(QLabel("1日の目標レビュー数 · Daily goal"))
        self.goal_spin = QSpinBox()
        self.goal_spin.setRange(5, 200)
        self.goal_spin.setValue(db.get_setting("daily_goal", 20))
        self.goal_spin.valueChanged.connect(self._goal_changed)
        goal_row.addWidget(self.goal_spin)
        goal_row.addStretch(1)
        learning.add_layout(goal_row)
        totals = db.totals()
        learning.add(QLabel(
            f"累計レビュー：{totals['reviewed']} 件 · "
            f"正答：{totals['correct']} 件 · "
            f"学習時間：{totals['minutes']} 分"))
        grid.addWidget(learning)

        # Data
        data = Card("データ · Data", "学習記録はこの端末に保存されます。")
        row = QHBoxLayout()
        export = QPushButton("記録をエクスポート")
        export.clicked.connect(self._export)
        row.addWidget(export)
        reset = QPushButton("すべての進捗をリセット")
        reset.setObjectName("danger")
        reset.clicked.connect(self._reset)
        row.addWidget(reset)
        row.addStretch(1)
        data.add_layout(row)
        grid.addWidget(data)

        # About
        about = Card("このアプリについて", "あきら にほんご · 完全自習ジャーニー")
        info = Panel()
        info.add(QLabel(f"収録レッスン：{len(ALL_LESSONS)}"))
        info.add(QLabel(f"収録語彙：{len(ALL_VOCAB)} 語"))
        info.add(QLabel(f"文法ポイント：{len(ALL_GRAMMAR)}"))
        info.add(QLabel(f"実用例・表現：{len(ALL_PHRASES)}"))
        info.add(QLabel("対応範囲：ひらがな・カタカナ・漢字基礎 / greetings / numbers / "
                        " Lessons 1–12 / 実践会話 / 勉強計画"))
        about.add(info)
        shortcuts = QLabel(
            "ショートカット：Ctrl+K で検索 · 左のナビゲーションで各ページへ移動")
        shortcuts.setObjectName("caption")
        about.add(shortcuts)
        about.add(pill("Version 1.1.0", "gold"))
        grid.addWidget(about)
        grid.addStretch(1)

    def _theme_changed(self, state: int) -> None:
        self.db.set_setting("dark_theme", bool(state))
        if self.window_ref:
            self.window_ref._apply_theme()

    def _font_changed(self, value: int) -> None:
        self.db.set_setting("font_size", value)
        if self.window_ref:
            self.window_ref._apply_theme()

    def _goal_changed(self, value: int) -> None:
        self.db.set_setting("daily_goal", value)
        if self.window_ref:
            self.window_ref._update_pills()

    def _export(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, tr("学習記録を保存"), str(Path.home() / f"nihongo-progress-{datetime.now():%Y%m%d}.json"),
            "JSON files (*.json)")
        if not path:
            return
        payload = {
            "exported": datetime.now().isoformat(),
            "settings": {
                "dark_theme": self.db.get_setting("dark_theme", True),
                "font_size": self.db.get_setting("font_size", 14),
                "daily_goal": self.db.get_setting("daily_goal", 20),
            },
            "activity": [dict(r) for r in self.db.conn.execute("SELECT * FROM activity")],
            "lessons": [dict(r) for r in self.db.conn.execute("SELECT * FROM lessons")],
            "planner": self.db.tasks(),
        }
        Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        QMessageBox.information(self, tr("完了"), tr("学習記録をエクスポートしました。"))

    def _reset(self) -> None:
        answer = QMessageBox.question(
            self, tr("確認"), tr("すべての学習記録、レビュー履歴、勉強計画を削除しますか？"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if answer == QMessageBox.StandardButton.Yes:
            self.db.reset_progress()
            if self.window_ref:
                self.window_ref.refresh_all()
            QMessageBox.information(self, tr("完了"), tr("学習記録をリセットしました。"))

    def refresh(self) -> None:
        pass
