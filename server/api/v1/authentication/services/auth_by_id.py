from sqlmodel import Session

from api.v1.user.models.user import User
from core import crud


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
