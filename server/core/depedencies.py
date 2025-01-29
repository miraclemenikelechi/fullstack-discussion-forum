from typing import Annotated, Any, Generator
from uuid import UUID

from fastapi import Depends
from fastapi.security import APIKeyHeader
from sqlmodel import Session

from authentication.model import User
from authentication.utils import verify_access_token
from utils.response import raiseHttpError

from .database import db_engine


def db_session() -> Generator[Session, Any, None]:
    with Session(db_engine) as session:
        yield session


DATABASE_SESSION_DEPENDENCY: Session = Annotated[Session, Depends(db_session)]

API_KEY_SCHEME = APIKeyHeader(name="Authorization", auto_error=True)

TOKEN_DEPENDENCY: str = Annotated[str, Depends(API_KEY_SCHEME)]


def get_token(token: TOKEN_DEPENDENCY):  # type: ignore
    print(f"API Key: {token}")

    if not token.startswith("Bearer "):
        raiseHttpError(message="invalid token format", status_code=403)

    return token[7:]


TOKEN_KEY_DEPENDENCY: str = Annotated[str, Depends(get_token)]


def get_current_user(
    session: DATABASE_SESSION_DEPENDENCY,  # type: ignore
    token: TOKEN_KEY_DEPENDENCY,  # type: ignore
):
    token_data = verify_access_token(access_token=token)
    user = session.get(User, UUID(token_data.sub))

    if not user:
        raiseHttpError(message="Invalid token", status_code=401)

    return user


CURRENT_USER_DEPENDENCY: User = Annotated[User, Depends(get_current_user)]
