from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Session

from core import crud
from utils.response import raiseHttpError

from ..models.thread import Thread

if TYPE_CHECKING:
    from api.v1.user.models.user import User


async def delete_thread(current_user: "User", db_access: Session, thread_id: str):
    try:
        _db_thread: Thread = crud.exists(
            arg="id", db=db_access, param=UUID(thread_id), table=Thread
        )

        if not bool(_db_thread):
            raiseHttpError(
                message=f"thread `{thread_id}` does not exist.",
                status_code=404,
            )

        if current_user.id != _db_thread.author_id:
            raiseHttpError(
                message="you do not have permission to delete this thread",
                status_code=403,
            )

        db_access.delete(_db_thread)
        db_access.commit()

        return _db_thread.serialize()

    except Exception as error:
        raise error
