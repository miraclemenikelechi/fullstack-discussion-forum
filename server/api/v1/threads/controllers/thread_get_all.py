from sqlmodel import Session

from core import crud

from ..models.thread import Thread


async def get_all(db_access: Session) -> list:
    try:
        return [
            data.to_dict()
            for data in crud.transact_by_param(db=db_access, table=Thread)
        ]

    except Exception as error:
        raise error
