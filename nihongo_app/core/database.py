"""SQLite persistence for progress, SRS and settings."""
from __future__ import annotations

import json
import sqlite3
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from .srs import ReviewResult, initial_result


class Database:
    def __init__(self, path: str | Path | None = None) -> None:
        if path is None:
            base = Path.home() / ".nihongo_sensei"
            base.mkdir(parents=True, exist_ok=True)
            path = base / "progress.sqlite3"
        self.path = Path(path)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self._create()

    def _create(self) -> None:
        with self.conn:
            self.conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY, value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS reviews (
                    item_id TEXT PRIMARY KEY,
                    ease REAL NOT NULL, interval INTEGER NOT NULL,
                    repetitions INTEGER NOT NULL, due TEXT NOT NULL,
                    lapses INTEGER NOT NULL, last_review TEXT
                );
                CREATE TABLE IF NOT EXISTS lessons (
                    lesson_id TEXT PRIMARY KEY,
                    completed INTEGER NOT NULL DEFAULT 0,
                    best_score INTEGER NOT NULL DEFAULT 0,
                    updated TEXT
                );
                CREATE TABLE IF NOT EXISTS activity (
                    day TEXT PRIMARY KEY, reviewed INTEGER NOT NULL DEFAULT 0,
                    correct INTEGER NOT NULL DEFAULT 0, minutes INTEGER NOT NULL DEFAULT 0
                );
                """
            )

    # ---------- settings ----------
    def get_setting(self, key: str, default: Any = None) -> Any:
        row = self.conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        if row is None:
            return default
        try:
            return json.loads(row["value"])
        except (ValueError, TypeError):
            return row["value"]

    def set_setting(self, key: str, value: Any) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO settings(key,value) VALUES(?,?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (key, json.dumps(value)),
            )

    # ---------- journey ----------
    def journey_stops(self) -> list[str]:
        """Stop keys the learner has explicitly completed on the journey."""
        value = self.get_setting("journey_stops", [])
        return list(value) if isinstance(value, list) else []

    def set_journey_stop(self, key: str, done: bool = True) -> None:
        stops = set(self.journey_stops())
        if done:
            stops.add(key)
        else:
            stops.discard(key)
        self.set_setting("journey_stops", sorted(stops))

    # ---------- SRS ----------
    def get_review(self, item_id: str) -> ReviewResult:
        row = self.conn.execute("SELECT * FROM reviews WHERE item_id=?", (item_id,)).fetchone()
        if row is None:
            return initial_result(item_id)
        return ReviewResult(
            item_id=row["item_id"], ease=row["ease"], interval=row["interval"],
            repetitions=row["repetitions"], due=row["due"], lapses=row["lapses"],
            last_review=row["last_review"] or "",
        )

    def save_review(self, result: ReviewResult) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO reviews VALUES(?,?,?,?,?,?,?) "
                "ON CONFLICT(item_id) DO UPDATE SET ease=excluded.ease, "
                "interval=excluded.interval, repetitions=excluded.repetitions, "
                "due=excluded.due, lapses=excluded.lapses, last_review=excluded.last_review",
                (result.item_id, result.ease, result.interval, result.repetitions,
                 result.due, result.lapses, result.last_review),
            )

    def due_items(self, item_ids: list[str]) -> list[str]:
        today = date.today().isoformat()
        due = []
        for item_id in item_ids:
            row = self.conn.execute(
                "SELECT due FROM reviews WHERE item_id=?", (item_id,)
            ).fetchone()
            if row is None or row["due"] <= today:
                due.append(item_id)
        return due

    # ---------- lessons ----------
    def mark_lesson(self, lesson_id: str, completed: bool, score: int = 0) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT INTO lessons(lesson_id,completed,best_score,updated) VALUES(?,?,?,?) "
                "ON CONFLICT(lesson_id) DO UPDATE SET "
                "completed=excluded.completed, "
                "best_score=MAX(lessons.best_score, excluded.best_score), "
                "updated=excluded.updated",
                (lesson_id, int(completed), score, date.today().isoformat()),
            )

    def lesson_done(self, lesson_id: str) -> bool:
        row = self.conn.execute(
            "SELECT completed FROM lessons WHERE lesson_id=?", (lesson_id,)
        ).fetchone()
        return bool(row and row["completed"])

    def completed_lessons(self) -> list[str]:
        return [r["lesson_id"] for r in self.conn.execute(
            "SELECT lesson_id FROM lessons WHERE completed=1"
        )]

    # ---------- activity ----------
    def log_activity(self, reviewed: int = 0, correct: int = 0, minutes: int = 0) -> None:
        today = date.today().isoformat()
        with self.conn:
            self.conn.execute(
                "INSERT INTO activity(day,reviewed,correct,minutes) VALUES(?,?,?,?) "
                "ON CONFLICT(day) DO UPDATE SET "
                "reviewed=activity.reviewed+excluded.reviewed, "
                "correct=activity.correct+excluded.correct, "
                "minutes=activity.minutes+excluded.minutes",
                (today, reviewed, correct, minutes),
            )

    def today_stats(self) -> dict[str, int]:
        row = self.conn.execute(
            "SELECT * FROM activity WHERE day=?", (date.today().isoformat(),)
        ).fetchone()
        return dict(row) if row else {"reviewed": 0, "correct": 0, "minutes": 0}

    def totals(self) -> dict[str, int]:
        row = self.conn.execute(
            "SELECT COALESCE(SUM(reviewed),0) reviewed, COALESCE(SUM(correct),0) correct, "
            "COALESCE(SUM(minutes),0) minutes FROM activity"
        ).fetchone()
        return dict(row)

    def streak(self) -> int:
        days = {r["day"] for r in self.conn.execute("SELECT day FROM activity WHERE reviewed>0")}
        count = 0
        cursor = date.today()
        if cursor.isoformat() not in days:
            cursor -= timedelta(days=1)
        while cursor.isoformat() in days:
            count += 1
            cursor -= timedelta(days=1)
        return count

    def week_activity(self) -> list[dict[str, Any]]:
        out = []
        for i in range(6, -1, -1):
            day = (date.today() - timedelta(days=i)).isoformat()
            row = self.conn.execute("SELECT * FROM activity WHERE day=?", (day,)).fetchone()
            out.append({"day": day, "reviewed": row["reviewed"] if row else 0,
                        "correct": row["correct"] if row else 0})
        return out

    # ---------- maintenance ----------
    def reset_progress(self) -> None:
        with self.conn:
            for table in ("reviews", "lessons", "activity"):
                self.conn.execute(f"DELETE FROM {table}")

    def close(self) -> None:
        self.conn.close()
