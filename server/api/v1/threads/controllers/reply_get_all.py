from uuid import UUID

from sqlmodel import Session

from core import crud
from utils.response import raiseHttpError

from ..models.thread import Thread
from ..models.comment import Comment


async def get_thread_replies(comment_id: str, db_access: Session, thread_id: str):
    try:
        _thread: Thread = crud.exists(
            arg="id", db=db_access, param=UUID(thread_id), table=Thread
        )

        if not bool(_thread):
            raiseHttpError(
                message=f"thread `{thread_id}` does not exist.", status_code=404
            )

        _comment: Comment = next(
            (comment for comment in _thread.comments if comment.id == UUID(comment_id)),
            None,
        )

        if not bool(_comment):
            raiseHttpError(
                message=f"comment `{comment_id}` does not exist on thread `{_thread.id}`",
                status_code=404,
            )

        return _comment.serialize()

    except Exception as error:
        raise error
