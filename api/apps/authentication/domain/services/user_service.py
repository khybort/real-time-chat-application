from abc import abstractmethod
from typing import List
from apps.authentication.domain.repositories.user_repository import UserRepository
from apps.authentication.domain.entities.user_entity import UserEntity
from apps.core.base_service import BaseService


class UserService(BaseService[UserEntity]):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @abstractmethod
    def get_user_by_username(self, username) -> UserEntity:
        raise NotImplementedError()

    @abstractmethod
    def create_user(self, entity: UserEntity):
        raise NotImplementedError()

    @abstractmethod
    def get_all_users(self) -> List[UserEntity]:
        raise NotImplementedError()

    @abstractmethod
    def delete_user_by_id(self, user_id) -> bool:
        raise NotImplementedError()
