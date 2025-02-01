from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.depedencies import db_session
from utils.response import (
    ResponseAPI,
    ResponseDataModel,
    ResponseErrorModel,
)

from ..controllers.signup import create_a_new_user
from ..models.signup import UserSignupForm

router = APIRouter()


@router.post(
    path="/signup",
    status_code=201,
    responses={
        201: {"model": ResponseDataModel},
        302: {"model": ResponseErrorModel},
        500: {"model": ResponseErrorModel},
    },
)
async def signup(
    data: UserSignupForm, session: Annotated[Session, Depends(db_session)]
):
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
