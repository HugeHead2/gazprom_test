from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status

from test_notice.dependencies.auth import get_auth_service
from test_notice.services.auth import AuthService

router = APIRouter(
    prefix="/oauth",
    tags=["oauth"]
)


@router.post("/register")
async def register_user(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    service: Annotated[AuthService, Depends(get_auth_service)]
) -> None:
    await service.register_user(username, password)


@router.post("/token")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    service: Annotated[AuthService, Depends(get_auth_service)]
):
    token = await service.login(username, password)

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": token,
        "token_type": "Bearer"
    }
