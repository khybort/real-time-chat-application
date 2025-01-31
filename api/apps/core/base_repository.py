from abc import ABC, abstractmethod
from typing import TypeVar, Generic

_T = TypeVar('_T')


class BaseRepository(ABC, Generic[_T]):
    """
        Abstract generic Repository
    """
    @abstractmethod
    def get(self, id_: int) -> _T:
        raise NotImplementedError()
