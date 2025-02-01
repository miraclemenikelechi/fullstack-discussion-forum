from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends
from sqlmodel import Session

from core.depedencies import db_session, get_current_user
from utils.response import ResponseAPI, ResponseDataModel, ResponseErrorModel

from ..controllers.thread_create import create
from ..models.thread import ThreadCreate

if TYPE_CHECKING:
    from api.v1.user.models.user import User


router = APIRouter(tags=["thread"])


@router.post(
    path="/",
    status_code=201,
    responses={
        201: {"model": ResponseDataModel},
        417: {"model": ResponseErrorModel},
        500: {"model": ResponseErrorModel},
    },
)
async def create_a_new_thread(
    data: ThreadCreate,
    session: Annotated[Session, Depends(db_session)],
    current_user: Annotated["User", Depends(get_current_user)],
):
    try:
        request = await create(
            author=current_user, data_to_create_in_db=data, db_access=session
        )

        if request is not None:
            return ResponseAPI(
                data=request,
                message=f"thread `{request['id']}` by user `{request['author_username']}` has been created!",
                status_code=201,
                success=True,
            )

    except Exception as error:
        return ResponseAPI(
            message=f"An error occured: {error}",
            status_code=500,
            success=False,
        ).response()
