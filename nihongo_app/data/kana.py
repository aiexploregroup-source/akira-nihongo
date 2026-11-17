"""Hiragana & Katakana tables, diacritics, contracted sounds, extended katakana."""
from __future__ import annotations

from ..core.models import KanaEntry

# rows: (row_name, [(char, romaji), ...])
HIRA_ROWS: list[tuple[str, list[tuple[str, str]]]] = [
    ("あ行", [("あ", "a"), ("い", "i"), ("う", "u"), ("え", "e"), ("お", "o")]),
    ("か行", [("か", "ka"), ("き", "ki"), ("く", "ku"), ("け", "ke"), ("こ", "ko")]),
    ("さ行", [("さ", "sa"), ("し", "shi"), ("す", "su"), ("せ", "se"), ("そ", "so")]),
    ("た行", [("た", "ta"), ("ち", "chi"), ("つ", "tsu"), ("て", "te"), ("と", "to")]),
    ("な行", [("な", "na"), ("に", "ni"), ("ぬ", "nu"), ("ね", "ne"), ("の", "no")]),
    ("は行", [("は", "ha"), ("ひ", "hi"), ("ふ", "fu"), ("へ", "he"), ("ほ", "ho")]),
    ("ま行", [("ま", "ma"), ("み", "mi"), ("む", "mu"), ("め", "me"), ("も", "mo")]),
    ("や行", [("や", "ya"), ("ゆ", "yu"), ("よ", "yo")]),
    ("ら行", [("ら", "ra"), ("り", "ri"), ("る", "ru"), ("れ", "re"), ("ろ", "ro")]),
    ("わ行", [("わ", "wa"), ("を", "wo"), ("ん", "n")]),
]

KATA_ROWS: list[tuple[str, list[tuple[str, str]]]] = [
    ("ア行", [("ア", "a"), ("イ", "i"), ("ウ", "u"), ("エ", "e"), ("オ", "o")]),
    ("カ行", [("カ", "ka"), ("キ", "ki"), ("ク", "ku"), ("ケ", "ke"), ("コ", "ko")]),
    ("サ行", [("サ", "sa"), ("シ", "shi"), ("ス", "su"), ("セ", "se"), ("ソ", "so")]),
    ("タ行", [("タ", "ta"), ("チ", "chi"), ("ツ", "tsu"), ("テ", "te"), ("ト", "to")]),
    ("ナ行", [("ナ", "na"), ("ニ", "ni"), ("ヌ", "nu"), ("ネ", "ne"), ("ノ", "no")]),
    ("ハ行", [("ハ", "ha"), ("ヒ", "hi"), ("フ", "fu"), ("ヘ", "he"), ("ホ", "ho")]),
    ("マ行", [("マ", "ma"), ("ミ", "mi"), ("ム", "mu"), ("メ", "me"), ("モ", "mo")]),
    ("ヤ行", [("ヤ", "ya"), ("ユ", "yu"), ("ヨ", "yo")]),
    ("ラ行", [("ラ", "ra"), ("リ", "ri"), ("ル", "ru"), ("レ", "re"), ("ロ", "ro")]),
    ("ワ行", [("ワ", "wa"), ("ヲ", "wo"), ("ン", "n")]),
]

VOICED_HIRA: list[tuple[str, list[tuple[str, str]]]] = [
    ("が行 (dakuten)", [("が", "ga"), ("ぎ", "gi"), ("ぐ", "gu"), ("げ", "ge"), ("ご", "go")]),
    ("ざ行 (dakuten)", [("ざ", "za"), ("じ", "ji"), ("ず", "zu"), ("ぜ", "ze"), ("ぞ", "zo")]),
    ("だ行 (dakuten)", [("だ", "da"), ("ぢ", "ji"), ("づ", "zu"), ("で", "de"), ("ど", "do")]),
    ("ば行 (dakuten)", [("ば", "ba"), ("び", "bi"), ("ぶ", "bu"), ("べ", "be"), ("ぼ", "bo")]),
    ("ぱ行 (handakuten)", [("ぱ", "pa"), ("ぴ", "pi"), ("ぷ", "pu"), ("ぺ", "pe"), ("ぽ", "po")]),
]

VOICED_KATA: list[tuple[str, list[tuple[str, str]]]] = [
    ("ガ行 (dakuten)", [("ガ", "ga"), ("ギ", "gi"), ("グ", "gu"), ("ゲ", "ge"), ("ゴ", "go")]),
    ("ザ行 (dakuten)", [("ザ", "za"), ("ジ", "ji"), ("ズ", "zu"), ("ゼ", "ze"), ("ゾ", "zo")]),
    ("ダ行 (dakuten)", [("ダ", "da"), ("ヂ", "ji"), ("ヅ", "zu"), ("デ", "de"), ("ド", "do")]),
    ("バ行 (dakuten)", [("バ", "ba"), ("ビ", "bi"), ("ブ", "bu"), ("ベ", "be"), ("ボ", "bo")]),
    ("パ行 (handakuten)", [("パ", "pa"), ("ピ", "pi"), ("プ", "pu"), ("ペ", "pe"), ("ポ", "po")]),
]

CONTRACTED_HIRA: list[tuple[str, list[tuple[str, str]]]] = [
    ("きゃ行", [("きゃ", "kya"), ("きゅ", "kyu"), ("きょ", "kyo")]),
    ("しゃ行", [("しゃ", "sha"), ("しゅ", "shu"), ("しょ", "sho")]),
    ("ちゃ行", [("ちゃ", "cha"), ("ちゅ", "chu"), ("ちょ", "cho")]),
    ("にゃ行", [("にゃ", "nya"), ("にゅ", "nyu"), ("にょ", "nyo")]),
    ("ひゃ行", [("ひゃ", "hya"), ("ひゅ", "hyu"), ("ひょ", "hyo")]),
    ("みゃ行", [("みゃ", "mya"), ("みゅ", "myu"), ("みょ", "myo")]),
    ("りゃ行", [("りゃ", "rya"), ("りゅ", "ryu"), ("りょ", "ryo")]),
    ("ぎゃ行", [("ぎゃ", "gya"), ("ぎゅ", "gyu"), ("ぎょ", "gyo")]),
    ("じゃ行", [("じゃ", "ja"), ("じゅ", "ju"), ("じょ", "jo")]),
    ("びゃ行", [("びゃ", "bya"), ("びゅ", "byu"), ("びょ", "byo")]),
    ("ぴゃ行", [("ぴゃ", "pya"), ("ぴゅ", "pyu"), ("ぴょ", "pyo")]),
]

CONTRACTED_KATA: list[tuple[str, list[tuple[str, str]]]] = [
    ("キャ行", [("キャ", "kya"), ("キュ", "kyu"), ("キョ", "kyo")]),
    ("シャ行", [("シャ", "sha"), ("シュ", "shu"), ("ショ", "sho")]),
    ("チャ行", [("チャ", "cha"), ("チュ", "chu"), ("チョ", "cho")]),
    ("ニャ行", [("ニャ", "nya"), ("ニュ", "nyu"), ("ニョ", "nyo")]),
    ("ヒャ行", [("ヒャ", "hya"), ("ヒュ", "hyu"), ("ヒョ", "hyo")]),
    ("ミャ行", [("ミャ", "mya"), ("ミュ", "myu"), ("ミョ", "myo")]),
    ("リャ行", [("リャ", "rya"), ("リュ", "ryu"), ("リョ", "ryo")]),
    ("ギャ行", [("ギャ", "gya"), ("ギュ", "gyu"), ("ギョ", "gyo")]),
    ("ジャ行", [("ジャ", "ja"), ("ジュ", "ju"), ("ジョ", "jo")]),
    ("ビャ行", [("ビャ", "bya"), ("ビュ", "byu"), ("ビョ", "byo")]),
    ("ピャ行", [("ピャ", "pya"), ("ピュ", "pyu"), ("ピョ", "pyo")]),
]

EXTENDED_KATA: list[tuple[str, list[tuple[str, str]]]] = [
    ("外来音", [
        ("ファ", "fa"), ("フィ", "fi"), ("フェ", "fe"), ("フォ", "fo"),
        ("ヴァ", "va"), ("ヴィ", "vi"), ("ヴ", "vu"), ("ヴェ", "ve"), ("ヴォ", "vo"),
        ("ティ", "ti"), ("ディ", "di"), ("トゥ", "tu"), ("ドゥ", "du"),
        ("チェ", "che"), ("ジェ", "je"), ("シェ", "she"), ("ウィ", "wi"), ("ウェ", "we"),
    ]),
]

SPECIAL: list[tuple[str, list[tuple[str, str]]]] = [
    ("特殊", [
        ("っ", "small tsu (double consonant / pause)"),
        ("ゃ", "small ya"), ("ゅ", "small yu"), ("ょ", "small yo"),
        ("ー", "long vowel mark"),
    ]),
]


def _entries(rows: list[tuple[str, list[tuple[str, str]]]], script: str, kind: str) -> list[KanaEntry]:
    out: list[KanaEntry] = []
    for group, items in rows:
        for char, romaji in items:
            out.append(KanaEntry(char, romaji, group, script, kind))
    return out


HIRAGANA: list[KanaEntry] = (
    _entries(HIRA_ROWS, "hiragana", "basic")
    + _entries(VOICED_HIRA, "hiragana", "voiced")
    + _entries(CONTRACTED_HIRA, "hiragana", "contracted")
    + _entries(SPECIAL, "hiragana", "special")
)

KATAKANA: list[KanaEntry] = (
    _entries(KATA_ROWS, "katakana", "basic")
    + _entries(VOICED_KATA, "katakana", "voiced")
    + _entries(CONTRACTED_KATA, "katakana", "contracted")
    + _entries(EXTENDED_KATA, "katakana", "extended")
    + _entries(SPECIAL, "katakana", "special")
)

ALL_KANA: list[KanaEntry] = HIRAGANA + KATAKANA

KANA_BY_CHAR: dict[str, KanaEntry] = {k.char: k for k in ALL_KANA}

WRITING_SYSTEM: list[tuple[str, str, str]] = [
    ("ひらがな · Hiragana", "46 basic syllables",
     "Used for native Japanese words, particles, and verb/adjective endings. e.g. あ、い、う、え、お"),
    ("カタカナ · Katakana", "46 basic syllables",
     "Used for foreign loanwords, onomatopoeia and names. e.g. ア、イ、ウ、エ、オ"),
    ("漢字 · Kanji", "Chinese characters",
     "Characters representing meaning and sound. Used for nouns and verb/adjective stems."),
    ("濁点 · Dakuten ( ゛)", "Voicing mark",
     "Changes unvoiced to voiced: k→g, s→z, t→d, h→b. e.g. か→が, は→ば"),
    ("半濁点 · Handakuten ( ゜)", "Semi-voicing mark",
     "Changes h→p. e.g. は→ぱ, ふ→ぷ"),
    ("拗音 · Contracted sounds", "Small ゃ ゅ ょ",
     "Combine with i-vowel kana: きゃ kya, しゅ shu, ちょ cho"),
    ("促音 · Double consonants", "Small っ",
     "Indicates a pause/gemination before a consonant. e.g. きって kitte"),
    ("長音 · Long vowels", "Vowel held twice as long",
     "おばさん (aunt) vs おばあさん (grandmother)"),
    ("高低アクセント · Pitch accent", "High / low syllables",
     "Japanese uses pitch accent; patterns vary by region."),
]
