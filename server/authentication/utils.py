from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from sqlmodel import Session

from core import crud
from core.config import appConfig

from .model import User


async def hash_password(password: str) -> str:
    return appConfig.PASSWORD_CONTEXT.hash(password)


async def verify_password(password: str, hashed_password: str) -> bool:
    return appConfig.PASSWORD_CONTEXT.verify(password, hashed_password)


async def create_access_token(data_to_encode) -> str | None:
    try:
        return jwt.encode(
            algorithm=appConfig.ALGORITHM,
            key=appConfig.SECRET_KEY,
            payload={
                "exp": datetime.now(timezone.utc)
                + timedelta(minutes=appConfig.VALID_TOKEN_IN_MINUTES),
                "sub": str(data_to_encode),
            },
        )

    except Exception as error:
        print(f"error: {error}")
        return None


async def verify_access_token(access_token: str) -> Any | None:
    try:
        return jwt.decode(
            algorithms=[appConfig.ALGORITHM],
            key=appConfig.SECRET_KEY,
            token=access_token,
        )

    except Exception:
        return None


async def authenticate_by_identifier(identifier: str, session: Session) -> User | None:
    email_exists: User = crud.exists(
        arg="email", db=session, table=User, param=identifier
    )

    username_exists: User = crud.exists(
        arg="username", db=session, table=User, param=identifier
    )

    if bool(email_exists):
        return email_exists

    elif bool(username_exists):
        return username_exists
