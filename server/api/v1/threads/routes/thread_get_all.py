from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from core.depedencies import db_session
from utils.response import ResponseAPI, ResponseDataModel, ResponseErrorModel

from ..controllers.thread_get_all import get_all

router = APIRouter(tags=["thread"])


@router.get(
    path="/",
    responses={
        200: {"model": ResponseDataModel},
        500: {"model": ResponseErrorModel},
    },
    status_code=200,
)
async def get_all_threads(session: Annotated[Session, Depends(db_session)]):
    try:
        request = await get_all(db_access=session)

        if request is not None:
            return ResponseAPI(
                data=request,
                message="all threads",
                status_code=200,
                success=True,
            ).response()

    except Exception as error:
        return ResponseAPI(
            message=f"An error occured: {error}",
            status_code=500,
            success=False,
        ).response()
