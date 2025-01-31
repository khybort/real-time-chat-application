from apps.authentication.models import User
from apps.authentication.domain.services.authentication_service import AuthenticationService
from apps.authentication.domain.entities.user_entity import UserEntity
from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication.domain.repositories.user_repository import UserRepository
from django.contrib.auth import authenticate


class AuthenticationServiceImpl(AuthenticationService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, username: str, email: str, password: str) -> UserEntity:
        return self.user_repository.create_user(username, email, password)

    def login_user(self, username: str, password: str) -> UserEntity | None:
        user = authenticate(username=username, password=password)
        if not user:
            raise ValueError("Invalid credentials")
        return user.to_entity()
    
    def generate_tokens(self, user: UserEntity) -> dict:
        user: User = User.from_entity(entity=user)
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        access['username'] = user.username
        return {
            "access": str(access),
            "refresh": str(refresh),
            "user": {
                "user_id": user.id,
                "username": user.username,
                "email": user.email
            }
        }

    def refresh_access_token(self, refresh_token: str) -> dict:
        refresh = RefreshToken(refresh_token)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
