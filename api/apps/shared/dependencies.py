from apps.chat.domain.services.room_service import RoomService
from apps.authentication.domain.repositories.user_repository import UserRepository
from apps.authentication.domain.services.authentication_service import AuthenticationService
from apps.authentication.domain.services.user_service import UserService
from apps.chat.domain.repositories.message_repository import MessageRepository
from apps.chat.domain.repositories.room_repository import RoomRepository
from apps.chat.domain.services.message_service import MessageService


def get_message_repository() -> MessageRepository:
    from apps.chat.data.repositories.message_repository_impl import MessageRepositoryImpl
    return MessageRepositoryImpl(
        room_repository=get_room_repository(),
        user_repository=get_user_repository()
    )

def get_room_repository() -> RoomRepository:
    from apps.chat.data.repositories.room_repository_impl import RoomRepositoryImpl
    return RoomRepositoryImpl()

def get_user_repository() -> UserRepository:
    from apps.authentication.data.repositories.user_repository_impl import UserRepositoryImpl
    return UserRepositoryImpl()

def get_authentication_service() -> AuthenticationService:
    from apps.authentication.data.services.authentication_service_impl import AuthenticationServiceImpl
    return AuthenticationServiceImpl(user_repository=get_user_repository())

def get_user_service() -> UserService:
    from apps.authentication.data.services.user_service_impl import UserServiceImpl
    return UserServiceImpl(get_user_repository())

def get_message_service() -> MessageService:
    from apps.chat.data.services.message_service_impl import MessageServiceImpl
    return MessageServiceImpl(message_repository=get_message_repository(),
                              room_repository=get_room_repository(),
                              user_repository=get_user_repository())

def get_room_service() -> RoomService:
    from apps.chat.data.services.room_service_impl import RoomServiceImpl
    return RoomServiceImpl(get_room_repository())
