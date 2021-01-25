from typing import List

from .base import BaseNormalizer

class Compose:
    """
    TextTransformオブジェクトのリストを引数に取ることで
    リストの順番に正規化を実行する
    """
    def __init__(self, normalizers: List[BaseNormalizer]):
        """
        Args:
            transform (List[TextTransform]): List of TextTransfrom
        """
        self.normalizers = normalizers

    def __call__(self, text:str, verbose:bool=False) -> str:
        for normalize in self.normalizers:
            text = normalize(text, verbose=verbose)
        return text