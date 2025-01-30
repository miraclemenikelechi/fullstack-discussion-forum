from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from sqlmodel import Session

from core import crud
from core.config import appConfig
from api.v1.user.models import User
from utils.response import raiseHttpError

from .model import TokenPayload


async def hash_password(password: str) -> str:
    return appConfig.PASSWORD_CONTEXT.hash(password)


async def verify_password(password: str, hashed_password: str) -> bool:
    return appConfig.PASSWORD_CONTEXT.verify(password, hashed_password)


async def create_access_token(data_to_encode: str | Any) -> str | None:
    expiry_time = datetime.now(timezone.utc) + timedelta(
        minutes=appConfig.VALID_TOKEN_IN_MINUTES
    )

    to_encode = {
        "exp": expiry_time,
        "sub": str(data_to_encode),
    }

    try:
        return jwt.encode(
            to_encode,
            appConfig.SECRET_KEY,
            algorithm=appConfig.ALGORITHM,
        )

    except Exception as error:
        raiseHttpError(message=f"{error}", status_code=417)


def verify_access_token(access_token: str) -> Any | None:
    try:
        payload = jwt.decode(
            access_token,
            appConfig.SECRET_KEY,
            algorithms=[appConfig.ALGORITHM],
        )

        return TokenPayload(**payload)

    except Exception as error:
        raiseHttpError(message=f"{error}", status_code=417)


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
