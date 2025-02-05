from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorDatabase

from test_notice.models.auth import User
from test_notice.models.notice import Notice
from test_notice.utils import get_env


async def init_mongo():
    client = AsyncIOMotorClient(
        host=get_env("MONGODB_HOST"),
        port=int(get_env("MONGODB_PORT", default="27017")),
        username=get_env("MONGODB_USERNAME"),
        password=get_env("MONGODB_PASSWORD"),
    )

    await init_beanie(
            database=AsyncIOMotorDatabase(client, "Authorization"),
            document_models=[
                User,
                Notice,
            ],
            multiprocessing_mode=True,
        )
