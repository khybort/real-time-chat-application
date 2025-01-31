from datetime import datetime


class UserEntity(object):
    def __init__(self, id: int | None,
                 username: str,
                 email: str,
                 password: str,
                 is_active: bool = True,
                 date_of_birth: datetime | None = None,
                 created_at: datetime | None = None,
                 updated_at: datetime | None = None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password,
        self.is_active = is_active,
        self.date_of_birth = date_of_birth,
        self.created_at = created_at,
        self.updated_at = updated_at
        
    