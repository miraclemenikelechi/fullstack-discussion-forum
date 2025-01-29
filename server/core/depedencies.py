from typing import Annotated, Any, Generator
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from authentication.model import User
from authentication.utils import verify_access_token
from utils.response import raiseHttpError

from .config import appConfig
from .database import db_engine


def db_session() -> Generator[Session, Any, None]:
    with Session(db_engine) as session:
        yield session


DATABASE_SESSION_DEPENDENCY: Session = Annotated[Session, Depends(db_session)]

TOKEN_URL: str = f"{appConfig.CURRENT_API_URL}/auth/login"
OAUTH2_SCHEME: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)

TOKEN_DEPENDENCY: str = Annotated[str, Depends(OAUTH2_SCHEME)]


def get_current_user(session: DATABASE_SESSION_DEPENDENCY, token: TOKEN_DEPENDENCY):  # type: ignore
    token_data = verify_access_token(access_token=token)
    user = session.get(User, UUID(token_data.sub))

    if not user:
        raiseHttpError(message="Invalid token", status_code=401)

    return user


CURRENT_USER_DEPENDENCY: User = Annotated[User, Depends(get_current_user)]
