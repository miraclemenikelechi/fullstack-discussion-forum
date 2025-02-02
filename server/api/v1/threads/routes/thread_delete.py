from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from core.depedencies import db_session, get_current_user
from utils.response import ResponseAPI, ResponseDataModel, ResponseErrorModel

from ..controllers.thread_delete import delete_thread

if TYPE_CHECKING:
    from api.v1.user.models.user import User


router = APIRouter(tags=["thread"])


@router.delete(
    path="/{thread_id}",
    status_code=200,
    responses={
        200: {"model": ResponseDataModel},
        403: {"model": ResponseErrorModel},
        404: {"model": ResponseErrorModel},
        500: {"model": ResponseErrorModel},
    },
)
async def delete_a_thread(
    thread_id: str,
    session: Annotated[Session, Depends(db_session)],
    current_user: Annotated["User", Depends(get_current_user)],
):
    try:
        request = await delete_thread(
            current_user=current_user, db_access=session, thread_id=thread_id
        )

        if request is not None:
            return ResponseAPI(
                message=f"thread `{request['id']}` has been deleted.",
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
