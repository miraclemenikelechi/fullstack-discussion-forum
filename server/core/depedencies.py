from typing import TYPE_CHECKING, Annotated, Any, Generator, Union
from uuid import UUID

from fastapi import Depends
from fastapi.security import APIKeyHeader
from sqlmodel import Session

from utils.response import raiseHttpError

from .database import db_engine

if TYPE_CHECKING:
    from api.v1.user.models.user import User


def db_session() -> Generator[Session, Any, None]:
    """
    Dependency that yields a database session. The session is created and
    torn down for each request, and is used to interact with the database.

    Yields:
        Session: a database session
    """
    with Session(db_engine) as session:
        yield session


def get_token(
    token: Annotated[str, Depends(APIKeyHeader(name="Authorization", auto_error=True))],
) -> str:
    """
    Dependency that extracts and validates the Bearer token from the Authorization header.

    Raises an HTTPException with a 403 status code if the token is invalid or missing.

    Returns:
        str: the token without the "Bearer " prefix
    """
    if not token.startswith("Bearer "):
        raiseHttpError(message="invalid token format", status_code=403)

    return token[7:]


def get_current_user(
    session: Annotated[Session, Depends(db_session)],
    token: Annotated[str, Depends(get_token)],
) -> Union["User", None]:
    """
    Dependency that retrieves the current authenticated user from the database.

    This function uses the provided session and token to verify the user's identity.
    It decodes the token to extract the user ID and fetches the user from the database.

    Args:
        session (Session): The database session used for querying the user.
        token (str): The Bearer token extracted from the Authorization header.

    Raises:
        HTTPException: If the token is invalid or if the user does not exist, with status code 401.

    Returns:
        User: The authenticated user object.
    """

    from api.v1.authentication.services.verify_access_token import verify_access_token
    from api.v1.user.models.user import User

    token_data = verify_access_token(access_token=token)
    user: User | None = session.get(User, UUID(token_data.sub))

    if not user:
        raiseHttpError(message="Invalid token", status_code=401)

    return user
