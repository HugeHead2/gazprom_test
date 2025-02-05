import os
from typing import Optional
from passlib.context import CryptContext


def get_env(name: str, default: Optional[str] = None) -> str:
    value = os.environ.get(name, None)

    if value is None and default is not None:
        return default

    if value is None and default is None:
        raise ValueError(f"Setting {name} not found. Set in configuration")

    return value


def hash_password(password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)
