from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.depedencies import db_session, get_current_user
from utils.response import ResponseAPI, ResponseDataModel, ResponseErrorModel

from ..controllers.comment_create import create_thread_comment
from ..models.comment import CommentCreateForm

if TYPE_CHECKING:
    from api.v1.user.models.user import User


router = APIRouter(tags=["comment"])


@router.post(
    path="/{thread_id}/comments",
    status_code=201,
    responses={
        201: {"model": ResponseDataModel},
        404: {"model": ResponseErrorModel},
        500: {"model": ResponseErrorModel},
    },
)
async def create_a_comment_in_a_thread(
    thread_id: str,
    comment_create: CommentCreateForm,
    session: Annotated[Session, Depends(db_session)],
    current_user: Annotated["User", Depends(get_current_user)],
):
    try:
        request = await create_thread_comment(
            comment=comment_create,
            current_user=current_user,
            db_access=session,
            thread_id=thread_id,
        )

        if request is not None:
            return ResponseAPI(
                data=request,
                message=f"comment `{request['id']}` created in response to thread `{request['thread_id']}`",
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
