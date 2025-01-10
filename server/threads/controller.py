from datetime import datetime
from typing import Any
from uuid import UUID

from sqlmodel import Session

from core import crud

from .model import Thread, Comment


async def all_threads_from_db(db_access: Session) -> list:
    try:
        return [
            data.to_dict()
            for data in crud.transact_by_param(db=db_access, table=Thread)
        ]

    except Exception as error:
        raise error


async def create_a_new_thread(
    data_to_create_in_db: dict, db_access: Session
) -> dict[str, Any]:
    db_data: Thread = {
        "author": data_to_create_in_db.author,
        "content": data_to_create_in_db.content,
        "title": data_to_create_in_db.title,
    }

    try:
        response: Thread = crud.create(data=db_data, db=db_access, table=Thread)

        return {
            "author": response.author,
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
    data_to_fetch_in_db: str, data_to_update_in_db: dict, db_access: Session
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

        for (
            key,
            value,
        ) in data_to_update_in_db.model_dump().items():
            setattr(
                response, key, value
            )  # response: Thread from db, key: what keys to update, value: values to be changed

        response.updated_at = datetime.now()

        db_access.commit()
        db_access.refresh(response)

        return {
            "content": response.content,
            "id": str(response.id),
            "title": response.title,
        }

    except Exception as error:
        raise error


async def delete_a_thread(
    data_to_fetch_in_db: str, db_access: Session
) -> dict[str, str]:
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

        db_access.delete(response)
        db_access.commit()

        return {
            "id": str(response.id),
        }

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

        return {"id": str(response.id), "comments": response.comments}

    except Exception as error:
        raise error


async def create_comment_in_a_thread(
    data_to_fetch_in_db: str, data_to_update_in_db: dict, db_access: Session
):
    try:
        is_thread: Thread = crud.exists(
            arg="id", db=db_access, param=UUID(data_to_fetch_in_db), table=Thread
        )

        if not bool(is_thread):
            raise ValueError(f"thread `{data_to_fetch_in_db}` does not exist.")

        comment_to_create: Comment = {
            "author": data_to_update_in_db.author,
            "content": data_to_update_in_db.content,
            "thread_id": is_thread.id,
        }

        created_comment: Comment = crud.create(
            data=comment_to_create, db=db_access, table=Comment
        )

        return {
            "author": created_comment.author,
            "content": created_comment.content,
            "thread_id": str(created_comment.thread_id),
            "id": str(created_comment.id),
            "created_at": str(created_comment.created_at),
            "replies": created_comment.replies,
        }

    except Exception as error:
        raise error
