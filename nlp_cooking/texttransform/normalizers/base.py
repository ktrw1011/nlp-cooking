import re
import html

from ..base import BaseTransform

from .patterns import (
    URL_PATTERN, HASHTAG_PATTERN, MENTION_PATTERN, SPACE_PATTERN, HIRAGANA_PATTERN, KANJI_POPULAR_PATTERN, KATAKANA_PATTERN
)

class NoneNormalizer(BaseTransform):
    def transform(self, text: str) -> str:
        return text

class LowerNormalizer(BaseTransform):
    def transform(self, text: str) -> str:
        return text.lower()

class UrlNormalizer(BaseTransform):
    def __init__(self, replace:str=""):
        self.pattern = re.compile(URL_PATTERN)
        self.replace = replace

    def transform(self, text:str) -> str:
        return re.sub(self.pattern, self.replace, text)

class HashtagNormalizer(BaseTransform):
    def __init__(self, replace:str=""):
        self.pattern = re.compile(HASHTAG_PATTERN)
        self.replace = replace

    def transform(self, text:str) -> str:
         return re.sub(self.pattern, self.replace, text)

class MentionNormalizer(BaseTransform):
    def __init__(self, replace: str=""):
        self.pattern = re.compile(MENTION_PATTERN)
        self.replace = replace

    def transform(self, text):
         return re.sub(self.pattern, self.replace, text)

class SpaceNormalizer(BaseTransform):
    """
    ユニコードで定義されるスペースとタブ文字改行などを削除
    pattern: \f\n\r\t\v\u0020\u00a0\u2000-\u200b\u2028-\u3000
    """
    def __init__(self, replace: str=" "):
        self.pattern = re.compile(SPACE_PATTERN)
        self.replace = replace

    def transform(self, text: str) -> str:
        return re.sub(self.pattern, self.replace, text)

class HtmlUnEscapeNormalizer(BaseTransform):
    def transform(self, text:str) -> str:
        return html.unescape(text)

class NumericalNormalizer(BaseTransform):
    def __init__(
        self,
        replace:str='0',
        ) -> None:
        self.pattern = re.compile(r'\d')

        self.replace = replace

    def transform(self, text: str) -> str:
        return re.sub(self.pattern, self.replace, text)

class EmojiNormalizer(BaseTransform):
    def __init__(self) -> None:
        try:
            import emoji
            self.pattern = emoji.UNICODE_EMOJI
        except:
            raise ImportError
    
    def transform(self, text:str) -> str:
        return ''.join(c for c in text if c not in self.pattern)


class CharLevelNormalizer(BaseTransform):
    """
    文字単位でフィルタリングを行う
    パターン:
        hiragana: r"[\u3040-\u309F]"
        kataka: r"[\u30A0-\u30FF]"
        kanji: r"[\u4E00-\u9FFF|\u3005]"
        alphabet: r"[a-z|A-Z]"
        symbol: r"[・|!|\?|～|ー|。|、|\-|\+|,|\.|=]"
        numerical: r"\d"
        custom: like [char|char] regex

    記号は一部記号を除いて全角を省くので先に半角に変換しておくことを推奨
    """
    def __init__(
        self,
        alphabet:bool=True,
        hiragana:bool=False,
        katakana:bool=False,
        kanji:bool=False,
        symbol:bool=False,
        numerical:bool=False,
        custom:str="",
        replace:str=" "
        ):

        self.pattern = ''

        if alphabet:
            self.pattern += r"[a-z|A-Z]" + "|"
        
        if hiragana:
            self.pattern += HIRAGANA_PATTERN + "|"
        
        if katakana:
            self.pattern += KATAKANA_PATTERN + "|"

        if kanji:
            self.pattern += KANJI_POPULAR_PATTERN + "|"

        if symbol:
            self.pattern += r"[・|!|\?|～|ー|\-|\+|=|/]" + "|"

        if numerical:
            self.pattern += r"[0-9]" + "|"

        if self.pattern == "":
            raise ValueError

        if custom != "":
            self.pattern += custom
        else:
            self.pattern = self.pattern[:-1]
    
        self.replace = replace

    def transform(self, text:str) -> str:
        return "".join([char if re.match(self.pattern, char) else self.replace for char in text])