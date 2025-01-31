from typing import List
from apps.authentication.domain.entities.user_entity import UserEntity
from apps.authentication.domain.repositories.user_repository import UserRepository
from apps.authentication.domain.services.user_service import UserService


class UserServiceImpl(UserService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def get(self, id_):
        return self.user_repository.get(id_)
    def get_user_by_username(self, username) -> UserEntity:
        user = self.user_repository.get_user_by_username(username)
        if not user:
            raise ValueError(f"User with username '{username}' does not exist.")
        return user

    def create_user(self, entity: UserEntity) -> UserEntity:
        if self.user_repository.get_user_by_username(entity.username):
            raise ValueError(f"User with username '{entity.username}' already exists.")
        return self.user_repository.create_user(entity.username, entity.email, entity.password)

    def get_all_users(self) -> List[UserEntity]:
        return self.user_repository.get_all_users()

    def delete_user_by_id(self, user_id) -> bool:
        if not self.user_repository.delete_user_by_id(user_id):
            raise ValueError(f"User with id '{user_id}' does not exist.")
        return True
