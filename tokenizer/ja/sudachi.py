from typing import Union, List
import sudachipy
import sudachipy.dictionary as sudachi_dict

from ..base import BaseTokenizer

class SudachiTokenizer(BaseTokenizer):
    def __init__(self, mode: str='c'):
        super().__init__()
        self.mode = mode
        self._init_tokenizer()

    def _init_tokenizer(self):
        self.obj = sudachi_dict.Dictionary().create()

        if self.mode.lower() == 'c':
            self.mode_obj = sudachipy.tokenizer.Tokenizer.SplitMode.C
        elif self.mode.lower() == 'b':
            self.mode_obj = sudachipy.tokenizer.Tokenizer.SplitMode.B
        elif self.mode.lower() == 'a':
            self.mode_obj = sudachipy.tokenizer.Tokenizer.SplitMode.A
        else:
            ValueError

    def __getstate__(self):
        # シリアライズできないのでpickle化のエラーを回避するための属性削除
        state = self.__dict__.copy()
        del state['obj'], state['mode_obj']
        return state

    def __setstate__(self, state):
        # クラス内の辞書に従ってインスタンスを復元する
        self.__dict__.update(state)
        self._init_tokenizer()
    
    def tokenize(self, text, pos=False) -> Union[List[str], List[List[str]]]:
        if pos:
            res = []
            for m in self.obj.tokenize(text, self.mode_obj):
                pos_attr = m.part_of_speech().copy()
                pos_attr.append(m.reading_form())
                res.append([m.surface(), pos_attr])
            return res
        else:
            return [m.surface() for m in self.obj.tokenize(text, self.mode_obj)]

    def normalize(self, tokens: Union[str, List[str]]) -> Union[str, List[str]]:
        if isinstance(tokens, str):
            return self.obj.tokenize(tokens, self.mode_obj)[0].normalized_form()
        else:
            return [self.obj.tokenize(token, self.mode_obj)[0].normalized_form() for token in tokens]