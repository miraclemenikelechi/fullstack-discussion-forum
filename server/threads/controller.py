from uuid import UUID

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
