from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from test_notice.models.auth import User
from test_notice.models.enums import UserRoles
from test_notice.services.auth import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/oauth/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    user = await AuthService().get_current_user(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_admin_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    user = await AuthService().get_current_user(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.role != UserRoles.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be admin",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_auth_service():
    return AuthService()
