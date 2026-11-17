"""Base class shared by all pages."""
from __future__ import annotations

from PySide6.QtWidgets import QWidget

from ..theme import theme


class Page(QWidget):
    def __init__(self, db, window=None) -> None:
        super().__init__()
        self.db = db
        self.window_ref = window
        self.setObjectName("root")

    def navigate(self, key: str, **kwargs) -> None:
        if self.window_ref is not None:
            self.window_ref.navigate(key, **kwargs)

    def refresh(self) -> None:
        """Override in pages that display persisted state."""

    def complete_stop(self, key: str) -> None:
        """Mark a non-lesson journey stop complete and refresh the map."""
        self.db.set_journey_stop(key, True)
        if self.window_ref is not None:
            self.window_ref.refresh_all()

    def on_theme_changed(self) -> None:
        """Override when a page caches palette colours."""
