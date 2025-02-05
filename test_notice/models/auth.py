from datetime import datetime
from typing import Optional

from beanie import Document

from test_notice.models.enums import UserRoles


class User(Document):
    username: str
    hashed_password: str
    token: Optional[str] = None
    expires_in: Optional[datetime] = None
    role: UserRoles = UserRoles.user
