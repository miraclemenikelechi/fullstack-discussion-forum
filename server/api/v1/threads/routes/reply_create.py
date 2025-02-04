from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.depedencies import db_session, get_current_user
from utils.response import ResponseAPI, ResponseDataModel, ResponseErrorModel

from ..controllers.reply_create import create_reply
from ..models.comment import CommentCreateForm

if TYPE_CHECKING:
    from api.v1.user.models.user import User


router = APIRouter(tags=["reply"])


@router.post(
    path="/{thread_id}/comments/{comment_id}/replies",
    responses={
        201: {"model": ResponseDataModel},
        404: {"model": ResponseErrorModel},
        500: {"model": ResponseErrorModel},
    },
    status_code=201,
)
async def create_reply_to_comment(
    comment_id: str,
    current_user: Annotated["User", Depends(get_current_user)],
    reply_create: CommentCreateForm,
    session: Annotated[Session, Depends(db_session)],
    thread_id: str,
    parent_reply_id: str | None = None,
):
    try:
        request = await create_reply(
            comment_id=comment_id,
            current_user=current_user,
            db_access=session,
            parent_reply_id=parent_reply_id,
            reply=reply_create,
            thread_id=thread_id,
        )

        if request is not None:
            return ResponseAPI(
                data=request,
                message=f"reply `{request['id']}` created in response to comment `{request['comment_id']}`",
                status_code=201,
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
