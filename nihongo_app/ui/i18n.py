"""Persistent Japanese/English UI language switching.

The learning content (vocabulary, kana, example sentences) always stays in
Japanese — only the application chrome is translated.  The selected language
is stored in the settings table so it becomes the default on every launch.
"""
from __future__ import annotations

import re
from typing import Any

LANG_SETTING = "language"
SUPPORTED = ("ja", "en")
LANG_LABELS = {"ja": "🌐 English", "en": "🌐 日本語"}

_lang = "ja"


# ------------------------------------------------------------------- state
def normalize(lang: str | None) -> str:
    value = (lang or "ja").strip().lower()
    if value.startswith("en"):
        return "en"
    return "ja"


def load(db: Any) -> str:
    """Load the persisted language (defaults to Japanese)."""
    global _lang
    _lang = normalize(db.get_setting(LANG_SETTING, "ja")) if db is not None else "ja"
    return _lang


def current() -> str:
    return _lang


def set_language(lang: str, db: Any = None) -> str:
    global _lang
    _lang = normalize(lang)
    if db is not None:
        db.set_setting(LANG_SETTING, _lang)
    return _lang


def toggle(db: Any = None) -> str:
    return set_language("ja" if _lang == "en" else "en", db)


def is_english() -> bool:
    return _lang == "en"


# -------------------------------------------------------------- dictionary
JA_EN: dict[str, str] = {
    # brand / global
    "学びの旅へ戻る": "Back to your journey",
    "ゼロから N5 への旅": "Your journey to N5",
    "テーマを切り替え (Ctrl+T)": "Toggle theme (Ctrl+T)",
    "テーマを切り替え": "Toggle theme",
    "⚙  設定": "⚙  Settings",
    "今日の一歩から、N5 へ": "One step at a time, toward N5",
    "⌕  ことばを探す…  (Ctrl+K)": "⌕  Search words…  (Ctrl+K)",
    "あきら にほんご について": "About あきら にほんご",
    "あきら にほんご · N5 への旅": "Akira Nihongo · Journey to N5",
    "あきら にほんご · ゼロから N5 への旅": "Akira Nihongo · From zero to N5",
    "おはようございます": "Good morning",
    "こんにちは": "Good afternoon",
    "こんばんは": "Good evening",

    # menu bar
    "旅": "Journey",
    "ホーム · 学びの旅": "Home · Journey",
    "学習": "Learn",
    "章": "Chapters",
    "12 章": "12 Chapters",
    "実践": "Apply",
    "練習": "Practice",
    "表示": "View",
    "検索": "Search",
    "設定": "Settings",
    "ヘルプ": "Help",
    "その他": "More",

    # navigation / page titles
    "学びの旅": "Journey",
    "学びの道のり": "Your learning path",
    "文字の基礎": "Writing Foundations",
    "あいさつ": "Greetings",
    "すうじ": "Numbers & Time",
    "実践日本語": "Real-Life Japanese",
    "文字の練習": "Kana Practice",
    "フラッシュカード": "Flashcards",
    "クイズ": "Quiz",
    "文字の練習 · ひらがな・カタカナをやさしく反復": "Kana Practice",
    "フラッシュカード · 間隔反復で語彙を定着させる": "Flashcards",
    "クイズ · 語彙・文法・文字をまとめて確認": "Quiz",
    "検索 · 教材全体をひとつの検索欄から": "Search",
    "設定 · 外観・目標・データの管理": "Settings",

    # dashboard
    "今日のミッション": "Today's mission",
    "学びの旅をはじめよう": "Start your journey",
    "ひとつずつ、確実に進めていきます。": "Make steady progress, one step at a time.",
    "ミッションを始める  →": "Start mission  →",
    "クイズで確認": "Check with a quiz",
    "旅の進捗": "Journey progress",
    "連続学習": "Streak",
    "今日のレビュー": "Reviews today",
    "正答率": "Accuracy",
    "完了した章": "Chapters done",
    "はじまりの道": "The Beginning Path",
    "文字と、最初のことば": "Characters and your first words",
    "前半": "Lessons 1–6",
    "L1–L6 · 基本の文型をつくる": "L1–L6 · Build core sentence patterns",
    "後半": "Lessons 7–12",
    "L7–L12 · 表現の幅を広げる": "L7–L12 · Expand your expression",
    "実践の森": "Practice Forest",
    "使える日本語へ": "Toward usable Japanese",
    "章を開く / 閉じる": "Expand / collapse chapter",
    "完了": "Done",
    "いまここ": "You are here",
    "いつでも挑戦できます": "Practice anytime",
    "ひらがな・カタカナの土台を、少しずつ身につけます。":
        "Build a solid hiragana & katakana foundation, little by little.",
    "まずは挨拶とおじぎ。日本語の第一歩です。":
        "Start with greetings and bowing — your first step in Japanese.",
    "数・時間・日付に馴染んで、会話の幅を広げます。":
        "Get comfortable with numbers, time and dates to widen your conversation.",
    "習った言葉を、日常の場面で使ってみましょう。":
        "Try using what you have learned in everyday situations.",
    "語彙・文法・文化をミッションずつ学びます。":
        "Learn vocabulary, grammar and culture one mission at a time.",
    "次の一歩を踏み出しましょう。": "Take your next step.",

    # study deck
    "シャッフル": "Shuffle",
    "カードをタップして答えを見る": "Tap the card to reveal the answer",
    "カードがありません": "No cards available",
    "←  前へ": "←  Previous",
    "答えを見る  ▼": "Show answer  ▼",
    "🔊  聞く": "🔊  Listen",
    "次へ  →": "Next  →",
    "もう一度": "Again",
    "できた": "Got it",
    "語彙": "Vocabulary",
    "文法": "Grammar",
    "文化": "Culture",
    "表現": "Expressions",
    "すべて": "All",
    "文字のルール": "Writing rules",
    "相対時間": "Relative time",
    "日付・曜日": "Dates & weekdays",
    "おじぎの文化": "Bowing culture",
    "使い方のコツ": "Usage tips",
    "文化ノート": "Culture note",

    # page headers
    "あいさつ · Greetings": "Greetings",
    "すうじ · Numbers & Time": "Numbers & Time",
    "文字の基礎 · Writing Foundations": "Writing Foundations",
    "実践日本語 · Real-Life Japanese": "Real-Life Japanese",
    "設定 · Settings": "Settings",
    "検索 · Search": "Search",
    "一枚ずつ、場面に合った表現を音と意味で覚えます。":
        "Learn situation-appropriate expressions one card at a time, with sound and meaning.",
    "一枚ずつ、実際に使う場面ごとに覚えます。":
        "Learn one card at a time, grouped by real-life use.",
    "一枚ずつ、文字とルールを音つきで覚えます。":
        "Learn characters and rules one card at a time, with audio.",
    "場面を選んで、表現を一枚ずつ練習します。":
        "Pick a scenario and practise its expressions one card at a time.",
    "語彙・文法・表現・文字をまとめて検索できます。":
        "Search vocabulary, grammar, phrases and characters all at once.",
    "この章を完了": "Complete this chapter",
    "完了しました": "Completed",
    "この章を完了する": "Complete this chapter",
    "復習カード": "Review cards",
    "▤  復習カード": "▤  Review cards",
    "✓  クイズ": "✓  Quiz",
    "✓  この章を完了": "✓  Complete this chapter",
    "✓  完了しました": "✓  Completed",

    # settings page
    "外観、学習目標、データの管理。": "Appearance, goals and data management.",
    "外観 · Appearance": "Appearance",
    "ダークテーマを使う（あきら Premium）": "Use dark theme (Akira Premium)",
    "文字サイズ · Font size": "Font size",
    "学習 · Learning": "Learning",
    "1日の目標レビュー数 · Daily goal": "Daily review goal",
    "データ · Data": "Data",
    "学習記録はこの端末に保存されます。": "Progress is stored on this device.",
    "記録をエクスポート": "Export progress",
    "すべての進捗をリセット": "Reset all progress",
    "このアプリについて": "About this app",
    "あきら にほんご · 完全自習ジャーニー": "あきら にほんご · Complete self-study journey",
    "収録レッスン": "Lessons included",
    "収録語彙": "Vocabulary",
    "文法ポイント": "Grammar points",
    "実用例・表現": "Phrases & expressions",
    "対応範囲": "Coverage",
    "ショートカット：Ctrl+K で検索 · 左のナビゲーションで各ページへ移動":
        "Shortcuts: Ctrl+K to search · use the navigation on the left to move between pages",
    "学習記録を保存": "Save study record",
    "学習記録をエクスポートしました。": "Study record exported.",
    "確認": "Confirm",
    "すべての学習記録とレビュー履歴を削除しますか？":
        "Delete all study records and review history?",
    "学習記録をリセットしました。": "Study record reset.",
    "はい": "Yes",
    "いいえ": "No",

    # flashcards page
    "フラッシュカード · Spaced Repetition": "Flashcards · Spaced Repetition",
    "忘れる直前に復習する SM-2 方式で、語彙を長期記憶に定着させます。":
        "Review just before you forget with SM-2 scheduling to build lasting vocabulary.",
    "デッキを選ぶ": "Choose a deck",
    "デッキ · Deck": "Deck",
    "別のデッキを選ぶ  →": "Choose another deck  →",
    "むずかしい": "Difficult",
    "レビューを始める  →": "Start review  →",
    "ローマ字 → 日本語": "Romaji → Japanese",
    "復習が届いているカードだけ出す": "Only show due cards",
    "▤  今日のレビュー": "▤  Reviews today",
    "✓  完了した章": "✓  Chapters done",

    # quiz page
    "クイズ · Practice Test": "Quiz · Practice Test",
    "語彙・文法・文字をランダム出題。間違えた問題は解説でその場に定着させましょう。":
        "Random questions on vocabulary, grammar and characters. Learn from each explanation.",
    "問題の種類 · Mode": "Question mode",
    "デッキ · Deck（語彙・文法）": "Deck (vocabulary & grammar)",
    "もう一度  →": "Try again  →",
    "次の問題へ  →": "Next question  →",
    "クイズを始める  →": "Start quiz  →",
    "語彙：日本語 → 意味": "Vocabulary: Japanese → Meaning",
    "語彙：意味 → 日本語": "Vocabulary: Meaning → Japanese",
    "語彙：ローマ字 → 日本語": "Vocabulary: Romaji → Japanese",
    "語彙：日本語 → 読み方": "Vocabulary: Japanese → Reading",
    "文法：英文 → 日本文": "Grammar: English → Japanese",
    "文字：文字 → ローマ字": "Characters: Character → Romaji",
    "文字：ローマ字 → 文字": "Characters: Romaji → Character",

    # kana practice page
    "文字の練習 · Kana Drill": "Kana Practice",
    "ひらがな・カタカナを、認識と入力の両方で素早く思い出せるようにしましょう。":
        "Recall hiragana and katakana quickly through both recognition and typing.",
    "練習の設定": "Practice settings",
    "練習を始める  →": "Start practice  →",
    "すべて（拗音含む）": "All (including contracted sounds)",
    "選択（文字 → ローマ字）": "Multiple choice (character → romaji)",
    "入力（ローマ字 → 文字）": "Typing (romaji → character)",
    "ミックス": "Mixed",
    "ひらがな": "Hiragana",
    "カタカナ": "Katakana",

    "日本語": "Japanese",
    "復習": "Review",
    "予習": "Preview",
    "単語": "Vocabulary",
    "漢字": "Kanji",
    "会話": "Conversation",
    "読解": "Reading",
    "作文": "Writing",
    "数学": "Math",
    "英語": "English",
    "理科": "Science",
    "国語": "Language arts",
    "歴史": "History",
    "地理": "Geography",
    "体育": "PE",
    "音楽": "Music",
    "美術": "Art",
    "情報": "IT",
    "リスニング": "Listening",

    # settings coverage line
    "対応範囲：ひらがな・カタカナ・漢字基礎 / greetings / numbers /  Lessons 1–12 / 実践会話":
        "Coverage: Hiragana / Katakana / basic Kanji / Greetings / Numbers / "
        "Lessons 1–12 / Real-life conversation",

    # practice session messages
    "この文字は？": "What is this character?",
    "ひらがな / カタカナで入力（ローマ字）": "Type the hiragana / katakana (romaji shown)",
    "見事！ N5 レベルに近づいています。": "Excellent! You're getting close to N5.",
    "良い結果です。間違えた問題を復習しましょう。": "Good result. Review the questions you missed.",
    "繰り返しが上達のコツ。もう一度挑戦しましょう。": "Repetition is the key. Try again!",
    "素晴らしい！ 文字がしっかり身についています。": "Wonderful! The characters are sticking.",
    "いい調子です。間違えた文字を復習しましょう。": "Nice work. Review the characters you missed.",
    "もう一度挑戦して、一文字ずつ覚えていきましょう。": "Try again and learn one character at a time.",
    "すべて正解しました！": "All correct!",
    "復習する問題：": "Review these:",
}

# Level titles come from the registry so navigation and breadcrumbs translate.
try:
    from ..data.registry import LEVELS as _LEVELS
    for _level in _LEVELS:
        JA_EN.setdefault(_level.jp, _level.en)
except Exception:  # pragma: no cover - registry always imports, defensive only
    pass


# ------------------------------------------------------- dynamic templates
_PATTERNS: list[tuple[re.Pattern[str], Any]] = [
    (re.compile(r"^(L\d+ · )(.*)$"),
     lambda m: f"{m.group(1)}{tr(m.group(2))}"),
    (re.compile(r"^(.+?)   (.+)$"),
     lambda m: f"{m.group(1)}   {tr(m.group(2))}"),
    (re.compile(r"^今日の目標 (\d+)%$"), lambda m: f"Daily goal {m.group(1)}%"),
    (re.compile(r"^🔥 (\d+) 日$"), lambda m: f"🔥 {m.group(1)} days"),
    (re.compile(r"^(\d+) 日$"), lambda m: f"{m.group(1)} days"),
    (re.compile(r"^(\d+) 件$"), lambda m: f"{m.group(1)} reviews"),
    (re.compile(r"^累計レビュー：(\d+) 件 · 正答：(\d+) 件 · 学習時間：(\d+) 分$"),
     lambda m: f"Total reviews: {m.group(1)} · Correct: {m.group(2)} · Study time: {m.group(3)} min"),
    (re.compile(r"^収録レッスン：(\d+)$"), lambda m: f"Lessons included: {m.group(1)}"),
    (re.compile(r"^収録語彙：(\d+) 語$"), lambda m: f"Vocabulary: {m.group(1)} words"),
    (re.compile(r"^文法ポイント：(\d+)$"), lambda m: f"Grammar points: {m.group(1)}"),
    (re.compile(r"^実用例・表現：(\d+)$"), lambda m: f"Phrases & expressions: {m.group(1)}"),
    (re.compile(r"^(.*?) · 完了$"), lambda m: f"{m.group(1)} · Done"),
    (re.compile(r"^いまここ · (.*)$"), lambda m: f"You are here · {m.group(1)}"),
    (re.compile(r"^(.*?) · いつでも挑戦できます$"), lambda m: f"{m.group(1)} · Practice anytime"),
    (re.compile(r"^(\d+) 枚のカードを復習しました。\n正答率 (\d+)% · 次回の復習日は自動で設定されます。$"),
     lambda m: (f"Reviewed {m.group(1)} cards.\n"
                f"Accuracy {m.group(2)}% · next review dates are scheduled automatically.")),
    (re.compile(r"^語彙 (\d+)$"), lambda m: f"Vocabulary {m.group(1)}"),
    (re.compile(r"^文法 (\d+)$"), lambda m: f"Grammar {m.group(1)}"),
    (re.compile(r"^表現 (\d+)$"), lambda m: f"Expressions {m.group(1)}"),
    (re.compile(r"^正解 (\d+)$"), lambda m: f"Correct {m.group(1)}"),
    (re.compile(r"^問題 (\d+) / (\d+)$"), lambda m: f"Question {m.group(1)} / {m.group(2)}"),
    (re.compile(r"^✓  正解！  (.+)$"), lambda m: f"✓  Correct!  {m.group(1)}"),
    (re.compile(r"^✕  もう一度。  (.+)$"), lambda m: f"✕  Try again.  {m.group(1)}"),
    (re.compile(r"^✕  正解は「(.+)」\n(.+)$"),
     lambda m: f"✕  Correct answer: 「{m.group(1)}」\n{m.group(2)}"),
    (re.compile(r"^(\d+) / (\d+) 正解\n(.+)$"),
     lambda m: f"{m.group(1)} / {m.group(2)} correct\n{m.group(3)}"),
    (re.compile(r"^(\d+) 表現 · (\d+) コツ$"),
     lambda m: f"{m.group(1)} phrases · {m.group(2)} tips"),
    (re.compile(r"^文化ノート (\d+)$"), lambda m: f"Culture note {m.group(1)}"),
    (re.compile(r"^コツ (\d+)$"), lambda m: f"Tip {m.group(1)}"),
    (re.compile(r"^おじぎ (\d+)$"), lambda m: f"Bowing {m.group(1)}"),
]


def tr(text: str | None) -> str:
    """Translate a single UI string into the active language."""
    if not text or _lang == "ja":
        return text or ""
    value = str(text)
    if value in JA_EN:
        return JA_EN[value]
    for pattern, repl in _PATTERNS:
        match = pattern.fullmatch(value)
        if match:
            return repl(match)
    return value


# --------------------------------------------------------- widget traversal
def _sync(target: Any, getter, setter, prop: str) -> None:
    """Translate a property while remembering its source and last output.

    If a page refresh replaces the text with fresh Japanese, ``cur != last``
    detects it and re-translates the new value.  Switching back to Japanese
    simply returns the remembered source.
    """
    try:
        cur = getter()
    except Exception:
        return
    if not isinstance(cur, str) or not cur:
        return
    src = target.property(prop)
    last = target.property(prop + "_last")
    if src is None or (last is not None and cur != last):
        src = cur
        target.setProperty(prop, src)
    out = tr(src)
    try:
        setter(out)
    except Exception:
        return
    target.setProperty(prop + "_last", out)


def _translate_text_widget(widget: Any) -> None:
    if hasattr(widget, "text") and hasattr(widget, "setText"):
        # Line edits hold user input — translate the placeholder instead.
        if not hasattr(widget, "placeholderText"):
            _sync(widget, widget.text, widget.setText, "_i18n_text")
    if hasattr(widget, "toolTip") and hasattr(widget, "setToolTip"):
        _sync(widget, widget.toolTip, widget.setToolTip, "_i18n_tip")
    if hasattr(widget, "placeholderText") and hasattr(widget, "setPlaceholderText"):
        _sync(widget, widget.placeholderText, widget.setPlaceholderText, "_i18n_ph")
    if hasattr(widget, "count") and hasattr(widget, "itemText") and hasattr(widget, "setItemText"):
        for index in range(widget.count()):
            _sync(widget,
                  lambda i=index: widget.itemText(i),
                  lambda value, i=index: widget.setItemText(i, value),
                  f"_i18n_item_{index}")
    if hasattr(widget, "tabText") and hasattr(widget, "setTabText") and hasattr(widget, "count"):
        for index in range(widget.count()):
            _sync(widget,
                  lambda i=index: widget.tabText(i),
                  lambda value, i=index: widget.setTabText(i, value),
                  f"_i18n_tab_{index}")


def apply_language(window: Any) -> None:
    """Apply the active language across the whole window tree."""
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import QMenu, QStatusBar, QWidget

    # Window title
    title_src = window.property("_i18n_win_title")
    if title_src is None:
        title_src = window.windowTitle()
        window.setProperty("_i18n_win_title", title_src)
    window.setWindowTitle(tr(title_src))

    # Status bar
    for status in window.findChildren(QStatusBar):
        _sync(status, status.currentMessage, status.showMessage, "_i18n_status")

    # Menu bar actions and their submenus
    menubar = window.menuBar()
    menus = list(menubar.findChildren(QMenu))
    for menu in menus:
        if menu.objectName() == "languageMenu":
            continue
        _sync(menu, menu.title, menu.setTitle, "_i18n_menu_title")
        for action in menu.actions():
            _translate_action(action)
    for action in menubar.actions():
        _translate_action(action)

    # All widgets (labels, buttons, combos, deck, pages, ...)
    for widget in window.findChildren(QWidget):
        if isinstance(widget, (QMenu,)):
            continue
        _translate_text_widget(widget)

    # Language action always shows the *target* language.
    for action in window.findChildren(QAction):
        if action.objectName() == "languageAction":
            action.setText(LANG_LABELS.get(_lang, LANG_LABELS["ja"]))


def _translate_action(action: Any) -> None:
    if action.objectName() == "languageAction":
        return
    _sync(action, action.text, action.setText, "_i18n_action_text")
    _sync(action, action.toolTip, action.setToolTip, "_i18n_action_tip")
    menu = action.menu()
    if menu is not None:
        _sync(menu, menu.title, menu.setTitle, "_i18n_menu_title")
        for child in menu.actions():
            _translate_action(child)
