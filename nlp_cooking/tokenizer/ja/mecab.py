from typing import Union, List, Optional

import MeCab
import regex
import jaconv

from ..base import BaseTokenizer

def _is_hiragana_katakana(word) -> bool:
    if regex.search(r"^[\p{Hiragana}|\p{Katakana}|ー]+$", word):
        return True
    else:
        return False

class MeCabTokenizer(BaseTokenizer):
    def __init__(self, mecabrc_path:Optional[str]=None, dict_path:Optional[str]=None) -> None:
        super().__init__()

        if mecabrc_path is not None:
            self.mecabrc_path = mecabrc_path
        else:
            self.mecabrc_path = "/usr/local/etc/mecabrc"

        if dict_path is not None:
            self.dict_path = dict_path
        else:
            self.dict_path = "/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd"

        self._init_tokenizer()

    def _init_tokenizer(self):
        self.mecab = MeCab.Tagger(f'-r {self.mecabrc_path} -d {self.dict_path}')
        self.mecab.parse("")

    def __getstate__(self):
        # シリアライズできないのでpickle化のエラーを回避するための属性削除
        state = self.__dict__.copy()
        del state['mecab']
        return state

    def __setstate__(self, state):
        # クラス内の辞書に従ってインスタンスを復元する
        self.__dict__.update(state)
        self._init_tokenizer()

    def tokenize(self, text:str, pos:bool=False) -> Union[List[str], List[List[str]]]:
        res = []
        for word_attr in self.mecab.parse(text).strip().split('\n')[:-1]:
            # 正規化されていないと稀に一部の文字でエラーが発生する
            try:
                token, pos_attr = word_attr.split('\t')
            except ValueError:
                continue

            pos_attr = pos_attr.split(',')
            pos_attr, yomi = pos_attr[:-3], pos_attr[-2]
            pos_attr.append(yomi)
            if pos:
                res.append([token, pos_attr])
            else:
                res.append(token)
        return res
    
    def yomi(self, word:str) -> str:
        yomi = []
        attrs = self.tokenize(word, pos=True)
        for token, attr in attrs:
            if _is_hiragana_katakana(token):
                # 形態素がひらがなorカタカナの場合にはそのまま
                yomi.append(jaconv.hira2kata(token))
            else:
                yomi.append(attr[-1])
        return ''.join(yomi)
