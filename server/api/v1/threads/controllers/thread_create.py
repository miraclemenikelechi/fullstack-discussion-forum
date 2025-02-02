from typing import TYPE_CHECKING, Any

from sqlmodel import Session

from core import crud

from ..models.thread import Thread, ThreadCreate

if TYPE_CHECKING:
    from api.v1.user.models.user import User


async def create(
    data_to_create_in_db: ThreadCreate, db_access: Session, author: "User"
) -> dict[str, Any]:
    _thread = Thread(
        author_id=author.id,
        content=data_to_create_in_db.content,
        title=data_to_create_in_db.title,
    ).model_dump()

    try:
        _db_thread: Thread = crud.create(data=_thread, db=db_access, table=Thread)

        return {
            "author": _db_thread.author,
            "comments": _db_thread.comments,
            "content": _db_thread.content,
            "id": str(_db_thread.id),
            "title": _db_thread.title,
        }

    except Exception as error:
        raise error
