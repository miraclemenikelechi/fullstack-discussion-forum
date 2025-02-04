from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.depedencies import db_session
from utils.response import ResponseAPI, ResponseDataModel, ResponseErrorModel

from ..controllers.reply_get_all import get_thread_replies

router = APIRouter(tags=["reply"])


@router.get(
    path="/{thread_id}/comments/{comment_id}/replies",
    responses={
        200: {"model": ResponseDataModel},
        404: {"model": ResponseErrorModel},
        500: {"model": ResponseErrorModel},
    },
    status_code=200,
)
async def get_replies_to_a_comment(
    comment_id: str, thread_id: str, session: Annotated[Session, Depends(db_session)]
):
    try:
        request = await get_thread_replies(
            comment_id=comment_id, db_access=session, thread_id=thread_id
        )

        if request is not None:
            return ResponseAPI(
                data=request["replies"],
                message=f"comment `{request['id']}` replies on thread `{request['thread_id']}`",
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
