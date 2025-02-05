from typing import Annotated, List, Literal

from fastapi import APIRouter, Depends, HTTPException, status

from test_notice.dependencies.auth import get_current_user
from test_notice.dependencies.notice import get_notice_service, validate_notice_id
from test_notice.models.auth import User
from test_notice.models.enums import UserRoles
from test_notice.models.notice import Notice
from test_notice.schemas.notice import PatchCreateNoticeSchema
from test_notice.services.notice import NoticeService


router = APIRouter(
    prefix="/notices",
    tags=["notices"]
)


@router.get("/")
async def notices_list(
        current_user: Annotated[User, Depends(get_current_user)],
        service: Annotated[NoticeService, Depends(get_notice_service)]
) -> List[Notice]:
    return await service.get_notices(Notice.user_id == str(current_user.id), Notice.is_deleted == False)


@router.put("/")
async def create_notice(
        current_user: Annotated[User, Depends(get_current_user)],
        service: Annotated[NoticeService, Depends(get_notice_service)],
        schema: PatchCreateNoticeSchema
) -> Notice:
    return await service.create_notice(str(current_user.id), schema)


@router.get("/{notice_id}")
async def get_notice(
        current_user: Annotated[User, Depends(get_current_user)],
        service: Annotated[NoticeService, Depends(get_notice_service)],
        notice_id: Annotated[str, Depends(validate_notice_id)]
) -> Notice:
    notice = await service.get_notice(
        notice_id,
        Notice.user_id == str(current_user.id),
        Notice.is_deleted == False
    )

    if notice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return notice


@router.patch("/{notice_id}")
async def patch_notice(
        current_user: Annotated[User, Depends(get_current_user)],
        service: Annotated[NoticeService, Depends(get_notice_service)],
        schema: PatchCreateNoticeSchema,
        notice_id: Annotated[str, Depends(validate_notice_id)]
) -> Notice:
    new_notice = await service.patch_notice(
        notice_id,
        schema,
        Notice.user_id == str(current_user.id),
        Notice.is_deleted == False
    )

    if new_notice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return new_notice


@router.delete("/{notice_id}")
async def delete_notice(
        current_user: Annotated[User, Depends(get_current_user)],
        service: Annotated[NoticeService, Depends(get_notice_service)],
        notice_id: str
) -> Literal[True]:
    deleted = await service.delete_notice(
        notice_id,
        Notice.user_id == str(current_user.id),
        Notice.is_deleted == False
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return deleted
