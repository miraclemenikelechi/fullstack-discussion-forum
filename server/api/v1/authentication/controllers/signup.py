from sqlmodel import Session

from api.v1.user.models.user import User
from core import crud
from utils.response import raiseHttpError

from ..models.signup import UserSignupForm
from ..services.hash_password import hash_password


async def create_a_new_user(
    user_to_create_in_db: UserSignupForm, db_access: Session
) -> dict[str, str]:
    try:
        _username = (
            f"{user_to_create_in_db.firstname}_+_{user_to_create_in_db.lastname}"
        )

        _username_exists = crud.exists(
            arg="username", db=db_access, table=User, param=_username
        )

        _email_exists = crud.exists(
            arg="email", db=db_access, table=User, param=user_to_create_in_db.email
        )

        if bool(_email_exists):
            raiseHttpError(
                message=f"user `{user_to_create_in_db.email}` already exists. sign in instead.",
                status_code=409,
            )

        if bool(_username_exists):
            raiseHttpError(
                message=f"user `{_username}` already exists. sign in instead.",
                status_code=409,
            )

        _user: User = {
            "email": user_to_create_in_db.email,
            "firstname": user_to_create_in_db.firstname,
            "lastname": user_to_create_in_db.lastname,
            "password": await hash_password(password=user_to_create_in_db.password),
            "username": _username,
        }

        _db_user: User = crud.create(data=_user, db=db_access, table=User)

        return {
            "email": _db_user.email,
            "username": _db_user.username,
        }

        # return _db_user.serialize() // TODO: return serialized user

    except Exception as error:
        raise error
