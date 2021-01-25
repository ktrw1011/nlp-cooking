import os
from typing import List, Union

from joblib import delayed, Parallel

from .base import BaseTransform

class Compose:
    """
    TextTransformオブジェクトのリストを引数に取ることで
    リストの順番に正規化を実行する
    """
    def __init__(self, transforms: List[BaseTransform], parallelize:bool=False):
        """
        Args:
            transform (List[TextTransform]): List of TextTransfrom
        """
        self.transforms = transforms
        self.parallelize = parallelize

    def __call__(self, text:Union[str, List[str]], verbose:bool=False) -> Union[str, List[str]]:
        def func(text, verbose=False) -> str:
            for normalize in self.transforms:
                text = normalize(text, verbose=verbose)
            return text

        if isinstance(text, str):
            return func(text, verbose=verbose)
        else:
            if self.parallelize:
                return Parallel(n_jobs=os.cpu_count()-2, verbose=1)([delayed(func)(text) for text in text])
            else:
                return [func(t) for t in text]