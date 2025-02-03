from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.depedencies import db_session, get_current_user
from utils.response import ResponseAPI, ResponseDataModel, ResponseErrorModel

from ..controllers.comment_delete import delete_thread_comment

if TYPE_CHECKING:
    from api.v1.user.models.user import User


router = APIRouter(tags=["comment"])


@router.delete(
    path="/{thread_id}/comments/{comment_id}",
    status_code=200,
    responses={
        200: {"model": ResponseDataModel},
        403: {"model": ResponseErrorModel},
        404: {"model": ResponseErrorModel},
        500: {"model": ResponseErrorModel},
    },
)
async def delete_a_thread_comment(
    comment_id: str,
    current_user: Annotated["User", Depends(get_current_user)],
    session: Annotated[Session, Depends(db_session)],
    thread_id: str,
):
    try:
        request = await delete_thread_comment(
            comment_id=comment_id,
            current_user=current_user,
            db_access=session,
            thread_id=thread_id,
        )

        if request is not None:
            return ResponseAPI(
                message=f"comment `{request['id']}` has been deleted from thread `{request['thread_id']}`",
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
