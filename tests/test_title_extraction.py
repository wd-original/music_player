
from src.utils.str_match import process_title, SongTitleData, ErrCodes


athr1: str = "author1"
athr2: str = "author2"
athr3: str = "author3"
athr4: str = "author4"
comma: str = ", "
ex: str = " x "
ampers: str = " & "
# use as name[3:], skip ' - '
name: str = " - name"
ft: str = "ft. "
feat: str = "feat. "
featuring: str = "featuring "
feat1: str = "featuring1"
feat2: str = "featuring2"
feat3: str = "featuring3"
ov = "(Official Video)"
slowed = "(slowed)"
brackets = "[official tiktok version]"


def test_basic():
    assert SongTitleData([athr1], [], name[3:]) == process_title(athr1 + name)


def test_feat():
    assert SongTitleData([athr1], [feat1], name[3:]) == process_title(
        athr1 + feat + feat1 + name
    )


def test_multiple_feats():
    assert SongTitleData([athr1], [feat1, feat2, feat3], name[3:]) == (
        process_title(athr1 + ft + feat1 + ampers + feat2 + ex + feat3 + name)
    )


def test_multiple_authors():
    assert SongTitleData([athr1, athr2, athr3, athr4], [], name[3:]) == (
        process_title(athr1 + comma + athr2 + ampers + athr3 + ex + athr4 + name)
    )


# gemini generated ones (im jus lazy, but i can make em, and i made em, some of them are mine ackshally)
# --- New Combined & Edge Case Tests ---


def test_multiple_authors_and_features():
    # Combining multiple main authors and featured artists
    # Input: "author1, author2 ft. featuring1 & featuing2 - name"
    raw = athr1 + comma + athr2 + " " + ft + feat1 + ampers + feat2 + name
    expected = SongTitleData(
        authors=[athr1, athr2], feats=[feat1, feat2], song_name=name[3:]
    )
    assert expected == process_title(raw)


def test_multiple_authors_and_features_and_brackets_after():
    # Input: "author1, author2 ft. featuring1 & featuing2 - name (Official Video)"
    raw = athr1 + comma + athr2 + " " + ft + feat1 + ampers + feat2 + name + " " + ov
    expected = SongTitleData(
        authors=[athr1, athr2], feats=[feat1, feat2], song_name=name[3:]
    )
    assert expected == process_title(raw)


def test_title_with_parentheses_and_brackets():
    # Title containing metadata tags at the end
    # Input: "author1 - name (Official Video) [official tiktok version]"
    raw = athr1 + name + " " + ov + " " + brackets
    expected = SongTitleData(
        authors=[athr1],
        feats=[],
        song_name=name[3:]
    )
    assert expected == process_title(raw)


def test_title_with_parentheses_and_brackets_and_feat_between():
    # Input: "author1 - name (Official Video) featuring featuring1 [official tiktok version]"
    raw = athr1 + name + " " + ov + " " + featuring + feat1 + " " + brackets
    expected = SongTitleData(
        authors=[athr1],
        feats=[feat1],
        song_name=name[3:]
    )
    assert expected == process_title(raw)


def test_title_with_parentheses_and_brackets_and_feat_in_parantheses():
    # Input: "author1 - name (Official Video) (featuring featuring1) [official tiktok version]"
    raw = athr1 + name + " " + ov + " (" + featuring + feat1 + ") " + brackets
    expected = SongTitleData(
        authors=[athr1],
        feats=[feat1],
        song_name=name[3:]
    )
    assert expected == process_title(raw)


def test_title_with_parentheses_and_brackets_and_feat_after():
    # Input: "author1 - name (Official Video) [official tiktok version] featuring featuring1"
    raw = athr1 + name + " " + ov + " " + brackets + featuring + feat1
    expected = SongTitleData(
        authors=[athr1],
        feats=[feat1],
        song_name=name[3:]
    )
    assert expected == process_title(raw)


def test_title_with_parentheses_and_brackets_and_multiple_feat_in_parantheses():
    # Input: "author1 - name (Official Video) (featuring featuring1) [official tiktok version]"
    raw = athr1 + name + " " + ov + " (" + featuring + feat1 + comma + feat2 + ") " + brackets
    expected = SongTitleData(
        authors=[athr1],
        feats=[feat1, feat2],
        song_name=name[3:]
    )
    assert expected == process_title(raw)


def test_title_with_parentheses_and_brackets_and_multiple_feat_after():
    # Input: "author1 - name (Official Video) [official tiktok version] featuring featuring1 & featuring2 x featuring3"
    raw = athr1 + name + " " + ov + " " + brackets + featuring + feat1 + ampers + feat2 + ex + feat3
    expected = SongTitleData(
        authors=[athr1],
        feats=[feat1, feat2, feat3],
        song_name=name[3:]
    )
    assert expected == process_title(raw)


def test_features_in_parentheses():
    # Featuring artists inside parentheses after title
    # Input: "author1 - name (feat. featuring1)"
    raw = athr1 + name + f" ({feat}{feat1})"
    expected = SongTitleData(
        authors=[athr1], feats=[feat1], song_name=name[3:]
    )
    assert expected == process_title(raw)


def test_mixed_delimiters_and_descriptors():
    # Complex real-world pattern: Multiple authors (comma/x), featured artists (ft.), and audio descriptors
    # Input: "author1 x author2 ft. featuring1 - name (slowed)"
    raw = athr1 + ex + athr2 + " " + ft + feat1 + name + " " + slowed
    expected = SongTitleData(
        authors=[athr1, athr2], feats=[feat1], song_name=name[3:]
    )
    assert expected == process_title(raw)


def test_featuring_variation_spelling():
    # Test alternative featuring syntax ("feat." vs "ft.")
    raw_ft = athr1 + " " + ft + feat1 + name
    raw_feat = athr1 + " " + feat + feat1 + name
    assert process_title(raw_ft) == process_title(raw_feat)


extensive_test: list[tuple[str, SongTitleData]] = [
    ("Miyagi feat. HLOY - Try (Official Audio)", SongTitleData(authors=["Miyagi"], feats=["HLOY"], song_name="Try")),
    ("Miyagi - Sorry (Official Audio)", SongTitleData(authors=["Miyagi"], feats=[], song_name="Sorry")),
    ("Miyagi & Эндшпиль - Дама (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Дама")),
    ("Miyagi & Эндшпиль - When I Win (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="When I Win")),
    ("Miyagi feat. Ollane - Весна (Official Audio)", SongTitleData(authors=["Miyagi"], feats=["Ollane"], song_name="Весна")),
    ("Miyagi - Captain (Official Audio)", SongTitleData(authors=["Miyagi"], feats=[], song_name="Captain")),
    ("Miyagi & Эндшпиль - Колизей (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Колизей")),
    ("Эндшпиль feat. onna badvibes - Aura (Official Audio)", SongTitleData(authors=["Эндшпиль"], feats=["onna badvibes"], song_name="Aura")),
    ("Miyagi & Эндшпиль - Голгофа (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Голгофа")),
    ("Гуф - Письмо домой (Альбом Сам и)", SongTitleData(authors=["Гуф"], feats=[], song_name="Письмо домой")),
    ("Miyagi & Эндшпиль - Я хочу любить (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Я хочу любить")),
    ("Miyagi & Эндшпиль - Look at the Scars (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Look at the Scars")),
    ("Miyagi - Marlboro (Official Audio)", SongTitleData(authors=["Miyagi"], feats=[], song_name="Marlboro")),
    ("Miyagi & Andy Panda - Minor (Mood Video)", SongTitleData(authors=["Miyagi", "Andy Panda"], feats=[], song_name="Minor")),
    ("Miyagi & Эндшпиль - Fire Man (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Fire Man")),
    ("Miyagi & Эндшпиль feat. Oiseau & Papillon - Banger (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=["Oiseau", "Papillon"], song_name="Banger")),
    ("Miyagi & Andy Panda - Патрон (Official Audio)", SongTitleData(authors=["Miyagi", "Andy Panda"], feats=[], song_name="Патрон")),
    ("Miyagi & Эндшпиль - Last of Us (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Last of Us")),
    ("Miyagi & Эндшпиль - Narrative (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Narrative")),
    ("Miyagi feat. TumaniYO, KADI - Bismarck (Official Audio)", SongTitleData(authors=["Miyagi"], feats=["TumaniYO", "KADI"], song_name="Bismarck")),
    ("Miyagi & Andy Panda - Tantra (Official Audio)", SongTitleData(authors=["Miyagi", "Andy Panda"], feats=[], song_name="Tantra")),
    ("TumaniYO feat. HLOY - Rainy Day (Official Audio)", SongTitleData(authors=["TumaniYO"], feats=["HLOY"], song_name="Rainy Day")),
    ("KADI feat. Miyagi - Prayers (Official Audio)", SongTitleData(authors=["KADI"], feats=["Miyagi"], song_name="Prayers")),
    ("Miyagi feat. KADI - Родная Пой (Official Audio)", SongTitleData(authors=["Miyagi"], feats=["KADI"], song_name="Родная Пой")),
    # TODO: here we return without (seniorita), 
    # idk make a set of known expressions in brackets and warn on unknown ones
    # idk how to tell the script this is valid title this is not...
    ("GIMS, Maluma - Hola Señorita (Maria) [Official Video]", SongTitleData(authors=["GIMS", "Maluma"], feats=[], song_name="Hola Señorita")),
    ("Konfuz — Ратата (Mood video)", SongTitleData(authors=["Konfuz"], feats=[], song_name="Ратата")),
    ("Сергей Лазарев - Это все она (Official video)", SongTitleData(authors=["Сергей Лазарев"], feats=[], song_name="Это все она")),
    ("Дима Билан - Держи", SongTitleData(authors=["Дима Билан"], feats=[], song_name="Держи")),
    ("Miyagi & Эндшпиль & N.E.R.A.K. - Именно та (Audio)🎧 /Andy Panda", SongTitleData(authors=["Miyagi", "Эндшпиль", "N.E.R.A.K."], feats=[], song_name="Именно та")),
    ("Сати Казанова feat. Arsenium - До рассвета", SongTitleData(authors=["Сати Казанова"], feats=["Arsenium"], song_name="До рассвета")),
    # same thing here, without ' (Лада Седан)'
    ("Тимати feat. Рекорд Оркестр - Баклажан (Лада Седан)", SongTitleData(authors=["Тимати"], feats=["Рекорд Оркестр"], song_name="Баклажан")),
    ("Тима Белорусских - Витаминка (Премьера официального клипа)", SongTitleData(authors=["Тима Белорусских"], feats=[], song_name="Витаминка")),
    ("Эльбрус Джанмирзоев \"Бродяга\"", SongTitleData(authors=["Эльбрус Джанмирзоев"], feats=[], song_name="Бродяга", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("INNA - Caliente (by Play & Win) | Lyrics Video", SongTitleData(authors=["INNA"], feats=[], song_name="Caliente")),
    ("Тима Белорусских - МОКРЫЕ КРОССЫ /OFFICIAL (трек)/", SongTitleData(authors=["Тима Белорусских"], feats=[], song_name="МОКРЫЕ КРОССЫ")),
    ("GIMS - Est-ce que tu m'aimes ? (Clip officiel)", SongTitleData(authors=["GIMS"], feats=[], song_name="Est-ce que tu m'aimes ?")),
    ("Тима Белорусских - Незабудка", SongTitleData(authors=["Тима Белорусских"], feats=[], song_name="Незабудка")),
    ("IOWA - Улыбайся", SongTitleData(authors=["IOWA"], feats=[], song_name="Улыбайся")),
    ("JONY - Титры", SongTitleData(authors=["JONY"], feats=[], song_name="Титры")),
    ("Dabro - Юность (премьера песни, 2020) | Звук поставим на всю", SongTitleData(authors=["Dabro"], feats=[], song_name="Юность")),
    ("Егор Крид feat. Филипп Киркоров - Цвет настроения черный (премьера трека, 2018)", SongTitleData(authors=["Егор Крид"], feats=["Филипп Киркоров"], song_name="Цвет настроения черный")),
    ("ФАБРИКА - Не родись красивой", SongTitleData(authors=["ФАБРИКА"], feats=[], song_name="Не родись красивой")),
    # same thing here (not / niusha, but only the first half) though we warn here
    ("NYUSHA / НЮША - Наедине (Official Clip) HD", SongTitleData(authors=["NYUSHA"], feats=[], song_name="Наедине", err_code=ErrCodes.REFUSED)),
    ("Stromae - Alors on danse (Official Music Video)", SongTitleData(authors=["Stromae"], feats=[], song_name="Alors on danse")),
    ("Чёрные глаза", SongTitleData(authors=[], feats=[], song_name="Чёрные глаза", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Егор Крид - Потрачу (премьера клипа, 2017)", SongTitleData(authors=["Егор Крид"], feats=[], song_name="Потрачу")),
    ("HammAli & Navai - Птичка (Премьера клипа)", SongTitleData(authors=["HammAli", "Navai"], feats=[], song_name="Птичка")),
    ("Indila - Love Story (Official Music Video)", SongTitleData(authors=["Indila"], feats=[], song_name="Love Story")),
    ("Jennifer Lopez, Pitbull - On The Floor (Official Music Video)", SongTitleData(authors=["Jennifer Lopez", "Pitbull"], feats=[], song_name="On The Floor")),
    ("INNA - Amazing (Official Video)", SongTitleData(authors=["INNA"], feats=[], song_name="Amazing")),
    ("Jah Khalib - Лейла", SongTitleData(authors=["Jah Khalib"], feats=[], song_name="Лейла")),
    ("50 Cent - In Da Club (Official Music Video)", SongTitleData(authors=["50 Cent"], feats=[], song_name="In Da Club")),
    ("Shakira - Chantaje (Official Video) ft. Maluma", SongTitleData(authors=["Shakira"], feats=["Maluma"], song_name="Chantaje")),
    ("Элджей & Кравц - Дисконнект", SongTitleData(authors=["Элджей", "Кравц"], feats=[], song_name="Дисконнект")),
    ("Sean Paul - No Lie ft. Dua Lipa", SongTitleData(authors=["Sean Paul"], feats=["Dua Lipa"], song_name="No Lie")),
    ("J Balvin, Willy William - Mi Gente (Official Video)", SongTitleData(authors=["J Balvin", "Willy William"], feats=[], song_name="Mi Gente")),
    ("DJ Snake - Taki Taki ft. Selena Gomez, Ozuna, Cardi B (Official Music Video)", SongTitleData(authors=["DJ Snake"], feats=["Selena Gomez", "Ozuna", "Cardi B"], song_name="Taki Taki")),
    ("Miyagi & Эндшпиль feat. KADI - In Love (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=["KADI"], song_name="In Love")),
    ("Alan Walker - Faded", SongTitleData(authors=["Alan Walker"], feats=[], song_name="Faded")),
    ("Miyagi - Angel (Official Audio)", SongTitleData(authors=["Miyagi"], feats=[], song_name="Angel")),
    ("Major Lazer & DJ Snake - Lean On (feat. MØ) [Official 4K Music Video]", SongTitleData(authors=["Major Lazer", "DJ Snake"], feats=["MØ"], song_name="Lean On")),
    ("INNA - Caliente | Official Music Video", SongTitleData(authors=["INNA"], feats=[], song_name="Caliente")),
    ("NYUSHA / НЮША - Выше (Official clip) HD", SongTitleData(authors=["NYUSHA"], feats=[], song_name="Выше", err_code=ErrCodes.REFUSED)),
    ("In And Out Of Love (Slowed Version)", SongTitleData(authors=[], feats=[], song_name="In And Out Of Love", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("The Limba & Andro - X.O (Mood video)", SongTitleData(authors=["The Limba", "Andro"], feats=[], song_name="X.O")),
    ("Luis Fonsi - Despacito ft. Daddy Yankee", SongTitleData(authors=["Luis Fonsi"], feats=["Daddy Yankee"], song_name="Despacito")),
    ("MORGENSHTERN - ПОЙДЕТ (Веселый Клип, 2023)", SongTitleData(authors=["MORGENSHTERN"], feats=[], song_name="ПОЙДЕТ")),
    ("Элджей & Rakhim - URUS (Official Video)", SongTitleData(authors=["Элджей", "Rakhim"], feats=[], song_name="URUS")),
    ("Каспийский Груз - На белом (feat. Гио Пика)", SongTitleData(authors=["Каспийский Груз"], feats=["Гио Пика"], song_name="На белом")),
    ("Miyagi & Эндшпиль - Санавабич (Music Clip)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Санавабич")),
    ("Miyagi & Эндшпиль - В последний раз (Lyric Video) | YouTube Exclusive", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="В последний раз")),
    ("104 - НЕ ЖАЛЬ (ft. Скриптонит, MiyaGi) [Official Audio]", SongTitleData(authors=["104"], feats=["Скриптонит", "MiyaGi"], song_name="НЕ ЖАЛЬ")),
    ("Наследство", SongTitleData(authors=[], feats=[], song_name="Наследство", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("THRILL PILL, Егор Крид & MORGENSHTERN - Грустная Песня", SongTitleData(authors=["THRILL PILL", "Егор Крид", "MORGENSHTERN"], feats=[], song_name="Грустная Песня")),
    ("MORGENSHTERN - DINERO (Official Video, 2021)", SongTitleData(authors=["MORGENSHTERN"], feats=[], song_name="DINERO")),
    ("Miyagi & Andy Panda - Там Ревели Горы (Mood Video)", SongTitleData(authors=["Miyagi", "Andy Panda"], feats=[], song_name="Там Ревели Горы")),
    ("Miyagi & Эндшпиль - OneLove (Lyric video)/ Andy Panda", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="OneLove")),
    ("Miyagi - Настырный (Lyric video)", SongTitleData(authors=["Miyagi"], feats=[], song_name="Настырный")),
    ("MORGENSHTERN, Aarne - DALEKO (Official Video, 2022)", SongTitleData(authors=["MORGENSHTERN", "Aarne"], feats=[], song_name="DALEKO")),
    ("Miyagi & Эндшпиль - Фая (Lyric video)/Andy Panda", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Фая")),
    ("IVOXYGEN - LOVE (prod. MORECALCIUM)", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="LOVE")),
    ("SAY3AM, GERXMVP - Amnesia (Official Audio)", SongTitleData(authors=["SAY3AM", "GERXMVP"], feats=[], song_name="Amnesia")),
    ("zodivk \"Devil Eyes\"", SongTitleData(authors=["zodivk"], feats=[], song_name="Devil Eyes", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Lithe - Like We Wrote (MYSTIK Remix) [Wave/Phonk]", SongTitleData(authors=["Lithe"], feats=[], song_name="Like We Wrote")),
    ("JONY - Френдзона", SongTitleData(authors=["JONY"], feats=[], song_name="Френдзона")),
    ("MXRGX - MY WAY", SongTitleData(authors=["MXRGX"], feats=[], song_name="MY WAY")),
    ("Леша Свик - Малиновый свет (Премьера 2018)", SongTitleData(authors=["Леша Свик"], feats=[], song_name="Малиновый свет")),
    ("Miyagi & Andy Panda feat. TumaniYO - Brooklyn (Official Video)", SongTitleData(authors=["Miyagi", "Andy Panda"], feats=["TumaniYO"], song_name="Brooklyn")),
    ("Miyagi & Эндшпиль - Фея (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Фея")),
    ("IVOXYGEN - casino143", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="casino143")),
    ("Miyagi & Эндшпиль feat. Рем Дигга - Untouchable (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=["Рем Дигга"], song_name="Untouchable")),
    ("Carla's Dreams - Imperfect | Official Video", SongTitleData(authors=["Carla's Dreams"], feats=[], song_name="Imperfect")),
    ("n u a g e s - closer", SongTitleData(authors=["n u a g e s"], feats=[], song_name="closer")),
    ("DVRST - Motion", SongTitleData(authors=["DVRST"], feats=[], song_name="Motion")),
    ("Miyagi & Эндшпиль - Наоборот (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Наоборот")),
    ("Downpour", SongTitleData(authors=[], feats=[], song_name="Downpour", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("The Quintessential Quintuplets Opening | Gotoubun no Kimochi", SongTitleData(authors=[], feats=[], song_name="The Quintessential Quintuplets Opening | Gotoubun no Kimochi", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Navai, MONA - Есенин", SongTitleData(authors=["Navai", "MONA"], feats=[], song_name="Есенин")),
    ("𝐯𝐢𝐝𝐞𝐨𝐜𝐥𝐮𝐛 𝐑𝐎𝐈 / 𝐢𝐧𝐬𝐭𝐫𝐮𝐦𝐞𝐧𝐭𝐚𝐥 / 𝐬𝐮𝐩𝐞𝐫 𝐬𝐥𝐨𝐰𝐞𝐝", SongTitleData(authors=[], feats=[], song_name="𝐯𝐢𝐝𝐞𝐨𝐜𝐥𝐮𝐛 𝐑𝐎𝐈 / 𝐢𝐧𝐬𝐭𝐫𝐮𝐦𝐞𝐧𝐭𝐚𝐥 / 𝐬𝐮𝐩𝐞𝐫 𝐬𝐥𝐨𝐰𝐞𝐝", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("HammAli & Navai - Девочка - война", SongTitleData(authors=["HammAli", "Navai"], feats=[], song_name="Девочка - война", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("5admin - Silence", SongTitleData(authors=["5admin"], feats=[], song_name="Silence")),
    ("Miyagi - Корабли (Official Audio)", SongTitleData(authors=["Miyagi"], feats=[], song_name="Корабли")),
    ("JONY, HammAli - Наверно ты меня не помнишь", SongTitleData(authors=["JONY", "HammAli"], feats=[], song_name="Наверно ты меня не помнишь")),
    ("Miyagi feat. даена, HLOY - DAO (Official Audio)", SongTitleData(authors=["Miyagi"], feats=["даена", "HLOY"], song_name="DAO")),
    ("Magnat & Feoctist - Elegantă [Videoclip Oficial 2023]", SongTitleData(authors=["Magnat", "Feoctist"], feats=[], song_name="Elegantă")),
    ("Magnat & Feoctist - Ce-am făcut cu viața mea! [Videoclip Oficial 2023]", SongTitleData(authors=["Magnat", "Feoctist"], feats=[], song_name="Ce-am făcut cu viața mea!")),
    ("TXDO - SOMETHING FOR YOU (Wave)", SongTitleData(authors=["TXDO"], feats=[], song_name="SOMETHING FOR YOU")),
    ("Miyagi & Эндшпиль feat. Рем Дигга - I Got Love (Official Video)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=["Рем Дигга"], song_name="I Got Love")),
    ("MC ORSEN - WARNING", SongTitleData(authors=["MC ORSEN"], feats=[], song_name="WARNING")),
    ("DVRST, OBLXKQ - ENDLESS LOVE", SongTitleData(authors=["DVRST", "OBLXKQ"], feats=[], song_name="ENDLESS LOVE")),
    ("MXRGX, NERONUS - GET AWAY II", SongTitleData(authors=["MXRGX", "NERONUS"], feats=[], song_name="GET AWAY II")),
    ("IVOXYGEN - Falling (Pamex Remix/Music Video)", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="Falling")),
    ("pathetic - dancing nihilist (slowed)", SongTitleData(authors=["pathetic"], feats=[], song_name="dancing nihilist")),
    ("MACAN - Кино (Официальная премьера трека)", SongTitleData(authors=["MACAN"], feats=[], song_name="Кино")),
    ("Miyagi feat. Andy Panda - Говори мне (Official Audio)", SongTitleData(authors=["Miyagi"], feats=["Andy Panda"], song_name="Говори мне")),
    ("IVOXYGEN - eraserhead", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="eraserhead")),
    ("Carla's Dreams - Acele | Official Video", SongTitleData(authors=["Carla's Dreams"], feats=[], song_name="Acele")),
    ("Magnat - Bespredel [Official Video]", SongTitleData(authors=["Magnat"], feats=[], song_name="Bespredel")),
    ("LXST CXNTURY - DEEP FUSION", SongTitleData(authors=["LXST CXNTURY"], feats=[], song_name="DEEP FUSION")),
    ("IVOXYGEN - Purple Sky [Prod. Kubsy Beats]", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="Purple Sky")),
    ("Miyagi & Andy Panda - Не Жалея (Official Audio)", SongTitleData(authors=["Miyagi", "Andy Panda"], feats=[], song_name="Не Жалея")),
    ("Izzamuzzic - Shootout", SongTitleData(authors=["Izzamuzzic"], feats=[], song_name="Shootout")),
    ("Rauf Faik - детство (Official audio)", SongTitleData(authors=["Rauf Faik"], feats=[], song_name="детство")),
    ("Dabro - На часах ноль-ноль (Official video)", SongTitleData(authors=["Dabro"], feats=[], song_name="На часах ноль-ноль")),
    ("Kapushon feat. Victoria Beregoi - Rap ca pe manele | Official Music Video", SongTitleData(authors=["Kapushon"], feats=["Victoria Beregoi"], song_name="Rap ca pe manele")),
    ("Carla’s Dreams – Ne Topim | Nocturn: Act 7", SongTitleData(authors=["Carla’s Dreams"], feats=[], song_name="Ne Topim")),
    ("Miyagi & Эндшпиль - Пронзай (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Пронзай")),
    ("Бабек Мамедрзаев - Принцесса (ПРЕМЬЕРА ХИТА 2019)", SongTitleData(authors=["Бабек Мамедрзаев"], feats=[], song_name="Принцесса")),
    ("niteboi - u.", SongTitleData(authors=["niteboi"], feats=[], song_name="u.")),
    ("Carla's Dreams - Unde | Official Video", SongTitleData(authors=["Carla's Dreams"], feats=[], song_name="Unde")),
    ("IVOXYGEN - SING (Prod. Caps.Ctrl) (Lyrics Video)", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="SING")),
    ("ННД", SongTitleData(authors=[], feats=[], song_name="ННД", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Miyagi & Andy Panda - Utopia (Official Audio)", SongTitleData(authors=["Miyagi", "Andy Panda"], feats=[], song_name="Utopia")),
    ("Скриптонит - Москва любит... [Official Audio]", SongTitleData(authors=["Скриптонит"], feats=[], song_name="Москва любит...")),
    ("HammAli & Navai - Прятки ( 2019 )", SongTitleData(authors=["HammAli", "Navai"], feats=[], song_name="Прятки")),
    ("это снова я", SongTitleData(authors=[], feats=[], song_name="это снова я", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("オンリー", SongTitleData(authors=[], feats=[], song_name="オンリー", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("DVRST - Dream Space", SongTitleData(authors=["DVRST"], feats=[], song_name="Dream Space")),
    ("SPACYBOI - Last Memory (2023)", SongTitleData(authors=["SPACYBOI"], feats=[], song_name="Last Memory")),
    ("Carla's Dreams - Te Rog | Official Video", SongTitleData(authors=["Carla's Dreams"], feats=[], song_name="Te Rog")),
    ("Carla's Dreams - Pana La Sange | Official Video", SongTitleData(authors=["Carla's Dreams"], feats=[], song_name="Pana La Sange")),
    ("Classroom of the Elite Season 3 - Ending | The Great Revolution of this World", SongTitleData(authors=[], feats=[], song_name="Classroom of the Elite Season 3 - Ending | The Great Revolution of this World", err_code=ErrCodes.AUTHOR_NAME_TOO_LONG_WARNING)),
    ("IVOXYGEN - the girl next door", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="the girl next door")),
    ("Xcho - Ты и Я (Official Audio)", SongTitleData(authors=["Xcho"], feats=[], song_name="Ты и Я")),
    ("RSAC x ELLA — NBA (Не мешай) (OFFICIAL VIDEO)", SongTitleData(authors=["RSAC", "ELLA"], feats=[], song_name="NBA")),
    ("Элджей & Feduk - Розовое вино", SongTitleData(authors=["Элджей", "Feduk"], feats=[], song_name="Розовое вино")),
    ("HammAli & Navai - Как тебя забыть ( 2019 )", SongTitleData(authors=["HammAli", "Navai"], feats=[], song_name="Как тебя забыть")),
    ("8. Jah Khalib - Колыбельная | E.G.O. | ПРЕМЬЕРА АЛЬБОМА", SongTitleData(authors=["Jah Khalib"], feats=[], song_name="Колыбельная", err_code=ErrCodes.AUTHOR_NAME_COULD_BE_WRONG_WARNING)),
    ("Carla's Dreams - Lacrimi si Pumni in Pereti | Official Video", SongTitleData(authors=["Carla's Dreams"], feats=[], song_name="Lacrimi si Pumni in Pereti")),
    ("Øneheart - next to you", SongTitleData(authors=["Øneheart"], feats=[], song_name="next to you")),
    ("祈りの唄", SongTitleData(authors=[], feats=[], song_name="祈りの唄", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("IVOXYGEN - plateau", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="plateau")),
    ("Люся Чеботина - Солнце Монако (ПРЕМЬЕРА КЛИПА)", SongTitleData(authors=["Люся Чеботина"], feats=[], song_name="Солнце Монако")),
    ("MiyaGi & Эндшпиль, Amigo - Самая", SongTitleData(authors=["MiyaGi", "Эндшпиль", "Amigo"], feats=[], song_name="Самая")),
    ("Fyripu - Nocturnus ナイト [Atmospheric Space Phonk]", SongTitleData(authors=["Fyripu"], feats=[], song_name="Nocturnus ナイト")),
    ("CYREX - AFTERLIFE", SongTitleData(authors=["CYREX"], feats=[], song_name="AFTERLIFE")),
    ("Баста, HammAli & Navai - Где ты теперь и с кем", SongTitleData(authors=["Баста", "HammAli", "Navai"], feats=[], song_name="Где ты теперь и с кем")),
    ("IVOXYGEN - TEEN (Official Music Video)", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="TEEN")),
    ("New Jeans Jersey Remix (Audio Edited) (Miside Mita Edit TikTok Version) [made by purple drip boy]", SongTitleData(authors=[], feats=[], song_name="New Jeans Jersey Remix", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("The Motans feat. Irina Rimes - POEM | Official Video", SongTitleData(authors=["The Motans"], feats=["Irina Rimes"], song_name="POEM")),
    ("Magnat & Feoctist - Dă-mă mamă după Iura [Videoclip Oficial 2024]", SongTitleData(authors=["Magnat", "Feoctist"], feats=[], song_name="Dă-mă mamă după Iura")),
    ("旅人の唄", SongTitleData(authors=[], feats=[], song_name="旅人の唄", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("INTERWORLD \"METAMORPHOSIS 2\"", SongTitleData(authors=["INTERWORLD"], feats=[], song_name="METAMORPHOSIS 2", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("IVOXYGEN - YOUNG KID (Official Music Video)", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="YOUNG KID")),
    ("IVOXYGEN - write my name in your heart", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="write my name in your heart")),
    ("Xcho - Зачарованная (Official Audio)", SongTitleData(authors=["Xcho"], feats=[], song_name="Зачарованная")),
    ("IVOXYGEN - URBAN MELODY", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="URBAN MELODY")),
    ("IVOXYGEN - kid is afraid to be alone", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="kid is afraid to be alone")),
    ("風と行く道", SongTitleData(authors=[], feats=[], song_name="風と行く道", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("IVOXYGEN - keep on dancing in the dark", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="keep on dancing in the dark")),
    ("villiam lane - particles (slowed)", SongTitleData(authors=["villiam lane"], feats=[], song_name="particles")),
    ("IVOXYGEN - 2055", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="2055")),
    ("Alan Walker - Broken Strings (Official Music Video)", SongTitleData(authors=["Alan Walker"], feats=[], song_name="Broken Strings")),
    ("Magnat & Feoctist - Cumaniok [Videoclip Oficial 2024]", SongTitleData(authors=["Magnat", "Feoctist"], feats=[], song_name="Cumaniok")),
    ("PLAYBOI CARTI - WOK (Prod.LHBeats)", SongTitleData(authors=["PLAYBOI CARTI"], feats=[], song_name="WOK")),
    ("KoruSe, mzmff - Two Different Worlds (Slowed & Reverb)", SongTitleData(authors=["KoruSe", "mzmff"], feats=[], song_name="Two Different Worlds")),
    ("Каспийский Груз - Табор вернулся в город", SongTitleData(authors=["Каспийский Груз"], feats=[], song_name="Табор вернулся в город")),
    ("Desolate", SongTitleData(authors=[], feats=[], song_name="Desolate", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("jessie (Slowed)", SongTitleData(authors=[], feats=[], song_name="jessie", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("IVOXYGEN - LAUREN", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="LAUREN")),
    ("Dabro - Юность (Official video)", SongTitleData(authors=["Dabro"], feats=[], song_name="Юность")),
    ("IVOXYGEN - cut my mind like a cable", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="cut my mind like a cable")),
    ("DJ UNIVXRSEL - voices in my head", SongTitleData(authors=["DJ UNIVXRSEL"], feats=[], song_name="voices in my head")),
    ("IVOXYGEN - CRASHOUT", SongTitleData(authors=["IVOXYGEN"], feats=[], song_name="CRASHOUT")),
    ("Miyagi - Самурай (Official Audio)", SongTitleData(authors=["Miyagi"], feats=[], song_name="Самурай")),
    ("Afterglow", SongTitleData(authors=[], feats=[], song_name="Afterglow", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Alan Walker - Alone", SongTitleData(authors=["Alan Walker"], feats=[], song_name="Alone")),
    ("Lost Soul", SongTitleData(authors=[], feats=[], song_name="Lost Soul", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("104 - НЕ ЖАЛЬ (ft. Скриптонит, MiyaGi) [Official Audio] MOLODOI BOSS", SongTitleData(authors=["104"], feats=["Скриптонит", "MiyaGi"], song_name="НЕ ЖАЛЬ")),
    ("Alan Walker - Darkside (feat. Au/Ra and Tomine Harket)", SongTitleData(authors=["Alan Walker"], feats=["Au/Ra", "Tomine Harket"], song_name="Darkside", err_code=ErrCodes.REFUSED)),
    ("Miyagi & Эндшпиль - Бэйба судьба (Lyric video)/ Andy Panda", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Бэйба судьба")),
    ("Navjaxx - Overload Memories (4K Official Music Video)", SongTitleData(authors=["Navjaxx"], feats=[], song_name="Overload Memories")),
    ("Miyagi & Andy Panda - Kosandra (Official Audio)", SongTitleData(authors=["Miyagi", "Andy Panda"], feats=[], song_name="Kosandra")),
    ("Crystal Castles \"KEROSENE\" Official Castles official", SongTitleData(authors=["Crystal Castles"], feats=[], song_name="KEROSENE", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Miyagi & Эндшпиль - Дизлайк (Lyric Video) | YouTube Exclusive /Andy Panda", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Дизлайк")),
    ("INTERWORLD - RAPTURE (PHONK) Vibe Guide", SongTitleData(authors=["INTERWORLD"], feats=[], song_name="RAPTURE")),
    ("DVRST - YOUR NAME", SongTitleData(authors=["DVRST"], feats=[], song_name="YOUR NAME")),
    ("Miyagi & Эндшпиль feat Brick Bazuka - Бошка (Lyric video)/Andy Panda", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=["Brick Bazuka"], song_name="Бошка")),
    ("LOWX - SEA OF FEELINGS", SongTitleData(authors=["LOWX"], feats=[], song_name="SEA OF FEELINGS")),
    ("Ollane feat. Miyagi & Andy Panda - Where Are You (Official Audio)", SongTitleData(authors=["Ollane"], feats=["Miyagi", "Andy Panda"], song_name="Where Are You")),
    ("Miyagi & Эндшпиль - Временно (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Временно")),
    ("JONY - Love your voice", SongTitleData(authors=["JONY"], feats=[], song_name="Love your voice")),
    ("Carla's Dreams - Simplu si Usor | Official Video", SongTitleData(authors=["Carla's Dreams"], feats=[], song_name="Simplu si Usor")),
    ("Miyagi & Эндшпиль - Listen to Your Heart (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Listen to Your Heart")),
    ("Carla's Dreams x EMAA - N-aud | Official Video", SongTitleData(authors=["Carla's Dreams", "EMAA"], feats=[], song_name="N-aud")),
    ("Тима Белорусских - Окей (трек)", SongTitleData(authors=["Тима Белорусских"], feats=[], song_name="Окей")),
    ("Carla’s Dreams - Luna | Nocturn: Act 4", SongTitleData(authors=["Carla’s Dreams"], feats=[], song_name="Luna")),
    ("JONY - Комета", SongTitleData(authors=["JONY"], feats=[], song_name="Комета")),
    ("Carla's Dreams - Seara de Seara | Official Video", SongTitleData(authors=["Carla's Dreams"], feats=[], song_name="Seara de Seara")),
    ("Каспийский Груз - Табор уходит в небо", SongTitleData(authors=["Каспийский Груз"], feats=[], song_name="Табор уходит в небо")),
    ("Rauf Faik - вечера (Official video)", SongTitleData(authors=["Rauf Faik"], feats=[], song_name="вечера")),
    ("acies", SongTitleData(authors=[], feats=[], song_name="acies", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("juno, blindheart - Solitude - Slowed", SongTitleData(authors=["juno", "blindheart"], feats=[], song_name="Solitude", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("INSONAMIA Slowed + Reverb", SongTitleData(authors=[], feats=[], song_name="INSONAMIA", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("9. Jah Khalib - Медина | E.G.O. | ПРЕМЬЕРА АЛЬБОМА", SongTitleData(authors=["Jah Khalib"], feats=[], song_name="Медина", err_code=ErrCodes.AUTHOR_NAME_COULD_BE_WRONG_WARNING)),
    ("Andy Panda feat. Miyagi - Endorphin (Official Audio)", SongTitleData(authors=["Andy Panda"], feats=["Miyagi"], song_name="Endorphin")),
    ("Carla's Dreams - Scara 2, etajul 7 | Official Video", SongTitleData(authors=["Carla's Dreams"], feats=[], song_name="Scara 2, etajul 7")),
    ("TumaniYO feat. Miyagi & Эндшпиль - Dance Up (Official Audio)", SongTitleData(authors=["TumaniYO"], feats=["Miyagi", "Эндшпиль"], song_name="Dance Up")),
    ("HENSY - Поболело и прошло (Официальная премьера трека)", SongTitleData(authors=["HENSY"], feats=[], song_name="Поболело и прошло")),
    ("Magnat & Feoctist - Londra [ Videoclip Oficial 2020 ]", SongTitleData(authors=["Magnat", "Feoctist"], feats=[], song_name="Londra")),
    ("starly (Slowed)", SongTitleData(authors=[], feats=[], song_name="starly", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("my!lane - This Feeling", SongTitleData(authors=["my!lane"], feats=[], song_name="This Feeling")),
    ("NBSPLV - The Lost Soul Down", SongTitleData(authors=["NBSPLV"], feats=[], song_name="The Lost Soul Down")),
    ("DVRST - Close Eyes (Slowed + Reverb)", SongTitleData(authors=["DVRST"], feats=[], song_name="Close Eyes")),
    ("JONY, HammAli & Navai - Без тебя я не я", SongTitleData(authors=["JONY", "HammAli", "Navai"], feats=[], song_name="Без тебя я не я")),
    ("SABI, MIA BOYKA - Базовый минимум (Lyric video)", SongTitleData(authors=["SABI", "MIA BOYKA"], feats=[], song_name="Базовый минимум")),
    ("Miyagi & Эндшпиль - Двигайся (Music Clip)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Двигайся")),
    ("Miyagi & Andy Panda - All The Time (Official Audio)", SongTitleData(authors=["Miyagi", "Andy Panda"], feats=[], song_name="All The Time")),
    ("Zivert - Life | Премьера клипа", SongTitleData(authors=["Zivert"], feats=[], song_name="Life")),
    ("Hensonn-Flare", SongTitleData(authors=[], feats=[], song_name="Hensonn-Flare", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Miyagi & Andy Panda - Там ревели горы (2020)", SongTitleData(authors=["Miyagi", "Andy Panda"], feats=[], song_name="Там ревели горы")),
    ("Miyagi & Andy Panda - YAMAKASI (Official Video)", SongTitleData(authors=["Miyagi", "Andy Panda"], feats=[], song_name="YAMAKASI")),
    ("CYGO - Panda E", SongTitleData(authors=["CYGO"], feats=[], song_name="Panda E")),
    ("HammAli & Navai, Jah Khalib – Боже, как завидую", SongTitleData(authors=["HammAli", "Navai", "Jah Khalib"], feats=[], song_name="Боже, как завидую")),
    ("Wilee - Night Drive", SongTitleData(authors=["Wilee"], feats=[], song_name="Night Drive")),
    ("MiyaGi - Бонни [Official Music Video] HD", SongTitleData(authors=["MiyaGi"], feats=[], song_name="Бонни")),
    ("Miyagi - Топи До Талого Братан", SongTitleData(authors=["Miyagi"], feats=[], song_name="Топи До Талого Братан")),
    ("archangel (Slowed)", SongTitleData(authors=[], feats=[], song_name="archangel", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Hatsukoi FULL LYRICS (KAN|ROM|ENG) - Gotoubun no Hanayome ED3 ( Season 2 Ending )", SongTitleData(authors=[], feats=[], song_name="Hatsukoi FULL LYRICS (KAN|ROM|ENG) - Gotoubun no Hanayome ED3 ( Season 2 Ending )", err_code=ErrCodes.AUTHOR_NAME_TOO_LONG_WARNING)),
    ("BABYDOLL (slowed) - DAVID LAID", SongTitleData(authors=["DAVID LAID"], feats=[], song_name="BABYDOLL", err_code=ErrCodes.AUTHOR_NAME_COULD_BE_WRONG_WARNING)),
    ("Magnat & Feoctist - Unde te duci? [Videoclip Oficial 2020]", SongTitleData(authors=["Magnat", "Feoctist"], feats=[], song_name="Unde te duci?")),
    ("Irokz - FUNK UNIVERSO", SongTitleData(authors=["Irokz"], feats=[], song_name="FUNK UNIVERSO")),
    ("King Von - Wayne's Story (Official Video)", SongTitleData(authors=["King Von"], feats=[], song_name="Wayne's Story")),
    ("Xcho & Пабло & ALEMOND - Only you (Official Audio)", SongTitleData(authors=["Xcho", "Пабло", "ALEMOND"], feats=[], song_name="Only you")),
    ("DHARIA - Sugar & Brownies (by Monoir) [Official Video]", SongTitleData(authors=["DHARIA"], feats=[], song_name="Sugar & Brownies")),
    ("Тает лёд", SongTitleData(authors=[], feats=[], song_name="Тает лёд", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Konfuz — Кайф ты поймала (Official Music Video)", SongTitleData(authors=["Konfuz"], feats=[], song_name="Кайф ты поймала")),
    ("PLAYAMANE x Nateki - MIDNIGHT", SongTitleData(authors=["PLAYAMANE", "Nateki"], feats=[], song_name="MIDNIGHT")),
    ("【ゼンゼロ】モエチャッカファイア / エレン・ジョー（CV：若山詩音）cover", SongTitleData(authors=[], feats=[], song_name="【ゼンゼロ】モエチャッカファイア / エレン・ジョー（CV：若山詩音）cover", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("EMIN feat. JONY - КАМИН", SongTitleData(authors=["EMIN"], feats=["JONY"], song_name="КАМИН")),
    ("Miyagi & Andy Panda - Мало Нам (Mood Video)", SongTitleData(authors=["Miyagi", "Andy Panda"], feats=[], song_name="Мало Нам")),
    ("Andy Panda - Orange Sunset (Official Audio)", SongTitleData(authors=["Andy Panda"], feats=[], song_name="Orange Sunset")),
    ("Miyagi & Эндшпиль feat. Truwer - No Reason (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=["Truwer"], song_name="No Reason")),
    ("Roi - Videoclub (instrumental) Super Slowed [Chainsaw Man Girls]", SongTitleData(authors=["Roi"], feats=[], song_name="Videoclub")),
    ("Miyagi - Бонни (Audio)🎧", SongTitleData(authors=["Miyagi"], feats=[], song_name="Бонни")),
    ("Eternxlkz - GURU ~ (SLOWED + REVERB) [BRAZILIAN PHONK]", SongTitleData(authors=["Eternxlkz"], feats=[], song_name="GURU")),
    ("MiyaGi - Колибри (Music Clip)", SongTitleData(authors=["MiyaGi"], feats=[], song_name="Колибри")),
    ("JONY - Лали", SongTitleData(authors=["JONY"], feats=[], song_name="Лали")),
    ("MACAN - Май", SongTitleData(authors=["MACAN"], feats=[], song_name="Май")),
    ("Miyagi - По уши в тебя влюблён (Lyric video)", SongTitleData(authors=["Miyagi"], feats=[], song_name="По уши в тебя влюблён")),
    ("Jah Khalib – Доча | ПРЕМЬЕРА ТРЕКА", SongTitleData(authors=["Jah Khalib"], feats=[], song_name="Доча")),
    ("Jah Khalib – Искал-Нашёл | Премьера клипа", SongTitleData(authors=["Jah Khalib"], feats=[], song_name="Искал-Нашёл")),
    ("Coolio - Gangsta's Paradise (feat. L.V.) [Official Music Video]", SongTitleData(authors=["Coolio"], feats=["L.V."], song_name="Gangsta's Paradise")),
    ("Miyagi feat. HLOY - My Block (Official Audio)", SongTitleData(authors=["Miyagi"], feats=["HLOY"], song_name="My Block")),
    ("Night Lovell - Polozhenie", SongTitleData(authors=["Night Lovell"], feats=[], song_name="Polozhenie")),
    ("Jah Khalib – Лиловая | Премьера трека", SongTitleData(authors=["Jah Khalib"], feats=[], song_name="Лиловая")),
    ("Miyagi & Эндшпиль - Pronzai", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Pronzai")),
    ("STRUCT (Slowed)", SongTitleData(authors=[], feats=[], song_name="STRUCT", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("1. Jah Khalib - Воу-Воу Палехчэ | E.G.O. | ПРЕМЬЕРА АЛЬБОМА", SongTitleData(authors=["Jah Khalib"], feats=[], song_name="Воу-Воу Палехчэ", err_code=ErrCodes.AUTHOR_NAME_COULD_BE_WRONG_WARNING)),
    ("эндшпиль - малиновый рассвет (ｓｌｏｗｅｄ)", SongTitleData(authors=["эндшпиль"], feats=[], song_name="малиновый рассвет")),
    ("give me everything. (instrumental - slowed)", SongTitleData(authors=[], feats=[], song_name="give me everything.", err_code=ErrCodes.AUTHOR_NAME_TOO_LONG_WARNING)),
    ("CYREX x Ax3S - OVERDRIVE (OFFICIAL VIDEO)", SongTitleData(authors=["CYREX", "Ax3S"], feats=[], song_name="OVERDRIVE")),
    ("Jah Khalib feat. Айжан Байсакова – На параллельных путях", SongTitleData(authors=["Jah Khalib"], feats=["Айжан Байсакова"], song_name="На параллельных путях")),
    ("2pac-Still Ballin (How We Do Remix)", SongTitleData(authors=["2pac"], feats=[], song_name="Still Ballin", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Goth (Slowed + Reverb)", SongTitleData(authors=[], feats=[], song_name="Goth", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("King Von - Armed & Dangerous (Official Video)", SongTitleData(authors=["King Von"], feats=[], song_name="Armed & Dangerous")),
    ("ELMAN, MONA — Черная любовь (Премьера клипа)", SongTitleData(authors=["ELMAN", "MONA"], feats=[], song_name="Черная любовь")),
    ("Miyagi & Эндшпиль feat. Скриптонит - Quartz (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=["Скриптонит"], song_name="Quartz")),
    ("ARTIFICIAL INTELLIGENCE (BEST PART - SLOWED)", SongTitleData(authors=[], feats=[], song_name="ARTIFICIAL INTELLIGENCE", err_code=ErrCodes.AUTHOR_NAME_TOO_LONG_WARNING)),
    ("Miyagi - БадаБум (Lyric Video) | YouTube Exclusive", SongTitleData(authors=["Miyagi"], feats=[], song_name="БадаБум")),
    ("𝗠𝗔𝗥𝗘𝗨𝗫 – 𝗞𝗜𝗟𝗟𝗘𝗥 (𝗦𝗟𝗢𝗪𝗘𝗗)", SongTitleData(authors=["𝗠𝗔𝗥𝗘𝗨𝗫"], feats=[], song_name="𝗞𝗜𝗟𝗟𝗘𝗥")),
    ("JONY - Мир сошёл с ума", SongTitleData(authors=["JONY"], feats=[], song_name="Мир сошёл с ума")),
    ("The Limba - СМУЗИ (Official Lyric Video)", SongTitleData(authors=["The Limba"], feats=[], song_name="СМУЗИ")),
    ("HammAli & Navai - Птичка", SongTitleData(authors=["HammAli", "Navai"], feats=[], song_name="Птичка")),
    ("HammAli & Navai - А если это любовь?", SongTitleData(authors=["HammAli", "Navai"], feats=[], song_name="А если это любовь?")),
    ("Miyagi & Эндшпиль - Ночь (Official Audio)", SongTitleData(authors=["Miyagi", "Эндшпиль"], feats=[], song_name="Ночь")),
    ("JONY, Andro - Мадам", SongTitleData(authors=["JONY", "Andro"], feats=[], song_name="Мадам")),
    ("Jah Khalib - Медина (текст)", SongTitleData(authors=["Jah Khalib"], feats=[], song_name="Медина")),
    ("HammAli & Navai - У окна", SongTitleData(authors=["HammAli", "Navai"], feats=[], song_name="У окна")),
    ("Wiz Khalifa - See You Again ft. Charlie Puth [Official Video] Furious 7 Soundtrack", SongTitleData(authors=["Wiz Khalifa"], feats=["Charlie Puth"], song_name="See You Again")),
    ("Ed Sheeran - Shape of You (Official Music Video)", SongTitleData(authors=["Ed Sheeran"], feats=[], song_name="Shape of You")),
    ("Crazy Frog - Axel F (Official Video)", SongTitleData(authors=["Crazy Frog"], feats=[], song_name="Axel F")),
    ("PSY - GANGNAM STYLE(강남스타일) M/V", SongTitleData(authors=["PSY"], feats=[], song_name="GANGNAM STYLE")),
    ("Mark Ronson - Uptown Funk (Official Video) ft. Bruno Mars", SongTitleData(authors=["Mark Ronson"], feats=["Bruno Mars"], song_name="Uptown Funk")),
    ("श्री हनुमान चालीसा 🌺🙏| Shree Hanuman Chalisa Original Video |🙏🌺| GULSHAN KUMAR | HARIHARAN | 8K", SongTitleData(authors=["GULSHAN KUMAR", "HARIHARAN"], feats=[], song_name="Shree Hanuman Chalisa", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Dancing Green Alien - Dame Tu Cosita feat. Cutty Ranks (Official Video)\"", SongTitleData(authors=["Dancing Green Alien"], feats=["Cutty Ranks"], song_name="Dame Tu Cosita")),
    ("Shakira - Waka Waka (This Time for Africa) (The Official 2010 FIFA World Cup™ Song)", SongTitleData(authors=["Shakira"], feats=[], song_name="Waka Waka")),
    ("OneRepublic - Counting Stars", SongTitleData(authors=["OneRepublic"], feats=[], song_name="Counting Stars")),
    ("Maroon 5 - Sugar (Official Music Video)", SongTitleData(authors=["Maroon 5"], feats=[], song_name="Sugar")),
    ("Katy Perry - Roar", SongTitleData(authors=["Katy Perry"], feats=[], song_name="Roar")),
    ("Katy Perry - Dark Horse ft. Juicy J", SongTitleData(authors=["Katy Perry"], feats=["Juicy J"], song_name="Dark Horse")),
    ("Ed Sheeran - Perfect (Official Music Video)", SongTitleData(authors=["Ed Sheeran"], feats=[], song_name="Perfect")),
    ("Justin Bieber - Sorry (PURPOSE : The Movement)", SongTitleData(authors=["Justin Bieber"], feats=[], song_name="Sorry")),
    ("Passenger | Let Her Go (Official Video)", SongTitleData(authors=["Passenger"], feats=[], song_name="Let Her Go", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Maroon 5 - Girls Like You ft. Cardi B (Official Music Video)", SongTitleData(authors=["Maroon 5"], feats=["Cardi B"], song_name="Girls Like You")),
    ("Ed Sheeran - Thinking Out Loud (Official Music Video)", SongTitleData(authors=["Ed Sheeran"], feats=[], song_name="Thinking Out Loud")),
    ("Gente De Zona\"", SongTitleData(authors=[], feats=[], song_name="Gente De Zona", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Taylor Swift - Blank Space", SongTitleData(authors=["Taylor Swift"], feats=[], song_name="Blank Space")),
    ("Justin Bieber - Baby ft. Ludacris", SongTitleData(authors=["Justin Bieber"], feats=["Ludacris"], song_name="Baby")),
    ("Idina Menzel - Let It Go (From Frozen/Sing-Along)", SongTitleData(authors=["Idina Menzel"], feats=[], song_name="Let It Go")),
    ("Taylor Swift - Shake It Off", SongTitleData(authors=["Taylor Swift"], feats=[], song_name="Shake It Off")),
    ("Willy William - Mi Gente (Official Video)\"", SongTitleData(authors=["Willy William"], feats=[], song_name="Mi Gente")),
    ("Charlie Puth - We Don't Talk Anymore (feat. Selena Gomez) [Official Video]", SongTitleData(authors=["Charlie Puth"], feats=["Selena Gomez"], song_name="We Don't Talk Anymore")),
    ("The Chainsmokers - Closer (Lyric) ft. Halsey", SongTitleData(authors=["The Chainsmokers"], feats=["Halsey"], song_name="Closer")),
    ("Dua Lipa - New Rules (Official Music Video)", SongTitleData(authors=["Dua Lipa"], feats=[], song_name="New Rules")),
    ("Bruno Mars - The Lazy Song (Official Music Video)", SongTitleData(authors=["Bruno Mars"], feats=[], song_name="The Lazy Song")),
    ("Adele - Hello (Official Music Video)", SongTitleData(authors=["Adele"], feats=[], song_name="Hello")),
    ("twenty one pilots: Stressed Out [OFFICIAL VIDEO]", SongTitleData(authors=["twenty one pilots"], feats=[], song_name="Stressed Out", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Clean Bandit - Rockabye (feat. Sean Paul & Anne-Marie) [Official Video]", SongTitleData(authors=["Clean Bandit"], feats=["Sean Paul", "Anne-Marie"], song_name="Rockabye")),
    ("Daddy Yankee & Snow - Con Calma (Video Oficial)", SongTitleData(authors=["Daddy Yankee", "Snow"], feats=[], song_name="Con Calma")),
    ("Eminem - Love The Way You Lie ft. Rihanna", SongTitleData(authors=["Eminem"], feats=["Rihanna"], song_name="Love The Way You Lie")),
    ("Farruko - Calma (Remix - Official Video)\"", SongTitleData(authors=["Farruko"], feats=[], song_name="Calma", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Swae Lee - Sunflower (Spider-Man: Into the Spider-Verse)\"", SongTitleData(authors=["Swae Lee"], feats=[], song_name="Sunflower")),
    ("Fifth Harmony - Work from Home (Official Video) ft. Ty Dolla $ign", SongTitleData(authors=["Fifth Harmony"], feats=["Ty Dolla $ign"], song_name="Work from Home")),
    ("Imagine Dragons - Believer (Official Music Video)", SongTitleData(authors=["Imagine Dragons"], feats=[], song_name="Believer")),
    ("Rihanna - This Is What You Came For (Official Video)", SongTitleData(authors=["Rihanna"], feats=[], song_name="This Is What You Came For")),
    ("Sia - Chandelier (Official Video)", SongTitleData(authors=["Sia"], feats=[], song_name="Chandelier")),
    ("Pitbull - On The Floor (Official Music Video)\"", SongTitleData(authors=["Pitbull"], feats=[], song_name="On The Floor")),
    ("Adele - Rolling in the Deep (Official Music Video)", SongTitleData(authors=["Adele"], feats=[], song_name="Rolling in the Deep")),
    ("Natti Natasha ❌ Ozuna - Criminal [Official Video]", SongTitleData(authors=["Natti Natasha", "Ozuna"], feats=[], song_name="Criminal")),
    ("Christina Perri - A Thousand Years [Official Music Video]", SongTitleData(authors=["Christina Perri"], feats=[], song_name="A Thousand Years")),
    ("Cardi B (Official Music Video)\"", SongTitleData(authors=[], feats=[], song_name="Cardi B", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Shawn Mendes - Treat You Better", SongTitleData(authors=["Shawn Mendes"], feats=[], song_name="Treat You Better")),
    ("The Weeknd - Starboy ft. Daft Punk (Official Video) ft. Daft Punk", SongTitleData(authors=["The Weeknd"], feats=["Daft Punk"], song_name="Starboy")),
    ("Numb (Official Music Video) [4K UPGRADE] – Linkin Park", SongTitleData(authors=["Linkin Park"], feats=[], song_name="Numb", err_code=ErrCodes.AUTHOR_NAME_COULD_BE_WRONG_WARNING)),
    ("Marshmello - Alone (Official Music Video)", SongTitleData(authors=["Marshmello"], feats=[], song_name="Alone")),
    ("John Legend - All of Me (Official Video)", SongTitleData(authors=["John Legend"], feats=[], song_name="All of Me")),
    ("Meghan Trainor - All About That Bass (Official Video)", SongTitleData(authors=["Meghan Trainor"], feats=[], song_name="All About That Bass")),
    ("Bad Bunny - Mayores (Official Video)\"", SongTitleData(authors=["Bad Bunny"], feats=[], song_name="Mayores")),
    ("Gotye - Somebody That I Used To Know (feat. Kimbra) [Official Music Video]", SongTitleData(authors=["Gotye"], feats=["Kimbra"], song_name="Somebody That I Used To Know")),
    ("MAGIC! - Rude (Official Video)", SongTitleData(authors=["MAGIC!"], feats=[], song_name="Rude")),
    ("Bad Bunny - No Me Conoce (Remix)\"", SongTitleData(authors=["Bad Bunny"], feats=[], song_name="No Me Conoce")),
    ("ROSÉ & Bruno Mars - APT. (Official Music Video)", SongTitleData(authors=["ROSÉ", "Bruno Mars"], feats=[], song_name="APT.")),
    ("Ozuna - Te Bote Remix (Video Oficial)\"", SongTitleData(authors=["Ozuna"], feats=[], song_name="Te Bote Remix")),
    ("Rihanna - Diamonds", SongTitleData(authors=["Rihanna"], feats=[], song_name="Diamonds")),
    ("GoonRock\"", SongTitleData(authors=[], feats=[], song_name="GoonRock", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Adele - Someone Like You (Official Music Video)", SongTitleData(authors=["Adele"], feats=[], song_name="Someone Like You")),
    ("Bruno Mars - That’s What I Like [Official Music Video]", SongTitleData(authors=["Bruno Mars"], feats=[], song_name="That’s What I Like")),
    ("The Chainsmokers & Coldplay - Something Just Like This (Official Lyric Video)", SongTitleData(authors=["The Chainsmokers", "Coldplay"], feats=[], song_name="Something Just Like This")),
    ("Avicii - Wake Me Up (Official Video)", SongTitleData(authors=["Avicii"], feats=[], song_name="Wake Me Up")),
    ("Demi Lovato - Échame La Culpa", SongTitleData(authors=["Demi Lovato"], feats=[], song_name="Échame La Culpa")),
    ("a-ha - Take On Me (Official Video) [4K]", SongTitleData(authors=["a-ha"], feats=[], song_name="Take On Me")),
    ("Khalid - lovely", SongTitleData(authors=["Khalid"], feats=[], song_name="lovely")),
    ("Guns N' Roses - November Rain", SongTitleData(authors=["Guns N' Roses"], feats=[], song_name="November Rain")),
    ("Ariana Grande ft. Nicki Minaj - Side To Side (Official Video) ft. Nicki Minaj", SongTitleData(authors=["Ariana Grande"], feats=["Nicki Minaj"], song_name="Side To Side")),
    ("Eminem - Without Me (Official Music Video)", SongTitleData(authors=["Eminem"], feats=[], song_name="Without Me")),
    ("Fifth Harmony - Worth It (Official Video) ft. Kid Ink", SongTitleData(authors=["Fifth Harmony"], feats=["Kid Ink"], song_name="Worth It")),
    ("Los Ángeles Azules - Nunca Es Suficiente ft. Natalia Lafourcade (Live)", SongTitleData(authors=["Los Ángeles Azules"], feats=["Natalia Lafourcade"], song_name="Nunca Es Suficiente")),
    ("Imagine Dragons - Thunder", SongTitleData(authors=["Imagine Dragons"], feats=[], song_name="Thunder")),
    ("Romeo Santos - Propuesta Indecente (Official Video)", SongTitleData(authors=["Romeo Santos"], feats=[], song_name="Propuesta Indecente")),
    ("ZAYN - Dusk Till Dawn (Official Video) ft. Sia", SongTitleData(authors=["ZAYN"], feats=["Sia"], song_name="Dusk Till Dawn")),
    ("Ellie Goulding - Love Me Like You Do (Official Video)", SongTitleData(authors=["Ellie Goulding"], feats=[], song_name="Love Me Like You Do")),
    ("BLACKPINK - ‘뚜두뚜두 (DDU-DU DDU-DU)’ M/V", SongTitleData(authors=["BLACKPINK"], feats=[], song_name="뚜두뚜두", err_code=ErrCodes.TITLE_COULD_BE_WRONG_WARNING)),
    ("twenty one pilots: Heathens (from Suicide Squad: The Album) [OFFICIAL VIDEO]", SongTitleData(authors=["twenty one pilots"], feats=[], song_name="Heathens", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("Ozuna & J Balvin - China (Video Oficial)\"", SongTitleData(authors=["Ozuna", "J Balvin"], feats=[], song_name="China")),
    ("X (EQUIS) - Nicky Jam x J. Balvin | Video Oficial (Prod. Afro Bros & Jeon)", SongTitleData(authors=["Nicky Jam", "J. Balvin"], feats=[], song_name="X (EQUIS)", err_code=ErrCodes.AUTHOR_NAME_COULD_BE_WRONG_WARNING)),
    ("The Chainsmokers - Don't Let Me Down (Official Video) ft. Daya", SongTitleData(authors=["The Chainsmokers"], feats=["Daya"], song_name="Don't Let Me Down")),
    ("NATTI NATASHA - Sin Pijama (Official Video)\"", SongTitleData(authors=["NATTI NATASHA"], feats=[], song_name="Sin Pijama")),
    ("In The End [Official HD Music Video] - Linkin Park", SongTitleData(authors=["Linkin Park"], feats=[], song_name="In The End", err_code=ErrCodes.AUTHOR_NAME_COULD_BE_WRONG_WARNING)),
    ("Justin Bieber - What Do You Mean?", SongTitleData(authors=["Justin Bieber"], feats=[], song_name="What Do You Mean?")),
    ("Michael Jackson - Billie Jean (Official Video)", SongTitleData(authors=["Michael Jackson"], feats=[], song_name="Billie Jean")),
    ("The Weeknd - The Hills", SongTitleData(authors=["The Weeknd"], feats=[], song_name="The Hills")),
    ("Piso 21 & Manuel Turizo - Déjala Que Vuelva (Video Oficial)", SongTitleData(authors=["Piso 21", "Manuel Turizo"], feats=[], song_name="Déjala Que Vuelva")),
    ("TONES AND I - DANCE MONKEY (OFFICIAL VIDEO)", SongTitleData(authors=["TONES AND I"], feats=[], song_name="DANCE MONKEY")),
    ("J Balvin - Con Altura (Official Video) ft. El Guincho", SongTitleData(authors=["J Balvin"], feats=["El Guincho"], song_name="Con Altura")),
    ("Rag'n'Bone Man - Human (Official Video)", SongTitleData(authors=["Rag'n'Bone Man"], feats=[], song_name="Human")),
    ("Coldplay - Hymn For The Weekend (Official Video)", SongTitleData(authors=["Coldplay"], feats=[], song_name="Hymn For The Weekend")),
    ("Future - Life Is Good (Official Music Video) ft. Drake", SongTitleData(authors=["Future"], feats=["Drake"], song_name="Life Is Good")),
    ("J. Balvin - Ay Vamos (Official Video)", SongTitleData(authors=["J. Balvin"], feats=[], song_name="Ay Vamos", err_code=ErrCodes.AUTHOR_NAME_COULD_BE_WRONG_WARNING)),
    ("4 Non Blondes - What's Up (Official Music Video)", SongTitleData(authors=["4 Non Blondes"], feats=[], song_name="What's Up")),
    ("Nirvana - Smells Like Teen Spirit (Official Music Video)", SongTitleData(authors=["Nirvana"], feats=[], song_name="Smells Like Teen Spirit")),
    ("BLACKPINK - 'Kill This Love' M/V", SongTitleData(authors=["BLACKPINK"], feats=[], song_name="Kill This Love", err_code=ErrCodes.TITLE_COULD_BE_WRONG_WARNING)),
    ("The Weeknd - Save Your Tears (Official Music Video)", SongTitleData(authors=["The Weeknd"], feats=[], song_name="Save Your Tears")),
    ("Bruno Mars - Just The Way You Are (Official Music Video)", SongTitleData(authors=["Bruno Mars"], feats=[], song_name="Just The Way You Are")),
    # ---- freshly added ----
    ("DVRST, Øneheart - Never Leave", SongTitleData(authors=["DVRST", "Øneheart"], feats=[], song_name="Never Leave")),
    ("Элджей - Минимал", SongTitleData(authors=["Элджей"], feats=[], song_name="Минимал")),
    ("Navjaxx - Phantom Glitches (4K Official Music Video)", SongTitleData(authors=["Navjaxx"], feats=[], song_name="Phantom Glitches")),
    ("INTERWORLD \"METAMORPHOSIS\"", SongTitleData(authors=["INTERWORLD"], feats=[], song_name="METAMORPHOSIS", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
    ("AKAI (Slowed)", SongTitleData(authors=[], feats=[], song_name="AKAI", err_code=ErrCodes.SEPARATOR_MISSMATCH)),
]

def test_big_dataset():
    eq: bool = False
    processed: SongTitleData
    passed: int = 0
    for raw, expected in extensive_test:
        processed = process_title(raw)
        eq = processed == expected

        if not eq:
            print(f"got wrong input on ({raw}):")
            print("expected:")
            expected.print_data()
            print()

            print("returned:")
            processed.print_data()

            print(f"\npassed: {passed}")

        assert eq
        passed += 1


def test_error_code_check():
    assert process_title("song1 but no separator author").has_err_code()

