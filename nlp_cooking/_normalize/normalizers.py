import re
import html

from .base import BaseNormalizer
from .patterns import (
    MENTION_PATTERN, URL_PATTERN, DATE_PATTERN, SPACE_PATTERN, HASHTAG_PATTERN,
    HIRAGANA_PATTERN, KANJI_POPULAR_PATTERN, KATAKANA_PATTERN, UNIT_PATTERN
    )

class NoneNormalizer(BaseNormalizer):
    def transform(self, text: str) -> str:
        return text

class LowerNormalizer(BaseNormalizer):
    def transform(self, text: str) -> str:
        return text.lower()

class UrlNormalizer(BaseNormalizer):
    def __init__(self, replace:str=""):
        self.pattern = re.compile(URL_PATTERN)
        self.replace = replace

    def transform(self, text:str) -> str:
        return re.sub(self.pattern, self.replace, text)

class HashtagNormalizer(BaseNormalizer):
    def __init__(self, replace:str=""):
        self.pattern = re.compile(HASHTAG_PATTERN)
        self.replace = replace

    def transform(self, text:str) -> str:
         return re.sub(self.pattern, self.replace, text)

class MentionNormalizer(BaseNormalizer):
    def __init__(self, replace: str=""):
        self.pattern = re.compile(MENTION_PATTERN)
        self.replace = replace

    def transform(self, text):
         return re.sub(self.pattern, self.replace, text)

class DateNormalizer(BaseNormalizer):
    def __init__(self, replace:str="0", remove_unit:bool=True) -> None:
        self.pattern = re.compile(DATE_PATTERN)
        self.replace = replace
        self.remove_unit = remove_unit

    def transform(self, text:str) -> str:
        def sub(m):
            t = m.group(0)
            t = re.sub(r'\d', self.replace, t)
            if self.remove_unit:
                return re.sub(r'[^\d]', '', t)
            else:
                return t

        return re.sub(self.pattern, sub, text)

class UnitNormalizer(BaseNormalizer):
    def __init__(self, replace:str="0", remove_unit:bool=True) -> None:
        self.pattern = re.compile(UNIT_PATTERN)
        self.replace = replace
        self.remove_unit = remove_unit

    def transform(self, text:str) -> str:
        def sub(m):
            t = m.group(0)
            t = re.sub(r'\d', self.replace, t)
            if self.remove_unit:
                return re.sub(r'[^\d]', '', t)
            else:
                return t

        return re.sub(self.pattern, sub, text)

class NumericalNormalizer(BaseNormalizer):
    def __init__(
        self,
        replace:str='0',
        ) -> None:
        self.pattern = re.compile(r'\d')

        self.replace = replace

    def transform(self, text: str) -> str:
        return re.sub(self.pattern, self.replace, text)


class SpaceNormalizer(BaseNormalizer):
    """
    ユニコードで定義されるスペースとタブ文字改行などを削除
    pattern: \f\n\r\t\v\u0020\u00a0\u2000-\u200b\u2028-\u3000
    """
    def __init__(self, replace: str=" "):
        self.pattern = re.compile(SPACE_PATTERN)
        self.replace = replace

    def transform(self, text: str) -> str:
        return re.sub(self.pattern, self.replace, text)


class EmojiNormalizer(BaseNormalizer):
    def __init__(self) -> None:
        try:
            import emoji
        except:
            raise ImportError

        self.pattern = emoji.UNICODE_EMOJI
    
    def transform(self, text:str) -> str:
        return ''.join(c for c in text if c not in self.pattern)


class CharLevelNormalizer(BaseNormalizer):
    """
    文字単位でフィルタリングを行う
    パターン:
        ひらがな: r"[\u3040-\u309F]"
        かたかな: r"[\u30A0-\u30FF]"
        漢字一般: r"[\u4E00-\u9FFF|\u3005]"
        アルファベット: r"[a-z|A-Z]"
        記号: r"[・|!|\?|～|ー|。|、|\-|\+|,|\.|=]"
        数字: r"\d"

    記号は一部記号を除いて全角を省くので先に半角に変換しておくことを推奨
    """
    def __init__(self, replace:str=" "):
        self.pattern = \
            HIRAGANA_PATTERN + "|" \
            + KATAKANA_PATTERN + "|" \
            + KANJI_POPULAR_PATTERN + "|" \
            + r"[a-z|A-Z]" + "|" \
            + r"[・|!|\?|～|ー|\-|\+|=|/]" + "|" \
            + r"[0-9]"

        self.replace = replace

    def transform(self, text:str) -> str:
        return "".join([char if re.match(self.pattern, char) else self.replace for char in text])


class NeologdnNormalizer(BaseNormalizer):
    """
    neologdnによる正規化を行う
    """
    def __init__(self, repeat:int=2):
        try:
            import neologdn
            self.func = neologdn
        except:
            raise ImportError

        self.repeat = repeat
        
    def transform(self, text: str) -> str:
        return self.func.normalize(text, repeat=self.repeat)

class HtmlUnEscapeNormalizer(BaseNormalizer):
    def transform(self, text:str) -> str:
        return html.unescape(text)
