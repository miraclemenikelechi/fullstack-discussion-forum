from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.depedencies import db_session
from utils.response import ResponseAPI, ResponseDataModel, ResponseErrorModel

from ..controllers.comment_get_all import get_thread_comments

router = APIRouter(tags=["comment"])


@router.get(
    path="/{thread_id}/comments",
    status_code=200,
    responses={
        200: {"model": ResponseDataModel},
        404: {"model": ResponseErrorModel},
        500: {"model": ResponseErrorModel},
    },
)
async def get_all_comments_from_thread(
    thread_id: str,
    session: Annotated[Session, Depends(db_session)],
):
    try:
        request = await get_thread_comments(thread_id=thread_id, db_access=session)

        if request is not None:
            return ResponseAPI(
                data=request["comments"],
                message=f"all comments from thread `{request['id']}`.",
                status_code=200,
                success=True,
            ).response()

    except HTTPException as error:
        raise error

    except Exception as error:
        return ResponseAPI(
            message=f"An error occured: {error}",
            status_code=500,
            success=False,
        ).response()
