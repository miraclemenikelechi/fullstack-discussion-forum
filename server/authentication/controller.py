from sqlmodel import Session

from core import crud
from user.model import User
from utils.response import raiseHttpError


from .utils import (
    authenticate_by_identifier,
    create_access_token,
    hash_password,
    verify_password,
)


async def create_a_new_user(user_to_create_in_db, db_access: Session) -> dict[str, str]:
    try:
        username = f"{user_to_create_in_db.firstname}_+_{user_to_create_in_db.lastname}"

        username_exists = crud.exists(
            arg="username", db=db_access, table=User, param=username
        )

        email_exists = crud.exists(
            arg="email", db=db_access, table=User, param=user_to_create_in_db.email
        )

        if bool(email_exists):
            raiseHttpError(
                message=f"user `{user_to_create_in_db.email}` already exists. sign in instead.",
                status_code=400,
            )

        if bool(username_exists):
            raiseHttpError(
                message=f"user `{username}` already exists. sign in instead.",
                status_code=400,
            )

        user: User = {
            "email": user_to_create_in_db.email,
            "firstname": user_to_create_in_db.firstname,
            "lastname": user_to_create_in_db.lastname,
            "password": await hash_password(password=user_to_create_in_db.password),
            "username": username,
        }

        db_user: User = crud.create(data=user, db=db_access, table=User)

        return {
            "email": db_user.email,
            "firstname": db_user.firstname,
            "lastname": db_user.lastname,
            "username": db_user.username,
        }

    except Exception as error:
        raise error


async def sign_in_a_user(user_to_sign_in, db_access) -> dict[str, str | None]:
    try:
        user_exists: User = await authenticate_by_identifier(
            identifier=user_to_sign_in.identifier, session=db_access
        )

        if not bool(user_exists):
            raiseHttpError(
                message=f"can not get account for `{user_to_sign_in.identifier}`",
                status_code=404,
            )

        if not await verify_password(
            hashed_password=user_exists.password, password=user_to_sign_in.password
        ):
            raiseHttpError(
                message="wrong password. request new password if you forgot it already.",
                status_code=401,
            )

        return {"token": await create_access_token(data_to_encode=user_exists.id)}

    except Exception as error:
        raise error
