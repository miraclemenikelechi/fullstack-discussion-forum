from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Session

from core import crud
from utils.response import raiseHttpError

from ..models.comment import Comment
from ..models.thread import Thread

if TYPE_CHECKING:
    from api.v1.user.models.user import User


async def delete_thread_comment(
    comment_id: str, current_user: "User", db_access: Session, thread_id: str
):
    try:
        _thread: Thread = crud.exists(
            arg="id", db=db_access, param=UUID(thread_id), table=Thread
        )

        if not bool(_thread):
            raiseHttpError(
                message=f"thread `{thread_id}` does not exist.", status_code=404
            )

        _db_comment: Comment = next(
            (comment for comment in _thread.comments if comment.id == UUID(comment_id)),
            None,
        )

        if _db_comment is None:
            raiseHttpError(
                message=f"comment `{comment_id}` does not exist on thread `{thread_id}`",
                status_code=404,
            )

        if current_user.id is not _db_comment.author_id:
            raiseHttpError(
                message="you do not have permission to delete this comment",
                status_code=403,
            )

        db_access.delete(_db_comment)
        db_access.commit()

        return _db_comment.serialize()

    except Exception as error:
        raise error
