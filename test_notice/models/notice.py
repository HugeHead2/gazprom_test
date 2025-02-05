from beanie import Document
from pydantic import Field


class Notice(Document):
    title: str = Field(default=None, max_length=256)
    body: str = Field(default=None, max_length=65536)
    user_id: str
    is_deleted: bool = False
