from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status

from test_notice.dependencies.auth import get_current_admin_user
from test_notice.dependencies.notice import get_notice_service
from test_notice.models.auth import User
from test_notice.models.notice import Notice
from test_notice.services.notice import NoticeService


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.get("/notices")
async def get_notices(
    current_admin: Annotated[User, Depends(get_current_admin_user)],
    service: Annotated[NoticeService, Depends(get_notice_service)]
) -> List[Notice]:
    return await service.get_notices()


@router.get("/notices/{notice_id}")
async def get_notice(
    current_admin: Annotated[User, Depends(get_current_admin_user)],
    service: Annotated[NoticeService, Depends(get_notice_service)],
    notice_id: str
) -> Notice:
    return await service.get_notice(notice_id)


@router.patch("/notices/{notice_id}/restore")
async def restore_notice(
    current_admin: Annotated[User, Depends(get_current_admin_user)],
    service: Annotated[NoticeService, Depends(get_notice_service)],
    notice_id: str
) -> bool:
    restored = await service.restore_notice(notice_id)

    if not restored:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return restored


@router.get("/users/{user_id}/notices")
async def get_user_notices(
    current_admin: Annotated[User, Depends(get_current_admin_user)],
    service: Annotated[NoticeService, Depends(get_notice_service)],
    user_id: str
) -> List[Notice]:
    return await service.get_notices(Notice.user_id == user_id)
