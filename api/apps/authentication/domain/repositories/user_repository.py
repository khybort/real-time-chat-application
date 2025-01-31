from abc import abstractmethod
from typing import List
from apps.authentication.domain.entities.user_entity import UserEntity
from apps.core.base_repository import BaseRepository

class UserRepository(BaseRepository[UserEntity]):
    
    @abstractmethod
    def create_user(self, username: str, email: str, password: str) -> UserEntity:
        raise NotImplementedError()
    
    @abstractmethod
    def get_user_by_username(self, username: str) -> UserEntity | None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_all_users(self) -> List[UserEntity]:
        raise NotImplementedError()
    
    @abstractmethod
    def delete_user_by_id(self, user_id) -> bool:
        raise NotImplementedError()
