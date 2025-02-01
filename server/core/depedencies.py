from typing import Annotated, Any, Generator
from uuid import UUID

from fastapi import Depends
from fastapi.security import APIKeyHeader
from sqlmodel import Session

from utils.response import raiseHttpError

from .database import db_engine


def db_session() -> Generator[Session, Any, None]:
    with Session(db_engine) as session:
        yield session


def get_token(
    token: Annotated[str, Depends(APIKeyHeader(name="Authorization", auto_error=True))],
):
    if not token.startswith("Bearer "):
        raiseHttpError(message="invalid token format", status_code=403)

    return token[7:]


def get_current_user(
    session: Annotated[Session, Depends(db_session)],
    token: Annotated[str, Depends(get_token)],
):
    from api.v1.authentication.services.verify_access_token import verify_access_token
    from api.v1.user.models.user import User

    token_data = verify_access_token(access_token=token)
    user = session.get(User, UUID(token_data.sub))

    if not user:
        raiseHttpError(message="Invalid token", status_code=401)

    return user
