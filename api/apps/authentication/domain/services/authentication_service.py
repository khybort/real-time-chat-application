from abc import ABC, abstractmethod
from apps.authentication.domain.entities.user_entity import UserEntity
from apps.authentication.domain.repositories.user_repository import UserRepository


class AuthenticationService(ABC):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @abstractmethod
    def register_user(self, username: str, email: str, password: str) -> UserEntity:
        raise NotImplementedError()

    @abstractmethod
    def login_user(self, username: str, password: str) -> UserEntity | None:
        raise NotImplementedError()
    
    @staticmethod
    def generate_tokens(user: UserEntity) -> dict:
        raise NotImplementedError()

    @staticmethod
    def refresh_access_token(refresh_token: str) -> dict:
        raise NotImplementedError()
