from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt

from test_notice.constants import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from test_notice.models.auth import User
from test_notice.utils import hash_password, verify_password


class AuthService():
    async def get_user_db(self, username: str):
        return await User.find_one(User.username == username)

    async def get_current_user(self, token: str) -> User:
        return await User.find_one(User.token == token)

    async def register_user(self, username: str, password: str) -> None:
        await User(
            username=username,
            hashed_password=hash_password(password)
        ).insert()

    async def authenticate_user(self, username: str, password: str):
        user = await self.get_user_db(username)

        if user is None:
            return None

        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def login(self, username: str, password: str) -> str:
        user = await self.authenticate_user(username, password)

        if user is None:
            return None

        if user.token is not None and datetime.now() < user.expires_in:
            return user.token

        access_token_expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await self.create_access_token(
            data={"sub": user.username, "role": user.role},
            expire=access_token_expires,
        )

        await user.set(
            {
                User.token: access_token,
                User.expires_in: access_token_expires
            }
        )

        return access_token

    async def create_access_token(self, data: dict, expire: Optional[timedelta] = None):
        data.update({"exp": expire})
        encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
