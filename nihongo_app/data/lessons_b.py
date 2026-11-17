"""Genki I (3rd Edition) — Lessons 7 to 12."""
from __future__ import annotations

from ..core.models import GrammarPoint, Lesson, Phrase, VocabItem
from .lessons_a import g, p, v


LESSON_7 = Lesson(
    number=7,
    title_jp="家族の写真",
    title_en="Family Picture",
    vocab=(
        v(7, "Nouns", [
            ("かぞく", "kazoku", "family"),
            ("おじいさん", "ojiisan", "grandfather; old man"),
            ("おばあさん", "obaasan", "grandmother; old woman"),
            ("おにいさん", "oniisan", "older brother"),
            ("おねえさん", "oneesan", "older sister"),
            ("ちち", "chichi", "(my) father"), ("はは", "haha", "(my) mother"),
            ("あに", "ani", "(my) older brother"), ("あね", "ane", "(my) older sister"),
            ("いもうと", "imooto", "younger sister"),
            ("おとうと", "otooto", "younger brother"),
            ("きょうだい", "kyoodai", "brothers and sisters"),
            ("おとこのひと", "otoko no hito", "man"),
            ("おんなのひと", "onna no hito", "woman"),
            ("かいしゃ", "kaisha", "company"), ("しょくどう", "shokudoo", "cafeteria; dining commons"),
            ("デパート", "depaato", "department store"), ("かみ", "kami", "hair"),
            ("くち", "kuchi", "mouth"), ("め", "me", "eye"),
            ("めがね", "megane", "glasses"), ("うた", "uta", "song"),
            ("サークル", "saakuru", "club activity"), ("くるま", "kuruma", "car"),
        ])
        + v(7, "い-adjectives", [
            ("ながい", "nagai", "long"), ("みじかい", "mijikai", "short (length)"),
            ("はやい", "hayai", "fast"), ("せがたかい", "se ga takai", "tall (stature)"),
            ("せがひくい", "se ga hikui", "short (stature)"),
            ("あたまがいい", "atama ga ii", "bright; smart; clever"),
            ("かわいい", "kawaii", "cute"),
        ])
        + v(7, "な-adjectives", [
            ("しんせつ(な)", "shinsetsu (na)", "kind"),
            ("べんり(な)", "benri (na)", "convenient"),
        ])
        + v(7, "U-verbs", [
            ("うたう", "utau", "to sing"), ("かぶる", "kaburu", "to put on (a hat)"),
            ("はく", "haku", "to put on (items below your waist)"),
            ("しる", "shiru", "to get to know"), ("すむ", "sumu", "to live"),
            ("はたらく", "hataraku", "to work"), ("ふとる", "futoru", "to gain weight"),
        ])
        + v(7, "R-verbs", [
            ("かける", "kakeru", "to put on (glasses)"),
            ("きる", "kiru", "to put on (clothes above your waist)"),
            ("やせる", "yaseru", "to lose weight"),
        ])
        + v(7, "Irregular Verb", [("けっこんする", "kekkon suru", "to get married")])
        + v(7, "Adverbs & Expressions", [
            ("～が", "...ga", "... but"),
            ("なにも + negative", "nanimo", "not ... anything"),
            ("～にん", "...nin", "[counter for people]"),
            ("ひとり", "hitori", "one person"), ("ふたり", "futari", "two people"),
            ("べつに + negative", "betsuni", "nothing in particular"),
            ("もちろん", "mochiron", "of course"), ("よかったら", "yokattara", "if you like"),
        ])
    ),
    grammar=[
        g(7, "1. ～ている (Action in Progress)", "Verb te-form + いる = action in progress or habitual action.",
          [("ソラさんは今勉強しています。", "Sora is studying right now.")]),
        g(7, "2. ～ている (Result of a Change)", "For change verbs, describes a state resulting from a past change.",
          [("山下先生は結婚しています。", "Professor Yamashita is married.")]),
        g(7, "3. メアリーさんは髪が長いです", "Describing physical attributes: Person は Body Part が Adjective.",
          [("トムさんは髪が長いです。", "Tom has long hair.")]),
        g(7, "4. Adjective/Noun Te-forms for Joining Sentences", "い-adj: ～くて. な-adj: ～で. Noun: ～で.",
          [("安い → 安くて", "cheap → cheap and"), ("元気 → 元気で", "healthy → healthy and"),
           ("日本人 → 日本人で", "Japanese person → being Japanese and")]),
        g(7, "5. Verb Stem + に行く", "Go to a place to do something. Verb stem + に + 行く/来る/帰る.",
          [("デパートにかばんを買いに行きました。", "I went to a department store to buy a bag.")]),
        g(7, "6. Counting People", "一人 (hitori), 二人 (futari), 三人 (sannin), etc.",
          [("私のクラスにインドネシア人の学生が一人います。",
            "There is one Indonesian student in our class.")]),
    ],
    culture=[
        "Different terms are used for one's own family vs. someone else's family.",
        "Someone else's family: お父さん, お母さん, お兄さん, お姉さん.",
        "My family (formal): 父, 母, 兄, 姉.",
        "My family (casual): お父さん, お母さん, etc.",
    ],
    useful=p("Parts of the Body (からだのぶぶん)", [
        ("あたま", "atama", "head"), ("かみ", "kami", "hair"), ("かお", "kao", "face"),
        ("め", "me", "eye"), ("みみ", "mimi", "ear"), ("はな", "hana", "nose"),
        ("くち", "kuchi", "mouth"), ("は", "ha", "tooth"), ("くび", "kubi", "neck"),
        ("かた", "kata", "shoulder"), ("むね", "mune", "chest"), ("おなか", "onaka", "stomach"),
        ("せなか", "senaka", "back"), ("おしり", "oshiri", "buttocks"),
        ("あし", "ashi", "leg/foot"), ("て", "te", "hand"), ("ゆび", "yubi", "finger"),
    ]),
)

LESSON_8 = Lesson(
    number=8,
    title_jp="バーベキュー",
    title_en="Barbecue",
    vocab=(
        v(8, "Nouns", [
            ("はれ", "hare", "sunny weather"), ("あめ", "ame", "rain"),
            ("くもり", "kumori", "cloudy weather"), ("ゆき", "yuki", "snow"),
            ("てんきよほう", "tenkiyohoo", "weather forecast"),
            ("きおん", "kion", "temperature"), ("なつ", "natsu", "summer"),
            ("ふゆ", "fuyu", "winter"), ("けさ", "kesa", "this morning"),
            ("あさって", "asatte", "the day after tomorrow"),
            ("まいしゅう", "maishuu", "every week"), ("こんげつ", "kongetsu", "this month"),
            ("らいげつ", "raigetsu", "next month"),
            ("かいしゃいん", "kaishain", "office worker"),
            ("しごと", "shigoto", "job; work; occupation"),
            ("カメラ", "kamera", "camera"), ("カラオケ", "karaoke", "karaoke"),
            ("ところ", "tokoro", "place"), ("トマト", "tomato", "tomato"),
            ("はし", "hashi", "chopsticks"), ("パーティー", "paatii", "party"),
            ("バーベキュー", "baabekyuu", "barbecue"),
            ("ホームステイ", "hoomusutei", "homestay"), ("おふろ", "ofuro", "bath"),
            ("スペイン", "Supein", "Spain"), ("なにか", "nanika", "something"),
        ])
        + v(8, "な-adjectives", [
            ("じょうず(な)", "joozu (na)", "skillful; good at"),
            ("へた(な)", "heta (na)", "clumsy; poor at"),
            ("ゆうめい(な)", "yuumei (na)", "famous"),
        ])
        + v(8, "U-verbs", [
            ("あらう", "arau", "to wash"), ("いう", "iu", "to say"),
            ("いる", "iru", "to need"), ("おそくなる", "osokunaru", "to be late"),
            ("おふろにはいる", "ofuro ni hairu", "to take a bath"),
            ("おもう", "omou", "to think"), ("きる", "kiru", "to cut"),
            ("つくる", "tsukuru", "to make"),
            ("(あめ/ゆきが)ふる", "(ame/yuki ga) furu", "(rain/snow) falls"),
            ("もっていく", "motteiku", "to take (a thing)"),
        ])
        + v(8, "R-verbs", [
            ("すてる", "suteru", "to throw away"), ("はじめる", "hajimeru", "to begin"),
        ])
        + v(8, "Irregular Verbs", [
            ("うんてんする", "unten suru", "to drive"),
            ("せんたくする", "sentaku suru", "to do laundry"),
            ("そうじする", "sooji suru", "to clean"),
            ("りょうりする", "ryoori suru", "to cook"),
        ])
        + v(8, "Adverbs & Expressions", [
            ("うん", "un", "uh-huh; yes"), ("ううん", "uun", "uh-uh; no"),
            ("いつも", "itsumo", "always"), ("おそく", "osoku", "(do something) late"),
            ("かんぱい", "kanpai", "Cheers!"), ("みんなで", "minna de", "all (of the people) together"),
            ("ざんねん(です)", "zannen (desu)", "That's too bad."),
            ("まだ", "mada", "not...yet"),
            ("～について", "...ni tsuite", "about...; concerning..."),
            ("～ど", "...do", "...degrees (temperature)"), ("どう", "doo", "how"),
        ])
    ),
    grammar=[
        g(8, "1. Short Forms", "Present affirmative: verbs dictionary form; い-adj drop です; な-adj/Noun replace です with だ. Present negative: verbs ～ない; い-adj ～くない; な-adj/Noun ～じゃない.",
          [("読む / かわいい / 静かだ / 学生だ", "read / cute / quiet / student"),
           ("読まない / かわいくない / 静かじゃない / 学生じゃない", "don't read / not cute / not quiet / not a student")]),
        g(8, "2. Short Forms in Informal Speech", "Used with close friends/family. Drop particles, use rising intonation for questions.",
          [("元気？", "Are you good?"), ("うん、元気。", "Yes, I am.")]),
        g(8, "3. ～と思います", '"I think that..." (quoted speech with short forms).',
          [("たけしさんはメアリーさんが好きだと思います。", "I think Takeshi likes Mary.")]),
        g(8, "4. ～と言っていました", '"Someone said that..."',
          [("けんさんはアルバイトがあると言っていました。", "Ken said he had a part-time job.")]),
        g(8, "5. ～ないでください", "\"Please don't do...\"",
          [("まだ飲まないでください。", "Please don't drink yet.")]),
        g(8, "6. Verb のが好きです/上手です", '"I like doing..." / "I am good at doing..."',
          [("ロバートさんは料理するのが好きです。", "Robert likes cooking.")]),
        g(8, "7. Subject Particle が", "Marks the subject of a sentence, especially with 好き, 上手, etc.",
          [("ロバートさんは日本語が上手です。", "Robert is good at Japanese.")]),
        g(8, "8. 何か and 何も", "何か = something. 何も + negative = nothing.",
          [("何か持っていきましょうか。", "Shall I bring something?"),
           ("何もいらないと思います。", "I think nothing is needed.")]),
    ],
    culture=[
        "Japanese foods: すし (sushi), てんぷら (tempura), そば (soba), うどん (udon), ラーメン (ramen), カレー (curry), とんかつ (tonkatsu).",
        "Meal etiquette: say いただきます before eating and ごちそうさまでした after.",
    ],
    useful=p("At the Supermarket (スーパーで)", [
        ("すみません", "sumimasen", "Excuse me"),
        ("～はどこですか", "...wa doko desu ka", "Where is ~?"),
        ("～をください", "...o kudasai", "Please give me ~"),
        ("いくらですか", "ikura desu ka", "How much is it?"),
        ("おねがいします", "onegaishimasu", "Please"),
        ("ありがとうございました", "arigatoo gozaimashita", "Thank you very much"),
    ]),
)

LESSON_9 = Lesson(
    number=9,
    title_jp="かぶき",
    title_en="Kabuki",
    vocab=(
        v(9, "Nouns", [
            ("かぶき", "kabuki", "Kabuki"), ("おんがく", "ongaku", "music"),
            ("え", "e", "picture"), ("きっぷ", "kippu", "ticket"),
            ("こども", "kodomo", "child"), ("すもう", "sumoo", "sumo"),
            ("ちかてつ", "chikatetsu", "subway"), ("でんしゃ", "densha", "train"),
            ("にほんりょうり", "nihon ryoori", "Japanese food"),
            ("はなみ", "hanami", "flower viewing"),
            ("びじゅつかん", "bijutsukan", "art museum"),
            ("まつり", "matsuri", "festival"), ("やきゅう", "yakyuu", "baseball"),
        ])
        + v(9, "い-adjectives", [
            ("うつくしい", "utsukushii", "beautiful"), ("おそい", "osoi", "slow"),
            ("こい", "koi", "dark (color); thick"), ("こわい", "kowai", "frightening"),
            ("つまらない", "tsumaranai", "boring"), ("ひろい", "hiroi", "wide; spacious"),
            ("ふるい", "furui", "old"), ("まずい", "mazui", "tastes bad"),
        ])
        + v(9, "な-adjectives", [
            ("すてき(な)", "suteki (na)", "lovely; wonderful"),
            ("にんき(な)", "ninki (na)", "popular"),
        ])
        + v(9, "U-verbs", [
            ("うたう", "utau", "to sing"), ("おどる", "odoru", "to dance"),
            ("おわる", "owaru", "to finish"), ("けいかくする", "keikaku suru", "to plan"),
            ("さく", "saku", "to bloom"), ("つかれる", "tsukareru", "to get tired"),
            ("のぼる", "noboru", "to climb"), ("はしる", "hashiru", "to run"),
        ])
        + v(9, "R-verbs", [
            ("きめる", "kimeru", "to decide"),
            ("でる", "deru", "to appear; to leave"),
            ("はじまる", "hajimaru", "to begin"),
        ])
        + v(9, "Irregular Verbs", [
            ("けんぶつする", "kenbutsu suru", "to go sightseeing"),
            ("よやくする", "yoyaku suru", "to reserve"),
        ])
        + v(9, "Adverbs & Expressions", [
            ("いちばん", "ichiban", "best; most"), ("おそらく", "osoraku", "probably"),
            ("きっと", "kitto", "surely"), ("たぶん", "tabun", "probably; maybe"),
            ("はやく", "hayaku", "early; quickly"), ("まっすぐ", "massugu", "straight"),
            ("みんなで", "minna de", "all together"), ("もちろん", "mochiron", "of course"),
            ("よかったら", "yokattara", "if you like"),
        ])
    ),
    grammar=[
        g(9, "1. Past Tense Short Forms", "Verbs: ～た / ～なかった. い-adj: ～かった / ～くなかった. な-adj/Noun: ～だった / ～じゃなかった.",
          [("読んだ / 読まなかった", "read / didn't read"),
           ("かわいかった / かわいくなかった", "was cute / wasn't cute"),
           ("静かだった / 静かじゃなかった", "was quiet / wasn't quiet")]),
        g(9, "2. Past Tense Short Forms in Informal Speech", "Used in casual conversation.",
          [("昨日、映画を見た？", "Did you see a movie yesterday?")]),
        g(9, "3. ～と思います (past)", '"I thought that..."',
          [("明日は雨が降ると思います。", "I think it will rain tomorrow.")]),
        g(9, "4. ～と言っていました (past)", '"Someone said that..."',
          [("たけしさんは昨日学校を休んだと言っていました。",
            "Takeshi said he was absent from school yesterday.")]),
        g(9, "5. Qualifying Nouns with Verbs and Adjectives", "Short form + Noun.",
          [("昨日買った本", "the book I bought yesterday"), ("おいしい料理", "delicious food")]),
        g(9, "6. もう～ました / まだ～ていません", "もう～ました = have already done. まだ～ていません = have not done yet.",
          [("もう昼ご飯を食べました。", "I have already eaten lunch."),
           ("まだ食べていません。", "I haven't eaten yet.")]),
        g(9, "7. Explanation から", "から at the end of a sentence to explain a reason.",
          [("明日テストがありますから。", "Because I have a test tomorrow.")]),
    ],
    culture=[
        "Kabuki: traditional Japanese drama with elaborate costumes and makeup.",
        "Sumo: traditional Japanese wrestling.",
        "Flower Viewing (Hanami): enjoying cherry blossoms in spring.",
        "Tea Ceremony (Sadou): traditional way of preparing and drinking tea.",
    ],
    useful=p("Colors (いろ)", [
        ("あか", "aka", "red"), ("あお", "ao", "blue"), ("きいろ", "kiro", "yellow"),
        ("みどり", "midori", "green"), ("しろ", "shiro", "white"),
        ("くろ", "kuro", "black"), ("むらさき", "murasaki", "purple"),
        ("ピンク", "pinku", "pink"), ("オレンジ", "orenji", "orange"),
        ("ちゃいろ", "chairo", "brown"), ("はいいろ", "haiiro", "gray"),
    ]),
)

LESSON_10 = Lesson(
    number=10,
    title_jp="冬休みの予定",
    title_en="Winter Vacation Plans",
    vocab=(
        v(10, "Nouns", [
            ("あき", "aki", "fall"), ("いちがつ", "ichigatsu", "January"),
            ("おしょうがつ", "oshoogatsu", "New Year's"), ("おんせん", "onsen", "hot spring"),
            ("がいこく", "gaikoku", "foreign country"), ("きせつ", "kisetsu", "season"),
            ("くうこう", "kuukoo", "airport"), ("しちがつ", "shichigatsu", "July"),
            ("しゅう", "shuu", "week"), ("しんぶん", "shinbun", "newspaper"),
            ("にがつ", "nigatsu", "February"), ("はる", "haru", "spring"),
            ("ふゆやすみ", "fuyuyasumi", "winter vacation"),
            ("ほっかいどう", "Hokkaidoo", "Hokkaido"), ("りょこう", "ryokoo", "travel"),
        ])
        + v(10, "い-adjectives", [
            ("あたたかい", "atatakai", "warm"), ("すずしい", "suzushii", "cool"),
            ("つめたい", "tsumetai", "cold (thing)"), ("ねむい", "nemui", "sleepy"),
            ("ひろい", "hiroi", "wide; spacious"),
        ])
        + v(10, "な-adjectives", [
            ("かんたん(な)", "kantan (na)", "easy; simple"),
            ("たいへん(な)", "taihen (na)", "tough"),
            ("べんり(な)", "benri (na)", "convenient"),
        ])
        + v(10, "U-verbs", [
            ("おくる", "okuru", "to send"), ("おわる", "owaru", "to finish"),
            ("かえす", "kaesu", "to return (a thing)"),
            ("けいかくする", "keikaku suru", "to plan"),
            ("さがす", "sagasu", "to look for"), ("する", "suru", "to do"),
            ("つかう", "tsukau", "to use"), ("てつだう", "tetsudau", "to help"),
            ("とまる", "tomaru", "to stay (at a hotel)"),
            ("はじまる", "hajimaru", "to begin"),
        ])
        + v(10, "R-verbs", [
            ("きめる", "kimeru", "to decide"), ("でかける", "dekakeru", "to go out"),
            ("みせる", "miseru", "to show"),
        ])
        + v(10, "Irregular Verbs", [
            ("けんぶつする", "kenbutsu suru", "to go sightseeing"),
            ("よやくする", "yoyaku suru", "to reserve"),
        ])
        + v(10, "Adverbs & Expressions", [
            ("いちばん", "ichiban", "best; most"), ("いつか", "itsuka", "sometime"),
            ("おそらく", "osoraku", "probably"), ("きっと", "kitto", "surely"),
            ("たぶん", "tabun", "probably; maybe"), ("はやく", "hayaku", "early; quickly"),
            ("まっすぐ", "massugu", "straight"), ("みんなで", "minna de", "all together"),
            ("もちろん", "mochiron", "of course"), ("よかったら", "yokattara", "if you like"),
        ])
    ),
    grammar=[
        g(10, "1. Comparison between Two Items", "AはBより～です。 (A is more ~ than B.)",
          [("東京は大阪より大きいです。", "Tokyo is bigger than Osaka.")]),
        g(10, "2. Comparison among Three or More Items", "Aの中でBが一番～です。 (Among A, B is the most ~.)",
          [("日本の食べ物の中で寿司が一番好きです。", "Among Japanese food, I like sushi the most.")]),
        g(10, "3. Adjective/Noun + の", "の can replace a noun when the meaning is clear.",
          [("もっと大きいのをください。", "Please give me a bigger one.")]),
        g(10, "4. ～つもりだ", '"Intend to..."',
          [("冬休みに北海道に行くつもりです。", "I intend to go to Hokkaido during winter vacation.")]),
        g(10, "5. Adjective + なる", '"Become ~"',
          [("寒くなりました。", "It has become cold.")]),
        g(10, "6. どこかに / どこにも", "どこかに = somewhere. どこにも + negative = nowhere.",
          [("どこかに行きましたか。", "Did you go somewhere?"),
           ("どこにも行きませんでした。", "I didn't go anywhere.")]),
        g(10, "7. で (means/tool)", "Particle for means/tool.",
          [("電車で行きます。", "I will go by train.")]),
    ],
    culture=[
        "Trains: very punctual and efficient.", "Buses: useful for local travel.",
        "Subways: common in large cities.", "Taxis: expensive but convenient.",
        "IC Cards: Suica, Pasmo, Icoca are rechargeable cards for public transport.",
    ],
    useful=p("At the Station (えきで)", [
        ("きっぷ", "kippu", "ticket"), ("きっぷうりば", "kippu uriba", "ticket office"),
        ("みどりのまどぐち", "midori no madoguchi", "JR ticket office (Midori no Madoguchi)"),
        ("～はどこですか", "...wa doko desu ka", "Where is ~?"),
        ("～に行きたいです", "...ni ikitai desu", "I want to go to ~"),
        ("何時に出ますか", "nanji ni demasu ka", "What time does it leave?"),
        ("何番線ですか", "nanbansen desu ka", "Which platform?"),
    ]),
)

LESSON_11 = Lesson(
    number=11,
    title_jp="休みのあと",
    title_en="After the Vacation",
    vocab=(
        v(11, "Nouns", [
            ("おみやげ", "omiyage", "souvenir"), ("おんがく", "ongaku", "music"),
            ("かぜ", "kaze", "cold (illness)"), ("きって", "kitte", "stamp"),
            ("しゃしん", "shashin", "picture; photograph"), ("しゅみ", "shumi", "hobby"),
            ("つり", "tsuri", "fishing"), ("でんしゃ", "densha", "train"),
            ("にっき", "nikki", "diary"), ("はがき", "hagaki", "postcard"),
            ("びょういん", "byooin", "hospital"), ("ふね", "fune", "ship; boat"),
            ("ほん", "hon", "book"), ("やま", "yama", "mountain"),
        ])
        + v(11, "い-adjectives", [
            ("おそい", "osoi", "slow"), ("こわい", "kowai", "frightening"),
            ("つまらない", "tsumaranai", "boring"), ("ひどい", "hidoi", "terrible"),
            ("ふかい", "fukai", "deep"), ("やさしい", "yasashii", "kind; easy"),
        ])
        + v(11, "な-adjectives", [
            ("たいへん(な)", "taihen (na)", "tough"), ("ひま(な)", "hima (na)", "free (time)"),
        ])
        + v(11, "U-verbs", [
            ("おくる", "okuru", "to send"), ("おもう", "omou", "to think"),
            ("かえす", "kaesu", "to return (a thing)"), ("さがす", "sagasu", "to look for"),
            ("する", "suru", "to do"), ("つかう", "tsukau", "to use"),
            ("てつだう", "tetsudau", "to help"), ("とまる", "tomaru", "to stay (at a hotel)"),
            ("はじまる", "hajimaru", "to begin"),
        ])
        + v(11, "R-verbs", [
            ("きめる", "kimeru", "to decide"), ("でかける", "dekakeru", "to go out"),
            ("みせる", "miseru", "to show"),
        ])
        + v(11, "Irregular Verbs", [
            ("けんぶつする", "kenbutsu suru", "to go sightseeing"),
            ("よやくする", "yoyaku suru", "to reserve"),
        ])
        + v(11, "Adverbs & Expressions", [
            ("いちばん", "ichiban", "best; most"), ("いつか", "itsuka", "sometime"),
            ("おそらく", "osoraku", "probably"), ("きっと", "kitto", "surely"),
            ("たぶん", "tabun", "probably; maybe"), ("はやく", "hayaku", "early; quickly"),
            ("まっすぐ", "massugu", "straight"), ("みんなで", "minna de", "all together"),
            ("もちろん", "mochiron", "of course"), ("よかったら", "yokattara", "if you like"),
        ])
    ),
    grammar=[
        g(11, "1. ～たい", '"Want to do..."',
          [("日本に行きたいです。", "I want to go to Japan.")]),
        g(11, "2. ～たり～たりする", '"Do things like ... and ..."',
          [("週末は映画を見たり、本を読んだりします。",
            "On weekends, I do things like watch movies and read books.")]),
        g(11, "3. ～ことがある", '"Have done ~ before."',
          [("京都に行ったことがあります。", "I have been to Kyoto before.")]),
        g(11, "4. Noun Aや Noun B", '"A and B (among others)."',
          [("りんごやバナナを買いました。", "I bought apples and bananas, among other things.")]),
    ],
    culture=[
        "Oshoogatsu: New Year's, the most important holiday in Japan.",
        "Traditional foods: おせち料理 (osechi ryoori), もち (mochi).",
        "Visiting a shrine: 初詣 (hatsumoode).",
        "Otoshidama: money given to children by parents and relatives.",
    ],
    useful=p("In Japanese Class (にほんごのクラスで)", [
        ("しつもんがあります", "shitsumon ga arimasu", "I have a question"),
        ("もういちどおねがいします", "moo ichido onegaishimasu", "One more time, please"),
        ("ゆっくりおねがいします", "yukkuri onegaishimasu", "Slowly, please"),
        ("わかりました", "wakarimashita", "I understand"),
        ("わかりません", "wakarimasen", "I don't understand"),
        ("～はどういういみですか", "...wa doo iu imi desu ka", "What does ~ mean?"),
        ("～はにほんごでなんですか", "...wa nihongo de nan desu ka", "What is ~ in Japanese?"),
    ]),
)

LESSON_12 = Lesson(
    number=12,
    title_jp="病気",
    title_en="Feeling Ill",
    vocab=(
        v(12, "Nouns", [
            ("あたま", "atama", "head"), ("おなか", "onaka", "stomach"),
            ("かぜ", "kaze", "cold (illness)"), ("くすり", "kusuri", "medicine"),
            ("けが", "kega", "injury"), ("のど", "nodo", "throat"),
            ("は", "ha", "tooth"), ("びょうき", "byooki", "illness"),
            ("ねつ", "netsu", "fever"),
        ])
        + v(12, "い-adjectives", [
            ("いたい", "itai", "painful"), ("つかれた", "tsukareta", "tired"),
            ("ねむい", "nemui", "sleepy"), ("ひどい", "hidoi", "terrible"),
        ])
        + v(12, "な-adjectives", [
            ("しんぱい(な)", "shinpai (na)", "worried"),
            ("たいへん(な)", "taihen (na)", "tough"),
        ])
        + v(12, "U-verbs", [
            ("いたむ", "itamu", "to hurt"), ("かぜをひく", "kaze o hiku", "to catch a cold"),
            ("けがをする", "kega o suru", "to get injured"),
            ("ねつがある", "netsu ga aru", "to have a fever"),
            ("のむ", "nomu", "to take (medicine)"), ("やすむ", "yasumu", "to rest"),
        ])
        + v(12, "R-verbs", [
            ("でる", "deru", "to go out; to leave"), ("ねる", "neru", "to sleep"),
        ])
        + v(12, "Irregular Verbs", [("りょうりする", "ryoori suru", "to cook")])
        + v(12, "Adverbs & Expressions", [
            ("おだいじに", "odaiji ni", "Take care of yourself."),
            ("おやすみなさい", "oyasuminasai", "Good night."),
            ("げんきがない", "genki ga nai", "to look pale; to be in low spirits"),
            ("だいじょうぶ", "daijoobu", "It's okay."),
            ("どうしたんですか", "dooshitan desu ka", "What's the matter?"),
            ("びょういんに行く", "byooin ni iku", "to go to the hospital"),
            ("びょうきです", "byooki desu", "I am sick."),
        ])
    ),
    grammar=[
        g(12, "1. ～んです", "Explains a situation or gives a reason.",
          [("どうしたんですか。", "What's the matter?"),
           ("頭が痛いんです。", "The thing is, I have a headache.")]),
        g(12, "2. ～すぎる", '"Too much ~"',
          [("食べすぎました。", "I ate too much.")]),
        g(12, "3. ～ほうがいいです", '"It is better to do ~."',
          [("早く寝たほうがいいです。", "It is better to go to bed early.")]),
        g(12, "4. ～ので", '"Because ~" (more polite than から).',
          [("風邪をひいたので、学校を休みます。", "Because I caught a cold, I will be absent from school.")]),
        g(12, "5. ～なければいけません / ～なきゃいけません", '"Must do ~."',
          [("薬を飲まなければいけません。", "I must take medicine.")]),
        g(12, "6. ～でしょうか", '"I wonder if ~" (polite question).',
          [("これはいくらでしょうか。", "I wonder how much this is.")]),
    ],
    culture=[
        "Four distinct seasons: spring, summer, fall, winter.",
        "Rainy season (梅雨, tsuyu): June to July.",
        "Typhoons: late summer and early fall.",
        "Winter: cold in most areas, heavy snow in Hokkaido and on the Japan Sea coast.",
    ],
    useful=p("Health and Illness (けんこうとびょうき)", [
        ("げんきですか", "genki desu ka", "How are you?"),
        ("げんきです", "genki desu", "I'm fine."),
        ("ぐあいがわるいです", "guai ga warui desu", "I feel sick."),
        ("くすりをのみました", "kusuri o nomimashita", "I took medicine."),
        ("かぜをひきました", "kaze o hikimashita", "I caught a cold."),
        ("ねつがあります", "netsu ga arimasu", "I have a fever."),
        ("あたまがいたいです", "atama ga itai desu", "I have a headache."),
        ("おなかがいたいです", "onaka ga itai desu", "I have a stomachache."),
        ("びょういんに行きました", "byooin ni ikimashita", "I went to the hospital."),
        ("おだいじに", "odaiji ni", "Take care of yourself."),
    ]),
)

LESSONS_B: list[Lesson] = [LESSON_7, LESSON_8, LESSON_9, LESSON_10, LESSON_11, LESSON_12]
