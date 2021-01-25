import sys
from abc import ABCMeta, abstractmethod

from loguru import logger

logger.remove()
logger.add(
    sys.stdout,
    format="{message}"
)

class BaseTransform(metaclass=ABCMeta):

    @abstractmethod
    def transform(self, text:str) -> str:
        raise NotImplementedError

    def __call__(self, text:str, verbose:bool=False) -> str:
        cls_name = self.__class__.__name__
        if verbose:
            logger.debug(f"==={cls_name}===")
            logger.debug(f"{'[Before]:':<10}{text:<10}")
        text = self.transform(text)
        if verbose:
            logger.debug(f"{'[After]:':<10}{text:<10}")
        return text