from sqlmodel import Session

from core import crud
from utils.print import print_json
from utils.response import raiseHttpError

from .model import User
from .utils import hash_password


async def create_a_new_user(user_to_create_in_db, db_access: Session):
    try:
        is_user = crud.exists(
            arg="email", db=db_access, table=User, param=user_to_create_in_db.email
        )

        if bool(is_user):
            raiseHttpError(
                message=f"user `{user_to_create_in_db.email}` already exists. sign in instead.",
                status_code=400,
            )

        user: User = {
            "email": user_to_create_in_db.email,
            "firstname": user_to_create_in_db.firstname,
            "lastname": user_to_create_in_db.lastname,
            "password": await hash_password(password=user_to_create_in_db.password),
            "username": f"{user_to_create_in_db.firstname}_+_{user_to_create_in_db.lastname}",
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
