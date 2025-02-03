from uuid import UUID

from sqlmodel import Session

from core import crud
from utils.response import raiseHttpError

from ..models.thread import Thread


async def get_thread_comments(thread_id: str, db_access: Session):
    try:
        _thread: Thread = crud.exists(
            arg="id", db=db_access, param=UUID(thread_id), table=Thread
        )

        if not bool(_thread):
            raiseHttpError(
                message=f"thread `{thread_id}` does not exist.",
                status_code=404,
            )

        return _thread.serialize(
            exclude={"content", "created_at", "title", "updated_at"},
            include={"comments": True},
        )

    except Exception as error:
        raise error
