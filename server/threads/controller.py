from sqlmodel import Session

from core import crud

from .model import Thread


async def all_threads_from_db(db_access: Session):
    return crud.transact_by_param(db=db_access, table=Thread)


async def create_a_new_thread(data_to_create_in_db: dict, db_access: Session):
    db_data: Thread = {
        "author": data_to_create_in_db.author,
        "content": data_to_create_in_db.content,
        "title": data_to_create_in_db.title,
    }

    return crud.create(data=db_data, db=db_access, table=Thread)
