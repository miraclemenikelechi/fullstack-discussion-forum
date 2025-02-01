from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.depedencies import db_session
from utils.response import (
    ResponseAPI,
    ResponseDataModel,
    ResponseErrorModel,
)

from ..controllers.login import sign_in_a_user
from ..models.login import UserLoginForm

router = APIRouter()


@router.post(
    path="/login",
    status_code=200,
    responses={
        200: {"model": ResponseDataModel},
        401: {"model": ResponseErrorModel},
        404: {"model": ResponseErrorModel},
        500: {"model": ResponseErrorModel},
    },
)
async def login(data: UserLoginForm, session: Annotated[Session, Depends(db_session)]):
    try:
        request = await sign_in_a_user(user_to_sign_in=data, db_access=session)

        if request is not None:
            return ResponseAPI(
                message="log in success",
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
