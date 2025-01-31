from datetime import datetime


class MessageEntity(object):
    def __init__(
        self,
        id: int | None,
        room_id: int,
        user_id: int,
        content: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        is_deleted: bool = False
    ):
        self.id = id
        self.room_id = room_id
        self.user_id = user_id
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_deleted = is_deleted
    
    @staticmethod
    def to_dict(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'user_id': self.user_id,
            'content': self.content,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'is_deleted': self.is_deleted,
        }
    
