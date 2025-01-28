from fastapi import HTTPException
from sqlmodel import Session
from core import crud
from .model import User
from utils.print import print_json
from utils.response import raiseHttpError


async def create_a_new_user(user_to_create_in_db, db_access: Session):
    try:
        is_user = crud.exists(
            arg="email", db=db_access, table=User, param=user_to_create_in_db.email
        )

        if not bool(is_user):
            raiseHttpError(
                message=f"user `{user_to_create_in_db.email}` already exists. sign in instead.",
                status_code=400,
            )

        db_user: User = {
            "email": user_to_create_in_db.email,
            "firstname": user_to_create_in_db.firstname,
            "lastname": user_to_create_in_db.lastname,
            "password": is_user,
            "username": f"{user_to_create_in_db.firstname}_+_{user_to_create_in_db.lastname}",
        }

        print()
        print_json(db_user)
        print()

        return db_user

    except Exception as error:
        raise error

    # return user_to_create_in_db.model_dump()
