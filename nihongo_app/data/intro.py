"""Introduction content: greetings, numbers, basic culture notes."""
from __future__ import annotations

from ..core.models import Phrase

GREETINGS: list[Phrase] = [
    Phrase("おはよう。", "Ohayoo.", "Good morning. (Casual)", "Greetings"),
    Phrase("おはようございます。", "Ohayoo gozaimasu.", "Good morning. (Polite)", "Greetings"),
    Phrase("こんにちは。", "Konnichiwa.", "Good afternoon. / Hello.", "Greetings"),
    Phrase("こんばんは。", "Konbanwa.", "Good evening.", "Greetings"),
    Phrase("さようなら。", "Sayoonara.", "Good-bye. (Formal / long term)", "Greetings"),
    Phrase("おやすみ(なさい)。", "Oyasumi (nasai).", "Good night.", "Greetings"),
    Phrase("ありがとう。", "Arigatoo.", "Thank you. (Casual)", "Greetings"),
    Phrase("ありがとうございます。", "Arigatoo gozaimasu.", "Thank you. (Polite)", "Greetings"),
    Phrase("すみません。", "Sumimasen.", "Excuse me. / I'm sorry. / Thank you.", "Greetings"),
    Phrase("いいえ。", "Iie.", "No. / Not at all.", "Greetings"),
    Phrase("いってきます。", "Itte kimasu.", "I'll go and come back. (Leaving home)", "Greetings"),
    Phrase("いってらっしゃい。", "Itterasshai.", "Please go and come back. (Response)", "Greetings"),
    Phrase("ただいま。", "Tadaima.", "I'm home.", "Greetings"),
    Phrase("おかえり(なさい)。", "Okaeri (nasai).", "Welcome home.", "Greetings"),
    Phrase("いただきます。", "Itadakimasu.", "Thank you for the meal. (Before eating)", "Greetings"),
    Phrase("ごちそうさま(でした)。", "Gochisoosama (deshita).", "Thank you for the meal. (After eating)", "Greetings"),
    Phrase("はじめまして。", "Hajimemashite.", "How do you do? (First meeting)", "Greetings"),
    Phrase("～です。", "...desu.", "I am ...", "Greetings"),
    Phrase("よろしくおねがいします。", "Yoroshiku onegai shimasu.",
           "Nice to meet you. / Please treat me well.", "Greetings"),
]

BOWING_NOTES: list[str] = [
    "Bowing is used for greetings, respect, gratitude, and apologies.",
    "Depth and length of the bow indicate formality: a small nod for casual, a deeper longer bow for respect or apology.",
    "Handshaking is becoming common in business situations with foreigners.",
    "Meeshi (名刺) — business cards are exchanged with a small bow, presented with both hands.",
]

NUMBERS: list[tuple[str, str, str]] = [
    ("0", "ゼロ / れい", "zero / rei"),
    ("1", "いち", "ichi"),
    ("2", "に", "ni"),
    ("3", "さん", "san"),
    ("4", "よん / し", "yon / shi"),
    ("5", "ご", "go"),
    ("6", "ろく", "roku"),
    ("7", "なな / しち", "nana / shichi"),
    ("8", "はち", "hachi"),
    ("9", "きゅう / く", "kyuu / ku"),
    ("10", "じゅう", "juu"),
    ("100", "ひゃく", "hyaku"),
    ("1,000", "せん", "sen"),
    ("10,000", "いちまん", "ichiman"),
]

# Hour / minute readings from Lesson 1 useful expressions.
HOURS: list[tuple[str, str]] = [
    ("1:00", "いちじ"), ("2:00", "にじ"), ("3:00", "さんじ"), ("4:00", "よじ"),
    ("5:00", "ごじ"), ("6:00", "ろくじ"), ("7:00", "しちじ"), ("8:00", "はちじ"),
    ("9:00", "くじ"), ("10:00", "じゅうじ"), ("11:00", "じゅういちじ"), ("12:00", "じゅうにじ"),
]

MINUTES: list[tuple[str, str]] = [
    ("1 min", "いっぷん"), ("2 min", "にふん"), ("3 min", "さんぷん"), ("4 min", "よんぷん"),
    ("5 min", "ごふん"), ("6 min", "ろっぷん"), ("7 min", "ななふん"), ("8 min", "はっぷん"),
    ("9 min", "きゅうふん"), ("10 min", "じゅっぷん"), ("11 min", "じゅういっぷん"),
    ("12 min", "じゅうにふん"), ("13 min", "じゅうさんぷん"), ("14 min", "じゅうよんぷん"),
    ("15 min", "じゅうごふん"), ("16 min", "じゅうろっぷん"), ("17 min", "じゅうななふん"),
    ("18 min", "じゅうはっぷん"), ("19 min", "じゅうきゅうふん"), ("20 min", "にじゅっぷん"),
    ("30 min", "さんじゅっぷん"),
]

DAYS_OF_WEEK: list[tuple[str, str, str]] = [
    ("日曜日", "にちようび", "nichiyoobi", "Sunday"),
    ("月曜日", "げつようび", "getsuyoobi", "Monday"),
    ("火曜日", "かようび", "kayoobi", "Tuesday"),
    ("水曜日", "すいようび", "suiyoobi", "Wednesday"),
    ("木曜日", "もくようび", "mokuyoobi", "Thursday"),
    ("金曜日", "きんようび", "kinyoobi", "Friday"),
    ("土曜日", "どようび", "doyoobi", "Saturday"),
]

MONTHS: list[tuple[str, str, str]] = [
    ("一月", "いちがつ", "ichigatsu", "January"), ("二月", "にがつ", "nigatsu", "February"),
    ("三月", "さんがつ", "sangatsu", "March"), ("四月", "しがつ", "shigatsu", "April"),
    ("五月", "ごがつ", "gogatsu", "May"), ("六月", "ろくがつ", "rokugatsu", "June"),
    ("七月", "しちがつ", "shichigatsu", "July"), ("八月", "はちがつ", "hachigatsu", "August"),
    ("九月", "くがつ", "kugatsu", "September"), ("十月", "じゅうがつ", "juugatsu", "October"),
    ("十一月", "じゅういちがつ", "juuichigatsu", "November"),
    ("十二月", "じゅうにがつ", "juunigatsu", "December"),
]

DAYS_OF_MONTH: list[tuple[str, str]] = [
    ("1日", "ついたち"), ("2日", "ふつか"), ("3日", "みっか"), ("4日", "よっか"),
    ("5日", "いつか"), ("6日", "むいか"), ("7日", "なのか"), ("8日", "ようか"),
    ("9日", "ここのか"), ("10日", "とおか"), ("11日", "じゅういちにち"),
    ("12日", "じゅうににち"), ("13日", "じゅうさんにち"), ("14日", "じゅうよっか"),
    ("15日", "じゅうごにち"), ("16日", "じゅうろくにち"), ("17日", "じゅうななにち"),
    ("18日", "じゅうはちにち"), ("19日", "じゅうきゅうにち"), ("20日", "はつか"),
    ("21日", "にじゅういちにち"), ("22日", "にじゅうににち"), ("23日", "にじゅうさんにち"),
    ("24日", "にじゅうよっか"), ("25日", "にじゅうごにち"), ("26日", "にじゅうろくにち"),
    ("27日", "にじゅうななにち"), ("28日", "にじゅうはちにち"),
    ("29日", "にじゅうきゅうにち"), ("30日", "さんじゅうにち"), ("31日", "さんじゅういちにち"),
]

RELATIVE_TIME: list[tuple[str, str, str]] = [
    ("おととい", "ototoi", "day before yesterday"),
    ("きのう", "kinoo", "yesterday"),
    ("きょう", "kyoo", "today"),
    ("あした", "ashita", "tomorrow"),
    ("あさって", "asatte", "day after tomorrow"),
    ("せんしゅう", "senshuu", "last week"),
    ("こんしゅう", "konshuu", "this week"),
    ("らいしゅう", "raishuu", "next week"),
    ("せんげつ", "sengetsu", "last month"),
    ("こんげつ", "kongetsu", "this month"),
    ("らいげつ", "raigetsu", "next month"),
    ("きょねん", "kyonen", "last year"),
    ("ことし", "kotoshi", "this year"),
    ("らいねん", "rainen", "next year"),
]
