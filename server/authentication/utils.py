from datetime import datetime, timedelta, timezone

import jwt
from sqlmodel import Session

from authentication.model import User
from core import crud
from core.config import appConfig


async def hash_password(password: str) -> str:
    return appConfig.PASSWORD_CONTEXT.hash(password)


async def verify_password(password: str, hashed_password: str) -> bool:
    return appConfig.PASSWORD_CONTEXT.verify(password, hashed_password)


async def create_access_token(data_to_encode):
    try:
        return jwt.encode(
            algorithm=[appConfig.ALGORITHM],
            claims={
                "exp": datetime.now(timezone.utc())
                + timedelta(minutes=appConfig.VALID_TOKEN_IN_MINUTES),
                "sub": str(data_to_encode),
            },
            key=appConfig.SECRET_KEY,
        )

    except Exception:
        return None


async def verify_access_token(access_token: str):
    try:
        return jwt.decode(
            algorithms=[appConfig.ALGORITHM],
            key=appConfig.SECRET_KEY,
            token=access_token,
        )

    except Exception:
        return None


async def authenticate_by_identifier(identifier: str, session: Session):
    email_exists = crud.exists(arg="email", db=session, table=User, param=identifier)

    username_exists = crud.exists(
        arg="username", db=session, table=User, param=identifier
    )

    if bool(email_exists):
        return email_exists

    elif bool(username_exists):
        return username_exists
