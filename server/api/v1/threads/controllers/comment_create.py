from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Session

from core import crud
from utils.response import raiseHttpError

from ..models.comment import Comment, CommentCreateForm
from ..models.thread import Thread

if TYPE_CHECKING:
    from api.v1.user.models.user import User


async def create_thread_comment(
    comment: CommentCreateForm, current_user: "User", db_access: Session, thread_id: str
):
    try:
        _thread: Thread = crud.exists(
            arg="id", db=db_access, param=UUID(thread_id), table=Thread
        )

        if not bool(_thread):
            raiseHttpError(
                message=f"thread `{thread_id}` does not exist.", status_code=404
            )

        _comment = Comment(
            author_id=current_user.id, content=comment.content, thread_id=_thread.id
        ).model_dump()

        _db_comment: Comment = crud.create(data=_comment, db=db_access, table=Comment)

        return _db_comment.serialize()

    except Exception as error:
        raise error
