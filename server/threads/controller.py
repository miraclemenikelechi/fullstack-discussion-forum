from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Session

from core import crud

from .model import Thread


async def all_threads_from_db(db_access: Session):
    try:
        return [
            data.to_dict()
            for data in crud.transact_by_param(db=db_access, table=Thread)
        ]

    except Exception as error:
        raise error


async def create_a_new_thread(data_to_create_in_db: dict, db_access: Session):
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


async def get_a_thread(data_to_fetch_in_db: str, db_access: Session):
    try:
        response: Thread = crud.transact_by_param(
            db=db_access,
            arg="id",
            table=Thread,
            op="==",
            param=UUID(data_to_fetch_in_db),
            single=True,
        )

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
):
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
        ) in data_to_update_in_db.dict().items():
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


async def delete_a_thread(data_to_fetch_in_db: str, db_access: Session):
    try:
        pass

    except Exception as error:
        raise error
