# URL
URL_PATTERN = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
# 日付
DATE_PATTERN = r"(\d{1,4})年|(\d{1,2})月|(\d{1,2})日|(\d{2,4})[/-](\d{1,2})[/-](\d{1,2})|\d{1,2}:\d{1,2}"
# 空白
SPACE_PATTERN = r"[\f\n\r\t\v\u0020\u00a0\u2000-\u200b\u2028-\u3000]+"
# ハッシュタグパターン
HASHTAG_PATTERN = r"[#|＃](\w+)"
# メンション
MENTION_PATTERN = r"\@\w+:?"
# ひらがな
HIRAGANA_PATTERN = r"[\u3040-\u309F]"
# カタカナ
KATAKANA_PATTERN = r"[\u30A0-\u30FF]"
# 一般的な漢字(+々)(半角スペースを含む)
KANJI_POPULAR_PATTERN = r"[\u4E00-\u9FFF|\u3005]"

class UNIT_LIST:
    # 物理量
    PHYSICAL_UNITS = [
        # グラム
        'kg',
        'g',
        'mg',
        
        # リットル
        'l',
        'ml',

        # ワット
        'w',
        # ボルト
        'v',
        
        # 温度
        '℃',
        '度',
    ]

    # 通貨
    CURENCY_UNITS_LIST = [
        '兆円',
        '億円',
        '万円',
        '千円',
        '円',
    ]

    # 時間
    TIME_UNITS = [
        '年',
        '月',
        'か月'
        'カ月'
        'ケ月',
        'ヶ月'
        '週',
        '日',
        '時',
        '分',
        '秒',
    ]

    # その他
    OTHER_UNITS = [
        'パック',
        'シーズン',
        '杯',
        '番',
        '本',
        '巻',
        '杯',
        '話',
        '線',
        '歳',
        '才',
        '名',
        '票',
        '作',
        '点',
        '人',
    ]

PREFFIX_UNITS = '|'.join([
    '第',
    'シーズン',
])

SUFFIX_UNITS = '|'.join(UNIT_LIST.PHYSICAL_UNITS + UNIT_LIST.CURENCY_UNITS_LIST + UNIT_LIST.TIME_UNITS + UNIT_LIST.OTHER_UNITS)

UNIT_PATTERN = fr"({PREFFIX_UNITS})?[\d\.,]+({SUFFIX_UNITS})"