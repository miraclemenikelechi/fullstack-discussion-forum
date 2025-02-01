from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.depedencies import db_session
from utils.response import ResponseAPI, ResponseDataModel, ResponseErrorModel
from ..controllers.thread_get import get_thread

router = APIRouter(tags=["thread"])


@router.get(
    path="/{thread_id}",
    status_code=302,
    responses={
        302: {"model": ResponseDataModel},
        404: {"model": ResponseErrorModel},
        500: {"model": ResponseErrorModel},
    },
)
async def get_a_thread(
    thread_id: str, session: Annotated[Session, Depends(db_session)]
):
    try:
        request = await get_thread(data_to_fetch_in_db=thread_id, db_access=session)

        if request is not None:
            return ResponseAPI(
                data=request,
                message=f"thread `{request['id']}` by `{request['author']['username']}`",
                status_code=302,
                success=True,
            )

    except HTTPException as error:
        raise error

    except Exception as error:
        return ResponseAPI(
            message=f"An error occured: {error}",
            status_code=500,
            success=False,
        ).response()
