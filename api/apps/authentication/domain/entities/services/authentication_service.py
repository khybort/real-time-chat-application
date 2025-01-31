from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication.repositories.user_repository_impl import UserRepository
from django.contrib.auth import authenticate
from apps.authentication.models import User


class AuthenticationService:
    def __init__(self, user_repository: UserRepository = UserRepository()):
        self.user_repository = user_repository

    def register_user(self, username: str, email: str, password: str) -> User:
        user = self.user_repository.create_user(username, email, password)
        return user

    def login_user(self, username: str, password: str) -> User | None:
        user = authenticate(username=username, password=password)
        if not user:
            raise ValueError("Invalid credentials")
        return user
    
    @staticmethod
    def generate_tokens(user: User) -> dict:
        """
        Kullanıcı için access ve refresh token oluşturur.
        """
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        access['username'] = user.username
        return {
            "access": str(access),
            "refresh": str(refresh),
        }

    @staticmethod
    def refresh_access_token(refresh_token: str) -> dict:
        """
        Refresh token kullanarak yeni bir access token oluşturur.
        """
        refresh = RefreshToken(refresh_token)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
