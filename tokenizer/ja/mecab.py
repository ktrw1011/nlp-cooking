from typing import Union, List

import MeCab

from ..base import BaseTokenizer

class MeCabTokenizer(BaseTokenizer):
    def __init__(self, dict_path: str="/usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd") -> None:
        super().__init__()

        self.dict_path = dict_path
        self._init_tokenizer()

    def _init_tokenizer(self):
        self.mecab = MeCab.Tagger(f'-d {self.dict_path}')
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
            token, pos_attr = word_attr.split('\t')
            pos_attr = pos_attr.split(',')
            pos_attr, yomi = pos_attr[:-3], pos_attr[-2]
            pos_attr.append(yomi)
            if pos:
                res.append([token, pos_attr])
            else:
                res.append(token)
        return res
