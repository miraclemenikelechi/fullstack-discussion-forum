from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Session

from core import crud
from utils.response import raiseHttpError

from ..models.comment import Comment, CommentCreateForm
from ..models.reply import Reply
from ..models.thread import Thread

if TYPE_CHECKING:
    from api.v1.user.models.user import User


async def create_reply(
    comment_id: str,
    current_user: "User",
    db_access: Session,
    reply: CommentCreateForm,
    thread_id: str,
    parent_reply_id: str | None = None,
):
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
                message=f"comment `{comment_id}` does not exist.", status_code=404
            )

        if parent_reply_id:
            _parent_reply: Reply = crud.exists(
                arg="id", db=db_access, param=UUID(parent_reply_id), table=Reply
            )

            if not bool(_parent_reply):
                raiseHttpError(
                    message=f"parent reply `{parent_reply_id}` does not exist",
                    status_code=404,
                )

            _reply = Reply(
                author_id=current_user.id,
                comment_id=_comment.id,
                content=reply.content,
                parent_reply_id=_parent_reply.id,
            ).model_dump()

        else:
            _reply = Reply(
                author_id=current_user.id,
                comment_id=_comment.id,
                content=reply.content,
            ).model_dump()

        _db_reply: Reply = crud.create(data=_reply, db=db_access, table=Reply)

        return _db_reply.serialize()

    except Exception as error:
        raise error
