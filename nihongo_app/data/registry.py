"""Central registry: levels, aggregated content and lookup helpers."""
from __future__ import annotations

from dataclasses import dataclass

from ..core.models import GrammarPoint, KanaEntry, Phrase, VocabItem
from .intro import BOWING_NOTES, GREETINGS
from .kana import ALL_KANA, HIRAGANA, KATAKANA
from .lessons_a import LESSONS_A
from .lessons_b import LESSONS_B
from .real_life import SCENARIOS

ALL_LESSONS = LESSONS_A + LESSONS_B
LESSON_BY_NUMBER = {lesson.number: lesson for lesson in ALL_LESSONS}

ALL_VOCAB: list[VocabItem] = []
_seen_vocab: set[str] = set()
for _lesson in ALL_LESSONS:
    for _item in _lesson.vocab:
        if _item.uid not in _seen_vocab:
            _seen_vocab.add(_item.uid)
            ALL_VOCAB.append(_item)

ALL_GRAMMAR: list[GrammarPoint] = [
    gp for lesson in ALL_LESSONS for gp in lesson.grammar
]

ALL_PHRASES: list[Phrase] = list(GREETINGS)
for _lesson in ALL_LESSONS:
    ALL_PHRASES.extend(_lesson.useful)
for _scenario in SCENARIOS:
    ALL_PHRASES.extend(_scenario.phrases)

ALL_KANA_ENTRIES: list[KanaEntry] = ALL_KANA
HIRAGANA_ENTRIES: list[KanaEntry] = HIRAGANA
KATAKANA_ENTRIES: list[KanaEntry] = KATAKANA


@dataclass(frozen=True)
class Level:
    key: str
    jp: str
    en: str
    icon: str
    stage: str
    page: str
    lesson: int | None = None

    @property
    def label(self) -> str:
        return f"{self.icon}  {self.jp}"


LEVELS: list[Level] = [
    Level("foundations", "文字の基礎", "Writing Foundations", "あ", "STAGE 0 · FOUNDATIONS", "foundations"),
    Level("greetings", "あいさつ", "Greetings & Bowing", "◉", "STAGE 1 · FIRST WORDS", "greetings"),
    Level("numbers", "すうじ", "Numbers & Time", "0", "STAGE 1 · FIRST WORDS", "numbers"),
]

for _lesson in ALL_LESSONS:
    LEVELS.append(Level(
        key=f"lesson-{_lesson.number}",
        jp=_lesson.title_jp,
        en=_lesson.title_en,
        icon=str(_lesson.number),
        stage=f"STAGE {_lesson.number // 3 + 2} · LESSON {_lesson.number}",
        page="lesson",
        lesson=_lesson.number,
    ))

LEVELS.append(Level("real-life", "実践日本語", "Real-Life Japanese", "✦", "STAGE 14 · APPLY", "real_life"))
LEVELS.append(Level("planner", "勉強計画", "Study Planner", "▦", "STAGE 14 · APPLY", "planner"))

LEVEL_BY_KEY = {level.key: level for level in LEVELS}


def vocab_for_lesson(number: int) -> list[VocabItem]:
    lesson = LESSON_BY_NUMBER.get(number)
    return list(lesson.vocab) if lesson else []


def grammar_for_lesson(number: int) -> list[GrammarPoint]:
    lesson = LESSON_BY_NUMBER.get(number)
    return list(lesson.grammar) if lesson else []


def search_content(query: str) -> list[tuple[str, str, str, str]]:
    """Return (kind, jp, sub, detail) matches."""
    q = query.strip().lower()
    if not q:
        return []
    results: list[tuple[str, str, str, str]] = []
    for item in ALL_VOCAB:
        hay = f"{item.jp} {item.romaji} {item.meaning}".lower()
        if q in hay:
            results.append(("語彙 · L" + str(item.lesson), item.jp,
                            f"{item.romaji} · {item.category}", item.meaning))
    for gp in ALL_GRAMMAR:
        hay = f"{gp.title} {gp.explanation}".lower()
        if q in hay:
            ex = gp.examples[0][0] if gp.examples else ""
            results.append(("文法 · L" + str(gp.lesson), gp.title, gp.explanation, ex))
    for ph in ALL_PHRASES:
        hay = f"{ph.jp} {ph.romaji} {ph.meaning}".lower()
        if q in hay:
            results.append(("表現", ph.jp, ph.romaji, ph.meaning))
    for kana in ALL_KANA_ENTRIES:
        if q == kana.char.lower() or q == kana.romaji.lower():
            results.append(("文字", kana.char, kana.romaji, f"{kana.script} · {kana.group}"))
    return results[:300]


CULTURE_NOTES: list[tuple[str, str, list[str]]] = [
    (f"Lesson {lesson.number} · {lesson.title_en}", lesson.title_jp, lesson.culture)
    for lesson in ALL_LESSONS if lesson.culture
]
CULTURE_NOTES.insert(0, ("Greetings & Bowing", "あいさつとおじぎ", BOWING_NOTES))
