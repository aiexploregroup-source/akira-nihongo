"""Typed content models used across the application."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class VocabItem:
    jp: str
    romaji: str
    meaning: str
    category: str = ""
    lesson: int = 0

    @property
    def uid(self) -> str:
        return f"v{self.lesson}:{self.jp}:{self.meaning}"


@dataclass(frozen=True)
class GrammarPoint:
    title: str
    explanation: str
    examples: tuple[tuple[str, str], ...] = ()
    lesson: int = 0

    @property
    def uid(self) -> str:
        return f"g{self.lesson}:{self.title}"


@dataclass(frozen=True)
class Phrase:
    jp: str
    romaji: str
    meaning: str
    group: str = ""


@dataclass(frozen=True)
class KanaEntry:
    char: str
    romaji: str
    group: str
    script: str  # hiragana | katakana
    kind: str = "basic"  # basic | voiced | semi | contracted | extended | special

    @property
    def uid(self) -> str:
        return f"k:{self.script}:{self.char}"


@dataclass
class Lesson:
    number: int
    title_jp: str
    title_en: str
    vocab: list[VocabItem] = field(default_factory=list)
    grammar: list[GrammarPoint] = field(default_factory=list)
    culture: list[str] = field(default_factory=list)
    useful: list[Phrase] = field(default_factory=list)

    @property
    def uid(self) -> str:
        return f"lesson-{self.number}"


@dataclass(frozen=True)
class Scenario:
    key: str
    title_jp: str
    title_en: str
    icon: str
    description: str
    phrases: tuple[Phrase, ...]
    tips: tuple[str, ...] = ()


@dataclass(frozen=True)
class QuizQuestion:
    prompt: str
    prompt_sub: str
    choices: tuple[str, ...]
    answer_index: int
    explanation: str
    source: str
    prompt_is_japanese: bool = True
