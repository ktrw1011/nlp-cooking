from typing import List, Union
from abc import ABCMeta, abstractmethod

class BaseTokenizer(metaclass=ABCMeta):
    @abstractmethod
    def tokenize(self, text:str, pos:bool=False) -> Union[List[str], List[List[str]]]:
        pass