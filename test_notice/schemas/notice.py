from typing import Optional
from pydantic import BaseModel


class PatchCreateNoticeSchema(BaseModel):
    title: str
    body: str
