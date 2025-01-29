from fastapi import APIRouter, HTTPException

from authentication.controller import create_a_new_user, sign_in_a_user
from core.depedencies import DATABASE_SESSION_DEPENDENCY
from utils.response import ResponseAPI, ResponseDataModel

from .model import UserLogin, UserSignup

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(path="/login", response_model=ResponseDataModel, status_code=200)
async def login(data: UserLogin, session: DATABASE_SESSION_DEPENDENCY):  # type: ignore
    print(data)

    try:
        request = await sign_in_a_user(user_to_sign_in=data, db_access=session)

        if request is not None:
            return ResponseAPI(
                message="Log in success.",
                data=request,
                status_code=200,
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


@router.post(path="/signup", response_model=ResponseDataModel, status_code=201)
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
