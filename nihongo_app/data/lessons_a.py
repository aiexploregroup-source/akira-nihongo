"""Genki I (3rd Edition) — Lessons 1 to 6."""
from __future__ import annotations

from ..core.models import GrammarPoint, Lesson, Phrase, VocabItem


def v(lesson: int, category: str, rows: list[tuple[str, str, str]]) -> list[VocabItem]:
    return [VocabItem(jp, romaji, meaning, category, lesson) for jp, romaji, meaning in rows]


def g(lesson: int, title: str, explanation: str,
      examples: list[tuple[str, str]]) -> GrammarPoint:
    return GrammarPoint(title, explanation, tuple(examples), lesson)


def p(group: str, rows: list[tuple[str, str, str]]) -> list[Phrase]:
    return [Phrase(jp, romaji, meaning, group) for jp, romaji, meaning in rows]


LESSON_1 = Lesson(
    number=1,
    title_jp="あたらしいともだち",
    title_en="New Friends",
    vocab=(
        v(1, "School", [
            ("だいがく", "daigaku", "college; university"),
            ("こうこう", "kookoo", "high school"),
            ("がくせい", "gakusee", "student"),
            ("だいがくせい", "daigakusee", "college student"),
            ("りゅうがくせい", "ryuugakusee", "international student"),
            ("せんせい", "sensee", "teacher; professor"),
            ("～ねんせい", "...nensee", "... year student"),
            ("せんこう", "senkoo", "major"),
        ])
        + v(1, "Person", [
            ("わたし", "watashi", "I"),
            ("ともだち", "tomodachi", "friend"),
            ("～さん", "...san", "Mr./Ms... (honorific)"),
            ("～じん", "...jin", "... people"),
            ("にほんじん", "nihonjin", "Japanese people"),
        ])
        + v(1, "Time", [
            ("いま", "ima", "now"),
            ("ごぜん", "gozen", "A.M."),
            ("ごご", "gogo", "P.M."),
            ("～じ", "...ji", "o'clock"),
            ("いちじ", "ichiji", "one o'clock"),
            ("はん", "han", "half"),
            ("にじはん", "niji han", "half past two"),
        ])
        + v(1, "Others", [
            ("にほん", "Nihon", "Japan"),
            ("アメリカ", "Amerika", "U.S.A."),
            ("～ご", "...go", "... language"),
            ("にほんご", "nihongo", "Japanese language"),
            ("～さい", "...sai", "... years old"),
            ("でんわ", "denwa", "telephone"),
            ("～ばん", "...ban", "number..."),
            ("ばんごう", "bangoo", "number"),
            ("なまえ", "namae", "name"),
            ("なん / なに", "nan / nani", "what"),
        ])
        + v(1, "Expressions", [
            ("あのう", "anoo", "um..."),
            ("はい", "hai", "yes"),
            ("そうです", "soo desu", "That's right."),
            ("そうですか", "soo desu ka", "I see.; Is that so?"),
        ])
    ),
    grammar=[
        g(1, "1. XはYです", '"X is Y." は (wa) is the topic marker, pronounced "wa".',
          [("わたしは がくせいです。", "I am a student.")]),
        g(1, "2. Question Sentences", "Add か at the end of a statement to make a question.",
          [("りゅうがくせいですか。", "Are you an international student?")]),
        g(1, "3. Noun1のNoun2", "の connects two nouns. Noun1 modifies Noun2.",
          [("にほんごの がくせい", "a student of Japanese")]),
        g(1, "4. ～さん", "Honorific suffix added to names. Never used for oneself.",
          [("たけしさん", "Mr. Takeshi")]),
        g(1, "5. ～じん", "Suffix for nationality.",
          [("アメリカじん", "American person")]),
        g(1, "6. ～さい", "Counter for age.",
          [("じゅうきゅうさい", "19 years old")]),
        g(1, "7. ～ね / ～よ", "ね = seeking agreement (\"right?\"). よ = giving new information (\"I tell you\").",
          [("そうですね。", "That's right, isn't it?"), ("おいしいですよ。", "It's delicious, I tell you.")]),
    ],
    culture=[
        "Family name comes first, then given name.",
        "Often only the family name is used when introducing oneself.",
        "Common family names: 佐藤 (Satoo), 鈴木 (Suzuki), 高橋 (Takahashi), 田中 (Tanaka), 伊藤 (Itoo).",
        "Common given names: ゆうと (Yuuto), かいた (Kaito), そうた (Soota), はるき (Haruki), "
        "だいすけ (Daisuke), さくら (Sakura), ゆい (Yui), あおい (Aoi), りん (Rin), かな (Kana).",
    ],
    useful=p("Time (じかん)", [
        ("いちじ", "ichiji", "1:00"), ("にじ", "niji", "2:00"), ("さんじ", "sanji", "3:00"),
        ("よじ", "yoji", "4:00"), ("ごじ", "goji", "5:00"), ("ろくじ", "rokuji", "6:00"),
        ("しちじ", "shichiji", "7:00"), ("はちじ", "hachiji", "8:00"),
        ("くじ", "kuji", "9:00"), ("じゅうじ", "juuji", "10:00"),
        ("じゅういちじ", "juuichiji", "11:00"), ("じゅうにじ", "juuniji", "12:00"),
        ("いっぷん", "ippun", "1 minute"), ("にふん", "nifun", "2 minutes"),
        ("さんぷん", "sanpun", "3 minutes"), ("よんぷん", "yonpun", "4 minutes"),
        ("ごふん", "gofun", "5 minutes"), ("ろっぷん", "roppun", "6 minutes"),
        ("ななふん", "nanafun", "7 minutes"), ("はっぷん", "happun", "8 minutes"),
        ("きゅうふん", "kyuufun", "9 minutes"), ("じゅっぷん", "juppun", "10 minutes"),
        ("じゅういっぷん", "juuippun", "11 minutes"), ("じゅうにふん", "juunifun", "12 minutes"),
        ("じゅうさんぷん", "juusanpun", "13 minutes"), ("じゅうよんぷん", "juuyonpun", "14 minutes"),
        ("じゅうごふん", "juugofun", "15 minutes"), ("じゅうろっぷん", "juuroppun", "16 minutes"),
        ("じゅうななふん", "juunanafun", "17 minutes"), ("じゅうはっぷん", "juuhappun", "18 minutes"),
        ("じゅうきゅうふん", "juukyuufun", "19 minutes"), ("にじゅっぷん", "nijuppun", "20 minutes"),
        ("さんじゅっぷん", "sanjuuppun", "30 minutes"),
        ("はん", "han", "half past"), ("ごぜん", "gozen", "A.M."), ("ごご", "gogo", "P.M."),
    ]),
)

LESSON_2 = Lesson(
    number=2,
    title_jp="かいもの",
    title_en="Shopping",
    vocab=(
        v(2, "Words That Point", [
            ("これ", "kore", "this one"), ("それ", "sore", "that one"),
            ("あれ", "are", "that one (over there)"), ("どれ", "dore", "which one"),
            ("この", "kono", "this..."), ("その", "sono", "that..."),
            ("あの", "ano", "that... (over there)"), ("どの", "dono", "which..."),
            ("ここ", "koko", "here"), ("そこ", "soko", "there"),
            ("あそこ", "asoko", "over there"), ("どこ", "doko", "where"),
            ("だれ", "dare", "who"),
        ])
        + v(2, "Food", [
            ("おいしい", "oishii", "delicious"), ("さかな", "sakana", "fish"),
            ("とんかつ", "tonkatsu", "pork cutlet"), ("にく", "niku", "meat"),
            ("メニュー", "menyuu", "menu"), ("やさい", "yasai", "vegetable"),
        ])
        + v(2, "Things", [
            ("かさ", "kasa", "umbrella"), ("かばん", "kaban", "bag"),
            ("くつ", "kutsu", "shoes"), ("さいふ", "saifu", "wallet"),
            ("ジーンズ", "jiinzu", "jeans"), ("じてんしゃ", "jitensha", "bicycle"),
            ("しんぶん", "shinbun", "newspaper"), ("スマホ", "sumaho", "smartphone"),
            ("Tシャツ", "tiishatsu", "T-shirt"), ("とけい", "tokee", "watch; clock"),
            ("ノート", "nooto", "notebook"), ("ペン", "pen", "pen"),
            ("ぼうし", "booshi", "hat; cap"),
        ])
        + v(2, "Expressions", [
            ("いらっしゃいませ", "irasshaimase", "Welcome. (store greeting)"),
            ("どうぞ", "doozo", "Please. / Here you are."),
            ("どうも", "doomo", "Thanks."),
            ("じゃあ", "jaa", "then; well then"),
            ("おねがいします", "onegaishimasu", "Please. (making a request)"),
            ("～をください", "...o kudasai", "Please give me..."),
            ("～をどうぞ", "...o doozo", "Here is..."),
            ("いくら", "ikura", "how much"),
            ("～えん", "...en", "... yen"),
        ])
    ),
    grammar=[
        g(2, "1. これ/それ/あれ/どれ", "Stand-alone pronouns for things. これ (near speaker), それ (near listener), あれ (far from both), どれ (question).",
          [("これは いくらですか。", "How much is this?")]),
        g(2, "2. この/その/あの/どの + Noun", "Demonstrative adjectives. Must be followed by a noun.",
          [("このほんは いくらですか。", "How much is this book?")]),
        g(2, "3. ここ/そこ/あそこ/どこ", "Pronouns for places.",
          [("トイレは どこですか。", "Where is the restroom?")]),
        g(2, "4. だれの Noun", '"Whose Noun".',
          [("これは だれの かばんですか。", "Whose bag is this?")]),
        g(2, "5. Nounも", '"Noun also/too". Replaces は or が.',
          [("たけしさんは にほんじんです。ゆいさんも にほんじんです。",
            "Takeshi is Japanese. Yui is Japanese, too.")]),
        g(2, "6. Nounじゃないです", "Negative of \"X is Y\". じゃないです is colloquial; じゃありません is more formal.",
          [("にほんじんじゃないです。", "I am not Japanese.")]),
        g(2, "7. ～ね / ～よ", "ね = seeking confirmation. よ = asserting.",
          [("これは にくじゃないですね。", "This isn't meat, is it?"),
           ("とんかつは さかなじゃないですよ。", "Tonkatsu is not fish, I tell you.")]),
    ],
    culture=[
        "Currency is the yen (円, en).",
        "Bills: 10,000 yen (Fukuzawa Yukichi), 5,000 yen (Higuchi Ichiyoo), 2,000 yen (Shurei Gate), 1,000 yen (Noguchi Hideyo).",
        "Coins: 500 yen, 100 yen, 50 yen, 10 yen, 5 yen, 1 yen.",
    ],
    useful=p("In the Classroom (きょうしつ)", [
        ("こくばん", "kokuban", "blackboard"), ("つくえ", "tsukue", "desk"),
        ("けしゴム", "keshigomu", "eraser"), ("えんぴつ", "enpitsu", "pencil"),
        ("ほん", "hon", "book"), ("じしょ", "jisho", "dictionary"),
        ("でんき", "denki", "light"), ("ドア", "doa", "door"),
        ("まど", "mado", "window"), ("カーテン", "kaaten", "curtain"),
        ("いす", "isu", "chair"),
        ("わかりますか。", "Wakarimasu ka.", "Do you understand?"),
        ("わかります。", "Wakarimasu.", "I understand."),
        ("わかりません。", "Wakarimasen.", "I don't understand."),
        ("ゆっくり いってください。", "Yukkuri itte kudasai.", "Please say it slowly."),
        ("もういちど いってください。", "Moo ichido itte kudasai.", "Please say it again."),
        ("ちょっと まってください。", "Chotto matte kudasai.", "Please wait for a while."),
        ("きいてください。", "Kiite kudasai.", "Please listen. / Please ask."),
        ("10ページを みてください。", "Juu peeji o mite kudasai.", "Please look at page 10."),
    ]),
)

LESSON_3 = Lesson(
    number=3,
    title_jp="デートの約束",
    title_en="Making a Date",
    vocab=(
        v(3, "Entertainment & Sports", [
            ("えいが", "eiga", "movie"), ("おんがく", "ongaku", "music"),
            ("ざっし", "zasshi", "magazine"), ("スポーツ", "supootsu", "sports"),
            ("デート", "deeto", "date"), ("テニス", "tenisu", "tennis"),
            ("テレビ", "terebi", "TV"),
        ])
        + v(3, "Foods & Drinks", [
            ("アイスクリーム", "aisukuriimu", "ice cream"),
            ("ハンバーガー", "hanbaagaa", "hamburger"),
            ("おさけ", "osake", "sake; alcoholic drink"), ("おちゃ", "ocha", "green tea"),
            ("コーヒー", "koohii", "coffee"), ("みず", "mizu", "water"),
            ("あさごはん", "asagohan", "breakfast"), ("ひるごはん", "hirugohan", "lunch"),
            ("ばんごはん", "bangohan", "dinner"),
        ])
        + v(3, "Places", [
            ("いえ", "ie", "home; house"), ("うち", "uchi", "home; house; my place"),
            ("がっこう", "gakkoo", "school"), ("カフェ", "kafe", "cafe"),
        ])
        + v(3, "Time", [
            ("あした", "ashita", "tomorrow"), ("きょう", "kyoo", "today"),
            ("あさ", "asa", "morning"), ("こんばん", "konban", "tonight"),
            ("まいにち", "mainichi", "every day"), ("まいばん", "maiban", "every night"),
            ("しゅうまつ", "shuumatsu", "weekend"), ("どようび", "doyoobi", "Saturday"),
            ("にちようび", "nichiyoobi", "Sunday"), ("いつ", "itsu", "when"),
        ])
        + v(3, "U-verbs", [
            ("いく", "iku", "to go"), ("かえる", "kaeru", "to go back; to return"),
            ("きく", "kiku", "to listen; to hear"), ("のむ", "nomu", "to drink"),
            ("はなす", "hanasu", "to speak; to talk"), ("よむ", "yomu", "to read"),
        ])
        + v(3, "R-verbs", [
            ("おきる", "okiru", "to get up"), ("たべる", "taberu", "to eat"),
            ("ねる", "neru", "to sleep; to go to sleep"),
            ("みる", "miru", "to see; to look at; to watch"),
        ])
        + v(3, "Irregular Verbs", [
            ("くる", "kuru", "to come"), ("する", "suru", "to do"),
            ("べんきょうする", "benkyoosuru", "to study"),
        ])
        + v(3, "Adjectives", [("いい", "ii", "good"), ("はやい", "hayai", "early")])
        + v(3, "Adverbs", [
            ("あまり + negative", "amari", "not much"),
            ("ぜんぜん + negative", "zenzen", "not at all"),
            ("たいてい", "taitei", "usually"), ("ちょっと", "chotto", "a little"),
            ("ときどき", "tokidoki", "sometimes"), ("よく", "yoku", "often; much"),
        ])
        + v(3, "Expressions", [
            ("そうですね", "soo desu ne", "That's right.; Let me see."),
            ("でも", "demo", "but"),
            ("どうですか", "doo desu ka", "How about...?; How is...?"),
            ("ええ", "ee", "yes"),
        ])
    ),
    grammar=[
        g(3, "1. Verb Conjugation", "Ru-verbs: replace る with ます/ません. U-verbs: replace final u with imasu/imasen. Irregular: する→します, くる→きます.",
          [("食べる → 食べます", "eat → eats / will eat"), ("飲む → 飲みます", "drink → drinks / will drink")]),
        g(3, "2. Verb Types & Present Tense", "Present tense expresses habitual action or future action.",
          [("私はよくテレビを見ます。", "I often watch TV."),
           ("明日京都に行きます。", "I will go to Kyoto tomorrow.")]),
        g(3, "3. Particles を / で / に / へ", "を (o): direct object. で (de): location of action. に (ni): destination, time. へ (e): destination.",
          [("日本語を勉強します。", "I study Japanese."),
           ("図書館で勉強します。", "I study at the library.")]),
        g(3, "4. Time References", "Use に with specific times/days. Do not use に with relative time words (today, tomorrow) or regular intervals (every day).",
          [("日曜日に行きます。", "I will go on Sunday."), ("明日来ます。", "I will come tomorrow.")]),
        g(3, "5. ～ませんか", "Invitation: \"Would you like to...?\"",
          [("映画を見ませんか。", "Would you like to see a movie?")]),
        g(3, "6. Frequency Adverbs", "毎日 (every day), よく (often), ときどき (sometimes), あまり (not much), ぜんぜん (not at all).",
          [("私はあまりテレビを見ません。", "I don't watch TV much.")]),
        g(3, "7. Word Order", "Topic – Time – Place – Object – Verb.",
          [("私は今日図書館で日本語を勉強します。", "I study Japanese at the library today.")]),
        g(3, "8. Topic Particle は", "Can present non-subject phrases as topic.",
          [("晩ご飯は？", "How about dinner?")]),
    ],
    culture=[
        "ふすま (fusuma): opaque sliding doors.",
        "障子 (shooji): paper sliding doors.",
        "畳 (tatami): straw mat flooring.",
        "玄関 (genkan): entryway where shoes are removed.",
        "お風呂 (ofuro): bathroom with a deep soaking tub, separate from the toilet. Family members share the same bathwater; wash the body before entering.",
    ],
    useful=p("Days / Weeks / Months / Years (ひ・しゅう・つき・とし)", [
        ("日曜日", "nichiyoobi", "Sunday"), ("月曜日", "getsuyoobi", "Monday"),
        ("火曜日", "kayoobi", "Tuesday"), ("水曜日", "suiyoobi", "Wednesday"),
        ("木曜日", "mokuyoobi", "Thursday"), ("金曜日", "kinyoobi", "Friday"),
        ("土曜日", "doyoobi", "Saturday"),
        ("一月", "ichigatsu", "January"), ("二月", "nigatsu", "February"),
        ("三月", "sangatsu", "March"), ("四月", "shigatsu", "April"),
        ("五月", "gogatsu", "May"), ("六月", "rokugatsu", "June"),
        ("七月", "shichigatsu", "July"), ("八月", "hachigatsu", "August"),
        ("九月", "kugatsu", "September"), ("十月", "juugatsu", "October"),
        ("十一月", "juuichigatsu", "November"), ("十二月", "juunigatsu", "December"),
        ("おととい", "ototoi", "day before yesterday"), ("きのう", "kinoo", "yesterday"),
        ("きょう", "kyoo", "today"), ("あした", "ashita", "tomorrow"),
        ("あさって", "asatte", "day after tomorrow"),
        ("せんしゅう", "senshuu", "last week"), ("こんしゅう", "konshuu", "this week"),
        ("らいしゅう", "raishuu", "next week"), ("せんげつ", "sengetsu", "last month"),
        ("こんげつ", "kongetsu", "this month"), ("らいげつ", "raigetsu", "next month"),
        ("きょねん", "kyonen", "last year"), ("ことし", "kotoshi", "this year"),
        ("らいねん", "rainen", "next year"),
    ]),
)

LESSON_4 = Lesson(
    number=4,
    title_jp="初めてのデート",
    title_en="The First Date",
    vocab=(
        v(4, "Activities", [
            ("ゲーム", "geemu", "game"), ("アルバイト", "arubaito", "part-time job"),
            ("かいもの", "kaimono", "shopping"), ("クラス", "kurasu", "class"),
        ])
        + v(4, "People & Things", [
            ("いぬ", "inu", "dog"), ("ねこ", "neko", "cat"), ("ひと", "hito", "person"),
            ("こども", "kodomo", "child"), ("あなた", "anata", "you"),
            ("いす", "isu", "chair"), ("つくえ", "tsukue", "desk"),
            ("しゃしん", "shashin", "picture; photograph"),
            ("はな", "hana", "flower"), ("レポート", "repooto", "(term) paper"),
            ("ごはん", "gohan", "rice; meal"), ("パン", "pan", "bread"),
        ])
        + v(4, "Places", [
            ("おてら", "otera", "temple"), ("こうえん", "kooen", "park"),
            ("スーパー", "suupaa", "supermarket"), ("バスてい", "basutei", "bus stop"),
            ("びょういん", "byooin", "hospital"), ("ホテル", "hoteru", "hotel"),
            ("ほんや", "hon'ya", "bookstore"), ("まち", "machi", "town; city"),
            ("レストラン", "resutoran", "restaurant"),
        ])
        + v(4, "Time", [
            ("きのう", "kinoo", "yesterday"), ("～じかん", "...jikan", "... hours"),
            ("いちじかん", "ichijikan", "one hour"), ("せんしゅう", "senshuu", "last week"),
            ("とき", "toki", "when...; at the time of..."),
            ("げつようび", "getsuyoobi", "Monday"), ("かようび", "kayoobi", "Tuesday"),
            ("すいようび", "suiyoobi", "Wednesday"), ("もくようび", "mokuyoobi", "Thursday"),
            ("きんようび", "kinyoobi", "Friday"),
        ])
        + v(4, "U-verbs", [
            ("あう", "au", "to meet; to see (a person)"),
            ("ある", "aru", "there is... (non-living)"), ("かう", "kau", "to buy"),
            ("かく", "kaku", "to write"), ("とる", "toru", "to take (a picture)"),
            ("まつ", "matsu", "to wait"), ("わかる", "wakaru", "to understand"),
        ])
        + v(4, "R-verb", [
            ("いる", "iru", "(a person) is in...; stays at..."),
        ])
        + v(4, "Adverbs & Expressions", [
            ("～ぐらい", "...gurai", "about (approximate measurement)"),
            ("ごめんなさい", "gomen nasai", "I'm sorry."),
            ("それから", "sorekara", "and then"), ("だから", "dakara", "so; therefore"),
            ("たくさん", "takusan", "many; a lot"),
            ("～と", "...to", "together with (a person); and"),
            ("どうして", "dooshite", "why"),
            ("ひとりで", "hitoride", "alone"),
            ("もしもし", "moshi moshi", "Hello? (used on the phone)"),
        ])
        + v(4, "Location Words", [
            ("みぎ", "migi", "right"), ("ひだり", "hidari", "left"),
            ("まえ", "mae", "front"), ("うしろ", "ushiro", "back"),
            ("なか", "naka", "inside"), ("うえ", "ue", "on; above"),
            ("した", "shita", "under; below"), ("ちかく", "chikaku", "near; nearby"),
            ("となり", "tonari", "next to"), ("あいだ", "aida", "between"),
        ])
    ),
    grammar=[
        g(4, "1. Xがあります / います", '"There is X." あります for non-living things, います for living things.',
          [("つくえの上に本があります。", "There is a book on the desk."),
           ("公園に子供がいます。", "There are children in the park.")]),
        g(4, "2. Describing Where Things Are", "Use location words + の + noun.",
          [("銀行は図書館のとなりです。", "The bank is next to the library.")]),
        g(4, "3. Past Tense of です", "Affirmative: でした. Negative: じゃなかったです / じゃありませんでした.",
          [("山下先生は学生でした。", "Prof. Yamashita was a student.")]),
        g(4, "4. Past Tense of Verbs", "Affirmative: ～ました. Negative: ～ませんでした.",
          [("メアリーさんは九時ごろうちに帰りました。", "Mary returned home at about nine.")]),
        g(4, "5. も for actions", '"Also/too" for actions. Replaces を, が, は. Follows other particles.',
          [("私は京都に行きました。大阪にも行きました。", "I went to Kyoto. I went to Osaka, too.")]),
        g(4, "6. 一時間", "Counter for hours.",
          [("一時間待ちました。", "I waited for one hour.")]),
        g(4, "7. たくさん", '"A lot/many". Can be used with を or が.',
          [("写真をたくさん撮りました。", "I took a lot of pictures.")]),
        g(4, "8. と", '"And" for nouns; "together with" for people.',
          [("日本語と英語を話します。", "I speak Japanese and English."),
           ("メアリーさんはソラさんと韓国に行きます。", "Mary will go to Korea with Sora.")]),
    ],
    culture=[
        "元日 (New Year's Day): January 1", "成人の日 (Coming-of-Age Day): 2nd Monday of January",
        "建国記念の日 (National Foundation Day): February 11",
        "天皇誕生日 (Emperor's Birthday): February 23",
        "春分の日 (Vernal Equinox Day): Around March 21",
        "昭和の日 (Showa Day): April 29", "憲法記念日 (Constitution Day): May 3",
        "みどりの日 (Greenery Day): May 4", "こどもの日 (Children's Day): May 5",
        "海の日 (Marine Day): 3rd Monday of July", "山の日 (Mountain Day): August 11",
        "敬老の日 (Respect-for-the-Aged Day): 3rd Monday of September",
        "秋分の日 (Autumnal Equinox Day): Around September 23",
        "スポーツの日 (Sports Day): 2nd Monday of October",
        "文化の日 (Culture Day): November 3",
        "勤労感謝の日 (Labor Thanksgiving Day): November 23",
        "Golden Week: April 29 to May 5",
    ],
    useful=p("Directions (みちをきく/おしえる)", [
        ("まっすぐいく", "massugu iku", "go straight"),
        ("ひだりにまがる", "hidari ni magaru", "turn left"),
        ("みぎにまがる", "migi ni magaru", "turn right"),
        ("みちをわたる", "michi o wataru", "cross the street"),
        ("ふたつめのかどをひだりにまがる", "futatsume no kado o hidari ni magaru",
         "turn left at the second corner"),
        ("ひとつめのしんごうをみぎにまがる", "hitotsume no shingoo o migi ni magaru",
         "turn right at the first traffic light"),
        ("みちのひだりがわ", "michi no hidari gawa", "left side of the street"),
        ("みちのみぎがわ", "michi no migi gawa", "right side of the street"),
        ("きた", "kita", "north"), ("にし", "nishi", "west"),
        ("ひがし", "higashi", "east"), ("みなみ", "minami", "south"),
    ]),
)

LESSON_5 = Lesson(
    number=5,
    title_jp="沖縄旅行",
    title_en="A Trip to Okinawa",
    vocab=(
        v(5, "Nouns", [
            ("たべもの", "tabemono", "food"), ("のみもの", "nomimono", "drink"),
            ("くだもの", "kudamono", "fruit"), ("やすみ", "yasumi", "holiday; day off; absence"),
            ("りょこう", "ryokoo", "travel"), ("うみ", "umi", "sea"),
            ("サーフィン", "saafin", "surfing"), ("おみやげ", "omiyage", "souvenir"),
            ("バス", "basu", "bus"), ("てんき", "tenki", "weather"),
            ("しゅくだい", "shukudai", "homework"), ("テスト", "tesuto", "test"),
            ("たんじょうび", "tanjoobi", "birthday"), ("へや", "heya", "room"),
            ("ぼく", "boku", "I (used by men)"), ("Lサイズ", "eru saizu", "size L"),
        ])
        + v(5, "い-adjectives", [
            ("あたらしい", "atarashii", "new"), ("ふるい", "furui", "old (thing)"),
            ("あつい", "atsui", "hot (weather / thing)"), ("さむい", "samui", "cold (weather)"),
            ("いそがしい", "isogashii", "busy"), ("おおきい", "ookii", "large"),
            ("ちいさい", "chiisai", "small"), ("おもしろい", "omoshiroi", "interesting; funny"),
            ("つまらない", "tsumaranai", "boring"),
            ("やさしい", "yasashii", "easy (problem); kind (person)"),
            ("むずかしい", "muzukashii", "difficult"), ("かっこいい", "kakkoii", "good-looking"),
            ("こわい", "kowai", "frightening"), ("たのしい", "tanoshii", "fun"),
            ("やすい", "yasui", "inexpensive; cheap"),
        ])
        + v(5, "な-adjectives", [
            ("すき(な)", "suki (na)", "fond of; to like"),
            ("きらい(な)", "kirai (na)", "disgusted with; to dislike"),
            ("だいすき(な)", "daisuki (na)", "very fond of; to love"),
            ("だいきらい(な)", "daikirai (na)", "to hate"),
            ("きれい(な)", "kirei (na)", "beautiful; clean"),
            ("げんき(な)", "genki (na)", "healthy; energetic"),
            ("しずか(な)", "shizuka (na)", "quiet"),
            ("にぎやか(な)", "nigiyaka (na)", "lively"),
            ("ひま(な)", "hima (na)", "not busy; free (time)"),
        ])
        + v(5, "U-verbs", [
            ("およぐ", "oyogu", "to swim"), ("きく", "kiku", "to ask"),
            ("のる", "noru", "to ride; to board"), ("やる", "yaru", "to do; to perform"),
        ])
        + v(5, "R-verb", [("でかける", "dekakeru", "to go out")])
        + v(5, "Adverbs & Expressions", [
            ("いっしょに", "issho ni", "together"), ("すごく", "sugoku", "extremely"),
            ("だいじょうぶ", "daijoobu", "It's okay; Not to worry"),
            ("とても", "totemo", "very"), ("どんな", "donna", "what kind of..."),
            ("～まい", "...mai", "[counter for flat objects]"),
        ])
    ),
    grammar=[
        g(5, "1. Adjectives (Present Tense)", "い-adj: ～いです / ～くないです. な-adj: ～です / ～じゃないです.",
          [("さむいです。", "It is cold."), ("さむくないです。", "It is not cold."),
           ("元気です。", "She is healthy."), ("元気じゃないです。", "She is not healthy.")]),
        g(5, "2. Adjectives (Past Tense)", "い-adj: ～かったです / ～くなかったです. な-adj: ～でした / ～じゃなかったです.",
          [("たかい → たかかったです / たかくなかったです", "expensive → was expensive / was not"),
           ("きれい → きれいでした / きれいじゃなかったです", "pretty → was pretty / was not")]),
        g(5, "3. Adjectives (Noun Modification)", "い-adj + Noun. な-adj + な + Noun.",
          [("おもしろい映画", "interesting movie"), ("きれいな写真", "beautiful picture")]),
        g(5, "4. 好き(な) / きらい(な)", "XはYが好きです。 (X likes Y.)",
          [("ロバートさんは日本語のクラスが好きです。", "Robert likes his Japanese class.")]),
        g(5, "5. ～ましょう / ～ましょうか", "\"Let's...\" / \"Shall we...?\"",
          [("泳ぎましょう。", "Let's swim."),
           ("あした一緒にやりましょうか。", "Shall we do it together tomorrow?")]),
        g(5, "6. Counting (～枚)", "Different counters for different items. ～枚 (mai) for flat objects.",
          [("二枚ください。", "Two (flat objects), please.")]),
    ],
    culture=[
        "札幌雪祭り (Sapporo Snow Festival): February, snow sculptures.",
        "青森ねぶた祭り (Aomori Nebuta Festival): August 2–7, large lantern floats.",
        "京都祇園祭 (Kyoto Gion Festival): July, traditional parade.",
        "徳島阿波踊り (Tokushima Awa Dance Festival): August 12–15, dancing parade.",
        "仙台七夕祭り (Sendai Tanabata Festival): August 6–8, colorful paper decorations.",
    ],
    useful=p("Colors (いろ)", [
        ("あか", "aka", "red"), ("あお", "ao", "blue"), ("きいろ", "kiro", "yellow"),
        ("みどり", "midori", "green"), ("しろ", "shiro", "white"),
        ("くろ", "kuro", "black"), ("むらさき", "murasaki", "purple"),
        ("ピンク", "pinku", "pink"), ("オレンジ", "orenji", "orange"),
        ("ちゃいろ", "chairo", "brown"), ("はいいろ", "haiiro", "gray"),
    ]),
)

LESSON_6 = Lesson(
    number=6,
    title_jp="ロバートさんの一日",
    title_en="A Day in Robert's Life",
    vocab=(
        v(6, "Nouns", [
            ("かんじ", "kanji", "kanji; Chinese character"),
            ("きょうかしょ", "kyookasho", "textbook"), ("ページ", "peeji", "page"),
            ("つぎ", "tsugi", "next"), ("おかね", "okane", "money"),
            ("にもつ", "nimotsu", "baggage"), ("パソコン", "pasokon", "personal computer"),
            ("シャワー", "shawaa", "shower"), ("エアコン", "eakon", "air conditioner"),
            ("でんき", "denki", "electricity; light"), ("まど", "mado", "window"),
            ("でんしゃ", "densha", "train"), ("くに", "kuni", "country; place of origin"),
            ("こんしゅう", "konshuu", "this week"), ("らいしゅう", "raishuu", "next week"),
            ("らいねん", "rainen", "next year"), ("よる", "yoru", "night"),
        ])
        + v(6, "な-adjective", [("たいへん(な)", "taihen (na)", "tough (situation)")])
        + v(6, "U-verbs", [
            ("あそぶ", "asobu", "to play; to spend time pleasantly"),
            ("いそぐ", "isogu", "to hurry"), ("かえす", "kaesu", "to return (a thing)"),
            ("けす", "kesu", "to turn off; to erase"), ("しぬ", "shinu", "to die"),
            ("すわる", "suwaru", "to sit down"), ("たつ", "tatsu", "to stand up"),
            ("たばこをすう", "tabako o suu", "to smoke"), ("つかう", "tsukau", "to use"),
            ("てつだう", "tetsudau", "to help"), ("はいる", "hairu", "to enter"),
            ("もつ", "motsu", "to carry; to hold"),
            ("やすむ", "yasumu", "to be absent; to rest"),
        ])
        + v(6, "R-verbs", [
            ("あける", "akeru", "to open (something)"),
            ("しめる", "shimeru", "to close (something)"),
            ("おしえる", "oshieru", "to teach; to instruct"),
            ("わすれる", "wasureru", "to forget; to leave behind"),
            ("おりる", "oriru", "to get off"), ("かりる", "kariru", "to borrow"),
            ("シャワーをあびる", "shawaa o abiru", "to take a shower"),
            ("つける", "tsukeru", "to turn on"),
        ])
        + v(6, "Irregular Verbs", [
            ("でんわする", "denwa suru", "to call"),
            ("つれてくる", "tsuretekuru", "to bring (a person)"),
            ("もってくる", "mottekuru", "to bring (a thing)"),
        ])
        + v(6, "Adverbs & Expressions", [
            ("あとで", "atode", "later on"), ("すぐ", "sugu", "right away"),
            ("ゆっくり", "yukkuri", "slowly; leisurely"),
            ("けっこうです", "kekkoo desu", "That would be fine.; That wouldn't be necessary."),
            ("ほんとうですか", "hontoo desu ka", "Really?"),
        ])
    ),
    grammar=[
        g(6, "1. Te-form", "Ru-verbs: る → て. U-verbs: う/つ/る → って; む/ぶ/ぬ → んで; く → いて; ぐ → いで; す → して. Irregular: する → して, くる → きて.",
          [("食べる → 食べて", "eat → eating/and eat"), ("書く → 書いて", "write → writing/and write"),
           ("する → して", "do → doing/and do")]),
        g(6, "2. ～てください", '"Please do..."',
          [("窓を開けてください。", "Please open the window.")]),
        g(6, "3. Describing Two Activities", "Te-form + Te-form + Verb.",
          [("朝起きて、コーヒーを飲みます。", "I get up in the morning and drink coffee.")]),
        g(6, "4. ～てもいいです", '"You may do..." / "Is it okay if I do...?"',
          [("写真を撮ってもいいですか。", "May I take a picture?")]),
        g(6, "5. ～てはいけません", '"You must not do..."',
          [("クラスで寝てはいけません。", "You must not sleep in class.")]),
        g(6, "6. ～から", '"Because..."',
          [("あしたテストがありますから。", "Because we will have an exam tomorrow.")]),
        g(6, "7. ～ましょうか (Offering Assistance)", '"Shall I do...?" / "Let me do..."',
          [("荷物を持ちましょうか。", "Shall I carry your bag?")]),
    ],
    culture=[
        "Elementary School: 6 years. Junior High: 3 years (compulsory).",
        "High School: 3 years (not compulsory). University: 4 years.",
        "School year starts in April and ends in March.",
        "Summer vacation: late July to August. Winter vacation: late December to early January. Spring vacation: late March to early April.",
    ],
    useful=p("Directions (みちをきく/おしえる)", [
        ("まっすぐいく", "massugu iku", "go straight"),
        ("ひだりにまがる", "hidari ni magaru", "turn left"),
        ("みぎにまがる", "migi ni magaru", "turn right"),
        ("みちをわたる", "michi o wataru", "cross the street"),
        ("ふたつめのかどをひだりにまがる", "futatsume no kado o hidari ni magaru",
         "turn left at the second corner"),
        ("ひとつめのしんごうをみぎにまがる", "hitotsume no shingoo o migi ni magaru",
         "turn right at the first traffic light"),
        ("みちのひだりがわ", "michi no hidari gawa", "left side of the street"),
        ("みちのみぎがわ", "michi no migi gawa", "right side of the street"),
        ("きた", "kita", "north"), ("にし", "nishi", "west"),
        ("ひがし", "higashi", "east"), ("みなみ", "minami", "south"),
    ]),
)

LESSONS_A: list[Lesson] = [LESSON_1, LESSON_2, LESSON_3, LESSON_4, LESSON_5, LESSON_6]
