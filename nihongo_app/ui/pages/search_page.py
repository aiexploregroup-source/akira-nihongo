"""Global search across the whole curriculum."""
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView, QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout,
)

from ...core.database import Database
from ...data.registry import search_content
from ..speech import speak
from ..theme import theme
from ..widgets import Chip, pill
from .base import Page


class SearchPage(Page):
    def __init__(self, db: Database, window=None) -> None:
        super().__init__(db, window)
        self.initial_query = ""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 26)
        layout.setSpacing(14)
        header = QVBoxLayout()
        title = QLabel("検索 · Search")
        title.setObjectName("title")
        sub = QLabel("語彙・文法・表現・文字をまとめて検索できます。")
        sub.setObjectName("subtitle")
        header.addWidget(title)
        header.addWidget(sub)
        layout.addLayout(header)

        bar = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("例：たべる / です / ありがとう / あ")
        self.search.setMinimumHeight(44)
        self.search.textChanged.connect(self._search)
        bar.addWidget(self.search)
        layout.addLayout(bar)

        filter_row = QHBoxLayout()
        self.filters = {}
        for key, label in [("all", "すべて"), ("語彙", "語彙"), ("文法", "文法"),
                           ("表現", "表現"), ("文字", "文字")]:
            chip = Chip(label)
            chip.setChecked(key == "all")
            chip.clicked.connect(lambda _=False, k=key: self._select_filter(k))
            self.filters[key] = chip
            filter_row.addWidget(chip)
        filter_row.addStretch(1)
        self.count_pill = pill("0 件", "green")
        filter_row.addWidget(self.count_pill)
        layout.addLayout(filter_row)
        self.current_filter = "all"

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["種類", "日本語 / 単語", "読み・詳細", "意味 / 例文"])
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        head = self.table.horizontalHeader()
        head.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        head.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        head.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        head.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.doubleClicked.connect(self._speak)
        layout.addWidget(self.table, 1)

    def on_navigated(self, query: str = "", **kwargs) -> None:
        if query:
            self.initial_query = query
            self.search.setText(query)
            self.search.setFocus()
            self._search()

    def _select_filter(self, key: str) -> None:
        self.current_filter = key
        for k, chip in self.filters.items():
            chip.setChecked(k == key)
        self._search()

    def _speak(self, index) -> None:
        item = self.table.item(index.row(), 1)
        if item:
            speak(item.text())

    def _search(self) -> None:
        query = self.search.text().strip()
        results = search_content(query) if query else []
        if self.current_filter != "all":
            results = [r for r in results if r[0].startswith(self.current_filter)]
        self.table.setRowCount(len(results))
        from PySide6.QtGui import QFont
        for row, (kind, jp, sub, detail) in enumerate(results):
            self.table.setItem(row, 0, QTableWidgetItem(kind))
            jp_item = QTableWidgetItem(jp)
            jp_item.setFont(QFont(theme.font_jp_primary, 16))
            self.table.setItem(row, 1, jp_item)
            self.table.setItem(row, 2, QTableWidgetItem(sub))
            self.table.setItem(row, 3, QTableWidgetItem(detail))
        self.count_pill.setText(f"{len(results)} 件")

    def refresh(self) -> None:
        if self.initial_query and not self.search.text():
            self.search.setText(self.initial_query)
            self._search()
