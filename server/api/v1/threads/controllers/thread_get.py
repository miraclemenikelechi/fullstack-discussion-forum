from typing import Any
from uuid import UUID

from sqlmodel import Session

from core import crud
from utils.response import raiseHttpError

from ..models.thread import Thread


async def get_thread(data_to_fetch_in_db: str, db_access: Session) -> dict[str, Any]:
    try:
        _thread: Thread = crud.transact_by_param(
            db=db_access,
            arg="id",
            table=Thread,
            op="==",
            param=UUID(data_to_fetch_in_db),
            single=True,
        )

        if not bool(_thread):
            raiseHttpError(
                message=f"thread `{data_to_fetch_in_db}` does not exist.",
                status_code=404,
            )

        return _thread.serialize(
            include={"author": True},
            exclude={"author": {"firstname", "lastname", "password", "registered_at"}},
        )

    except Exception as error:
        raise error
