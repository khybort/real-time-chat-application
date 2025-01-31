from abc import ABC, abstractmethod
from typing import TypeVar, Generic

_T = TypeVar('_T')
class BaseService(ABC, Generic[_T]):
    """
    Abstract Generic Service
    """
    
    @abstractmethod
    def get(self, id_: int) -> _T:
        raise NotImplementedError()
    