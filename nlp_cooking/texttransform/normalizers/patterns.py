URL_PATTERN = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
DATE_PATTERN = r"(\d{1,4})年|(\d{1,2})月|(\d{1,2})日|(\d{2,4})[/-](\d{1,2})[/-](\d{1,2})|\d{1,2}:\d{1,2}"
SPACE_PATTERN = r"[\f\n\r\t\v\u0020\u00a0\u2000-\u200b\u2028-\u3000]+"
HASHTAG_PATTERN = r"(?:#|\uFF03)([ーa-zA-Z0-9_\u3041-\u3094\u3099-\u309C\u30A1-\u30FA\u3400-\uD7FF\uFF10-\uFF19\uFF20-\uFF3A\uFF41-\uFF5A\uFF66-\uFF9E]+)"
MENTION_PATTERN = r"\@\w+:?"
HIRAGANA_PATTERN = r"[\u3040-\u309F]"
KATAKANA_PATTERN = r"[\u30A0-\u30FF]"
# 一般的な漢字(+々)(半角スペースを含む)
KANJI_POPULAR_PATTERN = r"[\u4E00-\u9FFF|\u3005]"