from beanie import PydanticObjectId
import bson
from fastapi import HTTPException, status
from test_notice.services.notice import NoticeService


async def get_notice_service():
    return NoticeService()


async def validate_notice_id(notice_id: str):
    try:
        PydanticObjectId(notice_id)
        return notice_id
    except bson.errors.InvalidId as ex:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid notice id",
            headers={"WWW-Authenticate": "Bearer"},
        ) from ex
