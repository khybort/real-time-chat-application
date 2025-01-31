
from apps.authentication.domain.entities.user_entity import UserEntity
from apps.authentication.domain.repositories.user_repository import UserRepository
from apps.authentication.models import User

class UserRepositoryImpl(UserRepository):
    def create_user(self, username: str, email: str, password: str) -> UserEntity:
        return User.objects.create_user(username=username, email=email, password=password).to_entity()
    
    def get(self, id_: int) -> UserEntity:
        return User.objects.get(id=id_).to_entity()
    
    def get_user_by_username(self, username: str) -> UserEntity | None:
        try:
            return User.objects.get(username=username).to_entity()
        except User.DoesNotExist:
            return None

    def get_user_by_email(self, email: str) -> UserEntity | None:
        try:
            return User.objects.get(email=email).to_entity()
        except User.DoesNotExist:
            return None
    
    def get_all_users(self) -> UserEntity:
        return [user.to_entity() for user in User.objects.all()]

    def delete_user_by_id(self, user_id: int) -> bool:
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return True
        except User.DoesNotExist:
            return False
