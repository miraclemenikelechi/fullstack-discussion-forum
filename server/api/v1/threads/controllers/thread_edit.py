from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Session

from core import crud
from utils.response import raiseHttpError

from ..models.thread import Thread, ThreadUpdateForm

if TYPE_CHECKING:
    from api.v1.user.models.user import User


async def update_a_thread(
    current_user: "User",
    db_access: Session,
    thread_id: str,
    thread_update: ThreadUpdateForm,
):
    try:
        _db_thread: Thread = crud.exists(
            arg="id", db=db_access, param=UUID(thread_id), table=Thread
        )

        if not bool(_db_thread):
            raiseHttpError(
                message=f"thread `{thread_id}` does not exist.", status_code=404
            )

        if current_user.id != _db_thread.author_id:
            raiseHttpError(
                message="you do not have authorization to edit this thread",
                status_code=403,
            )

        for _key, _value in thread_update.model_dump().items():
            setattr(_db_thread, _key, _value)

        _db_thread.updated_at = datetime.now()

        db_access.commit()
        db_access.refresh(_db_thread)

        return _db_thread.serialize()

    except Exception as error:
        raise error
