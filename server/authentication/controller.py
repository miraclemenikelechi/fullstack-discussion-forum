from sqlmodel import Session

from core import crud
from utils.print import print_json
from utils.response import raiseHttpError


from .model import User
from .utils import authenticate_by_identifier, hash_password, verify_password


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


async def sign_in_a_user(user_to_sign_in, db_access):
    try:
        user_exists = await authenticate_by_identifier(
            identifier=user_to_sign_in.identifier, session=db_access
        )

        if not bool(user_exists):
            raiseHttpError(
                message=f"user `{user_to_sign_in.identifier}` does not exist",
                status_code=404,
            )

        if not await verify_password(
            hashed_password=user_exists.password, password=user_to_sign_in.password
        ):
            raiseHttpError(message="invalid credentials", status_code=401)

    except Exception as error:
        raise error


# print()
# print_json(db_user.to_dict())
# print()
