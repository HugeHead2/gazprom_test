from beanie import PydanticObjectId
from test_notice.models.notice import Notice
from test_notice.schemas.notice import PatchCreateNoticeSchema


class NoticeService():
    async def get_notices(self, *args, **kwargs):
        return await Notice.find_many(*args, **kwargs).to_list()

    async def get_notice(self, notice_id: str, *args, **kwargs):
        return await Notice.find_one(
            Notice.id == PydanticObjectId(notice_id),
            *args,
            **kwargs
        )

    async def create_notice(self, user_id: str, schema: PatchCreateNoticeSchema) -> Notice:
        new_notice = await Notice(
            title=schema.title,
            body=schema.body,
            user_id=user_id
        ).insert()

        return new_notice

    async def patch_notice(self, notice_id: str, schema: PatchCreateNoticeSchema, *args, **kwargs) -> Notice:
        notice = await Notice.find_one(Notice.id == PydanticObjectId(notice_id), *args, **kwargs)

        if notice is None:
            return None

        await notice.set({
            Notice.title: schema.title,
            Notice.body: schema.body
        })

        return notice

    async def delete_notice(self, notice_id, *args, **kwargs) -> bool:
        notice = await Notice.find_one(Notice.id == PydanticObjectId(notice_id), *args, **kwargs)

        if notice is None:
            return False

        await notice.set({
            Notice.is_deleted: True
        })

        return True

    async def restore_notice(self, notice_id, *args, **kwargs) -> bool:
        notice = await Notice.find_one(Notice.id == PydanticObjectId(notice_id), *args, **kwargs)

        if notice is None:
            return False

        await notice.set({
            Notice.is_deleted: False
        })

        return True

