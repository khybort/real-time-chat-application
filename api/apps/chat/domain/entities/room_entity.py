from datetime import datetime
from typing import List


class RoomEntity(object):
    def __init__(
        self,
        id: int | None,
        name: str,
        members: List[int],
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        is_deleted: bool = False,
    ):
        self.id = id
        self.name = (name,)
        self.members = members
        self.is_deleted = (is_deleted,)
        self.created_at = (created_at,)
        self.updated_at = updated_at
