from typing import TYPE_CHECKING

from sqlmodel import Session

from ..models.thread import Thread, ThreadCreate

if TYPE_CHECKING:
    from api.v1.user.models.user import User


async def create(
    data_to_create_in_db: ThreadCreate, db_access: Session, author: "User"
):
    _thread: Thread = {
        "author_id": str(author.id),
        "content": data_to_create_in_db.content,
        "title": data_to_create_in_db.title,
    }
    print()
    print(_thread)
    print()
