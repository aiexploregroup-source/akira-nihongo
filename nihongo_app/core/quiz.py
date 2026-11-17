"""Question generation for vocabulary, grammar and kana practice."""
from __future__ import annotations

import random
from dataclasses import dataclass

from ..data.kana import ALL_KANA
from ..data.registry import ALL_GRAMMAR, ALL_VOCAB
from .models import KanaEntry, QuizQuestion, VocabItem


@dataclass
class DeckInfo:
    key: str
    title: str
    subtitle: str
    items: list[VocabItem]


def build_decks() -> list[DeckInfo]:
    decks = [DeckInfo("all", "All vocabulary",
                      "Every word in the curriculum", list(ALL_VOCAB))]
    for n in range(1, 13):
        items = [v for v in ALL_VOCAB if v.lesson == n]
        if items:
            decks.append(DeckInfo(f"lesson-{n}", f"Lesson {n}", f"{len(items)} words", items))
    return decks


def _choices(correct: str, pool: list[str], count: int = 4) -> tuple[tuple[str, ...], int]:
    options = [correct]
    candidates = [x for x in pool if x != correct]
    random.shuffle(candidates)
    for candidate in candidates:
        if len(options) >= count:
            break
        if candidate not in options:
            options.append(candidate)
    while len(options) < count:
        options.append("—")
    random.shuffle(options)
    return tuple(options), options.index(correct)


def vocab_questions(items: list[VocabItem], mode: str, count: int) -> list[QuizQuestion]:
    pool = list(ALL_VOCAB)
    random.shuffle(items)
    questions: list[QuizQuestion] = []
    for item in items[:count]:
        if mode == "jp_en":
            choices, idx = _choices(item.meaning, [v.meaning for v in pool])
            questions.append(QuizQuestion(
                prompt=item.jp, prompt_sub=item.romaji, choices=choices, answer_index=idx,
                explanation=f"{item.jp} ({item.romaji}) = {item.meaning}",
                source=f"Lesson {item.lesson} · {item.category}", prompt_is_japanese=True))
        elif mode == "en_jp":
            choices, idx = _choices(item.jp, [v.jp for v in pool])
            questions.append(QuizQuestion(
                prompt=item.meaning, prompt_sub="Choose the Japanese",
                choices=choices, answer_index=idx,
                explanation=f"{item.meaning} = {item.jp} ({item.romaji})",
                source=f"Lesson {item.lesson} · {item.category}", prompt_is_japanese=False))
        elif mode == "romaji_jp":
            choices, idx = _choices(item.jp, [v.jp for v in pool])
            questions.append(QuizQuestion(
                prompt=item.romaji, prompt_sub="Choose the Japanese script",
                choices=choices, answer_index=idx,
                explanation=f"{item.romaji} = {item.jp} · {item.meaning}",
                source=f"Lesson {item.lesson} · {item.category}", prompt_is_japanese=False))
        elif mode == "jp_romaji":
            choices, idx = _choices(item.romaji, [v.romaji for v in pool])
            questions.append(QuizQuestion(
                prompt=item.jp, prompt_sub=f"Reading · {item.meaning}",
                choices=choices, answer_index=idx,
                explanation=f"{item.jp} is read {item.romaji} · {item.meaning}",
                source=f"Lesson {item.lesson} · {item.category}", prompt_is_japanese=True))
    return questions


def grammar_questions(count: int, lesson: int | None = None) -> list[QuizQuestion]:
    points = [gp for gp in ALL_GRAMMAR if lesson is None or gp.lesson == lesson]
    if not points:
        points = list(ALL_GRAMMAR)
    random.shuffle(points)
    all_examples = [ex[0] for gp in ALL_GRAMMAR for ex in gp.examples]
    questions: list[QuizQuestion] = []
    for gp in points[:count]:
        if not gp.examples:
            continue
        jp, en = random.choice(gp.examples)
        choices, idx = _choices(jp, all_examples)
        questions.append(QuizQuestion(
            prompt=en, prompt_sub=f"Which Japanese sentence matches? · L{gp.lesson}",
            choices=choices, answer_index=idx,
            explanation=f"{gp.title}: {gp.explanation}\n{jp} — {en}",
            source=f"Grammar · Lesson {gp.lesson}", prompt_is_japanese=False))
    return questions


def kana_questions(count: int, script: str | None = None,
                   modes: tuple[str, ...] = ("char_romaji", "romaji_char"),
                   kinds: tuple[str, ...] = ("basic", "voiced", "contracted")) -> list[QuizQuestion]:
    pool = [k for k in ALL_KANA if k.kind in kinds
            and (script is None or k.script == script)]
    random.shuffle(pool)
    romaji_pool = [k.romaji for k in pool]
    char_pool = [k.char for k in pool]
    questions: list[QuizQuestion] = []
    for i, kana in enumerate(pool[:count]):
        mode = modes[i % len(modes)]
        if mode == "char_romaji":
            choices, idx = _choices(kana.romaji, romaji_pool)
            questions.append(QuizQuestion(
                prompt=kana.char, prompt_sub=f"Read this {kana.script}",
                choices=choices, answer_index=idx,
                explanation=f"{kana.char} = {kana.romaji} · {kana.group}",
                source=f"Kana · {kana.script}", prompt_is_japanese=True))
        else:
            choices, idx = _choices(kana.char, char_pool)
            questions.append(QuizQuestion(
                prompt=kana.romaji, prompt_sub="Choose the correct character",
                choices=choices, answer_index=idx,
                explanation=f"{kana.romaji} = {kana.char} · {kana.group}",
                source=f"Kana · {kana.script}", prompt_is_japanese=False))
    return questions


def kana_typing_targets(script: str | None = None, count: int = 20,
                        kinds: tuple[str, ...] = ("basic", "voiced", "contracted")) -> list[KanaEntry]:
    pool = [k for k in ALL_KANA if k.kind in kinds
            and (script is None or k.script == script)]
    random.shuffle(pool)
    return pool[:count]
