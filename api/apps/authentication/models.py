from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.authentication.domain.entities.user_entity import UserEntity

class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    
    @staticmethod
    def from_entity(entity: UserEntity) -> 'User':
        return User(
            id=entity.id,
            username=entity.username,
            email=entity.email,
            password=entity.password,
            is_active=entity.is_active,
            date_of_birth=entity.date_of_birth,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            username=self.username,
            email=self.email,
            password=self.password,
            is_active=self.is_active,
            date_of_birth=self.date_of_birth,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
