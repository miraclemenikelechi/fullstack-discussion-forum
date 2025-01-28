from fastapi import APIRouter, HTTPException

from authentication.controller import create_a_new_user
from core.depedencies import DATABASE_SESSION_DEPENDENCY
from utils.response import ResponseAPI, ResponseApiModel, ResponseDataModel

from .model import UserLogin, UserSignup

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login")
async def login(data: UserLogin, session: DATABASE_SESSION_DEPENDENCY):  # type: ignore
    try:
        request = await create_a_new_user()

        if request is not None:
            pass

    except Exception as error:
        return ResponseAPI(
            message=f"An error occurred: {error}",
            status_code=500,
            success=False,
        ).response()


@router.post("/signup")
async def signup(data: UserSignup, session: DATABASE_SESSION_DEPENDENCY):  # type: ignore
    try:
        request = await create_a_new_user(user_to_create_in_db=data, db_access=session)

        if request is not None:
            return ResponseAPI(
                message="Profile created successfully.",
                data=request,
                status_code=201,
                success=True,
            ).response()

    except HTTPException as error:
        raise error

    except Exception as error:
        return ResponseAPI(
            message=f"An error occurred: {error}",
            status_code=500,
            success=False,
        ).response()
