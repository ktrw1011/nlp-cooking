import neologdn

from ..base import BaseTransform, CharLevelNormalizer

class NeologdnNormalizer(BaseTransform):
    """
    neologdnによる正規化を行う
    """
    def __init__(self, repeat:int=2):
        self.repeat = repeat
        
    def transform(self, text: str) -> str:
        return neologdn.normalize(text, repeat=self.repeat)

class CharLevelNormalizer(CharLevelNormalizer):
    def __init__(self, custom:str="", replace:str=" "):
        super().__init__(
            alphabet=True, hiragana=True, katakana=True, kanji=True, symbol=True, numerical=True, custom=custom, replace=replace)