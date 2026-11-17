"""Japanese-language study planner with persistence."""
from __future__ import annotations

from datetime import date, timedelta

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QCheckBox, QComboBox, QDateEdit, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QScrollArea, QSpinBox, QVBoxLayout, QWidget,
)

from ...core.database import Database
from ..theme import theme
from ..widgets import Card, Panel, jp_label, pill
from .base import Page

SUBJECTS = [
    "日本語", "復習", "予習", "単語", "漢字", "文法", "会話",
    "リスニング", "読解", "作文", "数学", "英語", "理科", "国語",
    "歴史", "地理", "体育", "音楽", "美術", "情報",
]

PRESETS: list[tuple[str, list[tuple[str, str, int]]]] = [
    ("毎日の基本", [
        ("単語", "新しい単語を20個覚える", 20),
        ("復習", "フラッシュカードを復習する", 15),
        ("漢字", "漢字を10个字書く", 15),
        ("会話", "今日の表現を声に出す", 10),
        ("文法", "文法ポイントを一つ練習する", 20),
        ("読解", "短い文章を読む", 15),
        ("目標", "今週の目標を振り返る", 10),
    ]),
    ("試験対策ウィーク", [
        ("復習", "レッスン1〜4の語彙を復習する", 30),
        ("文法", " helping verb の活用を練習する", 25),
        ("読解", "長文を二つ読む", 25),
        ("リスニング", "会話を聞き取る練習", 20),
        ("作文", "自己紹介を書く", 20),
        ("会話", "ロールプレイをする", 20),
        ("目標", "模擬試験を受ける", 40),
    ]),
]


class PlannerPage(Page):
    def __init__(self, db: Database, window=None) -> None:
        super().__init__(db, window)
        self.week_start = date.today()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 26)
        layout.setSpacing(16)
        header = QVBoxLayout()
        title = QLabel("勉強計画 · Study Planner")
        title.setObjectName("title")
        sub = QLabel("日本語で自分の学習計画を立てましょう。毎日の小さな目標が、N5 への近道です。")
        sub.setObjectName("subtitle")
        header.addWidget(title)
        header.addWidget(sub)
        layout.addLayout(header)

        columns = QHBoxLayout()
        columns.setSpacing(16)
        columns.addWidget(self._form_card(), 0)
        columns.addWidget(self._week_card(), 1)
        layout.addLayout(columns, 1)

    def _form_card(self) -> QWidget:
        card = Card("予定を追加", "Add a task in Japanese")
        card.setMaximumWidth(390)
        self.date_edit = QDateEdit(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd (ddd)")
        card.add(QLabel("日付 · Date"))
        card.add(self.date_edit)

        card.add(QLabel("科目 · Subject"))
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(SUBJECTS)
        card.add(self.subject_combo)

        card.add(QLabel("活動 · Activity"))
        self.activity_edit = QLineEdit()
        self.activity_edit.setPlaceholderText("例：単語を20個復習する")
        card.add(self.activity_edit)

        minutes_row = QHBoxLayout()
        minutes_row.addWidget(QLabel("時間 · Minutes"))
        self.minutes_spin = QSpinBox()
        self.minutes_spin.setRange(5, 240)
        self.minutes_spin.setSingleStep(5)
        self.minutes_spin.setValue(30)
        minutes_row.addWidget(self.minutes_spin)
        card.add_layout(minutes_row)

        card.add(QLabel("メモ · Note"))
        self.note_edit = QLineEdit()
        self.note_edit.setPlaceholderText("例：間違えた語彙を重点的に")
        card.add(self.note_edit)

        add_btn = QPushButton("＋  予定を追加する")
        add_btn.setObjectName("primary")
        add_btn.clicked.connect(self._add_task)
        card.add(add_btn)

        preset_label = QLabel("テンプレート · Presets")
        preset_label.setObjectName("section")
        card.add(preset_label)
        for preset_name, tasks in PRESETS:
            btn = QPushButton(f"✦  {preset_name}（7日分）")
            btn.clicked.connect(lambda _=False, name=preset_name, items=tasks: self._apply_preset(name, items))
            card.add(btn)
        card.stretch()
        return card

    def _week_card(self) -> QWidget:
        card = Card("今週の計画", "This week · 7 days")
        top = QHBoxLayout()
        self.week_label = QLabel("")
        self.week_label.setObjectName("accentText")
        top.addWidget(self.week_label)
        top.addStretch(1)
        self.week_pill = pill("0 件", "green")
        top.addWidget(self.week_pill)
        card.add_layout(top)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.task_host = QWidget()
        self.task_host.setObjectName("root")
        self.task_layout = QVBoxLayout(self.task_host)
        self.task_layout.setContentsMargins(4, 4, 4, 4)
        self.task_layout.setSpacing(7)
        self.scroll.setWidget(self.task_host)
        self.scroll.setMinimumHeight(320)
        card.add(self.scroll)
        return card

    # ---------------------------------------------------------------- actions
    def _add_task(self) -> None:
        activity = self.activity_edit.text().strip()
        if not activity:
            self.activity_edit.setPlaceholderText("⚠  活動を入力してください")
            return
        day = self.date_edit.date().toString("yyyy-MM-dd")
        self.db.add_task(day, self.subject_combo.currentText(), activity,
                         self.minutes_spin.value(), self.note_edit.text().strip())
        self.activity_edit.clear()
        self.note_edit.clear()
        self.refresh()

    def _apply_preset(self, name: str, tasks: list[tuple[str, str, int]]) -> None:
        start = self.date_edit.date().toString("yyyy-MM-dd")
        base = date.fromisoformat(start)
        for offset, (subject, activity, minutes) in enumerate(tasks):
            day = (base + timedelta(days=offset)).isoformat()
            self.db.add_task(day, subject, activity, minutes, f"{name} · {offset + 1}日目")
        self.refresh()

    def _toggle(self, task_id: int) -> None:
        self.db.toggle_task(task_id)
        self.refresh()

    def _delete(self, task_id: int) -> None:
        self.db.delete_task(task_id)
        self.refresh()

    # ---------------------------------------------------------------- render
    def refresh(self) -> None:
        if not hasattr(self, "task_layout"):
            return
        while self.task_layout.count():
            item = self.task_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        start = self.date_edit.date().toString("yyyy-MM-dd")
        end = (date.fromisoformat(start) + timedelta(days=6)).isoformat()
        tasks = [t for t in self.db.tasks() if start <= t["day"] <= end]
        days = sorted({t["day"] for t in tasks})
        for day in days:
            heading = QLabel(f"📅  {day}  ·  {len([t for t in tasks if t['day'] == day])} 件")
            heading.setObjectName("section")
            self.task_layout.addWidget(heading)
            for task in [t for t in tasks if t["day"] == day]:
                self.task_layout.addWidget(self._task_row(task))
        if not tasks:
            empty = QLabel("まだ予定がありません。左のフォームから追加しましょう。")
            empty.setObjectName("subtitle")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.task_layout.addStretch(1)
            self.task_layout.addWidget(empty)
            self.task_layout.addStretch(1)

        done = sum(1 for t in tasks if t["done"])
        self.week_label.setText(f"{start}  →  {end}")
        self.week_pill.setText(f"{len(tasks)} 件 · 完了 {done}")

    def _task_row(self, task: dict) -> QWidget:
        row = Panel()
        layout = QHBoxLayout()
        row.layout_.addLayout(layout)
        check = QCheckBox()
        check.setChecked(bool(task["done"]))
        check.stateChanged.connect(lambda: self._toggle(task["id"]))
        layout.addWidget(check)
        text_col = QVBoxLayout()
        title = jp_label(f"{task['subject']} — {task['activity']}", 15)
        if task["done"]:
            title.setStyleSheet(
                f"color: {theme.palette.faint}; text-decoration: line-through;")
        text_col.addWidget(title)
        sub = QLabel(f"{task['minutes']} 分" + (f"  ·  {task['note']}" if task["note"] else ""))
        sub.setObjectName("caption")
        text_col.addWidget(sub)
        layout.addLayout(text_col, 1)
        delete = QPushButton("✕")
        delete.setObjectName("ghost")
        delete.setToolTip("削除")
        delete.clicked.connect(lambda: self._delete(task["id"]))
        layout.addWidget(delete)
        return row
