from datetime import datetime
from typing import Any
from uuid import UUID

from sqlmodel import Session

from core import crud
from user.model import User
from utils.response import raiseHttpError

from .model import Comment, Reply, Thread


async def all_threads_from_db(db_access: Session) -> list:
    try:
        return [
            data.to_dict()
            for data in crud.transact_by_param(db=db_access, table=Thread)
        ]

    except Exception as error:
        raise error


async def create_a_new_thread(
    data_to_create_in_db: dict, db_access: Session, thread_author: User
) -> dict[str, Any]:
    db_data: Thread = {
        "author": str(thread_author.id),
        "content": data_to_create_in_db.content,
        "title": data_to_create_in_db.title,
    }

    try:
        response: Thread = crud.create(data=db_data, db=db_access, table=Thread)

        return {
            "author_id": response.author,
            "author_username": thread_author.username,
            "comments": response.comments,
            "content": response.content,
            "id": str(response.id),
            "title": response.title,
        }

    except Exception as error:
        raise error


async def get_a_thread(data_to_fetch_in_db: str, db_access: Session) -> dict[str, Any]:
    try:
        response: Thread = crud.transact_by_param(
            db=db_access,
            arg="id",
            table=Thread,
            op="==",
            param=UUID(data_to_fetch_in_db),
            single=True,
        )

        if response is None:
            raise ValueError(f"thread `{data_to_fetch_in_db}` does not exist.")

        return {
            "author": response.author,
            "comments": response.comments,
            "content": response.content,
            "created_at": response.created_at,
            "id": str(response.id),
            "title": response.title,
            "updated_at": response.updated_at,
        }

    except Exception as error:
        raise error


async def update_a_thread(
    data_to_fetch_in_db: str,
    data_to_update_in_db: dict,
    db_access: Session,
    current_user: User,
) -> dict[str, Any]:
    try:
        db_thread: Thread = crud.exists(
            arg="id", db=db_access, param=UUID(data_to_fetch_in_db), table=Thread
        )

        if not bool(db_thread):
            raise raiseHttpError(
                message=f"thread `{data_to_fetch_in_db}` does not exist.",
                status_code=404,
            )

        if current_user.id is not db_thread.author:
            raiseHttpError(
                message="you do not have permission to edit this thread",
                status_code=403,
            )

        for (
            key,
            value,
        ) in data_to_update_in_db.model_dump().items():
            setattr(
                db_thread, key, value
            )  # db_thread: Thread from db, key: what keys to update, value: values to be changed

        db_thread.updated_at = datetime.now()

        db_access.commit()
        db_access.refresh(db_thread)

        return {
            "content": db_thread.content,
            "id": str(db_thread.id),
            "title": db_thread.title,
        }

    except Exception as error:
        raise error


async def delete_a_thread(
    data_to_fetch_in_db: str, db_access: Session, current_user: User
) -> dict[str, str]:
    try:
        db_thread: Thread = crud.exists(
            arg="id", db=db_access, param=UUID(data_to_fetch_in_db), table=Thread
        )

        if not bool(db_thread):
            raise raiseHttpError(
                message=f"thread `{data_to_fetch_in_db}` does not exist.",
                status_code=404,
            )

        if current_user.id is not db_thread.author:
            raiseHttpError(
                message="you do not have permission to delete this thread",
                status_code=403,
            )

        db_access.delete(db_thread)
        db_access.commit()

        return {"id": str(db_thread.id)}

    except Exception as error:
        raise error


async def get_all_comments_from_a_thread(
    data_to_fetch_in_db: str, db_access: Session
) -> dict[str, Any]:
    try:
        response: Thread = crud.transact_by_param(
            db=db_access,
            arg="id",
            table=Thread,
            op="==",
            param=UUID(data_to_fetch_in_db),
            single=True,
        )

        if response is None:
            raise ValueError(f"thread `{data_to_fetch_in_db}` does not exist.")

        return {
            "id": str(response.id),
            "comments": [comment.to_dict() for comment in response.comments],
        }

    except Exception as error:
        raise error


async def create_comment_in_a_thread(
    data_to_fetch_in_db: str, data_to_update_in_db: dict, db_access: Session
) -> dict[str, Any]:
    try:
        is_thread: Thread = crud.exists(
            arg="id", db=db_access, param=UUID(data_to_fetch_in_db), table=Thread
        )

        if not bool(is_thread):
            raise ValueError(f"thread `{data_to_fetch_in_db}` does not exist.")

        comment: Comment = {
            "author": data_to_update_in_db.author,
            "content": data_to_update_in_db.content,
            "thread_id": is_thread.id,
        }

        db_comment: Comment = crud.create(data=comment, db=db_access, table=Comment)

        return {
            "author": db_comment.author,
            "content": db_comment.content,
            "thread_id": str(db_comment.thread_id),
            "id": str(db_comment.id),
            "created_at": str(db_comment.created_at),
            "replies": db_comment.replies,
        }

    except Exception as error:
        raise error


async def delete_comment_from_a_thread(
    data_to_fetch_in_db: str, data_to_transact_with_in_db: str, db_access: Session
) -> dict[str, str]:
    try:
        is_thread: Thread = crud.exists(
            arg="id", db=db_access, param=UUID(data_to_fetch_in_db), table=Thread
        )

        if not bool(is_thread):
            raise ValueError(f"thread `{data_to_fetch_in_db}` does not exist.")

        db_comment: Comment = next(
            (
                comment
                for comment in is_thread.comments
                if comment.id == UUID(data_to_transact_with_in_db)
            ),
            None,
        )

        if db_comment is None:
            raise ValueError(
                f"comment `{data_to_transact_with_in_db}` does not exist on thread `{data_to_fetch_in_db}`."
            )

        db_access.delete(db_comment)
        db_access.commit()

        return {"id": str(db_comment.id), "thread_id": str(is_thread.id)}

    except Exception as error:
        raise error


async def get_all_replies_from_comment_in_a_thread(
    data_to_fetch_in_db: str, data_to_transact_with_in_db: str, db_access: Session
):
    try:
        is_thread: Thread = crud.exists(
            arg="id", db=db_access, param=UUID(data_to_fetch_in_db), table=Thread
        )

        if not bool(is_thread):
            raise ValueError(f"thread `{data_to_fetch_in_db}` does not exist.")

        db_comment: Comment = next(
            (
                comment
                for comment in is_thread.comments
                if comment.id == UUID(data_to_transact_with_in_db)
            ),
            None,
        )

        if db_comment is None:
            raise ValueError(
                f"comment `{data_to_transact_with_in_db}` does not exist on thread `{data_to_fetch_in_db}`."
            )

        return {
            "id": str(db_comment.id),
            "replies": [reply.to_dict() for reply in db_comment.replies],
            "thread_id": str(is_thread.id),
        }

    except Exception as error:
        raise error


async def create_a_reply_to_comment_in_a_thread(
    data_to_fetch_in_db: str,
    data_to_transact_with_in_db: str,
    data_to_update_in_db: dict,
    db_access: Session,
):
    try:
        is_thread: Thread = crud.exists(
            arg="id", db=db_access, param=UUID(data_to_fetch_in_db), table=Thread
        )

        if not bool(is_thread):
            raise ValueError(f"thread `{data_to_fetch_in_db}` does not exist.")

        db_comment: Comment = next(
            (
                comment
                for comment in is_thread.comments
                if comment.id == UUID(data_to_transact_with_in_db)
            ),
            None,
        )

        if db_comment is None:
            raise ValueError(
                f"comment `{data_to_transact_with_in_db}` does not exist on thread `{data_to_fetch_in_db}`."
            )

        reply: Reply = {
            "author": data_to_update_in_db.author,
            "content": data_to_update_in_db.content,
            "comment_id": db_comment.id,
        }

        db_reply: Reply = crud.create(data=reply, db=db_access, table=Reply)

        return {
            "author": db_reply.author,
            "comment_id": str(db_reply.comment_id),
            "content": db_reply.content,
            "created_at": str(db_reply.created_at),
            "id": str(db_reply.id),
            "updated_at": str(db_reply.updated_at),
        }

    except Exception as error:
        raise error


async def delete_a_reply_from_comment_in_a_thread(
    data_to_fetch_in_db: str, data_to_transact_with_in_db: str, db_access: Session
):
    try:
        is_comment: Comment = crud.exists(
            arg="id", db=db_access, param=UUID(data_to_fetch_in_db), table=Comment
        )

        if not bool(is_comment):
            raise ValueError(f"comment `{data_to_fetch_in_db}` does not exist.")

        db_reply: Reply = next(
            (
                reply
                for reply in is_comment.replies
                if reply.id == UUID(data_to_transact_with_in_db)
            ),
            None,
        )

        if db_reply is None:
            raise ValueError(
                f"reply `{data_to_transact_with_in_db}` does not exist on comment `{data_to_fetch_in_db}' in thread `{str(is_comment.thread_id)}`"
            )

        db_access.delete(db_reply)
        db_access.commit()

        return {
            "comment_id": str(is_comment.id),
            "id": str(db_reply.id),
            "thread_id": str(is_comment.thread_id),
        }

    except Exception as error:
        raise error
